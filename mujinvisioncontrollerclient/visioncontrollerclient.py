# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 MUJIN Inc
# Mujin vision controller client for bin picking task

# system imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Dict, List, Optional, Tuple, Union, Any # noqa: F401 # used in type check
    import mujinvisiontypes as types

# mujin imports
from mujinplanningclient import zmqclient, zmqsubscriber, TimeoutError
from . import VisionControllerClientError, VisionControllerTimeoutError
from . import json
from . import zmq
from . import ugettext as _

# logging
from logging import getLogger
log = getLogger(__name__)

class VisionControllerClient(object):
    """Mujin Vision Controller client for binpicking tasks.
    """

    _ctx = None  # type: Optional[zmq.Context] # zeromq context to use
    _ctxown = None  # type: Optional[zmq.Context]
    # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # type: Optional[str] # hostname of vision controller
    commandport = None  # type: Optional[int] # command port of vision controller
    configurationport = None  # type: Optional[int] # configuration port of vision controller, usually command port + 2
    statusport = None  # type: Optional[int] # status publishing port of vision manager, usually command port + 3

    _commandsocket = None  # type: Optional[zmqclient.ZmqClient]
    _configurationsocket = None  # type: Optional[zmqclient.ZmqClient]
    
    _callerid = None # the callerid to send to vision
    _checkpreemptfn = None # called periodically when in a loop
    
    _subscriber = None # an instance of ZmqSubscriber, used for subscribing to the state
    _slaverequestid = None # slave request id used when calling vision manager master to route to the correct vision manager slave
    
    def __init__(self, hostname='127.0.0.1', commandport=7004, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None, slaverequestid=None):
        # type: (str, int, Optional[zmq.Context], Optional[Callable], float, Optional[str], Optional[str]) -> None
        """Connects to vision server, initializes vision server, and sets up parameters

        Args:
            hostname (str, optional): e.g. visioncontroller1
            commandport (int, optional): e.g. 7004
            ctx (zmq.Context, optional): The ZMQ context
            checkpreemptfn (Callable, optional): Called periodically when in a loop. A function handle to preempt the socket. The function should raise an exception if a preempt is desired.
            reconnectionTimeout (float, optional): Sets the "timeout" parameter of the ZmqSocketPool instance
            slaverequestid (str, optional): slave request id used when calling vision manager master to route to the correct vision manager slave
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2
        self.statusport = commandport + 1
        self._callerid = callerid
        self._checkpreemptfn = checkpreemptfn
        self._slaverequestid = slaverequestid
        
        if ctx is None:
            self._ctxown = zmq.Context()
            self._ctxown.linger = 100
            self._ctx = self._ctxown
        else:
            self._ctx = ctx
        
        self._commandsocket = zmqclient.ZmqClient(self.hostname, commandport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
        self._configurationsocket = zmqclient.ZmqClient(self.hostname, self.configurationport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
    
    def __del__(self):
        self.Destroy()
    
    def Destroy(self):
        # type: () -> None
        self.SetDestroy()

        if self._commandsocket is not None:
            try:
                self._commandsocket.Destroy()
                self._commandsocket = None
            except Exception as e:
                log.exception('problem destroying commandsocket: %s', e)

        if self._configurationsocket is not None:
            try:
                self._configurationsocket.Destroy()
                self._configurationsocket = None
            except Exception as e:
                log.exception('problem destroying configurationsocket: %s', e)

        if self._subscriber is not None:
            self._subscriber.Destroy()
            self._subscriber = None
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
                self._ctxown = None
            except Exception as e:
                log.exception('problem destroying ctxown: %s', e)

        self._ctx = None

    def SetDestroy(self):
        # type: () -> None
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()
    
    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True, blockwait=True, slaverequestid=None):
        # type: (Dict, bool, float, bool, bool, bool) -> Optional[Dict]
        if self._callerid:
            command['callerid'] = self._callerid
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
        if slaverequestid is not None:
            command['slaverequestid'] = slaverequestid
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt, blockwait=blockwait)
        if blockwait and not fireandforget:
            return self._ProcessResponse(response, command=command, recvjson=recvjson)
        return response

    def _ProcessResponse(self, response, command=None, recvjson=True):
        # type: (Optional[Dict], Optional[Dict], bool) -> Optional[Dict]
        
        def _HandleError(response):
            # type: (Optional[Dict]) -> None
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('desc', ''), errortype=response['error'].get('type', ''))
            else:
                raise VisionControllerClientError(_('Got unknown error from vision manager: %r') % response['error'], errortype='unknownerror')
        if recvjson:
            if 'error' in response:
                _HandleError(response)
        else:
            if len(response) > 0 and response[0] == '{' and response[-1] == '}':
                response = json.loads(response)
                if 'error' in response:
                    _HandleError(response)
            if len(response) == 0:
                raise VisionControllerClientError(_('Vision command %(command)s failed with empty response %(response)r') % {'command': command, 'response': response}, errortype='emptyresponseerror')
        return response

    def _WaitForResponse(self, recvjson=True, timeout=None, command=None):
        """Waits for a response for a command sent on the RPC socket.

        Args:
            recvjson (bool, optional): If the response is json, should be the same value with `recvjson` of `SendAndReceive`. (Default: True)
            timeout (float, optional): (Default: None)
            command (dict, optional): Command sent to sensorbridge (Default: None)

        Raises:
            VisionControllerClientError
        """
        commandName = ''
        if command is not None and isinstance(command, dict):
            commandName = command.get('command') or ''

        if not self._commandsocket.IsWaitingReply():
            raise VisionControllerClientError(_('Waiting on command "%(commandName)s" when wait signal is not on') % {
                'commandName': commandName,
            }, errortype='invalidwait')
        
        try:
            response = self._commandsocket.ReceiveCommand(timeout=timeout, recvjson=recvjson)
        except TimeoutError as e:
            raise VisionControllerTimeoutError(_('Timed out after %.03f seconds to get response message %s from %s:%d: %s') % (timeout, commandName, self.hostname, self.commandport, e), errortype='timeout')
        except Exception as e:
            raise VisionControllerClientError(_('Problem receiving response from the last vision manager async call %s: %s') % (commandName, e), errortype='unknownerror')
        return self._ProcessResponse(response, command=command, recvjson=recvjson)

    def IsWaitingResponse(self):
        """Returns whether the client is waiting for response on the command socket, and caller should call WaitForResponse().
        """
        return self._commandsocket.IsWaitingReply()

    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True, recvjson=True, slaverequestid=None):
        # type: (Dict, bool, float, bool, bool) -> Optional[Dict]
        if self._callerid:
            configuration['callerid'] = self._callerid
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
        if slaverequestid is not None:
            configuration['slaverequestid'] = slaverequestid
        response = self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        if not fireandforget:
            return self._ProcessResponse(response, command=configuration, recvjson=recvjson)
        return response
    
    def TerminateSlaves(self, slaverequestids, timeout=None, fireandforget=None, checkpreempt=True):
        """terminate slaves with specific slaverequestids
        """
        return self.SendConfig({'command':'TerminateSlaves', 'slaverequestids':slaverequestids}, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)
    
    def CancelSlaves(self, slaverequestids, timeout=None, fireandforget=None, checkpreempt=True):
        """cancel the current commands on the slaves with specific slaverequestids
        """
        return self.SendConfig({'command':'cancel', 'slaverequestids':slaverequestids}, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)
    
    #
    # Commands
    #

    def StartObjectDetectionTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (Optional[types.SystemState], Optional[types.visionTaskObjectDetectionParametersSchema], float, Dict) -> Optional[Dict]
        """Starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.

        Args:
            taskId (str, optional): If specified, the specific taskId to use
            systemState (types.SystemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
            visionTaskParameters (types.visionTaskObjectDetectionParametersSchema or dict): Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {'command': 'StartObjectDetectionTask'}  # type: Dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartContainerDetectionTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (Optional[types.SystemState], Optional[types.visionTaskContainerDetectionParametersSchema], float, Dict) -> Optional[Dict]
        """Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.

        Args:
            taskId (str, optional): If specified, the specific taskId to use
            systemState (types.SystemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
            visionTaskParameters (types.visionTaskContainerDetectionParametersSchema or dict): Parameters for the container detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting container detection thread...')
        command = {'command': 'StartContainerDetectionTask'}  # type: Dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartVisualizePointCloudTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0):
        # type: (Optional[types.SystemState], Optional[types.visionTaskVisualizePointCloudParametersSchema], float) -> Optional[Dict]
        """Start point cloud visualization thread to sync camera info from the mujin controller and send the raw camera point clouds to mujin controller
        
        Args:
            taskId (str, optional): If specified, the specific taskId to use
            systemState (types.SystemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
            visionTaskParameters (types.visionTaskVisualizePointCloudParametersSchema or dict): Parameters for the point cloud visualization task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.
        """
        log.verbose('Starting visualize pointcloud thread...')
        command = {'command': 'StartVisualizePointCloudTask'}  # type: Dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StopTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, removeTask=False, fireandforget=False, timeout=2.0):
        """Stops a set of tasks that meet the filter criteria

        Args:
            taskId (str, optional): If specified, the specific taskId to stop
            taskIds (list[str], optional): If specified, a list of taskIds to stop
            taskType (str, optional): The task type to stop.
            taskTypes (list[str], optional): If specified, a list of task types to stop.
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            waitForStop (bool, optional): If True, then wait for task to stop, otherwise just trigger it to stop, but do not wait (Default: True)
            removeTask (bool, optional): If True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            dict: A dictionary with the structure:

            isStopped (bool): true, if the specific taskId or set of tasks with a specific taskType(s) is stopped
        """
        command = {
            'command': 'StopTask',
            'waitForStop': waitForStop,
            'removeTask': removeTask,
        }
        if taskTypes is not None:
            command['taskTypes'] = taskTypes
        if taskId is not None:
            command['taskId'] = taskId
        if taskIds is not None:
            command['taskIds'] = taskIds
        if taskType is not None:
            command['taskType'] = taskType
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        return self._ExecuteCommand(command, timeout=timeout, fireandforget=fireandforget)

    def ResumeTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, fireandforget=False, timeout=2.0):
        """Resumes a set of tasks that meet the filter criteria

        Args:
            taskId (str, optional): If specified, the specific taskId to resume
            taskIds (list[str], optional): If specified, a list of taskIds to resume
            taskType (str, optional): The task type to resume.
            taskTypes (list[str], optional): If specified, a list of task types to resume
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            waitForStop (bool, optional): DEPRECATED. This is unused. (Default: True)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            dict: A dictionary with the structure:

            taskIds (list[str]): List of taskIds that have been resumed
        """
        command = {
            'command': 'ResumeTask',
            'waitForStop': waitForStop,
        }
        if taskId is not None:
            command['taskId'] = taskId
        if taskIds is not None:
            command['taskIds'] = taskIds
        if taskType is not None:
            command['taskType'] = taskType
        if taskTypes is not None:
            command['taskTypes'] = taskTypes
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        return self._ExecuteCommand(command, timeout=timeout, fireandforget=fireandforget)

    def BackupVisionLog(self, cycleIndex, sensorTimestamps=None, fireandforget=False, timeout=2.0):
        # type: (str, Optional[List], bool, float) -> Optional[Dict]
        """Backs up the vision log for a given cycle index and/or sensor timestamps.

        Args:
            cycleIndex (str): Unique cycle index string for tracking, backing up, and differentiating cycles.
            sensorTimestamps (list[float], optional): The sensor timestamps to backup
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'BackupDetectionLogs',
            'cycleIndex': cycleIndex,
        }
        if sensorTimestamps is not None:
            command['sensorTimestamps'] = sensorTimestamps
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def GetLatestDetectedObjects(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0, slaverequestid=None):
        """Gets the latest detected objects.

        Args:
            taskId (str, optional): If specified, the taskId to retrieve the detected objects from.
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            taskType (str, optional): The task type to retrieve the detected objects from.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            dict: a list of the latest detection results, having the structure
            A dictionary with the structure:

            detectionResults (dict): A dictionary with the structure:

                cycleIndex (str): Unique cycle index string for tracking, backing up, and differentiating cycles.
                detectedObjects (list)
                detectionResultState (dict)
                imageEndTimeStampMS (int)
                imageStartTimestampMS (int)
                locationName (str)
                pointCloudId (str)
                resultTimestampMS (int)
                sensorSelectionInfos (list[dict])
                statsUID (str)
                targetUpdateName (str)
                taskId (str)
        """
        command = {
            'command': 'GetLatestDetectedObjects',
        }
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout, slaverequestid=slaverequestid)

    def GetLatestDetectionResultImages(self, taskId=None, cycleIndex=None, taskType=None, newerThanResultTimestampMS=0, sensorSelectionInfo=None, metadataOnly=False, imageTypes=None, limit=None, blockwait=True, timeout=2.0, slaverequestid=None):
        """Gets the latest detected result images.

        Args:
            taskId (str, optional): If specified, the taskId.
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            taskType (str, optional): The task type.
            newerThanResultTimestampMS (int, optional): If specified, starttimestamp of the image must be newer than this value in milliseconds. (Default: 0)
            sensorSelectionInfo (dict, optional):
            metadataOnly (bool, optional): Default: False
            imageTypes (list, optional): Mujin image types
            limit (int, optional):
            blockwait (bool, optional): (Default: True)
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            str: Raw image data
        """
        command = {
            'command': 'GetLatestDetectionResultImages',
            'newerThanResultTimestampMS': newerThanResultTimestampMS,
            'metadataOnly': metadataOnly,
        }
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        if sensorSelectionInfo is not None:
            command['sensorSelectionInfo'] = sensorSelectionInfo
        if imageTypes is not None:
            command['imageTypes'] = imageTypes
        if limit is not None:
            command['limit'] = limit
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False, blockwait=blockwait, slaverequestid=slaverequestid)

    def WaitForGetLatestDetectionResultImages(self, timeout=2.0):
        """Waits for response to GetLatestDetectionResultImages command

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        return self._WaitForResponse(recvjson=False, timeout=timeout)


    def GetDetectionHistory(self, timestamp, timeout=2.0):
        # type: (int, float) -> Any
        """Gets detection result with given timestamp (sensor time)

        Args:
            timestamp (int): Unix timestamp in milliseconds
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            str: Binary blob of detection data
        """
        command = {
            'command': 'GetDetectionHistory',
            'timestamp': timestamp,
        }
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)
    
    def GetVisionStatistics(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0):
        """Gets the latest vision stats.

        Args:
            taskId (str, optional): If specified, the taskId.
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            taskType (str, optional): The task type.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            dict: a list of all currently active vision task statistics. Each task statistics have the following structure
            A dictionary with the structure:

            visionStatistics (dict): A dictionary with the structure:

                cycleIndex (str): Unique cycle index string for tracking, backing up, and differentiating cycles.
                taskId (str): The taskId.
                taskType (str): The task type.
                taskStartTimeMS (int)
                totalDetectionTimeMS (int)
                totalDetectionCount (int)
                totalGetImagesCount (int)
                targetURIs (int)
                detectionHistory (list)
        """
        command = {
            'command': 'GetVisionStatistics',
        }
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)
    
    def Ping(self, timeout=2.0, fireandforget=False):
        # type: (float) -> Optional[Dict]
        """Sends a ping to the visionmanager.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'Ping',
        }
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def SetLogLevel(self, componentLevels, timeout=2.0):
        """Sets the log level for the visionmanager.

        Args:
            componentLevels (dict): A dictionary of component names and their respective log levels.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'setloglevel',
            'componentLevels': componentLevels,
        }
        return self._SendConfiguration(command, timeout=timeout)

    def Cancel(self, timeout=2.0):
        # type: (float) -> Optional[Dict]
        """Cancels the current command.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'cancel',
        }
        return self._SendConfiguration(command, timeout=timeout)

    def Quit(self, timeout=2.0):
        # type: (float) -> Optional[Dict]
        """Quits the visionmanager.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'quit',
        }
        return self._SendConfiguration(command, timeout=timeout)

    def GetTaskStateService(self, taskId=None, cycleIndex=None, taskType=None, timeout=4.0):
        """Gets the task state of the visionmanager.

        Args:
            taskId (str, optional): If specified, the taskId to retrieve the task state of.
            cycleIndex (str, optional): Unique cycle index string for tracking, backing up, and differentiating cycles.
            taskType (str, optional): The taskType for which the status was requested
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 4.0)

        Returns:
            dict: A dictionary with the structure:

            visionTaskParameters (dict): describes the task specific parameters if present, eg. detection params, execution verification params..
            initializeTaskMS (int): timestamp at which the task was received and initialized , in ms (linux epoch)
            isStopTask (bool): True if task is currently running
            scenepk (str): scene file name
            taskId (str): The taskId for which the status was requested
            taskStatus (str): status of the task
            taskStatusMessage (str): describes the task status
            taskType (str): The task type for which the status was requested
        """
        command = {
            'command': 'GetTaskState',
        }
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)

    def GetPublishedStateService(self, timeout=4.0):
        """Gets the published state of the visionmanager.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 4.0)
        """
        response = self._ExecuteCommand({"command": "GetPublishedState"}, timeout=timeout)
        return response

    # for subscribing to the state
    def GetPublishedServerState(self, timeout=None):
        if self._subscriber is None:
            self._subscriber = zmqsubscriber.ZmqSubscriber('tcp://%s:%d' % (self.hostname, self.statusport), ctx=self._ctx)
        rawState = self._subscriber.SpinOnce(timeout=timeout, checkpreemptfn=self._checkpreemptfn)
        if rawState is not None:
            return json.loads(rawState)
        return None

    def GetPublishedState(self, timeout=2.0):
        """Return most recent published state. If publishing is disabled, then will return None
        """
        serverState = self.GetPublishedServerState(timeout=timeout)
        if serverState is not None and 'slavestates' in serverState:
            return serverState['slavestates'].get('slaverequestid-%s' % self._slaverequestid)
        return None

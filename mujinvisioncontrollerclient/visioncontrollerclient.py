# -*- coding: utf-8 -*-
# Copyright (C) 2023 MUJIN Inc
# Mujin vision controller client for bin picking task
# AUTO GENERATED FILE! DO NOT EDIT!


# system imports
import os
import os.path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Tuple, Union, Literal # noqa: F401 # used in type check
    import mujinvisiontypes as types

# mujin imports
from mujinplanningclient import zmqclient, zmqsubscriber, TimeoutError
from . import _, json, zmq, six, VisionControllerClientError, VisionControllerTimeoutError

# logging
import logging
log = logging.getLogger(__name__)

class VisionClient(object):
    """Mujin Vision Controller client for the binpicking tasks."""

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
    _slaverequestid = None # slave request id used when calling vision manager master to route to the correct vision slave

    _deprecated = None # used to mark arguments as deprecated (set argument default value to this)

    def __init__(self, hostname='127.0.0.1', commandport=7004, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None, slaverequestid=None):
        # type: (str, int, Optional[zmq.Context], Optional[Callable], float, Optional[str], Optional[str]) -> None
        """Connects to the vision server, initializes vision server, and sets up parameters

        Args:
            hostname (str, optional): e.g. visioncontroller1
            commandport (int, optional): e.g. 7004
            ctx (zmq.Context, optional): The ZMQ context
            checkpreemptfn (Callable, optional): Called periodically when in a loop. A function handle to preempt the socket. The function should raise an exception if a preempt is desired.
            reconnectionTimeout (float, optional): Sets the "timeout" parameter of the ZmqSocketPool instance
            callerid (str, optional): The callerid to send to vision.
            slaverequestid (str, optional): Slave request id used when calling vision manager master to route to the correct vision slave.
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
        self._validationQueue = None
        self._lastCommandCall = None
        if os.environ.get('MUJIN_VALIDATE_APIS', 'false').lower() == 'true':
            from mujinapispecvalidation.apiSpecServicesValidation import ValidationQueue, ParameterIgnoreRule
            try:
                from visionapi.spec import visionControllerClientSpec
            except ImportError:
                log.warn('Could not import spec, using JSON instead')
                installDir = os.environ.get('MUJIN_INSTALL_DIR', 'opt')
                specExportPath = os.path.join(installDir, 'share', 'apispec', 'en_US.UTF-8', 'visionapi.spec.visionControllerClientSpec.json')
                visionControllerClientSpec = json.load(open(specExportPath))
            ignoreParametersConfigs = [ParameterIgnoreRule(parameter=p) for p in ['command', 'callerid', 'sendTimeStamp', 'queueid', 'slaverequestid']]
            self._validationQueue = ValidationQueue(apiSpec=visionControllerClientSpec, parameterIgnoreRules=ignoreParametersConfigs, clientName='VisionControllerClient', logDirectory=os.environ.get('MUJIN_LOG_DIR', '/var/log/mujin'))

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
        if self._validationQueue:
            self._validationQueue.StopValidationProcess()

    def SetDestroy(self):
        # type: () -> None
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()

    def GetSlaveRequestId(self):
        # type: () -> Optional[str]
        return self._slaverequestid

    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True, blockwait=True, slaverequestid=None):
        # type: (dict, bool, float, bool, bool, bool, Optional[str]) -> Any
        """Executes given command.

        Args:
            configuration (dict): Command in json format.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            recvjson (bool, optional): If True, a json is received.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
            blockwait (bool, optional): If True, will block and wait until function is done. Otherwise user will have to call _ProcessResponse on their own. (Default: True)
        """
        assert self._commandsocket is not None
        if self._callerid:
            command['callerid'] = self._callerid
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
        if slaverequestid is not None:
            command['slaverequestid'] = slaverequestid
        if self._validationQueue:
            self._lastCommandCall = command
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt, blockwait=blockwait)
        if blockwait and not fireandforget:
            return self._ProcessResponse(response, command=command, recvjson=recvjson)
        return response

    def _ProcessResponse(self, response, command=None, recvjson=True):
        # type: (Any, Optional[dict], bool) -> Any

        def _HandleError(response):
            # type: (dict) -> None
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('desc', ''), errortype=response['error'].get('type', ''))
            else:
                raise VisionControllerClientError(_('Got unknown error from vision manager: %r') % response['error'], errortype='unknownerror')
        if recvjson:
            if 'error' in response:
                _HandleError(response)
            elif self._validationQueue:
                if command is None:
                    log.warn('Cannot validate! Got response=' + str(response))
                else:
                    self._validationQueue.Add(command['command'], command, response)
        else:
            if len(response) > 0 and response[0] == '{' and response[-1] == '}':
                response = json.loads(response)
                if 'error' in response:
                    _HandleError(response)
                elif self._validationQueue:
                    if command is None:
                        log.warn('Cannot validate! Got response=' + str(response))
                    else:
                        self._validationQueue.Add(command['command'], command, response)
            if len(response) == 0:
                raise VisionControllerClientError(_('Vision command %(command)s failed with empty response %(response)r') % {'command': command, 'response': response}, errortype='emptyresponseerror')
        return response

    def _WaitForResponse(self, recvjson=True, timeout=None, command=None):
        # type: (bool, Optional[float], Optional[dict]) -> dict
        """Waits for a response for a command sent on the RPC socket.

        Args:
            recvjson (bool, optional): If the response is json, should be the same value with `recvjson` of `SendAndReceive`. (Default: True)
            timeout (float, optional): (Default: None)
            command (dict, optional): Command sent to sensorbridge (Default: None)

        Raises:
            VisionControllerClientError
        """
        assert self._commandsocket is not None
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
        # type: () -> bool
        """Returns whether the client is waiting for response on the command socket, and caller should call WaitForResponse().
        """
        assert self._commandsocket is not None
        return self._commandsocket.IsWaitingReply()

    def WaitForGetLatestDetectionResultImages(self, timeout=2.0):
        # type: (float) -> dict
        """Waits for response to GetLatestDetectionResultImages command

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        return self._WaitForResponse(recvjson=False, timeout=timeout)

    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True, recvjson=True, slaverequestid=None):
        # type: (dict, bool, float, bool, bool, Optional[str]) -> Any
        """Sends a configuration command.

        Args:
            configuration (dict): Configuration to send in json format.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
            recvjson (bool, optional): If True, a json is received.
        """
        assert self._configurationsocket is not None
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

    #
    # Commands (generated from the spec)
    #

    def TerminateSlaves(self, slaverequestids, timeout=None, fireandforget=False, checkpreempt=True):
        # type: (list[str], Optional[float], bool, bool) -> Optional[types.TerminateSlavesReturns]
        """
        Terminate slaves with specific slaverequestids.

        Args:
            slaverequestids:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: None)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
            checkpreempt: If the preempt function should be checked during execution. (Default: True)
        """
        command = {
            'command': 'TerminateSlaves',
            'slaverequestids': slaverequestids,
        }  # type: dict[str, Any]
        return self._SendConfiguration(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)

    def CancelSlaves(self, slaverequestids, timeout=None, fireandforget=False, checkpreempt=True):
        # type: (list[str], Optional[float], bool, bool) -> Optional[Any]
        """
        Terminate slaves with specific slaverequestids.

        Args:
            slaverequestids:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: None)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
            checkpreempt: If the preempt function should be checked during execution. (Default: True)
        """
        command = {
            'command': 'cancel',
            'slaverequestids': slaverequestids,
        }  # type: dict[str, Any]
        return self._SendConfiguration(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)

    def StartObjectDetectionTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (Optional[str], Optional[types.StartObjectDetectionTaskParametersSystemState], Optional[types.StartObjectDetectionTaskParametersVisionTaskParameters], float, Optional[Any]) -> Optional[types.StartObjectDetectionTaskReturns]
        """
        Starts detection thread to continuously detect objects. The vision server will send detection results directly to mujin controller.

        Args:
            taskId: If specified, the specific taskId to use. (Default: None)
            systemState: The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details. (Default: None)
            visionTaskParameters: Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile. (Default: None)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            Returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {
            'command': 'StartObjectDetectionTask',
        }  # type: dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartContainerDetectionTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (Optional[str], Optional[types.StartContainerDetectionTaskParametersSystemState], Optional[types.StartContainerDetectionTaskParametersVisionTaskParameters], float, Optional[Any]) -> Optional[types.StartContainerDetectionTaskReturns]
        """
        Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.

        Args:
            taskId: If specified, the specific taskId to use. (Default: None)
            systemState: The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details. (Default: None)
            visionTaskParameters: Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile. (Default: None)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            Returns immediately once the call completes
        """
        log.verbose('Starting container detection thread...')
        command = {
            'command': 'StartContainerDetectionTask',
        }  # type: dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartVisualizePointCloudTask(self, taskId=None, systemState=None, visionTaskParameters=None, timeout=2.0):
        # type: (Optional[str], Optional[types.StartVisualizePointCloudTaskParametersSystemState], Optional[types.StartVisualizePointCloudTaskParametersVisionTaskParameters], float) -> Optional[types.StartVisualizePointCloudTaskReturns]
        """
        Start point cloud visualization thread to sync camera info from the Mujin controller and send the raw camera point clouds to Mujin controller

        Args:
            taskId: If specified, the specific taskId to use. (Default: None)
            systemState: The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details. (Default: None)
            visionTaskParameters: Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile. (Default: None)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        log.verbose('Starting visualize pointcloud thread...')
        command = {
            'command': 'StartVisualizePointCloudTask',
        }  # type: dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StopTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, removeTask=False, fireandforget=False, timeout=2.0):
        # type: (Optional[str], Optional[list[str]], Optional[str], Optional[list[str]], Optional[str], bool, bool, bool, float) -> Optional[types.StopTaskReturns]
        """
        Stops a set of tasks that meet the filter criteria

        Args:
            taskId: If specified, the specific taskId to stop (Default: None)
            taskIds: If specified, a list of taskIds to stop (Default: None)
            taskType: The task type to stop. (Default: None)
            taskTypes: If specified, a list of task types to stop. (Default: None)
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles. (Default: None)
            waitForStop: If True, then wait for task to stop, otherwise just trigger it to stop, but do not wait (Default: True)
            removeTask: If True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning. (Default: False)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        log.verbose('Stopping detection thread...')
        command = {
            'command': 'StopTask',
            'waitForStop': waitForStop,
            'removeTask': removeTask,
        }  # type: dict[str, Any]
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
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def ResumeTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=_deprecated, fireandforget=False, timeout=2.0):
        # type: (Optional[str], Optional[list[str]], Optional[str], Optional[list[str]], Optional[str], Optional[bool], bool, float) -> Optional[types.ResumeTaskReturns]
        """
        Resumes a set of tasks that meet the filter criteria

        Args:
            taskId: If specified, the specific taskId to resume (Default: None)
            taskIds: If specified, a list of taskIds to resume (Default: None)
            taskType: The task type to resume. (Default: None)
            taskTypes: If specified, a list of task types to resume (Default: None)
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles. (Default: None)
            waitForStop: **deprecated** This is unused. (Default: None)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        log.verbose('Resuming detection thread...')
        command = {
            'command': 'ResumeTask',
        }  # type: dict[str, Any]
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
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def BackupVisionLog(self, cycleIndex, sensorTimestamps=None, fireandforget=False, timeout=2.0):
        # type: (str, Optional[list[float]], bool, float) -> Optional[types.BackupDetectionLogsReturns]
        """
        Backs up the vision log for a given cycle index and/or sensor timestamps.

        Args:
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles.
            sensorTimestamps: The sensor timestamps to backup (Default: None)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'BackupDetectionLogs',
            'cycleIndex': cycleIndex,
        }  # type: dict[str, Any]
        if sensorTimestamps is not None:
            command['sensorTimestamps'] = sensorTimestamps
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def GetLatestDetectedObjects(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0, slaverequestid=None):
        # type: (Optional[str], Optional[str], Optional[str], float, Optional[str]) -> Optional[types.GetLatestDetectedObjectsReturns]
        """
        Gets the latest detected objects.

        Args:
            taskId: If specified, the taskId to retrieve the detected objects from. (Default: None)
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles. (Default: None)
            taskType: The task type to retrieve the detected objects from. (Default: None)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
            slaverequestid: Slave request id used when calling vision manager master to route to the correct vision manager slave. (Default: None)
        """
        command = {
            'command': 'GetLatestDetectedObjects',
        }  # type: dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout, slaverequestid=slaverequestid)

    def GetLatestDetectionResultImages(self, taskId=None, cycleIndex=None, taskType=None, newerThanResultTimestampUS=0, sensorSelectionInfo=None, metadataOnly=False, imageTypes=None, limit=None, blockwait=True, timeout=2.0, slaverequestid=None):
        # type: (Optional[str], Optional[str], Optional[str], int, Optional[types.GetLatestDetectionResultImagesParametersSensorSelectionInfo], bool, Optional[list[types.ImageType]], Optional[int], bool, float, Optional[str]) -> Optional[str]
        """
        Gets the latest detected result images.

        Args:
            taskId: If specified, the taskId to retrieve the detected objects from. (Default: None)
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles. (Default: None)
            taskType: If specified, the task type to retrieve the detected objects from. (Default: None)
            newerThanResultTimestampUS: If specified, starttimestamp of the image must be newer than this value in milliseconds. (Default: 0)
            sensorSelectionInfo: Sensor selection infos (see schema). (Default: None)
            metadataOnly: (Default: False)
            imageTypes: Mujin image types (Default: None)
            limit: (Default: None)
            blockwait: If true, waits for the next image to be available. If false, returns immediately. (Default: True)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
            slaverequestid: Slave request id used when calling vision manager master to route to the correct vision manager slave. (Default: None)

        Returns:
            Raw image data
        """
        log.verbose("Getting latest detection result images...")
        command = {
            'command': 'GetLatestDetectionResultImages',
            'newerThanResultTimestampUS': newerThanResultTimestampUS,
            'metadataOnly': metadataOnly,
        }  # type: dict[str, Any]
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

    def GetDetectionHistory(self, timestamp, timeout=2.0):
        # type: (int, float) -> Optional[str]
        """
        Gets detection result with given timestamp (sensor time)

        Args:
            timestamp: Unix timestamp in milliseconds of the sensor capture time ("targetsensortimestamp" from detected objects).
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)

        Returns:
            Binary blob of detection data
        """
        log.verbose("Getting detection result at %r ...", timestamp)
        command = {
            'command': 'GetDetectionHistory',
            'timestamp': timestamp,
        }  # type: dict[str, Any]
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)

    def Ping(self, timeout=2.0, fireandforget=False):
        # type: (float, bool) -> Optional[types.PingReturns]
        """
        Sends a ping to the visionmanager.

        Args:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
            fireandforget: If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. (Default: False)
        """
        command = {
            'command': 'Ping',
        }  # type: dict[str, Any]
        return self._ExecuteCommand(command, timeout=timeout, fireandforget=fireandforget)

    def SetLogLevel(self, componentLevels, timeout=2.0):
        # type: (types.SetLogLevelParametersComponentLevels, float) -> Optional[types.SetLogLevelReturns]
        """
        Sets the log level for the visionmanager.

        Args:
            componentLevels: A dictionary of component names and their respective log levels.
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'SetLogLevel',
            'componentLevels': componentLevels,
        }  # type: dict[str, Any]
        return self._SendConfiguration(command, timeout=timeout)

    def Quit(self, timeout=2.0):
        # type: (float) -> Optional[types.QuitReturns]
        """
        Quits the visionmanager.

        Args:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        command = {
            'command': 'quit',
        }  # type: dict[str, Any]
        return self._SendConfiguration(command, timeout=timeout)

    def GetTaskStateService(self, taskId=None, cycleIndex=None, taskType=None, timeout=4.0):
        # type: (Optional[str], Optional[str], Optional[str], float) -> Optional[types.GetTaskStateReturns]
        """
        Gets the task state from visionmanager.

        Args:
            taskId: The taskId to retrieve the detected objects from. If not specified, defaults to current slaverequest id. (Default: None)
            cycleIndex: Unique cycle index string for tracking, backing up, and differentiating cycles. (Default: None)
            taskType: The taskType for which the status was requested. If not specified, defaults to the controller monitor task. (Default: None)
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 4.0)
        """
        command = {
            'command': 'GetTaskState',
        }  # type: dict[str, Any]
        if taskId is not None:
            command['taskId'] = taskId
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if taskType is not None:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)

    def GetPublishedStateService(self, timeout=4.0):
        # type: (float) -> Optional[types.GetPublishedStateServiceReturns]
        """
        Gets the published state of the visionmanager.

        Args:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: 4.0)
        """
        command = {
            'command': 'GetPublishedState',
        }  # type: dict[str, Any]
        return self._ExecuteCommand(command, timeout=timeout)

    def Cancel(self, timeout=None):
        # type: (Optional[float]) -> None
        """
        Cancels the current command.

        Args:
            timeout: Time in seconds after which the command is assumed to have failed. (Default: None)
        """
        log.info('Canceling command...')
        command = {
            'command': 'cancel',
        }  # type: dict[str, Any]
        response = self._SendConfiguration(command, timeout=timeout)
        log.info('Command is stopped.')
        return response


    # Subscription command (subscribes to the state)
    def GetPublishedServerState(self, timeout=None, fireandforget=False):
        # type: (Optional[float], bool) -> Optional[dict]
        """
        Args:
            timeout (float, optional):
            fireandforget (bool, optional): (Default: False)

        Returns:
            dict: An unstructured dictionary.
        """
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


VisionControllerClient = VisionClient

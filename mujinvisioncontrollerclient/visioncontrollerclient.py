# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 MUJIN Inc
# Mujin vision controller client for bin picking task

# system imports
import typing # noqa: F401 # used in type check
if typing.TYPE_CHECKING:
    from .visiontypes import SystemState

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

    _ctx = None  # type: zmq.Context # zeromq context to use
    _ctxown = None  # type: zmq.Context
    # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # type: str # hostname of vision controller
    commandport = None  # type: int # command port of vision controller
    configurationport = None  # type: int # configuration port of vision controller, usually command port + 2
    statusport = None  # type: int # status publishing port of vision manager, usually command port + 3

    _commandsocket = None  # type: typing.Optional[zmqclient.ZmqClient]
    _configurationsocket = None  # type: typing.Optional[zmqclient.ZmqClient]
    
    _callerid = None # the callerid to send to vision
    _checkpreemptfn = None # called periodically when in a loop
    
    _subscriber = None # an instance of ZmqSubscriber, used for subscribing to the state
    
    def __init__(self, hostname='127.0.0.1', commandport=7004, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None):
        # type: (str, int, typing.Optional[zmq.Context]) -> None
        """Connects to vision server, initializes vision server, and sets up parameters

        Args:
            hostname (str, optional): e.g. visioncontroller1
            commandport (int, optional): e.g. 7004
            ctx (zmq.Context, optional): The ZMQ context
            checkpreemptfn (Callable, optional): Called periodically when in a loop. A function handle to preempt the socket. The function should raise an exception if a preempt is desired.
            reconnectionTimeout (float, optional): Sets the "timeout" parameter of the ZmqSocketPool instance
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2
        self.statusport = commandport + 3
        self._callerid = callerid
        self._checkpreemptfn = checkpreemptfn
        
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
    
    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True, blockwait=True):
        # type: (typing.Dict, bool, float, bool, bool) -> typing.Optional[typing.Dict]
        if self._callerid:
            command['callerid'] = self._callerid
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt, blockwait=blockwait)
        if blockwait and not fireandforget:
            return self._ProcessResponse(response, command=command, recvjson=recvjson)
        return response

    def _ProcessResponse(self, response, command=None, recvjson=True):
        
        def _HandleError(response):
            # type: (typing.Optional[typing.Dict]) -> None
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

    def StartObjectDetectionTask(self, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (typing.Optional[SystemState], typing.Optional[typing.Dict], float, **typing.Any) -> typing.Optional[typing.Dict]
        """Starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.

        Args:
            systemState (dict, optional): The state of the system. Used to select the base and overwrite profiles that the vision task will use.
                Represents the context of the request. See "Profile Selection" documentation for more details.
            visionTaskParameters (dict, optional): Vision task parameters. This is used to pass parameters that are dynamically set by the caller or orchestrator process.
                When the vision manager evaluates parameters, this will have a higher priority than the base profiles and a lower priority than the overwrite profiles.
                Has the same structure as the vision task profiles.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {'command': 'StartObjectDetectionTask'}
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartContainerDetectionTask(self, systemState=None, visionTaskParameters=None, timeout=2.0, **ignoredArgs):
        # type: (typing.Optional[SystemState], typing.Optional[typing.Dict], float, **typing.Any) -> typing.Optional[typing.Dict]
        """Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.

        Args:
            systemState (dict, optional): The state of the system. Used to select the base and overwrite profiles that the vision task will use.
                Represents the context of the request. See "Profile Selection" documentation for more details.
            visionTaskParameters (dict, optional): Vision task parameters. This is used to pass parameters that are dynamically set by the caller or orchestrator process.
                When the vision manager evaluates parameters, this will have a higher priority than the base profiles and a lower priority than the overwrite profiles.
                Has the same structure as the vision task profiles.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting container detection thread...')
        command = {'command': 'StartContainerDetectionTask'}
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StartVisualizePointCloudTask(self, systemState=None, visionTaskParameters=None, timeout=2.0):
        # type: (typing.Optional[SystemState], typing.Optional[typing.Dict], float) -> typing.Optional[typing.Dict]
        """Start point cloud visualization thread to sync camera info from the mujin controller and send the raw camera point clouds to mujin controller
        
        Args:
            systemState (dict, optional): The state of the system. Used to select the base and overwrite profiles that the vision task will use.
                Represents the context of the request. See "Profile Selection" documentation for more details.
            visionTaskParameters (dict, optional): Vision task parameters. This is used to pass parameters that are dynamically set by the caller or orchestrator process.
                When the vision manager evaluates parameters, this will have a higher priority than the base profiles and a lower priority than the overwrite profiles.
                Has the same structure as the vision task profiles.
        """
        log.verbose('Starting visualize pointcloud thread...')
        command = {'command': 'StartVisualizePointCloudTask'}
        if systemState is not None:
            command['systemState'] = systemState
        if visionTaskParameters is not None:
            command['visionTaskParameters'] = visionTaskParameters
        return self._ExecuteCommand(command, timeout=timeout)

    def StopTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, removeTask=False, fireandforget=False, timeout=2.0):
        """Stops a set of tasks that meet the filter criteria

        Args:
            taskId (optional): if specified, the specific taskId to stop
            taskType (optional): if specified, only stop tasks of this task type
            taskTypes (optional): if specified, a list of task types to stop
            waitForStop (optional): if True, then wait for task to stop, otherwise just trigger it to stop, but do not wait
            removeTask (optional): if True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning.
        """
        log.verbose('Stopping detection thread...')
        command = {"command": "StopTask", 'waitForStop':waitForStop, 'removeTask':removeTask}
        if taskId:
            command['taskId'] = taskId
        if taskIds:
            command['taskIds'] = taskIds
        if taskType:
            command['taskType'] = taskType
        if taskTypes:
            command['taskTypes'] = taskTypes
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)
    
    def ResumeTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, fireandforget=False, timeout=2.0):
        """Resumes a set of tasks that meet the filter criteria

        Args:
            taskId (optional): if specified, the specific taskId to stop
            taskType (optional): if specified, only stop tasks of this task type
            taskTypes (optional): if specified, a list of task types to stop
            waitForStop (optional): if True, then wait for task to stop, otherwise just trigger it to stop, but do not wait
        """
        log.verbose('Stopping detection thread...')
        command = {"command": "ResumeTask", 'waitForStop':waitForStop}
        if taskId:
            command['taskId'] = taskId
        if taskIds:
            command['taskIds'] = taskIds
        if taskType:
            command['taskType'] = taskType
        if taskTypes:
            command['taskTypes'] = taskTypes
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def BackupVisionLog(self, cycleIndex, sensorTimestamps=None, fireandforget=False, timeout=2.0):
        # type: (str, list, bool, float) -> typing.Dict
        if sensorTimestamps is None:
            sensorTimestamps = []
        command = {'command': 'BackupDetectionLogs', 'cycleIndex': cycleIndex, 'sensorTimestamps': sensorTimestamps}
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    def GetLatestDetectedObjects(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0):
        """Gets the latest detected objects
        """
        command = {'command': 'GetLatestDetectedObjects'}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)
    
    def GetLatestDetectionResultImages(self, taskId=None, cycleIndex=None, taskType=None, newerThanResultTimestampMS=0, sensorSelectionInfo=None, metadataOnly=False, imageTypes=None, limit=None, blockwait=True, timeout=2.0):
        """gets the latest detected objects
        """
        log.verbose("Getting latest detection result images...")
        command = {'command': 'GetLatestDetectionResultImages'}
        if newerThanResultTimestampMS:
            command['newerThanResultTimestampMS'] = newerThanResultTimestampMS
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        if sensorSelectionInfo:
            command['sensorSelectionInfo'] = sensorSelectionInfo
        if metadataOnly:
            command['metadataOnly'] = metadataOnly
        if imageTypes:
            command['imageTypes'] = imageTypes
        if limit:
            command['limit'] = limit
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False, blockwait=blockwait)

    def WaitForGetLatestDetectionResultImages(self, timeout=2.0):
        return self._WaitForResponse(recvjson=False, timeout=timeout)
    
    def GetDetectionHistory(self, timestamp, timeout=2.0):
        # type: (float, float) -> typing.Any
        """Gets detection result with given timestamp (sensor time)
        
        Args:
            timestamp (int): unix timestamp in milliseconds
        """
        log.verbose("Getting detection result at %r ...", timestamp)
        command = {
            'command': 'GetDetectionHistory',
            'timestamp': timestamp
        }
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)
    
    def GetVisionStatistics(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0):
        """Gets the latest vision stats
        """
        command = {'command': 'GetVisionStatistics'}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)
    
    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True, recvjson=True):
        # type: (typing.Dict, bool, float, bool) -> typing.Dict
        if self._callerid:
            configuration['callerid'] = self._callerid
        response = self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        if not fireandforget:
            return self._ProcessResponse(response, command=configuration, recvjson=recvjson)
        return response
    
    def Ping(self, timeout=2.0):
        # type: (float) -> typing.Dict
        return self._SendConfiguration({"command": "Ping"}, timeout=timeout)
    
    def SetLogLevel(self, componentLevels, timeout=2.0):
        return self._SendConfiguration({
            "command": "SetLogLevel",
            "componentLevels": componentLevels
        }, timeout=timeout)
    
    def Cancel(self, timeout=2.0):
        # type: (float) -> typing.Dict
        log.info('canceling command...')
        response = self._SendConfiguration({"command": "Cancel"}, timeout=timeout)
        log.info('command is stopped')
        return response
    
    def Quit(self, timeout=2.0):
        # type: (float) -> typing.Dict
        log.info('stopping visionserver...')
        response = self._SendConfiguration({"command": "Quit"}, timeout=timeout)
        log.info('visionserver is stopped')
        return response
    
    def GetTaskStateService(self, taskId=None, cycleIndex=None, taskType=None, timeout=4.0):
        command = {"command": "GetTaskState"}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        response = self._SendConfiguration(command, timeout=timeout)
        return response
    
    def GetPublishedStateService(self, timeout=4.0):
        response = self._SendConfiguration({"command": "GetPublishedState"}, timeout=timeout)
        return response

    # for subscribing to the state
    def GetPublishedState(self, timeout=None, fireandforget=False):
        if self._subscriber is None:
            self._subscriber = zmqsubscriber.ZmqSubscriber('tcp://%s:%d' % (self.hostname, self.statusport), ctx=self._ctx)
        rawState = self._subscriber.SpinOnce(timeout=timeout, checkpreemptfn=self._checkpreemptfn)
        if rawState is not None:
            return json.loads(rawState)
        return None

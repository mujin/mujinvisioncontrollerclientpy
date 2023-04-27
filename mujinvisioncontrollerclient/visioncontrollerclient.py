# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 MUJIN Inc
# Mujin vision controller client for bin picking task

# system imports
import zmq
import json
import typing # noqa: F401 # used in type check
import time

# mujin imports
from mujinplanningclient import zmqclient
from . import VisionControllerClientError

# logging
from logging import getLogger
log = getLogger(__name__)

"""
vminitparams is a dict of Parameters needed to start visionmanager commands (see visionTaskCommonInputsSchema):
    mujinControllerIp (str): controller client ip
    mujinControllerPort (int): controller client port
    mujinControllerUsernamePass (str): controller client "{0}:{1}".format(username, password)

    binpickingTaskZmqPort (str):
    binpickingTaskHeartbeatPort (int):
    binpickingTaskHeartbeatTimeout (double): in seconds
    binpickingTaskScenePk (str):
    defaultTaskParameters (str): Params vision manager has to send to every request it makes to the mujin controller
    slaverequestid (str):
    controllertimeout (double): Controller command timeout in seconds (Default: 10s)
    tasktype (str): Controller client tasktype

    streamerIp (str):
    streamerPort (int):
    imagesubscriberconfig (str): JSON string
    containerParameters (dict):

    targetname (str):
    targeturi (str):
    targetupdatename (str): Name of the detected target which will be returned from detector. If not set, then the value from initialization will be used
    detectorconfigname (str): name of detector config
    targetdetectionarchiveurl (str): full url to download the target archive containing detector conf and templates
    targetDynamicDetectorParameters (str): allow passing of dynamically determined paramters to detector, python dict

    locale (str): (Default: en_US)

    visionManagerConfiguration (dict): See schema.
"""

class VisionControllerClient(object):
    """Mujin Vision Controller client for binpicking tasks.
    """

    _isok = False  # type: bool # False indicates that the client is about to be destroyed
    _ctx = None  # type: zmq.Context # zeromq context to use
    _ctxown = None  # type: zmq.Context
    # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # type: str # hostname of vision controller
    commandport = None  # type: int # command port of vision controller
    configurationport = None  # type: int # configuration port of vision controller, usually command port + 2

    _commandsocket = None  # type: typing.Optional[zmqclient.ZmqClient]
    _configurationsocket = None  # type: typing.Optional[zmqclient.ZmqClient]

    statusport = None
    _callerid = None # the callerid to send to vision
    _checkpreemptfn = None # called periodically when in a loop
    
    _subsocket = None # used for subscribing to the state
    
    def __init__(self, hostname='127.0.0.1', commandport=7004, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None):
        # type: (str, int, typing.Optional[zmq.Context]) -> None
        """Connects to vision server, initializes vision server, and sets up parameters

        Args:
            hostname (str, optional): e.g. visioncontroller1
            commandport (int, optional): e.g. 7004
            ctx (zmq.Context, optional): The ZMQ context
            checkpreemptfn (Callable, optional): Called periodically when in a loop. A function handle to preempt the socket. The function should raise an exception if a preempt is desired.
            reconnectionTimeout (float, optional): Sets the "timeout" parameter of the ZmqSocketPool instance
            callerid (str, optional): The callerid to send to vision.
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2
        self.statusport = commandport + 3
        self._callerid = callerid
        
        if ctx is None:
            assert(self._ctxown is None)
            self._ctxown = zmq.Context()
            self._ctxown.linger = 100
            self._ctx = self._ctxown
        else:
            self._ctx = ctx
        
        self._commandsocket = zmqclient.ZmqClient(self.hostname, commandport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
        self._configurationsocket = zmqclient.ZmqClient(self.hostname, self.configurationport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
        self._isok = True
    
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
                log.exception('problem destroying commandsocket')

        if self._configurationsocket is not None:
            try:
                self._configurationsocket.Destroy()
                self._configurationsocket = None
            except Exception as e:
                log.exception('problem destroying configurationsocket')

        if self._subsocket is not None:
            try:
                self._subsocket.close()
            except Exception as e:
                log.exception(u'caught socket: %s', e)
            self._subsocket=None
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
                self._ctxown = None
            except Exception as e:
                log.exception('problem destroying ctxown')

        self._ctx = None

    def SetDestroy(self):
        # type: () -> None
        self._isok = False
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()
    
    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True):
        # type: (typing.Dict, bool, float, bool, bool) -> typing.Optional[typing.Dict]
        if self._callerid:
            command['callerid'] = self._callerid
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt)
        if fireandforget:
            return None
        
        def HandleError(response):
            # type: (typing.Optional[typing.Dict]) -> None
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('type', ''), response['error'].get('desc', ''))
            else:
                raise VisionControllerClientError('unknownerror', u'Got unknown formatted error %r' % response['error'])
        if recvjson:

            if 'error' in response:
                HandleError(response)

            if 'computationtime' in response:
                log.verbose('%s took %f seconds' % (command['command'], response['computationtime'] / 1000.0))
            else:
                log.verbose('%s executed successfully' % (command['command']))
        else:
            if len(response) > 0 and response[0] == '{' and response[-1] == '}':
                response = json.loads(response)
                if 'error' in response:
                    HandleError(response)
            if len(response) == 0:
                raise VisionControllerClientError('emptyresponseerror', 'vision command %(command)s failed with empty response %(response)r' % {'command': command, 'response': response})
        return response

    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True):
        # type: (typing.Dict, bool, float, bool) -> typing.Dict
        """Sends a configuration command.

        Args:
            configuration (dict): 
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
        """
        try:
            return self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        except Exception as e:
            log.exception('Error occurred while sending configuration %r: %s', configuration, e)
            raise

    ###############################

    # Subscription command (subscribes to the state)
    def GetPublishedState(self, timeout=None, fireandforget=False):
        if self._subsocket is None:
            subsocket = self._ctx.socket(zmq.SUB)
            subsocket.setsockopt(zmq.CONFLATE, 1) # store only newest message. have to call this before connect
            subsocket.setsockopt(zmq.TCP_KEEPALIVE, 1) # turn on tcp keepalive, do these configuration before connect
            subsocket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 2) # the interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe; after the connection is marked to need keepalive, this counter is not used any further
            subsocket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 2) # the interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime
            subsocket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 2) # the number of unacknowledged probes to send before considering the connection dead and notifying the application layer
            subsocket.connect('tcp://%s:%s'%(self.hostname,self.statusport))
            subsocket.setsockopt(zmq.SUBSCRIBE, b'') # have to use b'' to make python3 compatible
            self._subsocket = subsocket
        
        starttime = time.time()
        msg = None
        # keep on reading any messages that are on the socket until end is reached
        while True:
            try:
                msg = self._subsocket.recv_json(zmq.NOBLOCK)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    if msg is not None:
                        break

                else:
                    log.exception('caught exception while trying to receive from subscriber socket: %s', e)
                    try:
                        self._subsocket.close()
                    except Exception as e2:
                        log.exception('failed to close subscriber socket: %s', e2)
                    self._subsocket = None
                    raise

                # sleep a little and try again
                self._subsocket.poll(20)
            if timeout is not None and time.time() - starttime > timeout:
                raise VisionControllerClientError('timeout to get response', u'%s:%d'%(self.hostname, self.statusport))

            if self._checkpreemptfn is not None:
                self._checkpreemptfn()
        return msg

    def GetPublishedStateService(self, timeout=4.0):
        response = self._SendConfiguration({"command": "GetPublishedState"}, timeout=timeout)
        return response

    def Ping(self, timeout=2.0):
        # type: (float) -> typing.Dict
        return self._SendConfiguration({"command": "Ping"}, timeout=timeout)

    def SetLogLevel(self, componentLevels, timeout=2.0):
        """Sets the log level for the visionmanager.

        Args:
            componentLevels (dict): A dictionary of component names and their respective log levels.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        return self._SendConfiguration({
            "command": "SetLogLevel",
            "componentLevels": componentLevels
        }, timeout=timeout)

    def Cancel(self, timeout=2.0):
        # type: (float) -> typing.Dict
        """Cancels the current command.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.info('Canceling command...')
        response = self._SendConfiguration({"command": "Cancel"}, timeout=timeout)
        log.info('Command is stopped')
        return response

    def Quit(self, timeout=2.0):
        # type: (float) -> typing.Dict
        """Quits the visionmanager.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.info('stopping visionserver...')
        response = self._SendConfiguration({"command": "Quit"}, timeout=timeout)
        log.info('visionserver is stopped')
        return response

    def GetTaskStateService(self, taskId=None, cycleIndex=None, taskType=None, timeout=4.0):
        """Gets the status port of visionmanager

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        command = {"command": "GetTaskState"}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        response = self._SendConfiguration(command, timeout=timeout)
        return response

    def GetVisionStatistics(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0):
        """Gets the latest vision stats

        Args:
            taskId (str, optional): If specified, the taskId to retrieve the detected objects from.
            cycleIndex (str, optional): The cycle index
            taskType (str, optional): If specified, the task type to retrieve the detected objects from.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        command = {'command': 'GetVisionStatistics'}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)

    def GetStatusPort(self, timeout=2.0):
        # type: (float) -> typing.Any
        """Gets the status port of visionmanager. 

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose("Getting status port...")
        command = {'command': 'GetStatusPort'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetConfigPort(self, timeout=2.0):
        # type: (float) -> typing.Any
        """Gets the config port of visionmanager

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose("Getting config port...")
        command = {'command': 'GetConfigPort'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetLatestDetectedObjects(self, taskId=None, cycleIndex=None, taskType=None, timeout=2.0):
        """Gets the latest detected objects

        Args:
            taskId (str, optional): If specified, the taskId to retrieve the detected objects from.
            cycleIndex (str, optional): The cycle index
            taskType (str, optional): If specified, the task type to retrieve the detected objects from.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose("Getting latest detected objects...")
        command = {'command': 'GetLatestDetectedObjects'}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)
    
    def GetLatestDetectionResultImages(self, taskId=None, cycleIndex=None, taskType=None, newerthantimestamp=0, sensorSelectionInfo=None, metadataOnly=False, imageTypes=None, limit=None, timeout=2.0):
        """Gets the latest detected result images.

        Args:
            taskId (str, optional): If specified, the taskId to retrieve the detected objects from.
            cycleIndex (str, optional): The cycle index
            taskType (str, optional): If specified, the task type to retrieve the detected objects from.
            newerthantimestamp (bool, optional): If specified, starttimestamp of the image must be newer than this value in milliseconds.
            sensorSelectionInfos (list, optional): sensor selection infos (see schema)
            metadataOnly (bool, optional): Default: False
            imagesTypes (list, optional):
            limit (int, optional):
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose("Getting latest detection result images...")
        command = {'command': 'GetLatestDetectionResultImages', 'newerthantimestamp': newerthantimestamp}
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
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)

    def GetDetectionHistory(self, timestamp, timeout=2.0):
        # type: (float, float) -> typing.Any
        """Gets detection result with given timestamp (sensor time)
        
        Args:
            timestamp (int): unix timestamp in milliseconds
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose("Getting detection result at %r ...", timestamp)
        command = {
            'command': 'GetDetectionHistory',
            'timestamp': timestamp
        }
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)

    def StopTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, removeTask=False, fireandforget=False, timeout=2.0):
        """Stops a set of tasks that meet the filter criteria

        Args:
            taskId (str, optional): If specified, the specific taskId to stop
            taskType (str, optional): If specified, only stop tasks of this task type
            taskTypes (list[str], optional): If specified, a list of task types to stop
            cycleIndex (str, optional): The cycle index
            waitForStop (bool, optional): If True, then wait for task to stop, otherwise just trigger it to stop, but do not wait
            removeTask (bool, optional): If True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose('Stopping detection thread...')
        command = {"command": "StopTask", 'waitForStop':waitForStop, 'removeTask':removeTask}
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
    
    def ResumeTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, fireandforget=False, timeout=2.0):
        """Resumes a set of tasks that meet the filter criteria

        Args:
            taskId (str, optional): If specified, the specific taskId to resume
            taskType (str, optional): If specified, only resume tasks of this task type
            taskTypes (list[str], optional): If specified, a list of task types to resume
            cycleIndex (str, optional): The cycle index
            waitForStop (bool, optional): DEPRECATED. This is unused.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
        """
        log.verbose('Resuming detection thread...')
        command = {"command": "ResumeTask"}
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

    def StartObjectDetectionTask(self, systemState=None, timeout=2.0, **ignoredArgs):
        """Starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.

        Args:
            systemState (types.systemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {'command': 'StartObjectDetectionTask'}
        if systemState is not None:
            command['systemState'] = systemState
        return self._ExecuteCommand(command, timeout=timeout)
    
    def StartContainerDetectionTask(self, systemState=None, timeout=2.0, **ignoredArgs):
        """Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.

        Args:
            systemState (types.systemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.

        Returns:
            dict: Returns immediately once the call completes
        """
        log.verbose('Starting container detection thread...')
        command = {'command': 'StartContainerDetectionTask'}
        if systemState is not None:
            command['systemState'] = systemState
        return self._ExecuteCommand(command, timeout=timeout)
    
    def StartVisualizePointCloudTask(self, systemState=None, timeout=2.0):
        """Start point cloud visualization thread to sync camera info from the mujin controller and send the raw camera point clouds to mujin controller
        
        Args:
            systemState (types.systemState or dict): The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
        """
        log.verbose('Starting visualize pointcloud thread...')
        command = {'command': 'StartVisualizePointCloudTask'}
        if systemState is not None:
            command['systemState'] = systemState
        return self._ExecuteCommand(command, timeout=timeout)

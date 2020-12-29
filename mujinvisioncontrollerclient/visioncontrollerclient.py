# -*- coding: utf-8 -*-
# Copyright (C) 2012-2017 MUJIN Inc
# Mujin vision controller client for bin picking task

# system imports
import zmq
import json
import time

# mujin imports
from mujincontrollerclient import zmqclient
from . import VisionControllerClientError

# logging
from logging import getLogger
log = getLogger(__name__)

"""
vminitparams (dict): Parameters needed for some visionmanager commands
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
    targetupdatename (str): Name of the detected target which will be returned from detector.
                            If not set, then the value from initialization will be used
    detectorconfigname (str): name of detector config
    targetdetectionarchiveurl (str): full url to download the target archive containing detector conf and templates
    targetDynamicDetectorParameters (str): allow passing of dynamically determined paramters to detector, python dict

    locale (str): (Default: en_US)

    visionManagerConfiguration (dict): 
    sensormapping(dict): cameraname(str) -> cameraid(str)
"""

class VisionControllerClient(object):
    """mujin vision controller client for bin picking task
    """

    _isok = False  # False indicates that the client is about to be destroyed
    _ctx = None  # zeromq context to use
    _ctxown = None  # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # hostname of vision controller
    commandport = None  # command port of vision controller
    configurationport = None  # configuration port of vision controller, usually command port + 2
    statusport = None
    
    _checkpreemptfn = None # called periodically when in a loop
    
    _commandsocket = None
    _configurationsocket = None
    _subsocket = None # used for subscribing to the state
    
    def __init__(self, hostname, commandport, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None):
        """connects to vision server, initializes vision server, and sets up parameters
        :param hostname: e.g. visioncontroller1
        :param commandport: e.g. 7004
        :param ctx: zmq context
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2
        self.statusport = commandport + 3
        
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
        self._isok = False
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()
    
    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True):
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt)
        if fireandforget:
            return None

        def HandleError(response):
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
    
    def IsDetectionRunning(self, timeout=10.0):
        log.verbose('checking detection status...')
        command = {'command': 'IsDetectionRunning'}
        return self._ExecuteCommand(command, timeout=timeout)['isdetectionrunning']
    
    def GetRunningState(self, timeout=10.0):
        command = {'command': 'GetRunningState'}
        return self._ExecuteCommand(command, timeout=timeout)
        
    def StartObjectDetectionTask(self, vminitparams, taskId=None, locationName=None, ignoreocclusion=None, targetDynamicDetectorParameters=None, detectionstarttimestamp=None, locale=None, maxnumfastdetection=1, maxnumdetection=0, stopOnNotNeedContainer=None, timeout=2.0, targetupdatename="", numthreads=None, cycleIndex=None, cycleMode=None, ignoreDetectionFileUpdateChange=None, sendVerificationPointCloud=None, clearRegion=True, waitForTrigger=False, detectionTriggerMode=None, **kwargs):
        """starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.
        :param vminitparams (dict): See documentation at the top of the file
        :param taskId: the taskId to request for this task
        :param targetname: name of the target
        :param locationName: name of the bin
        :param ignoreocclusion: whether to skip occlusion check
        :param targetDynamicDetectorParameters: name of the collision obstacle
        :param detectionstarttimestamp: min image time allowed to be used for detection, if not specified, only images taken after this call will be used
        :param sendVerificationPointCloud: if True, then send the source verification point cloud via AddPointCloudObstacle

        :param timeout in seconds
        :param targetupdatename name of the detected target which will be returned from detector. If not set, then the value from initialization will be used
        :param numthreads Number of threads used by different libraries that are used by the detector (ex. OpenCV, BLAS). If 0 or None, defaults to the max possible num of threads
        :param cycleIndex: cycle index

        :param ignoreBinpickingStateForFirstDetection: whether to start first detection without checking for binpicking state
        :param maxContainerNotFound: Max number of times detection results NotFound until container detection thread exits.
        :param maxNumContainerDetection: Max number of images to snap to get detection success until container detection thread exits.
        :param clearRegion: if True, then call detector->ClearRegion before any detection is done. This is usually used when a container contents in the detection location, and detector cannot reuse any history.
        :param detectionTriggerMode: If 'AutoOnChange', then wait for camera to be unoccluded and that the source container changed. if 'WaitTrigger', then the detector waits for `triggerDetectionCaptureInfo` to be published by planning in order to trigger the detector, otherwise it will not capture. The default value is 'AutoOnChange'
        :param waitingMode: Specifies the waiting mode of the task. If "", then task is processed reguarly. If "AfterFirstDetectionResults", then start waiting for a resume once the first detection results are sent over. If "StartWaiting", then go into waiting right away.
        :param stopOnNotNeedContainer: if true, then stop the detection based on needContainer signal
        
        :return: returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {'command': 'StartObjectDetectionTask',
                   'targetupdatename': targetupdatename
                   }
        command.update(vminitparams)
        if locationName is not None:
            command['locationName'] = locationName
        if taskId:
            command['taskId'] = taskId
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if targetDynamicDetectorParameters is not None:
            command['targetDynamicDetectorParameters'] = targetDynamicDetectorParameters
        if detectionstarttimestamp is not None:
            command['detectionstarttimestamp'] = detectionstarttimestamp
        if locale is not None:
            command['locale'] = locale
        if sendVerificationPointCloud is not None:
            command['sendVerificationPointCloud'] = sendVerificationPointCloud
        if stopOnNotNeedContainer is not None:
            command['stopOnNotNeedContainer'] = stopOnNotNeedContainer
        if maxnumdetection is not None:
            command['maxnumdetection'] = maxnumdetection
        if maxnumfastdetection is not None:
            command['maxnumfastdetection'] = maxnumfastdetection
        if numthreads is not None:
            command['numthreads'] = numthreads
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if cycleMode is not None:
            command['cycleMode'] = str(cycleMode)
        if ignoreDetectionFileUpdateChange is not None:
            command['ignoreDetectionFileUpdateChange'] = ignoreDetectionFileUpdateChange
        if clearRegion is not None:
            command['clearRegion'] = clearRegion
        if detectionTriggerMode is not None:
            command['detectionTriggerMode'] = detectionTriggerMode
        command.update(kwargs)
        return self._ExecuteCommand(command, timeout=timeout)
    
    def StartContainerDetectionTask(self, vminitparams, taskId=None, locationName=None, ignoreocclusion=None, targetDynamicDetectorParameters=None, detectionstarttimestamp=None, locale=None, timeout=2.0, numthreads=None, cycleIndex=None, cycleMode=None, stopOnNotNeedContainer=None, **kwargs):
        """starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.
        :param vminitparams (dict): See documentation at the top of the file
        :param taskId: the taskId to request for this task
        :param targetname: name of the target
        :param locationName: name of the bin
        :param ignoreocclusion: whether to skip occlusion check
        :param targetDynamicDetectorParameters: name of the collision obstacle
        :param detectionstarttimestamp: min image time allowed to be used for detection, if not specified, only images taken after this call will be used
        :param timeout in seconds
        :param numthreads Number of threads used by different libraries that are used by the detector (ex. OpenCV, BLAS). If 0 or None, defaults to the max possible num of threads
        :param cycleIndex: cycle index
        :param maxContainerNotFound: Max number of times detection results NotFound until container detection thread exits.
        :param maxNumContainerDetection: Max number of images to snap to get detection success until container detection thread exits.
        :param waitingMode: Specifies the waiting mode of the task. If "", then task is processed reguarly. If "AfterFirstDetectionResults", then start waiting for a resume once the first detection results are sent over. If "StartWaiting", then go into waiting right away.
        :param stopOnNotNeedContainer: if true, then stop the detection based on needContainer signal
        
        :return: returns immediately once the call completes
        """
        log.verbose('Starting container detection thread...')
        command = {'command': 'StartContainerDetectionTask'
                   }
        command.update(vminitparams)
        if taskId:
            command['taskId'] = taskId
        if locationName is not None:
            command['locationName'] = locationName
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if targetDynamicDetectorParameters is not None:
            command['targetDynamicDetectorParameters'] = targetDynamicDetectorParameters
        if detectionstarttimestamp is not None:
            command['detectionstarttimestamp'] = detectionstarttimestamp
        if locale is not None:
            command['locale'] = locale
        if numthreads is not None:
            command['numthreads'] = numthreads
        if cycleIndex is not None:
            command['cycleIndex'] = cycleIndex
        if cycleMode is not None:
            command['cycleMode'] = str(cycleMode)
        if stopOnNotNeedContainer is not None:
            command['stopOnNotNeedContainer'] = stopOnNotNeedContainer
        command.update(kwargs)
        return self._ExecuteCommand(command, timeout=timeout)
    
    def StopTask(self, taskId=None, taskIds=None, taskType=None, taskTypes=None, cycleIndex=None, waitForStop=True, fireandforget=False, timeout=2.0):
        """stops a set of tasks that meet the filter criteria
        :param taskId: if specified, the specific taskId to stop
        :param taskType: if specified, only stop tasks of this task type
        :param taskTypes: if specified, a list of task types to stop
        :param waitForStop: if True, then wait for task to stop, otherwise just trigger it to stop, but do not wait
        """
        log.verbose('Stopping detection thread...')
        command = {"command": "StopTask", 'waitForStop':waitForStop}
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
        """resumes a set of tasks that meet the filter criteria
        :param taskId: if specified, the specific taskId to stop
        :param taskType: if specified, only stop tasks of this task type
        :param taskTypes: if specified, a list of task types to stop
        :param waitForStop: if True, then wait for task to stop, otherwise just trigger it to stop, but do not wait
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
    
    def ClearRegion(self, locationName, fireandforget=False, timeout=2.0):
        """Clears any cache states associated with the region. This is called when the container in the region changes and now there are new parts
        """
        command = {"command": "ClearRegion", "locationName":locationName}
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)
    
    def SendVisionManagerConf(self, conf, fireandforget=True, timeout=2.0):
        """
        Send vision manager conf to vision manager. The conf is needed to kick
        off certain background process

        :param conf(dict): vision manager conf
        """
        command = {
            "command": "ReceiveVisionManagerConf",
            "conf": conf
        }
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)
    
    def VisualizePointCloudOnController(self, vminitparams, locationName=None, cameranames=None, pointsize=None, ignoreocclusion=None, newerthantimestamp=None, request=True, timeout=2.0, filteringsubsample=None, filteringvoxelsize=None, filteringstddev=None, filteringnumnn=None):
        """Visualizes the raw camera point clouds on mujin controller
        :param vminitparams (dict): See documentation at the top of the file
        :param locationName: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param newerthantimestamp: if specified, starttimestamp of the image must be newer than this value in milliseconds
        :param request: whether to take new images instead of getting off buffer
        :param timeout in seconds
        :param filteringsubsample: point cloud filtering subsample parameter
        :param filteringvoxelsize: point cloud filtering voxelization parameter in millimeter
        :param filteringstddev: point cloud filtering std dev noise parameter
        :param filteringnumnn: point cloud filtering number of nearest-neighbors parameter
        """
        log.verbose('sending camera point cloud to mujin controller...')
        command = {'command': 'VisualizePointCloudOnController'}
        command.update(vminitparams)
        if locationName is not None:
            command['locationName'] = locationName
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if pointsize is not None:
            command['pointsize'] = pointsize
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if newerthantimestamp is not None:
            command['newerthantimestamp'] = newerthantimestamp
        if request is not None:
            command['request'] = 1 if request is True else 0
        if filteringsubsample is not None:
            command['filteringsubsample'] = filteringsubsample
        if filteringvoxelsize is not None:
            command['filteringvoxelsize'] = filteringvoxelsize
        if filteringstddev is not None:
            command['filteringstddev'] = filteringstddev
        if filteringnumnn is not None:
            command['filteringnumnn'] = filteringnumnn
        return self._ExecuteCommand(command, timeout=timeout)

    def ClearVisualizationOnController(self, fireandforget=False, timeout=2.0):
        """Clears visualization made by VisualizePointCloudOnController
        :param timeout in seconds
        """
        log.verbose("clearing visualization on mujin controller...")
        command = {'command': 'ClearVisualizationOnController'}
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)
    
    def StartVisualizePointCloudTask(self, vminitparams, locationName=None, cameranames=None, pointsize=None, ignoreocclusion=None, newerthantimestamp=None, request=True, timeout=2.0, filteringsubsample=None, filteringvoxelsize=None, filteringstddev=None, filteringnumnn=None):
        """Start point cloud visualization thread to sync camera info from the mujin controller and send the raw camera point clouds to mujin controller
        :param vminitparams (dict): See documentation at the top of the file
        :param locationName: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param pointsize: in millimeter
        :param ignoreocclusion: whether to skip occlusion check
        :param newerthantimestamp: if specified, starttimestamp of the image must be newer than this value in milliseconds
        :param request: whether to take new images instead of getting off buffer
        :param timeout in seconds
        :param filteringsubsample: point cloud filtering subsample parameter
        :param filteringvoxelsize: point cloud filtering voxelization parameter in millimeter
        :param filteringstddev: point cloud filtering std dev noise parameter
        :param filteringnumnn: point cloud filtering number of nearest-neighbors parameter
        """
        log.verbose('Starting visualize pointcloud thread...')
        command = {'command': 'StartVisualizePointCloudTask',
                   }
        command.update(vminitparams)
        if locationName is not None:
            command['locationName'] = locationName
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if pointsize is not None:
            command['pointsize'] = pointsize
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if newerthantimestamp is not None:
            command['newerthantimestamp'] = newerthantimestamp
        if request is not None:
            command['request'] = 1 if request is True else 0
        if filteringsubsample is not None:
            command['filteringsubsample'] = filteringsubsample
        if filteringvoxelsize is not None:
            command['filteringvoxelsize'] = filteringvoxelsize
        if filteringstddev is not None:
            command['filteringstddev'] = filteringstddev
        if filteringnumnn is not None:
            command['filteringnumnn'] = filteringnumnn
        return self._ExecuteCommand(command, timeout=timeout)
        
    def GetVisionmanagerConfig(self, timeout=2.0):
        """Gets the current visionmanager config json string
        """
        log.verbose('getting current visionmanager config...')
        command = {'command': 'GetVisionmanagerConfig'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetDetectorConfig(self, timeout=2.0):
        """Gets the current detector config json string
        """
        log.verbose('getting current detector config...')
        command = {'command': 'GetDetectorConfig'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetImagesubscriberConfig(self, timeout=2.0):
        """Gets the current imagesubscriber config json string
        """
        log.verbose('getting current imagesubscriber config...')
        command = {'command': 'GetImagesubscriberConfig'}
        return self._ExecuteCommand(command, timeout=timeout)

    def SaveVisionmanagerConfig(self, visionmanagerconfigname, config="", timeout=2.0):
        """Saves the visionmanager config to disk
        :param visionmanagerconfigname name of the visionmanager config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving visionmanager config to disk...')
        command = {'command': 'SaveVisionmanagerConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout=timeout)

    def SaveDetectorConfig(self, detectorconfigname, config="", timeout=2.0):
        """Saves the detector config to disk
        :param detectorconfigname name of the detector config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving detector config to disk...')
        command = {'command': 'SaveDetectorConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout=timeout)

    def SaveImagesubscriberConfig(self, imagesubscriberconfigname, config="", timeout=2.0):
        """Saves the imagesubscriber config to disk
        :param imagesubscriberconfigname name of the imagesubscriber config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving imagesubscriber config to disk...')
        command = {'command': 'SaveImagesubscriberConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout=timeout)

    def BackupVisionLog(self, cycleIndex, fireandforget=False, timeout=2.0):
        command = {'command': 'BackupDetectionLogs', 'cycleIndex': cycleIndex}
        return self._ExecuteCommand(command, fireandforget=fireandforget, timeout=timeout)

    ############################
    # internal methods
    ############################

    def SyncRegion(self, vminitparams, locationName=None, timeout=2.0):
        """updates vision server with the lastest container info on mujin controller
        usage: user may want to update the region's transform on the vision server after it gets updated on the mujin controller
        :param vminitparams (dict): See documentation at the top of the file
        :param locationName: name of the bin
        :param timeout in seconds
        """
        log.verbose('Updating region...')
        command = {'command': 'SyncRegion'}
        command.update(vminitparams)
        if locationName is not None:
            command['locationName'] = locationName
        return self._ExecuteCommand(command, timeout=timeout)

    def SyncCameras(self, vminitparams, locationName=None, cameranames=None, timeout=2.0):
        """updates vision server with the lastest camera info on mujin controller
        usage: user may want to update a camera's transform on the vision server after it gets updated on the mujin controller
        :param vminitparams (dict): See documentation at the top of the file
        :param locationName: name of the bin, of which the relevant camera info gets updated
        :param cameranames: a list of names of cameras, if None, then use all cameras available
        :param timeout in seconds
        """
        log.verbose('Updating cameras...')
        command = {'command': 'SyncCameras',
                   }
        command.update(vminitparams)
        if locationName is not None:
            command['locationName'] = locationName
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        return self._ExecuteCommand(command, timeout=timeout)
    
    def GetStatusPort(self, timeout=2.0):
        """gets the status port of visionmanager
        """
        log.verbose("Getting status port...")
        command = {'command': 'GetStatusPort'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetConfigPort(self, timeout=2.0):
        """gets the config port of visionmanager
        """
        log.verbose("Getting config port...")
        command = {'command': 'GetConfigPort'}
        return self._ExecuteCommand(command, timeout=timeout)

    def GetLatestDetectedObjects(self, taskId=None, cycleIndex=None, taskType=None, returnpoints=False, timeout=2.0):
        """gets the latest detected objects
        """
        log.verbose("Getting latest detected objects...")
        command = {'command': 'GetLatestDetectedObjects', 'returnpoints': returnpoints}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout)
    
    def GetLatestDetectionResultImage(self, taskId=None, cycleIndex=None, taskType=None, newerthantimestamp=0, timeout=2.0):
        """gets the latest detected objects
        """
        log.verbose("Getting latest detection result images...")
        command = {'command': 'GetLatestDetectionResultImage', 'newerthantimestamp': newerthantimestamp}
        if taskId:
            command['taskId'] = taskId
        if cycleIndex:
            command['cycleIndex'] = cycleIndex
        if taskType:
            command['taskType'] = taskType
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)
    
    def GetDetectionHistory(self, timestamp, timeout=2.0):
        """ Get detection result with given timestamp (sensor time)
        :params timestamp: int. unix timestamp in milliseconds
        """
        log.verbose("Getting detection result at %r ...", timestamp)
        command = {
            'command': 'GetDetectionHistory',
            'timestamp': timestamp
        }
        return self._ExecuteCommand(command, timeout=timeout, recvjson=False)

#     def GetStatistics(self, timeout=2.0):
#         """gets the latest vision stats
#         """
#         log.verbose("Getting latest vision stats...")
#         command = {'command': 'GetStatistics'}
#         return self._ExecuteCommand(command, timeout=timeout)
    
    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True):
        try:
            return self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        except Exception as e:
            log.exception('occured while sending configuration %r', configuration)
            raise
    
    def Ping(self, timeout=2.0):
        return self._SendConfiguration({"command": "Ping"}, timeout=timeout)
    
    def SetLogLevel(self, componentLevels, timeout=2.0):
        return self._SendConfiguration({
            "command": "SetLogLevel",
            "componentLevels": componentLevels
        }, timeout=timeout)
    
    def Cancel(self, timeout=2.0):
        log.info('canceling command...')
        response = self._SendConfiguration({"command": "Cancel"}, timeout=timeout)
        log.info('command is stopped')
        return response
    
    def Quit(self, timeout=2.0):
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
    

# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
# Mujin vision controller client for bin picking task

# system imports
import json

# mujin imports
from mujincontrollerclient import zmqclient
from . import VisionControllerClientError

# logging
from logging import getLogger
log = getLogger(__name__)


class VisionControllerClient(object):
    """mujin vision controller client for bin picking task
    """

    _isok = False # False indicates that the client is about to be destroyed
    _ctx = None # zeromq context to use
    _ctxown = None # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None # hostname of vision controller
    commandport = None # command port of vision controller
    configurationport = None # configuration port of vision controller, usually command port + 2

    def __init__(self, hostname, commandport, ctx=None):
        """connects to vision server, initializes vision server, and sets up parameters
        :param hostname: e.g. visioncontroller1
        :param commandport: e.g. 7004
        :param ctx: zmq context
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2

        if ctx is None:
            assert(self._ctxown is None)
            self._ctxown = zmq.Context()
            self._ctxown.linger = 100
            self._ctx = self._ctxown
        else:
            self._ctx = ctx

        self._commandsocket = zmqclient.ZmqClient(self.hostname, commandport, self._ctx)
        self._configurationsocket = zmqclient.ZmqClient(self.hostname, self.configurationport, self._ctx)
        self._isok = True
        
    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
        self.SetDestroy()

        if self._commandsocket is not None:
            try:
                self._commandsocket.Destroy()
                self._commandsocket = None
            except:
                log.exception()

        if self._configurationsocket is not None:
            try:
                self._configurationsocket.Destroy()
                self._configurationsocket = None
            except:
                log.exception()

        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
                self._ctxown = None
            except:
                log.exception()

        self._ctx = None

    def SetDestroy(self):
        self._isok = False
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()
        
    def _ExecuteCommand(self, command, timeout=1.0):
        response = self._commandsocket.SendCommand(command, timeout=timeout)
        if 'error' in response:
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('type', ''), response['error'].get('desc', ''))

            else:
                raise VisionControllerClientError('unknownerror', u'Got unknown formatted error %r' % response['error'])
        if 'computationtime' in response:
            log.verbose('%s took %f seconds' % (command['command'], response['computationtime'] / 1000.0))
        else:
            log.verbose('%s executed successfully' % (command['command']))
        return response

    def InitializeVisionServer(self, visionmanagerconfigname, detectorconfigname, imagesubscriberconfigname, targetname, streamerIp, streamerPort, controllerclient, timeout=10.0, locale="", targeturi="", slaverequestid=None, defaultTaskParameters=None):
        """initializes vision server
        :param visionmanagerconfigname: name of visionmanager config
        :param detectorconfigname: name of detector config
        :param imagesubscribername: name of imagesubscriber config
        :param targetname: name of the target object
        :param streamerIp: ip of streamer
        :param streamerPort: port of streamer
        :param controllerclient: pointer to the BinpickingControllerClient that connects to the mujin controller we want the vision server to talk to
        :param timeout: in seconds
        :param slaverequestid: the slaverequestid that the vision manager should use when sending results
        :param defaultTaskParameters: python dictionary of default task parameters to have vision manager send to every request it makes to the mujin controller
        """
        controllerusernamepass = '%s:%s' % (controllerclient.controllerusername, controllerclient.controllerpassword)
        command = {"command": "Initialize",
                   "visionmanagerconfigname": visionmanagerconfigname,
                   "detectorconfigname": detectorconfigname,
                   "imagesubscriberconfigname": imagesubscriberconfigname,
                   "mujinControllerIp": controllerclient.controllerIp,
                   "mujinControllerPort": controllerclient.controllerPort,
                   "mujinControllerUsernamePass": controllerusernamepass,
                   "binpickingTaskZmqPort": controllerclient.taskzmqport,
                   "binpickingTaskHeartbeatPort": controllerclient.taskheartbeatport,
                   "binpickingTaskHeartbeatTimeout": controllerclient.taskheartbeattimeout,
                   "binpickingTaskScenePk": controllerclient.scenepk,
                   "targetname": targetname,
                   "streamerIp": streamerIp,
                   "streamerPort": streamerPort,
                   "tasktype": controllerclient.tasktype,
                   "locale": locale,
                   "targeturi": targeturi
                   }
        if defaultTaskParameters is not None:
            command["defaultTaskParameters"] = json.dumps(defaultTaskParameters)
        
        if slaverequestid is not None:
            command['slaverequestid'] = slaverequestid
        log.verbose('Initializing vision system...')
        return self._ExecuteCommand(command, timeout)

    def IsDetectionRunning(self, timeout=10.0):
        log.verbose('checking detection status...')
        command = {'command': 'IsDetectionRunning'}
        return self._ExecuteCommand(command, timeout)['isdetectionrunning']
    
    def DetectObjects(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None, fetchimagetimeout=1000, fastdetection=None, bindetection=None, request=False, timeout=10.0):
        """detects objects
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param fetchimagetimeout: max time in ms to fetch images for detection
        :param fastdetection: whether to prioritize speed
        :param bindetection: whether to detect bin
        :param request: whether to request new images instead of getting images off the buffer
        :param timeout in seconds
        :return: detected objects in world frame in a json dictionary, the translation info is in milimeter, e.g. {'objects': [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]}
        """
        log.verbose('Detecting objects...')
        command = {"command": "DetectObjects",
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        if fetchimagetimeout is not None:
            command['fetchimagetimeout'] = fetchimagetimeout
        if fastdetection is not None:
            command['fastdetection'] = 1 if fastdetection is True else 0
        if bindetection is not None:
            command['bindetection'] = 1 if bindetection is True else 0
        if request is not None:
            command['request'] = 1 if request is True else 0
        return self._ExecuteCommand(command, timeout)

    def StartDetectionThread(self, regionname=None, cameranames=None, worldResultOffsetTransform=None, voxelsize=None, pointsize=None, ignoreocclusion=None, maxage=None, fetchimagetimeout=None, obstaclename=None, starttime=None, locale=None, maxnumfastdetection=1, maxnumdetection=0, timeout=1.0):
        """starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param worldResultOffsetTransform: the offset to be applied to detection result, in the format of {'unit':  'm', 'translation_': [1,2,3], 'quat_': [1,0,0,0]}
        :param voxelsize: in meter
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param obstaclename: name of the collision obstacle
        :param starttime: min image time allowed to be used for detection, if not specified, only images taken after this call will be used
        :param timeout in seconds
        :return: returns immediately once the call completes
        """
        log.verbose('Starting detection thread...')
        command = {'command': 'StartDetectionLoop',
                   'maxnumfastdetection': maxnumfastdetection,
                   'maxnumdetection': maxnumdetection
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if voxelsize is not None:
            command['voxelsize'] = voxelsize
        if pointsize is not None:
            command['pointsize'] = pointsize
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        if fetchimagetimeout is not None:
            command['fetchimagetimeout'] = maxage
        if obstaclename is not None:
            command[obstaclename] = obstaclename
        if starttime is not None:
            command['starttime'] = starttime
        if locale is not None:
            command['locale'] = locale
        if worldResultOffsetTransform is not None:
            assert(len(worldResultOffsetTransform.get('translation_', [])) == 3)
            assert(len(worldResultOffsetTransform.get('quat_', [])) == 4)
            command['worldresultoffsettransform'] = worldResultOffsetTransform
        return self._ExecuteCommand(command, timeout)

    def StopDetectionThread(self, timeout=1.0):
        """stops detection thread
        :param timeout in seconds
        """
        log.verbose('Stopping detection thread...')
        command = {"command": "StopDetectionLoop"}
        return self._ExecuteCommand(command, timeout)

    def SendPointCloudObstacleToController(self, regionname=None, cameranames=None, detectedobjects=None, voxelsize=None, pointsize=None, obstaclename=None, maxage=None, fetchimagetimeout=1000, request=True, async=False, timeout=2.0):
        """Updates the point cloud obstacle with detected objects removed and sends it to mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param detectedobjects: a list of detected objects in world frame, the translation info is in meter, e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]
        :param voxelsize: in meter
        :param pointsize: in meter
        :param obstaclename: name of the obstacle
        :param request: whether to take new images instead of getting off buffer
        :param async: whether the call is async
        :param timeout in seconds
        """
        log.verbose('Sending point cloud obstacle to mujin controller...')
        command = {'command': 'SendPointCloudObstacleToController'}
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if detectedobjects is not None:
            command['detectedobjects'] = list(detectedobjects)
        if maxage is not None:
            command['maxage'] = maxage
        if fetchimagetimeout is not None:
            command['fetchimagetimeout'] = fetchimagetimeout
        if voxelsize is not None:
            command['voxelsize'] = voxelsize
        if pointsize is not None:
            command['pointsize'] = pointsize
        if obstaclename is not None:
            command['obstaclename'] = obstaclename
        if request is not None:
            command['request'] = 1 if request is True else 0
        if async is not None:
            command['async'] = 1 if async is True else 0
        return self._ExecuteCommand(command, timeout)

    def DetectRegionTransform(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None, fetchimagetimeout=1000, request=True, timeout=2.0):
        """Detects the transform of the region
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param fetchimagetimeout: max time in ms to fetch images for detection
        :param request: whether to take new images instead of getting off buffer
        :param timeout in seconds
        """
        log.verbose('Detecting transform of region')
        command = {'command': 'DetectRegionTransform',
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        if request is not None:
            command['request'] = 1 if request is True else 0
        return self._ExecuteCommand(command, timeout)

    def VisualizePointCloudOnController(self, regionname=None, cameranames=None, pointsize=None, ignoreocclusion=None, maxage=None, fetchimagetimeout=1000, request=True, timeout=2.0):
        """Visualizes the raw camera point clouds on mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param fetchimagetimeout: max time in ms to fetch images
        :param request: whether to take new images instead of getting off buffer
        :param timeout in seconds
        """
        log.verbose('sending camera point cloud to mujin controller...')
        command = {'command': 'VisualizePointCloudOnController',
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if pointsize is not None:
            command['pointsize'] = pointsize
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        if fetchimagetimeout is not None:
            command['fetchimagetimeout'] = fetchimagetimeout
        if request is not None:
            command['request'] = 1 if request is True else 0
        return self._ExecuteCommand(command, timeout)

    def ClearVisualizationOnController(self, timeout=1.0):
        """Clears visualization made by VisualizePointCloudOnController
        :param timeout in seconds
        """
        log.verbose("clearing visualization on mujin controller...")
        command = {'command': 'ClearVisualizationOnController'}
        return self._ExecuteCommand(command, timeout)

    def GetVisionmanagerConfig(self, timeout=1.0):
        """Gets the current visionmanager config json string
        """
        log.verbose('getting current visionmanager config...')
        command = {'command': 'GetVisionmanagerConfig'}
        return self._ExecuteCommand(command, timeout)

    def GetDetectorConfig(self, timeout=1.0):
        """Gets the current detector config json string
        """
        log.verbose('getting current detector config...')
        command = {'command': 'GetDetectorConfig'}
        return self._ExecuteCommand(command, timeout)

    def GetImagesubscriberConfig(self, timeout=1.0):
        """Gets the current imagesubscriber config json string
        """
        log.verbose('getting current imagesubscriber config...')
        command = {'command': 'GetImagesubscriberConfig'}
        return self._ExecuteCommand(command, timeout)

    def SaveVisionmanagerConfig(self, visionmanagerconfigname, config="", timeout=1.0):
        """Saves the visionmanager config to disk
        :param visionmanagerconfigname name of the visionmanager config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving visionmanager config to disk...')
        command = {'command': 'SaveVisionmanagerConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout)

    def SaveDetectorConfig(self, detectorconfigname, config="", timeout=1.0):
        """Saves the detector config to disk
        :param detectorconfigname name of the detector config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving detector config to disk...')
        command = {'command': 'SaveDetectorConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout)

    def SaveImagesubscriberConfig(self, imagesubscriberconfigname, config="", timeout=1.0):
        """Saves the imagesubscriber config to disk
        :param imagesubscriberconfigname name of the imagesubscriber config
        :param config if not specified, then saves the current config
        """
        log.verbose('saving imagesubscriber config to disk...')
        command = {'command': 'SaveImagesubscriberConfig'}
        if config != '':
            command['config'] = config
        return self._ExecuteCommand(command, timeout)

    ############################
    # internal methods
    ############################

    def SaveSnapshot(self, regionname=None, ignoreocclusion=None, maxage=None, fetchimagetimeout=1000, request=True, timeout=2.0):
        """makes each sensor save a snapshot, all files will be saved to the runtime directory of the vision server
        :param timeout in seconds
        """
        log.verbose('saving snapshot')
        command = {"command": "SaveSnapshot",
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        if fetchimagetimeout is not None:
            command['fetchimagetimeout'] = fetchimagetimeout
        if request is not None:
            command['request'] = 1 if request is True else 0
        return self._ExecuteCommand(command, timeout)

    def UpdateDetectedObjects(self, regionname, objects, state=None, sendtocontroller=False, timeout=1.0):
        """updates the list of objects the vision server maintains
        usage: user may want to process the object location locally and then update the list on the vision server to improve detection
        :param regionname: regionname
        :param objects: list of dictionaries of object info
        :param state: dict of additional object info
        :param sendtocontroller: whether to send the list to mujin controller
        :param timeout in seconds
        """
        log.verbose('Updating objects...')
        command = {"command": "UpdateDetectedObjects",
                   "regionname": regionname,
                   "detectedobjects": objects,
                   "sendtocontroller": sendtocontroller}
        if state is not None:
            state = json.dumps(state)
            command['state'] = state
        return self._ExecuteCommand(command, timeout)

    def SyncRegion(self, regionname=None, timeout=1.0):
        """updates vision server with the lastest caontainer info on mujin controller
        usage: user may want to update the region's transform on the vision server after it gets updated on the mujin controller
        :param regionname: name of the bin
        :param timeout in seconds
        """
        log.verbose('Updating region...')
        command = {'command': 'SyncRegion',
                   }
        if regionname is not None:
            command['regionname'] = regionname
        return self._ExecuteCommand(command, timeout)

    def SyncCameras(self, regionname=None, cameranames=None, timeout=1.0):
        """updates vision server with the lastest camera info on mujin controller
        usage: user may want to update a camera's transform on the vision server after it gets updated on the mujin controller
        :param regionname: name of the bin, of which the relevant camera info gets updated
        :param cameranames: a list of names of cameras, if None, then use all cameras available
        :param timeout in seconds
        """
        log.verbose('Updating cameras...')
        command = {'command': 'SyncCameras',
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        return self._ExecuteCommand(command, timeout)

    def GetCameraId(self, cameraname, timeout=1.0):
        """gets the id of the camera
        :param cameraname: name of the camera
        :param timeout in seconds
        """
        log.verbose("Getting camera id...")
        command = {'command': 'GetCameraId',
                   'cameraname': cameraname}
        return self._ExecuteCommand(command, timeout)

    def GetStatusPort(self, timeout=1.0):
        """gets the status port of visionmanager
        """
        log.verbose("Getting status port...")
        command = {'command': 'GetStatusPort'}
        return self._ExecuteCommand(command, timeout)

    def GetConfigPort(self, timeout=1.0):
        """gets the config port of visionmanager
        """
        log.verbose("Getting config port...")
        command = {'command': 'GetConfigPort'}
        return self._ExecuteCommand(command, timeout)

    def GetLatestDetectedObjects(self, returnpoints=False, timeout=1.0):
        """gets the latest detected objects
        """
        log.verbose("Getting latest detected objects...")
        command = {'command': 'GetLatestDetectedObjects', 'returnpoints': returnpoints}
        return self._ExecuteCommand(command, timeout)

    def _SendConfiguration(self, configuration, timeout=2.0):
        try:
            return self._configurationsocket.SendCommand(configuration, timeout=timeout)
        except:
            log.exception('occured while sending configuration %r', configuration)
            raise

    def Ping(self, timeout=2.0):
        return self._SendConfiguration({"command": "Ping"}, timeout=timeout)

    def Cancel(self, timeout=2.0):
        log.info('canceling command...')
        response = self._SendConfiguration({"command": "Cancel"}, timeout=timeout)
        log.info('command is stopped')
        return response

    def Quit(self, timeout=1.0):
        log.info('stopping visionserver...')
        response = self._SendConfiguration({"command": "Quit"}, timeout=timeout)
        log.info('visionserver is stopped')
        return response

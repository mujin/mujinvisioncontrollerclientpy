# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
# Mujin vision controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from mujincontrollerclient import zmqclient
from . import VisionControllerClientError


class VisionControllerClient(object):
    """mujin vision controller client for bin picking task
    """
    def __init__(self, visioncontrollerhostname, visioncontrollerport, detectorConfigurationFilename, imagesubscriberConfigurationFilename, targetname, controllerclient):
        """connects to vision server, initializes vision server, and sets up parameters
        :param visioncontrollerhostname: hostname of the vision controller, e.g. visioncontroller1
        :param visioncontrollerport: port of the vision controller, e.g. 5557
        :param detectorConfigurationFilename: name of the config file for detecting the target object, e.g. /home/controller/mujin/visioncontroller/mujindetection/plasticnut.json
        :param imagesubscriberConfigurationFilename: name of the config file for image subscribers, e.g. /home/controller/mujin/visioncontroller/mujindetection/imagesubscriber.json
        :param targetname: name of the target object
        :param controllerclient: pointer to the BinpickingControllerClient that connects to the mujin controller we want the vision server to talk to
        """
        self.visioncontrollerhostname = visioncontrollerhostname
        self.visioncontrollerport = visioncontrollerport
        self._zmqclient = zmqclient.ZmqClient(visioncontrollerhostname, visioncontrollerport)

        # initialize vision server
        self.detectorConfigurationFilename = detectorConfigurationFilename
        self.imagesubscriberConfigurationFilename = imagesubscriberConfigurationFilename
        self.controllerclient = controllerclient

        self.InitializeVisionServer(detectorConfigurationFilename, imagesubscriberConfigurationFilename, targetname, controllerclient)

    def _ExecuteCommand(self, command, timeout=1.0):
        response = self._zmqclient.SendCommand(command, timeout)
        if 'computationtime' in response:
            log.info('%s took %f seconds' % (command['command'], response['computationtime'] / 1000.0))
        else:
            log.info('%s executed successfully' % (command['command']))
        if 'error' in response:
            raise VisionControllerClientError(response['error'])
        return response

    def InitializeVisionServer(self, detectorConfigurationFilename, imagesubscriberConfigurationFilename, targetname, controllerclient, timeout=1.0):
        """initializes vision server
        :param detectorConfigurationFilename: name of the config file for detecting the target object, e.g. /home/controller/mujin/visioncontroller/mujindetection/plasticnut.json
        :param imagesubscriberConfigurationFilename: name of the config file for image subscribers, e.g. /home/controller/mujin/visioncontroller/mujindetection/imagesubscriber.json
        :param controllerclient: pointer to the BinpickingControllerClient that connects to the mujin controller we want the vision server to talk to
        :param timeout in seconds
        """
        controllerusernamepass = '%s:%s' % (controllerclient.controllerusername, controllerclient.controllerpassword)
        command = {"command": "Initialize",
                   "detectorConfigurationFilename": detectorConfigurationFilename,
                   "imagesubscriberConfigurationFilename": imagesubscriberConfigurationFilename,
                   "mujinControllerIp": controllerclient.controllerIp,
                   "mujinControllerPort": controllerclient.controllerPort,
                   "mujinControllerUsernamePass": controllerusernamepass,
                   "robotControllerUri": controllerclient.robotControllerUri,
                   "binpickingTaskZmqPort": controllerclient.taskzmqport,
                   "binpickingTaskHeartbeatPort": controllerclient.taskheartbeatport,
                   "binpickingTaskHeartbeatTimeout": controllerclient.taskheartbeattimeout,
                   "binpickingTaskScenePk": controllerclient.scenepk,
                   "robotname": controllerclient.robotname,
                   "targetname": targetname,
                   "tasktype": controllerclient.tasktype
                   }

        log.info('Initializing vision system...')
        return self._ExecuteCommand(command, timeout)

    def DetectObjects(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None, timeout=1.0):
        """detects objects
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param timeout in seconds
        :return: detected objects in world frame in a json dictionary, the translation info is in milimeter, e.g. {'objects': [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]}
        """
        log.info('Detecting objects...')
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
        return self._ExecuteCommand(command, timeout)

    def StartDetectionThread(self, regionname=None, cameranames=None, voxelsize=None, pointsize=None, ignoreocclusion=None, maxage=None, obstaclename=None, timeout=1.0):
        """starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param voxelsize: in meter
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param obstaclename: name of the collision obstacle
        :param timeout in seconds
        :return: returns immediately once the call completes
        """
        log.info('Starting detection thread...')
        command = {"command": "StartDetectionLoop",
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
        if obstaclename is not None:
            command[obstaclename] = obstaclename
        return self._ExecuteCommand(command, timeout)

    def StopDetectionThread(self, timeout=1.0):
        """stops detection thread
        :param timeout in seconds
        """
        log.info('Stopping detection thread...')
        command = {"command": "StopDetectionLoop"}
        return self._ExecuteCommand(command, timeout)

    def SendPointCloudObstacleToController(self, regionname=None, cameranames=None, detectedobjects=None, voxelsize=None, pointsize=None, obstaclename=None, timeout=1.0):
        """Updates the point cloud obstacle with detected objects removed and sends it to mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param detectedobjects: a list of detected objects in world frame, the translation info is in meter, e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]
        :param voxelsize: in meter
        :param pointsize: in meter
        :param obstaclename: name of the obstacle
        :param timeout in seconds
        """
        log.info('Sending point cloud obstacle to mujin controller...')
        command = {'command': 'SendPointCloudObstacleToController'}
        if regionname is not None:
            command['regionname'] = regionname
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if detectedobjects is not None:
            command['detectedobjects'] = list(detectedobjects)
        if voxelsize is not None:
            command['voxelsize'] = voxelsize
        if pointsize is not None:
            command['pointsize'] = pointsize
        if obstaclename is not None:
            command['obstaclename'] = obstaclename
        return self._ExecuteCommand(command, timeout)

    def DetectRegionTransform(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None, timeout=1.0):
        """Detects the transform of the region
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param timeout in seconds
        """
        log.info('Detecting transform of region')
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
        return self._ExecuteCommand(command, timeout)

    def VisualizePointCloudOnController(self, regionname=None, cameranames=None, pointsize=None, ignoreocclusion=None, maxage=None, timeout=1.0):
        """Visualizes the raw camera point clouds on mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :param timeout in seconds
        """
        log.info('sending camera point cloud to mujin controller...')
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
        return self._ExecuteCommand(command, timeout)

    def ClearVisualizationOnController(self, timeout=1.0):
        """Clears visualization made by VisualizePointCloudOnController
        :param timeout in seconds
        """
        log.info("clearing visualization on mujin controller...")
        command = {'command': 'ClearVisualizationOnController'}
        return self._ExecuteCommand(command, timeout)

    ############################
    # internal methods
    ############################

    def SaveSnapshot(self, regionname=None, ignoreocclusion=None, maxage=None, timeout=1.0):
        """makes each sensor save a snapshot, all files will be saved to the runtime directory of the vision server
        :param timeout in seconds
        """
        log.info('saving snapshot')
        command = {"command": "SaveSnapshot",
                   }
        if regionname is not None:
            command['regionname'] = regionname
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        return self._ExecuteCommand(command, timeout)

    def UpdateDetectedObjects(self, objects, sendtocontroller=False, timeout=1.0):
        """updates the list of objects the vision server maintains
        usage: user may want to process the object location locally and then update the list on the vision server to improve detection
        :param objects: list of dictionaries of object info in world frame, the translation info is in meter, e.g. [{'name':'target_0', 'translation': [1,2,3], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'score': 0.8}]
        :param sendtocontroller: whether to send the list to mujin controller
        :param timeout in seconds
        """
        log.info('Updating objects...')
        command = {"command": "UpdateDetectedObjects",
                   "detectedobjects": objects,
                   "sendtocontroller": sendtocontroller}
        return self._ExecuteCommand(command, timeout)

    def SyncRegion(self, regionname=None, timeout=1.0):
        """updates vision server with the lastest caontainer info on mujin controller
        usage: user may want to update the region's transform on the vision server after it gets updated on the mujin controller
        :param regionname: name of the bin
        :param timeout in seconds
        """
        log.info('Updating region...')
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
        log.info('Updating cameras...')
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
        log.info("Getting camera id...")
        command = {'command': 'GetCameraId',
                   'cameraname': cameraname}
        return self._ExecuteCommand(command, timeout)

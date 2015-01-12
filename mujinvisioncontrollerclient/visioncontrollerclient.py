# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc
# Mujin vision controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from mujincontrollerclient import zmqclient


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
        self.regionname = controllerclient.regionname

        self.InitializeVisionServer(detectorConfigurationFilename, imagesubscriberConfigurationFilename, targetname, controllerclient)

    def InitializeVisionServer(self, detectorConfigurationFilename, imagesubscriberConfigurationFilename, targetname, controllerclient):
        """initializes vision server
        :param detectorConfigurationFilename: name of the config file for detecting the target object, e.g. /home/controller/mujin/visioncontroller/mujindetection/plasticnut.json
        :param imagesubscriberConfigurationFilename: name of the config file for image subscribers, e.g. /home/controller/mujin/visioncontroller/mujindetection/imagesubscriber.json
        :param controllerclient: pointer to the BinpickingControllerClient that connects to the mujin controller we want the vision server to talk to
        """
        controllerusernamepass = '%s:%s'%(controllerclient.controllerusername, controllerclient.controllerpassword)
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
                   "regionname": controllerclient.regionname,
                   "targetname": targetname,
                   "tasktype": controllerclient.tasktype
                   }

        log.info('Initializing vision system...')
        response = {}
        try:
            response = self._zmqclient.SendCommand(command)
            log.info('initialized server, took: %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def DetectObjects(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None):
        """detects objects
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :return: detected objects in world frame in a json dictionary, the translation info is in milimeter, e.g. {'objects': [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]}
        """
        log.info('Detecting objects...')
        if regionname is None:
            regionname = self.regionname
        command = {"command": "DetectObjects",
                   "regionname": regionname,
                   }
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('detectd %d objects, took: %s seconds'%(len(response['objects']),response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def StartDetectionThread(self, regionname=None, cameranames=None, voxelsize=None, pointsize=None, ignoreocclusion=None, maxage=None):
        """starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.
        :param regionname: name of the bin
        :param cameranames: a list of names of cameras to use for detection, if None, then use all cameras available
        :param voxelsize: in meter
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        :return: returns immediately once the call completes
        """
        log.info('Starting detection thread...')
        if regionname is None:
            regionname = self.regionname
        command = {"command": "StartDetectionLoop",
                   "regionname": regionname,
                   }
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
        response = self._zmqclient.SendCommand(command)
        log.info(response)
        return response

    def StopDetectionThread(self):
        """stops detection thread
        """
        log.info('Stopping detection thread...')
        command = {"command": "StopDetectionLoop"}
        response = self._zmqclient.SendCommand(command)
        log.info(response)
        return response

    def SendPointCloudObstacleToController(self, regionname=None, cameranames=None, detectedobjects=None, voxelsize=None, pointsize=None):
        """Updates the point cloud obstacle with detected objects removed and sends it to mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param detectedobjects: a list of detected objects in world frame, the translation info is in meter, e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'confidence': 0.8}]
        :param voxelsize: in meter
        :param pointsize: in meter
        """
        log.info('Sending point cloud obstacle to mujin controller...')
        if regionname is None:
            regionname = self.regionname
        command = {'command': 'SendPointCloudObstacleToController',
                   'regionname': regionname}
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if detectedobjects is not None:
            command['detectedobjects'] = list(detectedobjects)
        if voxelsize is not None:
            command['voxelsize'] = voxelsize
        if pointsize is not None:
            command['pointsize'] = pointsize
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('sent point cloud obstacle, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def DetectRegionTransform(self, regionname=None, cameranames=None, ignoreocclusion=None, maxage=None):
        """Detects the transform of the region
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        """
        log.info('Detecting transform of region')
        if regionname is None:
            regionname = self.regionname
        command = {'command': 'DetectRegionTransform',
                   'regionname': regionname
                   }
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('Detected region transform, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def VisualizePointCloudOnController(self, regionname=None, cameranames=None, pointsize=None, ignoreocclusion=None, maxage=None):
        """Visualizes the raw camera point clouds on mujin controller
        :param regionname: name of the region
        :param cameranames: a list of camera names to use for visualization, if None, then use all cameras available
        :param pointsize: in meter
        :param ignoreocclusion: whether to skip occlusion check
        :param maxage: max time difference in ms allowed between the current time and the timestamp of image used for detection, 0 means infinity
        """
        log.info('sending camera point cloud to mujin controller...')
        if regionname is None:
            regionname = self.regionname
        command = {'command': 'VisualizePointCloudOnController',
                   'regionname': regionname
                   }
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        if pointsize is not None:
            command['pointsize'] = pointsize
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('sent point cloud, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def ClearVisualizationOnController(self):
        """Clears visualization made by VisualizePointCloudOnController
        """
        log.info("clearing visualization on mujin controller...")
        command = {'command': 'ClearVisualizationOnController'}
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('cleared visualization, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    ############################
    # internal methods
    ############################

    def SaveSnapshot(self, regionname=None, ignoreocclusion=None, maxage=None):
        """makes each sensor save a snapshot, all files will be saved to the runtime directory of the vision server
        """
        log.info('saving snapshot')
        if regionname is None:
            regionname = self.regionname
        command = {"command": "SaveSnapshot",
                   "regionname": regionname
                   }
        if ignoreocclusion is not None:
            command['ignoreocclusion'] = 1 if ignoreocclusion is True else 0
        if maxage is not None:
            command['maxage'] = maxage
        response = self._zmqclient.SendCommand(command)
        return response

    def UpdateDetectedObjects(self, objects, sendtocontroller=False):
        """updates the list of objects the vision server maintains
        usage: user may want to process the object location locally and then update the list on the vision server to improve detection
        :param objects: list of dictionaries of object info in world frame, the translation info is in meter, e.g. [{'name':'target_0', 'translation': [1,2,3], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'score': 0.8}]
        :param sendtocontroller: whether to send the list to mujin controller
        """
        log.info('Updating objects...')
        command = {"command": "UpdateDetectedObjects",
                   "detectedobjects": objects,
                   "sendtocontroller": sendtocontroller}
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('updated objects, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def SyncRegion(self, regionname=None):
        """updates vision server with the lastest caontainer info on mujin controller
        usage: user may want to update the region's transform on the vision server after it gets updated on the mujin controller
        :param regionname: name of the bin
        """
        log.info('Updating region...')
        if regionname is None:
            regionname = self.regionname
        command = {'command': 'SyncRegion',
                   'regionname': regionname}
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('updated region, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def SyncCameras(self, regionname=None, cameranames=None):
        """updates vision server with the lastest camera info on mujin controller
        usage: user may want to update a camera's transform on the vision server after it gets updated on the mujin controller
        :param regionname: name of the bin, of which the relevant camera info gets updated
        :param cameranames: a list of names of cameras, if None, then use all cameras available
        """
        log.info('Updating cameras...')
        if regionname is None:
            regionname = self.regionname
        command = {'command': 'SyncCameras',
                   'regionname': regionname}
        if cameranames is not None:
            command['cameranames'] = list(cameranames)
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('updated cameras, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

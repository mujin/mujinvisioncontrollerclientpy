# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc
# Mujin vision controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from . import visioncontrollerclient

class CalibrationVisionControllerClient(visioncontrollerclient.VisionControllerClient):
    """mujin vision controller client for calibration
    """
    def __init__(self, visioncontrollerhostname, visioncontrollerport, objectconfigurationfilename, binpickingcontrollerclient):
        """connects to vision server, initializes vision server, and sets up parameters
        :param visioncontrollerhostname: hostname of the vision controller, e.g. visioncontroller1
        :param visioncontrollerport: port of the vision controller, e.g. 5557
        :param objectconfigurationfilename: name of the config file for the target object, e.g. /home/controller/mujin/visioncontroller/caddata/koalamarch.conf
        :param binpickingcontrollerclient: pointer to the BinpickingControllerClient that connects to the mujin controller we want the vision server to talk to
        """
        super(CalibrationVisionControllerClient, self).__init__(visioncontrollerhostname, visioncontrollerport, objectconfigurationfilename, binpickingcontrollerclient)

    def StartCalibration(self, sensorindex = 1, numsamples = 15):
        """starts calibration
        :param sensorindex: id of the camera, assuming camera has name of the format 'camera_id'
        :param numsamples: number of samples to capture and use for calibration
        """
        log.info('Starting calibration...')
        command = {"command": "StartCalibration",
                   "sensorindex": sensorindex,
                   "numsamples": numsamples}
        response=self._zmqclient.SendCommand(command)
        try:
            log.info('calibration finished, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

'''
#TODO:
    def Calibrate(self,singlecameraname,cachedir, numsamples):
        log.info('calibrate')
        command = {"command": "_Calibrate", "singlecameraname": singlecameraname, "cachedir": cachedir, "numsamples": numsamples}
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('updated box, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response
    
    def CalibrateStereo(self,cameranames,cachedir, numsamples):
        log.info('calibrate')
        command = {"command": "_CalibrateStereo", "cameraname": cameranames, "cachedir": cachedir, "numsamples": numsamples}
        response = self._zmqclient.SendCommand(command)
        try:
            log.info('updated box, took %s seconds'%(response['computationtime']/1000.0))
        except:
            log.info(response)
        return response

    def StartStereoCalibration(self, cameranames, numsamples = 10):
        log.info('start stereo calibration')
        command = {"command": "StartStereoCalibration", "cameraname": cameranames, "numsamples": numsamples}
        response=self._zmqclient.SendCommand(command)
        return response

    def FindPattern(cameraname):
        command = {"command": "_FindPattern", "cameraname": cameraname}
        response=self._zmqclient.SendCommand(command)

        if (len(response["objects"]) != 2):
            log.info('invalid response')
            return response

        Tpatterntoworld = numpy.eye(4)
        Tcalibboardtoflange = numpy.eye(4)
        Tcornertocalibboard = numpy.eye(4)

        Tpatterntoworld[0:3,0:3] = numpy.array(response["objects"][0]['rotationmat'])
        Tpatterntoworld[0:3,3] = numpy.array(response["objects"][0]['translation'])/1000.0

        Tcalibboardtoflange[0:3,0:3] = numpy.array(response["objects"][1]['rotationmat'])
        Tcalibboardtoflange[0:3,3] = numpy.array(response["objects"][1]['translation'])/1000.0

        Tcornertocalibboard[0:3,3] = numpy.array([0.125, -0.125, 0.0050])

        Tcornerposes = []
        n = 18
        for i in range(0,n):
            T = None
            theta1 = 2*numpy.pi/n * i
            T1 = numpy.eye(4)
            T2 = numpy.eye(4)
            T3 = numpy.eye(4)
            T1[0:3,0:3] = rotationMatrixFromAxisAngle([0,0,1],theta1)
            T = numpy.dot(Tpatterntoworld,T1)
            T2[0:3,0:3] = rotationMatrixFromAxisAngle([1,0,0],30.0/180*numpy.pi)
            T = numpy.dot(T,T2)
            for theta2 in [25,45,65]:
                T3[0:3,0:3] = rotationMatrixFromAxisAngle([0,0,1],theta2/180*numpy.pi)
                T = numpy.dot(T,T3)
                Tcornerposes.append(T) 

        Tfrangeposes = [numpy.dot(cornerpose, numpy.invert(numpy.dot(Tcalibboardtoflange, Tcornertocalibboard)))  for cornerpose in Tcornerposes]
'''

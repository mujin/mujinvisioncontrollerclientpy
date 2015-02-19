# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from mujinvisioncontrollerclient.zmqclient import ZmqClient


class VisionControllerClientBase(object):
    def __init__(self, visioncontrollerhostname, visioncontrollerport):
        """
        :param visioncontrollerhostname: hostname of the vision controller, e.g. visioncontroller1
        :param visioncontrollerport: port of the vision controller, e.g. 5557
        """
        self.visioncontrollerhostname = visioncontrollerhostname
        self.visioncontrollerport = visioncontrollerport
        self._zmqclient = ZmqClient(visioncontrollerhostname, visioncontrollerport)

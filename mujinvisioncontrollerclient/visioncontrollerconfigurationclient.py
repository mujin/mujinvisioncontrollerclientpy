# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
# Mujin vision controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports
import argparse

# mujin imports
from mujincontrollerclient import zmqclient


class VisionControllerConfigurationClient(object):
    """mujin vision controller client for bin picking task
    """

    def __init__(self, visioncontrollerhostname, visioncontrollerport):
        """connects to vision server, initializes vision configuration server(?)
        :param visioncontrollerhostname: hostname of the vision controller, e.g. visioncontroller1
        :param visioncontrollerport: port of the vision configuration controller, e.g. 7006
        """
        self.visioncontrollerhostname = visioncontrollerhostname
        self.visioncontrollerport = visioncontrollerport
        self._zmqclient = zmqclient.ZmqClient(visioncontrollerhostname, visioncontrollerport)

    def Cancel(self):
        log.info('canceling command...')
        command = {"command": "Cancel",
                   }
        response = {}
        try:
            response = self._zmqclient.SendCommand(command)
        except:
            log.info(response)
        log.info('command is stopped')
        return response

    def Quit(self):
        log.info('stopping visionserver...')
        command = {"command": "Quit",
                   }
        response = {}
        try:
            response = self._zmqclient.SendCommand(command, 0) # no blocking
        except:
            log.info(response)
        log.info('visionserver is stopped')
        return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='vision server status monintor')
    parser.add_argument('--hostname', action='store', default="visioncontroller1", help="e.g. visioncontroller1")
    parser.add_argument('--statusport', action='store', default=7006, help="e.g. 7006")
    options = parser.parse_args()

    confclient = VisionControllerConfigurationClient(options.hostname, options.statusport)
    #from IPython.terminal import embed; ipshell=embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())

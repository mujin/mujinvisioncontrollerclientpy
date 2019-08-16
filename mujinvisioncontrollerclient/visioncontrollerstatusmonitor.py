# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
# Mujin vision controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports
import argparse
import simplejson
import six
import typing
# mujin imports
# FIXME: cannot find this in latest mujincontrollerclient
from mujincontrollerclient import zmqsubscriber


class VisionControllerStatusMonitor(object):

    class Status(object):
        lost, pending, active, preempting, preempted, succeeded, paused, aborted  = range(8)

        @staticmethod
        def GetStatusString(code):
            # type: (int) -> str
            for key, val in six.iteritems(VisionControllerStatusMonitor.Status.__dict__):
                if val == code:
                    return key
            return ""

        @staticmethod
        def GetStatusCode(string):
            # type: (str) -> int
            for key, val in six.iteritems(VisionControllerStatusMonitor.Status.__dict__):
                if key == string:
                    return val
            return VisionControllerStatusMonitor.Status.lost

    def __init__(self, visioncontrollerhostname, visioncontrollerstatusport):
        # type: (str, int) -> None
        """connects to vision status publisher.
        :param visioncontrollerhostname: hostname of the vision controller, e.g. visioncontroller1
        :param visioncontrollerstatusport: port of the vision status publisher, e.g. 7007
        """
        self.visioncontrollerhostname = visioncontrollerhostname
        self.visioncontrollerstatusport = visioncontrollerstatusport
        self._zmqsubscriber = zmqsubscriber.ZmqSubscriber(visioncontrollerhostname, visioncontrollerstatusport)

    def StartMonitoring(self):
        # type: () -> None
        self._zmqsubscriber.StartSubscription()

    def StopMonitoring(self):
        # type: () -> None
        self._zmqsubscriber.StopSubscription()

    def GetStatus(self):
        # type: () -> typing.Tuple[float, int, str]
        msg = self._zmqsubscriber.GetMessage()
        timestamp = None
        message = ""
        if msg is "":
            code = VisionControllerStatusMonitor.Status.lost
        else:
            d = simplejson.loads(msg)
            timestamp = d['timestamp']
            code = VisionControllerStatusMonitor.Status.GetStatusCode(d['status'])
            message = d['message']
        return timestamp, code, message

    def __enter__(self):
        # type: () -> "VisionControllerStatusMonitor"
        self.StartMonitoring()
        return self

    def __exit__(self, type, value, traceback):
        # type: (typing.Any, typing.Any, typing.Any) -> None
        self.StopMonitoring()


paststatus = []
pasttimestamp = []
pastmessage = []


def PrintStatus(timestamp, statuscode, message):
    # type: (float, int, str) -> None
    status = VisionControllerStatusMonitor.Status.GetStatusString(statuscode)
    if status != paststatus[0] or timestamp != pasttimestamp[0] or message != pastmessage[0]:
        if status != paststatus[0]:
            paststatus[1:] = paststatus[:-1]
            paststatus[0] = status
        if timestamp != pasttimestamp[0]:
            pasttimestamp[1:] = pasttimestamp[:-1]
            pasttimestamp[0] = timestamp
        if message != pastmessage[0]:
            pastmessage[1:] = pastmessage[:-1]
            pastmessage[0] = message
        line = []
        line.extend(["status:", status, " ["])
        for i in range(len(paststatus)):
            line.append(paststatus[i])
            if i == len(paststatus)-1:
                line.append("]")
        six.print_(*line)
        six.print_(timestamp, message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='vision server status monintor')
    parser.add_argument('--hostname', action='store', default="visioncontroller1", help="e.g. visioncontroller1")
    parser.add_argument('--statusport', action='store', default=7007, help="e.g. 7007")
    parser.add_argument('--historysize', action='store', default=5, help="e.g. 5")
    options = parser.parse_args()

    statusmonitor = VisionControllerStatusMonitor(options.hostname, options.statusport)
    paststatus = [None] * options.historysize
    pasttimestamp = [None] * options.historysize
    pastmessage = [None] * options.historysize
    import time
    with statusmonitor:
        while True:
            timestamp, statuscode, message = statusmonitor.GetStatus()
            while statuscode == VisionControllerStatusMonitor.Status.lost:
                six.print_("publisher seems to be offline, try again in 3 seconds")
                statusmonitor.StopMonitoring()
                time.sleep(3)
                statusmonitor.StartMonitoring()
                time.sleep(0.1)
                timestamp, statuscode, message = statusmonitor.GetStatus()
                PrintStatus(timestamp, statuscode, message)
            PrintStatus(timestamp, statuscode, message)
            # time.sleep(0.05)

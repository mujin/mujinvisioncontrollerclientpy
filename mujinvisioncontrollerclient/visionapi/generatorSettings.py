# -*- coding: utf-8 -*-
# Copyright (C) 2023 Mujin, Inc.

from collections import OrderedDict
from copy import deepcopy

from . import _
from mujincommon.dictutil import MergeDicts

from . import components


template = ('visionapi', 'templates/client_template.py.mako')

templateArgs = {
    'clientTaskName': 'binpicking',
    'parentClassFile': 'VisionControllerClient',
    'parentClassName': 'VisionControllerClient',
}

x_specModifications = {
    'services': OrderedDict([
        ('StartObjectDetectionTask', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('systemState', {
                    'paramOrderingIndex': 1,
                }),
                ('visionTaskParameters', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                )),
                ('ignoredArgs', {
                    'description': _('These arguments may be passed to the method, but are ignored.'),
                    'x-specialCase': {
                        'omitRegularAssignment': True,
                    },
                }),
            ]),
            'returns': {
                'description': _('Returns immediately once the call completes'),
            },
            'x-methodStartSetup': "log.verbose('Starting detection thread...')",
        }),
        ('StartContainerDetectionTask', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('systemState', {
                    'paramOrderingIndex': 1,
                }),
                ('visionTaskParameters', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                )),
                ('ignoredArgs', {
                    'description': _('These arguments may be passed to the method, but are ignored.'),
                    'x-specialCase': {
                        'omitRegularAssignment': True,
                    },
                }),
            ]),
            'returns': {
                'description': _('Returns immediately once the call completes'),
            },
            'x-methodStartSetup': "log.verbose('Starting container detection thread...')",
        }),
        ('StartVisualizePointCloudTask', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('systemState', {
                    'paramOrderingIndex': 1,
                }),
                ('visionTaskParameters', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                )),
            ]),
            'x-methodStartSetup': "log.verbose('Starting visualize pointcloud thread...')",
        }),
        ('StopTask', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('taskIds', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('taskTypes', {
                    'paramOrderingIndex': 3,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 4,
                }),
                ('waitForStop', {
                    'default': True,
                    'isRequired': True,
                    'paramOrderingIndex': 5,
                }),
                ('removeTask', {
                    'default': False,
                    'isRequired': True,
                    'paramOrderingIndex': 6,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 8,
                    }
                )),
                ('fireandforget', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'paramOrderingIndex': 7,
                    }
                )),
            ]),
            'x-methodStartSetup': "log.verbose('Stopping detection thread...')",
        }),
        ('ResumeTask', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('taskIds', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('taskTypes', {
                    'paramOrderingIndex': 3,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 4,
                }),
                ('waitForStop', {
                    'paramOrderingIndex': 5,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 7,
                    }
                )),
                ('fireandforget', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'paramOrderingIndex': 6,
                    }
                )),
            ]),
            'x-methodStartSetup': "log.verbose('Resuming detection thread...')",
        }),
        ('BackupVisionLog', {
            'parameters': OrderedDict([
                ('cycleIndex', {
                    'paramOrderingIndex': 0,
                }),
                ('sensorTimestamps', {
                    'paramOrderingIndex': 1,
                }),
                ('fireandforget', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'default': False,
                        'paramOrderingIndex': 2,
                    }
                )),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 2.0,
                        'paramOrderingIndex': 3,
                    }
                )),
            ]),
            'serversideCommandName': 'BackupDetectionLogs',
        }),
        ('GetLatestDetectedObjects', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                )),
            ]),
        }),
        ('GetLatestDetectionResultImages', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('newerThanResultTimestampMS', {
                    'default': 0,
                    'isRequired': True,
                    'mapsTo': 'newerThanResultTimestampMS',
                    'paramOrderingIndex': 3,
                }),
                ('sensorSelectionInfo', {
                    'paramOrderingIndex': 4,
                }),
                ('metadataOnly', {
                    'default': False,
                    'isRequired': True,
                    'paramOrderingIndex': 5,
                }),
                ('imageTypes', {
                    'paramOrderingIndex': 6,
                }),
                ('limit', {
                    'paramOrderingIndex': 7,
                }),
                ('blockwait', {
                    'default': True,
                    'paramOrderingIndex': 8,
                    'x-doNotAddToPayload': True,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 9,
                    }
                )),
            ]),
            'x-methodStartSetup': 'log.verbose("Getting latest detection result images...")',
            'x-modifiedReturnStatement': 'return self._ExecuteCommand(command, timeout=timeout, recvjson=False, blockwait=blockwait)',
            'x-omitRegularReturnStatement': True,
        }),
        ('GetDetectionHistory', {
            'parameters': OrderedDict([
                ('timestamp', {
                    'paramOrderingIndex': 0,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 1,
                    }
                )),
            ]),
            'x-methodStartSetup': 'log.verbose("Getting detection result at %r ...", timestamp)',
            'x-modifiedReturnStatement': 'return self._ExecuteCommand(command, timeout=timeout, recvjson=False)',
            'x-omitRegularReturnStatement': True,
        }),
        ('GetVisionStatistics', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                )),
            ]),
        }),
        ('Ping', {
            'parameters': OrderedDict([
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                )),
            ]),
        }),
        ('SetLogLevel', {
            'parameters': OrderedDict([
                ('componentLevels', {
                    'paramOrderingIndex': 0,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 1,
                    }
                )),
            ]),
        }),
        ('Cancel', {
            'parameters': OrderedDict([
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                )),
            ]),
            'x-methodStartSetup': "log.info('Canceling command...')",
            'x-modifiedReturnStatement': "response = self._SendConfiguration(command, timeout=timeout)\nlog.info('Command is stopped.')\nreturn response\n",
            'x-omitRegularReturnStatement': True,
        }),
        ('Quit', {
            'parameters': OrderedDict([
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                )),
            ]),
            'x-methodStartSetup': "log.info('Stopping visionserver...')",
            'x-modifiedReturnStatement': "response = self._SendConfiguration(command, timeout=timeout)\nlog.info('Visionserver is stopped.')\nreturn response\n",
            'x-omitRegularReturnStatement': True,
        }),
        ('GetTaskStateService', {
            'parameters': OrderedDict([
                ('taskId', {
                    'paramOrderingIndex': 0,
                }),
                ('cycleIndex', {
                    'paramOrderingIndex': 1,
                }),
                ('taskType', {
                    'paramOrderingIndex': 2,
                }),
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 4.0,
                        'paramOrderingIndex': 3,
                    }
                )),
            ]),
            'serversideCommandName': 'GetTaskState',
        }),
        ('GetPublishedStateService', {
            'parameters': OrderedDict([
                ('timeout', MergeDicts(
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 4.0,
                        'paramOrderingIndex': 0,
                    }
                )),
            ]),
            'serversideCommandName': 'GetPublishedState',
        }),
    ]),
}

generatorSettingsDict = {
    'template': template,
    'x-specModifications': x_specModifications,
    'templateArgs': templateArgs
}

# -*- coding: utf-8 -*-
# Copyright (C) 2023 Mujin, Inc.

from collections import OrderedDict
from copy import deepcopy

from . import _
from mujincommon.dictutil import MergeDicts

from . import components


template = (__name__, 'templates/client_template.py.mako')

templateArgs = {
    'clientTaskName': 'binpicking',
    'parentClassFile': 'VisionControllerClient',
    'parentClassName': 'VisionControllerClient',
}

x_specModifications = {
    'services': OrderedDict([
        ('StartObjectDetectionTask', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'systemState',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'visionTaskParameters',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                ])[0],
                {
                    'name': 'ignoredArgs',
                    'description': _('These arguments may be passed to the method, but are ignored.'),
                    'x-specialCase': {
                        'omitRegularAssignment': True,
                    },
                },
            ],
            'returns': {
                'description': _('Returns immediately once the call completes'),
            },
            'x-methodStartSetup': "log.verbose('Starting detection thread...')",
        }),
        ('StartContainerDetectionTask', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'systemState',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'visionTaskParameters',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                ])[0],
                {
                    'name': 'ignoredArgs',
                    'description': _('These arguments may be passed to the method, but are ignored.'),
                    'x-specialCase': {
                        'omitRegularAssignment': True,
                    },
                },
            ],
            'returns': {
                'description': _('Returns immediately once the call completes'),
            },
            'x-methodStartSetup': "log.verbose('Starting container detection thread...')",
        }),
        ('StartVisualizePointCloudTask', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'systemState',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'visionTaskParameters',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                ])[0],
            ],
            'x-methodStartSetup': "log.verbose('Starting visualize pointcloud thread...')",
        }),
        ('StopTask', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'taskIds',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                {
                    'name': 'taskTypes',
                    'paramOrderingIndex': 3,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 4,
                },
                {
                    'name': 'waitForStop',
                    'schema': {
                        'default': True,
                    },
                    'isRequired': True,
                    'paramOrderingIndex': 5,
                },
                {
                    'name': 'removeTask',
                    'schema': {
                        'default': False
                    },
                    'isRequired': True,
                    'paramOrderingIndex': 6,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 8,
                    }
                ])[0],
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'paramOrderingIndex': 7,
                    }
                ])[0],
            ],
            'x-methodStartSetup': "log.verbose('Stopping detection thread...')",
        }),
        ('ResumeTask', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'taskIds',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                {
                    'name': 'taskTypes',
                    'paramOrderingIndex': 3,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 4,
                },
                {
                    'name': 'waitForStop',
                    'paramOrderingIndex': 5,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 7,
                    }
                ])[0],
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'paramOrderingIndex': 6,
                    }
                ])[0],
            ],
            'x-methodStartSetup': "log.verbose('Resuming detection thread...')",
        }),
        ('BackupVisionLog', {
            'parameters': [
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'sensorTimestamps',
                    'paramOrderingIndex': 1,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['fireandforget']),
                    {
                        'default': False,
                        'paramOrderingIndex': 2,
                    }
                ])[0],
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 2.0,
                        'paramOrderingIndex': 3,
                    }
                ])[0],
            ],
            'serversideCommandName': 'BackupDetectionLogs',
        }),
        ('GetLatestDetectedObjects', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                ])[0],
            ],
        }),
        ('GetLatestDetectionResultImages', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                {
                    'name': 'newerThanResultTimestampMS',
                    'schema': {
                        'default': 0,
                    },
                    'isRequired': True,
                    'mapsTo': 'newerThanResultTimestampMS',
                    'paramOrderingIndex': 3,
                },
                {
                    'name': 'sensorSelectionInfo',
                    'paramOrderingIndex': 4,
                },
                {
                    'name': 'metadataOnly',
                    'schema': {
                        'default': False,
                    },
                    'isRequired': True,
                    'paramOrderingIndex': 5,
                },
                {
                    'name': 'imageTypes',
                    'paramOrderingIndex': 6,
                },
                {
                    'name': 'limit',
                    'paramOrderingIndex': 7,
                },
                {
                    'name': 'blockwait',
                    'schema': {
                        'default': True,
                    },
                    'paramOrderingIndex': 8,
                    'x-doNotAddToPayload': True,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 9,
                    }
                ])[0],
            ],
            'x-methodStartSetup': 'log.verbose("Getting latest detection result images...")',
            'x-modifiedReturnStatement': 'return self._ExecuteCommand(command, timeout=timeout, recvjson=False, blockwait=blockwait)',
            'x-omitRegularReturnStatement': True,
        }),
        ('GetDetectionHistory', {
            'parameters': [
                {
                    'name': 'timestamp',
                    'paramOrderingIndex': 0,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 1,
                    }
                ])[0],
            ],
            'x-methodStartSetup': 'log.verbose("Getting detection result at %r ...", timestamp)',
            'x-modifiedReturnStatement': 'return self._ExecuteCommand(command, timeout=timeout, recvjson=False)',
            'x-omitRegularReturnStatement': True,
        }),
        ('GetVisionStatistics', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 3,
                    }
                ])[0],
            ],
        }),
        ('Ping', {
            'parameters': [
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                ])[0],
            ],
        }),
        ('SetLogLevel', {
            'parameters': [
                {
                    'name': 'componentLevels',
                    'paramOrderingIndex': 0,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 1,
                    }
                ])[0],
            ],
        }),
        ('Cancel', {
            'parameters': [
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                ])[0],
            ],
            'x-methodStartSetup': "log.info('Canceling command...')",
            'x-modifiedReturnStatement': "response = self._SendConfiguration(command, timeout=timeout)\nlog.info('Command is stopped.')\nreturn response\n",
            'x-omitRegularReturnStatement': True,
        }),
        ('Quit', {
            'parameters': [
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'paramOrderingIndex': 0,
                    }
                ])[0],
            ],
            'x-methodStartSetup': "log.info('Stopping visionserver...')",
            'x-modifiedReturnStatement': "response = self._SendConfiguration(command, timeout=timeout)\nlog.info('Visionserver is stopped.')\nreturn response\n",
            'x-omitRegularReturnStatement': True,
        }),
        ('GetTaskStateService', {
            'parameters': [
                {
                    'name': 'taskId',
                    'paramOrderingIndex': 0,
                },
                {
                    'name': 'cycleIndex',
                    'paramOrderingIndex': 1,
                },
                {
                    'name': 'taskType',
                    'paramOrderingIndex': 2,
                },
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 4.0,
                        'paramOrderingIndex': 3,
                    }
                ])[0],
            ],
            'serversideCommandName': 'GetTaskState',
        }),
        ('GetPublishedStateService', {
            'parameters': [
                MergeDicts([
                    deepcopy(components.Internal_ExecuteCommandParameters['timeout']),
                    {
                        'default': 4.0,
                        'paramOrderingIndex': 0,
                    }
                ])[0],
            ],
            'serversideCommandName': 'GetPublishedState',
        }),
    ]),
}

generatorSettingsDict = {
    'template': template,
    'x-specModifications': x_specModifications,
    'templateArgs': templateArgs
}

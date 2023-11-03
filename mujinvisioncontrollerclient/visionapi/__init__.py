# -*- coding: utf-8 -*-

import mujincommon.i18n
import mujincommon.dictutil

ugettext, ungettext = mujincommon.i18n.GetDomain('binpickingui').GetTranslationFunctions()
_ = ugettext

from collections import OrderedDict
from copy import deepcopy

from mujincommon.dictutil import MergeDicts

from . import components
from mujinvisionmanager.schema import visionTaskParametersSchema

visionControllerClientSpec = {
    'info': {
        'title': 'MujinVisionControllerClient',
        'description': _('The API of the Mujin vision client.'),
        'mujinspecformatversion': '0.0.1'
    },
    'services': {
        'StartObjectDetectionTask': {
            'description': _('Starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the specific taskId to use.'),
                        'type': 'string',
                    }
                },
                deepcopy(components.systemState),
                {
                    'name': 'visionTaskParameters',
                    'description': _('Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.'),
                    'schema': visionTaskParametersSchema.visionTaskObjectDetectionParametersSchema,
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('taskId', {
                        'description': _('The taskId of the created task'),
                        'type': 'string',
                    }),
                ]),
                'type': 'object',
            },
        },
        'StartContainerDetectionTask': {
            'description': _('Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the specific taskId to use.'),
                        'type': 'string',
                    }
                },
                deepcopy(components.systemState),
                {
                    'name': 'visionTaskParameters',
                    'description': _('Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.'),
                    'schema': visionTaskParametersSchema.visionTaskObjectDetectionParametersSchema,
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('taskId', {
                        'description': _('The taskId of the created task'),
                        'type': 'string',
                    }),
                ]),
                'type': 'object',
            },
        },
        'StartVisualizePointCloudTask': {
            'description': _('Start point cloud visualization thread to sync camera info from the Mujin controller and send the raw camera point clouds to Mujin controller'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the specific taskId to use.'),
                        'type': 'string',
                    }
                },
                deepcopy(components.systemState),
                {
                    'name': 'visionTaskParameters',
                    'description': _('Parameters for the object detection task. These take precedence over the base profile selected via the system state, but are overwritten by the overwrite profile.'),
                    'schema': visionTaskParametersSchema.visionTaskObjectDetectionParametersSchema,
                },
            ],
            'returns': {
                'type': 'object',
            },
        },
        'StopTask': {
            'description': _('Stops a set of tasks that meet the filter criteria'),
            'parameters': [
                {
                    'name': 'taskTypes',
                    'schema': {
                        'description': _('If specified, a list of task types to stop.'),
                        'items': deepcopy(components.taskTypeSchema),
                        'type': 'array',
                    }
                },
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the specific taskId to stop'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'taskIds',
                    'schema': {
                        'description': _('If specified, a list of taskIds to stop'),
                        'items': {
                            'type': 'string',
                        },
                        'type': 'array',
                    }
                },
                {
                    'name': 'taskType',
                    'description': _('The task type to stop.'),
                    'schema': deepcopy(components.taskTypeSchema)
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'waitForStop',
                    'schema': {
                        'description': _('If True, then wait for task to stop, otherwise just trigger it to stop, but do not wait'),
                        'type': 'boolean',
                    }
                },
                {
                    'name': 'removeTask',
                    'schema': {
                        'description': _('If True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning.'),
                        'type': 'boolean',
                    }
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('isStopped', {
                        'description': _('true, if the specific taskId or set of tasks with a specific taskType(s) is stopped'),
                        'type': 'boolean',
                    }),
                ]),
                'type': 'object',
            },
        },
        'ResumeTask': {
            'description': _('Resumes a set of tasks that meet the filter criteria'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the specific taskId to resume'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'taskIds',
                    'schema': {
                        'description': _('If specified, a list of taskIds to resume'),
                        'items': {
                            'type': 'string',
                        },
                        'type': 'array',
                    }
                },
                {
                    'name': 'taskType',
                    'description': _('The task type to resume.'),
                    'schema': deepcopy(components.taskTypeSchema),
                },
                {
                    'name': 'taskTypes',
                    'schema': {
                        'description': _('If specified, a list of task types to resume'),
                        'items': {
                            'type': 'string',
                        },
                        'type': 'array',
                    }
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'waitForStop',
                    'schema': {
                        'deprecated': True,
                        'description': _('This is unused.'),
                        'type': 'boolean',
                    }
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('taskIds', {
                        'description': _('List of taskIds that have been resumed'),
                        'items': {
                            'type': 'string',
                        },
                        'type': 'array',
                    }),
                ]),
                'type': 'object',
            },
        },
        'BackupVisionLog': {
            'description': _('Backs up the vision log for a given cycle index and/or sensor timestamps.'),
            'parameters': [
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema),
                    'isRequired': True
                },
                {
                    'name': 'sensorTimestamps',
                    'schema': {
                        'description': _('The sensor timestamps to backup'),
                        'items': {
                            'type': 'number',
                        },
                        'type': 'array',
                    }
                },
            ],
            'returns': {
                'type': 'object',
            },
        },
        'GetLatestDetectedObjects': {
            'description': _('Gets the latest detected objects.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the taskId to retrieve the detected objects from.'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'taskType',
                    'description': _('The task type to retrieve the detected objects from.'),
                    'schema': deepcopy(components.taskTypeSchema),
                }
            ],
            'returns': {
                'properties': OrderedDict([
                    ('detectionResults', {
                        'description': _('A list of the latest detection results.'),
                        'items': {
                            'properties': OrderedDict([
                                ('cycleIndex', deepcopy(visionTaskParametersSchema.cycleIndexSchema)),
                                ('detectedObjects', {
                                    'type': 'array',
                                }),
                                ('detectionResultState', {
                                    'type': 'object',
                                }),
                                ('imageEndTimeStampMS', {
                                    'type': 'integer',
                                }),
                                ('imageStartTimestampMS', {
                                    'type': 'integer',
                                }),
                                ('locationName', {
                                    'type': 'string',
                                }),
                                ('pointCloudId', {
                                    'type': 'string',
                                }),
                                ('resultTimestampMS', {
                                    'type': 'integer',
                                }),
                                ('sensorSelectionInfos', {
                                    'items': {
                                        'type': 'object',
                                    },
                                    'type': 'array',
                                }),
                                ('statsUID', {
                                    'type': 'string',
                                }),
                                ('targetUpdateName', {
                                    'type': 'string',
                                }),
                                ('taskId', {
                                    'type': 'string',
                                }),
                            ]),
                            'type': 'object',
                        },
                        'type': 'array',
                    }),
                ]),
                'type': 'object',
            },
        },
        'GetLatestDetectionResultImages': {
            'description': _('Gets the latest detected result images.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('If specified, the taskId to retrieve the detected objects from.'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'taskType',
                    'description': _('If specified, the task type to retrieve the detected objects from.'),
                    'schema': deepcopy(components.taskTypeSchema),
                },
                {
                    'name': 'newerThanResultTimestampMS',
                    'schema': {
                        'description': _('If specified, starttimestamp of the image must be newer than this value in milliseconds.'),
                        'type': 'integer',
                    }
                },
                {
                    'name': 'sensorSelectionInfo',
                    'schema': {
                        'description': _('Sensor selection infos (see schema).'),
                        'type': 'object',
                    }
                },
                {
                    'name': 'metadataOnly',
                    'schema': {
                        'type': 'boolean',
                    }
                },
                {
                    'name': 'imageTypes',
                    'schema': {
                        'description': _('Mujin image types'),
                        'type': 'array',
                    }
                },
                {
                    'name': 'limit',
                    'schema': {
                        'type': 'integer',
                    }
                },
                {
                    'name': 'blockwait',
                    'schema': {
                        'description': _('If true, waits for the next image to be available. If false, returns immediately.'),
                        'type': 'boolean',
                    }
                },
            ],
            'returns': {
                'description': _('Raw image data'),
                'type': 'string',
            },
        },
        'GetDetectionHistory': {
            'description': _('Gets detection result with given timestamp (sensor time)'),
            'parameters': [
                {
                    'name': 'timestamp',
                    'schema': {
                        'description': _('Unix timestamp in milliseconds of the sensor capture time ("targetsensortimestamp" from detected objects).'),
                        'isRequired': True,
                        'type': 'integer',
                    }
                },
            ],
            'returns': {
                'description': _('Binary blob of detection data'),
                'type': 'string',
            },
        },
        'GetVisionStatistics': {
            'description': _('Gets the latest vision stats.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('The taskId to retrieve the detected objects from. If not specified, retrieves all currently active vision tasks'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'taskType',
                    'description': _('If specified, the task type to retrieve the detected objects from.'),
                    'schema': deepcopy(components.taskTypeSchema),
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('visionStatistics', {
                        'description': _('A list of all currently active vision task statistics.'),
                        'items': {
                            'properties': OrderedDict([
                                ('cycleIndex', deepcopy(visionTaskParametersSchema.cycleIndexSchema)),
                                ('taskId', {
                                    'description': _('The taskId.'),
                                    'type': 'string',
                                }),
                                ('taskType', deepcopy(components.taskTypeSchema)),
                                ('taskStartTimeMS', {
                                    'type': 'integer',
                                }),
                                ('totalDetectionTimeMS', {
                                    'type': 'integer',
                                }),
                                ('totalDetectionCount', {
                                    'type': 'integer',
                                }),
                                ('totalGetImagesCount', {
                                    'type': 'integer',
                                }),
                                ('targetURIs', {
                                    'type': 'string',
                                }),
                                ('detectionHistory', {
                                    'type': 'array',
                                }),
                            ]),
                            'type': 'object',
                        },
                        'type': 'array',
                    }),
                ]),
                'type': 'object',
            },
        },
        'Ping': {
            'description': _('Sends a ping to the visionmanager.'),
            'parameters': [],
            'returns': {
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
        'SetLogLevel': {
            'description': _('Sets the log level for the visionmanager.'),
            'parameters': [
                {
                    'name': 'componentLevels',
                    'schema': {
                        'description': _('A dictionary of component names and their respective log levels.'),
                        'isRequired': True,
                        'type': 'object',
                    }
                },
            ],
            'returns': {
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
        'Cancel': {
            'description': _('Cancels the current command.'),
            'parameters': [],
            'returns': {
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
        'Quit': {
            'description': _('Quits the visionmanager.'),
            'parameters': [],
            'returns': {
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
        'GetTaskStateService': {
            'description': _('Gets the task state from visionmanager.'),
            'parameters': [
                {
                    'name': 'taskId',
                    'schema': {
                        'description': _('The taskId to retrieve the detected objects from. If not specified, defaults to current slaverequest id.'),
                        'type': 'string',
                    }
                },
                {
                    'name': 'cycleIndex',
                    'schema': deepcopy(visionTaskParametersSchema.cycleIndexSchema)
                },
                {
                    'name': 'taskType',
                    'description': _('The taskType for which the status was requested. If not specified, defaults to the controller monitor task.'),
                    'schema': deepcopy(components.taskTypeSchema)
                },
            ],
            'returns': {
                'properties': OrderedDict([
                    ('taskParameters', {
                        'description': _('describes the task specific parameters if present, eg. detection params, execution verification params.'),
                        'type': 'object',
                    }),
                    ('initializeTaskMS', {
                        'description': _('timestamp at which the task was received and initialized , in ms (linux epoch)'),
                        'type': 'integer',
                    }),
                    ('isStopTask', {
                        'description': _('True if task is currently running'),
                        'type': 'boolean',
                    }),
                    ('scenepk', {
                        'description': _('scene file name'),
                        'type': 'string',
                    }),
                    ('taskId', {
                        'description': _('The taskId for which the status was requested'),
                        'type': 'string',
                    }),
                    ('taskStatus', {
                        'description': _('status of the task'),
                        'type': 'string',
                    }),
                    ('taskStatusMessage', {
                        'description': _('describes the task status'),
                        'type': 'string',
                    }),
                    ('taskType', MergeDicts([
                        deepcopy(components.taskTypeSchema),
                        {
                            'description': _('The task type for which the status was requested'),
                        }
                    ])[0]),
                ]),
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
        'GetPublishedStateService': {
            'description': _('Gets the published state of the visionmanager.'),
            'parameters': [],
            'returns': {
                'properties': OrderedDict([
                    ('statusMessage', {
                        'type': 'string',
                    }),
                    ('tasks', {
                        'type': 'array',
                    }),
                    ('timestamp', {
                        'type': 'integer',
                    }),
                    ('version', {
                        'type': 'string',
                    }),
                ]),
                'type': 'object',
            },
            'usesConfigSocket': True,
        },
    }
}


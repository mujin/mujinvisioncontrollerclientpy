# -*- coding: utf-8 -*-
# Copyright (C) 2023 Mujin, Inc.

from collections import OrderedDict

from . import _

systemState = {
    'name': 'systemState',
    'schema': {
        'description': _('The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.'),
        'type': 'object',
        'properties': {
            "sensorType": {"type": "string"},
            "sensorName": {"type": "string"},
            "sensorLinkName": {"type": "string"},
            "visionTaskType": {"type": "string"},
            "locationName": {"type": "string"},
            "partType": {"type": "string"},
            "graspSetName": {"type": "string"},
            "objectType": {"type": "string"},
            "objectMaterialType": {"type": "string"},
            "scenarioId": {"type": "string"},
            "applicationType": {"type": "string"},
            "detectionTriggerType": {"type": "string"},
            "detectionState": {"type": "string"},
            "sensorUsageType": {"type": "string"},
            "orchestratorUsageType": {"type": "string"}
        }
    }
}

taskTypeSchema = {
    'description': _('The task type.'),
    'type': 'string',
}

Internal_ExecuteCommandParameters = {
    'fireandforget': {
        'default': False,
        'description': _('If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.'),
        'type': 'boolean',
        'x-doNotAddToPayload': True,
    },
    'respawnopts': {
        'description': _('Settings to determine the respawning behavior of planning slaves. Restarts/respawns a planning slave if conditions are met.'),
        'properties': OrderedDict([
            ('allowrespawn', {
                'default': True,
                'description': _('Allow the planning slave to respawn.'),
                'type': 'boolean',
            }),
            ('forcerespawn', {
                'default': False,
                'description': _('Force the planning slave to respawn.'),
                'type': 'boolean',
            }),
            ('respawnMemoryThreshold', {
                'default': '2*1024*1024*1024',
                'description': _('The amount of memory that the planning slave may occupy before it is respawned.'),
                'type': 'float',
            }),
        ]),
        'isRequired': False,
        'type': 'object',
    },
    'timeout': {
        'default': 2.0,
        'description': _('Time in seconds after which the command is assumed to have failed.'),
        'type': 'number',
        'x-doNotAddToPayload': True,
    },
}

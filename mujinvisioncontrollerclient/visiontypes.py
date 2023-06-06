from . import _

import typing

# The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
SystemState = typing.TypedDict("SystemState", {
        "sensorType": str,
        "sensorName": str,
        "sensorLinkName": str,
        "visionTaskType": str,
        "locationName": str,
        "partType": str,
        "graspSetName": str,
        "objectType": str,
        "objectMaterialType": str,
        "scenarioId": str,
        "applicationType": str,
        "detectionTriggerType": str,
        "detectionState": str,
        "sensorUsageType": str,
    },
    total=False,
)

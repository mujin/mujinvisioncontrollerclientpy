
# This file contains the types used in the client
from typing import TypedDict, Union, Any, Optional, Literal
from typing_extensions import Required

TerminateSlavesReturnsOutput = TypedDict('TerminateSlavesReturnsOutput', {
    'result': Literal['succeeded'],
    'numTerminated': int,
}, total=False)

TerminateSlavesReturns = TypedDict('TerminateSlavesReturns', {
    'output': TerminateSlavesReturnsOutput,
}, total=False)

StartObjectDetectionTaskParametersSystemState = TypedDict('StartObjectDetectionTaskParametersSystemState', {
    'locationName': str,
    'sensorName': str,
    'scenarioId': str,
    'objectMaterialType': str,
    'detectionState': str,
    'partType': str,
    'sensorType': str,
    'sensorUsageType': str,
    'applicationType': str,
    'graspSetName': str,
    'sensorLinkName': str,
    'orchestratorUsageType': str,
    'visionTaskType': str,
    'detectionTriggerType': str,
    'objectType': str,
}, total=False)

StartObjectDetectionTaskParametersVisionTaskParametersPlanningClientInfo = TypedDict('StartObjectDetectionTaskParametersVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'heartbeatTimeout': float,
    'httpPort': int,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

RobotBridgeConnectionInfoParameters = TypedDict('RobotBridgeConnectionInfoParameters', {
    'queueid': str,
    'host': str,
    'basePort': int,
    'use': bool,
}, total=False)

SensorLinkName = str

SensorName = str

SensorSelectionInfo = TypedDict('SensorSelectionInfo', {
    'sensorLinkName': SensorLinkName,
    'sensorName': SensorName,
}, total=False)

SensorSelectionInfos = list[dict[str, str]]

StartObjectDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('StartObjectDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

StartObjectDetectionTaskParametersVisionTaskParametersRegionParametersMetaData = dict[str, Any]

StartObjectDetectionTaskParametersVisionTaskParametersRegionParameters = TypedDict('StartObjectDetectionTaskParametersVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': StartObjectDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': StartObjectDetectionTaskParametersVisionTaskParametersRegionParametersMetaData,
}, total=False)

StartObjectDetectionTaskParametersVisionTaskParametersRegisClientInfo = TypedDict('StartObjectDetectionTaskParametersVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

OcclusionCheckInfo = TypedDict('OcclusionCheckInfo', {
    'useLinkVisibility': bool,
    'robotname': str,
    'robotnames': list[str],
    'paddingTime': float,
    'paddingTimeStart': float,
    'maxSnappingTimeDuration': float,
    'paddingTimeEnd': float,
    'gridcolumns': int,
    'cameraMoveThreshold': float,
    'partialocclusionthreshold': float,
    'useLocationState': bool,
    'gridrows': int,
    'applyGrabbedState': bool,
    'occlusionCheckMode': Literal['All', 'Disabled', 'GetSensorInWorldPoseOnly', ''],
    'checkPartialOcclusion': bool,
}, total=False)

SensorBridgeConnectionInfo = TypedDict('SensorBridgeConnectionInfo', {
    'host': str,
    'use': bool,
    'basePort': int,
}, total=False)

UnitInfo = TypedDict('UnitInfo', {
    'timeDurationUnit': Literal['s', 'ms', 'us', 'ns', 'ps'],
    'massUnit': Literal['g', 'mg', 'kg', 'lb'],
    'lengthUnit': Literal['m', 'dm', 'cm', 'mm', 'um', 'nm', 'in', 'ft'],
    'angleUnit': Literal['rad', 'deg'],
    'timeStampUnit': Literal['s', 'ms', 'us', 'iso8601'],
}, total=False)

StartObjectDetectionTaskParametersVisionTaskParametersDefaultTaskParameters = TypedDict('StartObjectDetectionTaskParametersVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

StartObjectDetectionTaskParametersVisionTaskParameters = TypedDict('StartObjectDetectionTaskParametersVisionTaskParameters', {
    'targetUpdateNamePrefix': str,
    'planningClientInfo': StartObjectDetectionTaskParametersVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'targeturi': Optional[str],
    'useLocationState': bool,
    'ignoreInvalidDetectionFiles': bool,
    'regionParameters': StartObjectDetectionTaskParametersVisionTaskParametersRegionParameters,
    'detectionStartTimeStampMS': int,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'isPickExecution': Literal[-1, 0, 1],
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'runtimeDetectorParametersJSON': str,
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'regisClientInfo': StartObjectDetectionTaskParametersVisionTaskParametersRegisClientInfo,
    'maxNumDetection': int,
    'ignoreDetectionFileUpdateChange': bool,
    'syncRobotBridgeTimeStampUS': int,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'unitInfo': UnitInfo,
    'numthreads': int,
    'runtimeContainerDetectorParametersJSON': str,
    'maxNumFastDetection': int,
    'targetTemplateSceneDataJSON': str,
    'cycleIndex': str,
    'defaultTaskParameters': StartObjectDetectionTaskParametersVisionTaskParametersDefaultTaskParameters,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParametersPlanningClientInfo = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'heartbeatTimeout': float,
    'httpPort': int,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParametersRegionParametersMetaData = dict[str, Any]

StartObjectDetectionTaskReturnsVisionTaskParametersRegionParameters = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': StartObjectDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': StartObjectDetectionTaskReturnsVisionTaskParametersRegionParametersMetaData,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParametersRegisClientInfo = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

StartObjectDetectionTaskReturnsVisionTaskParameters = TypedDict('StartObjectDetectionTaskReturnsVisionTaskParameters', {
    'targetUpdateNamePrefix': str,
    'planningClientInfo': StartObjectDetectionTaskReturnsVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'targeturi': Optional[str],
    'useLocationState': bool,
    'ignoreInvalidDetectionFiles': bool,
    'regionParameters': StartObjectDetectionTaskReturnsVisionTaskParametersRegionParameters,
    'detectionStartTimeStampMS': int,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'isPickExecution': Literal[-1, 0, 1],
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'runtimeDetectorParametersJSON': str,
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'regisClientInfo': StartObjectDetectionTaskReturnsVisionTaskParametersRegisClientInfo,
    'maxNumDetection': int,
    'ignoreDetectionFileUpdateChange': bool,
    'syncRobotBridgeTimeStampUS': int,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'unitInfo': UnitInfo,
    'numthreads': int,
    'runtimeContainerDetectorParametersJSON': str,
    'maxNumFastDetection': int,
    'targetTemplateSceneDataJSON': str,
    'cycleIndex': str,
    'defaultTaskParameters': StartObjectDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters,
}, total=False)

StartObjectDetectionTaskReturns = TypedDict('StartObjectDetectionTaskReturns', {
    'slaverequestid': str,
    'taskId': str,
    'visionTaskParameters': StartObjectDetectionTaskReturnsVisionTaskParameters,
}, total=False)

StartContainerDetectionTaskParametersSystemState = TypedDict('StartContainerDetectionTaskParametersSystemState', {
    'locationName': str,
    'sensorName': str,
    'scenarioId': str,
    'objectMaterialType': str,
    'detectionState': str,
    'partType': str,
    'sensorType': str,
    'sensorUsageType': str,
    'applicationType': str,
    'graspSetName': str,
    'sensorLinkName': str,
    'orchestratorUsageType': str,
    'visionTaskType': str,
    'detectionTriggerType': str,
    'objectType': str,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParametersRegisClientInfo = TypedDict('StartContainerDetectionTaskParametersVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParametersPlanningClientInfo = TypedDict('StartContainerDetectionTaskParametersVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'httpPort': int,
    'heartbeatTimeout': float,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('StartContainerDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParametersRegionParametersMetaData = dict[str, Any]

StartContainerDetectionTaskParametersVisionTaskParametersRegionParameters = TypedDict('StartContainerDetectionTaskParametersVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': StartContainerDetectionTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': StartContainerDetectionTaskParametersVisionTaskParametersRegionParametersMetaData,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParametersDefaultTaskParameters = TypedDict('StartContainerDetectionTaskParametersVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

StartContainerDetectionTaskParametersVisionTaskParameters = TypedDict('StartContainerDetectionTaskParametersVisionTaskParameters', {
    'regisClientInfo': StartContainerDetectionTaskParametersVisionTaskParametersRegisClientInfo,
    'targetUpdateNamePrefix': str,
    'planningClientInfo': StartContainerDetectionTaskParametersVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'syncRobotBridgeTimeStampUS': int,
    'maxNumContainerDetection': int,
    'maxContainerNotFound': int,
    'targeturi': Optional[str],
    'useLocationState': bool,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'regionParameters': StartContainerDetectionTaskParametersVisionTaskParametersRegionParameters,
    'detectionStartTimeStampMS': int,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'unitInfo': UnitInfo,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'numthreads': int,
    'isPickExecution': Literal[-1, 0, 1],
    'ignoreInvalidDetectionFiles': bool,
    'runtimeDetectorParametersJSON': str,
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'cycleIndex': str,
    'defaultTaskParameters': StartContainerDetectionTaskParametersVisionTaskParametersDefaultTaskParameters,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParametersRegisClientInfo = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParametersPlanningClientInfo = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'httpPort': int,
    'heartbeatTimeout': float,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParametersRegionParametersMetaData = dict[str, Any]

StartContainerDetectionTaskReturnsVisionTaskParametersRegionParameters = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': StartContainerDetectionTaskReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': StartContainerDetectionTaskReturnsVisionTaskParametersRegionParametersMetaData,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

StartContainerDetectionTaskReturnsVisionTaskParameters = TypedDict('StartContainerDetectionTaskReturnsVisionTaskParameters', {
    'regisClientInfo': StartContainerDetectionTaskReturnsVisionTaskParametersRegisClientInfo,
    'targetUpdateNamePrefix': str,
    'planningClientInfo': StartContainerDetectionTaskReturnsVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'syncRobotBridgeTimeStampUS': int,
    'maxNumContainerDetection': int,
    'maxContainerNotFound': int,
    'targeturi': Optional[str],
    'useLocationState': bool,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'regionParameters': StartContainerDetectionTaskReturnsVisionTaskParametersRegionParameters,
    'detectionStartTimeStampMS': int,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'unitInfo': UnitInfo,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'numthreads': int,
    'isPickExecution': Literal[-1, 0, 1],
    'ignoreInvalidDetectionFiles': bool,
    'runtimeDetectorParametersJSON': str,
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'cycleIndex': str,
    'defaultTaskParameters': StartContainerDetectionTaskReturnsVisionTaskParametersDefaultTaskParameters,
}, total=False)

StartContainerDetectionTaskReturns = TypedDict('StartContainerDetectionTaskReturns', {
    'taskId': str,
    'visionTaskParameters': StartContainerDetectionTaskReturnsVisionTaskParameters,
}, total=False)

StartVisualizePointCloudTaskParametersSystemState = TypedDict('StartVisualizePointCloudTaskParametersSystemState', {
    'locationName': str,
    'sensorName': str,
    'scenarioId': str,
    'objectMaterialType': str,
    'detectionState': str,
    'partType': str,
    'sensorType': str,
    'sensorUsageType': str,
    'applicationType': str,
    'graspSetName': str,
    'sensorLinkName': str,
    'orchestratorUsageType': str,
    'visionTaskType': str,
    'detectionTriggerType': str,
    'objectType': str,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParametersPlanningClientInfo = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'heartbeatTimeout': float,
    'httpPort': int,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParametersMetaData = dict[str, Any]

StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParameters = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParametersMetaData,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParametersRegisClientInfo = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParametersDefaultTaskParameters = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

StartVisualizePointCloudTaskParametersVisionTaskParameters = TypedDict('StartVisualizePointCloudTaskParametersVisionTaskParameters', {
    'targetUpdateNamePrefix': str,
    'planningClientInfo': StartVisualizePointCloudTaskParametersVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'targeturi': Optional[str],
    'useLocationState': bool,
    'ignoreInvalidDetectionFiles': bool,
    'regionParameters': StartVisualizePointCloudTaskParametersVisionTaskParametersRegionParameters,
    'detectionStartTimeStampMS': int,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'isPickExecution': Literal[-1, 0, 1],
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'runtimeDetectorParametersJSON': str,
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'regisClientInfo': StartVisualizePointCloudTaskParametersVisionTaskParametersRegisClientInfo,
    'maxNumDetection': int,
    'ignoreDetectionFileUpdateChange': bool,
    'syncRobotBridgeTimeStampUS': int,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'unitInfo': UnitInfo,
    'numthreads': int,
    'runtimeContainerDetectorParametersJSON': str,
    'maxNumFastDetection': int,
    'targetTemplateSceneDataJSON': str,
    'cycleIndex': str,
    'defaultTaskParameters': StartVisualizePointCloudTaskParametersVisionTaskParametersDefaultTaskParameters,
}, total=False)

StartVisualizePointCloudTaskReturns = dict[str, Any]

StopTaskReturns = TypedDict('StopTaskReturns', {
    'isStopped': bool,
    'slaverequestid': str,
}, total=False)

ResumeTaskReturns = TypedDict('ResumeTaskReturns', {
    'resumedVisionTaskIds': list[str],
    'slaverequestid': str,
}, total=False)

BackupDetectionLogsReturns = dict[str, Any]

KinBodyFiles = dict[str, Any]

GrabbedInfoGrabbedUserData = dict[str, Any]

GrabbedInfo = TypedDict('GrabbedInfo', {
    'ignoreRobotLinkNames': list[str],
    'robotLinkName': str,
    'id': str,
    'grabbedName': str,
    'transform': tuple[float, float, float, float, float, float, float],
    'grabbedUserData': GrabbedInfoGrabbedUserData,
}, total=False)

LinkInfoFloatParametersArrayElement = TypedDict('LinkInfoFloatParametersArrayElement', {
    'values': list[float],
    'id': str,
}, total=False)

LinkInfoIntParametersArrayElement = TypedDict('LinkInfoIntParametersArrayElement', {
    'values': list[int],
    'id': str,
}, total=False)

LinkInfoStringParametersArrayElement = TypedDict('LinkInfoStringParametersArrayElement', {
    'values': list[str],
    'id': str,
}, total=False)

ReadableInterfaces = dict[str, Any]

Geometry = TypedDict('Geometry', {
    'outerExtents': list[float],
    'name': str,
    'diffuseColor': list[float],
    'positiveCropContainerEmptyMargins': list[float],
    'transform': tuple[float, float, float, float, float, float, float],
    'halfExtents': list[float],
    'negativeCropContainerEmptyMargins': list[float],
    'transparency': float,
    'negativeCropContainerMargins': list[float],
    'innerExtents': list[float],
    'type': Literal['mesh', 'box', 'container', 'cage', 'sphere', 'cylinder', 'axial', 'trimesh', 'calibrationboard', 'conicalfrustum', ''],
    'id': str,
    'positiveCropContainerMargins': list[float],
}, total=False)

LinkInfo = TypedDict('LinkInfo', {
    'isStatic': bool,
    'forcedAdjacentLinks': list[str],
    'name': str,
    'isSelfCollisionIgnored': bool,
    'isEnabled': bool,
    'transform': tuple[float, float, float, float, float, float, float],
    'inertiaMoments': tuple[float, float, float],
    'floatParameters': list[LinkInfoFloatParametersArrayElement],
    'mass': float,
    'massTransform': tuple[float, float, float, float, float, float, float],
    'intParameters': list[LinkInfoIntParametersArrayElement],
    'stringParameters': list[LinkInfoStringParametersArrayElement],
    'id': str,
    'readableInterfaces': ReadableInterfaces,
    'geometries': list[Geometry],
}, total=False)

KinBodyDofValuesArrayElement = TypedDict('KinBodyDofValuesArrayElement', {
    'jointName': str,
    'jointAxis': float,
    'value': float,
}, total=False)

JointInfoJointControlInfoExternalDevice = TypedDict('JointInfoJointControlInfoExternalDevice', {
    'externalDeviceType': str,
}, total=False)

JointInfoElectricMotorActuator = TypedDict('JointInfoElectricMotorActuator', {
    'noLoadSpeed': float,
    'modelType': str,
    'terminalResistance': float,
    'maxSpeedTorquePoints': list[tuple[float, float]],
    'coloumbFriction': float,
    'nominalTorque': float,
    'nominalSpeedTorquePoints': list[tuple[float, float]],
    'startingCurrent': float,
    'maxSpeed': float,
    'speedConstant': float,
    'gearRatio': float,
    'viscousFriction': float,
    'assignedPowerRating': float,
    'nominalVoltage': float,
    'rotorInertia': float,
    'stallTorque': float,
    'maxInstantaneousTorque': float,
    'torqueConstant': float,
}, total=False)

JointInfoJointControlInfoIO = TypedDict('JointInfoJointControlInfoIO', {
    'upperLimitSensorIsOn': list[list[int]],
    'deviceType': str,
    'upperLimitIONames': list[list[str]],
    'lowerLimitIONames': list[list[str]],
    'lowerLimitSensorIsOn': list[list[int]],
    'moveIONames': list[list[str]],
}, total=False)

JointInfoFloatParametersArrayElement = TypedDict('JointInfoFloatParametersArrayElement', {
    'values': list[float],
    'id': str,
}, total=False)

JointInfoMimicsArrayElement = TypedDict('JointInfoMimicsArrayElement', {
    'equations': tuple[str, str, str],
}, total=False)

JointInfoIntParametersArrayElement = TypedDict('JointInfoIntParametersArrayElement', {
    'values': list[int],
    'id': str,
}, total=False)

JointInfoJointControlInfoRobotController = TypedDict('JointInfoJointControlInfoRobotController', {
    'robotControllerAxisOffset': list[float],
    'robotControllerAxisIndex': list[int],
    'robotControllerAxisManufacturerCode': list[str],
    'robotControllerAxisProductCode': list[str],
    'robotControllerAxisMult': list[float],
    'controllerType': str,
}, total=False)

JointInfoStringParametersArrayElement = TypedDict('JointInfoStringParametersArrayElement', {
    'values': list[str],
    'id': str,
}, total=False)

JointInfo = TypedDict('JointInfo', {
    'hardMaxAccel': list[float],
    'childLinkName': str,
    'jointControlInfoExternalDevice': JointInfoJointControlInfoExternalDevice,
    'maxJerk': list[float],
    'electricMotorActuator': JointInfoElectricMotorActuator,
    'hardMaxJerk': list[float],
    'jointControlInfoIO': JointInfoJointControlInfoIO,
    'hardMaxVel': list[float],
    'resolutions': list[float],
    'id': str,
    'axes': list[tuple[float, float, float]],
    'maxAccel': list[float],
    'controlMode': Literal['None', 'RobotController', 'IO', 'ExternalDevice'],
    'floatParameters': list[JointInfoFloatParametersArrayElement],
    'type': Literal['revolute', 'prismatic', 'rr', 'rp', 'pr', 'pp', 'universal', 'hinge2', 'spherical', 'trajectory'],
    'parentLinkName': str,
    'maxInertia': list[float],
    'anchors': list[float],
    'lowerLimit': list[float],
    'offsets': list[float],
    'mimics': list[JointInfoMimicsArrayElement],
    'currentValues': list[float],
    'isCircular': list[int],
    'intParameters': list[JointInfoIntParametersArrayElement],
    'maxVel': list[float],
    'isActive': bool,
    'maxTorque': list[float],
    'name': str,
    'jointControlInfoRobotController': JointInfoJointControlInfoRobotController,
    'stringParameters': list[JointInfoStringParametersArrayElement],
    'weights': list[float],
    'readableInterfaces': ReadableInterfaces,
    'upperLimit': list[float],
}, total=False)

KinBody = TypedDict('KinBody', {
    'files': KinBodyFiles,
    'grabbed': list[GrabbedInfo],
    'name': str,
    'links': list[LinkInfo],
    'isRobot': bool,
    'dofValues': list[KinBodyDofValuesArrayElement],
    'joints': list[JointInfo],
    'referenceUri': str,
    'transform': tuple[float, float, float, float, float, float, float],
    '__isPartial__': bool,
    'interfaceType': str,
    'referenceUriHint': str,
    'id': str,
    'readableInterfaces': ReadableInterfaces,
}, total=False)

TargetTemplateSceneData = TypedDict('TargetTemplateSceneData', {
    'unitInfo': UnitInfo,
    'bodies': list[KinBody],
}, total=False)

RobotConfigurationState = TypedDict('RobotConfigurationState', {
    'connectedBodyActiveStates': list[Any],
    'robotName': str,
    'jointValues': list[float],
}, total=False)

CameraDynamicState = TypedDict('CameraDynamicState', {
    'sensorInWorldPose': list[list[float]],
    'sensorName': str,
    'sensorLinkName': str,
    'firstRobotConfigurationState': RobotConfigurationState,
    'lastRobotConfigurationState': RobotConfigurationState,
    'imagetype': str,
}, total=False)

DetectionResultMessage = dict[str, str]

DetectionResultStateDetectedObjectsArrayElement = TypedDict('DetectionResultStateDetectedObjectsArrayElement', {
    'name': str,
    'flip': list[Any],
    'flipScores': list[float],
    'localpose': list[Any],
}, total=False)

ContainerInspection = TypedDict('ContainerInspection', {
    'isOk': bool,
    'topLayerArea': float,
    'topLayerPercentageRequired': float,
    'topLayerPercentage': float,
}, total=False)

TopLayerVerificationResult = TypedDict('TopLayerVerificationResult', {
    'numValidSlots': int,
    'isOk': bool,
    'numSlots': int,
    'isOK': bool,
    'isTopLayerValid': bool,
}, total=False)

AABB = TypedDict('AABB', {
    'extents': tuple[float, float, float],
    'pos': tuple[float, float, float],
}, total=False)

DetectionResultState = TypedDict('DetectionResultState', {
    'containerTransform': list[list[float]],
    'detectionStartTimeStampMS': int,
    'cameraDynamicStates': list[CameraDynamicState],
    'detectEndTimeStampUS': int,
    'endcapturetime': int,
    'detectStartTimeStampUS': int,
    'isContainerDamaged': float,
    'numDetectedParts': float,
    'detectionResultMessage': DetectionResultMessage,
    'isContainerPresent': float,
    'detectedObjects': list[DetectionResultStateDetectedObjectsArrayElement],
    'isContainerEmpty': Literal[1, 0, -1, True, False],
    'containerInspection': ContainerInspection,
    'isBinDetectionOn': bool,
    'startcapturetime': int,
    'topLayerVerificationResult': TopLayerVerificationResult,
    'maxCandidateSize': list[Any],
    'contentsAABBInContainer': AABB,
    'minCandidateSize': list[Any],
    'resultInWorldFrame': bool,
}, total=False)

DetectionConfidence = TypedDict('DetectionConfidence', {
    'global_confidence': float,
}, total=False)

DetectedObjectCloudObstacleInfoVariantItemPrefix0ObjectsArrayElement = TypedDict('DetectedObjectCloudObstacleInfoVariantItemPrefix0ObjectsArrayElement', {
    'type': str,
    'pose': list[Any],
    'extents': list[float],
}, total=False)

DetectedObjectCloudObstacleInfoVariantItemPrefix0 = TypedDict('DetectedObjectCloudObstacleInfoVariantItemPrefix0', {
    'flapExtents': list[float],
    'extents': list[float],
    'uri': str,
    'pos': list[float],
    'geometryInfos': list[Geometry],
    'objects': list[DetectedObjectCloudObstacleInfoVariantItemPrefix0ObjectsArrayElement],
    'type': str,
    'flapPose': list[Any],
}, total=False)

MinViableRegion = TypedDict('MinViableRegion', {
    'cornerMask': int,
    'size2D': list[Any],
    'enableCheckTextureless': bool,
    'maxPossibleSize': list[float],
}, total=False)

DetectedObjectExtraInfoUncertaintyInfoArrayElement = TypedDict('DetectedObjectExtraInfoUncertaintyInfoArrayElement', {
    'pose': list[Any],
    'object_uri': str,
    'templID': str,
}, total=False)

ContainerDynamicPropertyMetaData = TypedDict('ContainerDynamicPropertyMetaData', {
    'numInContainer': float,
    'numPensPerStack': list[list[float]],
}, total=False)

ContainerDynamicProperty = TypedDict('ContainerDynamicProperty', {
    'isContainerPresent': int,
    'sensorTimeStampMS': int,
    'isContainerEmpty': Literal[1, 0, -1, True, False],
    'containerId': str,
    'containerType': str,
    'containerUsage': str,
    'metaData': ContainerDynamicPropertyMetaData,
}, total=False)

DetectedObjectExtraInfo = TypedDict('DetectedObjectExtraInfo', {
    'minViableRegion': MinViableRegion,
    'faceTransformZ': float,
    'detectionMethod': str,
    'detectedFaces': list[str],
    'uncertaintyInfo': list[DetectedObjectExtraInfoUncertaintyInfoArrayElement],
    'object_uri': str,
    'boxFullSize': list[float],
    'maxCornerIndex': int,
    'geometryInfos': list[Geometry],
    'containerDynamicProperties': ContainerDynamicProperty,
    'planeStd': float,
    'kinBodyName': str,
}, total=False)

DetectedObject = TypedDict('DetectedObject', {
    'isPickable': bool,
    'confidence': DetectionConfidence,
    'sensorTimeStampMS': float,
    'cloudObstacleInfo': Optional[DetectedObjectCloudObstacleInfoVariantItemPrefix0],
    'detectedBodyData': KinBody,
    'extra': DetectedObjectExtraInfo,
}, total=False)

ObjectDetectionTaskResultDefaultTaskParameters = TypedDict('ObjectDetectionTaskResultDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'randomBoxOrigin': list[float],
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'populateFnName': str,
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

ObjectDetectionTaskResult = TypedDict('ObjectDetectionTaskResult', {
    'targetUpdateNamePrefix': str,
    'pointSize': float,
    'imageEndTimeStampMS': int,
    'pointCloudId': str,
    'finishMessage': str,
    'targetTemplateSceneData': TargetTemplateSceneData,
    'detectionResultState': DetectionResultState,
    'statsUID': str,
    'imageStartTimeStampMS': int,
    'sensorSelectionInfos': SensorSelectionInfos,
    'taskId': str,
    'unitInfo': UnitInfo,
    'finishCode': str,
    'dynamicPointCloudNameBase': str,
    'containerName': str,
    'locationContainerType': str,
    'resultTimestampUS': int,
    'locationContainerId': str,
    'locationContainerUsage': str,
    'isPickExecution': Literal[-1, 0, 1],
    'detectedObjects': list[DetectedObject],
    'cycleIndex': str,
    'locationName': str,
    'isExecutionVerification': bool,
    'defaultTaskParameters': ObjectDetectionTaskResultDefaultTaskParameters,
}, total=False)

GetLatestDetectedObjectsReturns = TypedDict('GetLatestDetectedObjectsReturns', {
    'detectionResults': list[ObjectDetectionTaskResult],
}, total=False)

GetLatestDetectionResultImagesParametersSensorSelectionInfo = dict[str, Any]

ImageType = Literal['Unknown', 'Color', 'Depth', 'IR', 'DepthXYZ', 'DepthNormal', 'Disparity', 'DetectionResult', 'ColorRaw', 'IRRaw', 'Normals', 'IR_2', 'IRRaw_2']

PingReturns = dict[str, Any]

SetLogLevelParametersComponentLevels = dict[str, Any]

SetLogLevelReturns = dict[str, Any]

QuitReturns = dict[str, Any]

GetTaskStateReturnsTaskParameters = dict[str, Any]

GetTaskStateReturnsDetectionParamsRegisClientInfo = TypedDict('GetTaskStateReturnsDetectionParamsRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

GetTaskStateReturnsDetectionParamsPlanningClientInfo = TypedDict('GetTaskStateReturnsDetectionParamsPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'httpPort': int,
    'heartbeatTimeout': float,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

GetTaskStateReturnsDetectionParamsRegionParametersAddPointOffsetInfo = TypedDict('GetTaskStateReturnsDetectionParamsRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

GetTaskStateReturnsDetectionParamsRegionParametersMetaData = dict[str, Any]

GetTaskStateReturnsDetectionParamsRegionParameters = TypedDict('GetTaskStateReturnsDetectionParamsRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': GetTaskStateReturnsDetectionParamsRegionParametersAddPointOffsetInfo,
    'metaData': GetTaskStateReturnsDetectionParamsRegionParametersMetaData,
}, total=False)

GetTaskStateReturnsDetectionParamsDefaultTaskParameters = TypedDict('GetTaskStateReturnsDetectionParamsDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'populateFnName': str,
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'randomBoxOrigin': list[float],
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

GetTaskStateReturnsDetectionParams = TypedDict('GetTaskStateReturnsDetectionParams', {
    'regisClientInfo': GetTaskStateReturnsDetectionParamsRegisClientInfo,
    'targetUpdateNamePrefix': str,
    'planningClientInfo': GetTaskStateReturnsDetectionParamsPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'syncRobotBridgeTimeStampUS': int,
    'maxNumContainerDetection': int,
    'maxContainerNotFound': int,
    'targeturi': Optional[str],
    'useLocationState': bool,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'regionParameters': GetTaskStateReturnsDetectionParamsRegionParameters,
    'detectionStartTimeStampMS': int,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'unitInfo': UnitInfo,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'numthreads': int,
    'isPickExecution': Literal[-1, 0, 1],
    'ignoreInvalidDetectionFiles': bool,
    'runtimeDetectorParametersJSON': str,
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'cycleIndex': str,
    'defaultTaskParameters': GetTaskStateReturnsDetectionParamsDefaultTaskParameters,
}, total=False)

GetTaskStateReturnsVisionTaskParametersPlanningClientInfo = TypedDict('GetTaskStateReturnsVisionTaskParametersPlanningClientInfo', {
    'username': str,
    'commandTimeout': float,
    'heartbeatPort': int,
    'slaverequestid': str,
    'httpPort': int,
    'heartbeatTimeout': float,
    'host': str,
    'commandPort': int,
    'tasktype': str,
    'password': str,
    'sceneuri': str,
}, total=False)

GetTaskStateReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo = TypedDict('GetTaskStateReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo', {
    'yOffsetAtTop': float,
    'zOffsetAtTop': float,
    'use': bool,
    'xOffsetAtBottom': float,
    'yOffsetAtBottom': float,
    'zOffsetAtBottom': float,
    'xOffsetAtTop': float,
}, total=False)

GetTaskStateReturnsVisionTaskParametersRegionParametersMetaData = dict[str, Any]

GetTaskStateReturnsVisionTaskParametersRegionParameters = TypedDict('GetTaskStateReturnsVisionTaskParametersRegionParameters', {
    'containerName': str,
    'sensorSelectionInfos': SensorSelectionInfos,
    'containerUsage': str,
    'uri': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'rejectContainerIds': list[str],
    'locationName': str,
    'addPointOffsetInfo': GetTaskStateReturnsVisionTaskParametersRegionParametersAddPointOffsetInfo,
    'metaData': GetTaskStateReturnsVisionTaskParametersRegionParametersMetaData,
}, total=False)

GetTaskStateReturnsVisionTaskParametersRegisClientInfo = TypedDict('GetTaskStateReturnsVisionTaskParametersRegisClientInfo', {
    'username': str,
    'httpPort': int,
    'host': str,
    'password': str,
}, total=False)

GetTaskStateReturnsVisionTaskParametersDefaultTaskParameters = TypedDict('GetTaskStateReturnsVisionTaskParametersDefaultTaskParameters', {
    'populateTargetUri': str,
    'robotname': str,
    'sizeRoundUp': bool,
    'rollStepDegree': float,
    'heightIsAlwaysUncertain': bool,
    'randomBoxOrigin': list[float],
    'ignoreOverlapPointsFromNearbyTargets': float,
    'minCandidateMass': float,
    'belowBoxOverlap': float,
    'countOverlappingPoints': bool,
    'unitInfo': UnitInfo,
    'populateFnName': str,
    'pointSizeIncreaseMultForOverlapChecking': float,
    'sizePrecisionXYZ': list[float],
    'allowedPlacementOrientations': int,
    'addUnpickableRegionAcrossShortEdgeDist': bool,
    'ignoreOverlapPointsFromWall': bool,
    'maxCandidateMass': float,
}, total=False)

GetTaskStateReturnsVisionTaskParameters = TypedDict('GetTaskStateReturnsVisionTaskParameters', {
    'targetUpdateNamePrefix': str,
    'planningClientInfo': GetTaskStateReturnsVisionTaskParametersPlanningClientInfo,
    'robotBridgeClientInfo': RobotBridgeConnectionInfoParameters,
    'locale': str,
    'containerDetectionMode': Literal['once', 'always', 'never', 'onceOnChange'],
    'maxContainerNotFound': int,
    'targeturi': Optional[str],
    'useLocationState': bool,
    'maxNumFastDetection': int,
    'regionParameters': GetTaskStateReturnsVisionTaskParametersRegionParameters,
    'maxNumDetection': int,
    'waitTimeOnCaptureFailure': float,
    'forceClearRegion': bool,
    'stopOnNotNeedContainer': bool,
    'waitingMode': Literal['None', 'StartInWaiting', 'FirstDetectionAndWait'],
    'ignorePlanningState': bool,
    'isPickExecution': Literal[-1, 0, 1],
    'targetTemplateSceneDataJSON': str,
    'runtimeDetectorParametersJSON': str,
    'visionTaskType': Literal['Unknown', 'ObjectDetection', 'UpdateEnvironment', 'ControllerMonitor', 'ComputePointCloudObstacle', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SendExecutionVerification', 'ContainerDetection', 'RegisterGrabbedMVR', 'DetectionHistoryWriter'],
    'forceContainerDetectionOnceToAlways': bool,
    'regisClientInfo': GetTaskStateReturnsVisionTaskParametersRegisClientInfo,
    'detectionStartTimeStampMS': int,
    'ignoreDetectionFileUpdateChange': bool,
    'syncRobotBridgeTimeStampUS': int,
    'maxNumContainerDetection': int,
    'occlusionCheckInfo': OcclusionCheckInfo,
    'sensorBridgeClientInfo': SensorBridgeConnectionInfo,
    'executionVerificationMode': Literal['never', 'lastDetection', 'pointCloudOnChange', 'pointCloudAlways', 'pointCloudOnChangeWithDuration', 'pointCloudOnChangeFirstCycleOnly', 'pointCloudOnChangeAfterGrab'],
    'unitInfo': UnitInfo,
    'numthreads': int,
    'runtimeContainerDetectorParametersJSON': str,
    'ignoreInvalidDetectionFiles': bool,
    'detectionTriggerMode': Literal['AutoOnChange', 'WaitTrigger', 'Continuous'],
    'cycleIndex': str,
    'defaultTaskParameters': GetTaskStateReturnsVisionTaskParametersDefaultTaskParameters,
}, total=False)

GetTaskStateReturns = TypedDict('GetTaskStateReturns', {
    'taskParameters': GetTaskStateReturnsTaskParameters,
    'initializeTaskMS': int,
    'isStopTask': bool,
    'scenepk': str,
    'taskId': str,
    'taskStatus': str,
    'taskStatusMessage': str,
    'taskType': str,
    'hasFirstImagesForDetection': bool,
    'computePointCloudObstacleTaskId': str,
    'sendExecutionVerificationTaskId': str,
    'newerThanTimeStampMS': int,
    'detectionParams': GetTaskStateReturnsDetectionParams,
    'visionTaskParameters': GetTaskStateReturnsVisionTaskParameters,
    'resultTimestampMS': int,
    'resultImageEndTimestampMS': int,
}, total=False)

GetPublishedStateServiceReturns = TypedDict('GetPublishedStateServiceReturns', {
    'statusMessage': str,
    'tasks': list[Any],
    'timestamp': int,
    'version': str,
}, total=False)



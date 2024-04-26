from typing import TypedDict, List, Union, Dict, Any, Optional
from typing_extensions import Required
# This file contains typed dictionaries generated from the schemas in: mujinvisionmanager.schema.visionTaskParametersSchema

# The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details.
SystemState = TypedDict("SystemState", 
{   "sensorType": str,
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
    "sensorUsageType": str,}, total=False)

visionTaskSendExecutionVerificationParametersSchema_logging = TypedDict("visionTaskSendExecutionVerificationParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskSendExecutionVerificationParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskSendExecutionVerificationParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskSendExecutionVerificationParametersSchema_occlusionCheckInfo = TypedDict("visionTaskSendExecutionVerificationParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement = TypedDict("visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement = TypedDict("visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering = TypedDict("visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering", 
{   'cleanSizeXYZ': List[Any],
    'defaultMaxCleanSizeXYZ': List[float],
    'defaultMinCleanSizeXYZ': List[float],
    'filteringnumnn': int,
    'filteringstddev': float,
    'filteringsubsample': int,
    'medianFilterHalfSize': int,
    'percentageOfMinObjectDimForCleanSize': float,
    'pointsize': float,
    'radiusfilteringminnn': int,
    'radiusfilteringradius': float,
    'subsamplingMode': str,
    'unit': str}, total=False)

visionTaskSendExecutionVerificationParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskSendExecutionVerificationParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskSendExecutionVerificationParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskSendExecutionVerificationParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskSendExecutionVerificationParametersSchema_planningClientInfo = TypedDict("visionTaskSendExecutionVerificationParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskSendExecutionVerificationParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskSendExecutionVerificationParametersSchema_regisClientInfo = TypedDict("visionTaskSendExecutionVerificationParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

visionTaskSendExecutionVerificationParametersSchema = TypedDict("visionTaskSendExecutionVerificationParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'detectionTriggerMode': str,
    'dynamicPointCloudNameBase': str,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignorePlanningState': bool,
    'isPickExecution': bool,
    'locale': str,
    'locationName': str,
    'logging': visionTaskSendExecutionVerificationParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskSendExecutionVerificationParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskSendExecutionVerificationParametersSchema_planningClientInfo,
    'pointCloudFiltering': visionTaskSendExecutionVerificationParametersSchema_pointCloudFiltering,
    'regisClientInfo': visionTaskSendExecutionVerificationParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'robotBridgeClientInfo': visionTaskSendExecutionVerificationParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskSendExecutionVerificationParametersSchema_sensorBridgeClientInfo,
    'stopOnNotNeedContainer': bool,
    'useContainerMetaDataFromSignals': bool,
    'useLocationState': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

cropContainerEmptyMarginsSchema = TypedDict("cropContainerEmptyMarginsSchema", 
{   'negativeCropMargins': List[Any], 'positiveCropMargins': List[Any]}, total=False)

pointCloudFilteringParametersSchema_defaultMinCleanSizeXYZ_ArrayElement = TypedDict("pointCloudFilteringParametersSchema_defaultMinCleanSizeXYZ_ArrayElement", {}, total=False)

pointCloudFilteringParametersSchema_defaultMaxCleanSizeXYZ_ArrayElement = TypedDict("pointCloudFilteringParametersSchema_defaultMaxCleanSizeXYZ_ArrayElement", {}, total=False)

pointCloudFilteringParametersSchema = TypedDict("pointCloudFilteringParametersSchema", 
{   'cleanSizeXYZ': List[Any],
    'defaultMaxCleanSizeXYZ': List[float],
    'defaultMinCleanSizeXYZ': List[float],
    'filteringnumnn': int,
    'filteringstddev': float,
    'filteringsubsample': int,
    'medianFilterHalfSize': int,
    'percentageOfMinObjectDimForCleanSize': float,
    'pointsize': float,
    'radiusfilteringminnn': int,
    'radiusfilteringradius': float,
    'subsamplingMode': str,
    'unit': str}, total=False)

containerDetectionParametersSchema_regisClientInfo = TypedDict("containerDetectionParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

containerDetectionParametersSchema = TypedDict("containerDetectionParametersSchema", 
{   'detectionTriggerMode': str,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignorePlanningState': bool,
    'maxContainerNotFound': int,
    'maxNumContainerDetection': int,
    'regisClientInfo': containerDetectionParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'stopOnNotNeedContainer': bool,
    'useLocationState': bool}, total=False)

visionTaskControllerMonitorParametersSchema_logging = TypedDict("visionTaskControllerMonitorParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskControllerMonitorParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskControllerMonitorParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskControllerMonitorParametersSchema_occlusionCheckInfo = TypedDict("visionTaskControllerMonitorParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskControllerMonitorParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskControllerMonitorParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskControllerMonitorParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskControllerMonitorParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskControllerMonitorParametersSchema_planningClientInfo = TypedDict("visionTaskControllerMonitorParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskControllerMonitorParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskControllerMonitorParametersSchema = TypedDict("visionTaskControllerMonitorParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'enableCheckTextureless': bool,
    'enableMeasureHeightFromVision': bool,
    'locale': str,
    'locationName': str,
    'logging': visionTaskControllerMonitorParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskControllerMonitorParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskControllerMonitorParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskControllerMonitorParametersSchema_robotBridgeClientInfo,
    'saveMVRDebugInfo': bool,
    'sensorBridgeClientInfo': visionTaskControllerMonitorParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

sensorBridgeClientInfoSchema = TypedDict("sensorBridgeClientInfoSchema", 
{   'host': str, 'port': int, 'use': bool}, total=False)

objectDetectionParametersSchema_targetDynamicDetectorParameters_chuckingDirection_ArrayElement = TypedDict("objectDetectionParametersSchema_targetDynamicDetectorParameters_chuckingDirection_ArrayElement", {}, total=False)

objectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo = TypedDict("objectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo", 
{   'minNumSupportedFaces': float}, total=False)

objectDetectionParametersSchema_targetDynamicDetectorParameters = TypedDict("objectDetectionParametersSchema_targetDynamicDetectorParameters", 
{   'chuckingDirection': List[float],
    'hasOnlyOnePart': bool,
    'objectGraspModelInfo': objectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo,
    'objectMaxLoad': float,
    'objectPackingId': int,
    'objectType': str,
    'objectWeight': float,
    'partSize': List[Any]}, total=False)

objectDetectionParametersSchema_targetFetchURIs_ArrayElement = TypedDict("objectDetectionParametersSchema_targetFetchURIs_ArrayElement", {}, total=False)

objectDetectionParametersSchema_regisClientInfo = TypedDict("objectDetectionParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

objectDetectionParametersSchema = TypedDict("objectDetectionParametersSchema", 
{   'detectionTriggerMode': str,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignoreDetectionFileUpdateChange': bool,
    'ignorePlanningState': bool,
    'maxnumdetection': int,
    'maxnumfastdetection': int,
    'populateFnName': str,
    'regisClientInfo': objectDetectionParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'stopOnNotNeedContainer': bool,
    'targetDynamicDetectorParameters': objectDetectionParametersSchema_targetDynamicDetectorParameters,
    'targetFetchURIs': List[str],
    'targetupdatename': str,
    'useLocationState': bool}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_occlusionCheckInfo = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_logging = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering", 
{   'cleanSizeXYZ': List[Any],
    'defaultMaxCleanSizeXYZ': List[float],
    'defaultMinCleanSizeXYZ': List[float],
    'filteringnumnn': int,
    'filteringstddev': float,
    'filteringsubsample': int,
    'medianFilterHalfSize': int,
    'percentageOfMinObjectDimForCleanSize': float,
    'pointsize': float,
    'radiusfilteringminnn': int,
    'radiusfilteringradius': float,
    'subsamplingMode': str,
    'unit': str}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo = TypedDict("visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskComputePointCloudObstacleParametersSchema = TypedDict("visionTaskComputePointCloudObstacleParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'dynamicPointCloudNameBase': str,
    'locale': str,
    'locationName': str,
    'logging': visionTaskComputePointCloudObstacleParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskComputePointCloudObstacleParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskComputePointCloudObstacleParametersSchema_planningClientInfo,
    'pointCloudFiltering': visionTaskComputePointCloudObstacleParametersSchema_pointCloudFiltering,
    'robotBridgeClientInfo': visionTaskComputePointCloudObstacleParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskComputePointCloudObstacleParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

visionTaskUpdateEnvironmentParametersSchema_logging = TypedDict("visionTaskUpdateEnvironmentParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskUpdateEnvironmentParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskUpdateEnvironmentParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskUpdateEnvironmentParametersSchema_occlusionCheckInfo = TypedDict("visionTaskUpdateEnvironmentParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskUpdateEnvironmentParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskUpdateEnvironmentParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskUpdateEnvironmentParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskUpdateEnvironmentParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskUpdateEnvironmentParametersSchema_planningClientInfo = TypedDict("visionTaskUpdateEnvironmentParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskUpdateEnvironmentParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskUpdateEnvironmentParametersSchema = TypedDict("visionTaskUpdateEnvironmentParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'locale': str,
    'locationName': str,
    'logging': visionTaskUpdateEnvironmentParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskUpdateEnvironmentParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskUpdateEnvironmentParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskUpdateEnvironmentParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskUpdateEnvironmentParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

robotBridgeClientInfoSchema = TypedDict("robotBridgeClientInfoSchema", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

occlusionCheckInfoSchema = TypedDict("occlusionCheckInfoSchema", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

addPointOffsetInfoSchema = TypedDict("addPointOffsetInfoSchema", 
{   'use': bool,
    'xOffsetAtBottom': float,
    'xOffsetAtTop': float,
    'yOffsetAtBottom': float,
    'yOffsetAtTop': float,
    'zOffsetAtBottom': float,
    'zOffsetAtTop': float}, total=False)

visionTaskObjectDetectionParametersSchema_logging = TypedDict("visionTaskObjectDetectionParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskObjectDetectionParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskObjectDetectionParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters_chuckingDirection_ArrayElement = TypedDict("visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters_chuckingDirection_ArrayElement", {}, total=False)

visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo = TypedDict("visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo", 
{   'minNumSupportedFaces': float}, total=False)

visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters = TypedDict("visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters", 
{   'chuckingDirection': List[float],
    'hasOnlyOnePart': bool,
    'objectGraspModelInfo': visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters_objectGraspModelInfo,
    'objectMaxLoad': float,
    'objectPackingId': int,
    'objectType': str,
    'objectWeight': float,
    'partSize': List[Any]}, total=False)

visionTaskObjectDetectionParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement = TypedDict("visionTaskObjectDetectionParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskObjectDetectionParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement = TypedDict("visionTaskObjectDetectionParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskObjectDetectionParametersSchema_pointCloudFiltering = TypedDict("visionTaskObjectDetectionParametersSchema_pointCloudFiltering", 
{   'cleanSizeXYZ': List[Any],
    'defaultMaxCleanSizeXYZ': List[float],
    'defaultMinCleanSizeXYZ': List[float],
    'filteringnumnn': int,
    'filteringstddev': float,
    'filteringsubsample': int,
    'medianFilterHalfSize': int,
    'percentageOfMinObjectDimForCleanSize': float,
    'pointsize': float,
    'radiusfilteringminnn': int,
    'radiusfilteringradius': float,
    'subsamplingMode': str,
    'unit': str}, total=False)

visionTaskObjectDetectionParametersSchema_regisClientInfo = TypedDict("visionTaskObjectDetectionParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

visionTaskObjectDetectionParametersSchema_occlusionCheckInfo = TypedDict("visionTaskObjectDetectionParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskObjectDetectionParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskObjectDetectionParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskObjectDetectionParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskObjectDetectionParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskObjectDetectionParametersSchema_planningClientInfo = TypedDict("visionTaskObjectDetectionParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskObjectDetectionParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskObjectDetectionParametersSchema_targetFetchURIs_ArrayElement = TypedDict("visionTaskObjectDetectionParametersSchema_targetFetchURIs_ArrayElement", {}, total=False)

visionTaskObjectDetectionParametersSchema = TypedDict("visionTaskObjectDetectionParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'detectionTriggerMode': str,
    'dynamicPointCloudNameBase': str,
    'enableCheckTextureless': bool,
    'enableMeasureHeightFromVision': bool,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignoreDetectionFileUpdateChange': bool,
    'ignorePlanningState': bool,
    'isPickExecution': bool,
    'locale': str,
    'locationName': str,
    'logging': visionTaskObjectDetectionParametersSchema_logging,
    'maxnumdetection': int,
    'maxnumfastdetection': int,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskObjectDetectionParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskObjectDetectionParametersSchema_planningClientInfo,
    'pointCloudFiltering': visionTaskObjectDetectionParametersSchema_pointCloudFiltering,
    'populateFnName': str,
    'regisClientInfo': visionTaskObjectDetectionParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'robotBridgeClientInfo': visionTaskObjectDetectionParametersSchema_robotBridgeClientInfo,
    'saveMVRDebugInfo': bool,
    'sensorBridgeClientInfo': visionTaskObjectDetectionParametersSchema_sensorBridgeClientInfo,
    'stopOnNotNeedContainer': bool,
    'targetDynamicDetectorParameters': visionTaskObjectDetectionParametersSchema_targetDynamicDetectorParameters,
    'targetFetchURIs': List[str],
    'targetupdatename': str,
    'useContainerMetaDataFromSignals': bool,
    'useLocationState': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str,
    'syncRobotBridgeTimeStampUS': int}, total=False)

planningClientInfoSchema_defaultTaskParameters = TypedDict("planningClientInfoSchema_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

planningClientInfoSchema = TypedDict("planningClientInfoSchema", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': planningClientInfoSchema_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_logging = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_occlusionCheckInfo = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo = TypedDict("visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskDetectionHistoryWriterParametersSchema = TypedDict("visionTaskDetectionHistoryWriterParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'locale': str,
    'locationName': str,
    'logging': visionTaskDetectionHistoryWriterParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskDetectionHistoryWriterParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskDetectionHistoryWriterParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskDetectionHistoryWriterParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskDetectionHistoryWriterParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

regionDetectionParametersSchema = TypedDict("regionDetectionParametersSchema", {}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_occlusionCheckInfo = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_logging = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskRegisterGrabbedMVRParametersSchema = TypedDict("visionTaskRegisterGrabbedMVRParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'enableCheckTextureless': bool,
    'enableMeasureHeightFromVision': bool,
    'locale': str,
    'locationName': str,
    'logging': visionTaskRegisterGrabbedMVRParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskRegisterGrabbedMVRParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskRegisterGrabbedMVRParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskRegisterGrabbedMVRParametersSchema_robotBridgeClientInfo,
    'saveMVRDebugInfo': bool,
    'sensorBridgeClientInfo': visionTaskRegisterGrabbedMVRParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

regionParametersSchema_innerExtents_ArrayElement = TypedDict("regionParametersSchema_innerExtents_ArrayElement", {}, total=False)

regionParametersSchema_addPointOffsetInfo = TypedDict("regionParametersSchema_addPointOffsetInfo", 
{   'use': bool,
    'xOffsetAtBottom': float,
    'xOffsetAtTop': float,
    'yOffsetAtBottom': float,
    'yOffsetAtTop': float,
    'zOffsetAtBottom': float,
    'zOffsetAtTop': float}, total=False)

regionParametersSchema_rejectContainerIds_ArrayElement = TypedDict("regionParametersSchema_rejectContainerIds_ArrayElement", {}, total=False)

regionParametersSchema_ikparams_ArrayElement = TypedDict("regionParametersSchema_ikparams_ArrayElement", {}, total=False)

regionParametersSchema_outerExtents_ArrayElement = TypedDict("regionParametersSchema_outerExtents_ArrayElement", {}, total=False)

regionParametersSchema_validIntervalsX_ArrayElement = TypedDict("regionParametersSchema_validIntervalsX_ArrayElement", {}, total=False)

regionParametersSchema_validIntervalsY_ArrayElement = TypedDict("regionParametersSchema_validIntervalsY_ArrayElement", {}, total=False)

regionParametersSchema_regionDetectionParameters = TypedDict("regionParametersSchema_regionDetectionParameters", {}, total=False)

regionParametersSchema_geometryInfos_ArrayElement = TypedDict("regionParametersSchema_geometryInfos_ArrayElement", {}, total=False)

regionParametersSchema_metaData = TypedDict("regionParametersSchema_metaData", {}, total=False)

regionParametersSchema_sensorSelectionInfos_ArrayElement = TypedDict("regionParametersSchema_sensorSelectionInfos_ArrayElement", 
{   'sensorLinkName': Required[str], 'sensorName': Required[str]}, total=False)

regionParametersSchema = TypedDict("regionParametersSchema", 
{   'addPointOffsetInfo': regionParametersSchema_addPointOffsetInfo,
    'bindetectionMode': str,
    'bindetectionSearchXYZXYZ': List[Any],
    'containerDetectionMaxFractionGap': float,
    'containerEmptyDivisor': float,
    'containerName': str,
    'containerUsage': str,
    'expectedContainerId': str,
    'expectedContainerType': str,
    'geometryInfos': List[regionParametersSchema_geometryInfos_ArrayElement],
    'ikparams': List[regionParametersSchema_ikparams_ArrayElement],
    'innerExtents': List[float],
    'innerPose': List[Any],
    'instObjectInWorldPose': List[Any],
    'locationName': str,
    'metaData': regionParametersSchema_metaData,
    'negativeCropContainerEmptyMargins': List[Any],
    'negativeCropContainerMargins': List[Any],
    'outerExtents': List[float],
    'outerPose': List[Any],
    'positiveCropContainerEmptyMargins': List[Any],
    'positiveCropContainerMargins': List[Any],
    'regionDetectionParameters': regionParametersSchema_regionDetectionParameters,
    'rejectContainerIds': List[str],
    'sensorSelectionInfos': List[regionParametersSchema_sensorSelectionInfos_ArrayElement],
    'type': str,
    'unit': str,
    'uri': str,
    'validIntervalsX': List[List[Any]],
    'validIntervalsY': List[List[Any]]}, total=False)

visionTaskContainerDetectionParametersSchema_logging = TypedDict("visionTaskContainerDetectionParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskContainerDetectionParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskContainerDetectionParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskContainerDetectionParametersSchema_occlusionCheckInfo = TypedDict("visionTaskContainerDetectionParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskContainerDetectionParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement = TypedDict("visionTaskContainerDetectionParametersSchema_pointCloudFiltering_defaultMinCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskContainerDetectionParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement = TypedDict("visionTaskContainerDetectionParametersSchema_pointCloudFiltering_defaultMaxCleanSizeXYZ_ArrayElement", {}, total=False)

visionTaskContainerDetectionParametersSchema_pointCloudFiltering = TypedDict("visionTaskContainerDetectionParametersSchema_pointCloudFiltering", 
{   'cleanSizeXYZ': List[Any],
    'defaultMaxCleanSizeXYZ': List[float],
    'defaultMinCleanSizeXYZ': List[float],
    'filteringnumnn': int,
    'filteringstddev': float,
    'filteringsubsample': int,
    'medianFilterHalfSize': int,
    'percentageOfMinObjectDimForCleanSize': float,
    'pointsize': float,
    'radiusfilteringminnn': int,
    'radiusfilteringradius': float,
    'subsamplingMode': str,
    'unit': str}, total=False)

visionTaskContainerDetectionParametersSchema_regisClientInfo = TypedDict("visionTaskContainerDetectionParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

visionTaskContainerDetectionParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskContainerDetectionParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskContainerDetectionParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskContainerDetectionParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskContainerDetectionParametersSchema_planningClientInfo = TypedDict("visionTaskContainerDetectionParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskContainerDetectionParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskContainerDetectionParametersSchema = TypedDict("visionTaskContainerDetectionParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'detectionTriggerMode': str,
    'dynamicPointCloudNameBase': str,
    'enableCheckTextureless': bool,
    'enableMeasureHeightFromVision': bool,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignorePlanningState': bool,
    'isPickExecution': bool,
    'locale': str,
    'locationName': str,
    'logging': visionTaskContainerDetectionParametersSchema_logging,
    'maxContainerNotFound': int,
    'maxNumContainerDetection': int,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskContainerDetectionParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskContainerDetectionParametersSchema_planningClientInfo,
    'pointCloudFiltering': visionTaskContainerDetectionParametersSchema_pointCloudFiltering,
    'regisClientInfo': visionTaskContainerDetectionParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'robotBridgeClientInfo': visionTaskContainerDetectionParametersSchema_robotBridgeClientInfo,
    'saveMVRDebugInfo': bool,
    'sensorBridgeClientInfo': visionTaskContainerDetectionParametersSchema_sensorBridgeClientInfo,
    'stopOnNotNeedContainer': bool,
    'useContainerMetaDataFromSignals': bool,
    'useLocationState': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str,
    'syncRobotBridgeTimeStampUS': int}, total=False)

visionTaskParametersSchema_logging = TypedDict("visionTaskParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskParametersSchema_occlusionCheckInfo = TypedDict("visionTaskParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskParametersSchema_planningClientInfo = TypedDict("visionTaskParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskParametersSchema = TypedDict("visionTaskParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'locale': str,
    'locationName': str,
    'logging': visionTaskParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskParametersSchema_sensorBridgeClientInfo,
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

visionTaskVisualizePointCloudParametersSchema_sensorSelectionInfos_ArrayElement = TypedDict("visionTaskVisualizePointCloudParametersSchema_sensorSelectionInfos_ArrayElement", 
{   'sensorLinkName': Required[str], 'sensorName': Required[str]}, total=False)

visionTaskVisualizePointCloudParametersSchema_sensorBridgeClientInfo = TypedDict("visionTaskVisualizePointCloudParametersSchema_sensorBridgeClientInfo", 
{   'host': str, 'port': int, 'use': bool}, total=False)

visionTaskVisualizePointCloudParametersSchema_occlusionCheckInfo = TypedDict("visionTaskVisualizePointCloudParametersSchema_occlusionCheckInfo", 
{   'applyGrabbedState': bool,
    'cameraMoveThreshold': float,
    'checkPartialOcclusion': bool,
    'gridcolumns': int,
    'gridrows': int,
    'maxSnappingTimeDuration': float,
    'occlusionCheckMode': str,
    'paddingTime': float,
    'paddingTimeEnd': float,
    'paddingTimeStart': float,
    'partialocclusionthreshold': float,
    'robotname': str,
    'unit': str,
    'useLinkVisibility': bool,
    'useLocationState': bool}, total=False)

visionTaskVisualizePointCloudParametersSchema_logging = TypedDict("visionTaskVisualizePointCloudParametersSchema_logging", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

visionTaskVisualizePointCloudParametersSchema_robotBridgeClientInfo = TypedDict("visionTaskVisualizePointCloudParametersSchema_robotBridgeClientInfo", 
{   'basePort': int, 'host': str, 'queueid': str, 'use': bool}, total=False)

visionTaskVisualizePointCloudParametersSchema_planningClientInfo_defaultTaskParameters = TypedDict("visionTaskVisualizePointCloudParametersSchema_planningClientInfo_defaultTaskParameters", 
{   'countOverlappingPoints': bool}, total=False)

visionTaskVisualizePointCloudParametersSchema_planningClientInfo = TypedDict("visionTaskVisualizePointCloudParametersSchema_planningClientInfo", 
{   'commandPort': int,
    'commandTimeoutMS': float,
    'defaultTaskParameters': visionTaskVisualizePointCloudParametersSchema_planningClientInfo_defaultTaskParameters,
    'heartbeatPort': int,
    'heartbeatTimeoutMS': float,
    'host': str,
    'httpPort': int,
    'password': str,
    'scenepk': str,
    'slaverequestid': str,
    'tasktype': str,
    'uploadFilesWithNoModifyDate': bool,
    'username': str}, total=False)

visionTaskVisualizePointCloudParametersSchema = TypedDict("visionTaskVisualizePointCloudParametersSchema", 
{   'cycleIndex': str,
    'detectionStartTimeStampMS': int,
    'locale': str,
    'locationName': str,
    'logging': visionTaskVisualizePointCloudParametersSchema_logging,
    'numthreads': int,
    'occlusionCheckInfo': visionTaskVisualizePointCloudParametersSchema_occlusionCheckInfo,
    'planningClientInfo': visionTaskVisualizePointCloudParametersSchema_planningClientInfo,
    'robotBridgeClientInfo': visionTaskVisualizePointCloudParametersSchema_robotBridgeClientInfo,
    'sensorBridgeClientInfo': visionTaskVisualizePointCloudParametersSchema_sensorBridgeClientInfo,
    'sensorSelectionInfos': List[visionTaskVisualizePointCloudParametersSchema_sensorSelectionInfos_ArrayElement],
    'useContainerMetaDataFromSignals': bool,
    'waitTimeOnCaptureFailureMS': float,
    'waitingMode': str}, total=False)

visionTaskLoggingInfoSchema = TypedDict("visionTaskLoggingInfoSchema", 
{   'logMode': str, 'maxUsedSpaceFraction': float, 'numVisionCyclesToKeep': int, 'numberOfImages': int}, total=False)

detectionParametersSchema_regisClientInfo = TypedDict("detectionParametersSchema_regisClientInfo", 
{   'registrationIp': str,
    'registrationObjectSetPk': str,
    'registrationPort': int,
    'registrationpassword': str,
    'registrationusername': str}, total=False)

detectionParametersSchema = TypedDict("detectionParametersSchema", 
{   'detectionTriggerMode': str,
    'executionVerificationMode': str,
    'forceClearRegion': bool,
    'ignorePlanningState': bool,
    'regisClientInfo': detectionParametersSchema_regisClientInfo,
    'registrationObjectSetPK': str,
    'stopOnNotNeedContainer': bool,
    'useLocationState': bool}, total=False)

mujinControllerClientInfoSchema = TypedDict("mujinControllerClientInfoSchema", 
{   'host': str, 'httpPort': int, 'password': str, 'uploadFilesWithNoModifyDate': bool, 'username': str}, total=False)
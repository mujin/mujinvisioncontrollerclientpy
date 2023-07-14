// -*- coding: utf-8 -*-
// Copyright (C) 2022 Mujin,Inc.
// GENERATED FILE! DO NOT EDIT!
#ifndef MUJIN_VISIONCONTROLLERCLIENT_H
#define MUJIN_VISIONCONTROLLERCLIENT_H

#include <vector>

#include <mujincontrollercommon/datapool.h>
#include <mujincontrollercommon/mujincontrollercommon.h>
#include <mujincontrollercommon/mujinjson.h>
#include <mujincontrollercommon/zmq.hpp>
#include <mujincontrollercommon/zmqclient.h>

#include <mujinvisioncontrollerclient/config.h>

#include <rapidjson/document.h>
#include <rapidjson/memorybuffer.h>
#include <boost/function.hpp>
#include <boost/thread/tss.hpp>

namespace mujinvisioncontrollerclient {

class MUJINVISIONCONTROLLERCLIENT_API VisionControllerClientException : public mujincontrollercommon::MujinExceptionBase
{
public:
    enum VisionControllerClientErrorCode : uint32_t
    {
        // TODO(heman.gandhi): Fix the error masks below
        VCCEC_Failed = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 0,
        VCCEC_Assert = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 1,
        VCCEC_FailedToSendZMQRequest = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 2,       ///< failed to send a zmq command
        VCCEC_InvalidZMQResponse = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 3,    ///< invalid or unexpected data got received from the command
        VCCEC_CallTimeout = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 4,  ///< did not get the sensorbridge response
        VCCEC_ZMQRecvError = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 5, ///< failed to recv
        VCCEC_InvalidArgument = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 6, ///< invalid argument
        VCCEC_UnexpectedReturnData = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 7, ///< unexpected return data
    };

    static MUJINVISIONCONTROLLERCLIENT_API const char* GetVisionControllerClientErrorCodeString(VisionControllerClientErrorCode error);

    VisionControllerClientException(
        const std::string& s,
        VisionControllerClientErrorCode code = VCCEC_Failed,
        const std::string& countermeasure = std::string())
    {
        _s = "MujinVisionControllerClient (" + (GetVisionControllerClientErrorCodeString(code) + ("): " + s));
        _code = code;
        _countermeasure = countermeasure;
    }

    virtual ~VisionControllerClientException() throw() {}

    const char *GetCodeString() const override {
        return GetVisionControllerClientErrorCodeString(static_cast<VisionControllerClientErrorCode>(_code));
    }
};


class MUJINVISIONCONTROLLERCLIENT_API VisionControllerClient
{

public:
    VisionControllerClient(
        boost::shared_ptr<zmq::context_t>& context,
        const std::string& host = std::string("127.0.0.1"),
        const uint16_t port = 5718,
        const uint64_t timeoutMS = 200,
        const std::string& callerId = std::string());
    virtual ~VisionControllerClient();

    VisionControllerClient(VisionControllerClient const &) = delete;
    VisionControllerClient & operator=(VisionControllerClient const &) = delete;
    VisionControllerClient & operator=(VisionControllerClient &&) = delete;

    void SetConnectionInfo(const std::string& host, const uint16_t port);

    void SetCallerId(const char* callerId) {
        _callerId = callerId;
    }

    void SetCallerId(const std::string& callerId) {
        _callerId = callerId;
    }

    /// \brief Send a command to sensorbridge command socket and receive the result
    void SendAndReceiveCommand(
        const std::string& command,
        const rapidjson::Value& rParameterValue,
        rapidjson::Value& rReturnValue,
        rapidjson::Document::AllocatorType& rReturnAlloc,
        double timeout)
    {
        _SendAndReceiveFromSocket(_currentCommandSocket, command, rParameterValue, rReturnValue, rReturnAlloc, timeout);
    }

    /// \brief Send a command to sensorbridge config socket and receive the result
    void SendAndReceiveConfig(
        const std::string& command,
        const rapidjson::Value& rParameterValue,
        rapidjson::Value& rReturnValue,
        rapidjson::Document::AllocatorType& rReturnAlloc,
        double timeout)
    {
        _SendAndReceiveFromSocket(_currentConfigSocket, command, rParameterValue, rReturnValue, rReturnAlloc, timeout);
    }


    // GENERATED API

    ///
    /// 
    ///    
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void GetPublishedStateService(double timeout = 4.0);

    ///
    /// 
    ///    
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void Ping(double timeout = 2.0);

    ///
    /// Sets the log level for the visionmanager.
    ///    
    /// \param componentLevels (rapidjson::Value&): A dictionary of component names and their respective log levels.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void SetLogLevel(const rapidjson::Value& componentLevels, double timeout = 2.0);

    ///
    /// Cancels the current command.
    ///    
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void Cancel(double timeout = 2.0);

    ///
    /// Quits the visionmanager.
    ///    
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void Quit(double timeout = 2.0);

    ///
    /// Gets the task state of the visionmanager.
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    taskParameters (rapidjson::Value&): describes the task specific parameters if present, eg. detection params, execution verification params.. 
    ///    initializeTaskMS (int32_t): timestamp at which the task was received and initialized , in ms (linux epoch) 
    ///    isStopTask (bool): True if task is currently running 
    ///    scenepk (std::string&): scene file name 
    ///    taskId (std::string&): The taskId for which the status was requested 
    ///    taskStatus (std::string&): status of the task 
    ///    taskStatusMessage (std::string&): describes the task status 
    ///    taskType (std::string&): The task type for which the status was requested 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param taskId (std::string&): If specified, the taskId to retrieve the detected objects from.     
    /// \param taskType (std::string&): the taskType for which the status was requested     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void GetTaskStateService(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const std::string& cycleIndex, const std::string& taskId, const std::string& taskType, double timeout = 4.0);

    ///
    /// Gets the latest vision stats.
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): a list of all currently active vision task statistics. Each task statistics have the following structure A JSON object (rapidjson::Value) with structure:
    ///    cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles. 
    ///    taskId (std::string&): The taskId. 
    ///    taskType (std::string&): The task type. 
    ///    taskStartTimeMS (int32_t):  
    ///    totalDetectionTimeMS (int32_t):  
    ///    totalDetectionCount (int32_t):  
    ///    totalGetImagesCount (int32_t):  
    ///    targetURIs (int32_t):  
    ///    detectionHistory (void *):  
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param taskId (std::string&): If specified, the taskId.     
    /// \param taskType (std::string&): The task type.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void GetVisionStatistics(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const std::string& cycleIndex, const std::string& taskId, const std::string& taskType, double timeout = 3000.0);

    ///
    /// Gets the latest detected objects.
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): a list of the latest detection results, having the structure A JSON object (rapidjson::Value) with structure:
    ///    cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles. 
    ///    detectedObjects (void *):  
    ///    detectionResultState (rapidjson::Value&):  
    ///    imageEndTimeStampMS (int32_t):  
    ///    imageStartTimestampMS (int32_t):  
    ///    locationName (std::string&):  
    ///    pointCloudId (std::string&):  
    ///    resultTimestampMS (int32_t):  
    ///    sensorSelectionInfos (void *):  
    ///    statsUID (std::string&):  
    ///    targetUpdateName (std::string&):  
    ///    taskId (std::string&):  
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param taskId (std::string&): If specified, the taskId to retrieve the detected objects from.     
    /// \param taskType (std::string&): The task type to retrieve the detected objects from.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void GetLatestDetectedObjects(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const std::string& cycleIndex, const std::string& taskId, const std::string& taskType, double timeout = 3000.0);

    /// \brief options for configuring GetLatestDetectionResultImages commands.
    /// See the member documentation for more details.
    struct GetLatestDetectionResultImagesOptions {
        /// \brief Construct the GetLatestDetectionResultImagesOptions, with all the required parameters.
        explicit GetLatestDetectionResultImagesOptions(const std::vector<uint8_t>& imageTypes, int32_t limit, const rapidjson::Value& sensorSelectionInfo, const std::string& taskId, const std::string& taskType, const std::string& cycleIndex) :
            _imageTypes(imageTypes),
            _limit(limit),
            _sensorSelectionInfo(&sensorSelectionInfo),
            _taskId(taskId),
            _taskType(taskType),
            _cycleIndex(cycleIndex)
        {}

        ///        
        /// \param newerThanResultTimestampMS (int32_t): If specified, starttimestamp of the image must be newer than this value in milliseconds. 
        ///
        int32_t _newerThanResultTimestampMS = 0;
        ///        
        /// \param metadataOnly (bool): Default: False 
        ///
        bool _metadataOnly = false;
        ///        
        /// \param imageTypes (std::vector<uint8_t>&): Mujin image types 
        ///
        std::vector<uint8_t> _imageTypes;
        ///        
        /// \param limit (int32_t):  
        ///
        int32_t _limit;
        ///        
        /// \param sensorSelectionInfo (rapidjson::Value&):  
        ///
        const rapidjson::Value* _sensorSelectionInfo;
        ///        
        /// \param taskId (std::string&): If specified, the taskId. 
        ///
        std::string _taskId;
        ///        
        /// \param taskType (std::string&): The task type. 
        ///
        std::string _taskType;
        ///        
        /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles. 
        ///
        std::string _cycleIndex;

        /// \brief Save these options to the JSON value provided. Destroys the input value.
        void SaveToJson(rapidjson::Value& rValue, rapidjson::Document::AllocatorType& alloc) const;
    };

    ///
    /// Gets the latest detected result images.
    ///    
    /// \param returnValue (std::string&): Raw image data 
    /// \param options (const GetLatestDetectionResultImagesOptions&): The options for this command, passed into the JSON payload.    
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed.     
    /// \param blockwait (bool):  
    ///
    void GetLatestDetectionResultImages(std::string& returnValue, const GetLatestDetectionResultImagesOptions& options, double timeout = 3000.0, bool blockwait = true);

    ///
    /// Gets detection result with given timestamp (sensor time)
    ///    
    /// \param returnValue (std::string&): Binary blob of detection data     
    /// \param timestamp (int32_t): Unix timestamp in milliseconds     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void GetDetectionHistory(std::string& returnValue, int32_t timestamp, double timeout = 3000.0);

    ///
    /// Backs up the vision log for a given cycle index
    ///    
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param sensorTimestamps (std::vector<double>&): The sensor timestamps to backup     
    /// \param fireandforget (bool): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void BackupDetectionLog(const std::string& cycleIndex, const std::vector<double>& sensorTimestamps, double timeout = 2.0, bool fireandforget = false);

    ///
    /// Stops a set of tasks that meet the filter criteria
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    isStopped (bool): true, if the specific taskId or set of tasks with a specific taskType(s) is stopped 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param taskTypes (std::vector<std::string>&): If specified, a list of task types to stop.     
    /// \param waitForStop (bool): If True, then wait for task to stop, otherwise just trigger it to stop, but do not wait     
    /// \param removeTask (bool): If True, then remove the task from being tracked by the vision manager and destroy all its resources. Will wait for the task to end before returning.     
    /// \param taskId (std::string&): If specified, the specific taskId to stop     
    /// \param taskType (std::string&): The task type to stop.     
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed.     
    /// \param fireandforget (bool): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. 
    ///
    void StopTask(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const std::string& cycleIndex, bool removeTask, const std::string& taskId, const std::string& taskType, const std::vector<std::string>& taskTypes, bool waitForStop, double timeout = 3000.0, bool fireandforget = false);

    ///
    /// Resumes a set of tasks that meet the filter criteria
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    taskIds (std::vector<std::string>&): List of taskIds that have been resumed 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param taskTypes (std::vector<std::string>&): If specified, a list of task types to resume     
    /// \param waitForStop (bool): DEPRECATED. This is unused.     
    /// \param taskId (std::string&): If specified, the specific taskId to resume     
    /// \param taskType (std::string&): The task type to resume.     
    /// \param cycleIndex (std::string&): Unique cycle index string for tracking, backing up, and differentiating cycles.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed.     
    /// \param fireandforget (bool): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server. 
    ///
    void ResumeTask(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const std::string& cycleIndex, const std::string& taskId, const std::string& taskType, const std::vector<std::string>& taskTypes, bool waitForStop, double timeout = 3000.0, bool fireandforget = false);

    ///
    /// Starts detection thread to continuously detect objects. the vision server will send detection results directly to mujin controller.
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    taskId (std::string&): The taskId of the created task 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param systemState (rapidjson::Value&): A set of rules that select a profile. Each property is checked in the given order to select the profile that will be applied.
    ///    
    ///    Unset fields are not considered during the selection.
    ///    
    ///    See the documentation for more explanation. A JSON object (rapidjson::Value) with structure:
    ///    profileId (std::string&): Profile ID selected by this profile selector 
    ///    sensorType (std::string&): The type of sensor that is being used. 
    ///    
    ///    This is a unique identifier of the sensor model. 
    ///    sensorName (std::string&): The name of the sensor that is being used, e.g. source_camera, dest_camera...
    ///    
    ///    This can be found in the Scene Editor or the application settings. 
    ///    sensorLinkName (std::string&): The link name of the sensor that is being used.
    ///    
    ///    The link name can be found by selecting the combined sensor's body in the Scene Editor. 
    ///    locationName (std::string&): The location that is being considered, e.g. source, destination_1, destination_2...
    ///    
    ///    The location names can be modified in the Scene Editor. 
    ///    partType (std::string&): The type of part that is being detected or picked, e.g. 'Bolt_8mm', 'Ring_d50_h80', 'Cereal_Bag_Large'...
    ///    
    ///    This field can be used to set different sensor/detection settings and transfer speeds for specific parts. It refers to the unique identifier for each part.
    ///    
    ///    For referring to families of parts, see the 'objectType' field. 
    ///    graspSetName (std::string&): The name of the grasp set that is being considered.
    ///    
    ///    This field can be used to select a profile with e.g. more cautious transfer speeds for grasps that are less stable. 
    ///    objectType (std::string&): The type of object that is being detected or picked, e.g. 'box', 'box_with_flap', 'cylinder'...
    ///    
    ///    This field can be used to choose different detection approaches. 
    ///    objectMaterialType (std::string&): The material that the object is made of, e.g. 'rubber', 'cardboard'...
    ///    
    ///    This field can be used to e.g. increase exposure and/or gain when detecting materials that absorb a lot of light.
    ///    
    ///    A part's material can be checked by inspecting it in the parts manager. 
    ///    scenarioId (std::string&): The scenario that is being used.
    ///    
    ///    The 'scenario' is a setting that overrides configuration parameters of the system temporarily. A scenario may be active when testing a new setup. Scenarios are generally set when the system is started and do not change during operation.
    ///    
    ///    See the configuration to determine which scenarios are used in your system. 
    ///    applicationType (std::string&): The type of application that is being used, e.g. 'binpicking', 'depalletizing', 'palletizing', 'calibrationCameraWithRobot, 'calibrationCameraSingleShot'...
    ///    
    ///    For custom applications, the string is defined in the application. 
    ///    detectionTriggerType (std::string&): The type of detection trigger that is sent to vision when the robot has moved to the camera position, e.g. 'detection', 'pointCloudObstacle'...
    ///    
    ///    See the detectionTriggerType description in the binpicking parameters for more information. 
    ///    detectionState (std::string&): The state/result of the current detection, e.g. 'ImageTooDark', 'FewCandidates', 'Success'...
    ///    
    ///    This field can be used to e.g. increase exposure when detection is in a certain state. 
    ///    sensorUsageType (std::string&): Specifies what the captured data will be used for, e.g. 'Detection', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SourceExecutionVerification', 'DestExecutionVerification'.
    ///    
    ///    This field can be used to configure e.g. faster capturing when the resulting data will not be used for detection.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void StartObjectDetectionTask(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const rapidjson::Value& systemState, double timeout = 3000.0);

    ///
    /// Starts container detection thread to continuously detect a container. the vision server will send detection results directly to mujin controller.
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    taskId (std::string&): The taskId of the created task 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param systemState (rapidjson::Value&): A set of rules that select a profile. Each property is checked in the given order to select the profile that will be applied.
    ///    
    ///    Unset fields are not considered during the selection.
    ///    
    ///    See the documentation for more explanation. A JSON object (rapidjson::Value) with structure:
    ///    profileId (std::string&): Profile ID selected by this profile selector 
    ///    sensorType (std::string&): The type of sensor that is being used. 
    ///    
    ///    This is a unique identifier of the sensor model. 
    ///    sensorName (std::string&): The name of the sensor that is being used, e.g. source_camera, dest_camera...
    ///    
    ///    This can be found in the Scene Editor or the application settings. 
    ///    sensorLinkName (std::string&): The link name of the sensor that is being used.
    ///    
    ///    The link name can be found by selecting the combined sensor's body in the Scene Editor. 
    ///    locationName (std::string&): The location that is being considered, e.g. source, destination_1, destination_2...
    ///    
    ///    The location names can be modified in the Scene Editor. 
    ///    partType (std::string&): The type of part that is being detected or picked, e.g. 'Bolt_8mm', 'Ring_d50_h80', 'Cereal_Bag_Large'...
    ///    
    ///    This field can be used to set different sensor/detection settings and transfer speeds for specific parts. It refers to the unique identifier for each part.
    ///    
    ///    For referring to families of parts, see the 'objectType' field. 
    ///    graspSetName (std::string&): The name of the grasp set that is being considered.
    ///    
    ///    This field can be used to select a profile with e.g. more cautious transfer speeds for grasps that are less stable. 
    ///    objectType (std::string&): The type of object that is being detected or picked, e.g. 'box', 'box_with_flap', 'cylinder'...
    ///    
    ///    This field can be used to choose different detection approaches. 
    ///    objectMaterialType (std::string&): The material that the object is made of, e.g. 'rubber', 'cardboard'...
    ///    
    ///    This field can be used to e.g. increase exposure and/or gain when detecting materials that absorb a lot of light.
    ///    
    ///    A part's material can be checked by inspecting it in the parts manager. 
    ///    scenarioId (std::string&): The scenario that is being used.
    ///    
    ///    The 'scenario' is a setting that overrides configuration parameters of the system temporarily. A scenario may be active when testing a new setup. Scenarios are generally set when the system is started and do not change during operation.
    ///    
    ///    See the configuration to determine which scenarios are used in your system. 
    ///    applicationType (std::string&): The type of application that is being used, e.g. 'binpicking', 'depalletizing', 'palletizing', 'calibrationCameraWithRobot, 'calibrationCameraSingleShot'...
    ///    
    ///    For custom applications, the string is defined in the application. 
    ///    detectionTriggerType (std::string&): The type of detection trigger that is sent to vision when the robot has moved to the camera position, e.g. 'detection', 'pointCloudObstacle'...
    ///    
    ///    See the detectionTriggerType description in the binpicking parameters for more information. 
    ///    detectionState (std::string&): The state/result of the current detection, e.g. 'ImageTooDark', 'FewCandidates', 'Success'...
    ///    
    ///    This field can be used to e.g. increase exposure when detection is in a certain state. 
    ///    sensorUsageType (std::string&): Specifies what the captured data will be used for, e.g. 'Detection', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SourceExecutionVerification', 'DestExecutionVerification'.
    ///    
    ///    This field can be used to configure e.g. faster capturing when the resulting data will not be used for detection.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void StartContainerDetectionTask(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const rapidjson::Value& systemState, double timeout = 3000.0);

    ///
    /// Start point cloud visualization thread to sync camera info from the mujin controller and send the raw camera point clouds to mujin controller
    ///
    /// 
    /// \param returnValue (rapidjson::Value&): The JSON Value that holds the returned output. A JSON object (rapidjson::Value) with structure:
    ///    taskId (std::string&): The taskId of the created task 
    /// \param rReturnAlloc (rapidjson::Document::AllocatorType&): The allocator for the returned JSON value.    
    /// \param systemState (rapidjson::Value&): A set of rules that select a profile. Each property is checked in the given order to select the profile that will be applied.
    ///    
    ///    Unset fields are not considered during the selection.
    ///    
    ///    See the documentation for more explanation. A JSON object (rapidjson::Value) with structure:
    ///    profileId (std::string&): Profile ID selected by this profile selector 
    ///    sensorType (std::string&): The type of sensor that is being used. 
    ///    
    ///    This is a unique identifier of the sensor model. 
    ///    sensorName (std::string&): The name of the sensor that is being used, e.g. source_camera, dest_camera...
    ///    
    ///    This can be found in the Scene Editor or the application settings. 
    ///    sensorLinkName (std::string&): The link name of the sensor that is being used.
    ///    
    ///    The link name can be found by selecting the combined sensor's body in the Scene Editor. 
    ///    locationName (std::string&): The location that is being considered, e.g. source, destination_1, destination_2...
    ///    
    ///    The location names can be modified in the Scene Editor. 
    ///    partType (std::string&): The type of part that is being detected or picked, e.g. 'Bolt_8mm', 'Ring_d50_h80', 'Cereal_Bag_Large'...
    ///    
    ///    This field can be used to set different sensor/detection settings and transfer speeds for specific parts. It refers to the unique identifier for each part.
    ///    
    ///    For referring to families of parts, see the 'objectType' field. 
    ///    graspSetName (std::string&): The name of the grasp set that is being considered.
    ///    
    ///    This field can be used to select a profile with e.g. more cautious transfer speeds for grasps that are less stable. 
    ///    objectType (std::string&): The type of object that is being detected or picked, e.g. 'box', 'box_with_flap', 'cylinder'...
    ///    
    ///    This field can be used to choose different detection approaches. 
    ///    objectMaterialType (std::string&): The material that the object is made of, e.g. 'rubber', 'cardboard'...
    ///    
    ///    This field can be used to e.g. increase exposure and/or gain when detecting materials that absorb a lot of light.
    ///    
    ///    A part's material can be checked by inspecting it in the parts manager. 
    ///    scenarioId (std::string&): The scenario that is being used.
    ///    
    ///    The 'scenario' is a setting that overrides configuration parameters of the system temporarily. A scenario may be active when testing a new setup. Scenarios are generally set when the system is started and do not change during operation.
    ///    
    ///    See the configuration to determine which scenarios are used in your system. 
    ///    applicationType (std::string&): The type of application that is being used, e.g. 'binpicking', 'depalletizing', 'palletizing', 'calibrationCameraWithRobot, 'calibrationCameraSingleShot'...
    ///    
    ///    For custom applications, the string is defined in the application. 
    ///    detectionTriggerType (std::string&): The type of detection trigger that is sent to vision when the robot has moved to the camera position, e.g. 'detection', 'pointCloudObstacle'...
    ///    
    ///    See the detectionTriggerType description in the binpicking parameters for more information. 
    ///    detectionState (std::string&): The state/result of the current detection, e.g. 'ImageTooDark', 'FewCandidates', 'Success'...
    ///    
    ///    This field can be used to e.g. increase exposure when detection is in a certain state. 
    ///    sensorUsageType (std::string&): Specifies what the captured data will be used for, e.g. 'Detection', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SourceExecutionVerification', 'DestExecutionVerification'.
    ///    
    ///    This field can be used to configure e.g. faster capturing when the resulting data will not be used for detection.     
    /// \param timeout (double): Time in seconds after which the command is assumed to have failed. 
    ///
    void StartVisualizePointCloudTask(rapidjson::Value& returnValue, rapidjson::Document::AllocatorType& rReturnAlloc, const rapidjson::Value& systemState, double timeout = 3000.0);


    // END GENERATED API

private:
    typedef std::pair<rapidjson::MemoryBuffer, VisionControllerClient *> SendDataEntry; /// holds the memory buffer and a pointer to a send buffer

    void _EnsureSocket(boost::shared_ptr<zmq::socket_t> socket);

    void _SendAndReceiveFromSocket(
        boost::shared_ptr<zmq::socket_t> socket,
        const std::string& command,
        const rapidjson::Value& rParameterValue,
        rapidjson::Value& rReturnValue,
        rapidjson::Document::AllocatorType& rReturnAlloc,
        double timeout);

    /// @brief Send command. Tries reconnecting once.
    void _SendCommand(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS);

    /// @brief Receive response.
    void _ReceiveResponse(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS);

    /// @brief Send JSON command.
    void _SendCommandJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Value& rCommand, rapidjson::Document::AllocatorType& rAlloc, const char* commandString, uint64_t timeoutMS);

    /// @brief Receive and deserialize JSON response in rapidjson::Value.
    void _ReceiveResponseJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Document& rResponse, const char* commandString, uint64_t timeoutMS);

    static void _ReleaseSendBuffer(void* mbSendSendBufferData, void* sendDataEntry);

    // don't change the order
    mutable boost::shared_ptr<zmq::context_t> _context;
    std::string _host = "127.0.0.1";
    uint16_t _port = 5718;
    uint64_t _timeoutMS = 200;
    std::string _callerId; ///< 'callerid' passed into all the sensorbridge commands

    boost::shared_ptr<mujincontrollercommon::ZmqSocketPool> _commandSocketPool; ///< pool to create command sockets
    boost::shared_ptr<zmq::socket_t> _currentCommandSocket;                     ///< current created command socket
    boost::shared_ptr<mujincontrollercommon::ZmqSocketPool> _configSocketPool; ///< pool to create config sockets
    boost::shared_ptr<zmq::socket_t> _currentConfigSocket;                     ///< current created config socket

    std::vector<uint8_t> _vRapidJsonBuffer;                      ///< for internal rapidjson documents
    boost::shared_ptr<rapidjson::MemoryPoolAllocator<>> _rAlloc; ///< allocator for command rapidjson documents

    boost::shared_ptr<mujincontrollercommon::DataPool<SendDataEntry>> _sendDataPool;
};

typedef boost::shared_ptr<VisionControllerClient> VisionControllerClientPtr;

} // end namespace mujinsensorbridgeclient

#endif // MUJIN_VISIONCONTROLLERCLIENT_H
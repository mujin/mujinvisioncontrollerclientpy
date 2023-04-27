from . import _


class SystemState(dict):
    """The state of the system. Used to select the profile that the vision task will use. See "Profile Selection" documentation for more details."""

    @property
    def sensorType(self):
        """The type of sensor that is being used. 

        This is a unique identifier of the sensor model."""
        return self.get('sensorType')

    @sensorType.setter
    def sensorType(self, value):
        self['sensorType'] = value

    @property
    def sensorName(self):
        """The name of the sensor that is being used, e.g. source_camera, dest_camera...

        This can be found in the Scene Editor or the application settings."""
        return self.get('sensorName')

    @sensorName.setter
    def sensorName(self, value):
        self['sensorName'] = value

    @property
    def sensorLinkName(self):
        """The link name of the sensor that is being used.

        The link name can be found by selecting the combined sensor's body in the Scene Editor."""
        return self.get('sensorLinkName')

    @sensorLinkName.setter
    def sensorLinkName(self, value):
        self['sensorLinkName'] = value

    @property
    def visionTaskType(self):
        """The type of vision task that is being executed. E.g. 'visualizePointCloud', 'objectDetection'..."""
        return self.get('visionTaskType')

    @visionTaskType.setter
    def visionTaskType(self, value):
        self['visionTaskType'] = value

    @property
    def locationName(self):
        """The location that is being considered, e.g. source, destination_1, destination_2...

        The location names can be modified in the Scene Editor."""
        return self.get('locationName')

    @locationName.setter
    def locationName(self, value):
        self['locationName'] = value

    @property
    def partType(self):
        """The type of part that is being detected or picked, e.g. 'Bolt_8mm', 'Ring_d50_h80', 'Cereal_Bag_Large'...

        This field can be used to set different sensor/detection settings and transfer speeds for specific parts. It refers to the unique identifier for each part.

        For referring to families of parts, see the 'objectType' field."""
        return self.get('partType')

    @partType.setter
    def partType(self, value):
        self['partType'] = value

    @property
    def graspSetName(self):
        """The name of the grasp set that is being considered.

        This field can be used to select a profile with e.g. more cautious transfer speeds for grasps that are less stable."""
        return self.get('graspSetName')

    @graspSetName.setter
    def graspSetName(self, value):
        self['graspSetName'] = value

    @property
    def objectType(self):
        """The type of object that is being detected or picked, e.g. 'box', 'box_with_flap', 'cylinder'...

        This field can be used to choose different detection approaches."""
        return self.get('objectType')

    @objectType.setter
    def objectType(self, value):
        self['objectType'] = value

    @property
    def objectMaterialType(self):
        """The material that the object is made of, e.g. 'rubber', 'cardboard'...

        This field can be used to e.g. increase exposure and/or gain when detecting materials that absorb a lot of light.

        A part's material can be checked by inspecting it in the parts manager."""
        return self.get('objectMaterialType')

    @objectMaterialType.setter
    def objectMaterialType(self, value):
        self['objectMaterialType'] = value

    @property
    def scenarioId(self):
        """The scenario that is being used.

        The 'scenario' is a setting that overrides configuration parameters of the system temporarily. A scenario may be active when testing a new setup. Scenarios are generally set when the system is started and do not change during operation.

        See the configuration to determine which scenarios are used in your system."""
        return self.get('scenarioId')

    @scenarioId.setter
    def scenarioId(self, value):
        self['scenarioId'] = value

    @property
    def applicationType(self):
        """The type of application that is being used, e.g. 'binpicking', 'depalletizing', 'palletizing', 'calibrationCameraWithRobot, 'calibrationCameraSingleShot'...

        For custom applications, the string is defined in the application."""
        return self.get('applicationType')

    @applicationType.setter
    def applicationType(self, value):
        self['applicationType'] = value

    @property
    def detectionTriggerType(self):
        """The type of detection trigger that is sent to vision when the robot has moved to the camera position, e.g. 'detection', 'pointCloudObstacle'...

        See the detectionTriggerType description in the binpicking parameters for more information."""
        return self.get('detectionTriggerType')

    @detectionTriggerType.setter
    def detectionTriggerType(self, value):
        self['detectionTriggerType'] = value

    @property
    def detectionState(self):
        """The state/result of the current detection, e.g. 'ImageTooDark', 'FewCandidates', 'Success'...

        This field can be used to e.g. increase exposure when detection is in a certain state."""
        return self.get('detectionState')

    @detectionState.setter
    def detectionState(self, value):
        self['detectionState'] = value

    @property
    def sensorUsageType(self):
        """Specifies what the captured data will be used for, e.g. 'Detection', 'SendPointCloudObstacle', 'VisualizePointCloud', 'SourceExecutionVerification', 'DestExecutionVerification'.

        This field can be used to configure e.g. faster capturing when the resulting data will not be used for detection."""
        return self.get('sensorUsageType')

    @sensorUsageType.setter
    def sensorUsageType(self, value):
        self['sensorUsageType'] = value

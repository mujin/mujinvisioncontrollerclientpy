# Change log

## 0.13.0 (2023-04-25)

### Breaking changes

- Removed unused functions: `IsDetectionRunning`, `GetRunningState`, `SendVisionManagerConf`, `ClearVisualizationOnController`, `GetVisionmanagerConfig`, `GetDetectorConfig`, `GetImagesubscriberConfig`, `SaveVisionmanagerConfig`, `SaveDetectorConfig`, `SaveImagesubscriberConfig`
- Changed methods:
  - `GetLatestDetectedObject` does not take argument `returnpoints` anymore.
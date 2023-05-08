# Change log

## 0.14.0 (2023-05-08)

### Breaking changes

- `StartObjectDetectionTask`, `StartContainerDetectionTask` and `StartVisualizePointCloudTask` now only take `systemState` as an argument.

## 0.13.0 (2023-05-05)

### Breaking changes

- Remove unused functions: `VisualizePointCloudOnController`, `ClearVisualizationOnController`, `IsDetectionRunning`, `GetRunningState`, `SendVisionManagerConf`, `GetVisionmanagerConfig`, `GetDetectorConfig`, `GetImagesubscriberConfig`, `SaveVisionmanagerConfig`, `SaveDetectorConfig`, `SaveImagesubscriberConfig`, `GetStatusPort`, `GetConfigPort`
- Change methods:
  - `GetLatestDetectedObject` does not take argument `returnpoints` anymore.
  - `GetLatestDetectionResultImages` now takes the `blockwait` argument. When `blockwait` is `False`, `WaitForGetLatestDetectionResultImages` can be used instead.
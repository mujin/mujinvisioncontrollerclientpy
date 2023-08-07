# Changelog

## 0.14.0 (2023-05-08)

### Changes

- `StartObjectDetectionTask`, `StartContainerDetectionTask` and `StartVisualizePointCloudTask` changed API.

## 0.13.1

### Changes

- Use newerThanResultTimestampMS for GetLatestDetectionResultImages.

## 0.13.0 (2023-05-05)

### Changes

- Remove unused functions: `VisualizePointCloudOnController`, `ClearVisualizationOnController`, `IsDetectionRunning`, `GetRunningState`, `SendVisionManagerConf`, `GetVisionmanagerConfig`, `GetDetectorConfig`, `GetImagesubscriberConfig`, `SaveVisionmanagerConfig`, `SaveDetectorConfig`, `SaveImagesubscriberConfig`, `GetStatusPort`, `GetConfigPort`
- Change methods:
  - `GetLatestDetectedObject` does not take argument `returnpoints` anymore.
  - `GetLatestDetectionResultImages` now takes the `blockwait` argument. When `blockwait` is `False`, `WaitForGetLatestDetectionResultImages` can be used instead.
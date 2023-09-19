# Simple Heuristic Gesture Annotation

[Preview Video](https://i.imgur.com/Le4mvmY.mp4)

This script takes the the [world hand landmarks](https://google.github.io/mediapipe/solutions/hands.html#multi_hand_world_landmarks) generated by MediaPipe, compares the current frame's data to a known list of poses, and estimates the best fit.

![Hand Landmarks](https://mediapipe.dev/images/mobile/hand_landmarks.png)

For estimation, a "difference" value is estimated by comparing each unknown pose's keypoint distance to known pose keypoints, the lowest "difference" value wins.

There's a few caveats and room for improvement: the estimation algorithm will always check every pose and rank them via sorting by the lowest "difference" value, every frame. Distances seem to change based on where the hand is in the frame, but this can be alleviated by having multiple data points for a particular pose. Some poses may benefit from finer tuned estimation, such as ignoring directional tracking.

## Data Example
An example notebook showing how the hand tracking data is used and represented can be found [here](input_example.ipynb).

## Running

Install [PoseVis](https://github.com/Dasfaust/labgraph/blob/hand_tracking/devices/webcam/readme.md)

Check command line arguments:
```
python -m pose_vis.gesture.hand.gesture_vis --help
```

Run with:
```
python -m pose_vis.gesture.hand.gesture_vis --sources 0
```

Exporting videos:
```
python -m pose_vis.gesture.hand.gesture_vis --sources test_video.mp4 --resolutions *:1920x1080x30 --export test_video_annotated.mp4
```

You may specify a codec with:
```
python -m pose_vis.gesture.hand.gesture_vis ... --export-format h264
```
Codec codes can be found [here](https://learn.microsoft.com/en-us/windows/win32/medfound/video-fourccs).

## Adding Poses

When the script is running, press `Enter` to add poses: (note: this has only been tested on Windows, CV2 keycodes may differ between platforms.)

![Adding Poses](https://github.com/Dasfaust/labgraph/blob/hand_tracking/devices/webcam/pose_vis/gesture/hand/docs/images/adding_poses.png)

Enter a label for this pose and press `Enter` to continue, or `Escape` to exit. In this example, we're adding the label "OK".

![Collecting Data](https://github.com/Dasfaust/labgraph/blob/hand_tracking/devices/webcam/pose_vis/gesture/hand/docs/images/collecting_data.png)

Position your hand into the desired pose, and press `Spacebar` to collect a data point. Press `Escape` when finished, and test your pose.

[Result Preview](https://i.imgur.com/1VnVMlL.mp4)

Pose data, by default, is stored in `pose_vis/gesture/hand/data`, it consists of `labels.json` which are the label names, and a series of `.npy` files which is the recorded pose data that corresponds to each index in the labels array.
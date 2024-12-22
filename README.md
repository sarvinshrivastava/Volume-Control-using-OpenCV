# Volume Control using OpenCV

This project is a Python application that uses computer vision and hand tracking to control system volume. It utilizes `cv2` for video capture, `pycaw` for audio control, and threading for efficient volume management. The application adjusts volume based on the distance between specific hand landmarks.

## Installation

To install the required modules, run:
```sh
pip install -r requirements.txt
```

## Prerequisites

The following modules are required for this project:

- `python==3.8.10`
- `opencv-python==4.5.5.64`
- `mediapipe==0.10.11`
- `numpy==1.21.4`
- `comtypes==1.1.10`
- `pycaw==20181226`

## Usage

To run the main application, execute:
```sh
python volumeControl.py
```
To run the improved version of main application, execute:
```sh
python volumeControlusingThreading.py
```

## Credits

This project is inspired by Murtaza Hassan, founder of the YouTube channel "Murtaza's Workshop - Robotics and AI". His tutorials were of great help in the development of this project.

## Demo
Watch the demo of the project on YouTube:
```text
https://youtu.be/j1HaKpBAxYw
```
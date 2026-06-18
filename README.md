## **IMPORTANT!!!**  
In demo, the webcam is connected to wsl using usbipd-win, which mounts the camera to WSL  
Note: This method only works if your laptop webcam uses an internal USB bus. If it uses a MIPI bus, this method will not work.

## Introduction
This project is a real-time face detection and recognition application built with Python, utilizing the powerful face_recognition library and OpenCV. It captures video from a webcam (or IP camera), detects faces frame-by-frame, and draws bounding boxes around them.

## Features

Real-time processing: Optimized to process video streams efficiently (e.g., analyzing every 15th frame).

WSL2 Compatible: Includes specific optimizations and configurations for running OpenCV video captures within the Windows Subsystem for Linux (WSL2).

High Accuracy: Powered by dlib's state-of-the-art C++ machine learning models.


## Prerequisites
OS: Linux (Ubuntu/Debian) or WSL2 on Windows.

Python: Python 3.12 (Recommended).

Hardware: A working webcam or an IP Camera connected to the same network.

    sudo apt update  
    sudo apt install build-essential cmake python3.12-dev


## Installation
It is highly recommended to run this project inside an isolated Python Virtual Environment.

1.Create and activate a virtual environment:

    python3.12 -m venv venv  
    source venv/bin/activate

2.Upgrade basic build tools:

    pip install --upgrade pip setuptools wheel

3.Install dependencies (Using Tsinghua mirror for faster download in China):

    pip install dlib -i https://pypi.tuna.tsinghua.edu.cn/simple  
    pip install opencv-python face_recognition -i https://pypi.tuna.tsinghua.edu.cn/simple

4.⚠️ CRITICAL FIX for Python 3.12:

The face_recognition library relies on an older pkg_resources module to load its models, which was removed in recent versions of setuptools. You must downgrade setuptools to prevent the ModuleNotFoundError or fake missing model warnings:

    pip install "setuptools<70.0.0" -i https://pypi.tuna.tsinghua.edu.cn/simple


## Usage
Ensure your virtual environment is activated, then simply run the script:

    python face_recognizer.py
    (Press q in the video window to quit the application).


## Troubleshooting & Known Issues
1.incompatible function arguments (dlib Memory Error)
If you encounter a TypeError from compute_face_descriptor complaining about incompatible arguments, it is due to non-contiguous memory arrays when slicing BGR to RGB.
Fix: Always use OpenCV's native color conversion instead of Python array slicing:

    # DO NOT USE: rgb_frame = frame[:, :, ::-1]
    # USE THIS INSTEAD:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

2.WSL2 Webcam select() timeout or Black Screen
WSL2 has strict limitations on USB bandwidth for uncompressed video streams. If your camera times out or crashes OpenCV:
Fix: Force the camera to use the V4L2 backend and MJPG compression format in your code:

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

3.Cannot Access Webcam in WSL2
By default, WSL2 cannot access your Windows webcam. You have two options:

Option A (Recommended): Use an app like IP Webcam on your phone and change your code to read the network stream: cv2.VideoCapture("http://<YOUR_PHONE_IP>:8080/video")

Option B: Use the usbipd-win tool on Windows to pass your USB camera through to WSL2.

Developed with Python, OpenCV, and dlib.
# 🖐️ Real-Time AI Hand Gesture Interface

> **A computer vision-based Human-Computer Interaction (HCI) system that enables touchless control of Windows system audio using real-time hand tracking.**

---

## 📜 Project Overview

This project replaces traditional hardware peripherals with an AI-driven, touchless interface. By leveraging **Google's MediaPipe** framework and **OpenCV**, the application performs real-time detection of 21 distinct 3D hand landmarks.

The core logic utilizes a custom computer vision pipeline to map the **Euclidean distance** between the thumb and index finger directly to the **Windows Core Audio API** (via `pycaw` and `comtypes`). This results in a seamless, zero-latency volume control experience that operates efficiently on standard CPU architectures without the need for GPU acceleration.

## 🚀 Key Features

* **Sub-Millisecond Tracking:** utilizes a single-shot detector model to track hands at 30+ FPS.
* **Euclidean Distance Mapping:** Converts physical finger proximity (in pixels) to audio scalar values (0.0 to 1.0) using linear interpolation.
* **System-Level Integration:** Interfaces directly with Windows Audio Endpoints rather than simulating keyboard presses, ensuring smooth granular control.
* **Visual Feedback Loop:** Provides an Augmented Reality (AR) overlay on the webcam feed to visualize tracking status and volume levels.
* **Noise Stabilization:** Includes logic to dampen landmark jitter, preventing accidental volume jumps.

---

## 🛠️ Tech Stack & Architecture

This project was engineered using the following technologies:

| Component | Technology | Role in Architecture |
| :--- | :--- | :--- |
| **Language** | **Python 3.11** | Core logic and orchestration. |
| **Vision** | **OpenCV (cv2)** | Frame capture, colorspace conversion, and AR rendering. |
| **AI / ML** | **MediaPipe** | 21-point 3D hand landmark regression (Graph-based framework). |
| **Math** | **NumPy** | Vectorization and linear interpolation (`np.interp`) for range mapping. |
| **Audio API** | **Pycaw / Comtypes** | Low-level interface for Windows Core Audio Endpoint manipulation. |

---

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

* **Python 3.11.x** (Critical: Newer versions like 3.13 are not yet supported by MediaPipe).
* A working Webcam.
* Windows OS (Required for `pycaw` audio control).

---

## 📦 Installation Guide


1.  **Install Dependencies**
    To ensure compatibility, install the specific versions used in development:
    ```bash
    pip install opencv-python mediapipe==0.10.9 protobuf==3.20.3 comtypes==1.1.14 pycaw numpy
    ```

---

## 🎮 How to Use

1.  **Run the Application:**
    ```bash
    python VolumeControl.py
    ```

2.  **Initialize:**
    The webcam window will open. Wait for the system to detect your hand (landmarks will appear on your fingers).

3.  **Control Volume:**
    * **Volume UP:** Spread your **Thumb** and **Index Finger** apart.
    * **Volume DOWN:** Pinch your **Thumb** and **Index Finger** together.

4.  **Exit:**
    Press `q` to close the application.

---

## 🧠 How It Works (The Math)

The system follows a 4-step pipeline:

1.  **Detection:** The webcam frame is converted from BGR to RGB and passed to the MediaPipe Hands model.
2.  **Landmark Extraction:** The model returns coordinates $(x, y)$ for the **Thumb Tip (ID 4)** and **Index Finger Tip (ID 8)**.
3.  **Calculation:** We calculate the Euclidean distance ($D$) between these two points:
    $$D = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
4.  **Interpolation:** The distance $D$ (typically 30px to 300px) is linearly interpolated to the System Volume Range ($0.0$ to $1.0$):
    $$Vol = \text{np.interp}(D, [30, 150], [0.0, 1.0])$$

---

## 🚧 Troubleshooting

* **Error: "AttributeError: module 'mediapipe' has no attribute 'solutions'"**
    * *Fix:* You are likely using Python 3.13 or 3.14. Please uninstall and switch to **Python 3.11**.
* **Error: "AudioDevice has no attribute Activate"**
    * *Fix:* This is a `comtypes` version mismatch. Run: `pip install comtypes==1.1.14`.
* **Window closes immediately upon gesture:**
    * *Fix:* Check for a file named `pyautogui.py` in your folder and delete it to prevent namespace conflicts.

---

## 🔮 Future Improvements

* Implement "Smoothing" to reduce volume flicker.
* Add multi-hand support (Left hand for Brightness, Right hand for Volume).
* Create a GUI for sensitivity adjustment.

---

Author: Hasandeep Singh and Kritika

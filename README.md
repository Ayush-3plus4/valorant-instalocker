# VALORANT Tactical Instalocker ⚡

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-FF4655?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/Engine-OpenCV%20%2B%20MSS-00F0FF?style=for-the-badge)
![Developer](https://img.shields.io/badge/Developer-Ayush--3plus4-FF4655?style=for-the-badge&logo=github)

An ultra-fast, high-performance Valorant Agent Instalocker featuring a **Valorant Tactical HUD** GUI interface built with CustomTkinter, low-latency screen scanning (<10ms via `mss`), computer vision template matching (`opencv-python`), hardware DirectInput mouse automation (`pydirectinput`), and a multi-threaded responsive architecture.

Developed by **[Ayush-3plus4](https://github.com/Ayush-3plus4)**.

---

## 🎨 Visual Layout & Aesthetics

- **Dark Slate Palette:** Primary background `#0F1923` matched with `#1F2326` card containers.
- **Crimson Accents:** Signature Valorant `#FF4655` highlights on buttons, active borders, and scrollbars.
- **Tactical Status Card:** Live updating badge displaying `[IDLE]`, `[SEARCHING...]`, and `[LOCKED]`.
- **Card-Based Agent Grid:** Scrollable grid organizing agent target cards with smooth hover feedback.
- **Clickable Footer Attribution:** Direct link to the developer's GitHub profile (`https://github.com/Ayush-3plus4`).

---

## 🔥 Features & Architecture

- **MSS Screen Capture:** Fast low-overhead desktop frame capture.
- **OpenCV Pattern Recognition:** Support for template matching via `cv2.matchTemplate`.
- **PyDirectInput Automation:** Hardware-level direct mouse cursor simulation.
- **Global Hotkey Abort (F8):** Instant emergency cancel via background `keyboard` listener.
- **Configurable Coordinates:** JSON-driven screen coordinates for 1920x1080 resolution in `config.json`.

---

## 🛠️ Setup & Installation Instructions

### Prerequisites
- Python 3.9 or higher
- Display resolution set to **1920x1080**

### 1. Clone / Navigate to Directory
```bash
cd valorant-instalocker
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Application
```bash
python main.py
```

---

## 🏗️ Building Standalone Executable (.EXE)

Compile into a single executable file using `pyinstaller`:

```bash
pyinstaller --noconsole --onefile --name "ValorantInstalocker" main.py
```

The resulting binary will be located at `dist/ValorantInstalocker.exe`.

---

## 👤 Credits & Author

Created by **[Ayush-3plus4](https://github.com/Ayush-3plus4)**  
GitHub: [https://github.com/Ayush-3plus4](https://github.com/Ayush-3plus4)

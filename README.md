# VALORANT Tactical Instalocker ⚡

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-FF4655?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/Engine-OpenCV%20%2B%20MSS-00F0FF?style=for-the-badge)
![Developer](https://img.shields.io/badge/Developer-Ayush--3plus4-FF4655?style=for-the-badge&logo=github)

An ultra-fast, high-performance Valorant Agent Instalocker featuring a **Valorant Tactical HUD** GUI interface, low-latency screen scanning (<10ms via `mss`), hardware direct input automation, and multi-threaded responsive design.

Developed by **[Ayush-3plus4](https://github.com/Ayush-3plus4)**.

---

## 🔥 Key Features

- **Valorant Tactical HUD Theme:** Designed with Valorant's dark slate (`#0F1923`), crimson accent (`#FF4655`), off-white typography, and glowing status badges.
- **Ultra-Fast MSS Screen Capture:** Achieves ultra-low latency screen capture (<10ms) without frame drops.
- **DirectInput Mouse Simulation:** Low-level `ctypes` Windows API mouse automation to bypass game engine input suppression.
- **Multi-Threaded Architecture:** Keeps the GUI operating smoothly at 60 FPS while the detector scans asynchronously.
- **Global Emergency Abort (F8):** Instantly cancel active agent searching by pressing `F8`.
- **Configurable Coordinates:** Full flexibility via `config.json` for custom monitor resolutions and offsets.

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ayush-3plus4/valorant-instalocker.git
   cd valorant-instalocker
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application:**
   ```bash
   python main.py
   ```

---

## 🎮 How to Use

1. Launch **VALORANT** and ensure your display setting is **1920x1080 Borderless or Fullscreen**.
2. Run `ValorantInstalocker.exe` or `python main.py`.
3. Click your desired agent (e.g., **JETT**, **REYNA**, **RAZE**, **CHAMBER**, **ISO**).
4. Click **ACTIVATE LOCK-IN**.
5. Once match creation begins, the bot instantly selects and locks in your chosen agent.
6. Press **F8** at any time to abort the search.

---

## 🏗️ Building Executable (.EXE)

To compile the application into a standalone Windows executable:

```bash
pyinstaller --noconsole --onefile --name "ValorantInstalocker" main.py
```

The output file will be generated in `./dist/ValorantInstalocker.exe`.

---

## 👤 Developer & License

Developed with ❤️ by **[Ayush-3plus4](https://github.com/Ayush-3plus4)**.  
Open-source under the MIT License.

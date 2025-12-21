# 📂 Downloads Organizer

![Version](https://img.shields.io/github/v/release/YOUR_USERNAME/downloads-organizer?color=00ff88&label=Stable)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/Built%20With-Python-yellow?logo=python)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Stop the chaos.** A lightweight, open-source utility that automatically organizes your Windows Downloads folder in the background.

![App Screenshot](https://via.placeholder.com/800x400?text=Replace+This+With+A+Screenshot+Of+Your+App+Or+Website)

## ✨ Features

*   **⚡ Zero Latency:** Uses the Windows `Watchdog` API to detect file changes the millisecond they happen. No heavy scanning loops.
*   **🛡️ Defender Friendly:** Includes a built-in helper to add your Downloads folder to Windows Defender exclusions (prevents CPU spikes during moves).
*   **👻 Silent Operation:** Runs quietly in the System Tray. Right-click to access settings.
*   **🚀 Auto-Startup:** Option to launch automatically when Windows starts (Registry integrated).
*   **🎨 High-Res Icons:** optimized for Windows 10/11 Taskbar and System Tray.

## 📂 Supported File Types

The app automatically sorts files into these folders:

| Category | Extensions |
| :--- | :--- |
| **Installers** | `.exe`, `.msi`, `.bat`, `.apk`, `.jar` |
| **Images** | `.jpg`, `.png`, `.webp`, `.svg`, `.ico`, `.heic` |
| **Videos** | `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm` |
| **Documents** | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.ogg` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.iso` |
| **Code** | `.py`, `.js`, `.html`, `.css`, `.cpp`, `.json` |
| **Design** | `.psd`, `.ai`, `.fig`, `.sketch` |

*Files not listed above are moved to a `Miscellaneous` folder.*

---

## 📥 Installation

### Option 1: The Easy Way (Installer)
1.  Go to the **[Releases Page](../../releases)**.
2.  Download **`DownloadsOrganizer_Setup.exe`**.
3.  Run the installer.
    > **⚠️ Note:** Since this is an open-source indie tool, Windows Defender may flag it as "Unknown". Click **More Info** → **Run Anyway**.

### Option 2: Run from Source (For Developers)
If you prefer to run the raw Python code:

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/downloads-organizer.git
    cd downloads-organizer
    ```

2.  **Install dependencies:**
    ```bash
    pip install watchdog pystray pillow
    ```

3.  **Run the script:**
    ```bash
    python download_organizer.py
    ```

---

##  🤝 Contributing

1. **Contributions are welcome!**
2. **Fork the Project.**
3. **Create your Feature Branch (git checkout -b feature/AmazingFeature).**
4. **Commit your Changes (git commit -m 'Add some AmazingFeature').**
5. **Push to the Branch (git push origin feature/AmazingFeature).**
6. **Open a Pull Request.**



## 📄 License
Distributed under the MIT License. See LICENSE for more information.
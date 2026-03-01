# Downloads Organizer

Downloads Organizer is a lightweight utility that automatically sorts your downloaded files into categorized folders such as Installers, Images, Videos, and Documents. It operates silently in the background and ensures your Downloads folder remains clean and organized without manual effort.

## Overview

The project consists of two components:
1. Windows Desktop Application: Monitors the Downloads folder using the Windows Watchdog API and organizes files with zero latency.
2. Chromium Browser Extension: Intercepts downloads directly in the browser and routes them to the correct subfolder before they are saved to disk. This prevents "File Removed" errors in Chrome.

## Features

- Zero Latency: Files are detected and moved the millisecond they are fully written to disk.
- Defender Friendly: Includes a built-in helper to add your Downloads folder to Windows Defender exclusions to prevent CPU spikes.
- Silent Operation: Runs quietly in the System Tray with options for launching on Windows startup.
- Browser Integration: The companion extension works with Chrome, Edge, Brave, and Opera to organize files natively.

## Supported File Types

The application automatically sorts files into specific folders based on their extension:

- Installers: .exe, .msi, .bat, .apk, .jar
- Images: .jpg, .png, .webp, .svg, .ico, .heic
- Videos: .mp4, .mkv, .mov, .avi, .webm
- Documents: .pdf, .docx, .txt, .xlsx, .pptx
- Audio: .mp3, .wav, .flac, .ogg
- Archives: .zip, .rar, .7z, .tar, .iso
- Code: .py, .js, .html, .css, .cpp, .json
- Design: .psd, .ai, .fig, .sketch

Files not listed above are moved to a Miscellaneous folder.

## Installation

### Windows Application

1. Go to the Releases page.
2. Download the Downloads Organizer Setup executable.
3. Run the installer. (Note: standard Windows SmartScreen warnings may appear; click "More Info" and "Run Anyway").

### Browser Extension

1. Download the Downloads-Organizer-Extension.zip from the Releases page and extract it.
2. Open your chromium browser and navigate to the extensions page (e.g., chrome://extensions/).
3. Enable "Developer mode" in the top right corner.
4. Click "Load unpacked" and select the extracted extension folder.

## Running from Source

If you prefer to run the raw Python code:

1. Clone the repository
2. Install dependencies: pip install watchdog pystray pillow
3. Run the script: python download_organizer.py

## Developer

- [@Reyan Arshad](https://www.linkedin.com/in/reyan36/)


## License

Distributed under the MIT License. See `LICENSE` for more information.

## © 2026 Downloads Organizer All rights reserved

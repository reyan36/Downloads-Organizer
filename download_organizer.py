import os
import sys
import shutil
import time
import json
import subprocess
import ctypes
import winreg
from pathlib import Path
from tkinter import filedialog, Tk

# Third-party libraries
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# --- Configuration & Constants ---
APP_NAME = "Downloads Organizer"
VERSION = "v1.0.0"
CONFIG_FILE = "organizer_config.json"
ICON_NAME = "icon.ico"
ICON_PNG = "icon.png"

# --- 1. SINGLE INSTANCE CHECK ---
# This prevents the app from opening twice
kernel32 = ctypes.windll.kernel32
mutex = kernel32.CreateMutexW(None, False, "Global\\DownloadsOrganizer_Unique_Mutex_v1")
if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    sys.exit(0)

# --- 2. APP ID FIX (Taskbar Icon) ---
myappid = 'mycompany.downloadsorganizer.app.1.0.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

DEFAULT_DOWNLOADS = str(Path.home() / "Downloads")

# File Type Mappings
FILE_TYPES = {
    "Installers":   [".exe", ".msi", ".bat", ".cmd", ".sh", ".apk", ".bin", ".jar", ".vbs", ".deb", ".rpm"],
    "Archives":     [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".bz2", ".xz", ".tgz", ".sitx"],
    "Images":       [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".heic", ".raw"],
    "Videos":       [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".webm", ".m4v", ".mpeg", ".mpg", ".3gp"],
    "Audio":        [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff"],
    "Documents":    [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md", ".tex", ".wpd", ".wps"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".xlsm", ".tsv", ".numbers"],
    "Presentations":[".ppt", ".pptx", ".odp", ".pps", ".ppsx", ".key"],
    "Code":         [".py", ".js", ".html", ".css", ".cpp", ".java", ".json", ".sql", ".php", ".cs", ".go", ".rs", ".ts", ".xml", ".yaml", ".lua"],
    "Fonts":        [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Ebooks":       [".epub", ".mobi", ".azw3", ".cbz", ".cbr", ".pdf"],
    "Design":       [".psd", ".ai", ".eps", ".indd", ".sketch", ".fig", ".xcf", ".cdr"],
    "3D Models":    [".stl", ".obj", ".fbx", ".blend", ".3ds", ".dae", ".gcode", ".ply"],
    "Disk Images":  [".img", ".vcd", ".toast", ".dmg"],
    "Torrents":     [".torrent"],
}

IGNORE_EXTS = [".tmp", ".crdownload", ".part", ".ini", ".download", ".ut!"]
IGNORE_FILES = [CONFIG_FILE, os.path.basename(__file__), ICON_NAME, ICON_PNG, "desktop.ini"]

class ConfigManager:
    def __init__(self):
        self.config = {
            "target_folder": DEFAULT_DOWNLOADS,
            "run_on_startup": False,
            "defender_excluded": False
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config.update(json.load(f))
            except:
                pass

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

cfg = ConfigManager()

# --- Core Logic ---

def get_app_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(__file__)

def get_unique_filename(target_folder, filename):
    path_obj = Path(target_folder) / filename
    if not path_obj.exists():
        return path_obj
    
    stem = path_obj.stem
    suffix = path_obj.suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = Path(target_folder) / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def organize_file(file_path, manual_run=False):
    path_obj = Path(file_path)
    
    if not path_obj.exists() or not path_obj.is_file():
        return
    if path_obj.name in IGNORE_FILES:
        return
    if path_obj.name.startswith(".") or path_obj.suffix.lower() in IGNORE_EXTS:
        return

    # Time Check: Ignore files older than 2 mins unless manual
    if not manual_run:
        try:
            creation_time = os.path.getctime(file_path)
            if (time.time() - creation_time) > 120: 
                return
        except OSError:
            pass 

    extension = path_obj.suffix.lower()
    destination_folder = "Miscellaneous"
    
    for folder, exts in FILE_TYPES.items():
        if extension in exts:
            destination_folder = folder
            break
    
    target_base = Path(cfg.get("target_folder"))
    if path_obj.parent != target_base:
        return

    target_dir = target_base / destination_folder
    
    try:
        os.makedirs(target_dir, exist_ok=True)
        dest_path = get_unique_filename(target_dir, path_obj.name)
        time.sleep(0.5) 
        shutil.move(str(path_obj), str(dest_path))
    except Exception:
        pass

def run_organizer_now(icon, item):
    target = cfg.get("target_folder")
    if not os.path.exists(target):
        return
    for item_name in os.listdir(target):
        full_path = os.path.join(target, item_name)
        organize_file(full_path, manual_run=True)
    icon.notify("Organization complete.", "Success")

# --- Watchdog Handler ---
class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            organize_file(event.src_path, manual_run=False)

    def on_moved(self, event):
        if not event.is_directory:
            if os.path.basename(event.src_path) != os.path.basename(event.dest_path):
                organize_file(event.dest_path, manual_run=False)

# --- Windows Features ---

def toggle_startup(icon, item):
    # Toggle state
    current_state = cfg.get("run_on_startup")
    new_state = not current_state
    
    app_path = get_app_path()
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if new_state:
            # Add to registry
            if getattr(sys, 'frozen', False):
                cmd = f'"{app_path}"'
            else:
                cmd = f'"{sys.executable}" "{app_path}"'
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        else:
            # Remove from registry
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
        
        # Save new state so checkmark updates
        cfg.set("run_on_startup", new_state)
        
    except Exception as e:
        icon.notify(f"Registry Error: {e}", "Error")

def add_defender_exclusion(icon, item):
    # If already checked, do nothing
    if cfg.get("defender_excluded"): 
        return 
        
    path_to_exclude = cfg.get("target_folder")
    
    # --- 3. FIX: RUN POWERSHELL DIRECTLY (No App Restart) ---
    try:
        # This command asks PowerShell to run as Admin (Verb RunAs) and execute Add-MpPreference
        # It opens a UAC prompt for PowerShell, NOT the organizer app.
        ps_command = f"Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -Command Add-MpPreference -ExclusionPath \"{path_to_exclude}\"'"
        subprocess.run(["powershell", "-Command", ps_command], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Assume success if no crash, update config so checkmark appears
        cfg.set("defender_excluded", True)
        icon.notify("Exclusion request sent to Windows.", "Defender")
    except Exception as e:
        icon.notify(f"Failed: {e}", "Error")

def change_folder(icon, item):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory()
    root.destroy()
    
    if folder_selected:
        cfg.set("target_folder", folder_selected)
        restart_observer()

# --- 4. HIGH RES ICON GENERATOR ---
def load_icon():
    # Try loading local files first
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    for name in [ICON_PNG, ICON_NAME]:
        path = os.path.join(base_path, name)
        if os.path.exists(path):
            try:
                return Image.open(path)
            except:
                pass

    # GENERATE HIGH RES (256x256) GREEN ICON
    # This ensures no blurriness in System Tray or Taskbar
    size = 256
    image = Image.new('RGB', (size, size), color=(33, 33, 33))
    dc = ImageDraw.Draw(image)
    
    # Define Colors
    neon_green = (46, 204, 113)
    white = (255, 255, 255)
    
    # Draw Folder Shape (Scaled for 256px)
    # Tab
    dc.rectangle([40, 40, 120, 80], fill=neon_green)
    # Body
    dc.rectangle([40, 80, 216, 216], fill=neon_green)
    
    # Draw Arrow (Up/In)
    # Triangle
    dc.polygon([(128, 110), (168, 150), (88, 150)], fill=white)
    # Stem
    dc.rectangle([115, 150, 140, 180], fill=white)
    
    return image

observer = None

def start_observer():
    global observer
    path = cfg.get("target_folder")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

def stop_observer():
    global observer
    if observer:
        observer.stop()
        observer.join()

def restart_observer():
    stop_observer()
    start_observer()

def quit_app(icon, item):
    stop_observer()
    icon.stop()
    sys.exit(0)

def main():
    start_observer()
    
    # Define Menu with Dynamic Checkmarks
    # 'checked' parameter takes a callable that returns True/False
    menu = pystray.Menu(
        item(f'Version: {VERSION}', lambda i, It: None, enabled=False),
        pystray.Menu.SEPARATOR,
        item('Manage Existing Files', run_organizer_now),
        pystray.Menu.SEPARATOR,
        item(
            'Add to Defender Exclusion', 
            add_defender_exclusion,
            checked=lambda item: cfg.get("defender_excluded")
        ),
        item(
            'Start on Startup', 
            toggle_startup, 
            checked=lambda item: cfg.get("run_on_startup")
        ),
        item('Change Download Folder', change_folder),
        pystray.Menu.SEPARATOR,
        item('Exit', quit_app)
    )

    icon_img = load_icon()
    icon = pystray.Icon(APP_NAME, icon_img, f"{APP_NAME} ({VERSION})", menu)
    icon.run()

if __name__ == "__main__":
    main()
from __future__ import annotations

import os
import subprocess
import ctypes
import platform
import psutil
import pyautogui
import time
from pathlib import Path
from PIL import ImageGrab
from datetime import datetime


# ==================== SYSTEM CONTROL ====================

def lock_pc() -> None:
    """Lock the Windows PC."""
    if platform.system() == "Windows":
        ctypes.windll.user32.LockWorkStation()


def shutdown_pc(delay: int = 0) -> None:
    """Shutdown PC with optional delay (seconds)."""
    if platform.system() == "Windows":
        subprocess.run(f"shutdown /s /t {delay}", shell=True, check=False)


def restart_pc(delay: int = 0) -> None:
    """Restart PC with optional delay (seconds)."""
    if platform.system() == "Windows":
        subprocess.run(f"shutdown /r /t {delay}", shell=True, check=False)


def sleep_pc() -> None:
    """Put PC to sleep."""
    if platform.system() == "Windows":
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True, check=False)


def hibernate_pc() -> None:
    """Hibernate PC."""
    if platform.system() == "Windows":
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 1,1,1", shell=True, check=False)


def set_volume(level: int) -> None:
    """
    Set system volume level (0-100).
    Windows only - requires nircmd or similar tool.
    """
    level = max(0, min(100, level))
    if platform.system() == "Windows":
        try:
            subprocess.run(f"nircmd.exe setsysvolume {int(level * 655.36)}", shell=True, check=False)
        except Exception:
            print("nircmd not found. Install it for volume control.")


def set_brightness(level: int) -> None:
    """
    Set screen brightness (0-100).
    Windows only - requires nircmd or WMI.
    """
    level = max(0, min(100, level))
    if platform.system() == "Windows":
        try:
            subprocess.run(f"nircmd.exe setbrightness {int(level)}", shell=True, check=False)
        except Exception:
            print("nircmd not found. Install it for brightness control.")


def get_system_info() -> dict:
    """Get comprehensive system information."""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": psutil.virtual_memory().total / (1024**3),
            "available_gb": psutil.virtual_memory().available / (1024**3),
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total_gb": psutil.disk_usage("/").total / (1024**3),
            "used_gb": psutil.disk_usage("/").used / (1024**3),
            "free_gb": psutil.disk_usage("/").free / (1024**3),
            "percent": psutil.disk_usage("/").percent,
        },
        "timestamp": datetime.now().isoformat(),
    }


# ==================== MOUSE & KEYBOARD CONTROL ====================

def move_mouse(x: int, y: int, duration: float = 0.5) -> None:
    """Move mouse to coordinates (x, y) over duration seconds."""
    pyautogui.moveTo(x, y, duration=duration)


def click_mouse(x: int, y: int, button: str = "left", clicks: int = 1, interval: float = 0.1) -> None:
    """Click mouse at coordinates (x, y)."""
    pyautogui.click(x, y, button=button, clicks=clicks, interval=interval)


def double_click(x: int, y: int, interval: float = 0.1) -> None:
    """Double click at coordinates (x, y)."""
    pyautogui.click(x, y, clicks=2, interval=interval)


def right_click(x: int, y: int) -> None:
    """Right click at coordinates (x, y)."""
    pyautogui.click(x, y, button="right")


def drag_mouse(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> None:
    """Drag mouse from start to end coordinates."""
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.mouseUp()


def scroll_mouse(x: int, y: int, clicks: int = 3) -> None:
    """Scroll at coordinates (x, y)."""
    pyautogui.moveTo(x, y)
    pyautogui.scroll(clicks)


def type_text(text: str, interval: float = 0.05) -> None:
    """Type text with interval between characters."""
    pyautogui.typewrite(text, interval=interval)


def type_text_unicode(text: str, interval: float = 0.05) -> None:
    """Type text with Unicode support (special characters)."""
    pyautogui.write(text, interval=interval)


def press_key(key: str) -> None:
    """Press a single key (e.g., 'enter', 'esc', 'tab')."""
    pyautogui.press(key)


def press_hotkey(key1: str, key2: str, key3: str | None = None) -> None:
    """Press hotkey combination (e.g., 'ctrl', 'a' for Ctrl+A)."""
    if key3:
        pyautogui.hotkey(key1, key2, key3)
    else:
        pyautogui.hotkey(key1, key2)


def hold_key(key: str, duration: float = 1.0) -> None:
    """Hold a key for specified duration."""
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


# ==================== FILE MANAGEMENT ====================

def create_file(file_path: str, content: str = "") -> dict:
    """Create a new file with optional content."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "message": f"File created: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_file(file_path: str) -> dict:
    """Delete a file."""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return {"success": True, "message": f"File deleted: {file_path}"}
        return {"success": False, "error": "File not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def move_file(source: str, destination: str) -> dict:
    """Move/rename a file."""
    try:
        Path(source).rename(destination)
        return {"success": True, "message": f"File moved from {source} to {destination}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def copy_file(source: str, destination: str) -> dict:
    """Copy a file."""
    try:
        import shutil
        shutil.copy2(source, destination)
        return {"success": True, "message": f"File copied to {destination}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_folder(folder_path: str) -> dict:
    """Create a folder."""
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        return {"success": True, "message": f"Folder created: {folder_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_folder(folder_path: str) -> dict:
    """Delete a folder."""
    try:
        import shutil
        shutil.rmtree(folder_path)
        return {"success": True, "message": f"Folder deleted: {folder_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_files(folder_path: str) -> dict:
    """List files in a folder."""
    try:
        path = Path(folder_path)
        files = []
        folders = []
        for item in path.iterdir():
            if item.is_file():
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "size_bytes": item.stat().st_size,
                    "type": "file"
                })
            elif item.is_dir():
                folders.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "folder"
                })
        return {"success": True, "files": files, "folders": folders}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_file(file_path: str) -> dict:
    """Open a file with default application."""
    try:
        os.startfile(file_path) if platform.system() == "Windows" else subprocess.run(["open", file_path])
        return {"success": True, "message": f"Opening file: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_folder(folder_path: str) -> dict:
    """Open a folder in explorer."""
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        else:
            subprocess.run(["open", folder_path])
        return {"success": True, "message": f"Opening folder: {folder_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== PROCESS MANAGEMENT ====================

def list_processes() -> dict:
    """List all running processes."""
    try:
        processes = []
        for proc in psutil.process_iter(["pid", "name", "status", "memory_percent", "cpu_percent"]):
            try:
                pinfo = proc.as_dict(attrs=["pid", "name", "status", "memory_percent", "cpu_percent"])
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return {"success": True, "processes": processes}
    except Exception as e:
        return {"success": False, "error": str(e)}


def start_process(command: str) -> dict:
    """Start a new process."""
    try:
        subprocess.Popen(command, shell=True)
        return {"success": True, "message": f"Process started: {command}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def stop_process(process_name: str) -> dict:
    """Stop a process by name."""
    try:
        found = False
        for proc in psutil.process_iter(["name"]):
            if process_name.lower() in proc.info["name"].lower():
                proc.terminate()
                found = True
        if found:
            return {"success": True, "message": f"Process stopped: {process_name}"}
        return {"success": False, "error": "Process not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def kill_process_by_pid(pid: int) -> dict:
    """Kill a process by PID."""
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return {"success": True, "message": f"Process killed: PID {pid}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_application(app_path: str) -> dict:
    """Open an application."""
    try:
        if platform.system() == "Windows":
            os.startfile(app_path)
        else:
            subprocess.Popen(app_path)
        return {"success": True, "message": f"Application opened: {app_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def open_chrome() -> dict:
    """Open Chrome browser."""
    try:
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        ]
        for path in chrome_paths:
            if Path(path).exists():
                os.startfile(path)
                return {"success": True, "message": "Chrome opened"}
        return {"success": False, "error": "Chrome not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== SCREEN CONTROL ====================

def take_screenshot(save_path: str | None = None) -> dict:
    """Take a screenshot and save it."""
    try:
        if not save_path:
            save_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        return {"success": True, "path": save_path, "message": f"Screenshot saved: {save_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_screen_resolution() -> dict:
    """Get screen resolution."""
    try:
        width, height = pyautogui.size()
        return {"success": True, "width": width, "height": height}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_to_whatsapp(file_path: str) -> dict:
    """Send a file to WhatsApp Web."""
    try:
        if not Path(file_path).exists():
            return {"success": False, "error": "File not found"}
        
        # Open WhatsApp Web
        os.startfile("https://web.whatsapp.com") if platform.system() == "Windows" else subprocess.run(["open", "https://web.whatsapp.com"])
        
        time.sleep(5)  # Wait for WhatsApp to load
        
        # Simulate Ctrl+Shift+U to open attach file dialog
        pyautogui.hotkey("ctrl", "shift", "u")
        time.sleep(2)
        
        # Type file path and press Enter
        pyautogui.typewrite(file_path, interval=0.01)
        time.sleep(1)
        pyautogui.press("enter")
        
        return {"success": True, "message": f"File prepared to send via WhatsApp: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("PC Control Module Loaded")
    print("System Info:", get_system_info())

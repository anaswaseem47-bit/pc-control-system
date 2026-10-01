from __future__ import annotations

import json
from typing import Optional

from browser_control import (
    open_browser,
    open_whatsapp,
    search_web,
    parse_and_send_whatsapp,
)
from browser_monitor import get_recent_chrome_history
from learning import UsageLearner
from network_monitor import get_network_summary, monitor_internet_usage
from pc_control import (
    click_mouse,
    create_file,
    create_folder,
    delete_file,
    delete_folder,
    double_click,
    get_screen_resolution,
    get_system_info,
    hibernate_pc,
    list_files,
    list_processes,
    lock_pc,
    move_mouse,
    open_application,
    open_chrome,
    open_file,
    open_folder,
    press_hotkey,
    press_key,
    restart_pc,
    send_to_whatsapp,
    set_brightness,
    set_volume,
    shutdown_pc,
    sleep_pc,
    start_process,
    stop_process,
    take_screenshot,
    type_text,
)
from voice_control import VoiceAssistant


HELP_TEXT = """
PC Control Assistant

System:
  lock pc
  shutdown pc
  restart pc
  sleep pc
  hibernate pc
  system info
  volume 50
  brightness 50

Mouse and keyboard:
  move mouse 500 300
  click mouse 100 200
  double click 200 200
  press key enter
  hotkey ctrl c
  type hello world

Browser:
  open chrome
  open whatsapp
  open whatsapp in chrome
  open google
  open youtube
  search web for python tutorials
  search for python tutorials
  open website github.com
  find Ahmed and send hello
  send hello to Ahmed
  message Ahmed hello

App and file control:
  open file C:/path/to/file.txt
  open folder C:/path/to/folder
  list files C:/path/to/folder
  create file C:/path/to/file.txt
  delete file C:/path/to/file.txt
  create folder C:/path/to/folder
  delete folder C:/path/to/folder
  send file C:/path/to/file.pdf to whatsapp

Process and screen:
  list processes
  start process notepad
  stop process chrome
  take screenshot
  screen resolution

Monitoring:
  show usage
  internet usage
  chrome history
  learn my pattern

General:
  help
  exit
"""


def print_usage_summary(learner: UsageLearner) -> None:
    history = get_recent_chrome_history(limit=5)
    network = get_network_summary()
    summary = learner.generate_summary()

    print("\n=== Recent Chrome activity ===")
    if not history:
        print("No Chrome history found.")
    else:
        for item in history:
            print(f"- {item['title']} | {item['domain']} | {item['visited_at']}")

    print("\n=== Network usage ===")
    print(f"Sent: {network['bytes_sent_human']}")
    print(f"Received: {network['bytes_received_human']}")

    print("\n=== Learned pattern ===")
    if not summary["top_commands"]:
        print("No pattern yet. Use the assistant to train it.")
    else:
        print(f"Top commands: {', '.join(summary['top_commands'])}")
        print(f"Top sites: {', '.join(summary['top_sites'])}")


def extract_path_from_command(command: str, keyword: str) -> Optional[str]:
    if keyword not in command:
        return None
    remainder = command.split(keyword, 1)[1].strip()
    return remainder if remainder else None


def handle_command(command: str, learner: UsageLearner, voice: Optional[VoiceAssistant] = None) -> bool:
    text = command.strip().lower()
    if not text:
        return True

    learner.record_command(text)

    if text in {"exit", "quit", "close", "bye"}:
        if voice:
            voice.speak("Goodbye.")
        print("Exiting assistant.")
        return False

    if text in {"help", "?", "commands"}:
        print(HELP_TEXT)
        return True

    if "lock pc" in text:
        lock_pc()
        print("Locked the PC.")
        return True

    if "shutdown pc" in text:
        shutdown_pc(0)
        print("Shutdown command sent.")
        return True

    if "restart pc" in text:
        restart_pc(0)
        print("Restart command sent.")
        return True

    if "sleep pc" in text:
        sleep_pc()
        print("Sleep command sent.")
        return True

    if "hibernate pc" in text:
        hibernate_pc()
        print("Hibernate command sent.")
        return True

    if "system info" in text:
        print(json.dumps(get_system_info(), indent=2))
        return True

    if text.startswith("volume "):
        try:
            value = int(text.replace("volume ", "").strip())
            set_volume(value)
            print(f"Volume set to {value}.")
        except ValueError:
            print("Volume requires a number between 0 and 100.")
        return True

    if text.startswith("brightness "):
        try:
            value = int(text.replace("brightness ", "").strip())
            set_brightness(value)
            print(f"Brightness set to {value}.")
        except ValueError:
            print("Brightness requires a number between 0 and 100.")
        return True

    if "move mouse" in text:
        parts = text.replace("move mouse", "").strip().split()
        if len(parts) >= 2:
            x, y = int(parts[0]), int(parts[1])
            move_mouse(x, y)
            print(f"Moved mouse to ({x}, {y}).")
        else:
            print("Usage: move mouse X Y")
        return True

    if "click mouse" in text:
        parts = text.replace("click mouse", "").strip().split()
        if len(parts) >= 2:
            x, y = int(parts[0]), int(parts[1])
            click_mouse(x, y)
            print(f"Clicked mouse at ({x}, {y}).")
        return True

    if "double click" in text:
        parts = text.replace("double click", "").strip().split()
        if len(parts) >= 2:
            x, y = int(parts[0]), int(parts[1])
            double_click(x, y)
            print(f"Double clicked at ({x}, {y}).")
        return True

    if "press key" in text:
        key_name = text.replace("press key", "").strip()
        if key_name:
            press_key(key_name)
            print(f"Pressed key: {key_name}")
        return True

    if "hotkey" in text:
        keys = text.replace("hotkey", "").strip().split()
        if len(keys) >= 2:
            if len(keys) == 2:
                press_hotkey(keys[0], keys[1])
            else:
                press_hotkey(keys[0], keys[1], keys[2])
            print(f"Pressed hotkey: {' '.join(keys)}")
        return True

    if text.startswith("type "):
        typed = text.replace("type ", "", 1)
        type_text(typed)
        print(f"Typed: {typed}")
        return True

    whatsapp_words = (
        "find ",
        "send ",
        "message ",
    )

    if text.startswith(whatsapp_words):
        result = parse_and_send_whatsapp(command.strip())
        print(result)
        return True

    if "open whatsapp" in text or "whatsapp in chrome" in text or "open whatsapp web" in text:
        result = open_whatsapp()
        print(result)
        return True

    if "open google" in text:
        result = open_browser("https://www.google.com")
        print(result)
        return True

    if "open youtube" in text:
        result = open_browser("https://www.youtube.com")
        print(result)
        return True

    if text.startswith("search web for "):
        query = text.replace("search web for ", "", 1).strip()
        result = search_web(query)
        print(result)
        return True

    if text.startswith("search for "):
        query = text.replace("search for ", "", 1).strip()
        result = search_web(query)
        print(result)
        return True

    if text.startswith("open website "):
        url = text.replace("open website ", "", 1).strip()
        result = open_browser(url)
        print(result)
        return True

    if "open chrome" in text:
        open_chrome()
        print("Opened Chrome.")
        return True

    for app_name in ["notepad", "calculator", "paint", "task manager", "settings"]:
        if f"open {app_name}" in text:
            open_application(app_name)
            print(f"Opened {app_name}.")
            return True

    if "open file" in text:
        path = extract_path_from_command(text, "open file")
        if path:
            open_file(path)
            print(f"Opening file: {path}")
        else:
            print("Usage: open file C:/path/to/file.txt")
        return True

    if "open folder" in text:
        path = extract_path_from_command(text, "open folder")
        if path:
            open_folder(path)
            print(f"Opening folder: {path}")
        else:
            print("Usage: open folder C:/path/to/folder")
        return True

    if "list files" in text:
        path = extract_path_from_command(text, "list files")
        if path:
            result = list_files(path)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: list files C:/path/to/folder")
        return True

    if "create file" in text:
        path = extract_path_from_command(text, "create file")
        if path:
            result = create_file(path, "")
            print(json.dumps(result, indent=2))
        else:
            print("Usage: create file C:/path/to/file.txt")
        return True

    if "delete file" in text:
        path = extract_path_from_command(text, "delete file")
        if path:
            result = delete_file(path)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: delete file C:/path/to/file.txt")
        return True

    if "create folder" in text:
        path = extract_path_from_command(text, "create folder")
        if path:
            result = create_folder(path)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: create folder C:/path/to/folder")
        return True

    if "delete folder" in text:
        path = extract_path_from_command(text, "delete folder")
        if path:
            result = delete_folder(path)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: delete folder C:/path/to/folder")
        return True

    if "send file" in text and "whatsapp" in text:
        path = extract_path_from_command(text, "send file")
        if path:
            result = send_to_whatsapp(path)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: send file C:/path/to/file.pdf to whatsapp")
        return True

    if "list processes" in text:
        print(json.dumps(list_processes(), indent=2))
        return True

    if "start process" in text:
        proc = text.replace("start process", "").strip()
        if proc:
            print(json.dumps(start_process(proc), indent=2))
        else:
            print("Usage: start process notepad")
        return True

    if "stop process" in text:
        proc = text.replace("stop process", "").strip()
        if proc:
            print(json.dumps(stop_process(proc), indent=2))
        else:
            print("Usage: stop process chrome")
        return True

    if "take screenshot" in text:
        result = take_screenshot()
        print(json.dumps(result, indent=2))
        return True

    if "screen resolution" in text:
        print(json.dumps(get_screen_resolution(), indent=2))
        return True

    if "show usage" in text:
        print_usage_summary(learner)
        return True

    if "internet usage" in text:
        print(json.dumps(monitor_internet_usage(duration=3, interval=1), indent=2))
        return True

    if "chrome history" in text:
        print(json.dumps(get_recent_chrome_history(limit=10), indent=2))
        return True

    if "learn my pattern" in text:
        print(json.dumps(learner.generate_summary(), indent=2))
        return True

    print("Command not recognized. Type 'help' for available commands.")
    return True


def main() -> None:
    learner = UsageLearner("usage_data.json")

    voice = None
    try:
        voice = VoiceAssistant()
        print("Voice assistant ready.")
    except Exception as exc:
        print(f"Voice assistant unavailable: {exc}")

    print(HELP_TEXT)

    while True:
        try:
            user_input = input("\nCommand> ").strip()
            if not user_input:
                if voice:
                    try:
                        heard = voice.listen_for_command()
                        if heard:
                            print(f"Heard: {heard}")
                            user_input = heard
                        else:
                            continue
                    except Exception:
                        continue
                else:
                    continue

            should_continue = handle_command(user_input, learner, voice)
            if not should_continue:
                break
        except KeyboardInterrupt:
            print("\nAssistant stopped.")
            break
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


_driver = None


def get_driver():
    global _driver

    if _driver is not None:
        try:
            _driver.current_url  # Test if driver is still alive
            return _driver
        except Exception:
            _driver = None  # Reset if dead

    options = Options()

    profile_dir = Path.home() / "whatsapp_selenium_profile"
    options.add_argument(f"--user-data-dir={profile_dir}")

    options.add_argument("--start-maximized")

    _driver = webdriver.Chrome(options=options)
    return _driver


def open_browser(url: str = "https://www.google.com") -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    driver = get_driver()
    driver.get(url)
    return {"success": True, "url": url}


def open_whatsapp() -> dict:
    driver = get_driver()
    driver.get("https://web.whatsapp.com")

    return {
        "success": True,
        "message": (
            "WhatsApp Web opened. If this is the first run, scan the QR code once. "
            "The login will be saved for later runs."
        ),
    }


def search_web(query: str) -> dict:
    if not query.strip():
        return {"success": False, "error": "Search query is empty"}

    url = "https://www.google.com/search?q=" + quote(query.strip())
    return open_browser(url)


def _wait_for_whatsapp(driver, timeout: int = 60) -> None:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"]')
        )
    )


def _find_contact(driver, contact_name: str) -> None:
    wait = WebDriverWait(driver, 30)

    search_box = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//div[@contenteditable="true"]'
                '[@data-tab="3" or @data-tab="2"]',
            )
        )
    )

    search_box.click()
    search_box.send_keys(Keys.CONTROL, "a")
    search_box.send_keys(contact_name)
    time.sleep(2)

    result = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f'//span[@title="{contact_name}"]',
            )
        )
    )

    result.click()


def send_whatsapp_to_contact(contact_name: str, message: str) -> dict:
    contact_name = contact_name.strip()
    message = message.strip()

    if not contact_name:
        return {"success": False, "error": "Contact name is empty"}

    if not message:
        return {"success": False, "error": "Message is empty"}

    driver = get_driver()
    driver.get("https://web.whatsapp.com")

    try:
        _wait_for_whatsapp(driver, timeout=60)
        _find_contact(driver, contact_name)

        wait = WebDriverWait(driver, 30)

        message_box = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//footer//div[@contenteditable="true"]',
                )
            )
        )

        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        return {
            "success": True,
            "contact": contact_name,
            "message": message,
        }

    except TimeoutException:
        return {
            "success": False,
            "error": (
                "WhatsApp was not ready. Open WhatsApp Web and scan the QR code "
                "if required."
            ),
        }

    except NoSuchElementException:
        return {
            "success": False,
            "error": f"Could not find the WhatsApp contact: {contact_name}",
        }

    except Exception as exc:
        return {"success": False, "error": str(exc)}


def parse_and_send_whatsapp(command: str) -> dict:
    command = command.strip()

    patterns = [
        r"^find\s+(.+?)\s+and\s+send\s+(.+)$",
        r"^send\s+(.+?)\s+to\s+(.+)$",
        r"^message\s+(.+?)\s+(.+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, command, flags=re.IGNORECASE)

        if match:
            first = match.group(1).strip()
            second = match.group(2).strip()

            if pattern.startswith("^send"):
                message = first
                contact = second
            else:
                contact = first
                message = second

            return send_whatsapp_to_contact(contact, message)

    return {
        "success": False,
        "error": (
            "Use: find Ahmed and send Hello, "
            "send Hello to Ahmed, or message Ahmed Hello"
        ),
    }

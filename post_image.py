import cv2
import requests
import time

camera = cv2.VideoCapture(1)
if not camera.isOpened():
    raise RuntimeError('Could not start camera.')

URL = 'http://localhost:5000/live/upload'

while True:
    try:
        is_camera_online, image = camera.read()
        if is_camera_online:
            cv2.imwrite('live.jpg', image)
            files = {'file': open('live.jpg', 'rb')}
            requests.post(URL, files=files)
        time.sleep(0.024)
    except Exception as err:
        print str(err)

import handTrackingModule as hmt
import time
import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1080, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = hmt.handDetector(detectionCon=0.85)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

pTime = 0
cTime = 0

maxDis, minDis = 315, 20
vol = volume.GetVolumeRange()
volPer = np.interp(volume.GetMasterVolumeLevel(), [vol[0], vol[1]], [0, 100])

zmin, zmax = 266.5, 636.5

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    handLM = detector.findPosition(img)
    if len(handLM) != 0:
        # print(handLM[4], handLM[8])

        x1, y1 = handLM[4][1], handLM[4][2]
        x2, y2 = handLM[8][1], handLM[8][2]

        cv2.circle(img, (x1, y1), 7, (0, 255, 0), 5)
        cv2.circle(img, (x2, y2), 7, (0, 255, 0), 5)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if length < minDis:
            setVolume = vol[0]
        else:
            z = (handLM[4][2] + handLM[8][2]) / 2
            distance = np.interp(z, [zmin, zmax], [1, 5.5])
            setVolume = np.interp(length * distance, [minDis, maxDis], [vol[0], vol[1]])

        volPer = np.interp(setVolume, [vol[0], vol[1]], [0, 100])
        volume.SetMasterVolumeLevel(setVolume, None)


        # print(length, setVolume)


    else:
        print("No Detection")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    txt = "FPS: " + str(int(fps))

    cv2.putText(img, str(txt), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (13, 149, 245), 3)
    cv2.putText(img, str(str(int(volPer)) + '%'), (20, 600), cv2.FONT_HERSHEY_DUPLEX, 1, (13, 149, 245), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
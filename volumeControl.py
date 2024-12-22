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

maxDis, minDis = 316, 23
vol = volume.GetVolumeRange()
volPer = np.interp(volume.GetMasterVolumeLevel(), [vol[0], vol[1]], [0, 100])

zmin, zmax = 266.5, 636.5

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    handLM = detector.findPosition(img)
    if len(handLM) != 0:
        x1, y1, z1 = handLM[4][1], handLM[4][2], handLM[4][3]
        x2, y2, z2 = handLM[8][1], handLM[8][2], handLM[8][3]

        cv2.circle(img, (x1, y1), 7, (0, 255, 0), 5)
        cv2.circle(img, (x2, y2), 7, (0, 255, 0), 5)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        avgZ = (z1 + z2) / 2

        dynamicMinDis = np.interp(avgZ, [zmin, zmax], [minDis, maxDis])

        if length < dynamicMinDis:
            setVolume = vol[0]
        else:
            distance = np.interp(avgZ, [zmin, zmax], [1, 5.5])
            setVolume = np.interp(length * distance, [dynamicMinDis, maxDis], [vol[0], vol[1]])

        volPer = np.interp(setVolume, [vol[0], vol[1]], [0, 100])
        volume.SetMasterVolumeLevel(setVolume, None)

        print(length, setVolume, avgZ)

    else:
        print("No Detection")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    txt = "FPS: " + str(int(fps))

    cv2.putText(img, str(txt), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (137, 54, 177), 3)
    cv2.putText(img, str(str(int(volPer)) + '%'), (42, 650), cv2.FONT_HERSHEY_DUPLEX, 1, (137, 64, 177), 3)
    cv2.rectangle(img, (50, 150), (85, 600), (137, 64, 177), 3)
    cv2.rectangle(img, (52, int(np.interp(volPer, [0, 100], [600, 150]))), (83, 600), (13, 149, 245), cv2.FILLED)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
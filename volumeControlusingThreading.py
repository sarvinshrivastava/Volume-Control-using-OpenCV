import handTrackingModule as hmt
import time
import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading

wCam, hCam = 1080, 720


class VolumeControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.detector = hmt.handDetector(detectionCon=0.85)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

        self.maxDis, self.minDis = 315, 20
        self.vol = self.volume.GetVolumeRange()
        self.volPer = np.interp(self.volume.GetMasterVolumeLevel(), [self.vol[0], self.vol[1]], [0, 100])

        self.zmin, self.zmax = 266.5, 636.5

        self.pTime = 0
        self.cTime = 0

        self.running = True

    def volume_control(self):
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue

            img = self.detector.findHands(img, draw=False)
            handLM = self.detector.findPosition(img)
            if len(handLM) != 0:
                x1, y1 = handLM[4][1], handLM[4][2]
                x2, y2 = handLM[8][1], handLM[8][2]

                cv2.circle(img, (x1, y1), 7, (0, 255, 0), 5)
                cv2.circle(img, (x2, y2), 7, (0, 255, 0), 5)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if length < self.minDis:
                    setVolume = self.vol[0]
                else:
                    z = (handLM[4][2] + handLM[8][2]) / 2
                    distance = np.interp(z, [self.zmin, self.zmax], [1, 5.5])
                    setVolume = np.interp(length * distance, [self.minDis, self.maxDis], [self.vol[0], self.vol[1]])

                self.volPer = np.interp(setVolume, [self.vol[0], self.vol[1]], [0, 100])
                self.volume.SetMasterVolumeLevel(setVolume, None)
            else:
                print("No Detection")

            self.cTime = time.time()
            fps = 1 / (self.cTime - self.pTime)
            self.pTime = self.cTime
            txt = "FPS: " + str(int(fps))

            cv2.putText(img, str(txt), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (13, 149, 245), 3)
            cv2.putText(img, str(str(int(self.volPer)) + '%'), (20, 600), cv2.FONT_HERSHEY_DUPLEX, 1, (13, 149, 245), 3)
            cv2.imshow('Image', img)
            cv2.waitKey(1)

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    volume_control = VolumeControl()
    thread = threading.Thread(target=volume_control.volume_control)
    thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        volume_control.stop()
        thread.join()


if __name__ == "__main__":
    main()
import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplx=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplx = modelComplx

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.modelComplx, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=False):
        handLM = []

        if self.results.multi_hand_landmarks:
            currHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(currHand.landmark):
                h, w, c = img.shape
                # print(tuple([id, int(lm.x * w), int(lm.y * h)]))
                handLM.append(tuple([id, int(lm.x * w), int(lm.y * h), int(lm.z)]))
                # if id == handId and draw:
                #     cv2.circle(img, (int(cx), int(cy)), 10, (0, 255, 255), cv2.FILLED)

        return handLM


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        handLM = detector.findPosition(img)
        if len(handLM) != 0:
            print(handLM[4])
        else:
            print("No Detection")

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        txt = "FPS: " + str(int(fps))

        cv2.putText(img, str(txt), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

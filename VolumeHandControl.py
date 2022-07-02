import cv2
import time
import numpy as np
# importing our self based Hand tracking module
import HandTrackingModule as htm
import math

wCam, hCam = 1170, 430

cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()

    img = detector.findHands(img)

    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:

        area = (bbox[2] - bbox[0])*(bbox[3] - bbox[1])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 12, (88, 2, 194), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (88, 2, 194), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (102, 55, 96), 2)

        cx, cy = (x1 + x2)//2, (y1+y2)//2

        length = math.hypot(x1-x2, y1-y2)
        print(area)
        cmpLen = 190
        cmpArea = 140000

        length = (210*area)/cmpArea
        print(length)

        if length < 140:
            cv2.circle(img, (cx, cy), 12, (16, 16, 18), cv2.FILLED)
            cv2.putText(img, "Muted", (10, 500), cv2.FONT_HERSHEY_PLAIN, 1.5, (18, 216, 250), 2)


        litUp = lmList[20][2]
        litdown = lmList[19][2]

        if(litUp < litdown):
            vol = np.interp(length, [140, 210], [minVol, maxVol])
            per = max(0, int(((vol + 35)/35)*100))
            text = 'Volume : ' + str(per) + '%'
            volume.SetMasterVolumeLevel(vol, None)
            cv2.putText(img, text, (10, 80), cv2.FONT_HERSHEY_PLAIN, 1.5, (233, 245, 7), 2)

    cv2.putText(img, "WELCOME CHAMP !!", (345,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 229, 245), 2)
    cv2.putText(img, "For best experience stay 1.5 feets away", (185,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 29, 245), 2)


    cv2.imshow("Img", img)
    cv2.waitKey(1)


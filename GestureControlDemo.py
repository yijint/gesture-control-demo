# example based on https://youtube.com/watch?v=9iEPzbG-xLE&si=EnSIkaIECMiOmarE
import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
# https://github.com/AndreMiras/pycaw
import screen_brightness_control as sbc
# https://github.com/Crozzers/screen_brightness_control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###
widthCam, heightCam = 1280, 960

###

cap = cv2.VideoCapture(0)
# 3, and 4 are default id numbers for width and height of capture
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0

# default params: self, mode=False, maxHands=2, modelComplexity = 1, detectionCon=0.5, trackCon=0.5
detector = htm.handDetector(detectionCon=0.75)

### Dummy Code (volume)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# returns (min, max, ###)
volRange = volume.GetVolumeRange()
# changes laptop volume
# volume.SetMasterVolumeLevel(-5.0, None)
minVol = volRange[0]
maxVol = volRange[1]
# setVol = volume.GetMasterVolumeLevel()
# volBar = 400
###

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    # already drawing, so can set draw=False to reduce double draw
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # https://google.github.io/mediapipe/solutions/hands.html
        # tip of fingers ~ 4,8,12,16,20 (thumb to pinky)
        # print(lmList[4], lmList[8])
        # lmList is formatted (landmark#,xPos,yPos)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # midpoint of 2 fingers
        cX, cY = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
        cv2.circle(img, (cX, cY), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        # print(length)
        # distance range 50-300 (for ex.) 300-50 = 250 steps
        minLen = 50
        maxLen = 300
        # # scale vol from -65.25 to 0...
        # INCREMENT = ((length-minLen)/(maxLen-minLen))
        # setVol = minVol + INCREMENT*(maxVol-minVol)
        # print(setVol)
        # if maxVol > setVol > minVol:
        #     volume.SetMasterVolumeLevel(setVol, None)

        # cleaner numpy solution
        if dy > dx:
            # Check necessary? ===V
            volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel(), None)
            setVol = np.interp(length, [minLen, maxLen], [minVol, maxVol])
            # volBar = np.interp(length, [50, 300], [400, 150])
            volume.SetMasterVolumeLevel(setVol, None)
            if length < 50:
                cv2.circle(img, (cX, cY), 15, (255, 255, 0), cv2.FILLED)
        else:
            setBright = np.interp(length, [minLen, maxLen], [0, 100])  # brightness 0%~100%
            sbc.set_brightness(setBright)
            if length < 50:
                cv2.circle(img, (cX, cY), 15, (255, 255, 0), cv2.FILLED)

    # display volume bar
    # cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    # cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

    ###

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (30,50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Img", img) 
    cv2.waitKey(1)

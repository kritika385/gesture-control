import cv2
import time
import numpy as np
import mediapipe as mp
import math
import pyautogui  # New library to press keys

# --- Setup ---
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

print("System Ready. Pinch to change volume.")

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2] # Thumb
        x2, y2 = lmList[8][1], lmList[8][2] # Index
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        
        # --- KEYBOARD LOGIC ---
        # If fingers are super close (< 40), press Volume Down
        if length < 40:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            pyautogui.press("volumedown")
            
        # If fingers are far apart (> 200), press Volume Up
        elif length > 150:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
            pyautogui.press("volumeup")

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
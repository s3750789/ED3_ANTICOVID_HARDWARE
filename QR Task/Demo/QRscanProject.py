import cv2
import numpy as np
from pyzbar.pyzbar import decode
from gtts import gTTS
import time
import os

#img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)  # Camera Streaming
cap.set(3, 500)
cap.set(4, 500)
pTime = 0
language = "en"

with open('myDataFile.txt') as f:  # Open and read file
    myDataList = f.read().splitlines()  # Create the info array
    #print(myDataList)

while True:
    success, img = cap.read()  # Capture image
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    for barcode in decode(img):  # Scan Barcode
        myData = barcode.data.decode('utf-8')
        #print(myData)

        if myData in myDataList:  # Check on the list or not
            myOutput = 'Authorized'
            myColor = (0, 255, 0)  # Green
            # Voice the welcome message
            myData = myData[0:(len(myData)-9)]  # Filter out the student ID for welcome message
            wel_mess = "Welcome " + myData + " to the room!"
            print(wel_mess)
            output_voice = gTTS(text=wel_mess, lang=language, slow=False)
            output_voice.save("Welcome.mp3")
            os.system("start Welcome.mp3")
            time.sleep(7)
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)  # Red

        # Drawing bonding box for the scanned QR code
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect

        # Print content on the scanned barcode
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)
import DateTime.interfaces
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
from gtts import gTTS
import os

# Function:
def check_in_list(name):
    file_path = r"K:\RMIT\Course\2021\Sem C\Design 3\QR Task\Demo\check_in_list.txt"
    with open(file_path, "a") as f:  # Open and read file
        f.write(name+"\n")

cap = cv2.VideoCapture(0)  # Camera Streaming
cap.set(3, 500)
cap.set(4, 500)
pTime = 0
language ="en"

dataFile_path = r"K:\RMIT\Course\2021\Sem C\Design 3\QR Task\Demo\myDataFile.txt"
with open(dataFile_path, "r") as f:  # Open and read file
    myDataList = f.read().splitlines()  # Create the info array

while True:
    success, img = cap.read()  # Capture image
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    for barcode in decode(img):  # Scan Barcode
        myData = barcode.data.decode('utf-8')
        currentTime = time.ctime()

        if myData in myDataList:  # Check on the list or not
            myOutput = 'Authorized'
            myColor = (0, 255, 0)  # Green
            # Voice the welcome message
            myData = myData[0:(len(myData)-9)]  # Filter out the student ID for welcome message
            check_in_data = currentTime + '\tAuthorized\t\t' + myData
            check_in_list(check_in_data)

            print(check_in_data)
            # Drawing bonding box for the scanned QR code
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.imshow('Result', img)
            # Voice message
            wel_mess = myData + " has entered the room!"
            output_voice = gTTS(text=wel_mess, lang=language, slow=True)
            output_voice.save("Welcome.mp3")
            time.sleep(2)
            os.system("start Welcome.mp3")
            time.sleep(5)


        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)  # Red
            # Drawing bonding box for the scanned QR code
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.imshow('Result', img)
            check_in_data = currentTime + '\tUn-Authorized\t' + myData
            check_in_list(check_in_data)
            print(check_in_data)

    cv2.waitKey(100)
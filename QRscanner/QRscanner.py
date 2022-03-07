import time
import cv2
import mysql.connector
import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'qrdata')

if mydb.is_connected():
    print("connected")

def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        #print("Barcode: \n" + barcodeData)
        time.sleep(2)

        answers = barcodeData.split("\n")
        currentTime = datetime.now()
        Ans = {"Name" : answers[0],
               "Address" : answers[1],
               "Department" : answers[2],
               "Email" : answers[3],
               "Contact Number" : answers[4],
               "Purpose" : answers[5],
               "Date Time" : currentTime}

        mycursor = mydb.cursor()
        sql = "INSERT INTO answers (fullname, address, department, email, contactNo, purpose, dateTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (answers[0], answers[1], answers[2], answers[3], answers[4], answers[5], currentTime)
        mycursor.execute(sql, val)
        mydb.commit()
        print(Ans)
        print("Record Inserted")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
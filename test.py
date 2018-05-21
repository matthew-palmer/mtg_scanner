import numpy as np
import cv2
from PIL import Image

from os import listdir
import os.path
from os.path import isfile, join
import time

imagePath = 'mtg_images/'
outputPath = 'processed/'
cardsPerPage = 9

failure_thres = 3
# cap = cv2.VideoCapture(0)

files = [f for f in listdir(imagePath) if isfile(join(imagePath, f))]
print(files)
for file in files:
    filePath = imagePath + file
    outPath = outputPath

    image = cv2.imread(filePath)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    flag, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
    flag2, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy2 = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:cardsPerPage]
    contours2 = sorted(contours2, key=cv2.contourArea,reverse=True)[:cardsPerPage]
    contours.extend(contours2)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)
    height, width, channels = image.shape

    print height, width, channels
    correctx = 0
    correcty = 0
    firstRun = True
    jpg = 1
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if w<(width/3):
            if firstRun:
                print "firstRun"
                correctx = x + w
                correcty = y + h
                firstRun = False
                print correctx, correcty
            imcopy = image.copy()
            imy = y + h
            imx = x + w
            print imx, imy
            if imy>(correcty*.9) and imx>(correctx*.9) and jpg <= 9:
                cv2.drawContours(image, contour, -1, (0,255,0), 3)
                crop = imcopy[y:y+h,x:x+w]
                # cv2.imshow("Show", crop)
                # cv2.waitKey(0)
                cv2.imwrite(outPath + str(jpg) + file, crop)
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 0)
                jpg += 1

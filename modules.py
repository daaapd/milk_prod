# -*- coding: utf8 -*-
#import pytesseract
#pytesseract.pytesseract.tesseract_cmd=(r'./venv/Scripts')
import cv2
import numpy as np
import os
#print(cv2.__version__ )
milk = {}
milkItog = {}
# вытягивание цифр
path = os.getcwd()
def denoise(img):
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # #  Apply threshold to get image with only black and white
    # img = apply_threshold(img, method)
    # binarization
    _, img = cv2.threshold(img, 110, 255, cv2.THRESH_TOZERO)
    # cv2_imshow(img)
    return img


# загрузка классификатора
with open('./content/obj.names', 'rt', encoding='utf-8') as f:
    names = f.read().rstrip('\n').split('\n')

# импорт весов
net = cv2.dnn_DetectionModel('./content/yolov4-custom.cfg',
                             './content/yolov4-obj_last.weights')
net.setInputSize(704, 704)
net.setInputScale(1.0 / 255)
net.setInputSwapRB(True)


# поиск продуктов
def find_milk(path, fileName):
    milk = {}
    price = {}
    milkItog = {}
    fileAnalis='analis.jpg'
    os.rename(path + fileName, path + fileAnalis)
    frame = cv2.imread(path + fileAnalis)
    font = cv2.FONT_HERSHEY_COMPLEX

    classes, confidences, boxes = net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
    for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
        label = '%.2f' % confidence
        left, top, width, height = box
        # определение цены
        if height < 30 and classId - 1 >= 8:
            crop_img = frame[top: top + height, left: left + width].copy()
            crop_img = cv2.resize(crop_img, (0, 0), fx=2, fy=2)
            height, width = crop_img.shape[:2]
            y = round(height / 3)
            x = round(width / 2) - 5
            h = round(height / 2)
            w = round(width / 2.3)
            crop = crop_img[y:y + h, x:x + w].copy()
            # crop = denoise(crop)

            ###############Цена##############################
            #target = pytesseract.image_to_string(crop, lang='digits', config='--oem 1 --psm 6')
            #price[classId] = str(target)
            # print(target)
            #############################################
        else:
            # print(height,classId)
            milk[classId - 1] = 1 + milk.setdefault(classId - 1, 0)

    for i in range(0, 9):
        milkItog[i] = milk.setdefault(i, 0)
    os.rename(path + fileAnalis, path + fileName)
    return milkItog, price
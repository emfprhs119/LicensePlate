import cv2
import numpy as np
def imgOp(img):
    '''
    alpha = 1.3
    beta = 40
    gamma = 0.4
    #img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 9, 21)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                img[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)

    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    img = cv2.LUT(img, lookUpTable)
    '''
    img = cv2.bilateralFilter(img,9,75,75)
    #img = cv2.GaussianBlur(img, (7,7), 0)
    #cv2.imshow("img", img)
    '''
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = [[max(pixel - 25, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in hsv[:, :, 2]]
    #cv2.imshow('contrast', cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))
    #mask = cv2.inRange(hsv,(0, 50, 50), (150, 255,255))
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    '''
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #imgBlurred = cv2.GaussianBlur(imgGrayscale, (3, 3), 0)  # blur
    #cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)
    #cv2.namedWindow("imgCanny", cv2.WINDOW_AUTOSIZE)
    height,width = img.shape
    #a,imgBinary = cv2.threshold(img,50,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    #cv2.imshow("img1", img)
    #imgBinary = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,3)
    #cv2.imshow("img2", imgBinary)
    #imgBinary = cv2.erode(imgBinary,(11,11))
    #imgBinary = cv2.erode(imgBinary, (11, 11))
    #imgBinary = cv2.morphologyEx(imgBinary,cv2.MORPH_OPEN,(7,7));
    #cv2.imshow("img0", imgBinary)
    #img = cv2.Laplacian(img,cv2.CV_8U)
    #img = cv2.bitwise_not(img)
    imgBinary = cv2.Canny(img,100,200)
    #cv2.imshow("img0", imgBinary)
    #imgBinary = cv2.bitwise_not(imgBinary)
    return imgBinary
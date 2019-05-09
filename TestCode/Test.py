# CannyStill.py
##################################################################
import cv2
from os import listdir
import numpy as np
import os
import imageOp as im


def main():
    list = []
    dir = "test3"
    list = os.listdir(dir)
    #list.append("20120610_191840.jpg")
    for image in list:
        imgOriginal = cv2.imread(dir+"/"+image)
        height, width,ch = imgOriginal.shape
        imgOriginal= cv2.resize(imgOriginal,(800,int(800/width*height)),interpolation=cv2.INTER_AREA)
        height, width, ch = imgOriginal.shape
        imgBinary = im.imgOp(imgOriginal)
        #cv2.imshow("wo",imgBinary)
        height, width = imgBinary.shape
        #imgBinary = cv2.bitwise_not(imgBinary)
        #imgCanny = cv2.Canny(imgBinary, 50, 200,3)  # get Canny edges
        contours,hierachys=cv2.findContours(imgBinary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        cont =[]
        contMin = []
        rectsTmp = []
        rects = []
        #print(hierachys)
        #print(contours)
        #print(len(hierachys[0]))
        max=0
        boxes=[]
        for cnt in contours:
            flag = True

            for tu in cnt:
                tu = tu[0]
                if tu[0] <= 2 or tu[0] >= width-2 or tu[1] <= 10 or tu[1] >= height-2:
                    flag = False
                    break
            if flag:
                x,y,w,h = cv2.boundingRect(cnt)
                if h/w>1 and w*h>30 and h>10:
                    if not boxes.__contains__((x,y,w,h)):
                        boxes.append((x,y,w,h))
                    cv2.rectangle(imgOriginal,(x,y),(x+w,y+h),(0,255,0))

                '''
                if w>50 and h>50:
                    cont.append(cv2.convexHull(cnt))

                    if cv2.pointPolygonTest(cv2.convexHull(cnt),(width/2,height/2),False)<0:
                        continue
                    tmp = cv2.arcLength(cnt,True)
                    if max < tmp:
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        max = tmp

                    #cv2.circle(imgOriginal, center, radius, (0, 255, 0), 2)

                    #cont.append(contour)
                '''
        boxes.sort(key=lambda s:s[0])
        '''
        for i in range(len(boxes)):
            for j in range(1,len(boxes)-i):
                if boxes[i][0]<boxes[i+j][0]:
                    tmp = boxes[i]
                    boxes[i] = boxes[i+j]
                    boxes[i+j] = tmp
        '''
        frontList = []
        backList = []
        for i in range(len(boxes)):
            count= 0
            tmp = boxes[i]
            for j in range(1,len(boxes)-i):
                if abs(boxes[i][3]-boxes[j+i][3])<tmp[3]/10 and abs(tmp[1]-boxes[j+i][1])<tmp[3]/8 and boxes[j + i][0] < tmp[0]+tmp[2]+tmp[3] and boxes[j + i][0]>tmp[0]+tmp[2] :
                    tmp = boxes[j+i]
                    count+=1
                    if count>2:
                        frontList.append((boxes[i][0],boxes[i][1], boxes[i][0]+ boxes[i][2], boxes[i][1] + boxes[i][3]))
                        backList.append((tmp[0], tmp[1], tmp[0] +tmp[2], tmp[1] + tmp[3]))
                        #cv2.rectangle(imgOriginal, (boxes[i][0],boxes[i][1]), (boxes[i][0]+ boxes[i][2], boxes[i][1] + boxes[i][3]), (0, 0, 255))
                        break
        for i in range(len(frontList)):
            cv2.rectangle(imgOriginal,(frontList[i][0],frontList[i][1]),(frontList[i][2],frontList[i][3]),(0,0,255))
        for i in range(len(backList)):
            cv2.rectangle(imgOriginal,(backList[i][0],backList[i][1]),(backList[i][2],backList[i][3]),(255,0,0))

        last = len(backList)-1
        if (last != -1):
            standard = backList[last][3] - backList[last][1]
            left = backList[last][2] - 8 * standard
            if left < 0 :
                left = 0
            top = backList[last][3] - 2 * standard
            if top < 0 :
                top = 0
            right = backList[last][2]+int(standard/2)
            if right > width :
                right = width
            bottom = backList[last][3] + int(standard / 2)
            if bottom > height :
                bottom = height
            imgOriginal = imgOriginal[top:bottom,left:right]
            cv2.imshow(image,imgOriginal)

        #cv2.imshow(image,cv2.drawContours(imgOriginal,contMin,-1,(0,0,255),1))
        #cv2.imshow(image+"contours1",cv2.drawContours(imgOriginal,cont,-1,(0,0,255),1))
    '''
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w>width/25 and h>width/25 and w<width/2:
            cont.append(contour)
            rectsTmp.append((x,y,w,h))
    rectsTmp1 = []
    for rect0 in rectsTmp:
        flag = False;
        for rect1 in rectsTmp:
            if rect0==rect1:
                continue
            if abs((rect0[0]+rect0[2]/2) - (rect1[0]+rect1[2]/2))<=(rect0[2]/2+rect1[2]/2) and abs((rect0[1]+rect0[3]/2) - (rect1[1]+rect1[3]/2))<=(rect0[3]/2+rect1[3]/2):
                x = rect0[0] if rect0[0]<rect1[0] else rect1[0]
                y = rect0[1] if rect0[1] < rect1[1] else rect1[1]
                w = (rect0[0]+rect0[2] if rect0[0]+rect0[2] > rect1[0]+rect1[2] else rect1[0]+rect1[2]) - (rect0[0] if rect0[0]<rect1[0] else rect1[0])
                h = (rect0[1]+rect0[3] if rect0[1]+rect0[3] > rect1[1]+rect1[3] else rect1[1]+rect1[3]) - (rect0[1] if rect0[1]<rect1[1] else rect1[1])
                rectsTmp1.append([x,y,w,h])
                flag=True
                break
        if not flag:
            rectsTmp1.append(rect0)

    for rect in rectsTmp1:
        cv2.rectangle(imgOriginal, (rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(255,0))
    '''
    #cv2.imshow("rect",imgOriginal)
    cv2.waitKey()  # hold windows open until user presses a key
    cv2.destroyAllWindows()  # remove windows from memory
    return
    ##################################################################
if __name__ == "__main__":
    main()
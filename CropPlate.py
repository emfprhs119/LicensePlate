import cv2
import os
class Rect:
    x=0
    y=0
    w=0
    h=0
    def __init__(self,rt):
        self.x=rt[0]
        self.y=rt[1]
        self.w=rt[2]
        self.h=rt[3]
    def left(self):
        if (self.x + self.w < 0):
            return 0
        return self.x
    def top(self):
        if (self.y<0):
            return 0
        return self.y
    def right(self):
        return self.x+self.w
    def bottom(self):
        return self.y+self.h
    def similar(self,obj):
        return abs(self.x-obj.x)+abs(self.y-obj.y)+abs(self.w-obj.w)+abs(self.x-obj.h)<8
def main():
    dir = "test1"
    fileList = os.listdir(dir)
    '''
    fileList.clear()
    fileList.append("DSCF0639.jpg")
    '''
    for fileName in fileList:
        if not fileName.__contains__("."):
            continue
        imgOriginal = cv2.imread(dir + "/" + fileName)

        '''Image Process'''
        height, width, ch = imgOriginal.shape
        if width > 800:
            imgResize = cv2.resize(imgOriginal, (800, int(800 / width * height)), interpolation=cv2.INTER_AREA)
        else:
            imgResize = imgOriginal

        height, width, ch = imgResize.shape
        imgFilter = cv2.bilateralFilter(imgResize, 9, 75, 75)
        imgCvt = cv2.cvtColor(imgFilter, cv2.COLOR_BGR2GRAY)
        imgCanny= cv2.Canny(imgCvt, 100, 200)

        '''Find Contours'''
        contours, hierarchys = cv2.findContours(imgCanny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        boxes = []
        for cnt in contours:
            flag = True
            for tu in cnt:
                tu = tu[0]
                if tu[0] <= 2 or tu[0] >= width - 2 or tu[1] <= 10 or tu[1] >= height - 2: #remove outLine
                    flag = False
                    break
            if flag:
                x, y, w, h = cv2.boundingRect(cnt)
                if h / w > 1 and w * h > 30 and h > 10:
                    boxes.append(Rect([x,y,w,h]))
        boxes.sort(key=lambda s: s.x)

        '''Find Number'''
        rearList = []
        for i in range(len(boxes)):
            count = 0
            tmpBox = boxes[i]
            cv2.rectangle(imgResize,(tmpBox.x,tmpBox.y),(tmpBox.right(),tmpBox.bottom()),[0,0,255])
            for j in range(1, len(boxes) - i):
                if tmpBox.similar(boxes[j + i]):
                    continue
                if abs(boxes[i].h - boxes[j + i].h) < tmpBox.h / 10 and abs(tmpBox.y - boxes[j + i].y) < tmpBox.h / 8 \
                        and boxes[j + i].x < tmpBox.right() + tmpBox.h and boxes[j + i].x > tmpBox.right():
                    tmpBox = boxes[j + i]
                    cv2.rectangle(imgResize,(tmpBox.x,tmpBox.y),(tmpBox.right(),tmpBox.bottom()),[0,0,255])
                    count += 1
                    if count > 2:
                        rearList.append(tmpBox)
                        break

        '''Crop Image'''
        index = len(rearList)-1
        if index >= 0:
            rect = rearList[index]
            rect = Rect([rect.x-rect.h*7,rect.y - rect.h,int(rect.w + rect.h * 7.5),int(rect.h * 2.5)])
            if rect.x < 0:
                rect.w += rect.x
                rect.x = 0
            if rect.y < 0:
                rect.h += rect.y
                rect.y = 0
            if rect.w > width:
                rect.w = width
            if rect.h > height:
                rect.h = height
            imgCrop = imgResize[rect.y:rect.y+rect.h,rect.x:rect.x+rect.w]
            #cv2.imshow(fileName,imgCrop)
            if not os.path.isdir(dir+"/crop"):
                os.mkdir(dir+"/crop")
            cv2.imwrite(dir+"/crop/"+fileName,imgCrop)
        cv2.imshow(fileName+"1", imgResize)
    cv2.waitKey()  # hold windows open until user presses a key
    cv2.destroyAllWindows()  # remove windows from memory
    return
if __name__ == "__main__":
    main()
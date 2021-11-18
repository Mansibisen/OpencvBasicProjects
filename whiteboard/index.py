import cv2
import numpy as np

webCam = cv2.VideoCapture(0)
## color of markers we want to detect
markers = [[5 , 107 , 0 , 19 , 255 , 255] , [100 , 107 , 0 , 19 , 255 , 255] , [ 67, 107 , 0 , 19 , 255 , 255]]
colors =[[255 , 255 , 0],[ 32 , 143 , 67] ,[ 56, 78 , 230]]
points =[]
def contours(img):
    contours, hierarchy = cv2.findContours(img , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
    x , y, h, w =0,0,0,0
    for i in contours:
        area = cv2.contourArea(i)

        if area > 500:
            #cv2.drawContours(imgcontour, i, -1, (255, 0, 0), 6)
            arc = cv2.arcLength(i , True)
            cornorapprox = cv2.approxPolyDP(i , 0.02*arc, True)

            x , y , w , h,  = cv2.boundingRect(cornorapprox)
    return (x+w)//2 , y

def func(img , markers , colors ):
    imghsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    count = 0;
    newpoints =[]
    for i in markers:

        lower = np.array(i[0 :3])
        upper = np.array(i[3:])
        mask = cv2.inRange(imghsv , lower , upper)
        x, y = contours(mask)
        cv2.circle(imgcontour , (x, y) , 10 , colors[count] , cv2.FILLED )
        if(x!= 0 & y!=0):
            newpoints.append([x , y, id])
        #cv2.imshow( str(i[0]) , mask)
        count+= 1
    return newpoints
def draw(points , colors):
    for point in points:
        cv2.circle(imgcontour, (point[0], point[1]), 10, point[2], cv2.FILLED)

while True:
    success , video_to_img = webCam.read()
    imgcontour = video_to_img.copy()
    newpoints  = func(video_to_img , markers , colors)
    if len(newpoints) != 0:
        for i in newpoints:
            points.append(i)
    if len(points) != 0:
        draw(points , colors)

    cv2.imshow("output",imgcontour)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

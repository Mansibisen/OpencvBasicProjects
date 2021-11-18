import cv2
import numpy as np
width = 640
height = 480
webCam = cv2.VideoCapture(0)
webCam.set(3 , 600)
webCam.set(4 , 500)
webCam.set(10 , 100) ## brightness 10 is ID
def preprocessor(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblurr = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCaned = cv2.Canny(imgblurr, 150, 150)
    imgdial = cv2.dilate(imgCaned, np.ones((5, 5), np.uint8), iterations=2)
    imgerros = cv2.erode(imgdial, np.ones((5, 5), np.uint8), iterations=1)
    return imgerros
def contours(img):
    contours, hierarchy = cv2.findContours(img , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
    maxarea = 0
    biggest = np.array([])
    for i in contours:
        area = cv2.contourArea(i)

        if area > 5000:
            cv2.drawContours(imgcontour, i, -1, (255, 0, 0), 6)
            arc = cv2.arcLength(i , True)
            cornorapprox = cv2.approxPolyDP(i , 0.02*arc, True)
            if area> maxarea & len(cornorapprox) == 4:
                biggest = cornorapprox
                maxarea = area
    return biggest
def wrap(img , biggest):
    reorder(biggest)
    points = np.float32(biggest)
    points2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(points, points2)
    imgout = cv2.warpPerspective(img, matrix, (width, height))
    imgcropped  = imgout[20:imgout.shape[0]-20 , 20:imgout.shape[1]-20 ]
    imgcropped = cv2.resize(imgcropped, (width, height))
    return imgout

def reorder(points):
    points = np.reshape(points , (4, 2))
    results = np.zeros((4,1,2) , np.uint32)
    add = points.sum(1)
    results[0] = points[np.argmin(add)]
    results[3] = points[np.argmax(add)]
    diff = np.diff(points , axis = 1 )
    results[1] = points[np.argmin(diff)]
    results[2] = points[np.argmax(diff)]


while True:
    success , cam_to_img = webCam.read()

    cam_to_img = cv2.resize(cam_to_img , (width, height))
    imgcontour = cam_to_img.copy()
    imgThres = preprocessor(cam_to_img)
    biggest  = contours(imgThres)

    if(len(biggest) == 0):
        biggest =[[111  , 150 ], [ 145 , 200] ,[ 450 , 560]  , [490 , 600] ]

    imgout = wrap(cam_to_img, biggest)
    cv2.imshow('video', imgout)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

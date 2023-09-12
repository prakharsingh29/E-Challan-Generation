import cv2
from PIL import Image
import pytesseract
import time


#zero means only the webcam
#video = cv2.VideoCapture(0)
#video.set(3,500) #for width = 500
#video.set(4,500) #for width=500
#video.set(10,100) #for brightness=100

npcascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
minarea = 1000
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#path = 'product-500x500.jpeg'
#path = 'carimg.jpg'
path = 'C:/Users/91884/Desktop/carimg.jpg'
#path = 'demo.jpg'
#path = 'White-2BPlate.jpeg'
'''
while True:
    success,img = video.read()
    #img_resized = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
    # converting to a grayscale image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # searching co ordinates in the image(human face)
    number_plate = npcascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
    # creating face rectangle
    for x, y, w, h in number_plate:
        area = w*h
        if area > minarea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img,'Number Plate',(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            imgroi = img[y:y+h,x:x+w]
            cv2.imshow('ROI',imgroi)
    #img = cv2.resize(img,(int(img.shape[1]*3/4),int(img.shape[0]*3/4)))
    cv2.imshow('Original', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
'''

#for static images
img = cv2.imread(path)
#resizing the image
imgresized = cv2.resize(img, (int(img.shape[1]), int(img.shape[0])))
#cv2.imshow('Car',imgresized) #showing the image
gray_img = cv2.cvtColor(imgresized,cv2.COLOR_BGR2GRAY)

number_plate = npcascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
for x, y, w, h in number_plate:
        area = w*h
        if area > minarea:
            cv2.rectangle(imgresized, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(imgresized,'Number Plate',(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(100,200,100),2)
            imgroi = img[y:y+h,x:x+w]
            cv2.imshow('ROI',imgroi)
            roi_resized = cv2.resize(imgroi, (250, 250))
            cv2.imwrite('img.jpg',imgroi)

cv2.imshow('Detected Image',imgresized)

#delay of 4 seconds
cv2.waitKey(4000)
#delay of 1 second
time.sleep(1)

image = cv2.imread('img.jpg')
image = cv2.resize(img, (360, 360))
text = pytesseract.image_to_string(image,lang='eng')
print('NumberPlate:',text)
img_recog = img.copy()
for x, y, w, h in number_plate:
        area = w*h
        if area > minarea:
            cv2.rectangle(img_recog, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img_recog,text,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(100,200,100),2)
            imgroi = img[y:y+h,x:x+w]
            cv2.imshow('ROI',imgroi)
            roi_resized = cv2.resize(imgroi, (250, 250))

cv2.imshow('Recog Image',img_recog)
#delay of 3 seconds
cv2.waitKey(3000)

import cv2
import numpy as np
import time
import mediapipe as mp
import os

def fingerup(pos):
    flags=[0,0]

    if pos[8][1]<pos[7][1]:
        flags[0]=1
    else:
        flags[0]=0
    if pos[12][1]<pos[11][1]:
        flags[1]=1
    else:
        flags[1]=0

    return flags

mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils
folderpath="images"
thpath="thicknessimgs"
mylist2=os.listdir(thpath)
mylist=os.listdir(folderpath)
print(mylist[0])
overlaylist1=[]
for impath in mylist:
    image=cv2.imread(f'{thpath}/{impath}')
    overlaylist1.append(image)
fotter=overlaylist1[0]
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
header=overlaylist[0]
color=(37,193,255)
thickness=10
xp,yp=0,0
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

imgcanvas=np.zeros((1080,1280,3),np.uint8)


while True:

    success,img=cap.read()
    #print(img.shape)
    img = cv2.resize(img, (1280, 1080))
    img=cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    pointers=[]
    if results.multi_hand_landmarks:
        positions={}
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                #print(h,w,c,lm.x,lm.y)
                cx, cy = int(lm.x * w), int(lm.y * h)
               # print(id, cx, cy)
                positions[id]=[cx,cy]
                if(id==8 or id==12):
                    pointers.append([cx,cy])

            fg=fingerup(positions)

            if(fg[0] and fg[1]):
                xp,yp=0,0
                print(positions[8])
                if(positions[8][0]<450 and positions[8][0]>380 and positions[8][1]<100):
                    header = overlaylist[0]
                    color=(37,193,255)


                if(positions[8][0]>500 and positions[8][0]<570 and positions[8][1]<100):
                    header=overlaylist[1]
                    color=(48,48,255)


                if(positions[8][0]>650 and positions[8][0]<730 and positions[8][1]<100):
                    header=overlaylist[2]
                    color=(34,139,38)


                if(positions[8][0]>790 and positions[8][0]<900 and positions[8][1]<100):
                    header=overlaylist[3]
                    color=(0,0,0)


                if(positions[8][1]>280 and positions[8][1]<300 and positions[8][0]<100):
                    fotter=overlaylist1[0]
                    thickness=10
                if (positions[8][1] > 340 and positions[8][1] < 360 and positions[8][0] < 100):
                    fotter = overlaylist1[1]
                    thickness = 25
                if (positions[8][1] > 420 and positions[8][1] < 460 and positions[8][0] < 100):
                    fotter = overlaylist1[2]
                    thickness = 50





                cv2.rectangle(img,(positions[8][0],positions[8][1]-25),(positions[12][0],positions[12][1]+25),color,cv2.FILLED)
            if(fg[0]==1 and fg[1]==0):
                # print("drawing")
                print(pointers[0][0],pointers[0][1])

                img = cv2.circle(img, (pointers[0][0], pointers[0][1]), thickness, color, -1)
                # # print(xp,yp)
                if xp==0 and yp==0:
                    xp,yp=pointers[0][0],pointers[0][1]

                else:
                    cv2.line(img,(xp,yp),(pointers[0][0],pointers[0][1]),color,thickness)

                    cv2.line(imgcanvas, (xp, yp), (pointers[0][0], pointers[0][1]), color, thickness)

                    xp, yp = pointers[0][0], pointers[0][1]



    # img = cv2.resize(img, (1280, 1080))



    img[0:100,0:1280]=header
    img[250:500,0:100]=fotter
    img=cv2.addWeighted(img,0.7,imgcanvas,0.5,0)
    cv2.imshow("input",img)
   # print(img.shape,imgcanvas.shape)
   # cv2.imshow("input1", imgcanvas)
    cv2.waitKey(1)

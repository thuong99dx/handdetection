import cv2
import time
import os
import track as htm

widthCam,heightCam = 600, 450
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#cap.set(3, widthCam)
#cap.set(4, heightCam)

def getNumber(ar):
    s=""
    for i in range (0,5):
       s+=str(ar[i]);
    # if(s=="00000"):
    #     return (0)
    # elif(s=="01000"):
    #     return(1)
    # elif(s=="01100"):
    #     return(2) 
    # elif(s=="01110"):
    #     return(3)
    # elif(s=="01111"):
    #     return(4)
    # elif(s=="11111"):
    #     return(5) 
    if(s=="11000"):
        return(6)
    elif(s=="00111"):
        return(7)   
    else:
        totalFingers = ar.count(1)
        return totalFingers   
folderPath = "FingerImages"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    #print(f'{folderPath}/{imgPath}')
    overlayList.append(image )
detector = htm.handDetector(detectionCon=0.75, maxHands=2)
pTime = 0
#cot moc o dau cac ngon tay
tipIds = [4, 8, 12, 16, 20, 25, 29, 33, 37, 41]
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img= detector.findHands(img)
    hand_label, hand_pre = detector.handedness(img)
    #print(hand_label)
    lmlist = detector.findPosition(img,draw=False )
    if len(lmlist) != 0:
        fingers = [] 
        if len(lmlist) == 21: # chỉ có 1 bàn tay trong khung hình
        # right hand
            if lmlist[tipIds[1]][1] < lmlist[tipIds[3]][1]:
                #Thumb
                if lmlist[tipIds[0]][1] < lmlist[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0) 
            # left hand
        
            # 4 other fingers
            for id in range(1,5):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        #print(fingers)
        if len(lmlist) == 42: # có cả 2 bàn tay trong khung hình = 42 điểm mốc
            # 21 mốc đầu tiên là của bàn tay xuất hiện bên trái khung hình,
            # 21 mốc sau là bàn tay xuất hiện bên phải khung hình
            
            # Tay bên trái
            if lmlist[tipIds[1]][1] < lmlist[tipIds[3]][1]:
                #Thumb
                if lmlist[tipIds[0]][1] < lmlist[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0) 
            # 4 other fingers
            for id in range(1,5):
                    if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            
            # tay bên phải
            if lmlist[tipIds[6]][1] < lmlist[tipIds[8]][1]:
                    #Thumb
                if lmlist[tipIds[5]][1] < lmlist[tipIds[5]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if lmlist[tipIds[5]][1] > lmlist[tipIds[5]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            for id in range(6,10):
                    if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1)
        #cv2.rectangle(img,(100,25),(300,225),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(105,175),cv2.FONT_HERSHEY_PLAIN,10, (255,0,0), 15)
        # cv2.putText(img,str(getNumber(fingers)),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),20)    
        #h,w,d = overlayList[totalFingers-1].shape
        #img[0:h, 0:w] = overlayList[totalFingers-1]
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (350, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 100, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
            break

from tkinter import font
import cv2
import time
import os
import tracking1 as htm
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pyfirmata

# kết nối tới board Arduino thông qua cổng COM
board = pyfirmata.Arduino("COM3")

class Sample(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Finger Detection")
        self.pack(fill=BOTH, expand=1)
        # giao diện hệ thống
        imageBg = ImageTk.PhotoImage(Image.open('D:/AI.jpg').resize((1000,800)))
        backgroundLable = tk.Label(self, image = imageBg,width=1000, height=750)
        backgroundLable.image = imageBg
        backgroundLable.grid(row=0,column=0,rowspan=100)
        
        # logo = ImageTk.PhotoImage(Image.open("D:/hand.jpg").resize((180,180)))
        # bglogo = tk.Label(self,image=logo)
        # bglogo.image = logo
        # bglogo.grid(row=35,column=0)
        label = tk.Label(self, text="HỌC VIỆN KỸ THUẬT MẬT MÃ",font=("Helvetica",30), fg="red",bg="#FFFACD")
        label.grid( row= 6, column = 0)
        label1 = tk.Label(self, text = "THỊ GIÁC MÁY TÍNH TRÊN NỀN TẢNG NHÚNG", font=("Helvetica",20),fg="red",bg="#FFFACD")
        label1.grid(row = 10, column=0)
        label2 = tk.Label(self, text="ĐIỀU KHIỂN THIẾT BỊ BẰNG CỬ CHỈ TAY", font=("Helvetica",20),fg="red",bg="#FFFACD")
        label2.grid(row=12, column=0)
        
        button = tk.Button(self, text = "Điều khiển",font=("Helvetica",20),command=self.detectHand,fg="red",height=2,width=15,bg="#00FF7F")
        button.place(x=210, y=570)
        button1 = tk.Button(self, text="Thoát",font=("Helvetica",20),fg="red",command=lambda: self.parent.destroy(),height=2,width=15,bg="#00FF7F")
        button1.place(x=550,y=570)
    def detectHand(self):
        widthCam,heightCam = 600, 450
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        # đẩy các ptu ảnh trong thư mục vào thành 1 ds
        folderPath = "FingerImages"
        myList = os.listdir(folderPath)
        #print(myList)
        overlayList = []
        for imgPath in myList:
            image = cv2.imread(f'{folderPath}/{imgPath}') #ma trận ảnh
            #print(f'{folderPath}/{imgPath}') : đường dẫn ảnh
            overlayList.append(image )
        detector = htm.handDetector(detectionCon=0.75)
        pTime = 0
        cTime = 0
        #cot moc o dau cac ngon tay
        tipIds = [4, 8, 12, 16, 20]
        while True:
            success, img = cap.read()
            img = cv2.flip(img,1)
            img = detector.findHands(img)
            lmlist = detector.findPosition(img,draw=False )# phát hiện vị trí các mốc
            #print(lmlist)
            if len(lmlist) != 0:
                fingers = []
                # tay phải
                if lmlist[tipIds[1]][1] < lmlist[tipIds[3]][1]: # tọa độ x của đầu ngón trỏ nhỏ hơn đầu ngón áp út
                    # xét ngón cái: nếu mốc 4 có tọa độ y nhỏ hơn mốc 3 
                    if lmlist[tipIds[0]][1] < lmlist[tipIds[0]-1][1]:
                        fingers.append(1)# ngón tay đang mở
                    else:
                        fingers.append(0)# ngón tay đóng
                
                else: # ngược lại là tay trái
                    #  xét ngón cái
                    if lmlist[tipIds[0]][1] > lmlist[tipIds[0]-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0) 
                
                # 4 other fingers
                for id in range(1,5):
                    # xét tọa độ y
                    # nếu điểm đầu(8,12,16,20) của các ngón tay nhỏ hơn (6,10,14,18)
                    if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                        fingers.append(1) # ngón tay mở
                    else:
                        fingers.append(0) # ngón tay đóng
                print(fingers)
                totalFingers = self.getNumber(fingers)# tính tổng số ngón tay đang mở
                print(totalFingers)

                # điều khiển
                self.controlLed(totalFingers)  
                
                # ô hiển thị tổng số ngón tay mở
                cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
                cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10, (255,0,0), 20)
                #cv2.putText(img,str(getNumber(fingers)),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),20)  
                
                # gán ảnh vào khung hình của camera
                h,w,d = overlayList[totalFingers-1].shape
                img[0:h, 0:w] = overlayList[totalFingers-1]

            
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (350, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 100, 255), 3)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) == 27:
                    break
        cv2.destroyAllWindows()
    def getNumber(self,arr):
        s=""
        for i in range (0,5):
            s += str(arr[i]);
        if(s=="11000"):
            return(6)
        elif(s=="00111"):
            return(7)   
        else:
            totalFingers = arr.count(1)
            return totalFingers
    
    def controlLed(self,totalFingers):
        #board.digital[9].write(1)
        led =[8, 9, 10, 11, 12] # khai báo chân digital led
        if totalFingers == 0: # nếu cả bàn tay đang nắm lại thì tắt led
            self.TatLed(led)
        elif totalFingers == 6: # nếu tay đang có cử chỉ của số 6 thì nháy tất cả các led
                for i in range (0,5):
                    self.BatLed(led[i])
                self.TatLed(led)
        elif totalFingers == 7: # cử chỉ số 7 thì bật led 1,3,5
            for i in range(0,5,2):
                self.BatLed(led[i])
            arr = [9,11]
            self.TatLed(arr)
        else: # còn lại bật led theo đúng thứ tự của cử chỉ tay: 1-led1, 2-led2...
            self.BatLed(led[totalFingers-1])
        # print(led[totalFingers-1])
    def BatLed(self,a):
        print("Bat led ", a)
        board.digital[a].write(1)
        time.sleep(0.1)
    def TatLed(self,ar):
        for i in range (0,len(ar)):
            board.digital[ar[i]].write(0)
            print("Tat led",ar[i])
            time.sleep(0.1)

root = tk.Tk()
root.geometry("1000x800+300+0")
ex = Sample(root)
root.mainloop()

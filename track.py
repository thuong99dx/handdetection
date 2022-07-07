import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode = False, maxHands = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)
        #print(self.results.multi_handedness)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw: # vẽ các mốc và đường nối các mốc theo drawing_styles lên bàn tay
                    self.mpDraw.draw_landmarks(
                        img, 
                        hand_landmarks,
                        self.mpHands.HAND_CONNECTIONS,
                        self.drawing_styles.get_default_hand_landmarks_style(),
                        self.drawing_styles.get_default_hand_connections_style())
        return img

    def handedness(self,img):
        hand_label =''
        hand_pre = 0
        if self.results.multi_handedness:
            for hand_index, hand_info in enumerate(self.results.multi_handedness):
                hand_label = hand_info.classification[0].label # trả về kết quả tay trái hay tay phải
                hand_pre = hand_info.classification[0].score  # trả về độ chính xác khi phát hiện ra tay trái/phải
                print(hand_label)
                print(hand_pre)
        return hand_label, hand_pre
    def findPosition(self, img, draw = True):
        
        lmlist = [] # dùng để lưu tất các các điểm mốc cùng với vị trí tọa độ tương ứng của nó
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h) # tính x, y
                    lmlist.append([id, cx, cy])
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        #if len(lmlist) != 0:
            #print(lmlist[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1):
            break


if __name__ == "__main__":
    main()

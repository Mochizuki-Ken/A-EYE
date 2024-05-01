import mediapipe as mp
import cv2


class HandPose():
    def __init__(self) -> None:
        self.mpHands = mp.solutions.hands
        
        self.hands = self.mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils
        self.handLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
        self.handConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)

    def GetHandMarkPos(self,frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        HandResult = self.hands.process(imgRGB) 
        imgHeight = frame.shape[0]
        imgWidth = frame.shape[1]

        if HandResult.multi_hand_landmarks: 
            for handLms in HandResult.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS, self.handLmsStyle, self.handConStyle)
                x1,y1,x2,y2,x3,y3 = handLms.landmark[4].x * imgWidth , handLms.landmark[4].y * imgHeight ,handLms.landmark[8].x * imgWidth  ,handLms.landmark[8].y * imgHeight,handLms.landmark[12].x * imgWidth  ,handLms.landmark[12].y * imgHeight  
                return [frame,{"ThumbX":x1,"ThumbY":y1,"IndexX":x2,"IndexY":y2,"MiddleX":x3,"MiddleY":y3}]
        return False
                   # self.ACTION.DoubleClick_Detection(x1,y1,x2,y2,self.TIMER)



# if HandResult.multi_hand_landmarks: 
#     for handLms in HandResult.multi_hand_landmarks:
#         self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS, self.handLmsStyle, self.handConStyle)
#         for i, lm in enumerate(handLms.landmark):
#             xPos = int(lm.x * imgWidth)
#             yPos = int(lm.y * imgHeight)
#             x1,y1,x2,y2 = handLms.landmark[4].x * imgWidth , handLms.landmark[4].y* imgHeight ,handLms.landmark[8].x* imgWidth  ,handLms.landmark[8].y* imgHeight 
#             hand_x1,hand_y1,hand_x2,hand_y2 = x1,y1,x2,y2
#                 # double click detect 
#             print(self.Timer,self.ACTION_STATE[1])
#             return [frame,{x1,y1,x2,y2}]
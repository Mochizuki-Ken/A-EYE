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

        IMG_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        HAND_RESULTS = self.hands.process(IMG_RGB) 
        IMG_HEIGHT = frame.shape[0]
        IMG_WIDTH = frame.shape[1]

        if HAND_RESULTS.multi_hand_landmarks: 
            
            for handLms in HAND_RESULTS.multi_hand_landmarks:
                
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS, self.handLmsStyle, self.handConStyle)
                
                x1,y1,x2,y2,x3,y3 = handLms.landmark[4].x * IMG_WIDTH , handLms.landmark[4].y * IMG_HEIGHT ,handLms.landmark[8].x * IMG_WIDTH  ,handLms.landmark[8].y * IMG_HEIGHT,handLms.landmark[12].x * IMG_WIDTH  ,handLms.landmark[12].y * IMG_HEIGHT  
                
                return [frame,{"ThumbX":x1,"ThumbY":y1,"IndexX":x2,"IndexY":y2,"MiddleX":x3,"MiddleY":y3}]
        
        return False



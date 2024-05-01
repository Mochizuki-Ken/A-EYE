import cv2
import mediapipe as mp 
import math

from .action import Action
from .handPose import HandPose
from .objects import Objects

class A_EYE():

    GREEN = (0, 255, 0) 
    RED = (0, 0, 255) 
    BLUE = (255, 0, 0) 
    FONT_SIZE = 0.75

    def __init__(self,STREAM_INPUT) -> None:
        self.STREAM_INPUT = STREAM_INPUT
        self.TIMER = 0

        self.ACTION = Action()
        self.HANDPOSE = HandPose()
        self.OBJECT = Objects()

        self.ACTION_STATE = [0,0,0,"NONE","NONE"]#[ click state 0 = up / 1 = down , last time , click count , active click type]
        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.frame = 0

    def ShowDetail(self):

        cv2.putText(
            self.frame,
            'Time'+str(self.TIMER)+"",
            (20,45),
            cv2.FONT_HERSHEY_COMPLEX ,
            self.FONT_SIZE,self.GREEN,2
        )

        cv2.putText(
            self.frame,
            f"up/down {self.ACTION_STATE[0]} | last time {self.ACTION_STATE[1]} | count {self.ACTION_STATE[2]} | {self.ACTION_STATE[3]}",
            (20,90),
            cv2.FONT_HERSHEY_COMPLEX ,
            self.FONT_SIZE,self.GREEN,
            2
        )

    def Streaming(self):
        cap = cv2.VideoCapture(self.STREAM_INPUT)
        return cap
    
    def Service(self):

        HandPose = self.HANDPOSE.GetHandMarkPos(self.frame)
        # frame = HandPose[0]

        ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY = 0,0,0,0,0,0
        
        if ( HandPose ):

            self.ACTION_STATE = self.ACTION.ACTION_STATE

            ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY = HandPose[1]["ThumbX"],HandPose[1]["ThumbY"],HandPose[1]["IndexX"],HandPose[1]["IndexY"],HandPose[1]["MiddleX"],HandPose[1]["MiddleY"],

            self.ACTION.DoubleClick_Detection(
                ThumbX,
                ThumbY,
                IndexX,
                IndexY,
                MiddleX,
                MiddleY,
                self.TIMER
            )

            self.frame = HandPose[0]
         
        self.OBJECT.CURRENT_OBJECT_ANNOUNCEED = self.CURRENT_OBJECT_ANNOUNCEED
        self.frame = self.OBJECT.ObjectDetect(self.frame,ThumbX,ThumbY,IndexX,IndexY,self.ACTION_STATE[3])
        if(self.CURRENT_OBJECT_ANNOUNCEED != self.OBJECT.CURRENT_OBJECT_ANNOUNCEED):
            self.CURRENT_OBJECT_ANNOUNCEED= self.OBJECT.CURRENT_OBJECT_ANNOUNCEED
        
        return self.frame

    def Start(self):
        Stream = self.Streaming()

        while Stream:
            if Stream.isOpened():

                ret, frame = Stream.read()

                if ( frame is not None ):

                    self.frame = frame

                    self.ACTION.CURRENT_OBJECT_ANNOUNCEED = self.CURRENT_OBJECT_ANNOUNCEED 
                    self.ACTION.ActionCheck(self.TIMER)
                    self.CURRENT_OBJECT_ANNOUNCEED = self.ACTION.CURRENT_OBJECT_ANNOUNCEED

                    self.TIMER += 1

                    frame = self.Service()

                    self.ShowDetail()

                    

                    cv2.imshow("A_EYE",frame)

            key = cv2.waitKey(1)
            if key == ord("s"):
                break

        cv2.destroyAllWindows()
        Stream.release()
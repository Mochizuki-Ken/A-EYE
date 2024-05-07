import cv2

from .action import Action
from .handPose import HandPose
from .objects import Objects
from .speak import Text_To_Voice

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
        self.SPEAK = Text_To_Voice()
        self.OBJECT = 0#Objects()

        self.ACTION_STATE = [0,0,0,"NONE","NONE"]#[ click state 0 = up / 1 = down , last time , click count , active click type]
        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.frame = 0

        self.FRAME_WIDTH = 0
        self.FRAME_HEIGHT = 0

        self.HAND_DISAPPEAR_COUNT = 0

        self.CLICK_TYPE = ["MIDDLE_DOUBLE_CLICK","INDEX_DOUBLE_CLICK"]

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

        ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY = 0,0,0,0,0,0

        HandArea = 0
        
        if ( HandPose ):

            HandArea = HandPose[2]

            self.ACTION_STATE = self.ACTION.ACTION_STATE

            if( self.ACTION_STATE[3] in self.CLICK_TYPE and self.HAND_DISAPPEAR_COUNT == 0):

                self.HAND_DISAPPEAR_COUNT = 0

            ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY = HandPose[1]["ThumbX"],HandPose[1]["ThumbY"],HandPose[1]["IndexX"],HandPose[1]["IndexY"],HandPose[1]["MiddleX"],HandPose[1]["MiddleY"],

            self.ACTION.DoubleClick_Detection(
                HandArea,
                ThumbX,
                ThumbY,
                IndexX,
                IndexY,
                MiddleX,
                MiddleY,
                self.TIMER
            )

        elif ( self.HAND_DISAPPEAR_COUNT >=5 ):

            self.ACTION_STATE = [0,0,0,"NONE","NONE"]

            self.ACTION.ACTION_STATE =self.ACTION_STATE 

        else:

            self.HAND_DISAPPEAR_COUNT += 1
         
        self.OBJECT.CURRENT_OBJECT_ANNOUNCEED = self.CURRENT_OBJECT_ANNOUNCEED
        self.frame = self.OBJECT.ObjectDetect(self.frame,ThumbX,ThumbY,IndexX,IndexY,self.ACTION_STATE[3],HandArea,self.TIMER)
        self.OBJECT.HandEvent(self.ACTION_STATE[3])
        if(self.CURRENT_OBJECT_ANNOUNCEED != self.OBJECT.CURRENT_OBJECT_ANNOUNCEED):
            self.CURRENT_OBJECT_ANNOUNCEED= self.OBJECT.CURRENT_OBJECT_ANNOUNCEED
        
        if(HandPose!=False):self.frame = HandPose[0]

        return self.frame

    def Start(self):
        Stream = self.Streaming()

        while Stream:
            
            if Stream.isOpened():

                ret, frame = Stream.read()

                if ( frame is not None ):

                    if( self.FRAME_WIDTH == 0 and self.FRAME_HEIGHT == 0) :

                        #Do When First Frame Captured

                        self.FRAME_WIDTH = frame.shape[1]
                        self.FRAME_HEIGHT = frame.shape[0]

                        self.HANDPOSE.FRAME_WIDTH = frame.shape[1]
                        self.HANDPOSE.FRAME_HEIGHT = frame.shape[0]

                        self.OBJECT = Objects(self.FRAME_WIDTH,self.FRAME_HEIGHT)

                        self.SPEAK.ThreadSpeak(temp="Welcome")



                        print(self.FRAME_WIDTH,self.FRAME_HEIGHT)
                    
                    self.frame = frame

                    self.ACTION.CURRENT_OBJECT_ANNOUNCEED = self.CURRENT_OBJECT_ANNOUNCEED 
                    self.ACTION.ActionCheck(self.TIMER)
                    self.CURRENT_OBJECT_ANNOUNCEED = self.ACTION.CURRENT_OBJECT_ANNOUNCEED
                    self.OBJECT.CURRENT_OBJECT_ANNOUNCEED = self.CURRENT_OBJECT_ANNOUNCEED

                    self.TIMER += 1

                    self.OBJECT.TIMER = self.TIMER

                    frame = self.Service()

                    self.ShowDetail()

                    cv2.imshow("A_EYE",frame)

            key = cv2.waitKey(1)

            if key == ord("s"):break

        cv2.destroyAllWindows()

        Stream.release()
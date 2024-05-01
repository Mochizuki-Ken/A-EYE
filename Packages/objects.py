import torch
import cv2
from ultralytics import YOLO
from .action import Action
from .speak import Text_To_Voice

class Objects():

    OBJECTS_MODEL_PT_FILE = "./Test/best-2.pt"

    OBJECTS_LABEL = ["薯片","粟米片","咖啡","Tempo紙巾","高路潔牙膏","保溫瓶","hkd10","hkd100","hkd20","hkd50","hkd500"]

    GREEN = (0, 255, 0) 
    RED = (0, 0, 255) 
    BLUE = (255, 0, 0) 
    FONT_SIZE = 0.75

    def __init__(self) -> None:

        device: str = "mps" if torch.backends.mps.is_available() else "cpu"

        self.OBJECTS_MODEL = YOLO(self.OBJECTS_MODEL_PT_FILE)

        self.OBJECTS_MODEL.to(device=device)

        self.CASH_COUNTER = {"hkd10":0,"hkd20":0,"hkd50":0,"hkd100":0,"hkd500":0,}
        
        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.TARGET_OBJECT = []

        self.ACTION = Action()

        self.SPEAK = Text_To_Voice()


        return

    def Objects_Model_fit(self,frame):
        Object_Result = self.OBJECTS_MODEL(frame)
        # Object_Result = Object_Result.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']].values
        return Object_Result

    def ObjectDetect(self,frame,HandPosX1,HandPosY1,HandPosX2,HandPosY2,CurrentAction):

        results = self.Objects_Model_fit(frame)

        boxes = results[0].boxes.cpu().numpy()

        XYXYS = boxes.xyxy
        CONFIDENCE = boxes.conf
        CLASS_ID = boxes.cls

        for i in range(len(XYXYS)):
            Object_Name = self.OBJECTS_LABEL[int(CLASS_ID[int(i)])]
            # Object_Name = CLASS_ID[i]
            x1,y1,x2,y2 = int(XYXYS[i][0]),int(XYXYS[i][1]),int(XYXYS[i][2]),int(XYXYS[i][3])
            Confidence = CONFIDENCE[i]
            # Object = {"Object_Class_Name":object_name,"x1":x1,"y1":y1,"x2":x2,'y2':y2,"Confidence":Confidence,'distance':distance}
            #Touched_Detect(hand_x1,hand_y1,hand_x2,hand_y2,hand_distance,x1,y1,x2,y2,distance)
            if( CurrentAction == "INDEX_DOUBLE_CLICK" ):
                if( HandPosX1 and self.ACTION.Touched_Object_Detect(HandPosX1,HandPosY1,HandPosX2,HandPosY2,x1,y1,x2,y2) ):
                    cv2.rectangle(frame,(x1,y1),(x2,y2),self.GREEN,2)
                     # cv2.putText(frame,object_name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.GREEN,2)
                    cv2.putText(frame,'cto: '+Object_Name,(350,150),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.BLUE,2 )
                    if( self.CURRENT_OBJECT_ANNOUNCEED == False):
                        self.SPEAK.Say(text=Object_Name)
                            # self.TTS.Say(text=object_name)
                        self.CURRENT_OBJECT_ANNOUNCEED = True            
                    else:
                        if(Object_Name in self.CASH_COUNTER.keys()):
                            self.CASH_COUNTER[Object_Name]+=1
                            print(self.CASH_COUNTER)
            cv2.rectangle(frame,(x1,y1),(x2,y2),self.GREEN,2)
            cv2.putText(frame,Object_Name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)
            # cv2.putText(frame,'current touched object '+"NONE",(1100,40),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.GREEN,2)



        
        return frame    
            # self.Current_Cash = self.CASH_COUNTER
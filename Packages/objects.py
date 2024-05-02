import torch
import cv2
from ultralytics import YOLO
from .action import Action
from .speak import Text_To_Voice
from .navigate import Navigate

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

        self.MONEY_STATE = {"AppearCount":0,"PreviousAppearTime":0}
        
        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.TARGET_OBJECT = []

        self.ACTION = Action()

        self.NAVIGATE = Navigate()

        self.SPEAK = Text_To_Voice()

        return

    def Objects_Model_fit( self,frame ):
        
        return self.OBJECTS_MODEL(frame)

    def ObjectDetect( self,frame,HandPosX1,HandPosY1,HandPosX2,HandPosY2,CurrentAction,Time ):

        RESULTS = self.Objects_Model_fit(frame)
        BOXES = RESULTS[0].boxes.cpu().numpy()
        XYXYS = BOXES.xyxy
        CONFIDENCE = BOXES.conf
        CLASS_ID = BOXES.cls

        MONEY_APPEARED = 0

        for i in range( len( XYXYS ) ):

            Object_Name = self.OBJECTS_LABEL[ int( CLASS_ID[ int(i) ] ) ]
            x1,y1,x2,y2 = int( XYXYS[i][0] ), int( XYXYS[i][1] ), int( XYXYS[i][2] ), int( XYXYS[i][3] ) 
            Confidence = CONFIDENCE[i]
            
            if( CurrentAction == "INDEX_DOUBLE_CLICK" ):
                
                if( HandPosX1 and self.ACTION.Touched_Object_Detect(HandPosX1,HandPosY1,HandPosX2,HandPosY2,x1,y1,x2,y2) ):
                    
                    cv2.putText(frame,'cto: '+Object_Name,(350,150),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.BLUE,2 )
                    
                    if( self.CURRENT_OBJECT_ANNOUNCEED == False and (Object_Name not in self.CASH_COUNTER.keys())):

                        self.SPEAK.Say(text=Object_Name)

                        self.CURRENT_OBJECT_ANNOUNCEED = True 
            
            if( Object_Name in self.TARGET_OBJECT ):
                
                self.NAVIGATE.NavigateProduct()
                                  
            if(Object_Name in self.CASH_COUNTER.keys()):

                self.CASH_COUNTER[Object_Name]+=1
                            
                if( MONEY_APPEARED !=1  and i >= ( len(XYXYS) - 1 ) ):  

                    if( Time - self.MONEY_STATE["PreviousAppearTime"] <= 3 or ( self.MONEY_STATE["AppearCount"] == 0 and self.MONEY_STATE["PreviousAppearTime"] == 0 ) ):

                        self.MONEY_STATE["AppearCount"] += 1

                        self.MONEY_STATE["PreviousAppearTime"] = Time
                                
                    elif( Time - self.MONEY_STATE["PreviousAppearTime"] > 3 ):
                                     
                        self.MONEY_STATE = {"AppearCount":0,"PreviousAppearTime":0}

                    if( self.MONEY_STATE["AppearCount"] >= 12):

                        print("SAY MONEY")
                                    
                        self.SPEAK.SayMoney(self.CASH_COUNTER)
                                    
                        self.MONEY_STATE = {"AppearCount":0,"PreviousAppearTime":0}

                    MONEY_APPEARED = 1

            cv2.rectangle(frame,(x1,y1),(x2,y2),self.GREEN,2)
            cv2.putText(frame,Object_Name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)
            cv2.putText(frame,str(Confidence),(x1,y1+20),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)

        self.CASH_COUNTER = {"hkd10":0,"hkd20":0,"hkd50":0,"hkd100":0,"hkd500":0,}
                
        return frame    

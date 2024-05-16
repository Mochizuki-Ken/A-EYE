import cv2
import torch
from ultralytics import YOLO

from .action import Action
from .speak import Text_To_Voice
from .navigate import Navigate
from .sound import Sound
from .voice import Voice
from .product import Product

class Objects():

    OBJECTS_MODEL_PT_FILE = "./Test/best-2.pt"

    OBJECTS_LABEL = ["薯片","粟米片","咖啡","衛生紙","牙膏","保温瓶","hkd10","hkd100","hkd20","hkd50","hkd500"]

    GREEN = (0, 255, 0) 
    RED = (0, 0, 255) 
    BLUE = (255, 0, 0) 
    FONT_SIZE = 0.75

    def __init__(self,Frame_Width,Frame_Height) -> None:

        device: str = "mps" if torch.backends.mps.is_available() else "cpu"

        self.OBJECTS_MODEL = YOLO(self.OBJECTS_MODEL_PT_FILE)

        self.OBJECTS_MODEL.to(device=device)

        self.ACTION_STATE = [0,0,0,"NONE","NONE"]

        self.CASH_COUNTER = {"hkd10":0,"hkd20":0,"hkd50":0,"hkd100":0,"hkd500":0,}

        self.MONEY_STATE = {"AppearCount":0,"PreviousAppearTime":0}
        
        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.PRODUCT = Product()

        self.ACTION = Action()

        self.NAVIGATE = Navigate(Frame_Width,Frame_Height)

        self.SPEAK = Text_To_Voice()

        self.VOICE = Voice()

        self.SOUND = Sound()

        self.FRAME_WIDTH = 0

        self.FRAME_HEIGHT = 0

        self.TIMER = 0

        return

    def Objects_Model_fit( self,frame ):
        
        return self.OBJECTS_MODEL(frame)
    
    def HandEvent(self,CurrentAction):

        if(CurrentAction == "INDEX_DOUBLE_CLICK" and self.CURRENT_OBJECT_ANNOUNCEED == False):

            self.SOUND.ThreadPlaySound("Note-1")

            Input_Text = self.VOICE.StartCantonese()

            # print(Input_Text)

            Voice_Result = self.VOICE.GetResponse(Input_Text)

            if( Voice_Result == "Want_To_Buy"):

                self.PRODUCT.FindProduct(Input_Text)

            elif( Voice_Result == "Cancel_Target"):

                self.PRODUCT.CancelFindProduct()

            elif( Voice_Result == "Discount"):

                self.PRODUCT.SayDiscount()

            elif( Voice_Result == "Current_Target"):

                self.PRODUCT.SayCurrentTargets

            else:

                self.SPEAK.ThreadSpeak(Voice_Result)
            

                
            self.SOUND.ThreadPlaySound("Note-1")

            self.CURRENT_OBJECT_ANNOUNCEED = True 


    def ObjectDetect( self,frame,ThumbX,ThumbY,IndexX,IndexY,CurrentAction,HandArea,Time ):

        self.NAVIGATE.TIMER = self.TIMER

        RESULTS = self.Objects_Model_fit(frame)
        BOXES = RESULTS[0].boxes.cpu().numpy()
        XYXYS = BOXES.xyxy
        CONFIDENCE = BOXES.conf
        CLASS_ID = BOXES.cls

        MONEY_APPEARED = 0

        Hand = True

        if( ThumbX == 0 and ThumbY == 0 and IndexX == 0 and IndexY == 0):
            Hand = False

        for i in range( len( XYXYS ) ):

            Object_Name = self.OBJECTS_LABEL[ int( CLASS_ID[ int(i) ] ) ]
            ObjX1,ObjY1,ObjX2,ObjY2 = int( XYXYS[i][0] ), int( XYXYS[i][1] ), int( XYXYS[i][2] ), int( XYXYS[i][3] ) 
            Confidence = CONFIDENCE[i]

            if(Object_Name == "粟米片") : continue

            HandPos = {"ThumbX":ThumbX,"ThumbY":ThumbY,"IndexX":IndexX,"IndexY":IndexY}
            ObjPos = {"ObjX1":ObjX1,"ObjY1":ObjY1,"ObjX2":ObjX2,"ObjY2":ObjY2}

            OBJECT_NAME = self.ACTION.Hold_Detection( Object_Name,HandPos,ObjPos,HandArea,self.TIMER)
            
            if (OBJECT_NAME): 

                if self.PRODUCT.CheckIfTargetObj(OBJECT_NAME) == False :
                    
                    self.SPEAK.Say( "呢個係" + OBJECT_NAME )

                    self.SOUND.ThreadPlaySound("Note-1")

            self.HandEvent(CurrentAction)

            print(self.PRODUCT.TARGET_PRODUCTS)

            
            if( Object_Name in self.PRODUCT.TARGET_PRODUCTS and Hand and Object_Name not in self.PRODUCT.FOUND_PRODUCTS): 

                self.PRODUCT.FOUND_PRODUCTS.append(Object_Name)

            if( len(self.PRODUCT.FOUND_PRODUCTS) >= 1 and i >= ( len(XYXYS) - 1 ) and self.PRODUCT.TARGET_PRODUCT == ""):

                self.PRODUCT.ChooseTargetProducts( Count = 1 )

                print("Object_Name in self.PRODUCT.TARGET_PRODUCT")

                self.PRODUCT.FOUND_PRODUCTS_POS[ self.PRODUCT.TARGET_PRODUCT ] = ObjPos

            if( self.PRODUCT.TARGET_PRODUCT != "" and Object_Name == self.PRODUCT.TARGET_PRODUCT):

                self.NAVIGATE.NavigateProduct(HandPos,ObjPos)

                                  
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

            cv2.rectangle(frame,(ObjX1,ObjY1),(ObjX2,ObjY2),self.GREEN,2)
            cv2.putText(frame,Object_Name,(ObjX1,ObjY1),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)
            cv2.putText(frame,str(Confidence),(ObjX1,ObjY1+20),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)

        self.CASH_COUNTER = {"hkd10":0,"hkd20":0,"hkd50":0,"hkd100":0,"hkd500":0,}
                
        return frame    

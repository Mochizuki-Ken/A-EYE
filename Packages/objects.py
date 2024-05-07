import cv2
import torch
from ultralytics import YOLO

from .action import Action
from .speak import Text_To_Voice
from .navigate import Navigate
from .sound import Sound
from .voice import Voice

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

        self.TARGET_OBJECTS = []

        self.FOUND_OBJECTS_POS ={}

        self.FOUND_OBJECTS = []

        self.TARGET_OBJECT = ""

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
    
    def CheckIfTargetObj(self,Object_Name):
        if( Object_Name == self.TARGET_OBJECT) : 

            del self.FOUND_OBJECTS_POS[Object_Name]
                            
            self.FOUND_OBJECTS.pop(self.FOUND_OBJECTS.index(Object_Name))

            self.TARGET_OBJECTS.pop(self.TARGET_OBJECTS.index(Object_Name))

            self.TARGET_OBJECT = ""    

            self.SPEAK.ThreadSpeak(text = f"搵到目標物品{Object_Name}")
                            
            self.SOUND.DoneSound()

            return True
        
        return False
    
    def ChooseTargetObject( self,Count = 1 ):

        if( len(self.FOUND_OBJECTS) == 1 ):

            self.TARGET_OBJECT = self.FOUND_OBJECTS[0]

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = f"搵到{self.TARGET_OBJECT}" )

            return self.TARGET_OBJECT
        
        elif ( Count <= 3):

            if( Count == 1):

                TEXT = f"搵到"

                for Obj in self.FOUND_OBJECTS:

                    TEXT += f"{Obj},"

                TEXT += "你想搵邊個先？"

            else:

                TEXT = "唔好意思聽唔清楚, 再講多次呀，唔該! 你想搵"

                for Obj in self.FOUND_OBJECTS:

                    TEXT += f"{Obj} 定係"
                
            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            UserInput = self.VOICE.StartCantonese()

            if( UserInput in self.FOUND_OBJECTS ) : 

                self.TARGET_OBJECT = UserInput

                return UserInput
            
            else :
                 
                self.ChooseTargetObject(Count+1)
            
        else:

            TEXT = "等我幫你揀啦! 我哋搵咗"

            TEXT += f"{self.FOUND_OBJECTS[0]} 先啦"

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.TARGET_OBJECT = self.FOUND_OBJECTS[0]

            return self.TARGET_OBJECT

        return
    
    def HandEvent(self,CurrentAction):

        if(CurrentAction == "INDEX_DOUBLE_CLICK" and self.CURRENT_OBJECT_ANNOUNCEED == False):

            self.SOUND.ThreadPlaySound("Note-1")

            Input_Text = self.VOICE.StartCantonese()

            print(Input_Text)

            if( Input_Text and ( Input_Text[:3] == "我想買" or Input_Text[:3] == "我想搵" ) ):
                
                if( Input_Text[3:] in self.TARGET_OBJECTS ):

                    self.SPEAK.ThreadSpeak("已經搵緊呢個物品")
                    
                elif( Input_Text[3:] in self.OBJECTS_LABEL):

                    self.TARGET_OBJECTS.append(Input_Text[3:])

                    self.SPEAK.ThreadSpeak(f"添加尋找物品{Input_Text[3:]}")

                    self.SOUND.ThreadPlaySound("Note-1")
            
            else :

                response = self.VOICE.GetResponse(Input_Text)

                self.SPEAK.ThreadSpeak(f"{response}")

                
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

                if ( not self.CheckIfTargetObj(OBJECT_NAME) ) :

                    self.SPEAK.Say(OBJECT_NAME)

            # if( CurrentAction == "INDEX_DOUBLE_CLICK" ):
                
            #     if( Hand and self.ACTION.Touched_Object_Detect(ThumbX,ThumbY,IndexX,IndexY,ObjX1,ObjY1,ObjX2,ObjY2) ):
                    
            #         cv2.putText(frame,'cto: '+Object_Name,(350,150),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.BLUE,2 )
                    
            #         if( self.CURRENT_OBJECT_ANNOUNCEED == False and (Object_Name not in self.CASH_COUNTER.keys())):

            #             self.SPEAK.Say(text=Object_Name)

            #             self.CURRENT_OBJECT_ANNOUNCEED = True 

            #             self.CheckIfTargetObj(Object_Name)

            self.HandEvent(CurrentAction)

            
            if( Object_Name in self.TARGET_OBJECTS and Hand and Object_Name not in self.FOUND_OBJECTS): 

                self.FOUND_OBJECTS.append(Object_Name)

            if( len(self.FOUND_OBJECTS) >= 1 and i >= ( len(XYXYS) - 1 ) and self.TARGET_OBJECT == ""):

                self.ChooseTargetObject( Count = 1 )

                print("Object_Name in self.TARGET_OBJECT")

                self.FOUND_OBJECTS_POS[ self.TARGET_OBJECT ] = ObjPos

            if( self.TARGET_OBJECT != "" and Object_Name == self.TARGET_OBJECT):

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

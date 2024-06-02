import math

from .AeyeMath import EYE_MATH
from .sound import Sound
from .speak import Text_To_Voice

from .Data import *

class Navigate():

    TargetSignSize = {
        "Width":100,
        "Height":100,
        "AcceptableError":50
    }
    
    LoccationsDict = {
        "Food":"食品區",
        "Daily":"日用品區"
    }

    Locations = {

        "Point1":{
            "Front":None,
            "Back":None,
            "Left":"Food",
            "Right":"Daily",
            "Targets":["Food","Daily"],
            "Distance":0
        },
        "Food":{
            "Front":None,
            "Back":"Daily",
            "Left":None,
            "Right":"Point1",
            "Targets":["Daily","Point1"],
            "Distance":10

        },
        "Daily":{
            "Front":None,
            "Back":"Food",
            "Left":None,
            "Right":"Poin1",
            "Targets":["Food","Point1"],
            "Distance":20
        }

    }
    
    def __init__(self,Frame_Width,Frame_Height) -> None:
        
        self.SOUND = Sound()

        self.SPEAK = Text_To_Voice()

        self.TIMER = 0

        self.SOUND_PLAY_STATE = {"LastPlayTime":0}

        self.CloseDistance = []

        self.CurrentLocation = ""

        self.TargetLocations = []

        self.TargetOnlyLocations = []

        self.IsOnCurrentLocation = False

        self.CurrentNavigateState = ["No Sign",0] # "Too Far" , "Too Close" ,"Arrived"

        self.IsOnTargetLocation = False

        self.CurrentSign = ["",{"Width":100000,"Height":100000},{"ErrorX":1000000,"ErrorY":1000000}]
        
        self.Frame_Width = Frame_Width

        self.Frame_Height = Frame_Height

        self.Navigating = False

        if( Frame_Width >= 1920 and Frame_Height >= 1080) :

            self.CloseDistance = [150,350,500]

        else :

            self.CloseDistance = [100,200,300]
        
        return
    
    def NavigateProduct(self,HandPos,ObjPos):

        ThumbX,ThumbY,IndexX,IndexY = HandPos["ThumbX"],HandPos["ThumbY"],HandPos["IndexX"],HandPos["IndexY"]

        ObjX1,ObjY1,ObjX2,ObjY2 = ObjPos["ObjX1"],ObjPos["ObjY1"],ObjPos["ObjX2"],ObjPos["ObjY2"]

        ObjMiddleX,ObjMiddleY = EYE_MATH.find_middle_pos(ObjX1,ObjY1,ObjX2,ObjY2)

        Distancs = math.hypot(IndexX - ObjMiddleX , IndexY - ObjMiddleY)

        if( Distancs <= self.CloseDistance[0] and ( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] ) >= 2 ):

            self.SOUND.ThreadPlaySound("Note-Fast")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

            print("<=150")
            

        elif( Distancs <= self.CloseDistance[1] and ( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] ) >= 4 ):

            self.SOUND.ThreadPlaySound("Note-Fast")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

            print("<=350")

        elif( Distancs <= self.CloseDistance[2] and ( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] ) >= 5 ):

            self.SOUND.ThreadPlaySound("Note-Fast-2")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

            print("<=500")

        elif ( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] ) >= 9 :

            self.SOUND.ThreadPlaySound("Note-Fast-3")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

            print("Object In")


    def FindPlace(self,Input_Text):

        for char in Input_Text:

            if "食" == char:
                self.TargetOnlyLocations.append("Food")
                self.TargetLocations.append("Food")
                return True
            elif "日" == char:
                self.TargetOnlyLocations.append("Daily")
                self.TargetLocations.append("Daily")
                return True
        self.SOUND.ThreadPlaySound("Error")
        self.SPEAK.ThreadSpeak("對唔住呀,搵唔到呢個區域")


    def FindCurrentFrontSign(self,SignName,SignPos):

        SignX1,SignY1,SignX2,SignY2 = SignPos["ObjX1"],SignPos["ObjY1"],SignPos["ObjX2"],SignPos["ObjY2"]

        MiddleX,MiddleY = EYE_MATH.find_middle_pos(SignX1,SignY1,SignX2,SignY2)
        
        Width,Height = SignX2 - SignX1 , SignY2 - SignY1

        ErrorX,ErrorY = abs((self.Frame_Width//2) - MiddleX) , abs((self.Frame_Height//2) - MiddleY)
        
        if ( ErrorX < self.CurrentSign[2]["ErrorX"] and  ErrorY < self.CurrentSign[2]["ErrorY"]) :

            self.CurrentSign = [SignName,{"Width":Width,"Height":Height},{"ErrorX":ErrorX,"ErrorY":ErrorY}]
        
        return

    def ShortProductsByLocations(self,TargetProductList):

        if TargetProductList == []:
            return []

        CloserLocationProductList = []

        FarLocationProductList = []

        if self.CurrentLocation == "" or (self.CurrentLocation == "Point1" and self.CurrentNavigateState[0] == "TooFar") :

            if( len(self.TargetLocations) == 0 or( len(self.TargetLocations) >= 1  and self.TargetLocations[0]!="Point1")):
            
                print(self.CurrentLocation)
                
                CloserLocationProductList.append("Point1")

                print("Point1 ADDED")


        for product in TargetProductList:

            print(product)

            if  self.Locations[PRODUCT_LIST[product]["Location"]]["Distance"] >= 20:

                FarLocationProductList.append(product)
            
            elif self.Locations[PRODUCT_LIST[product]["Location"]]["Distance"] >= 10:

                CloserLocationProductList.append(product)

        for i in FarLocationProductList:

            CloserLocationProductList.append(i)

        return CloserLocationProductList
    
    def UpdateTargetLocations(self,TargetProductList):

        if TargetProductList == [] or (len(self.TargetLocations)>=1 and self.TargetLocations[0] == "Point1"):

            self.TargetLocations = []

            return

        for product in TargetProductList:

            self.TargetLocations.append(PRODUCT_LIST[product]["Location"] )

        return TargetProductList
    
    def GetTargetAreaText(self):
        if(len(self.TargetLocations)>=1 and self.TargetLocations[0]!="Point1"):
            return LOC_CHI[self.TargetLocations[0]]
        elif(len(self.TargetLocations) >=2):
            if(self.TargetLocations[0]=="Point1"):
                return LOC_CHI[self.TargetLocations[1]]
            
        return "目標區域"

    def MoveFront(self,Text = ""):

        print("HI")

        if( not self.Navigating ) : 

            if(Text == "Point1" and len(self.TargetLocations)>1) : self.SPEAK.ThreadSpeak("導航會先帶你去中轉點然後前往目標區域, 導航開始")
            else : self.SPEAK.ThreadSpeak(f"導航會帶你前往{self.GetTargetAreaText()}, 導航開始")
            self.SOUND.ThreadPlaySound("Note-1")
            
            self.SPEAK.Say("請向前行直至音效提示")

            self.Navigating = True

        if( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] > 5) :

            print("front")
        
            self.SOUND.ThreadPlaySound("Note-Fast")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

    def MoveBack(self):

        if( not self.Navigating ) : 

            self.SPEAK.ThreadSpeak(f"導航會帶你前往{self.GetTargetAreaText()}, 導航開始")
            self.SOUND.ThreadPlaySound("Note-1")
            
            self.SPEAK.Say("請轉向後方然後前行直至音效提示")

            self.Navigating = True

        self.MoveFront()

    def MoveRight(self):

        if( not self.Navigating ) : 

            # self.SPEAK.ThreadSpeak("導航會帶你前往目標區域, 導航開始")
            self.SOUND.ThreadPlaySound("Note-1")
            
            self.SPEAK.Say("請轉向右方然後前行直至音效提示")

            self.Navigating = True

        self.MoveFront()

    def MoveLeft(self):

        if( not self.Navigating ) : 

            # self.SPEAK.ThreadSpeak("導航會帶你前往目標區域, 導航開始")
            self.SOUND.ThreadPlaySound("Note-1")
            
            self.SPEAK.Say("請轉向左方然後前行直至音效提示")

            self.Navigating = True

        self.MoveFront()

    def NavigateArea(self):

        # print("NA")

        # print(self.CurrentLocation)

        print("dddd-",self.TargetLocations)
        print(self.CurrentLocation)

        if len(self.TargetLocations) >1 and self.CurrentLocation == self.TargetLocations[1]:

            self.TargetLocations.pop(0)

        # print(self.CurrentNavigateState[0])

        if( self.CurrentLocation == "" and self.TargetLocations[0] == "Point1"):

            self.MoveFront(Text="Point1")

        elif( self.CurrentLocation == self.TargetLocations[0] and self.CurrentNavigateState[0] == "TooFar"):

            self.MoveFront()

        elif( self.CurrentLocation != "" and self.TargetLocations[0] == self.Locations[self.CurrentLocation]["Front"]):

            self.MoveFront()
        
        elif( self.CurrentLocation != "" and self.TargetLocations[0] == self.Locations[self.CurrentLocation]["Back"]):

            self.MoveBack()
        
        elif( self.CurrentLocation != "" and self.TargetLocations[0] == self.Locations[self.CurrentLocation]["Left"]):

            self.MoveLeft()
        
        elif( self.CurrentLocation != "" and self.TargetLocations[0] == self.Locations[self.CurrentLocation]["Right"]):

            self.MoveRight()

        return False
    
    def UpdateCurrentLocation(self):

        print(self.CurrentLocation)

        CurrentFrontSignName = self.CurrentSign[0]

        if(CurrentFrontSignName==""):return

        self.CurrentLocation = PRODUCT_LIST[CurrentFrontSignName]["Location"]

        Width = self.CurrentSign[1]["Width"]
        Height = self.CurrentSign[1]["Height"]

        if ( len(self.TargetLocations)>=1 and self.TargetLocations[0] == "Point1" and self.CurrentLocation != "Point1" and len(self.TargetLocations)>1 and self.CurrentLocation == self.TargetLocations[1]):
            
            self.TargetLocations.pop(0)

            if( self.Navigating ):

                self.Navigating = False

            print("dddddd",self.TargetLocations)

            return

        if( len(self.TargetLocations)>=1 and self.TargetLocations[0] == "Point1" and self.CurrentLocation != "Point1" and len(self.TargetLocations)>1 and self.CurrentLocation != self.TargetLocations[1]):

            self.TargetLocations.pop(0)

            self.IsOnCurrentLocation = True

            self.CurrentNavigateState = ["Arrived",0]

            if( self.Navigating ):

                self.Navigating = False

        # elif( len(self.TargetLocations)>=1 and self.IsOnCurrentLocation and self.CurrentLocation == self.TargetLocations[0] ):

        #     self.CurrentNavigateState = ["Arrived",0]

        #     self.IsOnCurrentLocation = True

        elif( abs(Width - PRODUCT_LIST[CurrentFrontSignName]["Width"]) <= PRODUCT_LIST[CurrentFrontSignName]["AcceptableError"] and abs(Height - PRODUCT_LIST[CurrentFrontSignName]["Height"]) <=  PRODUCT_LIST[CurrentFrontSignName]["AcceptableError"]):

            self.CurrentNavigateState = ["Arrived",0]

            self.IsOnCurrentLocation = True

        elif( Width - PRODUCT_LIST[CurrentFrontSignName]["Width"] < 0 and  Height - PRODUCT_LIST[CurrentFrontSignName]["Height"] < 0 ):
            
            self.CurrentNavigateState = ["TooFar",0]

            self.IsOnCurrentLocation = False

        else:

            self.CurrentNavigateState = ["TooClose",0]

            self.IsOnCurrentLocation = False
    
    def CheckIsArrivedLocation(self):

        if(len(self.TargetLocations)==0):

            return

        if( not self.IsOnTargetLocation and  self.CurrentLocation == self.TargetLocations[0] and self.CurrentNavigateState[0] == "Arrived" ):

            if( self.TargetLocations[0] == "Point1" ):

                self.TargetLocations.pop(0)

                self.Navigating = False

                self.IsOnTargetLocation = False

                return False
            
            if( len(self.TargetOnlyLocations) >= 1 ):

                Loc = self.TargetOnlyLocations.pop(0)

                self.TargetLocations.pop(0)

                self.Navigating = False

                self.IsOnTargetLocation = False

                Loc = self.LoccationsDict[Loc]

                self.SOUND.DoneSound()

                self.SPEAK.ThreadSpeak("到達目標區域"+Loc)

            self.IsOnTargetLocation = True

            self.Navigating = False

            self.SOUND.DoneSound()

            self.SPEAK.Say("到達目標區域"+self.LoccationsDict[self.TargetLocations[0]])

            return True
        
        elif(self.CurrentLocation != self.TargetLocations[0] ) :

            self.IsOnTargetLocation = False


            return False



        

        









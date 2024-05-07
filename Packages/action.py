import math
from .voice import Voice

class Action():
    def __init__(self) -> None:

        self.ACTION_STATE = [0,0,0,"NONE","NONE"]#[ click state 0 = up / 1 = down , last time , click count , active click type , Prev Finger]
        
        self.HOLD_ACTION_STATE = [0,0,""] # [ Time , count , obj name]

        self.CURRENT_OBJECT_ANNOUNCEED = False

        self.VOICE = Voice()

    def Touched_Object_Detect(self,hand_x1,hand_y1,hand_x2,hand_y2,object_x1,object_y1,object_x2,object_y2):

        hand_mid_pos_x,hand_mid_pos_y = min(hand_x1,hand_x2) + (abs(hand_x2-hand_x1)/2),min(hand_y1,hand_y2) + (abs(hand_y2-hand_y1)/2)

        
        if( hand_mid_pos_x < max(object_x1,object_x2) and hand_mid_pos_x > min(object_x1,object_x2) and hand_mid_pos_y < max(object_y1,object_y2)and hand_mid_pos_y > min(object_y1,object_y2) ):
            print(True)
            return True
        return False

    def ActionCheck(self,TIME):

        if(TIME-self.ACTION_STATE[1]>=12 and self.ACTION_STATE[1] != 0):

            self.ACTION_STATE=[0,0,0,"NONE","NONE"]

            self.CURRENT_OBJECT_ANNOUNCEED = False 

    def Hold_Detection(self,Object_Name,HandPos,ObjPos,HandArea,Timer):

        # self.HOLD_ACTION_STATE[2] = Object_Name
        if(HandArea ==0 ):
            return False

        ObjX1,ObjY1,ObjX2,ObjY2 = ObjPos["ObjX1"],ObjPos["ObjY1"],ObjPos["ObjX2"],ObjPos["ObjY2"]
        ThumbX,ThumbY,IndexX,IndexY = HandPos["ThumbX"],HandPos["ThumbY"],HandPos["IndexX"],HandPos["IndexY"]

        MiddleHandX = abs(IndexX + ThumbX) / 2
        MiddleHandY = abs(IndexY + ThumbY) / 2

        MiddleObjX = abs(ObjX2 + ObjX1) / 2
        MiddleObjY = abs(ObjY2 + ObjY1) / 2

        if(IndexX and IndexY <= 0 ):
            MiddleHandX = ThumbX
            MiddleHandY = ThumbY
        elif( ThumbX and ThumbY <= 0 ):
            MiddleHandX = IndexX
            MiddleHandY = IndexY

        width = abs(ObjX2 - ObjX1)
        height = abs(ObjY2 - ObjY1)
        area = width * height

        if ( area <= 0 ): return False

        if( self.HOLD_ACTION_STATE[0]!=0 and Timer - self.HOLD_ACTION_STATE[0] >= 10):

            self.HOLD_ACTION_STATE = [0,0,""]

            return False
        
        if( max(HandArea,area)/min(HandArea,area) <= 1.3  or HandArea < area):

            print("abs(HandArea - area) <= 300")

            print(ThumbX,ThumbY)

            if( self.Touched_Object_Detect(ThumbX,ThumbY,IndexX,IndexY,ObjX1,ObjY1,ObjX2,ObjY2)):

                print("Hand Match Obj")

                if( self.HOLD_ACTION_STATE[1] >= 3): #2

                    self.HOLD_ACTION_STATE = [0,0,""]

                    return Object_Name

                elif( self.HOLD_ACTION_STATE[0] == 0 ):

                    self.HOLD_ACTION_STATE[0] = Timer
                    self.HOLD_ACTION_STATE[1] += 1
                    self.HOLD_ACTION_STATE[2] = Object_Name

                elif( Timer - self.HOLD_ACTION_STATE[0] and self.HOLD_ACTION_STATE[2] == Object_Name): 

                    self.HOLD_ACTION_STATE[1] += 1

        return False
    

    def DoubleClick_Detection(self,HandArea,ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY,TIME):

        if(self.ACTION_STATE[3]!="NONE"):

            return False
        
        Current_Finger = {"Finger":0,"Distance":0}
        
        Index_Distance = math.hypot(IndexX - ThumbX,IndexY - ThumbY)
        Middle_Distance = math.hypot(MiddleX - ThumbX,MiddleY - ThumbY)

        if( Index_Distance < Middle_Distance):

            Current_Finger["Finger"] = "Index"
            Current_Finger["Distance"] = Index_Distance

        else:

            Current_Finger["Finger"] = "Middle"
            Current_Finger["Distance"] = Middle_Distance

        # print(HandArea/300 - 200)

        #45

        if( Current_Finger["Distance"] <= 45 and ( (Current_Finger["Finger"] == "Index" and ThumbY>IndexY) or (Current_Finger["Finger"] == "Middle" and ThumbY>MiddleY) ) ):
            
            if(self.ACTION_STATE[2]>=1):

                if(self.ACTION_STATE[4] == "Index" and Current_Finger["Finger"] == "Index"):

                    self.ACTION_STATE=[0,TIME,0,"INDEX_DOUBLE_CLICK","NONE"]

                elif(self.ACTION_STATE[4] == "Middle" and Current_Finger["Finger"] == "Middle"):

                    self.ACTION_STATE=[0,TIME,0,"MIDDLE_DOUBLE_CLICK","NONE"]

                elif(self.ACTION_STATE[4] == "Index" and Current_Finger["Finger"] == "Middle"):

                    self.ACTION_STATE=[0,TIME,0,"INDEX_MIDDLE_DOUBLE_CLICK","NONE"]

                elif(self.ACTION_STATE[4] == "Middle" and Current_Finger["Finger"] == "Index"):

                    self.ACTION_STATE=[0,TIME,0,"MIDDLE_INDEX_DOUBLE_CLICK","NONE"]

                self.CURRENT_OBJECT_ANNOUNCEED=0

                print(self.ACTION_STATE)

                return

            if(self.ACTION_STATE[0]==0):

                self.ACTION_STATE[0] = 1

                self.ACTION_STATE[4] = Current_Finger["Finger"] 

        # print(HandArea/100)

        elif (Current_Finger["Distance"] >= HandArea / 400 ):

            if(self.ACTION_STATE[0]==1):

                self.ACTION_STATE[0]=0

                self.ACTION_STATE[1]=TIME

                self.ACTION_STATE[2]+=1      
                

        print(self.ACTION_STATE)
    
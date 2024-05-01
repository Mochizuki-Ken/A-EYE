import math
from .voice import Voice
class Action():
    def __init__(self) -> None:
        self.ACTION_STATE = [0,0,0,"NONE","NONE"]#[ click state 0 = up / 1 = down , last time , click count , active click type , Prev Finger]
        self.CURRENT_OBJECT_ANNOUNCEED = False
        self.VOICE = Voice()

    def Touched_Object_Detect(self,hand_x1,hand_y1,hand_x2,hand_y2,object_x1,object_y1,object_x2,object_y2):
        hand_mid_pos_x,hand_mid_pos_y = min(hand_x1,hand_x2)+(abs(hand_x2-hand_x1)/2),min(hand_y1,hand_y2)+(abs(hand_y2-hand_y1)/2)
        if(hand_mid_pos_x < max(object_x1,object_x2) and hand_mid_pos_x > min(object_x1,object_x2) and hand_mid_pos_y < max(object_y1,object_y2)and hand_mid_pos_y > min(object_y1,object_y2)):
            return True
        return False

    def ActionCheck(self,TIME):
        if(TIME-self.ACTION_STATE[1]>=12 and self.ACTION_STATE[1] != 0):
            self.ACTION_STATE=[0,0,0,"NONE","NONE"]
            self.CURRENT_OBJECT_ANNOUNCEED = False 

    def DoubleClick_Detection(self,ThumbX,ThumbY,IndexX,IndexY,MiddleX,MiddleY,TIME):
        # if(self.Timer-self.ACTION_STATE[1]>=12 and self.ACTION_STATE[1] != 0):
        #     self.ACTION_STATE=[0,0,0,"NONE"]
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

        if( Current_Finger["Distance"] <= 40 and ( (Current_Finger["Finger"] == "Index" and ThumbY>IndexY) or (Current_Finger["Finger"] == "Middle" and ThumbY>MiddleY) ) ):
            if(self.ACTION_STATE[2]>=1):
                if(self.ACTION_STATE[4] == "Index" and Current_Finger["Finger"] == "Index"):
                    self.ACTION_STATE=[0,TIME,0,"INDEX_DOUBLE_CLICK","NONE"]

                elif(self.ACTION_STATE[4] == "Middle" and Current_Finger["Finger"] == "Middle"):
                    self.ACTION_STATE=[0,TIME,0,"MIDDLE_DOUBLE_CLICK","NONE"]
                    self.VOICE.StartMic()


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
        else:
            if(self.ACTION_STATE[0]==1):
                self.ACTION_STATE[0]=0
                self.ACTION_STATE[1]=TIME
                self.ACTION_STATE[2]+=1      
                
            

        # fingers_distance = math.hypot(x2 - x1, y2 - y1)
        # if(fingers_distance <=40 and y2<y1 ):
                
        #     if(self.ACTION_STATE[0]==0):
        #             self.ACTION_STATE[0]=1
        # else:
        #     if(self.ACTION_STATE[0]==1):
        #         self.ACTION_STATE[0]=0
        #         self.ACTION_STATE[1]=TIME
        #         self.ACTION_STATE[2]+=1      
                
        #     if(self.ACTION_STATE[2]>=2):
        #         self.ACTION_STATE=[0,TIME,0,"DOUBLE_CLICK"]
        #         self.CURRENT_OBJECT_ANNOUNCEED=0
        print(self.ACTION_STATE)
    
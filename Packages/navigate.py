import math

from .AeyeMath import EYE_MATH
from .sound import Sound

class Navigate():
    
    def __init__(self,Frame_Width,Frame_Height) -> None:
        
        self.SOUND = Sound()

        self.TIMER = 0

        self.SOUND_PLAY_STATE = {"LastPlayTime":0}

        self.CloseDistance = []

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

        elif ( self.TIMER - self.SOUND_PLAY_STATE["LastPlayTime"] ) >= 7 :

            self.SOUND.ThreadPlaySound("Note-Fast-3")

            self.SOUND_PLAY_STATE["LastPlayTime"] = self.TIMER

            print("Object In")
    
    def NavigateArea(self):
        return
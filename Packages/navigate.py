from .sound import Sound
import math

class Navigate():
    
    def __init__(self) -> None:
        
        self.SOUND = Sound()
        
        return
    
    def FindMiddlePos(self,ObjX1,ObjY1,ObjX2,ObjY2):

        X = ( ObjX1 + ObjX2 ) /2
        Y = ( ObjY1 + ObjY2 ) /2

        return X,Y
    
    def NavigateProduct(self,HandPos,ObjPos):

        ThumbX,ThumbY,IndexX,IndexY = HandPos["ThumbX"],HandPos["ThumbY"],HandPos["IndexX"],HandPos["IndexY"]

        ObjX1,ObjY1,ObjX2,ObjY2 = ObjPos["ObjX1"],ObjPos["ObjY1"],ObjPos["ObjX2"],ObjPos["ObjY2"]

        ObjMiddleX,ObjMiddleY = self.FindMiddlePos(ObjX1,ObjY1,ObjX2,ObjY2)

        Distancs = math.hypot(IndexX - ObjMiddleX , IndexY - ObjMiddleY)

        if( Distancs <= 50):

            self.SOUND.Play("Note-Fast",0.2,2)

        elif( Distancs <= 100 ):

            self.SOUND.Play("Note-Fast",0.4,2)

        elif( Distancs <= 200):

            self.SOUND.Play("Note-Fast-2",0.5,2)

        else:

            self.SOUND.Play("Note-Fast-3",0.8,2)
        
        # Result = True
        
        # if( Result ):
        #     self.SOUND.DoneSound()
        # return
    
    def NavigateArea(self):
        return
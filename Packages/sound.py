from playsound import playsound
import time

class Sound():
    
    SOUNDS_PATH = {
    	"Noteflight-1":"/path",
        "Done":"/path"
    }
    
    def __init__(self) -> None:
        
        return 
        
    def DoneSound(self):
        
        playsound( self.SOUNDS_PATH["Done"] )
        
        return 
        
    def Play(self,Type,Rate,LoopType):
        
        if( Type not in self.SOUNDS_PATH.keys() ):
            
            return "error-No Type"
                
        for i in LoopType:
            
            playsound(self.SOUNDS_PATH[Type])
            
            time.wait(rate)
        
        return
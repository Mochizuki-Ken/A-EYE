from .sound import Sound

class Navigate():
    
    def __init__(self) -> None:
        
        self.SOUND = Sound()
        
        return
    
    def NavigateProduct(self):
        
        Result = True
        
        if( Result ):
            self.SOUND.DoneSound()
        return
    
    def NavigateArea(self):
        return
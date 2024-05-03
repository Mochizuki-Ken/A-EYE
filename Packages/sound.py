from playsound import playsound
import time
import asyncio
import threading

class Sound():
    
    SOUNDS_PATH = {
    	"Note-1":"./Media/Sound/Note1.mp3",
        "Note-2":"./Media/Sound/Note2.mp3",
        "Note-Fast":"./Media/Sound/NoteFast.mp3",
        "Note-Fast-2":"./Media/Sound/NoteFast.mp3",
        "Note-Fast-3":"./Media/Sound/NoteFast.mp3",
        "Done":"./Media/Sound/Done.mp3",
        "Error":"./Media/Sound/Error.mp3",
    }
    
    def __init__(self) -> None:

        self.TIME = 0
        
        return 
        
    def DoneSound(self):
        
        playsound( self.SOUNDS_PATH["Done"] )
        
        return 
        
    async def Play(self,Type,Speed,LoopType):
        
        if( Type not in self.SOUNDS_PATH.keys() ):
            
            return "error-No Type"
                
        for i in LoopType:
            
            threading.Thread(target=playsound, args=('./Media/Sound/song_fast.mp3',), daemon=True).start()

            await asyncio.sleep(Speed)

        return
    

# asyncio.run(p())



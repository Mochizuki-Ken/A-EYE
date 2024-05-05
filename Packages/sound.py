import threading

from playsound import playsound

class Sound():
    
    SOUNDS_PATH = {
    	"Note-1":"Media/Sound/Note1.mp3",
        "Note-2":"Media/Sound/Note2.mp3",
        "Note-Fast":"Media/Sound/NoteFast.mp3",
        "Note-Fast-2":"Media/Sound/NoteFast.mp3",
        "Note-Fast-3":"Media/Sound/NoteFast.mp3",
        "Done":"Media/Sound/Done.mp3",
        "Error":"Media/Sound/Error.mp3",
    }
    
    def __init__(self) -> None:

        self.TIME = 0
        
        return 
        
    def DoneSound(self):
        
        PATH = str(self.SOUNDS_PATH["Done"])
        
        threading.Thread(target=playsound, args=(PATH,), daemon=True).start()
        
        return 
    
    def ThreadPlaySound(self,Type):

        PATH = str(self.SOUNDS_PATH[Type])
        
        threading.Thread(target=playsound, args=(PATH,), daemon=True).start()

        return
   
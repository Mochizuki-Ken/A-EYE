from .speak import Text_to_Voice
from .sound import Sound
from .Data import *

class Product():
    
    def __init__(self) -> None:
        
        self.SOUND = Sound()
        
        self.SPEAK = Text_to_Voice()
        
        self.TARGET_PRODUCTS = []
        
        self.FOUND_PRODUCTS = []
        
        pass
        
    def ChooseTargetProducts( self,Count = 1 ):

        if( len(self.FOUND_PRODUCTS) == 1 ):

            self.TARGET_PRODUCTS = self.FOUND_PRODUCTS[0]

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = f"搵到{self.TARGET_OBJECT}" )

            return self.TARGET_PRODUCTS
        
        elif ( Count <= 3):

            if( Count == 1):

                TEXT = f"搵到"

                for Obj in self.FOUND_PRODUCTS:

                    TEXT += f"{Obj},"

                TEXT += "你想搵邊個先？"

            else:

                TEXT = "唔好意思聽唔清楚, 再講多次呀，唔該! 你想搵"

                for Obj in self.FOUND_PRODUCTS:

                    TEXT += f"{Obj} 定係"
                
            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            UserInput = self.VOICE.StartCantonese()
            
            

            if( UserInput in self.FOUND_PRODUCTS ) : 

                self.TARGET_PRODUCTS = UserInput

                return UserInput
            
            else :
                 
                self.ChooseTargetObject(Count+1)
            
        else:

            TEXT = "等我幫你揀啦! 我哋搵咗"

            TEXT += f"{self.FOUND_PRODUCTS[0]} 先啦"

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.TARGET_PRODUCTS = self.FOUND_PRODUCTS[0]

            return self.TARGET_PRODUCTS

        return False
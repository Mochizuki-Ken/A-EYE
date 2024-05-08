# def CheckIfTargetObj(self,Object_Name):
    #     if( Object_Name == self.TARGET_OBJECT) : 

    #         del self.FOUND_OBJECTS_POS[Object_Name]
                            
    #         self.FOUND_OBJECTS.pop(self.FOUND_OBJECTS.index(Object_Name))

    #         self.TARGET_OBJECTS.pop(self.TARGET_OBJECTS.index(Object_Name))

    #         self.TARGET_OBJECT = ""    

    #         self.SPEAK.ThreadSpeak(text = f"搵到目標物品{Object_Name}")
                            
    #         self.SOUND.DoneSound()

    #         return True
        
    #     return False
    
    # def ChooseTargetObject( self,Count = 1 ):

    #     if( len(self.FOUND_OBJECTS) == 1 ):

    #         self.TARGET_OBJECT = self.FOUND_OBJECTS[0]

    #         self.SOUND.ThreadPlaySound( Type = "Note-1")

    #         self.SPEAK.Say( text = f"搵到{self.TARGET_OBJECT}" )

    #         return self.TARGET_OBJECT
        
    #     elif ( Count <= 3):

    #         if( Count == 1):

    #             TEXT = f"搵到"

    #             for Obj in self.FOUND_OBJECTS:

    #                 TEXT += f"{Obj},"

    #             TEXT += "你想搵邊個先？"

    #         else:

    #             TEXT = "唔好意思聽唔清楚, 再講多次呀，唔該! 你想搵"

    #             for Obj in self.FOUND_OBJECTS:

    #                 TEXT += f"{Obj} 定係"
                
    #         self.SOUND.ThreadPlaySound( Type = "Note-1")

    #         self.SPEAK.Say( text = TEXT )

    #         self.SOUND.ThreadPlaySound( Type = "Note-1")

    #         UserInput = self.VOICE.StartCantonese()

    #         if( UserInput in self.FOUND_OBJECTS ) : 

    #             self.TARGET_OBJECT = UserInput

    #             return UserInput
            
    #         else :
                 
    #             self.ChooseTargetObject(Count+1)
            
    #     else:

    #         TEXT = "等我幫你揀啦! 我哋搵咗"

    #         TEXT += f"{self.FOUND_OBJECTS[0]} 先啦"

    #         self.SOUND.ThreadPlaySound( Type = "Note-1")

    #         self.SPEAK.Say( text = TEXT )

    #         self.SOUND.ThreadPlaySound( Type = "Note-1")

    #         self.TARGET_OBJECT = self.FOUND_OBJECTS[0]

    #         return self.TARGET_OBJECT

    #     return




# if( CurrentAction == "INDEX_DOUBLE_CLICK" ):
                
            #     if( Hand and self.ACTION.Touched_Object_Detect(ThumbX,ThumbY,IndexX,IndexY,ObjX1,ObjY1,ObjX2,ObjY2) ):
                    
            #         cv2.putText(frame,'cto: '+Object_Name,(350,150),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.BLUE,2 )
                    
            #         if( self.CURRENT_OBJECT_ANNOUNCEED == False and (Object_Name not in self.CASH_COUNTER.keys())):

            #             self.SPEAK.Say(text=Object_Name)

            #             self.CURRENT_OBJECT_ANNOUNCEED = True 

            #             self.CheckIfTargetObj(Object_Name)
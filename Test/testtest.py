for i in result:
            object_name = self.detection.Daily_Objects_List[int(i[5])]
            x1,y1,x2,y2 = int(i[0]) , int(i[1]) , int(i[2]) , int(i[3])
            Confidence  =  int(i[4])

            # distance = self.measureDistance.MeasureDistance(object_name,[x1,x2])
            # if(distance!=False):
            #     distance=int(distance)
            # else:
            if True:
                distance = "NO TYPE"
                Object = {"Object_Class_Name":object_name,"x1":x1,"y1":y1,"x2":x2,'y2':y2,"Confidence":Confidence,'distance':distance}
                if( len(i) > 0 ):
                    #Touched_Detect(hand_x1,hand_y1,hand_x2,hand_y2,hand_distance,x1,y1,x2,y2,distance)
                    if( self.click_motion_state[3] == "DOUBLE_CLICK" ):
                        if( HandPosX1 and self.ACTION.Touched_Object_Detect(HandPosX1,HandPosY1,HandPosX2,HandPosY2,x1,y1,x2,y2) ):
                            cv2.rectangle(frame,(x1,y1),(x2,y2),self.GREEN,2)
                             # cv2.putText(frame,object_name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.GREEN,2)
                            cv2.putText(frame,'cto: '+object_name,(350,150),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.BLUE,2 )
                            if( self.CURRENT_OBJECT_ANNOUNCEED == False):
                                self.ThreadSpeck(text=object_name)
                            # self.TTS.Say(text=object_name)
                            self.CURRENT_OBJECT_ANNOUNCEED = True
                                        
                    else:
                        if(object_name in self.CASH_COUNTER.keys()):
                            self.CASH_COUNTER[object_name]+=1
                                        
                        cv2.rectangle(frame,(x1,y1),(x2,y2),self.GREEN,2)
                        cv2.putText(frame,object_name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,0.6,self.GREEN,2)
                        cv2.putText(frame,'current touched object '+"NONE",(1100,40),cv2.FONT_HERSHEY_COMPLEX ,self.FONT_SIZE,self.GREEN,2)
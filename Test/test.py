import cv2

# detection = DETECTION()

cap = cv2.VideoCapture("http://192.168.0.23:5000/stream") 
  
GREEN = (0, 255, 0) 

while True: 
    _, frame = cap.read() 

    # if(frame is not None):
   
    #     result = detection.detect_Daily_Objects(frame) 

    #     for i in result:
    #         if(len(i)>0):
    #             cv2.rectangle(frame,(int(i[0]),int(i[1])),(int(i[2]),int(i[3])),GREEN,2)
    #             cv2.putText(frame,detection.Daily_Objects_List[int(i[5])],(int(i[0]),int(i[1])),cv2.FONT_HERSHEY_COMPLEX ,0.6,GREEN,2)

    cv2.imshow("frame", frame) 
    # else : break
  
    if cv2.waitKey(1) == ord("q"): 
        break
  
cap.release() 
  
cv2.destroyAllWindows() 

# img = cv2.imread('./example.jpg')
# detection.detect_Daily_Objects(img)

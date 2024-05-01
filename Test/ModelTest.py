import cv2
import torch
from ultralytics import YOLO

Model_Path = './Test/best.pt'

# Model = torch.hub.load('ultralytics/yolov5',"custom",path=Model_Path)
device: str = "mps" if torch.backends.mps.is_available() else "cpu"

Model = YOLO(Model_Path)

Model.to(device=device)

Video_Input = 0 #"http://172.20.10.11:5000/video_feed"

cap = cv2.VideoCapture(Video_Input) 
  
GREEN = (0, 255, 0) 

Objects = ["Cola","CornFlakes","PotatoChips","Tempo","ToothPaste","apple","banana","Bottle-water","hkd10","hkd100","hkd20","hkd50","hkd500","hkd1000","orange"]


while True: 
    _, frame = cap.read() 

    # if(frame is not None):
   
    #     result = detection.detect_Daily_Objects(frame) 

    #     for i in result:
    #         if(len(i)>0):
    #             cv2.rectangle(frame,(int(i[0]),int(i[1])),(int(i[2]),int(i[3])),GREEN,2)
    #             cv2.putText(frame,detection.Daily_Objects_List[int(i[5])],(int(i[0]),int(i[1])),cv2.FONT_HERSHEY_COMPLEX ,0.6,GREEN,2)

    # cv2.imshow("frame", frame) 

    results = Model.predict(frame,conf=0.6)
    # ModelResult = ModelResult.pandas().xyxy[0][['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']].values

    boxes = results[0].boxes.cpu().numpy()

    XYXYS = boxes.xyxy
    CONFIDENCE = boxes.conf
    CLASS_ID = boxes.cls

    # for result in results:
    #     boxes = result[0].boxes.cpu().numpy()
    #     XYXYS=(boxes.xyxy)
    #     CONFIDENCE=(boxes.conf)
    #     CLASS_ID=(boxes.cls)
    
    print(XYXYS,CLASS_ID,CONFIDENCE)


    for i in range(len(XYXYS)):
        Object_Name = Objects[int(CLASS_ID[int(i)])+1]
        # Object_Name = CLASS_ID[i]
        x1,y1,x2,y2 = int(XYXYS[i][0]),int(XYXYS[i][1]),int(XYXYS[i][2]),int(XYXYS[i][3])
        Confidence = CONFIDENCE[i]
            
        cv2.rectangle(frame,(x1,y1),(x2,y2),GREEN,2)
        cv2.putText(frame,Object_Name,(x1,y1),cv2.FONT_HERSHEY_COMPLEX ,0.6,GREEN,2)


    cv2.imshow("",frame)

    # else : break
  
    if cv2.waitKey(1) == ord("q"): 
        break
  
cap.release() 
  
cv2.destroyAllWindows() 
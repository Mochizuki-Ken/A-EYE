import cv2
import numpy as np
# detection = DETECTION()

cap = cv2.VideoCapture("udp://192.168.0.125:1234") 

# cap = cv2.VideoCapture(0) 

GREEN = (0, 255, 0) 


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

while True: 
    _, frame = cap.read() 

    # if(frame is not None):
   
    #     result = detection.detect_Daily_Objects(frame) 

    #     for i in result:
    #         if(len(i)>0):
    #             cv2.rectangle(frame,(int(i[0]),int(i[1])),(int(i[2]),int(i[3])),GREEN,2)
    #             cv2.putText(frame,detection.Daily_Objects_List[int(i[5])],(int(i[0]),int(i[1])),cv2.FONT_HERSHEY_COMPLEX ,0.6,GREEN,2)

    # frame = rotate_image(frame,90)
    cv2.imshow("frame", frame) 
    # else : break
  
    if cv2.waitKey(1) == ord("q"): 
        break
  
cap.release() 
  
cv2.destroyAllWindows() 

# img = cv2.imread('./example.jpg')
# detection.detect_Daily_Objects(img)

# raspivid -o - -t 0 -w 400 -h 200 -fps 20 -b 7000000 | ffmpeg -i - -c copy -f mpegts udp://192.168.0.125:1234

import cv2
import numpy as np 
import math 
from object_detection import ObjectDetection
from matplotlib import pyplot as plt 

od = ObjectDetection()
cap = cv2.VideoCapture("traffic6.mp4")
count = 0
center_pts_prev = []
track_id=0
tracking_obj = {}

while True:  
    ret,frame = cap.read()
    count += 1
    if not ret:
        break
    center_pts_cur = []

    #detect objects in frame
    (class_id , scores , boxes) = od.detect(frame)
    for box in boxes:
        (x,y,w,h)=box
        cx = int((x+x+w)/2)
        cy = int((y+y+h)/2)
        center_pts_cur.append((cx,cy))

        print("frame no" , count , " " , x,y,w,h)

        cv2.rectangle(frame , (x,y) , (x+w,y+h) , (0,255,0) , 2)
      


        if count<=2:
           for pt in center_pts_cur:
            for pt2 in center_pts_prev:
              distance =  math.hypot(pt2[0]-pt[0] , pt2[1]-pt[1])

              if distance < 20:
                  tracking_obj[track_id] = pt
                  track_id+=1

        else:
             tracking_obj_copy = tracking_obj.copy()
             for obj_id ,pt2 in tracking_obj_copy.items():
                 obj_exists = False
                 for pt in center_pts_cur:
                      distance =  math.hypot(pt2[0]-pt[0] , pt2[1]-pt[1])
                      if distance<20:
                          tracking_obj[obj_id]=pt
                          obj_exists=True
                          continue
             if not obj_id:
                 tracking_obj.pop(obj_id)



        for obj_id,pt in tracking_obj.items():
            cv2.circle(frame , (cx,cy) , 3 , (0,0,255) , -1)
                


                  
    print("tracking objects")
    print(tracking_obj)
    print("current frame")
    print(center_pts_cur)
    print("previous frame")
    print(center_pts_prev)
    cv2.imshow("Frame",frame)
    center_pts_prev = center_pts_cur.copy()
    key =  cv2.waitKey(1) 
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

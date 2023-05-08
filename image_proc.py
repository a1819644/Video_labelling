from ultralytics import YOLO
import cv2
import supervision 
import pandas as pd

def main():
    path = r"my_video_frame.png"

    image = cv2.imread(path, 0)
    
    start_point = (1178,2)

    end_point = (1532, 935)
    
    color = (255, 0, 100)
    
    window_name = 'image'
    
    centx = int((1178+1532)/2)
    centy = int((2+935)/2)
    print(centx,centy)
    
    
    # image = cv2.rectangle(image, start_point, end_point,color,2)
    image = cv2.circle(image, (centx,centy), radius=0, color=color, thickness=4)

    cv2.imshow(window_name, image)
    
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    
    # closing all open windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    columns_name = []
    row_name = []
    labels_tracker_id = []
    labels_tracker_class_name=[]
    labels_tracker_bbox = []
    main()

    

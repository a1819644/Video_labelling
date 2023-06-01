from ultralytics import YOLO
import cv2
import supervision 
import pandas as pd
import os
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import create_distance_analysis as create_distance_analysis
import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os
# import create_detect_movements as create_detect_movements




def main():
    model = YOLO("yolov8s.pt") # load the model
    
    # using the box annotator from the supervision 
    box_annotator = supervision.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale= 0.5
    )


    #track the results and show = 0 means the camera opening return the frames
    for result in model.track(source="people_watchingbirds.mp4", show=True, iou=0.5, stream=True):
        frame = result.orig_img
        # print(result.boxes.data)
        print(model.names)

        # lets store the frames in the supervision to do all the trackin things
        detections = supervision.Detections.from_yolov8(result)
        
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        


        labels = [
            f"{xyxy}{tracker_id} {model.model.names[class_id]} {confidence: 0.2f}"
            for xyxy,_,confidence,class_id,tracker_id,
            in detections
        ]
        print(labels)

        #based on the tracking_ids i need to add the 
        creating_dataframe(model, detections)
        # 
        # print(tracker_id, "   ",xyxy, "  ", class_id)
        # passing the bounding box _annotator to the frame
        
        
        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        cv2.imshow("yolov8",frame) # to pring the curr frame on the screen

        if(cv2.waitKey(30)  == 27): # kill the run 
            break

def creating_dataframe(model, detections):

    temp_tracker_id = [
            tracker_id
            for _,_,_,_,tracker_id,
            in detections
        ]
    labels_tracker_id.append(temp_tracker_id)
    temp_tracker_class_name = [
            model.model.names[class_id]
            for _,_,_,class_id,_,
            in detections
        ]
    labels_tracker_class_name.append(temp_tracker_class_name)
    temp_tracker_bboxe = [
            xyxy
            for xyxy,_,_,_,_,         
            in detections
        ]
    labels_tracker_bbox.append(temp_tracker_bboxe)
    
    #creating another df for the distance calculation purposes
    df_for_meassurements = pd.DataFrame(columns=columns_name, index=row_name)
    for _,_,_,class_id,tracker_id in detections:
        columns_name.append(model.model.names[class_id])
        row_name.append(tracker_id)
    df_for_meassurements.to_csv("calculation_dis.csv")
    print(df_for_meassurements)


    creating_dframe = pd.DataFrame({"tracker_ids":labels_tracker_id,
                                    "tracker_class_name":labels_tracker_class_name,
                                    "bounding_boxes":labels_tracker_bbox} )
    creating_dframe.to_csv("create_dframe.csv")
    return creating_dframe
        


def add_new_track_id(found_tracking_ids, detections):
    for i in detections.tracker_id.tolist():
        found_tracking_ids.add(i)
        


if __name__ == "__main__":
    columns_name = []
    row_name = []
    labels_tracker_id = []
    labels_tracker_class_name=[]
    labels_tracker_bbox = []
    main()

    # calling create_detect_movements_py file   
    with open("create_detect_movements.py") as create_detect_movements:
        exec(create_detect_movements.read())

    # calling create_distance_analysis.py file   
    with open("create_distance_analysis.py") as create_distance_analysis:
        exec(create_distance_analysis.read())
        
    # calling create_distance_analysis.py file   
    with open("analyse_movements.py") as analyse_movements:
        exec(analyse_movements.read())

    

    

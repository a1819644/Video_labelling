from ultralytics import YOLO
import cv2
import supervision 
import pandas as pd


def main():
    model = YOLO("yolov8s.pt") # load the model
    
    # using the box annotator from the supervision 
    box_annotator = supervision.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale= 0.5
    )


    #track the results and show = 0 means the camera opening return the frames
    for result in model.track(source="two_p.mp4", show=True, iou=0.5, stream=True):
        frame = result.orig_img

        # lets store the frames in the supervision to do all the trackin things
        detections = supervision.Detections.from_yolov8(result)
        
        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)
        


        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence: 0.2f}"
            for _,_,confidence,class_id,tracker_id,
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
            f"{tracker_id}"
            for _,_,_,_,tracker_id,
            in detections
        ]
    labels_tracker_id.append(temp_tracker_id)
    temp_tracker_class_name = [
            f"{model.model.names[class_id]}"
            for _,_,_,class_id,_,
            in detections
        ]
    labels_tracker_class_name.append(temp_tracker_class_name)
    temp_tracker_bboxe = [
            f"{xyxy}"
            for xyxy,_,_,_,_,
            in detections
        ]
    labels_tracker_bbox.append(temp_tracker_bboxe)
    creating_dframe = pd.DataFrame({"tracker_ids":labels_tracker_id,
                                    "tracker_class_name":labels_tracker_class_name,
                                    "bounding_boxes":labels_tracker_bbox} )
    creating_dframe.to_csv("create_dframe.csv")
    return creating_dframe
        


def add_new_track_id(found_tracking_ids, detections):
    for i in detections.tracker_id.tolist():
        found_tracking_ids.add(i)
        


if __name__ == "__main__":
    labels_tracker_id = []
    labels_tracker_class_name=[]
    labels_tracker_bbox = []
    main()

    

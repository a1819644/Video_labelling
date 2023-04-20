import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist

def main(read_dframe, read_calculation):
    x = None
    print("read_dframe")
    for column in read_dframe.loc[:,'bounding_boxes']:
        # Iterate over column names

        x = eval(column)
        for i in x:
            length = len(i)
            
            print("x  ",list(x))
            arrays = np.empty([length,length]) 
            # for j in x:
            #     print("j   ",j)
            for i in x: 
                    #[1178.4   ,    1.6609, 1532.1   ,  935.91  ] taking it one by one into item var
                    length = len(i)
                    arrays = np.empty([length,length]) 
                    for j in x:
                        get_distances(i, j, arrays)
                    print("one loop over")



    

def get_distances(rect1, rect2, arrays):
    # manually putted the weight and height of the frame
    w = 1080
    h = 1940
    distance = 0
    rect1x1, rect1y1, rect1x2, rect1y2 = pascal_voc_to_yolo(rect1[0], rect1[1], rect1[2], rect1[3],w,h)
    # print(rect1x1, rect1y1, rect1x2, rect1y2)
    rect2x1, rect2y1, rect2x2, rect2y2 = pascal_voc_to_yolo(rect2[0], rect2[1], rect2[2], rect2[3],w,h)
    
    
    ##get bouding boxes
    # (tl, tr, br, bl) = box     # (rect1[0], rect1[1], rect1[2], rect1[3]) 
    (rect1_tlblX, rect1_tlblY) = midpoint(rect1[0], rect1[3])
    (rect1_trbrX, rect1_trbrY) = midpoint(rect1[1], rect1[2])
    
    
    
    
    #getting the center of the rectangle
    # print((rect1))
    cx1, cy1 = int((rect1[0] + rect1[2]) / 2), int((rect1[1] + rect1[3])/ 2)
    cx2, cy2 = int((rect2[0] +   rect2[2])/2), int((rect2[1] + rect2[3]) / 2)
    dis = (np.sqrt(((cx2 - cx1) ** 2) + ((cy2 - cy1) ** 2)))
    dis = int(dis)
    print(dis)
    # CGFloat horizontalDistance = ( center2.x - center1.x );
    # CGFloat verticalDistance = ( center2.y - center1.y );

    # CGFloat distance = sqrt( ( horizontalDistance * horizontalDistance ) + ( verticalDistance * verticalDistance ) );
    return distance


#get midpoint
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Convert Pascal_Voc bb to Yolo
def pascal_voc_to_yolo(x1, y1, x2, y2, image_w, image_h):
    return [((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h]

if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    read_calculation = pd.read_csv('calculation_dis.csv')
    main(read_dframe, read_calculation)

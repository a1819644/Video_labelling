import pandas as pd
import numpy as np
from numpy import float32, array
import math

def main(read_dframe, read_calculation):
    
    print("read_dframe")
    for column in read_dframe['bounding_boxes']:
        # Iterate over column names
        x = eval(column)
    # [array([1178.4   ,    1.6609, 1532.1   ,  935.91  ], dtype=float32), array([761.56, 386.14, 953.42, 936.99], dtype=float32), array([ 458.4 ,  544.93, 1014.9 ,  943.33], dtype=float32)]
    # [1178.4       1.6609 1532.1     935.91  ]
        print('Column Contents : ', x)
        for i in x: 
            #[1178.4   ,    1.6609, 1532.1   ,  935.91  ] taking it one by one into item var
            length = len(i)
            arrays = np.empty([length,length]) 
            for j in x:
                get_distances(i, j, arrays)
                
            print("one loop over")
                
                
            

# def takes_bounding_boxes(arrays, item):
#     print(item)
    
    # iterate over each of the rows of the bounding box
    # for i in np.nditer(item):
    #     print (i)
        
    # print('xyxy of the rectangle:', arrays)
    

def get_distances(rect1, rect2, arrays):
    # manually putted the weight and height of the frame
    w = 416
    h = 234
    distance = 0
    rect1x1, rect1y1, rect1x2, rect1y2 = pascal_voc_to_yolo(rect1[0], rect1[1], rect1[2], rect1[3],w,h)
    # print(rect1x1, rect1y1, rect1x2, rect1y2)
    rect2x1, rect2y1, rect2x2, rect2y2 = pascal_voc_to_yolo(rect2[0], rect2[1], rect2[2], rect2[3],w,h)
    
    #getting the center of the rectangle
    print((rect1))
    cx1, cy1 = int(rect1[0] + rect1[2] / 2), int(rect1[1] + rect1[3]/ 2)
    cx2, cy2 = int(rect2[0] +   rect2[2]/2), int(rect2[1] + rect2[3] / 2)
    dis = (math.sqrt(((cx2 - cx1) ** 2) + ((cy2 - cy1) ** 2)) ** 0.5)
    dis = int(dis)
    print(dis)
    # CGFloat horizontalDistance = ( center2.x - center1.x );
    # CGFloat verticalDistance = ( center2.y - center1.y );

    # CGFloat distance = sqrt( ( horizontalDistance * horizontalDistance ) + ( verticalDistance * verticalDistance ) );
    return distance

# Convert Pascal_Voc bb to Yolo
def pascal_voc_to_yolo(x1, y1, x2, y2, image_w, image_h):
    return [((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h]

if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    read_calculation = pd.read_csv('calculation_dis.csv')
    main(read_dframe, read_calculation)

import pandas as pd
import numpy as np

def main(read_dframe, read_calculation):
    
    print("read_dframe")
    for column in read_dframe['bounding_boxes']:
       # Iterate over column names
        print('Column Contents : ', column.split(','))
        # found_items = [list(item) for item in column]
        # for i in range(len(found_items)):
        #     print(found_items[i])


# def get_distances(rect1, rect2):
#     #getting the center of the rectangle
#     CGPoint center1 = CGPointMake( CGRectGetMidX( rect1 ), CGRectGetMidY( rect1 ) );
#     CGPoint center2 = CGPointMake( CGRectGetMidX( rect2 ), CGRectGetMidY( rect2 ) );

#     CGFloat horizontalDistance = ( center2.x - center1.x );
#     CGFloat verticalDistance = ( center2.y - center1.y );

#     CGFloat distance = sqrt( ( horizontalDistance * horizontalDistance ) + ( verticalDistance * verticalDistance ) );
#     return distance



if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    read_calculation = pd.read_csv('calculation_dis.csv')
    main(read_dframe, read_calculation)

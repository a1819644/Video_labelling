import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os

def main(read_dframe):
    x = None
    count = 0;
    print("read_dframe")
    for column in read_dframe.loc[:,'bounding_boxes']:
        # Iterate over column names
        x = eval(column)
        get_current_row =0
        for i in x:
            length = len(i)
            # print("x  ",list(x))
            list_finally = []
            arrays = np.empty([length,length]) 
            for i in x: 
                #[1178.4   ,    1.6609, 1532.1   ,  935.91  ] taking it one by one into item var
                length = len(i)
                temp_ls = []
                # arrays = np.empty([length,length]) dont need it anymore
                for j in x:
                    temp_ls.append(get_distances(i, j, arrays))
                list_finally.append(temp_ls)
            get_current_row =get_current_row + 1
        create_distances_df(list_finally,read_dframe, count)
        count=count+1



def create_distances_df(distance_ls, read_dframe, count):
    copy_rdframe = read_dframe.copy()
        # creating dataframe like this
        # person1 person2 bench3
        # person1     NaN     NaN    NaN
        # person2     NaN     NaN    NaN
        # bench3      NaN     NaN    NaN
    lsdata_trackerId = eval(copy_rdframe.iloc[count,1])
    lsdata_class_name = eval(copy_rdframe.iloc[count,2])
    ls = []
    for track, class_name in zip(lsdata_trackerId,lsdata_class_name):
        xz = str(class_name)+str(track)
        ls.append(xz)       
    print(lsdata_class_name, lsdata_trackerId, count)
    df_for_meassurements = pd.DataFrame(distance_ls,columns=ls, index=ls)

    df_for_meassurements.to_csv(path+'/distance_tracking/'+str(count)+ '.csv', index=ls)
    # print(df_for_meassurements)

    

    

def get_distances(rect1, rect2, arrays):
    # manually putted the weight and height of the frame
    w = 1080
    h = 1940
    distance = 0
    # calculating the mid distance between rect1 and rect2
    centreRect1 = (rect1[0] + rect1[2])/2, (rect1[1] + rect1[3])/2
    centreRect2 = (rect2[0] + rect2[2])/2, (rect2[1] + rect2[3])/2
    #calculating the distance between the centre point and returning the distace     
    return euclidean_distance(centreRect1, centreRect2)


#get distance between center
def euclidean_distance(vx, vy):
    return int(sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5)


if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    path = os.getcwd()
    if os.path.isdir('distance_tracking') == False:
        os.mkdir('distance_tracking')
    main(read_dframe)
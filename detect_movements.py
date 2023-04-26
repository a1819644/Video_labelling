import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os
import functools


def main(read_dframe):
    x = None
    count = 0;
    get_count_tracking  =0

    # reading the bounding box data from each row
    for column in read_dframe.loc[:,'bounding_boxes']:
        # Iterate over column names
        x = eval(column)
        get_current_row =0
        print(x)
        # for i in x:
        #     length = len(i)
        #     print(i)
        #     create_tracking_movement_df(read_dframe, count)
        #     count +1
        get_tracked(x, get_count_tracking) # sending the tracked objs bounding boxes
        get_count_tracking = get_count_tracking + 5

# # def create_tracking_movement_df(i, read_dframe, count, get_count_tracking):
#     copy_rdframe = read_dframe.copy()
#         # creating dataframe like this
#         #            object1 objec2 obj3
#         # stayed      -1     -1      -1 
#         # person2     NaN     NaN    NaN
#         # bench3      NaN     NaN    NaN
#     lsdata_trackerId = eval(copy_rdframe.iloc[count,1])
#     lsdata_class_name = eval(copy_rdframe.iloc[count,2])
#     lsdata_tracking_type = ["not_moving", "walking", "togther"]
#     ls = []
#     for track, class_name in zip(lsdata_trackerId,lsdata_class_name):
#         xz = str(class_name)+str(track)
#         ls.append(xz)       
#     print(lsdata_class_name, lsdata_trackerId, count)
    
    
#     df_for_meassurements = pd.DataFrame(values,columns=lsdata_tracking_type, index=ls)
#     df_for_meassurements.to_csv(path+'/movements_tracking/'+str(count)+ '.csv', index=ls)
#     # print(df_for_meassurements)


# tracking the objects one by one
# count to check is this the first array from the first arrays
def get_tracked(current_array, get_count_tracking):
    if get_count_tracking == 0:
        prev_list.append(current_array)
    else:
        for prev in prev_list:
            # checking if the prev and cur arrays coming from the same tracking ids
            # if not then change it
            # print(prev , "prev", get_count_tracking)
            # print(current_array, "current", get_count_tracking)
            corrected_prev_list = check_tracking_to_bounding_boxes_loc_fix(prev,get_count_tracking)
            
    prev_list.clear()
    prev_list.append(current_array)


# correcting the order of the inserted arrays
def check_tracking_to_bounding_boxes_loc_fix(prev, get_count_tracking):
    copy_rdframe = read_dframe.copy() # copying the original csv
    correct_order_list =[]

    # get the list of the tracking from the same row /frame index
    if get_count_tracking <= len(copy_rdframe.index):
        lsdata_trackerId_current = eval(copy_rdframe.iloc[get_count_tracking,1]) #this shows the current one
        get_prev_lsa_index = eval(copy_rdframe.iloc[get_count_tracking-5,1])
        print(get_prev_lsa_index , "get_prev_lsa_index --data", eval(copy_rdframe.iloc[get_count_tracking-5,3]))
        print(lsdata_trackerId_current, "current tracking--> data",eval(copy_rdframe.iloc[get_count_tracking,3]))
        
        # filling the correct_order_list using current lsdata_trackerId_current id
        for i in lsdata_trackerId_current:
            get_val = i
            get_index = 0
            for x in get_prev_lsa_index:
                if x == i:
                    correct_order_list.append(prev[get_index])
                    break                    
                else:
                    get_index = get_index + 1
        print( "fixes .... prev", correct_order_list)
    return correct_order_list
        
# #calculate the the mid point of bounding boxes
# def mid_bounding_boxes(pre_array, current_array):
#     # calculating the mid distance between rect1 and rect2
#     prev = (pre_array[0] + (pre_array[2]/2), pre_array[1] + (pre_array[3]/2))
#     curr = (current_array[0] + (current_array[2]/2), current_array[1] + (current_array[3]/2))
#     return prev, curr



if __name__ == "__main__":
    prev_list = []
    current_list = []
    read_dframe = pd.read_csv('create_dframe.csv')
    path = os.getcwd()
    if os.path.isdir('movements_tracking') == False:
        os.mkdir('movements_tracking')
    main(read_dframe)
import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os



def main(read_dframe):

    rowcount = 0
    get_count_tracking_current= 5
    get_count_tracking_prev = 0
    for i in range(len(read_dframe.index)):
        if rowcount >= 5:
            get_tracked(get_count_tracking_prev,get_count_tracking_current) # sending the tracked objs bounding boxes
            get_count_tracking_current = get_count_tracking_current + 5
            get_count_tracking_prev = get_count_tracking_prev + 5
            rowcount = 0
        else:
            rowcount= rowcount + 1
        print(i)



# tracking the objects one by one
# count to check is this the first array from the first arrays
def get_tracked( get_count_tracking_prev, get_count_tracking_current):
    newList = []
    rows = ['not_moving', 'moving']
    dic_current, dic_previous, names = check_tracking_to_bounding_boxes_loc_fix(get_count_tracking_prev, get_count_tracking_current)
    not_moving = _is_stay_still(dic_current, dic_previous) # not_moving values 
    moved = moving(not_moving) # just fliping the values

    #this line must be run at the end 
    newList.append(not_moving)
    newList.append(moved)
    # cause do the moving part to
    create_df = pd.DataFrame(newList, index=rows, columns=names)
    print(create_df, "thats df")

def moving(lst):
   return list(map(lambda x: int(not x), lst))



# stay_still calculation between pre and current arrays
def _is_stay_still(dic_current, dic_previous):

    result = []# staying false  and 1 for the true
    
    # looping through dictonary of current, if the key/tracking id doesnt exist than we can move on 
    for key, value in dic_current.items():
        if key in dic_previous:
            prev_mid_point,curr_mid_point =mid_bounding_boxes(dic_previous[key], dic_current[key])
            result.append(comparing_dis_mid_points(prev_mid_point, curr_mid_point))
            
    print(result)
    return result


#get distance between centers
def comparing_dis_mid_points(vx, vy):
    if abs(vx[0] - vy[0]) < 2 and abs(vx[0] - vy[0]) < 2:
        # not moving
        return 1
    else:
        # moving 
        return 0

# calculate the the mid point of bounding boxes
def mid_bounding_boxes(pre_array, current_array):

    # calculating the mid distance between rect1 and rect2

    prev_mid = (pre_array[0] + pre_array[2]) / \
        2, (pre_array[1] + (pre_array[3]))/2
    curr_mid = (current_array[0] + current_array[2]) / \
        2, (current_array[1] + current_array[3])/2
    print(pre_array, "previous array", prev_mid)
    print(current_array, "current array", curr_mid)
    return prev_mid, curr_mid

# get distance between center
def euclidean_distance(vx, vy):
    return int(sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5)



# correcting the order of the inserted arrays
def check_tracking_to_bounding_boxes_loc_fix( get_count_tracking_prev,get_count_tracking_current ):
    copy_rdframe = read_dframe.copy() # copying the original csv
    # get the list of the tracking from the same row /frame index
    if get_count_tracking_current < len(copy_rdframe.index):
        lsdata_trackerId_current = eval(copy_rdframe.iloc[ get_count_tracking_current,1]) #this shows the current one
        get_prev_lsa_index = eval(copy_rdframe.iloc[get_count_tracking_prev,1])

        names = eval(
            copy_rdframe.iloc[get_count_tracking_current, 2])
        
        # imp dont delete the below comment
        # print(lsdata_trackerId_current, "current --> data",eval(copy_rdframe.iloc[get_count_tracking_current,3]))
        # print(get_prev_lsa_index , "previous -->data", eval(copy_rdframe.iloc[get_count_tracking_prev,3]))
        
        current = eval(copy_rdframe.iloc[get_count_tracking_current,3])
        previous = eval(copy_rdframe.iloc[get_count_tracking_prev,3])
        dic_current = {}
        for key, value in zip(lsdata_trackerId_current,current): 
            dic_current[key] = value

        dic_prev = {}
        for key, value in zip(get_prev_lsa_index,previous): 
            dic_prev[key] = value


    return dic_current, dic_prev, names



if __name__ == "__main__":
    prev_list = []
    current_list = []
    read_dframe = pd.read_csv('create_dframe.csv')
    path = os.getcwd()
    if os.path.isdir('movements_tracking') == False:
        os.mkdir('movements_tracking')
    main(read_dframe)
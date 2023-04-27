import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os



def main(read_dframe):
    x = None
    rowcount = 0
    get_count_tracking_current= 5
    get_count_tracking_prev = 4
    for i in range(len(read_dframe.index)):
        if rowcount >= 5:
            get_tracked(x,get_count_tracking_prev,get_count_tracking_current) # sending the tracked objs bounding boxes
            get_count_tracking_current = get_count_tracking_current + 5
            get_count_tracking_prev = get_count_tracking_prev + 5
            rowcount = 0
        else:
            rowcount= rowcount + 1
        print(i)



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
def get_tracked(current_array, get_count_tracking_prev, get_count_tracking_current):
    if  get_count_tracking_prev == 4: ## i know its the first loop  as predifined earlier
        prev_list.append(current_array)
        # print(current_array , "current and previous arrays are the same")

        for prev in prev_list:
            corrected_prev_list = check_tracking_to_bounding_boxes_loc_fix(get_count_tracking_prev,get_count_tracking_current)
    else:
        # print(prev_list, "previous array", get_count_tracking_prev)
        # print(current_array, "current array", get_count_tracking_current)
        for prev in prev_list:
            # checking if the prev and cur arrays coming from the same tracking ids
            dic_current, dic_previous = check_tracking_to_bounding_boxes_loc_fix(get_count_tracking_prev,get_count_tracking_current)
            was_stayed = _is_stay_still(dic_current, dic_previous)
            
    # print(current_array , "dsjkadsjashdjdsaj currrrent going to be the pre")
    prev_list.clear()
    prev_list.append(current_array)



# stay_still calculation between pre and current arrays
def _is_stay_still(dic_current, dic_previous):
    result = []# staying false  and 1 for the true
    
    # looping through dictonary of current, if the key/tracking id doesnt exist than we can move on 
    for key, value in dic_current.items():
        if key in dic_previous:
            prev_mid_point,curr_mid_point =mid_bounding_boxes(dic_previous[key], dic_current[key])
            result.append(comparing_dis_mid_points(prev_mid_point, curr_mid_point))
            
    print(result)
    # get_mid_boxes = 
    
    # print(get_mid_boxes)
    
    return result


#get distance between centers
def comparing_dis_mid_points(vx, vy):
    for x, y in zip(vx, vy):
        if x == y or x >= y+10 or y >= x+10: # tolerance between 10 px 
            return 1 # for the true
        else:
            return 0 # false 



# correcting the order of the inserted arrays
def check_tracking_to_bounding_boxes_loc_fix( get_count_tracking_prev,get_count_tracking_current ):
    copy_rdframe = read_dframe.copy() # copying the original csv
    # get the list of the tracking from the same row /frame index
    if get_count_tracking_current < len(copy_rdframe.index):
        lsdata_trackerId_current = eval(copy_rdframe.iloc[ get_count_tracking_current,1]) #this shows the current one
        get_prev_lsa_index = eval(copy_rdframe.iloc[get_count_tracking_prev,1])
        
        # imp dont delete the below comment
        print(lsdata_trackerId_current, "current tracking--> data",eval(copy_rdframe.iloc[get_count_tracking_current,3]))
        print(get_prev_lsa_index , "get_prev_lsa_index --data", eval(copy_rdframe.iloc[get_count_tracking_prev,3]))
        
        current = eval(copy_rdframe.iloc[get_count_tracking_current,3])
        previous = eval(copy_rdframe.iloc[get_count_tracking_prev,3])
        dic_current = {}
        for key, value in zip(lsdata_trackerId_current,current): 
            dic_current[key] = value

        dic_prev = {}
        for key, value in zip(get_prev_lsa_index,previous): 
            dic_prev[key] = value


    return dic_current, dic_prev

#calculate the the mid point of bounding boxes
def mid_bounding_boxes(pre_array, current_array):

    # calculating the mid distance between rect1 and rect2
    prev_mid = (pre_array[0] + (pre_array[2]/2), pre_array[1] + (pre_array[3]/2))
    curr_mid = (current_array[0] + (current_array[2]/2), current_array[1] + (current_array[3]/2))
    print(pre_array, "previous array", prev_mid )
    print(current_array, "current array", curr_mid)
    return prev_mid, curr_mid



if __name__ == "__main__":
    prev_list = []
    current_list = []
    read_dframe = pd.read_csv('create_dframe.csv')
    path = os.getcwd()
    if os.path.isdir('movements_tracking') == False:
        os.mkdir('movements_tracking')
    main(read_dframe)
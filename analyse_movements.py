# this files is analyzing the distance_tracking folder and the movements_tracking
import pandas as pd
import os
from pathlib import Path
import statistics
from glob import glob
import numpy as np
from collections import Counter
import collections
import re


def main():
    
    # capturing the columns of the movement_tracks_allinone df
    movements_name = list(movement_tracks_allinone.columns.values)
    movements_name.remove('Unnamed: 0')
    
    # removing the 'moving'  rows from the movement_tracks_allinone
    set_index_for_movements = movement_tracks_allinone.set_index("Unnamed: 0")
    mov_without_notMoving = set_index_for_movements.drop("moving")
    # print(mov_without_notMoving.head(10))





    # analyze closeness of the detected objects (using distance_tracking files)
    # print(distance_tracks_allinone.head(10))
    distance_tracks_allinone_new = distance_tracks_allinone.copy()
    distance_tracks_allinone_new.to_csv("just.csv")
    # print(distance_tracks_allinone_new.head(20), "distance_tracks_allinone")

    distance_name = list(distance_tracks_allinone_new.columns.values)
    distance_name.remove('Unnamed: 0')
    # print(len(distance_tracks_allinone_new))

    # analyzing togetherness of the detected objects (using distance_tracking files)
    resultfortogetherness = who_is_together(distance_tracks_allinone_new, distance_name)
    analyzing_togetherness(resultfortogetherness)
    
    # funciton to analyze the movement_tracks_allinone whether the object was moving or not
    _list_moving, list_non_moving = analyzing_movingness(mov_without_notMoving, movements_name)

    print(result_togetherness_record, "result_togetherness")
    print(_list_moving, "list of those who were moving")
    print(list_non_moving, "list of those who were not moving")
    # return result_togetherness_record, is_moving_reclst, isnt_moving_reclst


# def analyzing_not_movingness(result_movingness):
#     is_moving_rec = []        
#     for k, v in result_movingness.items():
#         if v <= 0.50:
#             is_moving_rec.append(k + togetherness_record[3])
#             ## found not  moving
#     return is_moving_rec

# def analyzing_movingness(result_movingness):
#     is_moving_rec = []
#     isnt_moving_rec = []
        
#     for k, v in result_movingness.items():
#         if v <= 0.50:
#             is_moving_rec.append(k + togetherness_record[2])
#             ## found moving
#         else:
#             isnt_moving_rec.append(k + togetherness_record[3])
#     return is_moving_rec, isnt_moving_rec


def analyzing_togetherness(resultfortogetherness):
    # print(resultfortogetherness)
    for k, v in resultfortogetherness.items():
        if v >= 0.50:
            result_togetherness_record.append(k + togetherness_record[1]) ## found together
        else:
            result_togetherness_record.append(k + togetherness_record[0]) ## far away from each other 


def who_is_together(distance_tracks_allinone_new, distance_name):
    dic_record = {}
    name_count  = []

    # print(dic_record)
    # {'person1-person1': [], 'person1-person2': [], 'person1-bench3': [], 
    # 'person2-person1': [], 'person2-person2': [], 'person2-bench3': [], 
    # 'bench3-person1': [], 'bench3-person2': [], 'bench3-bench3': []}
    space_in_between = " "
    for i in range(len(distance_tracks_allinone_new)):
        name = ""
        for j in range(len(distance_name)):
            if distance_name[j] != distance_tracks_allinone_new.iloc[i,0]:
                name =  distance_tracks_allinone_new.iloc[i,0] +space_in_between+ distance_name[j]
                name_count.append(distance_tracks_allinone_new.iloc[i,0])
                name_count.append(distance_name[j])
                dic_record[name] = []

    for i in range(len(distance_tracks_allinone_new)):
        name = ""
        for j in range(len(distance_name)):
            if distance_name[j] != distance_tracks_allinone_new.iloc[i,0]:
                name =  distance_tracks_allinone_new.iloc[i,0] + space_in_between + distance_name[j]
                val = distance_tracks_allinone_new.iloc[i,j +1]
                # print(type(val))
                if val < 700: 
                        dic_record[name].append(1) # 1 for close
                else:
                        dic_record[name].append(0) # 0 for far
                        
    # arranging in the descending order 
    dic_name_count = Counter(name_count)
    sorted_list = sorted(dic_name_count.items(), key = lambda x:x[1], reverse = True)
    dic_name_count.clear()
    for key, value in sorted_list:
        dic_name_count[key] = value

    #we will keep only the top 5 objects are relations only! and deleting rest of the keys and values from the dic_record dictionary
    first5pairs = {k: dic_name_count[k] for k in list(dic_name_count)[:5]} 

    for k,v in first5pairs.items(): 
        top_5_keys.append(k)
    
    # print(top_5_keys, "top_5_keys")
    # print(len(dic_record), "before")
    for k,v in dic_record.items():
            get_object_names_in_list_frmt = k.split() # get the object names
            # print(get_object_names_in_list_frmt)
            if  None == first5pairs.get(get_object_names_in_list_frmt[0]) or None == first5pairs.get(get_object_names_in_list_frmt[1]) : 
                remKeylist[get_object_names_in_list_frmt[0] + space_in_between+ get_object_names_in_list_frmt[1]]= ''
    
    # print(remKeylist, "remkeylist")
    # print(len(dic_record), "before")

    # removing the keys fromt the dic_record
    for key in remKeylist:
        del dic_record[key]
    # print(len(dic_record), "after")
    
    # deleting the keys like this "person:1 person:2" and " person:2 person:1" as they both 
    # represent same things
    fresh_results = {}
    for k,v in dic_record.items():
        get_object_names_in_list_frmt = k.split()
        temp = get_object_names_in_list_frmt[1] + space_in_between + get_object_names_in_list_frmt[0]
        if fresh_results.get(k) == None and  fresh_results.get(temp) == None:
            fresh_results[k] = v    
    # print(len(fresh_results), "del_duplicates_keys")
    
    dic_result = {} # storing the result from the dic_record
    for k,v in fresh_results.items():
        dic_result[k] = statistics.mean(v)
    return dic_result

    
def analyzing_movingness(notMoving, movements_name):
    # print(notMoving)
    # looping through the movement_tracks_allinone df and analyzing the movements tracking
    dic_tracking_movements ={}
    for names in movements_name:
        dic_tracking_movements[names] = notMoving[names].mean(axis = 0, skipna = True)
    
    # print((dic_tracking_movements), "before removal")
    # now removing which shows the least in the video 
    for k, v in dic_tracking_movements.items():
        for key in range(len(top_5_keys)):
            if  dic_tracking_movements.get(top_5_keys[key]) == None:
                del dic_tracking_movements[k]
                continue

    # print((dic_tracking_movements), "after removal")
    _result_moving = []
    _result_not_moving = []
    for k, v in dic_tracking_movements.items():
        if v <= 0.50:
            _result_moving.append(k + togetherness_record[2])
        else:
            _result_not_moving.append(k + togetherness_record[2])
    
    # print((_result_moving), "those who were walking") 
    # print(_result_not_moving, "those who were not walking")
    return _result_moving,_result_not_moving


if __name__ == "__main__":
    togetherness_record = [" were far away from each others", " were together", " was walking/moving", "was not moving"]
    result_togetherness_record =[]
    remKeylist = {}
    top_5_keys = []
    
    # for movements tracking folder
    cv_movements_tracking_files = sorted(glob('movements_tracking/*.csv'))
    movement_tracks_allinone = pd.concat((pd.read_csv(file) for file in cv_movements_tracking_files), axis='index')
    movement_tracks_allinone.to_csv("movement_tracks_allinone.csv")

    # #for distance_tracking folder
    cv_distance_tracking_files = sorted(glob('distance_tracking/*.csv'))
        #  code to delete the delete files  
    dir_path = 'distance_tracking'
    files = os.listdir(dir_path)
    csv_files = [f for f in files if f.endswith('.csv')]

    list_files_order = {}

    for file in csv_files:
        mystr = str(file)
        get_orderid = re.findall(r'\d+', mystr)
        list_files_order[int(get_orderid[0])] = 'distance_tracking/'+file

    sorted_dict_distance = dict(sorted(list_files_order.items()))
    distance_tracks_allinone = pd.concat((pd.read_csv(value) for key,value  in sorted_dict_distance.items()))
    distance_tracks_allinone.to_csv("distance_tracks_allinone.csv")
    
    # # print(movement_tracks_allinone.head(10))
    
    main() 
    
    # print(alltogether, "alltogether relationship record")
    # print(moving_rec, "moving record")
    # print(not_moving, "not_moving record")

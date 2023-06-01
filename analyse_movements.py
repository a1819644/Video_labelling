# this files is analyzing the distance_tracking folder and the movements_tracking
import pandas as pd
import os
from pathlib import Path
import statistics
from glob import glob
import numpy as np
from collections import Counter
import collections

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
    distance_tracks_allinone.to_csv("before_sorting_just.csv")
    distance_tracks_allinone_new = distance_tracks_allinone.copy()
    distance_tracks_allinone_new.to_csv("just.csv")
    # print(distance_tracks_allinone_new.head(20), "distance_tracks_allinone")

    distance_name = list(distance_tracks_allinone_new.columns.values)
    distance_name.remove('Unnamed: 0')
    # print(len(distance_tracks_allinone_new))

    resultfortogetherness = who_is_together(distance_tracks_allinone_new, distance_name)
    # print(resultfortogetherness)
    analyzing_togetherness(resultfortogetherness)
    
    # funciton to analyze the movement_tracks_allinone whether the object was moving or not
    result_moving = has_moved(mov_without_notMoving, movements_name)
    analyzing_movingness(result_moving)
    
    print(result_togetherness_record) 


def analyzing_movingness(result_movingness):
    
        
    for k, v in result_movingness.items():
        if v <= 0.60:
            result_togetherness_record.append(k +togetherness_record[2]) ## found moving


def analyzing_togetherness(resultfortogetherness):
    # print(resultfortogetherness)
    for k, v in resultfortogetherness.items():
        if v >= 0.60:
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
    
    
    # print(len(dic_record), "before")
    for k,v in dic_record.items():
            get_object_names_in_list_frmt = k.split() # get the object names
            # print(get_object_names_in_list_frmt)
            if get_object_names_in_list_frmt[0] in first5pairs or get_object_names_in_list_frmt[1] in first5pairs: 
                remKeylist.append(k)
    
    # print(remKeylist, "remkeylist")

    # removing the keys fromt the dic_record
    for key in remKeylist:
        del dic_record[key]
    print(len(dic_record), "after")
    
    dic_result = {} # storing the result from the dic_record
    for k,v in dic_record.items():
        dic_result[k] = statistics.mean(v)

    
    return dic_result

    
def has_moved(notMoving, movements_name):
    # looping through the movement_tracks_allinone df and analyzing the movements tracking
    dic_tracking_movements ={}
    # print(notMoving)
    for names in movements_name:
        dic_tracking_movements[names] = notMoving[names].mean(skipna = True)
    
    # print(len(dic_tracking_movements), "before removal")
    # now removing which shows the least in the video
    for key in range(len(top_5_keys)):
        if top_5_keys[key] in dic_tracking_movements:
            del dic_tracking_movements[top_5_keys[key]]

    
    # print(len(dic_tracking_movements), "after removal")   
    return dic_tracking_movements


if __name__ == "__main__":
    togetherness_record = [" were far away from each others", " were together", " was walking"]
    result_togetherness_record =[]
    remKeylist = []
    top_5_keys = []
    
    # for movements tracking folder
    cv_movements_tracking_files = sorted(glob('movements_tracking/*.csv'))
    movement_tracks_allinone = pd.concat((pd.read_csv(file) for file in cv_movements_tracking_files), axis='index')
    movement_tracks_allinone.to_csv("movement_tracks_allinone.csv")

    # #for distance_tracking folder
    cv_distance_tracking_files = sorted(glob('distance_tracking/*.csv'))
    distance_tracks_allinone = pd.concat((pd.read_csv(file) for file in cv_distance_tracking_files), axis='index')
    distance_tracks_allinone.to_csv("distance_tracks_allinone.csv")
    
    # print(movement_tracks_allinone.head(10))
    
    
    main()

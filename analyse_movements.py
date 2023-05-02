# this files is analyzing the distance_tracking folder and the movements_tracking
import pandas as pd
import os
from pathlib import Path
import statistics
import glob

def main():
    
    # capturing the columns of the movement_tracks_allinone df
    movements_name = list(movement_tracks_allinone.columns.values)
    movements_name.remove('Unnamed: 0')
    
    movements_name.remove('filename')
    # removing the 'moving'  rows from the movement_tracks_allinone
    set_index_for_movements = movement_tracks_allinone.set_index("Unnamed: 0")
    mov_without_notMoving = set_index_for_movements.drop("moving")
    # print(mov_without_notMoving.head(10))
    
    
    # funciton to analyze the movement_tracks_allinone whether the object was moving or not
    result_moving = has_moved(mov_without_notMoving, movements_name)
    analyzing_movingness(result_moving)
    # analyze closeness of the detected objects (using distance_tracking files)
    print(distance_tracks_allinone.head(10))
    distance_tracks_allinone.to_csv("before_sorting_just.csv")
    distance_tracks_allinone_new = distance_tracks_allinone.sort_values(by='filename')
    distance_tracks_allinone_new.to_csv("just.csv")
    print(distance_tracks_allinone_new.head(20), "distance_tracks_allinone")

    distance_name = list(distance_tracks_allinone_new.columns.values)
    distance_name.remove('Unnamed: 0')
    distance_name.remove('filename')
    # print(distance_name)

    resultfortogetherness = who_is_together(distance_tracks_allinone_new, distance_name)
    analyzing_togetherness(resultfortogetherness)
    print(result_togetherness_record)


def analyzing_movingness(result_movingness):
    for k, v in result_movingness.items():
        if v <= 0.50:
            result_togetherness_record.append( k +togetherness_record[2]) ## found moving


def analyzing_togetherness(resultfortogetherness):
    for k, v in resultfortogetherness.items():
        if v >= 0.60:
            result_togetherness_record.append(k +togetherness_record[1]) ## found together
        else:
            result_togetherness_record.append(k +togetherness_record[0]) ## found together


def who_is_together(distance_tracks_allinone_new, distance_name):
    dic_record = {}
    dic_record_keys = set()
    # print(dic_record)
    # {'person1-person1': [], 'person1-person2': [], 'person1-bench3': [], 
    # 'person2-person1': [], 'person2-person2': [], 'person2-bench3': [], 
    # 'bench3-person1': [], 'bench3-person2': [], 'bench3-bench3': []}
    altr_name = []
    names = []
    space_in_between = " "
    for i in range(len(distance_tracks_allinone_new)):
        name = ""
        for j in range(len(distance_name)):
            if distance_name[j] != distance_tracks_allinone_new.iloc[i,0]:
                name =  distance_tracks_allinone_new.iloc[i,0] +space_in_between+ distance_name[j]
                dic_record[name] = []

    for i in range(len(distance_tracks_allinone_new)):
        name = ""
        for j in range(len(distance_name)):
            if distance_name[j] != distance_tracks_allinone_new.iloc[i,0]:
                name =  distance_tracks_allinone_new.iloc[i,0] +space_in_between+ distance_name[j]
                val = distance_tracks_allinone_new.iloc[i,j +1]
                if val < 550: 
                    dic_record[name].append(1) # 1 for close
                else:
                    dic_record[name].append(0) # 0 for far
                
    # print(dic_record)
    
    dic_result = {} # storing the result from the dic_record
    for k,v in dic_record.items():
        dic_result[k] = statistics.mean(v)
    
    print(dic_result)
    return dic_result

    
def has_moved(mov_without_notMoving, movements_name):
    # looping through the movement_tracks_allinone df and analyzing the movements tracking
    dic_tracking_movements ={}
    
    for names in movements_name:
        dic_tracking_movements[names] = mov_without_notMoving[names].mean(skipna = True)
    
    return dic_tracking_movements


if __name__ == "__main__":
    togetherness_record = [" were faraway from each others", " were together", " were walking"]
    result_togetherness_record =[]
    
    # Get CSV files list from a folder
    path_movements_path = r'movements_tracking'
    path_dis_tracking_path = r'distance_tracking'
    
    #for movements tracking folder
    cv_movements_tracking_files = Path(path_movements_path).glob('*.csv')
    dfs = list()
    movement_tracks_allinone = pd.concat((pd.read_csv(f).assign(filename=f.stem) for f in cv_movements_tracking_files), ignore_index=True)
    movement_tracks_allinone.to_csv("movement_tracks_allinone.csv")
    #for distance_tracking folder
    cv_distance_tracking_files = Path(path_dis_tracking_path).glob('*.csv')
    dfs_distance = list()
    distance_tracks_allinone = pd.concat((pd.read_csv(f).assign(filename=f.stem) for f in cv_distance_tracking_files), ignore_index=True)
    distance_tracks_allinone.to_csv("distance_tracks_allinone.csv")
    # print(distannce_tracks_allinone.head(10))
    
    dfs = list()
    
    cv_distance_tracking_files22 =sorted(glob.glob('*.csv'))

    for f in cv_distance_tracking_files22:
        data = pd.read_csv(f)
        # .stem is method for pathlib objects to get the filename w/o the extension
        data['file'] = f.stem
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)

    df.to_csv("dfs.csv")
    
    main()

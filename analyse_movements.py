# this files is analyzing the distance_tracking folder and the movements_tracking
import pandas as pd
import os
from pathlib import Path

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
    has_moved(mov_without_notMoving, movements_name)
    
    # analyze closeness of the detected objects (using distance_tracking files)
    distance_tracks_allinone_new = distance_tracks_allinone.sort_values(by='filename', ascending=True)
    print(distance_tracks_allinone_new.head(10))

    distance_name = list(distance_tracks_allinone_new.columns.values)
    distance_name.remove('Unnamed: 0')
    distance_name.remove('filename')
    print(distance_name)
    
    name = 0
    for i in range(5):
        i = {}
        print(type(i))
    
    # for names in distance_name:
    for row in distance_tracks_allinone_new.index:
            print(distance_tracks_allinone["person1"][row])
    
    
    
    
    
def has_moved(mov_without_notMoving, movements_name):
    # looping through the movement_tracks_allinone df and analyzing the movements tracking
    dic_tracking_movements ={}
    
    for names in movements_name:
        dic_tracking_movements[names] = mov_without_notMoving[names].mean(skipna = True)
    
    # print(dic_tracking_movements) # {'person': 0.030303030303030304, 'bench': 0.7878787878787878, 'person.1': 0.0} this the result produced by it



if __name__ == "__main__":
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
    main()

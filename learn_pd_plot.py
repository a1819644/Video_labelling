
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

def main(get_pd_file):
    # manually putted the weight and height of the frame
    w = 1080
    h = 1940
    print(get_pd_file)  # printing all the tables
    get_pd_file.plot()





# main function
if __name__ == "__main__":
    
    # reading all the csv files in the directory "imp"
    current_dir = os.getcwd()
    print(current_dir)
    read_all_csv_files = glob.glob(current_dir + '/imp/*.csv')
    df_list = (pd.read_csv(file) for file in read_all_csv_files)
    #reading each of the csv files one by one
    for df in df_list:
        main(df)

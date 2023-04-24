import pandas as pd
import glob
import os

def main(get_pd_file):
    # print(get_pd_file) printing all the tables
    
    # finding out the movements of the objects in
    increased  = 0
    decreased = 0
    stayed_same = 0
    # readings each of the files to create the over one table

    # first lets create just one pd
    # we don't want to read the rows names our columns names are 
    # same as the rows names
    get_column_names = list(get_pd_file.columns.values)

    # reading 




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
import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist
import os

# using the create_dframe csv
def main(read_dframe):
    x = None
    count = 0;
    print("read_dframe")
    for column in read_dframe.loc[:,'bounding_boxes']:
        # Iterate over column names
        x = eval(column)
        get_current_row =0
        print(x)
        # for i in x:
        #     print(i)

if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    main(read_dframe)
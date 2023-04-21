import pandas as pd
import numpy as np
from numpy import float32, array
import math
from scipy.spatial import distance as dist

def main(read_dframe, read_calculation):
    print(read_dframe)
    result = read_dframe.iloc[[1]]
    print(result)
if __name__ == "__main__":
    read_dframe = pd.read_csv('create_dframe.csv')
    read_calculation = pd.read_csv('calculation_dis.csv')
    main(read_dframe, read_calculation)

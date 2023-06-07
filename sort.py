import os
import re

dir_path = 'distance_tracking'
files = os.listdir(dir_path)
csv_files = [f for f in files if f.endswith('.csv')]

list_files_order = {}

for file in csv_files:
    mystr = str(file)
    get_orderid = re.findall(r'\d+', mystr)
    list_files_order[int(get_orderid[0])] = file

sorted_dict = dict(sorted(list_files_order.items()))
count = 5
for i, file in sorted_dict.items(): 
    if count == i:
        count = i + 5
        continue
    else:
        os.remove(os.path.join(dir_path, file))
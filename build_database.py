# Use this script to write the python needed to complete this task

from unicodedata import name
import pandas as pd
import os
import glob as glb


class Table:
    def __init__(self, name, data_frame):
        self.name = name
        self.data_frame = data_frame

    def __str__(self):
        return f"{self.name}\n{self.data_frame})"

def load_data(): 

    tables = []

    current_directory = os.getcwd()
    all_csv = glb.glob(os.path.join(current_directory + "\data", "*.csv")) #Get all the files in the "data" folder

    for csv in all_csv:
        data_frame = pd.read_csv(csv)
        print('Location:', csv)
        csv_name = csv.split("\\")[-1]
        tables.append(Table(csv_name,data_frame))

    return tables


if __name__ == '__main__':
    tables = load_data()
    print(tables[1])


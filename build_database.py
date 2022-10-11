# Use this script to write the python needed to complete this task

from unicodedata import name
import pandas as pd
import os
import glob as glb
import sqlite3 as db
import requests


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
        csv_name = csv.split("\\")[-1]
        tables.append(Table(csv_name,data_frame))

    return tables

# call API to get what type of glass is needed for a drink
def get_glasses_drink_pair(drinks):
    pairs = []

    for drink in drinks:
        try:
            response = requests.get("http://www.thecocktaildb.com/api/json/v1/1/search.php?s="+str(drink))
        except Exception as e:
            print("Error During the API Call: " + str(e))

        if response.json().get("drinks") is None:
            continue

        response_json = response.json().get("drinks")[0]
        drink_glass = (response_json.get("strDrink"),response_json.get("strGlass"))
        pairs.append(drink_glass)

    return pairs

def initialise_db(cursor):
    print("Creating Tables")
    file = open("data_tables.SQL")
    sql_as_string = file.read()
    cursor.executescript(sql_as_string)
    return 

def insert_data_in_db(glass_report,transactions_report,drink_glass_pairs,cursor):
    try:

        for row in glass_report.itertuples():
            cursor.execute("INSERT INTO allGlass (GlassType,Stock,Bar) VALUES (?,?,?)", (row.glass_type, row.stock, row.bar))
        
        for row in transactions_report.itertuples():
            cursor.execute("INSERT INTO allTransactions (TransactionDate,Drink,Price,Bar) VALUES (?,?,?,?)", (row.TransactionDateTime, row.Drink, row.Price, row.Bar))
        
        for touple in drink_glass_pairs:
            cursor.execute("INSERT INTO drinkGlassPair (Drink,GlassType) VALUES (?,?)", (touple[0],touple[1]))

    except Exception as e:
        print("Issue Logged: " + str(e))
    return




if __name__ == '__main__':
    print("Starting Script Exceution...")
    connection = db.connect("db/mydb.db")
    cursor = connection.cursor()

    print("Initialise Database..")
    initialise_db(cursor)
    print("Done.")
    connection.commit()

    print("Load Data from CSV...")
    tables = load_data()
    glass_report = tables[0].data_frame.dropna()
    transactions_report = tables[1].data_frame.dropna()
    print("Done.")

    all_drinks = transactions_report["Drink"].unique()

    print("Get data from API..")
    drink_glass_pairs = get_glasses_drink_pair(all_drinks)
    print("Done.")

    print("Insert data into DB..")
    insert_data_in_db(glass_report,transactions_report,drink_glass_pairs,cursor)
    print("Done")

    connection.commit()

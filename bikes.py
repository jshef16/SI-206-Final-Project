import unittest
import sqlite3
import json
import os
import requests

def readfile():
    pass

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createBikesTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Bikes (bike_id INTEGER PRIMARY KEY, name TEXT, latitude NUMBER, longitude NUMBER, city TEXT, country TEXT, company TEXT)")
    conn.commit()

def createCitiesTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()

def readAPI():
    url = 'http://api.citybik.es/v2/networks'
    resp = requests.get(url)
    if resp.ok:
        results = resp.json()
        return results
    else:
        print('Request not set correctly')
        return None

def addBikes(cur, conn, bikes_dict):
    pass

def addCities(cur, conn, bikes_dict):
    pass






def main():
    cur, conn = setUpDatabase('bikes.db')
    createBikesTable(cur, conn)
    createCitiesTable(cur, conn)
    bikes_dict = readAPI()
    addCities(cur, conn, bikes_dict)
    addBikes(cur, conn, bikes_dict)



    
if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
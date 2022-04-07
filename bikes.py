from itertools import count
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
    cur.execute("CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.commit()

def createCountriesTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.commit()

def createCompaniesTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    conn.commit()

def createNamesTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Names (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
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
    # get last id inserted into the table
    cur.execute("SELECT * FROM Bikes")
    res = cur.fetchall()
    if len(res) == 0:
        i = 0
    else:
        i = res[-1][0] + 1
    target = i + 25

    bike_list = bikes_dict['networks']
    # start from last id and only insert 25 more entries into the table at once
    for row in range(25):
        if i < target and i < len(bike_list):
            id = i
            name = bike_list[i]['name']
            cur.execute("SELECT id FROM Names WHERE name = ?", (name,))
            name_id = cur.fetchone()[0]

            city = bike_list[i]['location']['city']
            cur.execute("SELECT id FROM Cities WHERE name = ?", (city,))
            city_id = cur.fetchone()[0]

            country = bike_list[i]['location']['country']
            cur.execute("SELECT id FROM Countries WHERE name = ?", (country,))
            country_id = cur.fetchone()[0]

            lat = bike_list[i]['location']['latitude']

            lon = bike_list[i]['location']['longitude']

            if bike_list[i]['company'] == None:
                company = ''
                company_id = None
            else:
                company = bike_list[i]['company'][0]
                cur.execute("SELECT id FROM Companies WHERE name = ?", (company,))
                company_id = cur.fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO Bikes (bike_id, name, city, country, latitude, longitude, company) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name_id, city_id, country_id, lat, lon, company_id))
            i += 1
    conn.commit()

def addCities(cur, conn, bikes_dict):
    cur.execute("SELECT * FROM Cities")
    res = cur.fetchall()
    if len(res) == 0:
        for row in bikes_dict['networks']:
            city = row['location']['city']
            cur.execute("INSERT OR IGNORE INTO Cities (name) VALUES (?)", (city,))
        conn.commit()
    

def addCountries(cur, conn, bikes_dict):
    cur.execute("SELECT * FROM Countries")
    res = cur.fetchall()
    if len(res) == 0:
        for row in bikes_dict['networks']:
            country = row['location']['country']
            cur.execute("INSERT OR IGNORE INTO Countries (name) VALUES (?)", (country,))
        conn.commit()

def addCompanies(cur, conn, bikes_dict):
    cur.execute("SELECT * FROM Companies")
    res = cur.fetchall()
    if len(res) == 0:
        for row in bikes_dict['networks']:
            if row['company'] == None:
                company = ''
            else:
                company = row['company'][0]

            cur.execute("INSERT OR IGNORE INTO Companies (name) VALUES (?)", (company,))
        conn.commit()

def addNames(cur, conn, bikes_dict):
    cur.execute("SELECT * FROM Cities")
    res = cur.fetchall()
    if len(res) == 0:
        for row in bikes_dict['networks']:
            name = row['name']
            cur.execute("INSERT OR IGNORE INTO Names (name) VALUES (?)", (name,))
        conn.commit()






def main():
    # create database
    cur, conn = setUpDatabase('bikes.db')
    # set up tables
    createBikesTable(cur, conn)
    createCitiesTable(cur, conn)
    createCountriesTable(cur, conn)
    createCompaniesTable(cur, conn)
    createNamesTable(cur, conn)
    
    # read in the API
    bikes_dict = readAPI()
    # add the data to the tables as long as reading API goes okay
    if bikes_dict != None:
        addCities(cur, conn, bikes_dict)
        addCountries(cur, conn, bikes_dict)
        addCompanies(cur, conn, bikes_dict)
        addNames(cur, conn, bikes_dict)
        addBikes(cur, conn, bikes_dict)



    
if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
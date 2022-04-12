from unicodedata import category
from xml.sax import parseString
from bs4 import BeautifulSoup
from numpy import equal
import requests
import re
import os
import csv
import unittest

def get_data():
    url = 'https://copenhagenizeindex.eu/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    city_list = []  
    table = soup.find('div', class_ = 'items')
    specific_cities = table.find_all('a', class_ = 'link')
    for specific_city in specific_cities:
        city_rank = specific_city.find('div', class_ = 'index19').text.strip()
        city_name = specific_city.find('div', class_ = 'name colorize').text.strip()
        city_score = specific_city.find('div', class_ = 'total-score total-score--sm').text.strip()
        city_list.append((city_rank, city_name, city_score))
    print(city_list)
    return(city_list)

def main():
    get_data()

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
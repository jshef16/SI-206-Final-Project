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
    city_dict = {}  
    cities = soup.find_all('div', class_ = 'city-info')
    for city in cities:
        city_name = city.find('div', class_ = 'name colorize').text.strip()
    scores = soup.find_all('div', class_ = 'city-score')
    for score in scores:
        city_score = city.find('div', class_ = 'total-score total-score--sm').text.strip()

def main():
    get_data()

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
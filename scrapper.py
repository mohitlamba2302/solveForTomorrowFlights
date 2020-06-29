from bs4 import BeautifulSoup
import urllib3
from requests import get
import requests
from time import sleep
import random
import re
import pprint
import csv
import json
import os

from datetime import datetime
import pickle

def scrape():
	pp = pprint.PrettyPrinter(indent=4)
	head_url = 'https://www.easemytrip.com/'
	built_url = 'https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|22/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
	response = get(built_url)
	# pp.pprint(response.text[:1000])
	soup = BeautifulSoup(response.text, "html.parser")
	
	for rows in soup.find_all('div', {'class': 'col-md-2 col-sm-2 col-xs-5 mr5 cle'}):
		pp.pprint(rows)



	# containers = soup.find_all('div', {'class': 'col-md-2 col-sm-2 col-xs-5 mr5 cle'})	
	# pp.pprint(containers[0])
	#    get data on the webpage that is the actual JD
	# page_content = ''
		
	# file_name = str(i[1]) + '.txt'
	# f= open(os.getenv('BASE_ROOT_PATH') + '/Scrapper/scrapped_indeed.com/scrapped_jds/' + file_name, "w+", encoding="utf-8")
	# f.write(page_content)
	# f.close() 

def build_json():
	cols = ['id', 'fly_from', 'fly_to', 'fly_on', 'original_price', 'discounted price', 'discount_percentage', 'offers']



scrape()

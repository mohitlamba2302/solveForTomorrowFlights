import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from flask import Flask, Response
import json
from flask import jsonify
from random import randint
from flask import request
import hashlib

driver = webdriver.PhantomJS()
app = Flask(__name__)
# app.config["DEBUG"]=True


def get_city_data():
	# url= 'https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json'
	# r = requests.get(url)
	# data= r.json()
	my_cities = []
	# for i in data:
	# 	my_cities.append([i['city']])
	my_cities = ['delhi', 'bangalore', 'mumbai', 'kolkata', 'pune', 'indore']
	return my_cities

def getAirportData(frm, dest):
	url= 'https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json'
	r = requests.get(url)
	data= r.json()

	frm_code = ''
	frm_city = ''
	frm_country = ''
	
	
	to_code=''
	to_city=''
	to_country=''
	for i in data:
		if i['city'].lower().find(frm.lower()) !=- 1:
			frm_code=i['code']
			frm_city=i['city']

			frm_country=i['country']
		
		if i['city'].lower().find(dest.lower()) !=- 1:
			to_code=i['code']
			to_city=i['city']

			to_country=i['country']
			
	return frm_code,frm_city,frm_country,to_code,to_city,to_country


def ease_form_url(frm, dest,date):
	frm_code,frm_city,frm_country,to_code,to_city,to_country = getAirportData(frm,dest)
	url = 'https://flight.easemytrip.com/FlightList/Index?srch='+frm_code+'-'+frm_city.replace(" ","")+'-'+frm_country.replace(" ","")+'|'+to_code+'-'+to_city.replace(" ","")+'-'+to_country.replace(" ","")+'|'+date+'&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
	return url	

def ease_get_html(frm,dest,date):
	url=ease_form_url(frm,dest,date)
	driver.get(url)
	time.sleep(10)
	html = driver.page_source
	return html

def ease_get_children(frm, dest,date):
	soup=BeautifulSoup(ease_get_html(frm,dest,date),'lxml')
	ele = soup.find_all('div',{'class':'fltResult'})
	return ele


def ixigo_form_url(frm, dest, date):
	frm_code,frm_city,frm_country,to_code,to_city,to_country = getAirportData(frm,dest)
	# url = 'https://flight.easemytrip.com/FlightList/Index?srch='+frm_code+'-'+frm_city.replace(" ","")+'-'+frm_country.replace(" ","")+'|'+to_code+'-'+to_city.replace(" ","")+'-'+to_country.replace(" ","")+'|'+date+'&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
	temp_date = date.split('/')
	new_date = ''
	for i in temp_date:
		new_date+=str(i)
	base_url = 'https://www.ixigo.com/search/result/flight/'+frm_code+'/'+to_code+'/'+new_date+'//1/0/0/e?source=Search%20Form'
	# url = 'https://www.cleartrip.com/flights/results?origin=New+Delhi,+IN+-+Indira+Gandhi+Airport+(DEL)&from=DEL&destination=Mumbai,+IN+-+Chatrapati+Shivaji+Airport+(BOM)&to=BOM&depart_date=27/07/2020&adults=1&childs=0&infants=0&class=Economy&airline=&carrier=&intl=n&sd=1593441434422&rnd_one=O'
	# print(base_url)
	return base_url

def ixigo_get_html(frm,dest,date):
	# url=form_url(frm,dest,date)
	# response = requests.get(url)
	# soup = BeautifulSoup(response.text, "html.parser")
	# return soup
	url=ixigo_form_url(frm,dest,date)
	driver.get(url)
	time.sleep(20)
	html = driver.page_source
	return html

def ixigo_get_children(frm, dest,date):
	soup=BeautifulSoup(ixigo_get_html(frm,dest,date),'lxml')
	ele = soup.find_all('div',{'class':'summary-section'})
#     ele = soup.find_all('div')
	return ele

def get_inner_offers(frm, dest,date):
    soup=BeautifulSoup(ease_get_html(frm,dest,date),'lxml')
    elements = driver.find_elements_by_class_name("book-bt-n")
    if(len(elements)>0):
        elements[0].click()
        time.sleep(10)
        html = driver.page_source
        soup=BeautifulSoup(html,'lxml')
        ele = soup.find_all('div',{'class':'coupn_scrl'})
        l = ele[0].text.split('\n')
        l=[x for x in l if x]
        if 'T&C Apply' in l: l.remove('T&C Apply')
        if ' T&C Apply' in l: l.remove(' T&C Apply')
        if 'T&C Apply ' in l: l.remove('T&C Apply ')
        del l[0::2]
        '\n'.join(l)
        return l
    else:
        print("couldn't connect")

def create_dict(frm, dest,date):

	child = ease_get_children(frm,dest,date)
	time.sleep(5)
	offers = get_inner_offers(frm, dest,date)
	content= []
	dic = {}
	for c in child:
		l = c.text.split('\n')
		l=[x for x in l if x]
		# if(l[9] == l[10]):
		# 	continue
		dic={
			"website": "easeMyTrip",
			"airline_name":l[0].replace(" ",""),
			"plane_number":l[1].replace(" ",""),
			"date": date,
			"departure_airport":l[3].replace(" ",""),
			"departure_time":l[2].replace(" ",""),
			"arrival_airport":l[7].replace(" ",""),
			"arrival_time":l[6].replace(" ",""),
			"flight_duration":l[4].replace(" ",""),
			"stops":l[5].replace(" ",""),
			"original_price": l[9].replace(" ",""),
			"reduced_price": l[10].replace(" ",""),
			"offers":offers
			
		}
		content.append(dic)
	
	child = ixigo_get_children(frm, dest, date)
	stop = '0'
 
	for c in child:
		left = c.find('div',{'class':'left-wing'})
		right = c.find('div',{'class':'right-wing'})
		plane_details = c.findAll('div',{'class': 'u-text-ellipsis'})
		if c.find(class_='label br').text!='non-stop':
			stop = c.find(class_='label br').text.split()[0]
		dic={
		  "website": "ixigo",
		  "airline_name":plane_details[1].text,
		  "plane_number":plane_details[2].text,
		  "date": date,
		  "departure_airport":left.find(class_='city u-text-ellipsis').text,
		  "departure_time":left.find(class_='time').text,
		  "arrival_airport":right.find(class_='city u-text-ellipsis').text,
		  "arrival_time":right.find(class_='time').text,
		  "flight_duration":c.find(class_='label tl').text,
		  "stops":stop,
		  "original_price":c.find('span',{'class':''}).text,
		  "reduced_price": c.find('span',{'class':''}).text,
		  "offers": c.find(class_='dynot').text
			
		}
		content.append(dic)
	return content


@app.route('/', methods = ['GET', 'POST'])	
def fetch():
	if request.method == 'POST':

		data = json.loads(request.data)
		if 'source' not in data:
			return 'data is required'

		frm = data['source']
		dest = data['destination']
		date = data['date']
		if frm==dest:
			return {}
		dictionary = create_dict(frm, dest, date)
		json_object = json.dumps(dictionary, indent = 4)
		print('writing')
		r = requests.post('https://flightscrap.herokuapp.com/api/flights/add', data={'flights':json_object}, allow_redirects=True)
		# print(r)
		# with open("sample.json", "w") as outfile: 
		# 	outfile.write(json_object) 
		return json_object

	if request.method == 'GET':
		my_cities = get_city_data()
		date = '22/07/2020'
		for frm in my_cities:
			for dest in my_cities:
				if frm==dest:
					continue
				dictionary = create_dict(frm, dest, '01/08/2020')
				json_object = json.dumps(dictionary, indent = 4)
				print('writing')
				r = requests.post('https://flightscrap.herokuapp.com/api/flights/add', data={'flights':json_object}, allow_redirects=True)
				print(r)

		return 'hello world'

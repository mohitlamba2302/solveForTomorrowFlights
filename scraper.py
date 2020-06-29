#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import time
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# browser = webdriver.Safari()

# url = 'https://www.easemytrip.com/'
# browser.get(url)
# WebDriverWait(browser,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
# from_element = browser.find_element_by_id('FromSector_show')
# from_element.click()
# from_element.send_keys(Keys.HOME)

# # For date 10 Oct 2015
# from_element.send_keys("Mumbai(BOM)")
# from_element.send_keys(Keys.TAB)

# to_element = browser.find_element_by_id('Editbox13_show')
# to_element.click()
# to_element.send_keys(Keys.HOME)

# # For date 10 Oct 2015
# to_element.send_keys("New Delhi(DEL)")
# to_element.send_keys(Keys.TAB)

# # fiv_0_28/06/2020
# ele = browser.find_element_by_id()
# browser.find_element_by_xpath("search").click()
# time.sleep(100)
# browser.close()


# In[2]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.PhantomJS()


url= 'https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json'
r = requests.get(url)
data= r.json()
# print(data)
type(data)

print(data[0])


# In[3]:


def getAirportData(frm, dest):
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


# In[4]:


def form_url(frm, dest,date):
    frm_code,frm_city,frm_country,to_code,to_city,to_country = getAirportData(frm,dest)
    url = 'https://flight.easemytrip.com/FlightList/Index?srch='+frm_code+'-'+frm_city.replace(" ","")+'-'+frm_country.replace(" ","")+'|'+to_code+'-'+to_city.replace(" ","")+'-'+to_country.replace(" ","")+'|'+date+'&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
    return url
    


# In[5]:


def get_html(frm,dest,date):
    url=form_url(frm,dest,date)
    driver.get(url)
    time.sleep(10)


    html = driver.page_source
    return html


# In[6]:


def get_children(frm, dest,date):
    soup=BeautifulSoup(get_html(frm,dest,date),'lxml')
    ele = soup.find_all('div',{'class':'fltResult'})
    return ele
    


# In[7]:


def create_dict(frm, dest,date):
    child = get_children(frm,dest,date)
    dic = {}
    content= []
    for c in child:
        l = c.text.split('\n')
        l=[x for x in l if x]
        if(l[9] == l[10]):
            continue
        dic={
            "Airline name":l[0],
            "Plane number":l[1],
            "Departure airport":l[3],
            "Departure time":l[2],
            "Arrival airport":l[7],
            "Arrival time":l[6],
            "Flight duration":l[4],
            "Stops":l[5],
            "Original price": l[9],
            "Reduced price": l[10],
            "Offers":l[12][:-(len(" Discount Applied"))]
            
        }
        content.append(dic)
    return content


# In[8]:


print(create_dict('delhi','mumbai','01/08/2020'))


# In[ ]:





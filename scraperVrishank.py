#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[7]:


import requests
from bs4 import BeautifulSoup



url= 'https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json'
r = requests.get(url)
data= r.json()
# print(data)
type(data)

print(data[0])


# In[8]:


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


# In[9]:


def form_url(frm, dest,date):
    frm_code,frm_city,frm_country,to_code,to_city,to_country = getAirportData(frm,dest)
    url = 'https://flight.easemytrip.com/FlightList/Index?srch='+frm_code+'-'+frm_city.replace(" ","")+'-'+frm_country.replace(" ","")+'|'+to_code+'-'+to_city.replace(" ","")+'-'+to_country.replace(" ","")+'|01/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
    
    return url
    


# In[13]:


form_url('delhi','mumbai','01/04/2021')


# In[11]:


def get_html(frm,dest,date):
    url=form_url(frm,dest,date)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content)
    return soup


# In[12]:


print(get_html('delhi','mumbai','01/04/2021'))


# In[ ]:





#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import re
import time
import math
import pandas as pd
import requests
import cx_Oracle
import json

con = cx_Oracle.connect('hr/hr@127.0.0.1/orcl')
start = time.time()
source='99_acres'

# scrape offline site
# f=open("D:\\Setup\\NEW SOFTWARE\\Python\\Programs\\rental_search\\99_acres\\Webpages\\Property for rent in Bangalore South - Rental properties in Bangalore South.html")
# soup=BeautifulSoup(f, 'html.parser')

def insert_bangalore_locality():
    city1 = 'Bangalore'
    bangalore_region = ['central-ffid', 'east-ffid', 'west-ffid', 'north-ffid', 'south-ffid']
    base_url = "https://www.99acres.com/rent-property-in-bangalore-"

    for num in range(0, bangalore_region.__len__()):
        new_url = str(base_url) + str(bangalore_region[num])
        page = requests.get(new_url)
        print(page.status_code)
        time.sleep(30)
        soup = BeautifulSoup(page.content, 'html.parser')

        locality = []
        id = []
        city = []
        region = []
        exp = soup.find_all('input', attrs={"id": "filter_data"})
        abc = exp[0].get('value')  # len(exp) = 1
        result = json.loads(str(abc))
        # get Top_Results_Array
        for i in range(0, (result['Locality']['Top_Results_Array'].__len__())):
            city.append(city1)
            region.append(bangalore_region[num].replace("-ffid", ""))
            id.append((result['Locality']['Top_Results_Array'][str(i)]['ID']))
            locality.append((result['Locality']['Top_Results_Array'][str(i)]['LABEL']))

        # get More_Locality_Array
        for j in range(0, (result['Locality']['More_Locality_Array'].__len__())):
            city.append(city1)
            region.append(bangalore_region[num].replace("-ffid", ""))
            id.append((result['Locality']['More_Locality_Array'][str(j)]['ID']))
            locality.append((result['Locality']['More_Locality_Array'][str(j)]['LABEL']))

        data = []
        for i in range(0, id.__len__()):
            data.append([id[i], locality[i], region[i], city[i]])
        print(data)

        cur = con.cursor()
        cur.bindarraysize = 7
        cur.setinputsizes(int, 20)
        cur.executemany("insert into locality(id,name,region,city) values (:1, :2,:3,:4)", data)

        con.commit()
        cur.close()
        con.close()

def get_region(col1_value):
    cur2 = con.cursor()
    cur2.prepare('SELECT distinct region FROM locality WHERE name= :n1')
    # params = (col1_value)
    # cur2.execute(sql, params)
    cur2.execute(None, {'n1': col1_value})
    # cur2.execute('select region from locality where name like ')
    res = cur2.fetchall()[0]
    cur2.close()
    con.close()
    return res

#insert_bangalore_locality
# search_loc='Marathahalli'
search_loc='Kadubeesanahalli'
region=get_region(search_loc)[0]
url=str('https://www.99acres.com/rent-property-in-'+search_loc+str('-bangalore-')+region+'-ffid')
print(url)


# scrape offline site
f=open("D:\\Setup\\NEW SOFTWARE\\Python\\Programs\\rental_search\\99_acres\\Webpages\\Property for rent in Kadubeesanahalli, Bangalore East - Rental properties in Kadubeesanahalli, Bangalore East.html")

soup=BeautifulSoup(f, 'html.parser')

# page = requests.get(url)
# print(page.status_code)
# soup = BeautifulSoup(page.content, 'html.parser')
# # #getting last page number
# max_array=soup.find_all('a',class_='pgsel').__len__()-1
# page_count = soup.find_all('a',class_='pgsel')[max_array]
# # time.sleep(10)
#
# for num in (1,page_count.get('value'+ 1)):
#
#     new_url=str(url)+'-page-'+str(num)
#     page = requests.get(new_url)
#     print (page.status_code)
#     time.sleep(30)

def get_elements(tag_name,attrib_val ):
   records = []
   element_list=soup.find_all(tag_name,class_=attrib_val)
   #print(element_list)
   for element in element_list:
        all_element=element.text.strip()
        #regular experession to remove multiple white space,new line and tab to single space
        records.append(re.sub('\s+', ' ', all_element))
   #print(records)
        #one line for loop
        # all_element=[mb.text.strip() for mb in element]
   return records;

# all_society=get_elements('span','doElip')
# all_hightight=get_elements('div','srpDataWrap')
# all_dealer_posted=get_elements('div','lf f13 hm10 mb5')


# print(all_society)
# print(all_dealer_posted)
# print(all_hightight)
all=soup.find_all("div",class_='srpWrap')

# print (all)
for item in all:
    try:
        a=all.find("div",{"class":"srpDataWrap"})
        print(a)
    except:
        pass
l=[]


for item in all:
    d={}

    try:
        d["source"] = source
    except:
        d["source"] = None

    try:
        d["heading"] = item.find("div", class_="wrapttl").find("a").text
    except:
        d["heading"] = None

    try:
        d["locaton"] =search_loc
    except:
        d["locaton"] = None

    try:
        d["super_buildup"] = item.find("div", class_="srpDataWrap").find("b").text
    except:
        d["super_buildup"] = None

    try:
        d["price"] = item.find("b",itemprop="price").next.replace(",","")
    except:
        d["price"]=None

    try:
        d["description"] = item.find("span",class_='srpDes').text.replace("\n","")
    except:
        d["description"] = None

    try:
        d["society"] = item.find("span", class_="doElip").find("b").text.replace(" ","").replace("\n","")
    except:
        d["society"] = None

    try:
        d["features"] = item.find("div", class_='iconDiv fc_icons fcInit').contents[1].attrs.get('value')
    except:
        d["features"] = None

    try:
        d["floor_info"] = item.find("div", class_='srpDataWrap').contents[9].contents[4].text.replace("/", "").strip()
    except:
        d["floor_info"] = None

    try:
        d["property_age"] = item.find("div",class_='srpDataWrap').contents[9].contents[2].text.replace("/","").replace("  ","").strip()
    except:
        d["property_age"] = None
    try:
        d["property_type"] = item.find("div",class_='srpDataWrap').contents[9].contents[3].text.replace("/","").replace("  ","").strip()
    except:
        d["property_type"] = None


    a = item.find("div", class_='lf f13 hm10 mb5').text.replace("\n", "").replace(" ", "")
    p, q, r = a.split(':')
    z, x = q.split()
    try:
        d["owner_dealer"] = p
    except:
        d["owner_dealer"] = None

    try:
        d["owner_dealer_name"] = z
    except:
        d["owner_dealer_name"] = None

    try:
        d["posted_date"] = r
    except:
        d["posted_date"] = None


    try:
        d["map"] = str("https://www.99acres.com/")+item.find("div", class_="wrapttl").find("i",class_="uline").attrs['data-ttlurl']
    except:
        d["map"] = None


# multiple feature code retrival
#
#     a = item.find("div", class_='iconDiv fc_icons fcInit').contents.__len__()
#     for i in range(1, a - 1):
#         try:
#             n=(item.find("div", class_='iconDiv fc_icons fcInit').contents[i].attrs.get('value'))
#             print(n)
#         except:
#             n=''
    l.append(d)

print(l)
# print(l[0]['price'])

import cx_Oracle

con = cx_Oracle.connect('hr/hr@127.0.0.1/orcl')

cur = con.cursor()
cur.bindarraysize = 7
cur.setinputsizes(int, 20)
cur.executemany("insert into property_detail(SOURCE, HEADING, LOCATION, SUPER_BUILDUP, PRICE, DESCRIPTION, SOCIETY, FEATURES, FLOOR_INFO, PROPERTY_AGE, PROPERTY_TYPE, OWNER_DEALER, OWNER_DEALER_NAME, POSTED_DATE, MAP) /"
                                    "values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)", l)

con.commit()


# df=pd.DataFrame(l)
# df.to_csv("output.csv")

elapsed = (time.time() - start)
print (elapsed, " seconds")



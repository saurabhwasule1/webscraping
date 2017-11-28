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
source1='99_acres'

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


# insert_bangalore_locality
# search_loc='Marathahalli'
# search_loc = 'Kadubeesanahalli'
# search_loc = 'Panathur'
# search_loc = 'Bellandur'
search_loc = 'Marathahalli'

region = get_region(search_loc)[0]
url = str('https://www.99acres.com/rent-property-in-' + search_loc + str('-bangalore-') + region + '-ffid')
print(url)

page = requests.get(url)
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
# #getting last page number
max_array=soup.find_all('a',class_='pgsel').__len__()-1
page_count = soup.find_all('a',class_='pgsel')[max_array]
time.sleep(10)
for num in range(1,int(page_count.get('value'))+1):
    new_url=str(url)+'-page-'+str(num)
    print(new_url)
    page = requests.get(new_url)
    print (page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    all = soup.find_all("div", class_='srpWrap')
    time.sleep(30)
    # print(all)
    for item in all:
        try:
            a = all.find("div", {"class": "srpDataWrap"})
            print(a)
        except:
            pass
    l = []
    source=[]
    price = []
    heading = []
    super_buildup = []
    society = []
    property_age = []
    property_type = []
    floor_info = []
    features = []
    locaton = []
    map1 = []
    description = []
    posted_date = []
    owner_dealer_name = []
    owner_dealer = []
    for item in all:

        try:
            source.append(source1)
        except:
            source.append(None)

        try:
            price.append(item.find("b", itemprop="price").next.replace(",", ""))
        except:
            price.append(None)

        try:
            heading.append(item.find("div", class_="wrapttl").find("a").text)
        except:
            heading.append(None)
        try:
            super_buildup.append(item.find("div", class_="srpDataWrap").find("b").text)
        except:
            super_buildup.append(None)
        try:
            society.append(item.find("span", class_="doElip").find("b").text.replace(" ", "").replace("\n", ""))
        except:
            society.append(None)
        try:
            property_age.append(
                item.find("div", class_='srpDataWrap').contents[9].contents[2].text.replace("/", "").replace("  ",
                                                                                                             "").strip())
        except:
            property_age.append(None)
        try:
            property_type.append(
                item.find("div", class_='srpDataWrap').contents[9].contents[3].text.replace("/", "").replace("  ",
                                                                                                             "").strip())
        except:
            property_type.append(None)
        try:
            floor_info.append(item.find("div", class_='srpDataWrap').contents[9].contents[4].text.replace("/", "").strip())
        except:
            floor_info.append(None)
        try:
            features.append(item.find("div", class_='iconDiv fc_icons fcInit').contents[1].attrs.get('value'))
        except:
            features.append(None)
        a = item.find("div", class_='lf f13 hm10 mb5').text.replace("\n", "").replace(" ", "")
        p, q, r = a.split(':')
        z, x = q.split()
        try:
            owner_dealer.append(p)
        except:
            owner_dealer.append(None)

        try:
            owner_dealer_name.append(z)
        except:
            owner_dealer_name.append(None)

        try:
            posted_date.append(r)
        except:
            posted_date.append(None)

        try:
            description.append(item.find("span", class_='srpDes').text.replace("\n", ""))
        except:
            description.append(None)

        try:
            map1.append(
                str("https://www.99acres.com/") + item.find("div", class_="wrapttl").find("i", class_="uline").attrs[
                    'data-ttlurl'])
        except:
            map1.append(None)

        try:
            locaton.append(search_loc)
        except:
            locaton.append(None)

    # multiple feature code retrival
    #
    #     a = item.find("div", class_='iconDiv fc_icons fcInit').contents.__len__()
    #     for i in range(1, a - 1):
    #         try:
    #             n=(item.find("div", class_='iconDiv fc_icons fcInit').contents[i].attrs.get('value'))
    #             print(n)
    #         except:
    #             n=''

    # print(price.__len__())
    # print(heading.__len__())
    # print(super_buildup.__len__())
    # print(society.__len__())
    # print(property_age.__len__())
    # print(property_type.__len__())
    # print(floor_info.__len__())
    # print(features.__len__())
    # print(locaton.__len__())
    # print(map1.__len__())
    # print(description.__len__())
    # print(posted_date.__len__())
    # print(owner_dealer_name.__len__())
    # print(owner_dealer.__len__())


    list=[]
    for i in range(0,heading.__len__()):
        list.append([source[i],heading [i],locaton [i],super_buildup [i],price [i],description [i],society [i],features [i],floor_info [i],property_age [i],property_type [i],owner_dealer [i],owner_dealer_name [i],posted_date [i],map1 [i]])

    # print(list)


    con1 = cx_Oracle.connect('hr/hr@127.0.0.1/orcl')

    cur = con1.cursor()
    # cur.bindarraysize = 7
    # cur.setinputsizes(int, 20)
    cur.executemany("insert into property_detail(SOURCE, HEADING, LOCATION, SUPER_BUILDUP, PRICE, DESCRIPTION, SOCIETY, FEATURES, FLOOR_INFO, PROPERTY_AGE, PROPERTY_TYPE, OWNER_DEALER, OWNER_DEALER_NAME, POSTED_DATE, MAP)values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)",list)

    con1.commit()
    # con1.close()


    # df=pd.DataFrame(l)
    # df.to_csv("output.csv")

    elapsed = (time.time() - start)
    print(elapsed, " seconds")

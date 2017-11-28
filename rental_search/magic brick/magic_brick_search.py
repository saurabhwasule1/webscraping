#download pages using the Python requests library
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import re
import pandas as pd

#Hit Live site
import requests
# try:
#     page = requests.get("https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Kadubeesanahalli&cityName=Bangalore")
#     print (page.status_code)
# except HTTPError as e:
#     print(e)
# except URLError as e:
#     print(e)
#     print("The server could not be found")
# try:
#     soup = BeautifulSoup(page.content, 'html.parser')
# except AttributeError as e:
#     print(e)
#     print("Tag not found")
# else:

    #scrape offline site
f=open("D:\\Setup\\NEW SOFTWARE\\Python\\Programs\\rental_search\\Webpages\\122 Flats for Rent in Panathur, Bangalore.html")

#     print(e)
# except URLError as e:
#     print(e)
#     print("The server could not be found")
# try:
soup=BeautifulSoup(f, 'html.parser')
# except AttributeError as e:
# print(e)
# print("Tag not found")
# else:

    #scrape offline site
#f=open("D:\\Setup\\NEW SOFTWARE\\Python\\Programs\\rental_search\\Webpages\\91 Flats for Rent in Kadubeesanahalli, Bangalore.html")

#soup=BeautifulSoup(f, 'html.parser')



#get_elements_div Function definition is here
def get_elements_div( str ):
   records = []
   element_list=soup.find_all('div',class_=str)
   #print(element_list)
   for element in element_list:
        all_element=element.text.strip()
        #regular experession to remove multiple white space,new line and tab to single space
        records.append(re.sub('\s+', ' ', all_element))
   #print(records)
        #one line for loop
        # all_element=[mb.text.strip() for mb in element]
   return records;

# Return content between opening and closing tag including tag.
#print(soup.title.text)

search_heading=soup.find('div',class_='SRHeadingPar').text
print(search_heading)

#search_heading2=soup.find('h1',class_='SRHeading').text
#print(search_heading2)

all_property_heading=get_elements_div("proHeading")
all_property_detail=get_elements_div("proDetailsRow__list")
all_property_desc=get_elements_div("showOneLilnerNot c_light_gray fo_11px")
all_property_agent_owner=get_elements_div("proAgent")
all_property_agent_owner_name=get_elements_div("comNameElip")
all_property_posted_date=get_elements_div("proRentPost")

property_status_records=[]
property_status_list=soup.find_all('div',class_='proDetailsRowElm')
for property_status in property_status_list:
    try:
        k = property_status.find('label', text='Status:').next_sibling
        all_property_status = re.sub('[\s+]', ' ', k)
        print(k)
        print(all_property_status)
        property_status_records.append(repr(all_property_status))
    except:
        pass

property_price_record=[]
property_price_list=soup.find_all('div',class_='proPrice')
for property_price in property_price_list:
    try:
        k = property_price.find('span', class_='rsFont').next_sibling
        all_property_price = re.sub('[\s+]', ' ', k.text)
        property_price_record.append((all_property_price))
    except:
        #print("Exception printing"+str(property_price))
        property_price_record.append(('Call for price'))
#print(property_price_record)
property_url=[]
for link in soup.find_all('a',class_='property-sticky-link'):
    property_url.append(str('https://www.magicbricks.com')+link.get('href'))



df=pd.DataFrame(list(zip(all_property_heading,property_price_record,all_property_posted_date,all_property_detail,property_status_records,all_property_desc,all_property_agent_owner,all_property_agent_owner_name,property_url)),
                  columns=['heading','price', 'posted_date','detail','status','description','agent_owner_info','agent_owner_name','url'])
#print(df.columns)
#print(df.values)
from time import gmtime, strftime
#with open('output/magic_brick_data1.txt', 'a') as f:
filename=strftime("Output%Y%m%d%H%M%S.txt", gmtime())
with open('output/'+filename, 'a') as f:
     df.to_csv(f, header=False, sep='|', encoding='utf-8')


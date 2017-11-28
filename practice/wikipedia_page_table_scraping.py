#import the library used to query a website
#import urllib
#specify the url
#wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

#download pages using the Python requests library
import requests

#page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
page = requests.get("https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India")
print (page.status_code)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
# Return content between opening and closing tag including tag.
print(soup.title)
#Return string within given tag
print(soup.title.string)
#Find all the links within page’s <a> tags
print(soup.a)
#all_links=soup.find_all("a")
#for link in all_links:
    #print(link.get("href"))

# command to extract information within all table tags
#all_tables=soup.find_all('table')
#print("printing all table")
#for table in all_tables:
 #   print(table)

#To get particular table(right table)
right_table=soup.find('table', class_='wikitable sortable plainrowheaders')
#Extract the information to DataFrame
#Generate lists
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    states=row.findAll('th') #To store second column data
    if len(cells)==6: #Only extract table body not heading
        A.append(cells[0].find(text=True))
        B.append(states[0].find(text=True))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))
        F.append(cells[4].find(text=True))
        G.append(cells[5].find(text=True))

#import pandas to convert list to data frame
import pandas as pd
df=pd.DataFrame(A,columns=['Number'])
df['State/UT']=B
df['Admin_Capital']=C
df['Legislative_Capital']=D
df['Judiciary_Capital']=E
df['Year_Capital']=F
df['Former_Capital']=G
print(df.columns)
print(df.values)
print(df.index)
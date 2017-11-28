#download pages using the Python requests library
import requests

page = requests.get("https://www.accuweather.com/en/in/bengaluru/204108/month/204108?view=table")
print (page.status_code)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# Return content between opening and closing tag including tag.
print(soup.title)
#To get particular table(right table)
right_table=soup.find('table', class_='calendar-list')
#Generate lists
dates=[]
Hi_lo=[]
Precip=[]
for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    th_cells=row.findAll('th') #To store second column data
    if len(cells)==5:
        Precip.append(cells[1].text)
        dates.append(th_cells[0].text)
print(dates)
print(Precip)

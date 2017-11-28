#download pages using the Python requests library
import requests

#page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
page = requests.get("https://www.accuweather.com/en/in/bengaluru/204108/month/204108?view=table")
print (page.status_code)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
# Return content between opening and closing tag including tag.
print(soup.title)
#To get particular table(right table)
right_table=soup.find('table', class_='calendar-list')
print(right_table)
#Extract the information to DataFrame
#Generate lists
dates=[]
Hi_lo=[]
Precip=[]
Snow=[]
Forcast=[]
Avg_hi_lo=[]

for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    th_row=row.findAll('th') #To store second column data
    if len(cells)==5: #Only extract table body not heading
        dates.append(th_row[0].text)
        Hi_lo.append(cells[0].text)
        Precip.append(cells[1].text)
        Snow.append(cells[2].text)
        Forcast.append(cells[3].text)
        Avg_hi_lo.append(cells[4].text)

print(dates)
print(Precip)
print(Snow)
print(Forcast)
print(Avg_hi_lo)



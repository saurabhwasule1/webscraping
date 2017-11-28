#!/usr/bin/env python
#download pages using the Python requests library
import requests
#page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
#try:
page = requests.get("http://forecast.weather.gov/MapClick.php?x=176&y=128&site=sjt&zmx=&zmy=&map_x=176&map_y=128")
print (page.status_code)
if (page.status_code==200) :
    print("Sucessfully connected")
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
# Return content between opening and closing tag including tag.
print(soup.title)
location_name = soup.find(id="current-conditions")
location_items=location_name.find_all(class_="panel-heading")
loc_name=location_items[0]
print(loc_name.prettify())
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]

loc = location_name.find(class_="panel-title").get_text()
print(loc)
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
periods
short_desc_tags = seven_day.select(".tombstone-container .short-desc")
short_desc = [pt.get_text() for pt in short_desc_tags]
short_desc

temp_tags = seven_day.select(".tombstone-container .temp")
temp = [pt.get_text() for pt in temp_tags]
temp

descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(periods)
print(short_desc)
print(temp)
print(descs)
#import pandas to convert list to data frame

import pandas as pd
weather = pd.DataFrame({
        "locaion":loc,
        "period": periods,
        "short_desc": short_desc,
        "temp": temp,
        "desc":descs
    })
weather
from pandas.io import sql
import MySQLdb

# Connect
db = MySQLdb.connect(host="localhost",
                     user="saurabh",
                     passwd="saurabh",
                     db="test")

cursor = db.cursor()

# Execute SQL select statement
cursor.execute("SELECT * FROM Persons")

# Commit your changes if writing
# In this case, we are only reading data
# db.commit()

# Get the number of rows in the resultset
numrows = cursor.rowcount

# Get and display one row at a time
for x in range(0, numrows):
    row = cursor.fetchone()
    print (row[0], "-->", row[1])

# Close the connection
db.close()

# #print(weather.columns)
# print(weather.values)
# temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
# weather["temp_num"] = temp_nums.astype('int')
#
# print(temp_nums)
#
# is_night = weather["temp"].str.contains("Low")
# weather["is_night"] = is_night
# print(is_night)
# print(weather[is_night])

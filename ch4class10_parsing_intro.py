### Parsing a web page with BeautifulSoup ###
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
pprint(page)
print(page.status_code)
pprint(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
pprint(soup.prettify())
pprint(list(soup.children))
pprint([type(item) for item in list(soup.children)])
html = list(soup.children)[2]
pprint(list(html.children))
body = list(html.children)[3]
pprint(list(body.children))
p = list(body.children)[1]
print(p.get_text())

p_all = soup.find_all('p')  # all instances of a tag
print(p_all)
p_text = soup.find_all('p')[0].get_text()
print(p_text)
print(soup.find('p'))  # the first instance of a tag

# Searching for tags by class and id
page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
print(soup.find_all('p', class_='outer-text'))
print(soup.find_all(id="first"))

# Using CSS selectors
print(soup.select("div p"))

### Real-world example: getting weather forecasts ###
# Go to this webpage http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.Wj-hLlWWaM8
# Hit Browser menu -> Web developer -> Inspector

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
print(period)
print(short_desc)
print(temp)

img = tonight.find("img")
desc = img['title']
print(desc)

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
print(periods)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)

# Construct a dataframe with weather data
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })

temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
print(weather["temp_num"].mean())

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night

### Example: getting the full list of S&P500 tickers ###
def WikiParse():
    """
    Download and parse the Wikipedia list of S&P500
    constituents using requests and BeautifulSoup.
    Returns a list of tuples for to add to MySQL.
    """
    response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(response.text)
# This selects the first table, using CSS Selector syntax and then ignores the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]
# Obtain the symbol information for each row in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
                (
                        tds[0].select('a')[0].text,  # Ticker
                        'stock',
                        tds[1].select('a')[0].text,  # Name
                        tds[3].text,  # Sector
                        'USD'
                        )
                )
    return symbols
                        
symbols = WikiParse()


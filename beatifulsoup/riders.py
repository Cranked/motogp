import pandas as pd
import requests
from bs4 import BeautifulSoup

import config

rider_list = []
country_list = []
times_list = []

api_token = config.APİ_TOKEN


col_list=["Times", "Rider", "Country"]
df = pd.DataFrame(columns=col_list)


def get_content(url,api_token):
    payload = {'api_key': api_token, 'url': url, 'render': 'true'}

    r = requests.get('http://api.scraperapi.com', params=payload)
    if r.status_code != 200:
        return False
    source = BeautifulSoup(r.text)

    times = source.find_all("td", attrs={"class", "table_item times qa_table_times"})
    for time in times:
        t = time.findNext("span", attrs={"class", "font-weight-bold"})
        times_list.append(t.text.strip())

    riders = source.find_all("td", attrs={"class", "table_item rider qa_table_rider"})
    for rider in riders:
        t = rider.findNext("span", attrs={"class", "surname qa_table_rider_surname"})
        rider_list.append(t.text.strip())

    countries = source.find_all("td", attrs={"class", "table_item nation qa_table_rider_nation"})
    for country in countries:
        t = country.findNext("span", attrs={"class", "country"})
        country_list.append(t.text.strip())
    return True


for i in range(1, 23):
    base_url = "https://www.motogp.com/en/statistics/riders-stats/All-seasons/All-circuits/All-classes/All-countries/fast-lap/?page=" + str(
        i)
    if not get_content(base_url, api_token):
        get_content(base_url, api_token)
        i = i - 1
    else:
        print(i)

    df = pd.DataFrame(zip(times_list,rider_list,country_list),columns=col_list)
    df.to_csv("./output/riders-stats.csv", index=False)

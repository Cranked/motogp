import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

season_list = []
rider_list = []
country_list = []
circuit_list = []
constructor_list = []
class_list = []

col_list = ['Season', 'Rider', 'Country', 'Constructor', 'Class']
df = pd.DataFrame(columns=col_list)


def get_content(url):
    payload = {'api_key': 'a7fe435fe6d3bf081fbca6c9ac63f470', 'url': url, 'render': 'true'}

    r = requests.get('http://api.scraperapi.com', params=payload)
    if r.status_code != 200:
        return False
    source = BeautifulSoup(r.text)
    seasons = source.find_all("td", attrs={"class": "table_item season qa_table_season"})
    for season in seasons:
        s = season.findNext("span", attrs={"class": "font-weight-bold"})
        season_list.append(s.text.strip())

    riders = source.find_all("span", attrs={"class": "surname qa_table_rider_surname"})
    for rider in riders:
        rider_list.append(rider.text.strip())

    countries = source.find_all("span", attrs={"class", "country"})
    for country in countries:
        country_list.append(country.text.strip())

    constructures = source.find_all("td", attrs={
        "class": "table_item constructor qa_table_constructor d-none d-sm-table-cell"})
    for constructure in constructures:
        constructor_list.append(constructure.text.strip())

    classes = source.find_all("td",
                              attrs={"class": "table_item category qa_table_category d-table-cell text-right pr-8"})
    for clas in classes:
        class_list.append(clas.text.strip())
    return True


for i in range(1, 15):
    base_url = "https://www.motogp.com/en/statistics/wc-winners/All-seasons/All-classes/All-countries/?page=" + str(
        i)
    if not get_content(base_url):
        i -= 1
        continue
    else:
        print(i)
    df = pd.DataFrame(zip(season_list, rider_list, country_list, constructor_list, class_list), columns=col_list)
    df.to_csv("./output/world-championship-winners.csv", index=False)

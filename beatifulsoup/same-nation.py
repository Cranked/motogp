import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

import config

season_list = []
track_list = []
riders_nation_list = []
class_list = []

api_token = config.APİ_TOKEN


col_list = ['Season', 'Track', 'Riders` Nation', 'Class']
df = pd.DataFrame(columns=col_list)


def get_content(url,api_token):
    payload = {'api_key': api_token, 'url': url, 'render': 'true'}

    r = requests.get('http://api.scraperapi.com', params=payload)
    code = r.status_code
    if code == 200:
        source = BeautifulSoup(r.text)
        seasons = source.find_all("td", attrs={"class": "table_item season qa_table_season"})
        for season in seasons:
            s = season.findNext("span", attrs={"class": "font-weight-bold"})
            season_list.append(s.text.strip())

        tracks = source.find_all("td", attrs={"class", "table_item track qa_table_track"})
        for track in tracks:
            t = track.findNext("p", attrs={"class", "mb-0"})
            track_list.append(t.text.strip())

        riders_nations = source.find_all("td", attrs={"class", "table_item nation qa_table_rider_nation px-0"})
        for nation in riders_nations:
            r = nation.findNext("span", attrs={"class": "country"})
            riders_nation_list.append(r.text.strip())

        classes = source.find_all("td",
                                  attrs={"class": "table_item category qa_table_category d-table-cell text-right pr-8"})
        for clas in classes:
            class_list.append(clas.text.strip())
        return True
    return False


for i in range(1, 15):
    base_url = "https://www.motogp.com/en/statistics/sm-podium-lockouts/All-seasons/All-circuits/All-classes/All-countries/?page=" + str(
        i)
    if not get_content(base_url,api_token):
        get_content(base_url,api_token)
        i = i - 1
    else:
        print(i)
    df = pd.DataFrame(zip(season_list, track_list, riders_nation_list,class_list), columns=col_list)
    df.to_csv("./output/same-nation-podium-lockouts.csv", index=False)

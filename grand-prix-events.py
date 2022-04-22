import pandas as pd
import requests
from bs4 import BeautifulSoup

import config

tracks_list = []
country_list = []
times_list = []

api_token = config.APİ_TOKEN


col_list=["Times", "Track", "Country"]
df = pd.DataFrame(columns=col_list)

def get_content(url,api_token):
    payload = {'api_key': api_token, 'url': url, 'render': 'true'}

    r = requests.get('http://api.scraperapi.com', params=payload)
    code = r.status_code
    if code == 200:
        source = BeautifulSoup(r.text)
        times = source.find_all("td", attrs={"class", "table_item times qa_table_times"})
        for time in times:
            t = time.findNext("span", attrs={"class", "font-weight-bold"})
            times_list.append(t.text.strip())

        tracks = source.find_all("td", attrs={"class", "table_item circuit qa_table_circuit"})
        for track in tracks:
            t = track.findNext("p", attrs={"class", "mb-0"})
            tracks_list.append(t.text.strip())

        countries = source.find_all("td", attrs={"class", "table_item nation qa_table_rider_nation"})
        for country in countries:
            t = country.findNext("span", attrs={"class", "country"})
            country_list.append(t.text.strip())
        return True
    return False


for i in range(1, 5):
    base_url = "https://www.motogp.com/en/statistics/gp-events-held/All-seasons/All-circuits/All-classes/All-countries/?page=" + str(
        i)
    if not get_content(base_url,api_token):
       get_content(base_url,api_token)
       i=i-1
    else:
        print(i)
    df = pd.DataFrame(zip(times_list, tracks_list, country_list), columns=col_list)
    df.to_csv("./output/grand-prix-events-held.csv", index=False)


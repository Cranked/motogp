import pandas as pd
import requests
from bs4 import BeautifulSoup

season_list = []
constructor_list = []
class_list = []

col_list = ['Season', 'Constructor', 'Class']
df = pd.DataFrame(columns=col_list)


def get_content(url):
    payload = {'api_key': '6b87ed77fc485b87e91cd12c0f1b925c', 'url': url, 'render': 'true'}

    r = requests.get('http://api.scraperapi.com', params=payload)
    code = r.status_code
    if code == 200:
        source = BeautifulSoup(r.text)
        seasons = source.find_all("td", attrs={"class": "table_item season qa_table_season"})
        for season in seasons:
            s = season.findNext("span", attrs={"class": "font-weight-bold"})
            season_list.append(s.text.strip())

        constructures = source.find_all("td", attrs={
            "class": "table_item constructor qa_table_constructor"})
        for constructure in constructures:
            constructor_list.append(constructure.text.strip())

        classes = source.find_all("td",
                                  attrs={"class": "table_item category qa_table_category d-table-cell text-right pr-8"})
        for clas in classes:
            c = clas.findNext("p", attrs={"class": "mb-0"}).text.strip()
            class_list.append(c)
        return True
    return False


for i in range(1, 16):
    base_url = "https://www.motogp.com/en/statistics/constructors-wc/All-seasons/All-classes/?page=" + str(
        i)
    if not get_content(base_url):
        get_content(base_url)
        i = i - 1
    else:
        print(i)
    df = pd.DataFrame(zip(season_list, constructor_list, class_list), columns=col_list)
    df.to_csv("./output/constructure-world-championship.csv", index=False)

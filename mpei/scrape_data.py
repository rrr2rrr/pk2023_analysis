from src.constants import headers

import requests
from bs4 import BeautifulSoup

import pandas as pd
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from src.classes import UniversityDirection, StudentsPrepWorkflow


def get_all_target_links():
    response = requests.get('https://pk.mpei.ru/inform/list.html', headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    all_group_links = soup.find_all('div', {'class':'groupFilterFormO'})[0].find_all('table')[0].find_all('a', {'class':"competitive-group"})
    len(all_group_links)
    target_links = [l for l in all_group_links if 'bacc' in l.get('href')]
    return target_links


def get_info_from_dir_page(url):
    response = requests.get('https://pk.mpei.ru/' + url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    dir = soup.find_all('div', {'class': "competitive-group"})[0].text
    places_text = [x for x in soup.find_all('div', {'class': "title1"})[0].getText("\n").split('\n') if
                   'Количество вакантных мест' in x][0]
    places_count = int(places_text.replace("Количество вакантных мест: ", ""))
    key = url.replace('/inform/list', '').replace('.html', '')
    ud = UniversityDirection(key=key, places=places_count,
                             properties={'name': dir, 'url': url.replace('/inform/list', '')})

    df = pd.read_html(response.text)[0]
    df.columns = [x[1] for x in df.columns]
    return key, ud, df
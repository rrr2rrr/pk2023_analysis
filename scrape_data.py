from bs4 import BeautifulSoup
import requests
from constants import headers
import pandas as pd
import re
import os

import warnings
from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def get_main_links():
    response = requests.get('https://priem.mai.ru/rating/', headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    place_url = [x.get('value') for x in soup.select('#place')[0].select('option') if x.text == 'МАИ'][0]
    response = requests.get(f'https://public.mai.ru/priem/rating/data/{place_url}.html', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features="lxml")
    level_select = [x.get('value') for x in soup.select('option') if x.text == 'Бакалавриат'][0]
    response = requests.get(f'https://public.mai.ru/priem/rating/data/{level_select}.html', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features="lxml")
    pay_select = [x.get('value') for x in soup.select('option') if x.text == 'Бюджет'][0]
    response = requests.get(f'https://public.mai.ru/priem/rating/data/{pay_select}.html', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features="lxml")
    form_select = [x.get('value') for x in soup.select('option') if x.text == 'очная'][0]
    response = requests.get(f'https://public.mai.ru/priem/rating/data/{form_select}.html', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features="lxml")
    spec_select = [{'link': x.get('value'), 'name': x.text} for x in soup.select('option') if x.get('value') != '0']
    return spec_select


def get_all_links():
    spec_selects = []
    response = requests.get('https://priem.mai.ru/rating/', headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    place_urls = [(x.get('value'), x.text) for x in soup.select('#place')[0].select('option') if x.get('value') != '0']
    for place_url, place_name in place_urls:
        response = requests.get(f'https://public.mai.ru/priem/rating/data/{place_url}.html', headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features="lxml")
        level_selects = [(x.get('value'), x.text) for x in soup.select('option') if x.get('value') != '0']
        for level_select, level_name in level_selects:
            response = requests.get(f'https://public.mai.ru/priem/rating/data/{level_select}.html', headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, features="lxml")
            pay_selects = [(x.get('value'), x.text) for x in soup.select('option') if x.get('value') != '0']
            for pay_select, pay_name in pay_selects:
                response = requests.get(f'https://public.mai.ru/priem/rating/data/{pay_select}.html', headers=headers)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, features="lxml")
                form_selects = [(x.get('value'), x.text) for x in soup.select('option') if x.get('value') != '0']
                for form_select, form_name in form_selects:
                    response = requests.get(f'https://public.mai.ru/priem/rating/data/{form_select}.html',
                                            headers=headers)
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, features="lxml")
                    spec_select = []
                    for x in soup.select('option'):
                        if x.get('value') != '0':
                            spec_select.append({'link': x.get('value'),
                                                'name': x.text,
                                                'place_url': place_name,
                                                'level_select': level_name,
                                                'pay_select': pay_name,
                                                'form_select': form_name,
                                                })
                    spec_selects += spec_select
    return spec_selects


def scrape_abitu(spec_select):
    target_data = []
    for spec in spec_select:
        link = spec['link']
        name = spec['name']
        response = requests.get(f'https://public.mai.ru/priem/rating/data/{link}.html', headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 404:
            raise Exception('Please, rerun script')
        DIR = f'cache/{link.split("_")[0]}'
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        with open(f'{DIR}/{link}.html', 'w') as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, features="lxml")
        h4s = soup.find_all("h4", string=re.compile('Лица, поступающие по общему конкурсу'))
        places_count = h4s[0].text[37:] if len(h4s) > 0 else 'нет общего конкурса'
        if len(h4s) > 0:
            dfs = pd.read_html(response.text)
            target_df = dfs[-1]
            df = target_df
            df_original = df[df['Подлинник или\xa0копия документа об\xa0образовании'].apply(
                lambda x: True if 'Подлинник' in x else False)]
            print(
                f'{link}: {name} {places_count}, подано {target_df.shape[0]}, из них оригиналы {df_original.shape[0]}')
            try:
                places_count = int(places_count.replace('(мест: ', '').replace(')', ''))
            except:
                places_count = 0
            target_data.append({
                'dir': dict(**spec, places=places_count),
                'df': target_df
            })
    return target_data

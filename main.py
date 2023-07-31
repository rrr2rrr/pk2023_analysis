from scrape_data import get_all_links
from scrape_data import scrape_abitu
from workflow import get_all_guys2, aggregate_guys, get_target_dict, fill_directions2
from log_results import print_min_points2
import pandas as pd
from dataclasses import asdict


def run_main_task(podlinnik=True):
    links = get_all_links()
    target_data = scrape_abitu(links)
    target_data = [x for x in target_data if x['dir']['level_select'] not in ('Среднее профессиональное образование')]
    df_all_guys = get_all_guys2(target_data)
    df_aggr = aggregate_guys(df_all_guys)
    all_guys_aggr = get_target_dict(df_aggr, podlinnik)
    listUniversityDirection = fill_directions2(target_data, all_guys_aggr)
    print_min_points2(listUniversityDirection)
    print('\n\n\n')
    df_min_points = pd.DataFrame([dict(**asdict(x), min=x.get_min_points()) for x in listUniversityDirection.values()])
    del df_min_points['students']
    df_min_points.to_csv('export.csv')
    print(df_min_points[['name', 'min', 'places', 'place', 'form', 'pay', 'level', 'link']].to_markdown())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_main_task(podlinnik=True)

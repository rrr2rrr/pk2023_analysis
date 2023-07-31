import pandas as pd

from mpei.scrape_data import get_all_target_links, get_info_from_dir_page
from src.classes import ListUniversityDirection, StudentsPrepWorkflow


def run_main_task(podlinnik=True):
    target_links = get_all_target_links()
    sw = StudentsPrepWorkflow()
    lud = ListUniversityDirection()
    students_dfs = {}
    for idx, link in enumerate(target_links):
        url = link.get('href')
        key, ud, students_df = get_info_from_dir_page(url)
        lud[key] = ud
        students_dfs[key] = students_df
        print(
            f'{(idx + 1)}/{len(target_links)}. Загружено направление {ud.properties["name"]}. '
            f'Мест {ud.places}. Подано заявлений {len(students_df)}.')

    all_students = []
    for key, df in students_dfs.items():
        df = df[df['Примечание'].apply(lambda x: False if 'Зачисляется в другой КГ' in str(x) else True)]
        st_df = df[['СНИЛС или Рег.номер', 'Сумма', 'Оригинал', 'Приоритет']]
        st_df.columns = ['snils', 'points', 'podl', 'priority']
        st_df['snils'] = st_df['snils'].apply(lambda x: x.replace('СНИЛС: ', ''))
        st_df['dir_key'] = key
        st_df['podl'] = st_df['podl'].apply(lambda x: True if 'да' in x else False)
        students = sw.df2StudentWithPriority(st_df)
        all_students += students

    students = sw.to_StudentsUniqueList(all_students)
    students_filtered = sw.filter_StudentsUniqueList(students, podlinnik)
    for st in students_filtered:
        st.dirs_priority = {x['priority']: x['dir_key'] for x in st.dirs_priority}

    lud.fill_guys(students_filtered)

    df = pd.DataFrame((lud.values()))
    del df['students']
    df['min'] = df['key'].apply(lambda x: lud[x].get_min_points())
    df['name'] = df['properties'].apply(lambda x: x['name'])
    del df['properties']
    df.to_csv("export.csv")
    print(df.to_markdown())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_main_task(podlinnik=True)

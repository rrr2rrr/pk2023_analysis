import pandas as pd
from classes import Student, UniversityDirection, UniversityDirection2

def get_all_guys(target_data):
    all_guys = []
    for data in target_data:
        try:
            df = data['df'][
                ['СНИЛС/УКП', 'Сумма конкурсных баллов', 'Подлинник или\xa0копия документа об\xa0образовании', 'Приоритет']]
        except:
            raise
        df.columns = ['snils', 'points', 'podl', 'priority']
        df['dir'] = data['dir']['name']
        all_guys += df.to_dict('records')
    df_all_guys = pd.DataFrame(all_guys)
    return df_all_guys


def get_all_guys2(target_data):
    all_guys = []
    for data in target_data:
        try:
            df = data['df'][
                ['СНИЛС/УКП', 'Сумма конкурсных баллов', 'Подлинник или\xa0копия документа об\xa0образовании', 'Приоритет']]
        except:
            raise
        df.columns = ['snils', 'points', 'podl', 'priority']
        df['dir'] = data['dir']['link']
        all_guys += df.to_dict('records')
    df_all_guys = pd.DataFrame(all_guys)
    return df_all_guys


def aggregate_guys(df_all_guys):
    df_all_guys.sort_values(['points', 'snils', 'priority'], ascending=[False, True, True], inplace=True)
    df_all_guys['dirs_priority'] = df_all_guys[['priority', 'dir']].to_dict('records')
    df_aggr = df_all_guys[['points', 'snils', 'podl', 'dirs_priority']].groupby(['points', 'snils', 'podl']).agg(
        list).reset_index()
    df_aggr.sort_values(['points', 'snils'], ascending=[False, True], inplace=True)
    return df_aggr

def get_target_dict(df_aggr, ONLY_PODLINNIK=True):
    if ONLY_PODLINNIK:
        df_aggr_target = df_aggr[df_aggr['podl'].apply(lambda x: True if 'Подлинник' in x else False)]
    else:
        df_aggr_target = df_aggr
    all_guys_aggr = df_aggr_target.to_dict('records')
    return all_guys_aggr


def fill_directions(target_data, all_guys_aggr):
    listUniversityDirection = {}

    for data in target_data:
        name, places = data['dir']['name'],  data['dir']['places']
        listUniversityDirection[name] = UniversityDirection(name, places, list())

    for guy in all_guys_aggr:
        points, snils, podl, dirs_priority = guy.values()
        if not student2dirs(listUniversityDirection, guy):
            pass
            # print(f'Student with {snils} will not be accepted to MAI. He has {points} EGE points')

    return listUniversityDirection


def student2dirs(listUniversityDirection, guy):
    points, snils, podl, dirs_priority = guy.values()
    for dir_priority in dirs_priority:
        priority, dir = dir_priority.values()
        student = Student(snils, points, podl, priority)
        ud = listUniversityDirection[dir]
        if ud.add(student):
            return True
    return False


def fill_directions2(target_data, all_guys_aggr):
    listUniversityDirection = {}

    for data in target_data:
        link, name, place, level, pay, form, places = data['dir'].values()
        listUniversityDirection[link] = UniversityDirection2(link, name, place, level, pay, form, places, list())

    for guy in all_guys_aggr:
        points, snils, podl, dirs_priority = guy.values()
        if not student2dirs(listUniversityDirection, guy):
            pass
            # print(f'Student with {snils} will not be accepted to MAI. He has {points} EGE points')

    return listUniversityDirection
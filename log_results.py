import re


def print_min_points(listUniversityDirection, filter_dirs=None):
    if filter_dirs:
        ud_list = [ud for ud in listUniversityDirection.values() if
                   len(re.findall(rf'({"|".join(filter_dirs.split(","))})', ud.name)) > 0]
    else:
        ud_list = listUniversityDirection.values()
    for ud in ud_list:
        print(f'Направление {ud.name} будет иметь минимальный балл {ud.get_min_points()}')


def print_min_points2(listUniversityDirection2, filter_dirs=None):
    if filter_dirs:
        ud_list = [ud for ud in listUniversityDirection2.values() if
                   len(re.findall(rf'({"|".join(filter_dirs.split(","))})', ud.name)) > 0]
    else:
        ud_list = listUniversityDirection2.values()
    for ud in ud_list:
        print(f'Направление {ud.link} - {ud.name} будет иметь минимальный балл {ud.get_min_points()}')

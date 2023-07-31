from dataclasses import dataclass, asdict, field
import pandas as pd


@dataclass
class Student:
    snils: str
    points: int
    podl: bool
    priority: int


@dataclass
class StudentWithPriority:
    snils: str
    points: int
    podl: bool
    priority: int
    dir_key: str


@dataclass
class StudentWithPriorities:
    snils: str
    points: int
    podl: bool
    dirs_priority: dict[int, str]


class StudentsPrepWorkflow:
    @staticmethod
    def list_dataclass2df(lst):
        return pd.DataFrame([asdict(x) for x in lst])

    @staticmethod
    def df2StudentWithPriority(st_df) -> list[StudentWithPriority]:
        return [StudentWithPriority(x['snils'],
                                    x['points'],
                                    x['podl'],
                                    x['priority'],
                                    x['dir_key']) for x in st_df.to_dict('records')]

    def df2StudentWithPriorities(self, df_aggr) -> list[StudentWithPriorities]:
        return [StudentWithPriorities(x['snils'],
                                      x['points'],
                                      x['podl'],
                                      x['dirs_priority']
                                      ) for x in df_aggr.to_dict('records')]

    def to_StudentsUniqueList(self, students: list[StudentWithPriority]) -> list[StudentWithPriorities]:
        df_all_guys = self.list_dataclass2df(students)
        df_all_guys.sort_values(['points', 'snils', 'priority'], ascending=[False, True, True], inplace=True)
        df_all_guys['dirs_priority'] = df_all_guys[['priority', 'dir_key']].to_dict('records')
        df_aggr = df_all_guys[['points', 'snils', 'podl', 'dirs_priority']].groupby(
            ['points', 'snils', 'podl']).agg(list).reset_index()
        df_aggr.sort_values(['points', 'snils'], ascending=[False, True], inplace=True)
        return self.df2StudentWithPriorities(df_aggr)

    def filter_StudentsUniqueList(self, students=list[StudentWithPriorities], podlinnik=True):
        df_aggr = self.list_dataclass2df(students)
        if podlinnik:
            df_aggr_target = df_aggr[df_aggr['podl']]
        else:
            df_aggr_target = df_aggr
        return self.df2StudentWithPriorities(df_aggr_target)


@dataclass
class UniversityDirection:
    key: str
    places: int
    properties: dict[str, str]
    students: list[Student | StudentWithPriorities] = field(default_factory=lambda: [])

    def add(self, s: Student | StudentWithPriorities):
        if len(self.students) < self.places:
            self.students.append(s)
            return True
        else:
            return False

    def get_min_points(self):
        if len(self.students) > 0:
            return min([x.points for x in self.students])
        else:
            return -1


@dataclass
class ListUniversityDirection(dict[str, UniversityDirection]):
    # directions: dict[str, UniversityDirection]

    def student2dirs(self, guy: StudentWithPriorities):
        dirs_priority_sorted = dict(sorted(guy.dirs_priority.items()))
        for priority, dir in dirs_priority_sorted.items():
            ud = self[dir]
            if ud.add(guy):
                return True
        return False

    def fill_guys(self, all_guys_aggr: list[StudentWithPriorities]):
        for guy in all_guys_aggr:
            if not self.student2dirs(guy):
                pass


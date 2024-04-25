import pandas as pd


def get_review_data(sheet_names):
    all_dfs = {}
    for sheet_name in sheet_names:
        all_dfs[sheet_name] = pd.read_excel("Derek_Performance_Review (1).xlsx", sheet_name=sheet_name)

    return all_dfs


def get_courses_data():
    import json
    return json.load(open('course (1).json', 'r'))


def get_goals_data():
    import docx2txt
    return docx2txt.process('Field Tech Lead Job aid (1).docx')

import pandas as pd

from younet_rnd_infrastructure.tri.find_place import find_place
from younet_rnd_infrastructure.tri.common import file_tool


def standardize_name():
    school_df = pd.read_csv('./database/selective_school_100.csv', encoding='utf-8')
    school_name = list(school_df['name'])
    school_name_detail = find_place.get_full_info_places(school_name)
    school_name_detail.to_csv('./database/school_detail.csv', index=None, encoding='utf-8')

if __name__ == '__main__':
    school_name_df = pd.read_csv('./database/school_detail.csv', encoding='utf-8')
    school_name_df.rename(columns={'raw_name': 'school_raw_name'}, inplace=True)

    data_df = pd.read_csv('./temp/data_detail.csv', encoding='utf-8')

    data_with_school_name_df = pd.merge(data_df, school_name_df, on='school_raw_name', how='left', suffixes=('', '_school'))
    group_school = dict()
    for name, group in data_with_school_name_df.groupby('place_id'):
        group_school[name] = list(group['id'])
    file_tool.save_json('database/group_school.json', group_school)
    print 'Done'
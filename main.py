# -*- coding: utf-8 -*-
import ast
import pandas as pd
import pickle

from younet_rnd_infrastructure.tri.common import utils
from younet_rnd_infrastructure.tri.common import file_tool
from younet_rnd_infrastructure.tri.facebook_crawl_unit.get_list_friends import get_list_friends

SEP = '#$@%()'


def extract_data():
    data_df = pd.read_csv('./input/data_700k.csv', encoding='utf-8')
    school_info_name = []
    school_info_type = []
    school_info_year = []
    data_df['education'].fillna('{}', inplace=True)
    for i in range(data_df.shape[0]):
        print i
        education_info = ast.literal_eval(data_df.loc[i, 'education'])

        schools_name = []
        schools_type = []
        schools_year = []
        for school in education_info:
            school_name = ''
            school_type = ''
            school_year = ''
            if 'school' in school.keys():
                school_name = school['school']['name']
            if 'type' in school.keys():
                school_type = school['type']
            if 'year' in school.keys():
                school_year = school['year']['name']
            schools_name.append(school_name)
            schools_type.append(school_type)
            schools_year.append(school_year)

        if len(schools_name) != 0:
            school_info_name.append(reduce(lambda x, y: x + SEP + y, schools_name))
        else:
            school_info_name.append('')

        if len(schools_type) != 0:
            school_info_type.append(reduce(lambda x, y: x + SEP + y, schools_type))
        else:
            school_info_type.append('')

        if len(schools_year) != 0:
            school_info_year.append(reduce(lambda x, y: x + SEP + y, schools_year))
        else:
            school_info_year.append('')

    data_df['school_name'] = school_info_name
    data_df['school_type'] = school_info_type
    data_df['school_year'] = school_info_year
    data_df.to_csv('./temp/data_detail.csv', encoding='utf-8', index=None)
    print 'Done'


def extract_data_v2():
    data_df = pd.read_csv('./input/data_700k.csv', encoding='utf-8')
    data_df['education'].fillna('{}', inplace=True)
    result = []
    for i in range(data_df.shape[0]):
        print i
        education_info = ast.literal_eval(data_df.loc[i, 'education'])
        for school in education_info:
            school_name = ''
            school_type = ''
            school_year = ''
            if 'school' in school.keys():
                school_name = school['school']['name']
            if 'type' in school.keys():
                school_type = school['type']
            if 'year' in school.keys():
                school_year = school['year']['name']
            record = data_df.iloc[i, :].to_dict()
            record['school_raw_name'] = school_name
            record['school_type'] = school_type
            record['school_year'] = school_year
            result.append(record)
    result_df = pd.DataFrame(result)
    result_df.to_csv('./temp/data_detail.csv', encoding='utf-8', index=None)
    print 'Done'
    return result_df


def clean_data(data_detail_df):
    data_detail_df.dropna(axis=0, subset=['school_raw_name'], how='any', inplace=True)
    data_detail_df.index = range(data_detail_df.shape[0])
    return data_detail_df


def build_set_school(data_df):
    school_names = []
    school_types = []
    for i in range(data_df.shape[0]):
        print '%s/%s' % (i, data_df.shape[0])
        names = data_df.loc[i, 'school_name'].split(SEP)
        types = data_df.loc[i, 'school_type'].split(SEP)
        school_names.extend(names)
        school_types.extend(types)
        if len(school_names) != len(school_types):
            print i
            raise Exception
    df = pd.DataFrame({'name': school_names, 'type': school_types})
    return df


def read_dump_file(filename):
    with open(filename, 'rb') as f:
        tmp = pickle.load(f)
        return tmp


if __name__ == '__main__':

    data_df = pd.read_csv('./temp/data_detail.csv', encoding='utf-8')
    print 'Done'
    # list_ids = list(set(list(data_df['id'])))
    # # 109.609470844 s -> 50 id
    # friends = utils.time_measure(utils.run_multi_url_request_with_time_constraint,
    #                              [get_list_friends.get_friends_id, 1, [list_ids[:50]]])
    friendships = file_tool.load_json('./temp/friends_0_1k.json')

    def convert_list_to_dict(list_friendships):
        friendships = dict()
        for item in list_friendships:
            friendships[item['id']] = item['friends']
        return friendships

    x = convert_list_to_dict(friendships)
    print 'Done'


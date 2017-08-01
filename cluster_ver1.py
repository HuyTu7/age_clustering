import pandas as pd
import json
import pickle
import csv
from json import dumps, loads, JSONEncoder, JSONDecoder
from younet_rnd_infrastructure.tri.common import file_tool


class FriendshipManager():
    def __init__(self):
        pass

    @staticmethod
    def loader():
        print 'Loading data ...'
        friendships = list()
        for i in range(1, 2):
            friendships.extend(file_tool.load_json('./temp/friends_%sk_%sk.json' % (i, i+1)))


        def convert_list_to_dict(list_friendships):
            friendships = dict()
            for item in list_friendships:
                if item['id'] in friendships.keys():
                    friendships[item['id']].update(item['friends'])
                else:
                    friendships[item['id']] = set(item['friends'])
            return friendships


        def filling(friendships_d):
            for key, value in friendships_d.items():
                if value:
                    for id in value:
                        if id in set(friendships_d.keys()):
                            friendships_d[id].add(key)
            print 'DONE FILLING'
            print count
            return friendships_d


        def sorting(friendships_d):
            friendships = dict.fromkeys(['ids', 'friends'])
            count = 0
            ids = set(friendships_d.keys())
            for id in ids:
                friends = ids.intersection(friendships_d[id])
                friendships[id] = friends
                count += 1
            print 'DONE SORTING'
            return friendships


        def set_to_list(friendships_d):
            friendships_dict = dict((k, list(v)) for k, v in friendships_d.iteritems() if v)
            return friendships_dict


        friendships_d = convert_list_to_dict(friendships)
        print 'Test d: %s, %s' % (friendships_d.keys()[0], len(friendships_d[friendships_d.keys()[0]]))
        friendships_d1 = sorting(friendships_d)
        print 'Test d1: %s, %s' % (friendships_d1.keys()[0], len(friendships_d1[friendships_d1.keys()[0]]))
        friendships_d2 = set_to_list(filling(friendships_d1))
        FriendshipManager.friendship_dict1 = friendships_d1
        FriendshipManager.friendship_dict2 = friendships_d2
        print 'Total id with the single nodes: %s' % len(FriendshipManager.friendship_dict1.keys())
        print 'Total id after fillings and without the single nodes: %s' % len(FriendshipManager.friendship_dict2.keys())
        f = open('result3.json', 'w')
        try:
            json.dump(FriendshipManager.friendship_dict2, f)
        finally:
            f.close()

def save_graph(data, filename):
    graph_d = dict.fromkeys(['ids', 'partitions'])
    graph_file = open(filename, 'w')
    count = 0
    for item in data:
        graph_d[count] = item
        count += 1
    try:
        json.dump(graph_d, graph_file)
    finally:
        graph_file.close()


def dfs(graph):
    unvisited = set()
    for vertex in graph.keys():
        unvisited.add(vertex)
    partitions = []
    while unvisited:
        start = next(iter(unvisited))
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                unvisited.remove(vertex)
                stack.extend(set(graph[vertex]) - visited)
        print "Finish 1 group"
        partitions.append(list(visited))
    return partitions


def sorting1(friendships_d):
    friendships = dict.fromkeys(['ids', 'friends'])
    count = 0
    ids = set(friendships_d.keys())
    for id in ids:
        friends = ids.intersection(friendships_d[id])
        friendships[id] = friends
        count += 1
    print 'DONE SORTING'
    return friendships


def set_to_list(friendships_d):
    friendships_dict = dict((k, list(v)) for k, v in friendships_d.iteritems() if v)
    return friendships_dict


def save_list(data, name):
    with open(name, 'wb') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    with open('result5.json') as f1:
        temp = json.load(f1, encoding="UTF-8")
    with open('groups_by_school_18k_age.json') as f2:
        schools = json.load(f2, encoding="UTF-8")
    length = 0
    for s in schools.values():
        length += len(s)
    print length
    school_ids = []

    for k, v in schools.items():
        school_ids.append(k)
    ids = []
    index = 0
    id_schools = dict()
    for s in school_ids:
        ids += schools[s]
        for p in schools[s]:
            id_schools[p] = index
        index += 1
    print len(ids)
    dataset = dict()
    #filters out ids that does not have school info
    for id in ids:
        if str(id) in temp:
            dataset[str(id)] = temp[str(id)]

    #sorting again to make sure that friends ids of one user
    #is in the keys of the dictionary
    dataset = sorting1(dataset)
    print len(dataset.keys())
    final_dataset = set_to_list(dataset)
    print len(final_dataset.keys())
    friends_f = open('ids_and_friends.json', 'w')
    try:
        json.dump(final_dataset, friends_f)
    finally:
        friends_f.close()
    
    schools_f = open('school_ids.json', 'w')
    try:
        json.dump(id_schools, schools_f)
    finally:
        schools_f.close()


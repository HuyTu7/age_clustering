import pandas as pd
import json
import numpy
import csv
import pickle
from json import dumps, loads, JSONEncoder, JSONDecoder
from younet_rnd_infrastructure.tri.common import file_tool


class FriendshipManager():
    def __init__(self):
        pass

    @staticmethod
    def loader():
        print 'Loading data ...'
        friendships = list()
        friendships = file_tool.load_json('./temp/friends_data_18k_age.json')

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
        f = open('new_result.json', 'w')
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


def dict_to_LofT(graph):
    graph_t = []
    keys = {}
    count = 0
    for k, v in graph.iteritems():
        graph_t.append((k, set(v)))
        keys[count] = k
        count += 1
    '''
    f = open('keys.json', 'w')
    try:
        json.dump(keys, f)
    finally:
        f.close()'''
    return graph_t


def dict_to_adjmatrix(graph):
    keys = [i[0] for i in graph]
    list_to_csv(keys)
    size = len(keys)
    M = numpy.zeros(shape=(size, size))
    for a, b in [(keys.index(a), keys.index(b)) for a, row in graph for b in row]:
        M[a][b] = 1
    numpy.savetxt("test_graph.csv", M, fmt='%1.0f', delimiter=",")
    return M


def dict_to_list(dict):
    keys = dict.values()
    with open('returns.csv', 'wb') as f:
        writer = csv.writer(f)
        for key in keys:
            writer.writerow([key])

def list_to_csv(dict):
    with open('test_ids.csv', 'wb') as f:
        writer = csv.writer(f)
        for key in dict:
            writer.writerow([key])


if __name__ == '__main__':
    #FriendshipManager.loader()
    #with open('new_result.json') as data_file:
    #    graph_data = dict_to_LofT(json.load(data_file))
    #dict_to_adjmatrix(graph_data)
    with open('temp.json') as data_file1:
        graph_data = dict_to_LofT(json.load(data_file1))
    dict_to_adjmatrix(graph_data)

    #partitions = dfs(graph_data)
    #save_graph(partitions, 'cluster_test_18k.json')
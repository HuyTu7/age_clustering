import pandas as pd
import json
import numpy
import csv
import networkx as nx
import operator
import random
from heapq import nsmallest
from sklearn.metrics import classification_report

def dict_to_LofT(graph):
    graph_t = []
    keys = {}
    count = 0
    for k, v in graph.iteritems():
        graph_t.append((k, set(v)))
        keys[count] = k
        count += 1
    return graph_t


def dict_to_nx(graph):
    g = nx.Graph()
    keys = [i[0] for i in graph]
    print len(keys)
    list_to_csv(keys)
    for a, row in graph:
        if not row:
            g.add_node(a)
        else:
            for b in row:
                #print "vertex: %s and vertex: %s" % (a, b)
                g.add_edge(a, b)
    return keys, g


def list_to_csv(dict):
    with open('test_ids.csv', 'wb') as f:
        writer = csv.writer(f)
        for key in dict:
            writer.writerow([key])


def getNeighbors(node, graph, k):
    with open('temp_data.json', 'r') as fp:
        data = json.load(fp)
    distances = []
    for m in graph.nodes():
        try:
            key = keygraph_gen(n, m)
            dist = data[key]
            distances.append((m, dist))
        except nx.exception.NetworkXNoPath:
            pass
    small_d = nsmallest(10, distance, key=operator.itemgetter(1))
    # distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        try:
            neighbors.append(small_d[x])
        except IndexError:
            pass
    return neighbors


def keygraph_gen(n, m):
    if int(n) != int(m):
        temp = [int(n), int(m)]
        temp.sort()
        key = str(temp[0]) + ":" + str(temp[1])
    else: 
        key = ""
    return key


def loadShortestPath(graph):
    graph_dist = {}
    count = 0 
    for n in graph.nodes():
        for m in graph.nodes():
            try:
                key = keygraph_gen(n, m)
                if key and key not in graph_dist:
                    dist = nx.dijkstra_path_length(graph, source=n, target=m)
                    graph_dist[key] = dist 
            except nx.exception.NetworkXNoPath:
                pass
        count += 1
        if count % 100 == 0:
            print count
    with open('temp_data.json', 'w') as fp:
        json.dump(graph_dist, fp)
    

def getResponse(neighbors, df):
    classVotes = {}
    for x in range(len(neighbors)):
        response = df[neighbors[x][0]]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def save_list(data, name):
    with open(name, 'wb') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow([d])


if __name__ == '__main__':
    random.seed(9001)
    split = 0.3
    pd_df = pd.read_csv('./data_18k_age_class.csv', encoding="UTF-8", dtype={'id': str})
    df = dict([(row['id'], row['age_class']) for index, row in pd_df.iterrows()])
    with open('./result5.json') as data_file1:
        graph_data = dict_to_LofT(json.load(data_file1, encoding="UTF-8"))
    keys, g = dict_to_nx(graph_data)
    print keys
    random.shuffle(keys)
    size = int(len(keys) * split)
    testSet = keys[:size]
    save_list(testSet, '18k_test.csv')
    print len(testSet)
    print("Number of nodes in the graph: ")
    print(len(g.nodes()))
    print("Edges of graph: ")
    print(len(g.edges()))

    predictions = []
    actuals = []
    k = 4
    print "start loading shorted distance between nodes"
    loadShortestPath(g)
    print "done loading shorted distance between nodes"
    for n in testSet:
        neighbors = getNeighbors(n, g, k)
        result = getResponse(neighbors, df)
        predictions.append(result)
        actuals.append(df[n])
        print('> predicted=' + repr(result) + ', actual=' + repr(df[n]))

    save_list(predictions, '18k_test_predicted.csv')
    save_list(actuals, '18k_test_actuals.csv')
    '''
    with open('test_predicted.csv') as f:
        predictions = [line.split() for line in f]
    '''
    print("Scores on test set: %s" % classification_report(actuals, predictions))
import pandas as pd
import json
import numpy
import csv
import networkx as nx
import operator
import random
import time

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


def dict_to_list(dict):
    keys = dict.values()
    with open('returns.csv', 'wb') as f:
        writer = csv.writer(f)
        for key in keys:
            writer.writerow([key])


def dict_to_nx(graph):
    g = nx.Graph()
    keys = [i[0] for i in graph]
    print len(keys)
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


def dist_cal(neighbors_list, num, dist, distances_list):
    #random.shuffle(neighbors_list)
    results = []
    nodes = [d[0] for d in distances_list]
    for n in neighbors_list:
        #if (len(neighbors_list) - 1) >= i:
        if neighbors_list[0][1] == n[1] and n[0] not in nodes:
            results.append((n[0], dist))            
        else:
            results.append((n[0], dist+5))
            #print i
    return results


def getNeighbors(node, graph, k_value, school_ids):
    distances = []
    neighbors = []
    #print node
    neighbors.append((node, school_ids[node]))
    temp_n1 = [(k, school_ids[k]) for k in graph[node].keys()]
    random.shuffle(temp_n1)
    neighbors += temp_n1
    k_value_new = int(k_value * 1.5)
    if len(neighbors) >= k_value_new:
        dist = 1
        distances = dist_cal(neighbors, k_value_new, dist, distances)
    else:
        temp_d = 1
        temp_neighbors = neighbors
        temp_num = len(temp_neighbors)
        while len(distances) < k_value_new:
            distances += dist_cal(temp_neighbors, temp_num, temp_d, distances)
            temp_neighbors = []
            temp_neighbors.append((node, school_ids[node]))
            temp_n2 =[]
            #print "Neighbors: %s" % neighbors
            for neighbor in neighbors:
                temp_n2 += [(x, school_ids[x]) for x in graph[neighbor[0]].keys()] 
            random.shuffle(temp_n2)
            temp_neighbors += temp_n2
            temp_num = k_value_new - temp_num
            temp_d += 1
    sorted_neighbors = sorted(distances, key=operator.itemgetter(1))
    #print "Sorted Neighbors: %s" % sorted_neighbors
    results = []
    for i in range(k_value):
        results.append(sorted_neighbors[i])
    
    #print "Final Sorted Neighbors: %s" % results
    return results


def getResponse(neighbors, dataset):
    classVotes = {}
    for x in range(len(neighbors)):
        response = dataset[neighbors[x][0]]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testS, preds, valids):
    correct = 0
    for x in testS:
        entry = valids[x]
        if entry['age_class'] == preds[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def save_list(data, name):
    with open(name, 'wb') as f:
        writer = csv.writer(f)
        for p in predictions:
            writer.writerow([p])


if __name__ == '__main__':
    random.seed(98)
    split = 0.4
    pd_df = pd.read_csv('./data_18k_age_class.csv', encoding="UTF-8", dtype={'id': str})
    df = dict([(row['id'], row['age_class']) for index, row in pd_df.iterrows()])
    with open('school_ids.json') as file1:
        s_ids = json.load(file1, encoding="UTF-8")
    #print s_ids
    with open('temp_final.json') as file2:
        graph_data = dict_to_LofT(json.load(file2, encoding="UTF-8"))
    keys, g = dict_to_nx(graph_data)
    #print keys
    random.shuffle(keys)
    size = int(len(keys) * split)
    testSet = keys[:size]
    print len(testSet)
    print("Nodes of graph: ")
    print(len(g.nodes()))
    print("Edges of graph: ")
    print(len(g.edges()))

    #print("Neighbors of node 100002597518977: %s") % g["100002597518977"].keys()
    print("School ID of %s: %s") % ("100014187279433", s_ids["100014187279433"])
    predictions = []
    actuals = []
    k = 3

    for n in testSet:
        k_neighbors = getNeighbors(n, g, k, s_ids)
        result = getResponse(k_neighbors, df)
        predictions.append(result)
        actuals.append(df[n])
        #print('> predicted=' + repr(result) + ', actual=' + repr(df[n]))

    save_list(predictions, '3s_test_predicted.csv')
    save_list(actuals, '3s_test_actuals.csv')
    
    #with open('test_predicted.csv') as f:
    #    predictions = [line.split() for line in f]
    print len(actuals)
    print len(predictions)
    print("Scores on test set: %s" % classification_report(actuals, predictions))
import pandas as pd
import json
import numpy
import csv
import networkx as nx


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


def networkx_graph(graph):
    g = nx.Graph()
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


if __name__ == '__main__':
    with open('temp.json') as data_file1:
        graph_data = dict_to_LofT(json.load(data_file1))
    dict_to_adjmatrix(graph_data)
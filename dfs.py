import numpy
import json

def dfs(graph):
    unvisited = []
    for vertex in graph.keys():
        unvisited.append(vertex)
    partitions = []
    print unvisited
    while unvisited:
        vertex = unvisited[0]
        visited, stack = [vertex], [vertex]  # add start index to both visited and stack
        print "Node: %s" % vertex
        while stack:     #while stack is not empty
            #for each of the children of current vertex we find the first non visited child and add it to visited as well as stack
            for i, node in enumerate(graph[vertex]):
                print "I: %s Node: %s" % (i, node)
                if node not in visited:
                    visited.append(node)
                    unvisited.remove(node)
                    stack += [node]  # push the element to stack if it is visited
                    vertex = node      #change current vertex to last visited vertex
                    print "Current Vertex: %s" % vertex
                    print unvisited
                    break            #since the stack keeps track of the order of elements we can jump to children of current vertex.
                else:
                    #if the length of children of a vertex is reached and all children are visited then pop the last element from stack
                    if i == len([vertex])-1:
                        vertex = stack.pop()
                        break
                    else:
                        continue    #continue till the end to check if all the children of current vertex are visited
        partitions.append(visited)
    return partitions

def dfs2(graph):
    graph = filling(graph)
    unvisited = set()
    for vertex in graph.keys():
        unvisited.add(vertex)
    partitions = []
    print unvisited
    while unvisited:
        start = next(iter(unvisited))
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                if vertex in unvisited:
                    unvisited.remove(vertex)
                    stack.extend(set(graph[vertex]) - visited)
        partitions.append(visited)
    return partitions


def filling(graph):
    for key, value in graph.items():
        if value:
            for id in value:
                print graph[id]
                if id in set(graph.keys()):
                    graph[id].add(key)
    print 'DONE FILLING'
    return graph


def dfs3(graph):
    start = graph.keys()[0]
    visited, stack = set(), [start]
    while stack:
       vertex = stack.pop()
       if vertex not in visited:
           visited.add(vertex)
           stack.extend(set(graph[vertex]) - visited)
           print stack
    return visited

def save_graph(data, filename):
    thefile = open(filename, 'w')
    for item in data:
        thefile.write("%s\n" % item)


def dict_to_adjmatrix(graph):
    keys = [i[0] for i in graph]
    print keys
    size = len(keys)
    print size
    M = numpy.zeros(shape=(size, size))
    print M
    for a, b in [(keys.index(a), keys.index(b)) for a, row in graph for b in row]:
        print "a: %s, b: %s" % (a, b)
        M[a][b] = 1
    numpy.savetxt("foo.csv", M, delimiter=",")
    return M

def dict_to_LofT(graph):
    graph_t = []
    keys = {}
    count = 0
    for k, v in graph.iteritems():
        graph_t.append((k, set(v)))
        keys[count] = k
        count += 1
    f = open('keys.json', 'w')
    try:
        json.dump(keys, f)
    finally:
        f.close()
    return graph_t

g = {'A': {'B', 'C'},
     'B': {'A', 'D', 'E'},
     'C': {'A', 'F'},
     'D': {'B'},
     'E': {'B', 'F'},
     'F': {'C', 'E'},
     'G': {'H', 'J'},
     'H': {'G'},
     'J': {'G', 'K'},
     'K': {'J'},
     'M': {'N'},
     'N': set(),
     'P': {'N'},
     }

visited = dfs2(g)
print visited
new_data = dict_to_LofT(g)
matrix = dict_to_adjmatrix(new_data)
print matrix
#visited = dfs3(graph)
#print visited
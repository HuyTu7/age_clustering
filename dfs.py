def dfs(graph):
    unvisited = []
    for vertex in graph.keys():
        unvisited.append(vertex)
    partitions = []
    print unvisited
    while unvisited:
        vertex = unvisited[0]
        visited, stack = [vertex], [vertex]  # add start index to both visited and stack
        while stack:     #while stack is not empty
            #for each of the children of current vertex we find the first non visited child and add it to visited as well as stack
            for i, node in enumerate(graph[vertex]):
                print "I: %s Node: %s" % (i, node)
                if node not in visited:
                    visited.append(node)
                    unvisited.remove(node)
                    stack += [node]  # push the element to stack if it is visited
                    vertex = node      #change current vertex to last visited vertex
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

graph = {'A': ['B', 'C'],
     'B': ['A', 'D', 'E'],
     'C': ['A', 'F'],
     'D': ['B'],
     'E': ['B', 'F'],
     'F': ['C', 'E'],
     'G': ['H', 'J'],
     'H': ['G'],
     'J': ['G', 'K'],
     'K': ['J']
         }

visited = dfs(graph)
print visited
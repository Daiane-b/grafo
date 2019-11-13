''' A very simple directed graph class
@author Daiane Barbosa da Cruz'''
import sys

class DiGraph(object):
    class Edge(object):
        ''''An edge holds the vertex it points to and its cost (or weight).'''
        def __init__ (self, n, c):
            '''Constructor from a node and its cost.
            @param n: node/vertex
            @param c: weight or cost associated with the edge'''
            self.__node = n
            self.__cost = c
        def cmp(x,y):
            '''Compare the two objects x and y and return an integer according to the outcome.
            @param x: first object
            @param y: second object
            @return a negative value if x < y, zero if x == y and strictly positive if x > y.'''
            if x < y:
                return -1
            elif x == y:
                return 0
            else:
                return 1
        def getVertex (self):
            '''Get the target vertex.
            @return the node this edge points to.'''
            return self.__node
        def getCost (self):
            '''Get this edge cost.
            @return the cost of this edge'''
            return self.__cost
        def setCost (self, c):
            '''Set the cost of this edge.'''
            self.__cost = c
        def cmpCost (self, other):
            '''Compare two edges based on the cost only, not on the vertex.
            @param other: the edge for comparing this edge to.'''
            return cmp(self.getCost(), other.getCost())
        def __repr__ (self):
            '''An unambiguous representaion of this edge.
            a string representation of this edge.'''
            return '< ' + str(self.__node) + ', ' + str(self.__cost) + '>'
        def __hash__ (self):
            '''An Edge object must be hashable.'''
            return hash((self.__node, self.__cost))

        def __eq__ (self, obj):
            '''Operator ==.
            Only compare the nodes but not the cost of the nodes.
            @param obj: the edge for comparing this edge to.'''
            return self.__node == obj.__node
        def __contains__ (self, obj):
            '''Operator in.
            Only compare the nodes but not the cost of the nodes.'''
            return self.__node == obj.__node
    class DiGraph(object):
        '''A Python Class
        A simple Python graph class, demonstrating the essential 
        facts and functionalities of graphs.'''
        def __init__(self, graph_dict=None):
            """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used"""
            if graph_dict == None:
                graph_dict = {}
            self.__graph_dict = graph_dict
            self.__infinity = sys.maxsize
            
        def getInfinity (self):
            """Returns the largest edge cost.
            @return returns de largest edge cost"""
            return self.__infinity
                    
        def addEdge (self, src, dst, c=1):
            """Add a directed edge from the source node to the destination node.
            @param src: source node
            @param dst: destinatation node
            @param c: weight of de edge
            @return False e if src or dst is None, or c <= 0, or src == dst,
            True if a new edge from src to dst is added with the weight."""
            edge = DiGraph.Edge(dst, c)
            if src == None or dst == None:
                return False
            elif src == dst:
                return False
            elif c <= 0:
                return False
            else:
                if self.__graph_dict[src].copy() == set():
                    self.__graph_dict[src].add(edge)
                else:
                    for node in self.__graph_dict[src].copy():
                        if node == edge:
                            node.setCost(c)
                        else:
                            self.__graph_dict[src].add(edge)
                            
                return True
        def addVertex (self, vertex):
            """Add a vertex to the graph with an empty set of edges associated with it
            @param vertex: Vertex to be added
            @return False if vertex is None or vertex is already in the graph
            True otherwise."""
            if vertex not in self.__graph_dict:
                self.__graph_dict[vertex] = set()
                return True
            else:
                return False
        def numVertices (self):
            """Returns the number of vertices in this graph.
            @return number of vertices in this graph"""
            return int(len(list(self.__graph_dict)))
        def vertices(self):
            """Returns all vertices in this graph.
            @return all vertices in this graph"""
            if len(list(self.__graph_dict))>0:
                return set(self.__graph_dict.keys())
            else:
                return set()
        def adjacentTo (self, vertex):
            """Gets all vertices adjacent to a given vertex.
            @param vertex: vertex to be checked
            @return An empty set is returned if there is no adjacent node,
            or the vertex is not in the graph,
            or vertex is None"""
            adjacent = set()
            try:
                if self.__graph_dict[vertex]:
                    for node in self.__graph_dict[vertex]:
                        adjacent.add(node)
            except KeyError:
                pass
            return adjacent
        def hasVertex (self, vertex):
            """Checks whether a given vertex is in the graph.
            @param vertex: given vertex
            @returns True if the given vertex is in the graph
            False otherwise, including the case of a None vertex."""
            try:
                if vertex in self.__graph_dict:
                    return True
                else:
                    return False, vertex
            except KeyError:
                return False
        def numEdges (self):
            """Returns the number of edges in this graph.
            @returns Total the number of edges in this graph"""
            edges = []
            for vertex in self.__graph_dict:
                for neighbour in self.__graph_dict[vertex]:
                    if [neighbour.getVertex(), vertex] not in edges:
                        edges.append([neighbour.getVertex(), vertex])
            __numEdges = len(edges)
            return __numEdges
        def getEdge (self, src, dst):
            """Gets the edge from src to dst, if such an edge exists.
            @param src: source vertex
            @param dst: target vertex
            @return an edge if there exists an edge from src to dst regardless of the weight
            None otherwise (including when either src or dst is None or src or dst is not in the graph)."""

            if self.hasVertex(src) and self.hasVertex(dst):
                for edge in self.__graph_dict[src]:
                        if edge.getVertex() == dst:
                            return [src, dst]
                else:
                    return None
            else:
                return None
        def hasEdge (self, src, dst):
            """Check whether an edge from src to dst exists.
            @param src: source vertex
            @param dst: target vertex
            @return True if there exists an edge from src to dst regardless of the weight, and
            False otherwise (including when either src or dst is None or src or dst is not in the graph)."""

            if self.getEdge(src, dst) == None:
                return False
            else:
                return True
        def removeVertex (self, vertex):
            """Remove this vertex from the graph if possible and calculate the number of edges in the graph accordingly.
            @param vertex: Vertex to be removed
            @return False if the vertex is None, or there is no such vertex in the graph
            True if removal is successful."""
            if self.hasVertex(vertex):
                for node in self.__graph_dict:
                    for neighbour in self.__graph_dict[node].copy():
                        if neighbour.getVertex() == vertex:
                            self.__graph_dict[node].discard(neighbour)                       
                del self.__graph_dict[vertex]
                return True
            else:
                return False
                
        def incomingEdges (self, vertex):
            """Return a set of nodes with edges coming to this given vertex.
            @param vertx: given vertex
            @return empty set if the vertex is None or the vertex is not in this graph.
             Otherwise, return a non-empty set consists of nodes with edges coming to this vertex."""
            nodes = set()
            if self.hasVertex(vertex):
                for node in self.__graph_dict:
                    if self.hasEdge(node, vertex):
                        nodes.add(self.getEdge(node, vertex)[0])
            return nodes
        def __generate_edges(self):
            """ A static method generating the edges of the 
                graph "graph". Edges are represented as sets 
                with one (a loop back to the vertex) or two 
                vertices 
            """
            edges = []
            for vertex in self.__graph_dict:
                for neighbour in self.__graph_dict[vertex]:
                    if [neighbour.getVertex(), vertex, neighbour.getCost()] not in edges:
                        edges.append((vertex, neighbour.getVertex(), neighbour.getCost()))
            return edges
        def find_all_paths(self, start_vertex, end_vertex, path=[], cost = 0):
            ''' find all paths from start_vertex to 
                end_vertex in graph
            @param start_vertex: source vertex
            @param end_vertex: target vertex
            @return a list of all paths from start_vertex and end_vertex, if don't have path, return a empty list'''
            graph = self.__graph_dict
            path = path + [[start_vertex, cost]]
            print('start_vertex, cost', start_vertex, cost, 'end_vertex', end_vertex)
            if start_vertex == end_vertex:
                print('passou aqui', 'start_vertex', start_vertex, 'end_vertex', end_vertex)
                return [path]
            if start_vertex not in graph:
                return []
            paths = []
            for vertex in graph[start_vertex]:
                if vertex.getVertex() not in path:
                    extended_paths = self.find_all_paths(vertex.getVertex(), 
                                                         end_vertex, 
                                                         path, vertex.getCost())
                    for p in path:
                        soma = 0
                        print('p', p)
                        for value in p:
                            if type(value) is int:
                                soma += value
                                print('value', value, 'soma', soma)
                        paths.append([p, soma])
                return paths
                
        def __repr__ (self):
            """Return a representation of the graph as a string."""
            res = "vertices: "
            for k in self.__graph_dict:
                res += str(k) + " "
            res += "\nedges: "
            for a in self.__generate_edges():
                res +="<"
                for edge in a:
                    if isinstance(edge, int):
                        res += str(edge)
                    else:
                        res += str(edge) + ", "
                res +="> "
            return res
        def Dijkstra (self, source):
            """Compute Dijkstra single source shortest path from the source node.
            @param source: Source node
            @return Empty dictionary if the source is None,
            or it is not a vertex in the graph,
            or it does not have any outgoing edges.
            Otherwise, return a dictionary of entries, each having a vertex and smallest cost going from the source
            node to it and a dictionary having the path between nodes"""
            ''' __pathToNode Holds the path from a source node to a given node
            __dist: Accumulated distance from source to a node.'''
            if source == None:
                return dict()
            if self.hasVertex(source):
                if not self.adjacentTo(source) == []:
                    __dist = self.getInfinity()
                    previous_vertices = {vertex: None for vertex in self.__graph_dict}
                    __pathToNode = {vertex: __dist for vertex in self.__graph_dict}
                    __pathToNode[source] = 0
                    vertices = self.vertices()
                    while vertices:
                        current_vertex = min(vertices, key=lambda vertex: __pathToNode[vertex])
                        vertices.remove(current_vertex)
                        if __pathToNode[current_vertex] == __dist:
                            break
                        for edge in self.__graph_dict[current_vertex]:
                            alternative_route = __pathToNode[current_vertex] + edge.getCost()
                            if alternative_route < __pathToNode[edge.getVertex()]:
                                __pathToNode[edge.getVertex()] = alternative_route
                                node = DiGraph.Edge(current_vertex, alternative_route)
                                previous_vertices[edge.getVertex()] = node
                    return __pathToNode, previous_vertices
                else:
                    return dict()
            else:
                return dict()
        def Dijkstra2 (self, source, dest):
            """Compute Dijkstra shortest path from the source to the destination node
            @param source: source vertex
            @param dest: target vertex
            @return Empty list if the source or dest are None,
            or they are not a vertex in the graph,
            or source does not have any outgoing edges.
            Otherwise, return a list of edges for reaching dest from source with the smallest cost."""

            ret = []
            if source == None or dest == None:
                return ret
            if self.hasVertex(source) and self.hasVertex(dest):
                if not self.adjacentTo(source) == []:
                    previous_vertices = self.Dijkstra(source)[1]
                    name = dest
                    try:
                        while source != name:
                            edge = DiGraph.Edge(name, previous_vertices[name].getCost())
                            ret.append(edge)
                            name = previous_vertices[name].getVertex()
                            if name == source:
                                break
                        ret.append(DiGraph.Edge(source, 0))
                        ret.reverse()
                    except:
                        pass
                return ret
                        
            else:
                return ret

if __name__ == "__main__":

    e1 = ("d",1)
    edge1 = DiGraph.Edge("d",1)

    g = { "a" : {edge1},
          "b" : {DiGraph.Edge("c",2)},
          "c" : {DiGraph.Edge("b",1), DiGraph.Edge("d",4), DiGraph.Edge("e",1)},
          "d" : {DiGraph.Edge("a",1), DiGraph.Edge("c",2)},
          "e" : {DiGraph.Edge("c",3)},
          "f" : {}
        }

    graph = DiGraph.DiGraph(g)
    print(graph)

    '''for node in graph.vertices():
        print(graph.vertex_degree(node))

    print("List of isolated vertices:")
    print(graph.find_isolated_vertices())'''

    print("""all vertex incoming""")
    print(graph.incomingEdges("a"))

    print("Add vertex 'z':")
    graph.addVertex("z")
    print(graph)

    print("Add edge ('z','a', 1): ")
    print(graph.addEdge('z', 'a', 1))
    print(graph)

    print("numero vertices")
    print(graph.numVertices())

    print("adjacentTo, z")
    print(graph.adjacentTo("z"))

    print("incomingEdges, c")
    print(graph.incomingEdges("c"))

    print("getEdge, a, z")
    print(graph.getEdge("z", "a"))

    print("Number of Edges:", graph.numEdges())
    
    print("""Dijkstra: c""")
    print(graph.Dijkstra("c"))

    '''print("""All pathes from "c" to "b": Dijkstra2""")
    print(graph.Dijkstra2("c", "b"))'''

    print("""self.adjacentTo(f)""")
    print(graph.adjacentTo("f"))


    

    print(graph.getInfinity())

    '''print("The maximum degree of the graph is:")
    print(graph.Delta())

    print("The minimum degree of the graph is:")
    print(graph.delta())

    print("Edges:")
    print(graph.edges())

    print("Degree Sequence: ")
    ds = graph.degree_sequence()
    print(ds)

    fullfilling = [ [2, 2, 2, 2, 1, 1}, 
                         [3, 3, 3, 3, 3, 3],
                         [3, 3, 2, 1, 1]
                       ] 
    non_fullfilling = [ [4, 3, 2, 2, 2, 1, 1],
                        [6, 6, 5, 4, 4, 2, 1],
                        [3, 3, 3, 1] ]

    for sequence in fullfilling + non_fullfilling :
        print(sequence, Graph.erdoes_gallai(sequence))


    

    print("Add edge ('a','d'): ")
    graph.add_edge(('a', 'd'))
    print(graph)

        print("delete vertice c")
    graph.removeVertex("c")
    print(graph)
'''

    

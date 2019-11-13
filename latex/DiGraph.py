""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.  @author Daiane Barbosa da Cruz
"""
class DiGraph(object):
    def __init__(self, graph_dict=None):
        """ initializes a graph object 
        If no dictionary or None is given, an empty dictionary will be used"""
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict
    def getInfinity (self):
        """Returns the largest edge cost.
        @return returns de largest edge cost"""
        
        
        pass
    def addEdge (self, src, dst, c=1):
        """Add a directed edge from the source node to the destination node.
        @param src: source node
        @param dst: destinatation node
        @param c: weight of de edge
        @return False e if src or dst is None, or c <= 0, or src == dst,
        True if a new edge from src to dst is added with the weight."""
        if scr == None or dst == None:
            return False
        elif scr == dst:
            return False
        elif c <= 0:
            return False
        else:
            edges = self.__graph_dict[(src, c)]
            edges.append(dst)
            self.__graph_dict[src] = edges
            return True
    def addVertex (self, vertex):
        """Add a vertex to the graph with an empty set of edges associated with it
        @param vertex: Vertex to be added
        @return False if vertex is None or vertex is already in the graph
        True otherwise."""
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
            return True
        else:
            return False
    def numVertices (self):
        """Returns the number of vertices in this graph.
        @return number of vertices in this graph"""
        return len(self.__graph_dict)
    def vertices(self):
        """Returns all vertices in this graph.
        @return all vertices in this graph"""
        return list(self.__graph_dict.keys())
    def adjacentTo (self, vertex):
        """Gets all vertices adjacent to a given vertex.
        @param vertex: vertex to be checked
        @return An empty set is returned if there is no adjacent node,
        or the vertex is not in the graph,
        or vertex is None"""
        adjacent = []
        try:
            if self.__graph_dict[vertex]:
                return list(self.__graph_dict[vertex])
            else:
                return adjacent
        except KeyError:
            return adjacent
    def hasVertex (self, vertex):
        """Checks whether a given vertex is in the graph.
        @param vertex: given vertex
        @returns True if the given vertex is in the graph
        False otherwise, including the case of a None vertex."""
        try:
            if self.__graph_dict[vertex]:
                return True
            else:
                return False
        except KeyError:
            return False
    def numEdges (self):
        """Returns the number of edges in this graph."""
        pass
    def getEdge (self, src, dst):
        """Gets the edge from src to dst, if such an edge exists."""
        pass
    def hasEdge (self, src, dst):
        """Check whether an edge from src to dst exists."""
        pass
    def removeVertex (self, vertex):
        """Remove this vertex from the graph if possible and calculate the number of edges in the graph accordingly."""
        pass
    def incomingEdges (self, vertex):
        """Return a set of nodes with edges coming to this given vertex."""
        pass
    def __repr__ (self):
        """Return a representation of the graph as a string."""
        pass
    def Dijkstra (self, source):
        """Compute Dijkstra single source shortest path from the source node."""
        pass
    def Dijkstra2 (self, source, dest):
        """Compute Dijkstra shortest path from the source to the destination node."""
        pass
    

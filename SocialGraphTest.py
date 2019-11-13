import unittest
import SocialGraph
import DiGraph
from DiGraph import DiGraph

class DiGraphTest(unittest.TestCase):
    def test_Digraph(self):
        g = { "a" : {DiGraph.Edge("d",1)},
        "b" : {DiGraph.Edge("c",2)},
        "c" : {DiGraph.Edge("b",1), DiGraph.Edge("d",4), DiGraph.Edge("e",1)},
        "d" : {DiGraph.Edge("a",1), DiGraph.Edge("c",2)},
        "e" : {DiGraph.Edge("c",3)},
        "f" : {}}
        result = DiGraph.DiGraph(g)
        self.assertEqual(result.addVertex("z"), True)
        self.assertEqual(result.incomingEdges("a"), {'d'})
        self.assertEqual(result.addEdge('z', 'a', 1), True)
        self.assertEqual(result.numVertices(), 7)

if __name__ == '__main__':
    unittest.main()

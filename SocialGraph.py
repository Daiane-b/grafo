'''Manages a social network of friendships
@author Daiane Barbosa da Cruz'''
import sys
from DiGraph import DiGraph

'''SocialGraph.py infile.txt'''

class SocialGraph(object):
    '''def main(args = None):
        Create an graph Graph and call the methods responsable to implement the comands
        written in the file
        arq = open(file, 'r')
        dg = DiGraph.DiGraph()
        socialgraph = SocialGraph(file, dg)
        #socialgraph.readGraphFile(file)
        for linha in arq:
                print()
                arg = linha.split(' ')
                #print(arg)
                if arg[0] == 'add':
                    dg.addVertex(arg[1])
                    dg.addVertex(arg[2])
                    print(linha,
                          'addEdge:',dg.addEdge(arg[1],arg[2], int(arg[3])),
                          '-', dg.numEdges(), 'edges,',
                          dg.numVertices(), 'vertices')
                elif arg[0] == 'remove':
                    print(linha,
                          'remove:',dg.removeVertex(arg[1].replace('\n', '')),
                          '-', dg.numEdges(), 'edges,',
                          dg.numVertices(), 'vertices')
                elif arg[0] == 'showFriends':
                    print(linha, dg.adjacentTo(arg[1].replace('\n', '')))
                elif arg[0] == 'recommendFriends':
                    print(linha, socialgraph.recommendFriends(arg[1], arg[2], int(arg[3])))
                elif arg[0] == 'shortestPath':
                    print(linha, dg.Dijkstra2(arg[1],arg[2].replace('\n', '')))#(arg[1], arg[2].replace('\n', '')))
                    
        arq.close()'''


    def create(self):
        arq = open(self.file, 'r')
        dg = DiGraph.DiGraph()
        socialgraph = SocialGraph(self.file, dg)
        #socialgraph.readGraphFile(file)
        for linha in arq:
                print()
                arg = linha.split(' ')
                #print(arg)
                if arg[0] == 'add':
                    dg.addVertex(arg[1])
                    dg.addVertex(arg[2])
                    print(linha,
                          'addEdge:',dg.addEdge(arg[1],arg[2], int(arg[3])),
                          '-', dg.numEdges(), 'edges,',
                          dg.numVertices(), 'vertices')
                elif arg[0] == 'remove':
                    print(linha,
                          'remove:',dg.removeVertex(arg[1].replace('\n', '')),
                          '-', dg.numEdges(), 'edges,',
                          dg.numVertices(), 'vertices')
                elif arg[0] == 'showFriends':
                    print(linha, dg.adjacentTo(arg[1].replace('\n', '')))
                elif arg[0] == 'recommendFriends':
                    print(linha, socialgraph.recommendFriends(arg[1], arg[2], int(arg[3])))
                elif arg[0] == 'shortestPath':
                    print(linha, dg.Dijkstra2(arg[1],arg[2].replace('\n', '')))#(arg[1], arg[2].replace('\n', '')))
        self.dg = dg
                    
        arq.close()
            
    def getdg(self):
        '''return the graph generated by a file'''
        return self.dg    
    def __init__ (self, file, dg = DiGraph.DiGraph()):
        '''Constructor from a file of commands.
        @param file: file to be used
        @param dg: Graph'''
        self.file = file
        self.dg = dg           
    def recommendFriends(self, personOfInterest, option, topK):
        '''Recommend topK (e.g., 5) best friend candidates who are not already a friend of personOfInterest.
                If dist option is used, find the shortest path from personOfInterest to all the other nodes in the graph using
                Dijkstra's single source shortest path algorithm and friendship distances. The smaller the distance means the
                closer the relationship.
                If weightedDist option is used, after computing the shortest path like in the dist option to all the other nodes
                in the graph, multiply each distance with the total number of edges in the graph less the number of incoming
                edges to that node.
                @param personOfInterest: Name of the person to recommend new friend candidates for
                @param option:
                Either dist or weightedDist, which indicates whether to use the friendship distance or the
                weighted friendship distance.
                @param topK: Desirable maximum number of candidate friends to recommend.'''

        ret = []
        conj = set()
        __recommend = self.dg.Dijkstra(personOfInterest)[0]
        retorno = sorted(__recommend.items(), key = lambda e: (e[1], e[0]))
        if option == 'dist':
            for item in retorno:
                if not self.dg.hasEdge(personOfInterest, item[0]): 
                    if item[1]!= 0 and item[1]<sys.maxsize:
                        edge = DiGraph.Edge(item[0], int(item[1]))
                        conj.add(edge.getCost())
                        ret.append(edge)
            topK = topK + (len(ret) - len(conj))
            for i in range(topK, len(ret)):
                del ret[i]
        if option == 'weightedDist':
            totalArestas = self.dg.numEdges()
            for item in retorno:
                if not self.dg.hasEdge(personOfInterest, item[0]):
                    if item[1]!= 0 and item[1]<sys.maxsize:
                        incoming = len(self.dg.incomingEdges(item[0]))
                        edge = DiGraph.Edge(item[0], int(item[1])*(totalArestas-incoming))
                        ret.append(edge)
                for i in range(topK, len(ret)):
                    del ret[i]
        return ret
                
            


if __name__ == "__main__":       
    if  (len(sys.argv) < 2):
        print("Erro!!! Arquivo de entrada não digitado")
    else:
        file = 'infile.txt'
        socialGraph = SocialGraph(file)
        socialGraph.create()



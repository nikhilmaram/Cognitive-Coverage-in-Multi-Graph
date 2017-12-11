import networkx as nx
import matplotlib.pyplot as plt
import copy

class Node:
    def __init__(self,name,feature1,feature2,feature3):
        self.name = str(name)
        self.feature1 = feature1
        self.feature2 = feature2
        self.feature3 =  feature3
        self.virtual = False
        self._visited = False
    def __str__(self):
        return self.name


class Graph:
    def __init__(self,name):
        self.name = name
        self.G = nx.Graph()

    def createNode(self,name,feature1,feature2,feature3):
        node = Node(name,feature1,feature2,feature3)
        self.G.add_node(node)
        return node

    def addNode(self,node):
        self.G.add_node(node)

    def createEdge(self,node1,node2):
        self.G.add_edge(node1,node2)

    def drawGraph(self):
        nx.draw(self.G,with_labels=True)
        plt.show()

    def drawGraphColors(self):
        node_color =[]
        for node in self.G.nodes:
            if(node.feature1 == True and node.feature2 == True and node.feature3 == True):
                value = 1
            elif(node.feature1 == True and node.feature2 == True):
                value = 3
            elif(node.feature1 and node.feature3 == True):
                value = 5
            elif (node.feature2 == True and node.feature3 == True) :
                value = 7
            elif(node.feature1 == True):
                value = 9
            elif(node.feature2== True):
                value = 11
            elif (node.feature3 == True):
                value = 13
            else:
                value = 15

            node_color.append(value)


        nx.draw(self.G,with_labels=True,node_color=node_color)
        plt.show()

    def createVirutalNode(self,name,feature1,feature2,feature3):
        virtualNode = Node(name,feature1,feature2,feature3)
        virtualNode.virtual = True
        return virtualNode

    def createBipartiteGraph(self,virtualNode,feature):
        for node in self.G.nodes:
            if not node.virtual:
                if(getattr(node,feature) == True):
                    self.createEdge(virtualNode,node)


    def makeNodesVisited(self,node):
        for neighbors in self.G.neighbors(node):
            neighbors._visited = True

    def neighborLength(self,neighborList):
        count = 0
        for node in neighborList:
            if node._visited == False and node.virtual == False :
                count = count + 1
        return count

    def choseBestNodes(self,virtualNodeList):
        nodesChosen = []
        ## Need to chose nodes which has the same feature as virtual node and has high degree.
        ## We are considering all the neighbors of the vertex chosen. Not only the nodes with same feature as virtual node.
        for vNode in virtualNodeList:
            maxNeighborLength = 0
            maxNeightbor = vNode
            for node in self.G.neighbors(vNode):
                if node._visited == False:
                    nLength = self.neighborLength(self.G.neighbors(node))+1
                    if (nLength > maxNeighborLength):
                        maxNeighborLength = nLength
                        maxNeightbor = node
            maxNeightbor._visited = True
            nodesChosen.append(maxNeightbor)
            self.makeNodesVisited(maxNeightbor)

        return nodesChosen


if __name__ == "__main__":
    Graph = Graph("bruteForce")

    Node1 = Graph.createNode(1, True, True, True)
    Node2 = Graph.createNode(2, False, False, False)
    Node3 = Graph.createNode(3, True, False, False)
    Node4 = Graph.createNode(4, True, True, True)
    Node5 = Graph.createNode(5, False, True, True)
    Node6 = Graph.createNode(6, False, True, False)
    Node7 = Graph.createNode(7, False, False, True)
    Node8 = Graph.createNode(8, False, False, False)
    Node9 = Graph.createNode(9, True, True, True)
    Node10 = Graph.createNode(10, False, True, True)

    ## Creating virtual nodes
    v1 = Graph.createVirutalNode('v1',True,False,False)
    v2 = Graph.createVirutalNode('v2',False,True,False)
    v3 = Graph.createVirutalNode('v3',False,False,True)

    ## Adding virtual nodes to the graph
    Graph.addNode(v1)
    Graph.addNode(v2)
    Graph.addNode(v3)

    ## Creating edges between the nodes
    Graph.createEdge(Node1, Node2)
    Graph.createEdge(Node1, Node3)
    Graph.createEdge(Node1, Node4)
    Graph.createEdge(Node1, Node5)
    Graph.createEdge(Node2, Node3)
    Graph.createEdge(Node3, Node4)
    Graph.createEdge(Node4, Node5)
    Graph.createEdge(Node1, Node6)
    Graph.createEdge(Node6, Node7)
    Graph.createEdge(Node6, Node8)
    Graph.createEdge(Node6, Node9)
    Graph.createEdge(Node6, Node10)
    Graph.createEdge(Node7, Node8)
    Graph.createEdge(Node8, Node9)
    Graph.createEdge(Node9, Node10)
    Graph.createEdge(Node2, Node7)

    ## Build the bipartite graph from virtual nodes

    Graph.createBipartiteGraph(v1,"feature1")
    Graph.createBipartiteGraph(v2, "feature2")
    Graph.createBipartiteGraph(v3, "feature3")

    nodesChosen = Graph.choseBestNodes([v1,v2,v3])
    for node in nodesChosen:
        print(node)


    Graph.drawGraphColors()
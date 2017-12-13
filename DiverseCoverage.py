import networkx as nx
import matplotlib.pyplot as plt
import copy
import time
import creatingGraph as cg


class Node:
    def __init__(self,name,feature1,feature2,feature3):
        self.name = str(name)
        self.feature1 = feature1
        self.feature2 = feature2
        self.feature3 =  feature3
        self.virtual = False
        self._visited = False
        self._covered = False

    def __str__(self):
        return self.name

class GraphClass:
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

        nx.circular_layout(self.G)
        nx.draw(self.G,with_labels=True,node_color=node_color,pos=nx.circular_layout(self.G))

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


    def markNodesUnvisited(self):
        for node in self.G.nodes:
            node._visited = False

    def neighborLength(self,neighborList):
        count = 0
        for node in neighborList:
            if node._visited == False and node.virtual == False :
                count = count + 1
        return count

    def choseBestNodes(self,virtualNodeList):
        nodesChosen = []
        totalCount = 0
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
            totalCount+=maxNeighborLength

        return nodesChosen,totalCount

    def setNodesCovered(self, nodeList):
        for node in nodeList:
            node = cg.name2Node[node.name]
            for neighbor in self.G.neighbors(node):
                neighbor._covered = True
            node._covered = True

    def measureCoveredNodes(self):
        nodeCount = 0
        coveredCount = 0
        for node in self.G.nodes:
            nodeCount = nodeCount + 1
            if (node._covered == True):
                coveredCount = coveredCount + 1
        return nodeCount, coveredCount

    def insertSelectedEdges(self, nodeSet):
        nodeList = list(nodeSet)
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                node1 = nodeList[i]
                node2 = nodeList[j]
                self.createEdge(node1, node2)



def permute(vnodeList,l,r,combinationList):

    if (l==r):
        combinationList.append(copy.copy(vnodeList))
    else:
        for i in range(l,r+1):
            vnodeList[l],vnodeList[i] = vnodeList[i],vnodeList[l]
            permute(vnodeList,l+1,r,combinationList)
            vnodeList[l],vnodeList[i] = vnodeList[i],vnodeList[l]

def createBasicGraph(Graph):
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

def createVirtualGraph(vGraph):
    maxCoverageNodeSet = []
    ## Creating virtual nodes
    v1 = vGraph.createVirutalNode('v1', True, False, False)
    v2 = vGraph.createVirutalNode('v2', False, True, False)
    v3 = vGraph.createVirutalNode('v3', False, False, True)

    ## Adding virtual nodes to the graph
    vGraph.addNode(v1)
    vGraph.addNode(v2)
    vGraph.addNode(v3)
    ## Build the bipartite graph from virtual nodes

    vGraph.createBipartiteGraph(v1, "feature1")
    vGraph.createBipartiteGraph(v2, "feature2")
    vGraph.createBipartiteGraph(v3, "feature3")

    a = [v1, v2, v3]
    combinationList = []
    ## Permute all different combinations of virtual nodes to be chosen
    permute(a, 0, len(a) - 1, combinationList)
    maxCoverage = 0

    for comb in combinationList:
        vNodePresent = False
        ## For each combination chose the best nodes
        nodesChosen, coverage = vGraph.choseBestNodes(comb)
        for node in nodesChosen:
            if (node.virtual == True):
                vNodePresent = True
        ## If the nodes chosen in particular combination of virtual Nodes are all normal node
        ## Chose the one with best maximum Coverage
        if (not vNodePresent and coverage > maxCoverage):
            maxCoverage = coverage
            maxCoverageNodeSet = nodesChosen

        vGraph.markNodesUnvisited()

    ## if all the combinations contain a virtual node


    return maxCoverageNodeSet

if __name__ == "__main__":

    start = time.time()
    ## Creating Basic Graph
    Graph = GraphClass("diverseCoverage")
    ##createBasicGraph(Graph)
    cg.creatingGraph(Graph,0,5100)

    ##Graph.drawGraphColors()
    for i in range(4):
        ## Building the virutal Graph
        vGraph = GraphClass("virtual Graph")
        vGraph.G = Graph.G.copy()
        maxCoverageSet = createVirtualGraph(vGraph)
        print("---------------------------------------")
        for node in maxCoverageSet:
            print(node)

        ## Setting the nodes as covered
        Graph.setNodesCovered(maxCoverageSet)
        ## Create edges between selected nodes
        Graph.insertSelectedEdges(maxCoverageSet)
        ## Vertices are marked unvisited for the next iteration
        Graph.markNodesUnvisited()

        del vGraph
        ##del maxCoverageSet
        try:
            diameter = nx.diameter(Graph.G)
        except nx.NetworkXError as m :
            diameter = "infinity"
        print("diameter of the graph : " + str(diameter))
        nodeCount, coveredCount = Graph.measureCoveredNodes()
        print("Node Count = %d , Coverage Count = %d" % (nodeCount, coveredCount))

    end = time.time()

    ## Calculating all the nodes that are covered


    print("Execution Time : " + str(end - start))
    ##Graph.drawGraphColors()
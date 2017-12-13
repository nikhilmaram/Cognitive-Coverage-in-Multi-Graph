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
        self._covered = False

    def __str__(self):
        return self.name

class coverageClass:
    def __init__(self,nodeList,featureCountList):
        self.nodeList = nodeList
        self.featureCountList = featureCountList
        #print(self.nodeList)
        #print(len(self.featureCountList))

    def __str__(self):
        string = ""
        for node in self.nodeList:
            string += "Node"+str(node.name)+", "
        return string + "feature1:"+str(self.featureCountList["feature1"])\
        +", feature2:" + str(self.featureCountList["feature1"])+", feature3:"+str(self.featureCountList["feature2"])

class GraphClass:
    def __init__(self,name):
        self.name = name
        self.G = nx.Graph()

    def createNode(self,name,feature1,feature2,feature3):
        node = Node(name,feature1,feature2,feature3)
        self.G.add_node(node)
        return node

    def addNode(self,name,feature1,feature2,feature3):
        self.G.add_node(Node(name,feature1,feature2,feature3))

    def createEdge(self,node1,node2):
        self.G.add_edge(node1,node2)

    def drawGraph(self):
        nx.draw(self.G,with_labels=True)
        plt.show()

    ## Creating a color map for each node for visualisation
    def drawGraphColors(self):
        node_color =[]
        for node in self.G.nodes:
            if(node.feature1 == True and node.feature2 == True and node.feature3 == True):
                node_color.append(1)
            elif(node.feature1 == True and node.feature2 == True):
                node_color.append(3)
            elif(node.feature1 and node.feature3 == True):
                node_color.append(5)
            elif (node.feature2 == True and node.feature3 == True) :
                node_color.append(7)
            elif(node.feature1 == True):
                node_color.append(9)
            elif(node.feature2== True):
                node_color.append(11)
            elif (node.feature3 == True):
                node_color.append(13)
            else:
                node_color.append(15)

        nx.draw(self.G,with_labels=True,node_color=node_color,pos=nx.circular_layout(self.G))
        plt.show()


    ## For given set of nodes we generate a coverage class which specifies the feature count of the features
    def coverageSet(self,nodeList,features):
        coveredNodes = []
        featureCount = {}

        for feature in features:
            featureCount[feature] = 0

        for node in nodeList:
            ## Checking the nodes that are considered
            if node not in coveredNodes:
                for feature in features:
                    if hasattr(node, feature) and (getattr(node, feature)==True):
                        featureCount[feature] += 1
            coveredNodes.append(node)

            ## Checking the neighbors of the nodes
            for neighbor in self.G.neighbors(node):
                ## Do not consider the node which has already considered
                if neighbor not in coveredNodes:
                    for feature in features:
                        if hasattr(neighbor, feature) and (getattr(neighbor, feature) == True):
                            featureCount[feature] += 1

                ## Add the neighbor to the negihbor list
                coveredNodes.append(neighbor)

            coverageObject = coverageClass(nodeList,featureCount)
        return coverageObject

    ## Recursively chosing the nodes depdending on the size to form a nodeSet
    def choseRecursiveCoverageSet(self,features,committeSize):
        nodeSet = list(self.G.nodes)
        presentNodeSet = []
        nodeCombinations = []
        self.choseRecursiveCoverageSetUtils(features,nodeSet,0,committeSize,presentNodeSet,nodeCombinations)
        return nodeCombinations

    def choseRecursiveCoverageSetUtils(self,features,nodeSet,start,committeeSize,presentNodeSet,nodeCombinations):
        ## Number of nodes in the presentNode set is total number of nodes to be considered
        if(committeeSize == len(presentNodeSet)):
            ##nodeCombinations.append(presentNodeSet)
            currCoverageSet = self.coverageSet(presentNodeSet,features)
            nodeCombinations.append(copy.deepcopy(currCoverageSet))
            return

        for i in range(start,len(nodeSet)):
            presentNodeSet.append(nodeSet[i])
            self.choseRecursiveCoverageSetUtils(features,nodeSet,i+1,committeeSize,presentNodeSet,nodeCombinations)
            presentNodeSet.remove(presentNodeSet[len(presentNodeSet)-1])

    ## Chosing the best nodeSet which contains all the feaures and covers maximum features
    def choseBestNodes(self,fullCoverageSet,featureList):
        maxFeatureCount = 0
        maxCoverageNode = fullCoverageSet[0]
        containsAllFeatures = True
        for coverage in fullCoverageSet:
            featureCountList = coverage.featureCountList
            featureCount = 0
            containsAllFeatures = True
            for value in featureCountList.values():
                if value == 0:
                    containsAllFeatures = False
                featureCount+=value

            if (containsAllFeatures and (featureCount > maxFeatureCount)):
                maxFeatureCount = featureCount
                maxCoverageNode = coverage

        return maxCoverageNode.nodeList

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
                node1Name = nodeList[i].name
                node2Name = nodeList[j].name
                self.createEdge(cg.name2Node[node1Name], cg.name2Node[node2Name])

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

    cg.name2Node['1'] = Node1
    cg.name2Node['2'] = Node2
    cg.name2Node['3'] = Node3
    cg.name2Node['4'] = Node4
    cg.name2Node['5'] = Node5
    cg.name2Node['6'] = Node6
    cg.name2Node['7'] = Node7
    cg.name2Node['8'] = Node8
    cg.name2Node['9'] = Node9
    cg.name2Node['10'] = Node10


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





if __name__ == "__main__":

    start = time.time()
    Graph = GraphClass("bruteForce")

    ##createBasicGraph(Graph)
    cg.creatingGraph(Graph,0,100)
    ##Graph.drawGraphColors()

    for i in range(4):
        nodeSelected = Graph.choseRecursiveCoverageSet(["feature1", "feature2", "feature3"],3)
        bestNodes = Graph.choseBestNodes(nodeSelected, ["feature1", "feature2", "feature3"])
        for node in bestNodes:
            print(node.name)

        ##Graph.drawGraphColors()
        ## Setting the nodes which are covered
        Graph.setNodesCovered(bestNodes)
        Graph.insertSelectedEdges(bestNodes)
        ##Graph.drawGraphColors()
        try:
            diameter = nx.diameter(Graph.G)
        except nx.NetworkXError as m :
            diameter = "infinity"
        print ("diameter of the graph : " + str(diameter))
        nodeCount, coveredCount = Graph.measureCoveredNodes()
        print("Node Count = %d , Coverage Count = %d" % (nodeCount, coveredCount))

    end = time.time()
    ## Calculating the nodes that are covered


    print("Execution Time : " + str(end - start))


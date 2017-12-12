import networkx as nx
name2Node = {}
attribValue ={'0' : False,'1' : True}
def creatingGraph(Graph,minNumber = 0 ,maxNumber = 100):
    f1 = open("../facebook_agm_small_tcl_aid/facebook_agm_small_tcl_aid.attr","r")
    f2 = open("../facebook_agm_small_tcl_aid/facebook_agm_small_tcl_aid.lab","r")
    f3 = open("../facebook_agm_small_tcl_aid/facebook_agm_small_tcl_aid.edges", "r")

    attributes = {}
    ## Attributes present in file1
    for i,l in enumerate(f1):
        values = l.strip('\n').split("::")
        attributes[values[0]] = {}
        attributes[values[0]]["attribute1"] = values[1]
        attributes[values[0]]["attribute2"] = values[2]
    ## Attributes present in file2
    for i,l in enumerate(f2):
        values = l.strip('\n').split("::")
        attributes[values[0]]["attribute3"] = values[1]

    ## Creating the nodes
    for key in attributes.keys():
        if int(key) < maxNumber and int(key) > minNumber:
            node = Graph.createNode(key,attribValue[attributes[key]["attribute1"]],attribValue[attributes[key]["attribute2"]],attribValue[attributes[key]["attribute3"]])
            name2Node[key] = node

    ## Creating the edges
    for i,l in enumerate(f3):
        values = l.strip('\n').split("::")
        if values[0] in name2Node.keys() and values[1] in name2Node.keys():
            Graph.createEdge(name2Node[values[0]],name2Node[values[1]])





if __name__ == "__main__":
    G = nx.Graph
    creatingGraph(G)
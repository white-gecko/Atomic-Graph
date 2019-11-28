import sys
import setSearchPath
import rdflib
import coloring


def isomorph(graph1, graph2):
    colouringAlgorithm = coloring.IsomorphicPartitioner()
    colourPartitioning0 = colouringAlgorithm.partitionIsomorphic(graph1)
    colourPartitioning1 = colouringAlgorithm.partitionIsomorphic(graph2)
    return (colourPartitioning0 == colourPartitioning1)


RDFFormat = []
graphs = []
testType = ""
flag = ""
skipFirst = True
for arg in sys.argv:
    if(skipFirst):
        skipFirst = False
        continue
    # set flag for next parameter
    if(arg[0] == "-"):
        flag = arg
        continue
    # use set flag parameter
    if(flag == "-f"):
        RDFFormat.append(arg)
        flag = ""
        continue
    if(flag == "-t"):
        testType = arg
        continue
    graphs.append(arg)

if(testType == "colouring"):
    g1 = rdflib.Graph()
    colouringAlgorithm = coloring.IsomorphicPartitioner()
    colouringAlgorithm.partitionIsomorphic(g1.parse(graphs[0],
                                                    format=RDFFormat[0]))
else:
    g1 = rdflib.Graph()
    g2 = rdflib.Graph()
    isomorph(g1.parse(graphs[0], format=RDFFormat[0]),
             g2.parse(graphs[1], format=RDFFormat[1]))

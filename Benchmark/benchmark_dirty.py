import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import rdflib
import atomicGraph
import coloring


def isomorph(graph1, graph2):
    colouringAlgorithm = coloring.IsomorphicPartitioner()
    colourMap1 = colouringAlgorithm.canonicalise(graph1).clr
    colourGroup1 = colouringAlgorithm.groupByColour(graph1, colourMap1)
    colourMap2 = colouringAlgorithm.canonicalise(graph2).clr
    colourGroup2 = colouringAlgorithm.groupByColour(graph2, colourMap2)
    if len(colourGroup1) == len(colourGroup2):
        for colour in colourGroup1:
            if(not (colour in colourGroup2)):
                return False
    else:
        return False
    return True


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
    colouringAlgorithm.canonicalise(g1.parse(graphs[0], format=RDFFormat[0]))
else:
    g1 = rdflib.Graph()
    g2 = rdflib.Graph()
    isomorph(g1.parse(graphs[0], format=RDFFormat[0]),
             g2.parse(graphs[1], format=RDFFormat[1]))

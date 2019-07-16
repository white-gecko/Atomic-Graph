import os
import sys
import inspect
import graphconverter
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import rdflib
import atomicGraph
import coloring
import timeit
import __main__


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


def benchmarkColouring(graph):
    setup = """
import coloring
import __main__
colouringAlgorithm = coloring.IsomorphicPartitioner()
"""
    __main__.graph = graph
    res = (timeit.
           timeit(stmt="colouringAlgorithm.canonicalise(__main__.graph)",
                  setup=setup, number=1))
    print(res)


def benchmarkIsomorphism(graph1, graph2, referenceResult=None):
    setup = """
import __main__
"""
    __main__.graph1 = graph1
    __main__.graph2 = graph2
    res = (timeit.
           timeit(stmt="__main__.isomorph(__main__.graph1, __main__.graph2)",
                  setup=setup, number=1))
    print(res)
    if(referenceResult is not None):
        isomorphic = isomorph(graph1, graph2)
        if(isomorphic != referenceResult):
            raise Exception(("Isomorphism test for ... and ... should be {}"
                             " but was {}").format(isomorphic, referenceResult)
                            )


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
    if RDFFormat[0] == "nquads":
        g1 = rdflib.graph.ConjunctiveGraph()
        g1.parse(graphs[0], format="nquads")
        for context in iter(g1.contexts()):
            benchmarkColouring(context)
    elif RDFFormat[0] == "graph":
        graph = graphconverter.convertGraphToRDF(graphs[0])
        benchmarkColouring(graph)
    else:
        g1 = rdflib.Graph()
        graph = g1.parse(graphs[0], format=RDFFormat[0])
        benchmarkColouring(graph)
else:
    # TODO add context relevant changes like in the true body
    g1 = rdflib.Graph()
    g1 = g1.parse(graphs[0], format=RDFFormat[0])
    g2 = rdflib.Graph()
    g2 = g2.parse(graphs[1], format=RDFFormat[1])
    benchmarkIsomorphism(g1, g2)

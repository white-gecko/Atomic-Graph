import sys
import graphconverter
import setSearchPath
import rdflib
import coloring
import timeit
import __main__


def isomorph(graph1, graph2):
    colouringAlgorithm = coloring.IsomorphicPartitioner()
    colourPartitioning0 = colouringAlgorithm.partitionIsomorphic(graph1)
    colourPartitioning1 = colouringAlgorithm.partitionIsomorphic(graph2)
    return (colourPartitioning0 == colourPartitioning1)


def benchmarkColouring(graph):
    setup = """
import coloring
import __main__
colouringAlgorithm = coloring.IsomorphicPartitioner()
"""
    __main__.graph = graph
    res = (timeit.
           timeit(stmt="colouringAlgorithm.partitionIsomorphic(__main__.graph)",
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


def prepareGraphs(graphs, RDFFormat):
    graphQueue = []
    for i in range(0, len(graphs)):
        if RDFFormat[i] == "nquads":
            g1 = rdflib.graph.ConjunctiveGraph()
            g1.parse(graphs[i], format="nquads")
            for context in iter(g1.contexts()):
                graphQueue.append(context)
        elif RDFFormat[i] == "graph":
            graph = graphconverter.convertGraphToRDF(graphs[i])
            graphQueue.append(graph)
        else:
            g1 = rdflib.Graph()
            graph = g1.parse(graphs[i], format=RDFFormat[i])
            graphQueue.append(graph)
    return graphQueue


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
    for graph in prepareGraphs(graphs, RDFFormat):
        benchmarkColouring(graph)
else:
    graphs = prepareGraphs(graphs, RDFFormat)
    for i in range(0, int(len(graphs) / 2)):
        benchmarkIsomorphism(graphs[i * 2], graphs[i * 2 + 1])

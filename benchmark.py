import rdflib
import atomicGraph
import coloring
import timeit
import __main__


def isomorph(graph1, graph2):
    print(len(graph1.all_nodes()))
    print(len(graph2.all_nodes()))
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


def benchmarkColoring(graph):
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


g1 = rdflib.Graph()
g2 = rdflib.Graph()
benchmarkColoring(g1.parse("example1.ttl", format="n3"))
g1 = rdflib.Graph()
benchmarkIsomorphism(g1.parse("example1.ttl", format="n3"),
                     g2.parse("example2.ttl", format="n3"))

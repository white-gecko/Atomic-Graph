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


def compareColourMap(graph1, colourMap1, graph2, colourMap2):
    print("started comparing")
    for subj, pred, obje in graph1:
        print("{} <> {} <> {}".format(subj, pred, obje))
        print("{} ==> {} ==> {}\n<<<".format(colourMap1[subj],
                                             colourMap1[pred],
                                             colourMap1[obje]))
    print("=============================================")
    for subj, pred, obje in graph2:
        print("{} <> {} <> {}".format(subj, pred, obje))
        print("{} ==> {} ==> {}\n<<<".format(colourMap2[subj],
                                             colourMap2[pred],
                                             colourMap2[obje]))


g1 = rdflib.Graph()
g2 = rdflib.Graph()
graph1 = g1.parse("./Examples/example1.ttl", format="n3")
graph2 = g2.parse("./Examples/example2.ttl", format="n3")
slicer1 = atomicGraph.GraphSlicer(graph1)
slicer1.run()
slicer2 = atomicGraph.GraphSlicer(graph2)
slicer2.run()
atomic = next(iter(slicer1.getAtomicGraphs()))
print(slicer1 == slicer2)

graphIso1 = rdflib.Graph()
graphIso2 = rdflib.Graph()
graphIso1 = graphIso1.parse("./Examples/isoSimpleGraph1.ttl", format="n3")
graphIso2 = graphIso2.parse("./Examples/isoSimpleGraph2.ttl", format="n3")
colouringAlgorithm = coloring.IsomorphicPartitioner()
compareColourMap(graphIso1, colouringAlgorithm.canonicalise(graphIso1).clr,
                 graphIso2, colouringAlgorithm.canonicalise(graphIso2).clr)
print("isomorph?: " + isomorph(graphIso1, graphIso2).__str__())

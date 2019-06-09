import rdflib
import atomicGraph
import coloring

g1 = rdflib.Graph()
g2 = rdflib.Graph()
graph1 = g1.parse("example1.ttl", format="n3")
graph2 = g2.parse("example2.ttl", format="n3")

slicer1 = atomicGraph.GraphSlicer(graph1)
slicer1.run()
slicer2 = atomicGraph.GraphSlicer(graph2)
slicer2.run()
atomic = next(iter(slicer1.getAtomicGraphs()))

print(slicer1 == slicer2)

graphIso1 = rdflib.Graph()
graphIso2 = rdflib.Graph()
graphIso1 = graphIso1.parse("isoSimpleGraph1.ttl", format="n3")
graphIso2 = graphIso2.parse("isoSimpleGraph2.ttl", format="n3")
colouringAlgorithm = coloring.GraphIsoPartitioner()


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


compareColourMap(graphIso1, colouringAlgorithm.colour(graphIso1),
                 graphIso2, colouringAlgorithm.colour(graphIso2))

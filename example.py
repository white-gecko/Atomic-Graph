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

partition = coloring.GraphIsoPartitioner()
atomic = next(iter(slicer1.getAtomicGraphs()))
partition.colour(atomic)

print(slicer1 == slicer2)

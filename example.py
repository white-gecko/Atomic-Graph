import rdflib
import atomicGraph

g1 = rdflib.Graph()
g2 = rdflib.Graph()
graph1 = g1.parse("example.ttl", format="n3")
graph2 = g2.parse("example.ttl", format="n3")

slicer1 = atomicGraph.GraphSlicer(graph1)
slicer1.run()
slicer2 = atomicGraph.GraphSlicer(graph2)
slicer2.run()

print(slicer1 == slicer2)

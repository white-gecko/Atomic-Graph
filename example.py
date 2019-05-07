import rdflib
import atomicGraph

g = rdflib.Graph()
graph = g.parse("example.ttl", format="n3")


slicer = atomicGraph.GraphSlicer(graph)
slicer.run()
graphs = slicer.getAtomicGraphs()
for _graph in list(graphs):
    for subj, pred, obj in _graph:
        print("{0} {1} {2}".format(subj, pred, obj))
    print("---------------------------------------")

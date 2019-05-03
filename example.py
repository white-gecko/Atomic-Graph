import rdflib
import atomicGraph

g = rdflib.Graph()
graph = g.parse(format="n3",
                data=("<http://example.org/subject> "
                      "<http://example.org/predicate> "
                      "[<http://example.org/predicate> _:object1;"
                      " <http://example.org/predicate> _:object2]."
                      "<http://example.org/subject1> "
                      "<http://example.org/predicate> "
                      "<http://example.org/subject>."
                      "<http://example.org/subject1> "
                      "<http://example.org/predicate> _:a ."
                      "<http://example.org/subject1> "
                      "<http://example.org/predicate> _:b ."
                      "<http://example.org/labelsubject1> "
                      "<http://example.org/predicate> \"This is a label\"."
                      "<http://example.org/labelsubject2> "
                      "<http://example.org/predicate> \"This is a label\"."
                      ))


slicer = atomicGraph.GraphSlicer(graph)
slicer.run()
graphs = slicer.getAtomicGraphs()
for _graph in graphs:
    for subj, pred, obj in _graph:
        print("{0} {1} {2}".format(subj, pred, obj))
    print("---------------------------------------")

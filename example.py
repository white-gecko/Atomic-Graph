import rdflib
import atomicGraph

graph_string1 = (
                "<http://example.org/subject> <http://example.org/predicate> "
                "[<http://example.org/predicate> _:object1;"
                " <http://example.org/predicate> _:object2]."
                "<http://example.org/subject1> <http://example.org/predicate> "
                "<http://example.org/subject>."
                "<http://example.org/subject1> "
                "<http://example.org/predicate> _:a ."
                "<http://example.org/subject1> "
                "<http://example.org/predicate> _:b ."
                "<http://example.org/labelsubject1> "
                "<http://example.org/predicate> \"This is a label\"."
                "<http://example.org/labelsubject2> "
                "<http://example.org/predicate> \"This is a label\"."
                )

graph_string2 = (
                "<http://example.org/subject1> <http://example.org/predicate> "
                "<http://example.org/subject>."
                "<http://example.org/subject1> "
                "<http://example.org/predicate> _:1 ."
                "<http://example.org/subject1> "
                "<http://example.org/predicate> _:2 ."
                "<http://example.org/subject> <http://example.org/predicate> "
                "[<http://example.org/predicate> _:obja;"
                " <http://example.org/predicate> _:objb]."
                "<http://example.org/labelsubject1> "
                "<http://example.org/predicate> \"This is a label\"."
                "<http://example.org/labelsubject2> "
                "<http://example.org/predicate> \"This is a label\"."
                )
g1 = rdflib.Graph()
g2 = rdflib.Graph()
graph1 = g1.parse(format="n3", data=graph_string1)
graph2 = g2.parse(format="n3", data=graph_string2)

slicer1 = atomicGraph.GraphSlicer(graph1)
slicer1.run()
slicer2 = atomicGraph.GraphSlicer(graph2)
slicer2.run()

print(slicer1 == slicer2)

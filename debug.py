import rdflib
import comp_graph
from Benchmark import graphconverter

#graph0 = graphconverter.convertGraphToRDF("./Examples/example1.ttl")
#graph1 = graphconverter.convertGraphToRDF("./Examples/example2.ttl")
graph0 = rdflib.Graph()
graph1 = rdflib.Graph()
graph0.parse("./Examples/isoSimpleGraph1.ttl", format="n3")
graph1.parse("./Examples/isoSimpleGraph2.ttl", format="n3")
isoGraph0 = comp_graph.ComparableGraph(store=graph0.store, identifier=graph0.identifier, namespace_manager=graph0.namespace_manager)
isoGraph1 = comp_graph.ComparableGraph(store=graph1.store, identifier=graph1.identifier, namespace_manager=graph1.namespace_manager)
isoGraph0 + isoGraph1
isoGraph0 - isoGraph1
isoGraph0 | isoGraph1
isoGraph0 & isoGraph1
isoGraph0 * isoGraph1
isoGraph0 ^ isoGraph1
for subj, pred, obj in isoGraph0:
    print("{} {} {}".format(subj, pred, obj))
print(isoGraph0.equal(isoGraph1))

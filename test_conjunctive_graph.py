import atomicgraphs
from atomicgraphs import atomic_graph
import rdflib


graph = rdflib.Graph('AtomicStore')
graph.parse(source="./examples/example1.ttl", format="n3")
factory = atomic_graph.AtomicGraphFactory(graph)
controllData = []
for atomic in factory:
    controllData.append(atomic.__str__())
cGraph = rdflib.ConjunctiveGraph('AtomicStore')
bNodeA = rdflib.BNode("_:0")
bNodeB = rdflib.BNode("_:1")
bNodeC = rdflib.BNode("_:2")
bNodeD = rdflib.BNode("_:3")
bNodeE = rdflib.BNode("_:4")

cGraph.add((rdflib.URIRef("http://subject.com/0"),
            rdflib.URIRef("http://predicate.com/"),
            bNodeA,
            rdflib.URIRef("http://context.com/0")))
cGraph.add((bNodeA,
            rdflib.URIRef("http://predicate.com/"),
            bNodeB,
            rdflib.URIRef("http://context.com/0")))
cGraph.add((bNodeB,
            rdflib.URIRef("http://predicate.com/"),
            rdflib.URIRef("http://object.com/1"),
            rdflib.URIRef("http://context.com/0")))
# atomic wise bNodeC is cut off
cGraph.add((rdflib.URIRef("http://object.com/1"),
            rdflib.URIRef("http://predicate.com/"),
            bNodeC,
            rdflib.URIRef("http://context.com/0")))

# combine bNodeB and bNodeC but in another context
cGraph.add((bNodeB,
            rdflib.URIRef("http://predicate.com/"),
            bNodeD,
            rdflib.URIRef("http://context.com/1")))
cGraph.add((bNodeD,
            rdflib.URIRef("http://predicate.com/"),
            bNodeC,
            rdflib.URIRef("http://context.com/1")))

factory = atomic_graph.AtomicGraphFactory(cGraph)
container = [iter(factory)]
print(len(container))

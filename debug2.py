from atomicgraphs import atomic_store
import rdflib
from rdflib import URIRef

graphA = rdflib.Graph('AtomicStore')
#graphA.parse(source="./examples/example1.ttl", format="n3")

graphB = rdflib.Graph('AtomicStore')
#graphB.parse(source="./examples/example2.ttl", format="n3")

triple = (rdflib.URIRef("http://subject.com"), rdflib.URIRef("http://predicate.com"), rdflib.URIRef("http://object.com"))
graphA.add(triple)
graphA.store.moveStatement(triple, graphA, graphB)

for subj, pred, obj in graphA:
    print("{} {} {}".format(subj, pred, obj))

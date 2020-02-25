import rdflib
import unittest
import setSearchPath
from atomicgraphs import atomic_graph


class TestConjunctiveGraphCases(unittest.TestCase):
    def testAtomiseConjunctiveGraph(self):
        cGraph = rdflib.ConjunctiveGraph('AtomicStore')
        bNodeA = rdflib.BNode("_:0")
        bNodeB = rdflib.BNode("_:1")
        bNodeC = rdflib.BNode("_:2")
        bNodeD = rdflib.BNode("_:3")

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

        controllGroup0 = set()
        controllGroup0.add(("(rdflib.term.BNode('_:1'), "
                            "rdflib.term.URIRef('http://predicate.com/'),"
                            " rdflib.term.URIRef('http://object.com/1'))"))
        controllGroup0.add(("(rdflib.term.URIRef('http://subject.com/0'), "
                            "rdflib.term.URIRef('http://predicate.com/'), "
                            "rdflib.term.BNode('_:0'))"))
        controllGroup0.add(("(rdflib.term.BNode('_:0'), "
                            "rdflib.term.URIRef('http://predicate.com/'), "
                            "rdflib.term.BNode('_:1'))"))

        controllGroup1 = set()
        controllGroup1.add(("(rdflib.term.URIRef('http://object.com/1'), "
                            "rdflib.term.URIRef('http://predicate.com/'), "
                            "rdflib.term.BNode('_:2'))"))

        controllGroup2 = set()
        controllGroup2.add(("(rdflib.term.BNode('_:3'), "
                            "rdflib.term.URIRef('http://predicate.com/'), "
                            "rdflib.term.BNode('_:2'))"))
        controllGroup2.add(("(rdflib.term.BNode('_:1'), "
                            "rdflib.term.URIRef('http://predicate.com/'), "
                            "rdflib.term.BNode('_:3'))"))

        controllGroups = [controllGroup0, controllGroup1, controllGroup2]

        factory = atomic_graph.AtomicGraphFactory(cGraph)
        for atom in factory:
            group = set()
            for triple in atom:
                group.add(str(triple))
            assert group in controllGroups
            controllGroups.remove(group)
        assert len(controllGroups) == 0


if __name__ == '__main__':
    unittest.main()

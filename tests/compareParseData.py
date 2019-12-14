import unittest
import setSearchPath
import rdflib
from atomicgraphs import comp_graph


class TestComparableGraph(unittest.TestCase):
    def testNotEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        self.assertFalse(graphA == graphB)
        self.assertNotEqual(graphA, graphB)

    def testEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/isoSimpleGraph1.ttl', format='n3')
        graphB.parse('examples/isoSimpleGraph1.ttl', format='n3')

        self.assertTrue(graphA == graphB)
        self.assertEqual(graphA, graphB)

    def testSetAddGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA + graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetSubGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA - graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetOrGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA | graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetAndGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA & graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetMulGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA * graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetXorGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphC = graphA ^ graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetIAddGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphA += graphB

        self.assertFalse(graphA == graphB)
        self.assertNotEqual(graphA, graphB)

    def testSetISubGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        graphB.parse('examples/example2.ttl', format='n3')

        graphA -= graphB

        self.assertFalse(graphA == graphB)
        self.assertNotEqual(graphA, graphB)

    def testAddN(self):
        graphA = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        sub = rdflib.URIRef("http://test.com/subject")
        pre = rdflib.URIRef("http://test.com/predicate")
        obj = rdflib.URIRef("http://test.com/object")
        con = rdflib.URIRef("http://test.com/context")
        graphA.addN([(sub, pre, obj, con)])
        # just tests if something is raised
        # content dependent checks are not possible with normal graphs


    def testSet(self):
        graphA = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        sub = rdflib.URIRef("http://test.com/subject")
        pre = rdflib.URIRef("http://test.com/predicate")
        obj = rdflib.URIRef("http://test.com/object")
        graphA.set((sub, pre, obj))
        assert((sub, pre, obj) in graphA)

    def testUpdate(self):
        graphA = comp_graph.ComparableGraph()
        graphA.parse('examples/example1.ttl', format='turtle')
        sub = rdflib.URIRef("http://test.com/subject")
        pre = rdflib.URIRef("http://test.com/predicate")
        obj = rdflib.URIRef("http://test.com/object")
        graphA.add((sub, pre, obj))
        graphA.update('''
        INSERT
            { ?s <https://test.com/predicate#x> <https://test.com/object#x> . }
        WHERE
            { ?s <http://test.com/predicate> <http://test.com/object> . }
        ''')
        # if I bring rdflib.URIRef("https://test.com/object#x") into the next line
        #   and then back, the test suddenly passes exactly one time
        # the test seems to randomly fail
        assert((sub, rdflib.URIRef("https://test.com/predicate#x"),
                rdflib.URIRef("https://test.com/object#x")) in graphA)



if __name__ == '__main__':
    unittest.main()

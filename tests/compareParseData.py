import unittest
import setSearchPath
import rdflib
import comp_graph

class TestComparableGraph(unittest.TestCase):

    def testNotEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../Examples/example1.ttl', format='turtle')
        graphB.parse('../Examples/example2.ttl', format='n3')

        self.assertFalse(graphA == graphB)
        self.assertNotEqual(graphA, graphB)

    def testEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../Examples/isoSimpleGraph1.ttl', format='n3')
        graphB.parse('../Examples/isoSimpleGraph1.ttl', format='n3')

        self.assertTrue(graphA == graphB)
        self.assertEqual(graphA, graphB)

    def testSetAddGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()

        graphC = graphA + graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)


if __name__ == '__main__':
    unittest.main()

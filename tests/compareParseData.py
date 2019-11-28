import unittest
import setSearchPath
import rdflib
import comp_graph


class TestComparableGraph(unittest.TestCase):
    def testNotEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        self.assertFalse(graphA == graphB)
        self.assertNotEqual(graphA, graphB)

    def testEqualGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/isoSimpleGraph1.ttl', format='n3')
        graphB.parse('../examples/isoSimpleGraph1.ttl', format='n3')

        self.assertTrue(graphA == graphB)
        self.assertEqual(graphA, graphB)

    def testSetAddGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA + graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetSubGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA - graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetOrGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA | graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetAndGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA & graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetMulGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA * graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    def testSetXorGraphs(self):
        graphA = comp_graph.ComparableGraph()
        graphB = comp_graph.ComparableGraph()
        graphA.parse('../examples/example1.ttl', format='turtle')
        graphB.parse('../examples/example2.ttl', format='n3')

        graphC = graphA ^ graphB

        self.assertFalse(graphA == graphC)
        self.assertNotEqual(graphA, graphC)
        self.assertFalse(graphB == graphC)
        self.assertNotEqual(graphB, graphC)

    # TODO other operators


if __name__ == '__main__':
    unittest.main()

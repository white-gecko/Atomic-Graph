import rdflib
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
             inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import coloring


class TestSimpleIsomorphism(unittest.TestCase):

    def testSimpleIsomorphism(self):
        g0 = rdflib.Graph()
        g1 = rdflib.Graph()
        graph0 = g0.parse("../Examples/isoSimpleGraph1.ttl", format="n3")
        graph1 = g1.parse("../Examples/isoSimpleGraph2.ttl", format="n3")
        isoAlgorithm = coloring.IsomorphicPartitioner()
        isoPartition0 = isoAlgorithm.partitionIsomorphicSimple(graph0)
        isoPartition1 = isoAlgorithm.partitionIsomorphicSimple(graph1)
        self.assertTrue(isoPartition0 == isoPartition1)


if __name__ == '__main__':
    unittest.main()

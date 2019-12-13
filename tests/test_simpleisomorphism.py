import rdflib
import unittest
import setSearchPath
from atomicgraphs import coloring


class TestSimpleIsomorphism(unittest.TestCase):

    def testSimpleIsomorphism(self):
        g0 = rdflib.Graph()
        g1 = rdflib.Graph()
        graph0 = g0.parse("examples/isoSimpleGraph1.ttl", format="n3")
        graph1 = g1.parse("examples/isoSimpleGraph2.ttl", format="n3")
        isoAlgorithm = coloring.IsomorphicPartitioner()
        isoPartition0 = isoAlgorithm.partitionIsomorphicSimple(graph0)
        isoPartition1 = isoAlgorithm.partitionIsomorphicSimple(graph1)
        self.assertTrue(isoPartition0 == isoPartition1)


if __name__ == '__main__':
    unittest.main()

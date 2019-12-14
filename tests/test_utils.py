import unittest
import setSearchPath
import rdflib
from atomicgraphs import atomic_graph
import re


class TestUtils(unittest.TestCase):
    def testStr(self):
        graph = rdflib.Graph()
        graph.parse('examples/example1.ttl', format='n3')
        slicer = atomic_graph.AtomicGraphFactory(graph)
        for aGraph in slicer:
            assert(re.match("AtomicHashGraph\(#IsoPartitions:\s\d\)", aGraph.__repr__()))
            assert(re.search("b'[^']+'\sb'[^']+'\sb'[^']+'.", aGraph.__str__()))


if __name__ == '__main__':
    unittest.main()

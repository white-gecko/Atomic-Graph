import rdflib
import unittest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import coloring
import atomicGraph
from Benchmark import graphconverter


class TestIsomorphism(unittest.TestCase):
    def setUp(self):
        self.log = open("Log.txt", "w+")

    def tearDown(self):
        self.log.close()

    def testSimpleIsomorphism(self):
        g0 = rdflib.Graph()
        g1 = rdflib.Graph()
        #graph0 = g0.parse("../../isoSimpleGraph1.ttl", format="n3")
        #graph1 = g1.parse("../../isoSimpleGraph2.ttl", format="n3")
        graph0 = graphconverter.convertGraphToRDF("../../AtomicGraph Files/eval/grid-2/grid-2-100")
        graph1 = graphconverter.convertGraphToRDF("../../AtomicGraph Files/eval/grid-2/grid-2-100")
        isoAlgorithm = coloring.IsomorphicPartitioner()
        isoPartition0 = isoAlgorithm.partitionIsomorphic(graph0)
        isoPartition1 = isoAlgorithm.partitionIsomorphic(graph1)
        self.assertTrue(isoPartition0 == isoPartition1)

    def testIsomorphism(self):
        successes = 0
        fails = 0
        for path, subdirs, files in os.walk("../../AtomicGraph Files/eval/"):
            for file in files:
                graph0 = graphconverter.convertGraphToRDF(os.path.join(path, file))
                graph1 = graphconverter.convertGraphToRDF(os.path.join(path, file))
                isoAlgorithm = coloring.IsomorphicPartitioner()
                isoPartition0 = isoAlgorithm.partitionIsomorphic(graph0)
                isoPartition1 = isoAlgorithm.partitionIsomorphic(graph1)
                result = (isoPartition0 == isoPartition1)
                if(not result):
                    msg = "{} => \n".format(os.path.join(path, file))
                    self.log.write(msg)
                    # show what went wrong
                    msg = "{}\n==\n{}".format(isoPartition0, isoPartition1)
                    self.log.write(msg)
                    fails += 1
                else:
                    successes += 1
                try:
                    self.assertTrue(result)
                except AssertionError:
                    msg = "successes: {}  fails: {}".format(successes, fails)
                    self.log.write(msg)
                    self.log.close()
                    raise
        msg = "successes: {}  fails: {}".format(successes, fails)
        self.log.write(msg)
        self.log.close()

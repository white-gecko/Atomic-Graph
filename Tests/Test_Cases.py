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
    @classmethod
    def setUpClass(cls):
        testGroup = []
        controlGroup = []
        nameGroup = []
        file = open('TestFilePath', 'r')
        testFilePath = file.readline().strip()
        file.close()
        for path, subdirs, files in os.walk(testFilePath):
            for file in files:
                graph0 = graphconverter.convertGraphToRDF(os.path.join(path,
                                                                       file))
                graph1 = graphconverter.convertGraphToRDF(os.path.join(path,
                                                                       file))
                isoAlgorithm = coloring.IsomorphicPartitioner()
                testGroup.append(isoAlgorithm.partitionIsomorphic(graph0))
                controlGroup.append(isoAlgorithm.partitionIsomorphic(graph1))
                nameGroup.append(os.path.join(path, file))
        cls.testGroup = testGroup
        cls.controlGroup = controlGroup
        cls.nameGroup = nameGroup

    def setUp(self):
        self.log = open("Log.txt", "a")

    def tearDown(self):
        self.log.close()

    def testSimpleIsomorphism(self):
        g0 = rdflib.Graph()
        g1 = rdflib.Graph()
        graph0 = g0.parse("../Examples/isoSimpleGraph1.ttl", format="n3")
        graph1 = g1.parse("../Examples/isoSimpleGraph2.ttl", format="n3")
        isoAlgorithm = coloring.IsomorphicPartitioner()
        isoPartition0 = isoAlgorithm.partitionIsomorphicSimple(graph0)
        isoPartition1 = isoAlgorithm.partitionIsomorphicSimple(graph1)
        self.assertTrue(isoPartition0 == isoPartition1)

    def testIsomorphism(self):
        errorPrefix = "TestIsomorphism: "
        error = None
        otherList = iter(self.__class__.controlGroup)
        otherPartition = TestIsomorphism.AlwaysFalse()
        testNames = iter(self.__class__.nameGroup)
        currentName = None
        for isoPartition in self.__class__.testGroup:
            previousName = currentName
            currentName = next(testNames)
            try:
                self.assertFalse(otherPartition == isoPartition)
            except AssertionError as e:
                errorMsg = (errorPrefix
                            + currentName
                            + " should not be isomorph to "
                            + previousName + "\n")
                self.log.write(errorMsg)
                # cache Exception to raise later
                error = e
            otherPartition = next(otherList)
            try:
                self.assertTrue(otherPartition == isoPartition)
            except AssertionError as e:
                errorMsg = (errorPrefix
                            + currentName
                            + " should be isomorph to its self\n")
                self.log.write(errorMsg)
                # cache Exception to raise later
                error = e
        self.log.close()
        # Test should still fail
        if(error is not None):
            raise error

    class AlwaysFalse:
        def __eq__(self, value):
            return False

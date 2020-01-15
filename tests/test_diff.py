import unittest
import re
import setSearchPath
from atomicgraphs import comp_graph

class TestDiff(unittest.TestCase):
    def testDiff(self):
        graph0 = comp_graph.ComparableGraph()
        graph1 = comp_graph.ComparableGraph()
        graph0.parse(source="../examples/example1.ttl", format="n3")
        graph1.parse(source="../examples/example2.ttl", format="n3")
        diffTupel = graph0.diff(graph1)
        tests = [r"^http:\/\/example\.org\/subjectT\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$",
                 r"^[a-zA-Z0-9]+\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$",
                 r"^[a-zA-Z0-9]+\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$"]
        for aGraph in diffTupel[0]:
            for subj, pred, obje in aGraph:
                done = None
                for test in tests:
                    if(re.match(test, "{} {} {}".format(subj, pred, obje))):
                        done = test
                self.assertNotEqual(done, None)
                tests.remove(test)
        assert(tests.__len__() == 0)
        tests = [r"^http:\/\/example\.org\/subject\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$",
                 r"^[a-zA-Z0-9]+\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$",
                 r"^[a-zA-Z0-9]+\shttp:\/\/example\.org\/predicate\s[a-zA-Z0-9]+$"]
        for aGraph in diffTupel[1]:
            for subj, pred, obje in aGraph:
                done = None
                for test in tests:
                    if(re.match(test, "{} {} {}".format(subj, pred, obje))):
                        done = test
                self.assertNotEqual(done, None)
                tests.remove(test)
        assert(tests.__len__() == 0)


if __name__ == '__main__':
    unittest.main()

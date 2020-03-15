import rdflib
import unittest
import setSearchPath
from atomicgraphs import atomic_graph


class TestSelectiveComparableCases(unittest.TestCase):
    def testAtomiseOnlySelectiveGraph(self):
        graph = rdflib.Graph()
        graph.parse(source="./examples/example1.ttl", format="n3")

        def getRandomBlankNode():
            for context in graph:
                for node in context:
                    if issubclass(node.__class__, rdflib.BNode):
                        yield node

        def getSpecificBlankNode(last_two_places):
            for context in graph:
                for node in context:
                    if (node.n3()[-2:] == last_two_places):
                        return node
        bNodeGen = iter(getRandomBlankNode())
        exampleBNodeA = next(bNodeGen)
        exampleBNodeB = next(bNodeGen)
        atomicFactory = atomic_graph.AtomicGraphFactory(graph, [exampleBNodeA, exampleBNodeB])
        resultList = list(iter(atomicFactory))
        result = set(iter(resultList))
        aInAtomic = False
        bInAtomic = False
        differentGraphs = False
        for atomic in result:
            nodesOfAtomic = atomic.all_nodes()
            assert((exampleBNodeA in nodesOfAtomic) or (exampleBNodeB in nodesOfAtomic))
            aInAtomic = aInAtomic or (exampleBNodeA in nodesOfAtomic)
            bInAtomic = bInAtomic or (exampleBNodeB in nodesOfAtomic)
            differentGraphs = differentGraphs or (not (aInAtomic and bInAtomic))
        if differentGraphs:
            if(resultList[0] == resultList[1]):
                # the resulting atomic graphs are isomorph
                assert(len(result) == 1)
            else:
                assert(len(result) == 2)
        else:
            # the used bNodes are both in the same graph
            assert(len(result) == 1)


if __name__ == '__main__':
    unittest.main()

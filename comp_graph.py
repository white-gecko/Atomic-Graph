import rdflib
import atomicGraph
import coloring


class ComparableGraph(rdflib.Graph):
    def __init__(self, graph):
        super()
        # TODO do something more clever
        #      we only copy so we can use this object like the original graph
        # for triple in graph.triples((None, None, None)):
        #     self.add(triple)
        slicer = atomicGraph.GraphSlicer(graph)
        slicer.run()
        self._sortAndGroupAtomicGraphs(slicer.getAtomicGraphs())

    def __eq__(self, value):
        if(issubclass(value.__class__, ComparableGraph)):
            if(len(value.atomicGraphTupel) != len(self.atomicGraphTupel)):
                return False
            otherATL = iter(value.atomicGraphTupel)
            for atomicTupel in self.atomicGraphTupel:
                if(not self._compareListSets(atomicTupel, next(otherATL))):
                    return False
            return True
        if(issubclass(value.__class__, rdflib.Graph)):
            return self == ComparableGraph(value)
        return False

    def _sortAndGroupAtomicGraphs(self, atomicSet):
        partitioner = coloring.IsomorphicPartitioner()

        atomicGraphs = list(atomicSet)
        atomicGraphs.sort(key=lambda atomic: (atomic.getMeta()[0],
                                              atomic.getMeta()[1]),
                          reverse=True)
        meta0 = -1
        meta1 = -1
        metaGroup = set()
        self.atomicGraphTupel = []
        for atomic in atomicGraphs:
            if(atomic.getMeta()[0] != meta0 or atomic.getMeta()[1] != meta1):
                if(metaGroup):
                    self.atomicGraphTupel.append(metaGroup)
                meta0 = atomic.getMeta()[0]
                meta1 = atomic.getMeta()[1]
                metaGroup = set()
            metaGroup.add((atomic, partitioner.partitionIsomorphic(atomic)))
        if metaGroup:
            self.atomicGraphTupel.append(metaGroup)

    def _compareListSets(self, setA, setB):
        setAC = setA.copy()
        setBC = setB.copy()
        for graphColourPairA in setAC:
            found = False
            for graphColourPairB in setBC:
                if(graphColourPairA[1] == graphColourPairB[1]):
                    setBC.remove(graphColourPairB)
                    found = True
                    break
            if(not found):
                return False
        return True

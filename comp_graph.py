import rdflib
import atomicGraph
import coloring


class ComparableGraph(rdflib.Graph):
    def __init__(self, graph):
        super()
        slicer = atomicGraph.GraphSlicer(graph)
        slicer.run()
        self.atomicGraphs = set()
        partitioner = coloring.IsomorphicPartitioner()
        for aGraph in slicer.getAtomicGraphs():
            self.atomicGraphs.add(ComparableGraph.AtomicHashGraph(aGraph, partitioner))

    def __eq__(self, value):
        if(issubclass(value.__class__, ComparableGraph)):
            if(len(self.atomicGraphs) == len(value.atomicGraphs)):
                # just check if all graphs are in the others atomicGraphs set
                for aGraph in self.atomicGraphs:
                    if(aGraph not in value.atomicGraphs):
                        return False
                return True
            return False
        if(issubclass(value.__class__, rdflib.Graph)):
            return self == ComparableGraph(value)
        return False

    class AtomicHashGraph:
        def __init__(self, atomicGraph, isomorphicPartitioner):
            self.atomicGraph = atomicGraph
            self.colourPartitions = isomorphicPartitioner.partitionIsomorphic(atomicGraph)

        def __eq__(self, value):
            return self.colourPartitions == value.colourPartitions

        def __hash__(self):
            return self.colourPartitions.__hash__()

        def __lt__(self, other):
            return hash(self) < hash(other)

        def __le__(self, other):
            return hash(self) <= hash(other)

        def __str__(self):
            result = ""
            for subj, pred, obj in self.atomicGraph:
                result += "{0} {1} {2}.\n".format(self.colourPartitions[subj],
                                                  self.colourPartitions[pred],
                                                  self.colourPartitions[obj])
            return result

        def __repr__(self):
            return "AtomicHashGraph(#IsoPartitions: {})".format(len(self.colourPartitions))

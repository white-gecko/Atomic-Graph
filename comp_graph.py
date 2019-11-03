import rdflib
import atomic_graph
import coloring


class ComparableGraph(rdflib.Graph):
    def __init__(self, graph, atomicGraphs=None):
        super(ComparableGraph, self).__init__(graph.store,
                                              graph.identifier, graph.namespace_manager)
        self.graph = graph
        if atomicGraphs is None:
            slicer = atomic_graph.GraphSlicer(graph)
            slicer.run()
            self.atomicGraphs = set()
            partitioner = coloring.IsomorphicPartitioner()
            for aGraph in slicer.getAtomicGraphs():
                self.atomicGraphs.add(ComparableGraph.AtomicHashGraph(aGraph, partitioner))
        else:
            self.atomicGraphs = atomicGraphs

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

    def __add__(self, other):
        result = ComparableGraph(self.graph.__or__(other.graph),
                                 self.atomicGraphs.__or__(other.atomicGraphs))
        return result

    def __sub__(self, other):
        result = ComparableGraph(self.graph.__sub__(other.graph),
                                 self.atomicGraphs.__sub__(other.atomicGraphs))
        return result

    def __or__(self, other):
        return self.__add__(other)

    def __and__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        result = ComparableGraph(self.graph.__mul__(other.graph),
                                 self.atomicGraphs.__and__(other.atomicGraphs))
        return result

    def __xor__(self, other):
        result = ComparableGraph(self.graph.__xor__(other.graph),
                                 self.atomicGraphs.__xor__(other.atomicGraphs))
        return result

    def __hash__(self):
        return super(ComparableGraph, self).__hash__()

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

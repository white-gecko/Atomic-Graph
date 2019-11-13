import rdflib
import atomic_graph


class ComparableGraph(rdflib.Graph):
    def __init__(self, graph, atomicGraphs=None, store='default', identifier=None, namespace_manager=None):
        super(ComparableGraph, self).__init__(store, identifier, namespace_manager)
        self.graph = graph
        if atomicGraphs is None:
            slicer = atomic_graph.AtomicGraphFactory(graph)
            self.atomicGraphs = set()
            for aGraph in slicer:
                self.atomicGraphs.add(aGraph)
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

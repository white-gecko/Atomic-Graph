import rdflib
import atomic_graph
from hash_combiner import HashCombiner


class ComparableGraph(rdflib.Graph, HashCombiner):
    def __init__(self, store='default', identifier=None, namespace_manager=None):
        super(ComparableGraph, self).__init__(store, identifier, namespace_manager)
        self.invalidate()

    def __add__(self, other):
        result = ComparableGraph(super().__or__(other).store)
        result.partition = self.partition.__or__(other.partition)
        return result

    def __sub__(self, other):
        result = ComparableGraph(super().__sub__(other).store)
        result.partition = self.partition.__sub__(other.partition)
        return result

    def __or__(self, other):
        return self.__add__(other)

    def __and__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        result = ComparableGraph(super().__mul__(other).store)
        result.partition = self.partition.__and__(other.partition)
        return result

    def __xor__(self, other):
        result = ComparableGraph(super().__xor__(other).store)
        result.partition = self.partition.__xor__(other.partition)
        return result

    def __hash__(self):
        return super(ComparableGraph, self).__hash__()

    def recalculatePartition(self):
        slicer = atomic_graph.AtomicGraphFactory(self)
        self._partition = set()
        hashList = []
        for atomicGraph in slicer:
            self._partition.add(atomicGraph)
            hashList.append(atomicGraph.__hash__().to_bytes(16, 'big'))
        hashList.sort()
        # this hash should not be returned by __hash__ since it can change
        self._hash = self.combine_ordered(hashList)

    @property
    def partition(self):
        if self._partition is None:
            self.recalculatePartition()
        return self._partition

    @partition.setter
    def partition(self, partition):
        self._partition = partition

    @property
    def hash(self):
        if self._hash is None:
            self.recalculatePartition()
        return self._hash

    def invalidate(self):
        self._partition = None
        self._hash = None

    def __eq__(self, other):
        if(issubclass(other.__class__, ComparableGraph)):
            return self.hash == other.hash
        if(isinstance(other, rdflib.Graph)):
            return super().__eq__(other)
        if(issubclass(other.__class__, rdflib.Graph)):
            return self == ComparableGraph(store=other.store,
                                           identifier=other.identifier,
                                           namespace_manager=other.namespace_manager)
        return False

    def add(self, triple):
        super().add(triple)
        self.invalidate()

    def addN(self, triples):
        super().addN(triples)
        self.invalidate()

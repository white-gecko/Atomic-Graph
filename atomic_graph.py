import rdflib
from rdflib.compare import to_isomorphic


class GraphSlicer:
    def __init__(self, graph):
        self.graph = rdflib.Graph()
        # make a copy of the graph so the original does not get consumed
        self.graph = self.graph + graph
        self.atomicGraphs = set()
        self.currentAtomicGraph = AtomicGraph()
        self.nextNodeOther = []
        self.nextNodeBlank = []
        self.nextNodeCurrent = []
        self.comparator = AtomicSetComparator(self)

    def __eq__(self, slicer):
        if(not self.comparator):
            self.comparator = AtomicSetComparator(self)
        return self.comparator.compare(slicer)

    def _is_atomic(self, rdfsubject, rdfobject):
        if not (isinstance(rdfsubject, rdflib.BNode) or isinstance(rdfobject, rdflib.BNode)):
            return True
        return False

    def _blank_node_adding(self, node):
        if(isinstance(node, rdflib.BNode)):
            self.nextNodeCurrent.append(node)
        else:
            self.nextNodeOther.append(node)

    def _atomic(self, statement, newNode):
        if(not isinstance(statement[newNode], rdflib.BNode)):
            newAtomicGraph = AtomicGraph()
            newAtomicGraph.add(statement)
            self.atomicGraphs.add(newAtomicGraph)
            self.graph.remove(statement)
            self.nextNodeOther.append(statement[newNode])
        else:
            self.nextNodeBlank.append(statement[newNode])

    def _analyse_node(self, node):
        if(isinstance(node, rdflib.BNode)):
            for tupel in iter(self.graph.predicate_objects(node)):
                self.currentAtomicGraph.add((node, tupel[0], tupel[1]))
                self.graph.remove((node, tupel[0], tupel[1]))
                self._blank_node_adding(tupel[1])
            for tupel in iter(self.graph.subject_predicates(node)):
                self.currentAtomicGraph.add((tupel[0], tupel[1], node))
                self.graph.remove((tupel[0], tupel[1], node))
                self._blank_node_adding(tupel[0])
        else:
            for tupel in iter(self.graph.predicate_objects(node)):
                self._atomic((node, tupel[0], tupel[1]), 2)

            for tupel in iter(self.graph.subject_predicates(node)):
                self._atomic((tupel[0], tupel[1], node), 0)

    def _next_node(self):
        if(self.nextNodeCurrent):
            return self.nextNodeCurrent.pop()
        # if no further nodes are found the current atomic graph is done
        if(self.currentAtomicGraph):
            self.atomicGraphs.add(self.currentAtomicGraph)
            self.currentAtomicGraph = AtomicGraph()
        if(self.nextNodeBlank):
            return self.nextNodeBlank.pop()
        if(self.nextNodeOther):
            return self.nextNodeOther.pop()
        return False

    def run(self):
        node = next(iter(self.graph.all_nodes()), False)
        while(node):
            self._analyse_node(node)
            node = self._next_node()
            while(node):  # empty lists are falsy
                self._analyse_node(node)
                node = self._next_node()
            # in case the graph has disconnected parts
            node = next(iter(self.graph.all_nodes()), False)

    def getAtomicGraphs(self):
        return self.atomicGraphs

    def getNumberOfAtomicGraphs(self):
        return len(self.atomicGraphs)


class AtomicSetComparator:
    def __init__(self, slicer):
        self.sortedGraphList = self._sort_atomic_list(slicer.getAtomicGraphs())
        self.matchNumber = slicer.getNumberOfAtomicGraphs()

    def __bool__(self):
        if self.sortedGraphList:
            return True
        else:
            return False

    # https://wiki.python.org/moin/TimeComplexity lists list sorting as
    # O(n log n)
    def _sort_atomic_list(self, atomicList):
        sortList = list(atomicList)
        sortList.sort(key=lambda atomic: (atomic.get_meta()[0],
                                          atomic.get_meta()[1]),
                      reverse=True)
        return sortList

    def _in_atomic_list(self, element, i, sortedAtomicGraphs, maxIndex):
        index = i
        for index in range(i, maxIndex):
            current = sortedAtomicGraphs[index]
            # early returns
            if(current < element):
                return False
            if(element == current):
                return True
        return False

    def compare(self, other_slicer):
        if(self.matchNumber == other_slicer.getNumberOfAtomicGraphs()):
            index = 0
            otherGraphList = self._sort_atomic_list(other_slicer.
                                                    getAtomicGraphs())
            for i in range(0, self.matchNumber):
                # TODO  use index to cull the beginnig of otherGraphArray
                if(not self._in_atomic_list(self.sortedGraphList[i], index,
                                            otherGraphList, self.matchNumber)):
                    return False
            # TODO this kind of comparison is only injective not bijective
            return True
        return False


class AtomicGraph(rdflib.Graph):
    numberOfBNodes = 0
    maxNumbersNeighbors = 0

    def __eq__(self, graph):
        if(not issubclass(graph.__class__, AtomicGraph)):
            return False
        result = False
        if(self.compare_meta(graph.get_meta())):
            # TODO this is only a place holder
            # the point was to use a better version of comparision then
            # standard rdflib isomorphism
            iso1 = to_isomorphic(self)
            iso2 = to_isomorphic(graph)
            result = iso1 == iso2
        return result

    def __hash__(self):
        return super(AtomicGraph, self).__hash__()

    def __ge__(self, graph):
        other_meta = graph.get_meta()
        if(self.numberOfBNodes > other_meta[0] or (
            self.numberOfBNodes == other_meta[0] and (
                self.maxNumbersNeighbors >= other_meta[1]))):
            return True
        return False

    def __lt__(self, graph):
        other_meta = graph.get_meta()
        if(self.numberOfBNodes < other_meta[0] or (
            self.numberOfBNodes == other_meta[0] and (
                self.maxNumbersNeighbors < other_meta[1]))):
            return True
        return False

    def __str__(self):
        result = ""
        for subj, pred, obj in self:
            result += "{0} {1} {2}.\n".format(subj, pred, obj)
        return result

    def compare_meta(self, metaArray):
        return ((self.numberOfBNodes == metaArray[0]) and(
            self.maxNumbersNeighbors == metaArray[1]))

    def get_meta(self):
        return [self.numberOfBNodes, self.maxNumbersNeighbors]

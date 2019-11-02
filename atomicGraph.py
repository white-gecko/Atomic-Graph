import rdflib
from rdflib.compare import to_isomorphic


class GraphSlicer:
    def __init__(self, graph):
        self.graph = graph
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

    def isAtomic(self, rdfsubject, rdfobject):
        if not (isinstance(rdfsubject, rdflib.BNode)
                or isinstance(rdfobject, rdflib.BNode)):
            return True
        return False

    def blankNodeAdding(self, node):
        if(isinstance(node, rdflib.BNode)):
            self.nextNodeCurrent.append(node)
        else:
            self.nextNodeOther.append(node)

    def atomic(self, statement, newNode):
        if(not isinstance(statement[newNode], rdflib.BNode)):
            newAtomicGraph = AtomicGraph()
            newAtomicGraph.add(statement)
            self.atomicGraphs.add(newAtomicGraph)
            self.graph.remove(statement)
            self.nextNodeOther.append(statement[newNode])
        else:
            self.nextNodeBlank.append(statement[newNode])

    def analyseNode(self, node):
        if(isinstance(node, rdflib.BNode)):
            for tupel in iter(self.graph.predicate_objects(node)):
                self.currentAtomicGraph.add((node, tupel[0], tupel[1]))
                self.graph.remove((node, tupel[0], tupel[1]))
                self.blankNodeAdding(tupel[1])
            for tupel in iter(self.graph.subject_predicates(node)):
                self.currentAtomicGraph.add((tupel[0], tupel[1], node))
                self.graph.remove((tupel[0], tupel[1], node))
                self.blankNodeAdding(tupel[0])
        else:
            for tupel in iter(self.graph.predicate_objects(node)):
                self.atomic((node, tupel[0], tupel[1]), 2)

            for tupel in iter(self.graph.subject_predicates(node)):
                self.atomic((tupel[0], tupel[1], node), 0)

    def nextNode(self):
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
            self.analyseNode(node)
            node = self.nextNode()
            while(node):  # empty lists are falsy
                self.analyseNode(node)
                node = self.nextNode()
            # in case the graph has disconnected parts
            node = next(iter(self.graph.all_nodes()), False)

    def getAtomicGraphs(self):
        return self.atomicGraphs

    def getNumberOfAtomicGraphs(self):
        return len(self.atomicGraphs)


class AtomicSetComparator:
    def __init__(self, slicer):
        self.sortedGraphList = self.sortAtomicList(slicer.getAtomicGraphs())
        self.matchNumber = slicer.getNumberOfAtomicGraphs()

    def __bool__(self):
        if self.sortedGraphList:
            return True
        else:
            return False

    # https://wiki.python.org/moin/TimeComplexity lists list sorting as
    # O(n log n)
    def sortAtomicList(self, atomicList):
        sortList = list(atomicList)
        sortList.sort(key=lambda atomic: (atomic.getMeta()[0],
                                          atomic.getMeta()[1]),
                      reverse=True)
        return sortList

    def compare(self, other_slicer):
        if(self.matchNumber == other_slicer.getNumberOfAtomicGraphs()):
            index = 0
            otherGraphList = self.sortAtomicList(other_slicer.
                                                 getAtomicGraphs())
            for i in range(0, self.matchNumber):
                # TODO  use index to cull the beginnig of otherGraphArray
                if(not self.inAtomicList(self.sortedGraphList[i], index,
                                         otherGraphList, self.matchNumber)):
                    return False
            # TODO this kind of comparison is only injective not bijective
            return True
        return False

    def inAtomicList(self, element, i, sortedAtomicGraphs, maxIndex):
        index = i
        for index in range(i, maxIndex):
            current = sortedAtomicGraphs[index]
            # early returns
            if(current < element):
                return False
            if(element == current):
                return True
        return False


class AtomicGraph(rdflib.Graph):
    numberOfBNodes = 0
    maxNumbersNeighbors = 0

    def __eq__(self, graph):

        if(not issubclass(graph.__class__, AtomicGraph)):
            return False
        result = False
        if(self.compareMeta(graph.getMeta())):
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
        other_meta = graph.getMeta()
        if(self.numberOfBNodes > other_meta[0] or (
            self.numberOfBNodes == other_meta[0] and (
                self.maxNumbersNeighbors >= other_meta[1]))):
            return True
        return False

    def __lt__(self, graph):
        other_meta = graph.getMeta()
        if(self.numberOfBNodes < other_meta[0] or (
            self.numberOfBNodes == other_meta[0] and (
                self.maxNumbersNeighbors < other_meta[1]))):
            return True
        return False

    def compareMeta(self, metaArray):
        return ((self.numberOfBNodes == metaArray[0]) and(
            self.maxNumbersNeighbors == metaArray[1]))

    def getMeta(self):
        return [self.numberOfBNodes, self.maxNumbersNeighbors]

    def __str__(self):
        result = ""
        for subj, pred, obj in self:
            result += "{0} {1} {2}.\n".format(subj, pred, obj)
        return result

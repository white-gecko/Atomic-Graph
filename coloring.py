import rdflib


# check http://aidanhogan.com/docs/skolems_blank_nodes_www.pdf
# for more information
class IsomorphicPartitioner:
    class __HashTupel:
        def hashT(self, colour1, colour2):
            return colour1 + colour2

    class __HashBag:
        def hashB(self, colour1, colour2):
            array = colour1.split("|") + colour2.split("|")
            array.sort()     # the operation become commutative and associative
            return "|".join(array)

    class __ColourPartion(set):
        def __init__(self, clr):
            self.clr = clr

        def setColourMap(self, clr):
            self.clr = clr

        def getColour(self):
            if len(self) == 0:
                return None
            return self.clr[next(iter(self))]

        def __lt__(self, partition):
            if(len(self) < len(partition)):
                return True
            if(len(self) == len(partition)
               and self.getColour() < partition.getColour()
               ):
                return True
            return False

    class __PartiallyOrderedGraph:
        def __init__(self, graph, clr, blanknodes):
            self.graph = graph
            self.clr = clr
            self.blanknodes = blanknodes

        def __lt__(self, other):
            for bnode in iter(self.blanknodes):
                smallerThenAll = True
                for oBNode in iter(other.blanknodes):
                    if(other.clr[oBNode] < self.clr[bnode]):
                        smallerThenAll = False
                if smallerThenAll:
                    return True
            return False

    def canonicalise(self, graph):
        clr = self.colour(graph)
        blanknodes = self.__extractBlanknodes(graph)
        partitions = self.__createPartitions(clr, blanknodes)
        # not part of the offical algorithm, but we need it as marker generator
        self.markerNr = -1
        self.hashTupel = IsomorphicPartitioner().__HashTupel()
        return self.__distinguish(graph, clr, partitions, blanknodes)

    def colour(self, graph, colour=None):
        if colour is None:
            colour = {}
            for node in iter(graph.all_nodes()):
                if isinstance(node, rdflib.BNode):
                    colour[node] = "[]"
                else:
                    colour[node] = node.n3()
            # all terms need colour codes
            for predicate in graph.predicates():
                colour[predicate] = predicate.n3()

        colourPrevious = {}  # init so while condition does not fail
        hashTupel = IsomorphicPartitioner().__HashTupel()
        hashBag = IsomorphicPartitioner().__HashBag()
        equalityRelation = False
        while(not equalityRelation):
            colourPrevious = colour
            colour = colourPrevious.copy()
            for subj, pred, obje in graph:
                if(isinstance(subj, rdflib.BNode)):
                    c = hashTupel.hashT(colourPrevious[pred],
                                        colourPrevious[obje])
                    colour[subj] = hashBag.hashB(c, colour[subj])
                elif(isinstance(obje, rdflib.BNode)):
                    c = hashTupel.hashT(colourPrevious[subj],
                                        colourPrevious[pred])
                    colour[obje] = hashBag.hashB(c, colour[obje])
            equalityRelation = self.__checkEqualityRelation(colourPrevious,
                                                            colour)
        return colour

    # group nodes by their colour
    # two graphs share the same colour group -> they are isomorph
    def groupByColour(self, graph, clr):
        colourGroup = {}
        for node in iter(graph.all_nodes()):
            if not clr[node] in colourGroup:
                colourGroup[clr[node]] = set()
            colourGroup[clr[node]].add(node)
        return colourGroup

    def __distinguish(self, graph, clr,
                      partitions, blanknodes, lowestGraph=None):
        sPart = self.__lowestNonTrivialPartition(partitions)
        for bnode in sPart:
            # should clr itself be changed or just a copy?
            clr[bnode] = self.hashTupel.hashT(clr[bnode],
                                              self.__generateMarker())
            clrExt = self.colour(graph, clr)
            bPart = self.__refine(partitions, clrExt, bnode, blanknodes)
            if(len(bPart) == len(blanknodes)):
                graph_c = (IsomorphicPartitioner().
                           __PartiallyOrderedGraph(graph, clr, blanknodes))
                if lowestGraph is None or graph_c < lowestGraph:
                    lowestGraph = graph_c
            else:
                lowestGraph = self.__distinguish(graph, clrExt,
                                                 bPart, blanknodes,
                                                 lowestGraph)
        return lowestGraph

    def __refine(self, partitions, clr, bnode, blanknodes):
        # find partition containing bnode
        i = 0
        while(not (bnode in partitions[i])):
            i += 1
        refinedPartition = []
        # init refinedPartition
        k = 0
        while(k < i):
            refinedPartition.append(partitions[k])
            k += 1
        # create Partition containing only the bnode
        singleton = set()
        singleton.add(bnode)
        refinedPartition.append(singleton)
        # init refinedPartition end
        newPartitioning = self.__createPartitions(clr, blanknodes)
        # init (B_i \ {b}, B_{i+1}, ... , B_n)
        iterategroup = []
        iterategroup.append(partitions[i].copy())
        iterategroup[0].remove(bnode)
        i += 1
        while(i < len(partitions)):
            iterategroup.append(partitions[i])
            i += 1
        # init (B_i \ {b}, B_{i+1}, ... , B_n) end
        for partition in iter(iterategroup):
            partitionPlus = []
            for newPartition in iter(newPartitioning):
                if len(partition & newPartition) > 0:
                    partitionPlus += (partition & newPartition)
            refinedPartition += partitionPlus
        return refinedPartition

    def __checkEqualityRelation(self, colourPrevious, colourNext):
        for key1 in colourNext:
            for key2 in colourNext:

                # A<->B = A->B and B->A = -A or B and -B or A
                if not ((colourPrevious[key1] != colourPrevious[key2]
                         or colourNext[key1] == colourNext[key2])
                        and (colourNext[key1] != colourNext[key2]
                             or colourPrevious[key1] == colourPrevious[key2])
                        ):
                    return False
        return True

    def __extractBlanknodes(self, graph):
        blanknodes = set()
        for node in iter(graph.all_nodes()):
            if isinstance(node, rdflib.BNode):
                blanknodes.add(node)
        return blanknodes

    def __createPartitions(self, clr, blanknodes):
        orderedPartitions = []
        for bnode in blanknodes:
            matchColour = clr[bnode]
            foundPartition = None
            for partition in orderedPartitions:
                if(matchColour == partition.getColour()):
                    foundPartition = partition
            if foundPartition is None:
                foundPartition = IsomorphicPartitioner().__ColourPartion(clr)
                orderedPartitions.append(foundPartition)
            foundPartition.add(bnode)

        return sorted(orderedPartitions)

    def __lowestNonTrivialPartition(self, partitions):
        for partition in partitions:
            if(len(partition) > 1):
                return partition
        # return an empty set if nothing was found
        # this causes the loop in __distinguish to stop
        return set()

    def __generateMarker(self):
        return "[@]"

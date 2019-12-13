import rdflib
import hashlib
from sortedcontainers import SortedList
from collections import defaultdict
from atomicgraphs.hash_combiner import HashCombiner


# check http://aidanhogan.com/docs/skolems_blank_nodes_www.pdf
# for more information
class IsomorphicPartitioner:
    def __init__(self):
        self.__hash_type = hashlib.md5
        self.__blank_hash = self.__hash_type("[]".encode('utf-8')).digest()
        self.__marker_hash = self.__hash_type("[@]".encode('utf-8')).digest()
        self.__hashBag = IsomorphicPartitioner.__HashBag()
        self.__hashTupel = IsomorphicPartitioner.__HashTupel()
        self.__genericHashCombiner = HashCombiner()

    def _colour(self, graph, colour=None):
        if colour is None:
            colour = self._init_colour(graph)
        colourPrevious = colour.copy()  # init so while condition does not fail
        equalityRelation = False
        changeHashCache = set()
        while(not equalityRelation):
            colourPrevious = colour
            colour = colourPrevious.copy()
            for subj, pred, obje in graph:
                if(isinstance(subj, rdflib.BNode)):
                    c = self.__hashTupel.hash(colourPrevious[pred],
                                              colourPrevious[obje])
                    self.__hashBag.add(subj, c)
                elif(isinstance(obje, rdflib.BNode)):
                    c = self.__hashTupel.hash(colourPrevious[subj],
                                              colourPrevious[pred])
                    self.__hashBag.add(obje, c)
            self.__hashBag.trigger_hashing(colour)
            currentChangeHash = self._create_colour_grouping_hash(colour)
            equalityRelation = currentChangeHash in changeHashCache
            changeHashCache.add(currentChangeHash)
        return colour

    def _init_colour(self, graph):
        colour = {}
        for node in iter(graph.all_nodes()):
            if isinstance(node, rdflib.BNode):
                self.__hashBag.init_node(node)
                colour[node] = self.__blank_hash
            else:
                colour[node] = self.__hash_type(node.n3()
                                                .encode('utf-8')).digest()
        # all terms need colour codes
        for predicate in graph.predicates():
            colour[predicate] = self.__hash_type(predicate.n3()
                                                 .encode('utf-8')).digest()
        return colour

    def _canonicalise(self, graph):
        clr = self._colour(graph)
        blanknodes = self._extract_blanknodes(graph)
        partitions = self._create_partitions(clr, blanknodes)
        result = self._distinguish(graph, clr, partitions, blanknodes)
        return result

    def _group_by_colour(self, nodes, clr):
        colourGroup = {}
        for node in iter(nodes):
            if clr[node] not in colourGroup:
                colourGroup[clr[node]] = set()
            colourGroup[clr[node]].add(node)
        return colourGroup

    def _distinguish(self, graph, clr,
                     partitions, blanknodes, lowestGraph=None):
        sPart = self._lowest_non_trivial_partition(partitions)
        for bnode in sPart:
            # should clr itself be changed or just a copy?
            clr[bnode] = self.__hashTupel.hash(clr[bnode],
                                               self._generate_marker())
            clrExt = self._colour(graph, clr)
            bPart = self._refine(partitions, clrExt, bnode, blanknodes)
            if(len(bPart) == len(blanknodes)):
                graph_c = (IsomorphicPartitioner().
                           __PartiallyOrderedGraph(graph, clr, blanknodes))
                if lowestGraph is None or graph_c < lowestGraph:
                    lowestGraph = graph_c
            else:
                lowestGraph = self._distinguish(graph, clrExt,
                                                bPart, blanknodes,
                                                lowestGraph)
        if(lowestGraph is None):
            return (IsomorphicPartitioner().
                    __PartiallyOrderedGraph(graph, clr, blanknodes))
        return lowestGraph

    def _refine(self, partitions, clr, bnode, blanknodes):
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
        newPartitioning = self._create_partitions(clr, blanknodes)
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
            partitionPlus = IsomorphicPartitioner.__ColourPartition(self.__hash_type().digest())
            for newPartition in iter(newPartitioning):
                if len(partition & newPartition) > 0:
                    partitionPlus.update(partition & newPartition)
            refinedPartition += partitionPlus
        return refinedPartition

    def _create_colour_grouping_hash(self, blankToColour):
        colourGroups = self._group_by_colour(blankToColour.keys(),
                                             blankToColour)
        hashList = SortedList()
        for colour in sorted(colourGroups):
            # the reinit is important -> don't use self.__hash_type
            currentHash = hashlib.md5()
            for blankNode in sorted(colourGroups[colour]):
                currentHash.update(blankNode.encode('utf-8'))
            hashList.add(currentHash.digest())
        return self.__genericHashCombiner.combine_ordered(hashList)

    def _extract_blanknodes(self, graph):
        blanknodes = set()
        for node in iter(graph.all_nodes()):
            if isinstance(node, rdflib.BNode):
                blanknodes.add(node)
        return blanknodes

    def _create_partitions(self, clr, blanknodes):
        orderedPartitions = ColourPartitionList(clr)
        madePartitions = defaultdict(lambda: False)
        for bnode in blanknodes:
            matchColour = clr[bnode]
            foundPartition = madePartitions[matchColour]
            if not foundPartition:
                foundPartition = IsomorphicPartitioner().__ColourPartition(clr)
                madePartitions[matchColour] = foundPartition
                orderedPartitions.append(foundPartition)
            foundPartition.add(bnode)
        orderedPartitions.sort()
        return orderedPartitions

    def _lowest_non_trivial_partition(self, partitions):
        for partition in partitions:
            if(len(partition) > 1):
                return partition
        # return an empty set if nothing was found
        # this causes the loop in _distinguish to stop
        return set()

    def _generate_marker(self):
        return self.__marker_hash

    def partitionIsomorphic(self, graph):
        lowestGraph = self._canonicalise(graph)
        self.__hashBag.colourCodeLists.clear()
        return self._create_partitions(lowestGraph.clr, lowestGraph.blanknodes)

    def partitionIsomorphicSimple(self, graph):
        colour = self._colour(graph)
        self.__hashBag.colourCodeLists.clear()
        blanknodes = self._extract_blanknodes(graph)
        return self._create_partitions(colour, blanknodes)

    class __HashTupel(HashCombiner):
        def hash(self, colour1, colour2):
            return self.combine_ordered([colour1, colour2])

    class __HashBag(HashCombiner):
        def __init__(self):
            self.colourCodeLists = {}

        def init_node(self, node):
            self.colourCodeLists[node] = []

        def add(self, node, colour):
            self.colourCodeLists[node].append(hashlib.md5(colour).digest())

        def trigger_hashing(self, colour):
            for node, code_array in self.colourCodeLists.items():
                code_array.append(colour[node])
                code_array.sort()
                colour[node] = self.combine_ordered(code_array)
                code_array.clear()

    class __ColourPartition(set):
        def __init__(self, clr):
            self.clr = clr

        def __lt__(self, partition):
            if(len(self) < len(partition)):
                return True
            if(len(self) == len(partition) and self.get_colour() < partition.get_colour()):
                return True
            return False

        def __eq__(self, value):
            return (len(self) == len(value) and self.get_colour() == value.get_colour())

        def __ne__(self, value):
            return not self.__eq__(value)

        def __str__(self):
            return "ColourPartition of {}".format(self.get_colour())

        def __hash__(self):
            return int.from_bytes(self.get_hash_code(), byteorder='big')

        def get_hash_code(self):
            hash = hashlib.md5()
            hash.update(self.get_colour())
            hash.update(len(self).to_bytes(16, 'big'))
            return hash.digest()

        def set_colour_map(self, clr):
            self.clr = clr

        def get_colour(self):
            if len(self) == 0:
                return None
            return self.clr[next(iter(self))]

    class __PartiallyOrderedGraph:
        def __init__(self, graph, clr, blanknodes):
            self.graph = graph
            self.clr = clr
            self.blanknodes = blanknodes

        def __lt__(self, other):
            if self.blanknodes.issubset(other.blanknodes):
                return True
            # this is niche case that prevents the return of a falsy True
            if other.blanknodes.issubset(self.blanknodes):
                return False
            # if e.g. the lowest colour belongs to all graphs
            # the following will always return true
            # --> its not a total ordering
            skipList = set(self.clr.values()).intersection(set(other.clr.values()))
            for bnode in iter(self.blanknodes):
                smallerThenAll = True
                if(self.clr[bnode] in skipList):
                    continue
                for oBNode in iter(other.blanknodes):
                    if(other.clr[oBNode] in skipList):
                        continue
                    if(other.clr[oBNode] < self.clr[bnode]):
                        smallerThenAll = False
                if smallerThenAll:

                    return True
            return False


class ColourPartitionList(list, HashCombiner):
    def __init__(self, colourMap):
        self._unhashed = True
        self._colourMap = colourMap

    def __getitem__(self, key):
        if issubclass(key.__class__, int):
            return super(ColourPartitionList, self).__getitem__(key)
        return self._colourMap[key]

    def __eq__(self, value):
        return self.__hash__() == value.__hash__()

    def __ne__(self, value):
        return not self.__eq__(value)

    def __str__(self):
        template = "ColourPartitionList: {}"
        return template.format(",  ".join(s.__str__() + ": " + str(len(s)) for s in self))

    def __hash__(self):
        return int.from_bytes(self.get_hash_code(), byteorder='big')

    def get_hash_code(self):
        if self._unhashed:
            # no need to order, its supposed to be already ordered when created
            sortedHashes = []
            for colourPartition in self:
                sortedHashes.append(colourPartition.get_hash_code())
            self.hash = self.combine_ordered(sortedHashes)
            self._unhashed = False
        return self.hash

import rdflib


class GraphIsoPartitioner:
    class HashTupel:
        def hashT(self, colour1, colour2):
            return colour1 + colour2

    class HashBag:
        def hashB(self, colour1, colour2):
            array = colour1.split("|") + colour2.split("|")
            array.sort()     # the operation become commutative and associative
            return "|".join(array)

    def colour(self, graph):
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
        hashTupel = GraphIsoPartitioner.HashTupel()
        hashBag = GraphIsoPartitioner.HashBag()
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
            equalityRelation = self.checkEqualityRelation(colourPrevious,
                                                          colour)
        return colour

    def checkEqualityRelation(self, colourPrevious, colourNext):
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

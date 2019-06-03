import rdflib


class GraphIsoPartitioner:
    class ColourHash:
        def __init__(self):
            self.hash = {}

    class HashTupel(ColourHash):
        def hash(colour1, colour2):
            return colour1 + colour2

    class HashBag(ColourHash):
        def hash(colour1, colour2):
            array = colour1.split("|") + colour2.split("|")
            array.sort()     # the operation become commutative and associative
            return "|".join(array)

    def colour(self, graph):
        colour = {}
        graph = rdflib.Graph()
        for node in iter(graph.all_nodes()):
            if isinstance(node, rdflib.BNode):
                colour[node] = ""
            else:
                colour[node] = node.n3()

        colourPrevious = {}  # init so while condition does not fail
        hashTupel = GraphIsoPartitioner.HashTupel()
        hashBag = GraphIsoPartitioner.HashBag()
        while(not self.checkEqualityRelation(colourPrevious, colour)):
            colourPrevious = colour
            colour = colourPrevious.copy()
            for statement in graph.triples():
                if(isinstance(statement[0], rdflib.BNode)):
                    c = hashTupel.hash(colourPrevious[statement[1]],
                                       colourPrevious[statement[2]])
                    colour[statement[0]] = hashBag.hash(c,
                                                        colour[statement[0]])
                elif(isinstance(statement[2], rdflib.BNode)):
                    c = hashTupel.hash(colourPrevious[statement[0]],
                                       colourPrevious[statement[1]])
                    colour[statement[2]] = hashBag.hash(c,
                                                        colour[statement[2]])
        return colour

    def checkEqualityRelation(self, colourPrevious, colourNext):
        for key in colourPrevious:
            if(colourPrevious[key] != colourNext[key]):
                return False
        return True

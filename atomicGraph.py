import rdflib

class GraphSlicer:
    def __init__(self, graph):
        self.graph = graph
        self.atomicGraphs = set()
        self.currentAtomicGraph = rdflib.Graph()
        self.nextNodeOther = []
        self.nextNodeBlank = []
        self.nextNodeCurrent = []

    def blankNodeAdding(self, node):
        if(node.n3()[:2] == "_:"):
            self.nextNodeCurrent.append(node)
        else:
            self.nextNodeOther.append(node)

    def atomic(self, statement, newNode):
        if(statement[newNode].n3()[:2] != "_:"):
            newAtomicGraph = rdflib.Graph()
            newAtomicGraph.add(statement)
            self.atomicGraphs.add(newAtomicGraph)
            self.graph.remove(statement)
            self.nextNodeOther.append(statement[newNode])
        else:
            self.nextNodeBlank.append(statement[newNode])

    def analyseNode(self, node):
        if(node.n3()[:2] == "_:"):
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
            self.currentAtomicGraph = rdflib.Graph()
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

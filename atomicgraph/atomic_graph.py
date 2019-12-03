import rdflib
from atomicgraph import coloring

import traceback

class AtomicGraphFactory:
    def __init__(self, graph):
        self.graph = rdflib.Graph()
        # make a copy of the graph so the original does not get consumed
        self.graph = self.graph + graph
        self.atomicGraphs = set()
        self.currentAtomicGraph = rdflib.Graph()
        self.nextNodeOther = []
        self.nextNodeBlank = []
        self.nextNodeCurrent = []
        self.iter = None

    def __iter__(self):
        if self.iter is None:
            self._run()
            self.iter = iter(self.atomicGraphs)
        return self

    def __next__(self):
        graph = next(self.iter)
        if graph:
            partitioner = coloring.IsomorphicPartitioner()
            cid = graph.store.__obj2id(graph)
            oldHash = graph.__hash__()
            graph.finalize()
            newHash = graph.__hash__()
            graph.store.__obj2int[oldHash] #delete
            if newHash in graph.store.__obj2int:
                # collision
                graph.store.__removeTripleContext(cid)
            else:
                graph.store.__obj2int[newHash] = cid
            # aGraph = AtomicGraph(store=graph.store, identifier=graph.identifier,
                                 # namespace_manager=graph.namespace_manager)
            graph.colourPartitions = partitioner.partitionIsomorphic(graph)
            # manual copying is necessary since overwritng atomicgraph.__hash__
            #   would otherwise causing us to lose graphs triples
            # even given the same store, a graph needs its hash to find its triples
            return graph
        else:
            raise StopIteration

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
            newAtomicGraph = rdflib.Graph()
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
            self.currentAtomicGraph = rdflib.Graph()
        if(self.nextNodeBlank):
            return self.nextNodeBlank.pop()
        if(self.nextNodeOther):
            return self.nextNodeOther.pop()
        return False

    def _run(self):
        node = next(iter(self.graph.all_nodes()), False)
        while(node):
            self._analyse_node(node)
            node = self._next_node()
            while(node):  # empty lists are falsy
                self._analyse_node(node)
                node = self._next_node()
            # in case the graph has disconnected parts
            node = next(iter(self.graph.all_nodes()), False)


class AtomicGraph(rdflib.Graph):
    self.final = False

    def finalize(self):
        self.final = True

    def __eq__(self, other):
        if isinstance(other, AtomicGraph):
            return self.__hash__() == other.__hash__()
        elif isinstance(other, rdflib.Graph):
            return self.identifier == other.identifier
        return False

    def __hash__(self):
        if self.final:
            traceback.print_stack()
            return self.colourPartitions.__hash__()
        else:
            super().__hash__()

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __le__(self, other):
        return hash(self) <= hash(other)

    def __str__(self):
        result = ""
        for subj, pred, obj in self:
            result += "{0} {1} {2}.\n".format(self.colourPartitions[subj],
                                              self.colourPartitions[pred],
                                              self.colourPartitions[obj])
        return result

    def __repr__(self):
        return "AtomicHashGraph(#IsoPartitions: {})".format(len(self.colourPartitions))

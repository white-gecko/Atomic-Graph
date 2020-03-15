import rdflib
from atomicgraphs.coloring import IsomorphicPartitioner


class AtomicGraphFactory:
    def __init__(self, graph, nodeList=None):
        if(issubclass(graph.__class__, rdflib.ConjunctiveGraph)):
            self.graph = rdflib.ConjunctiveGraph('AtomicStore')
            for quad in graph.quads():
                self.graph.add((quad[0], quad[1], quad[2], quad[3].identifier))
            self.contexts = list(self.graph.contexts())
        else:
            self.graph = rdflib.Graph('AtomicStore')
            self.graph += graph
            self.contexts = [self.graph]  # graph and self.graph are not the same context
        # make a copy of the graph so the original does not get consumed
        self.atomicGraphs = set()
        self.currentAtomicGraph = rdflib.Graph(store=self.graph.store)
        self.currentAtomicGraph.store.addNewContext(self.currentAtomicGraph)
        self.nextNodeOther = []
        self.nextNodeBlank = []
        self.nextNodeCurrent = []
        self.iter = None
        if(nodeList is None):
            def provideNewNodeFromGraph():
                return next(iter(self.currentContext.all_nodes()), False)
            self.provideNode = provideNewNodeFromGraph
            self.convertEntireGraph = True
        else:
            if(not issubclass(nodeList.__class__, list().__class__)):
                nodeList = list(nodeList)

            def provideNewNodeFromList():
                if(len(nodeList) > 0):
                    return nodeList.pop()
                else:
                    return False
            self.provideNode = provideNewNodeFromList
            self.convertEntireGraph = False

    def __iter__(self):
        if self.iter is None:
            self._run()
            self.iter = iter(self.atomicGraphs)
        return self

    def __next__(self):
        graph = next(self.iter)
        if graph:
            partitioner = IsomorphicPartitioner()
            aGraph = AtomicGraph(store=graph.store, identifier=graph.identifier,
                                 namespace_manager=graph.namespace_manager)
            aGraph.colourPartitions = partitioner.partitionIsomorphic(graph)
            return aGraph
        else:
            raise StopIteration

    def _blank_node_adding(self, node):
        if(isinstance(node, rdflib.BNode)):
            self.nextNodeCurrent.append(node)
        else:
            self.nextNodeOther.append(node)

    def _atomic(self, statement, newNode):
        if(not isinstance(statement[newNode], rdflib.BNode)):
            newAtomicGraph = rdflib.Graph(store=self.graph.store)
            self.graph.store.moveStatement(statement,
                                           source=self.currentContext,
                                           destination=newAtomicGraph)
            self.atomicGraphs.add(newAtomicGraph)
            self.nextNodeOther.append(statement[newNode])
        else:
            self.nextNodeBlank.append(statement[newNode])

    def _analyse_node(self, node):
        if(isinstance(node, rdflib.BNode)):
            for tupel in iter(self.currentContext.store.predicate_objects(node,
                                                                          self.currentContext)):
                self.currentContext.store.moveStatement((node, tupel[0], tupel[1]),
                                                        source=self.currentContext,
                                                        destination=self.currentAtomicGraph)
                self._blank_node_adding(tupel[1])
            for tupel in iter(self.currentContext.store.subject_predicates(node,
                                                                           self.currentContext)):
                self.currentContext.store.moveStatement((tupel[0], tupel[1], node),
                                                        source=self.currentContext,
                                                        destination=self.currentAtomicGraph)
                self._blank_node_adding(tupel[0])
        else:
            for tupel in iter(self.currentContext.store.predicate_objects(node,
                                                                          self.currentContext)):
                self._atomic((node, tupel[0], tupel[1]), 2)
            for tupel in iter(self.currentContext.store.subject_predicates(node,
                                                                           self.currentContext)):
                self._atomic((tupel[0], tupel[1], node), 0)

    def _next_node(self):
        if(self.nextNodeCurrent):
            return self.nextNodeCurrent.pop()
        # if no further nodes are found the current atomic graph is done
        if(self.currentAtomicGraph):
            self.atomicGraphs.add(self.currentAtomicGraph)
            self.currentAtomicGraph = rdflib.Graph(store=self.graph.store)
            self.graph.store.addNewContext(self.currentAtomicGraph)
        if(not self.convertEntireGraph):
            return False
        if(self.nextNodeBlank):
            return self.nextNodeBlank.pop()
        if(self.nextNodeOther):
            return self.nextNodeOther.pop()
        return False

    def _run(self):
        for context in self.contexts:
            self.currentContext = context
            node = self.provideNode()
            while(node):
                self._analyse_node(node)
                node = self._next_node()
                while(node):  # empty lists are falsy
                    self._analyse_node(node)
                    node = self._next_node()
                # in case the graph has disconnected parts
                node = self.provideNode()


class AtomicGraph(rdflib.Graph):
    def __init__(self, store='default', identifier=None, namespace_manager=None):
        super().__init__(store, identifier, namespace_manager)
        self._hashOn = False

    def __eq__(self, value):
        if isinstance(value, AtomicGraph):
            return self.__hash__() == value.__hash__()
        else:
            return super().__eq__(value)

    def __hash__(self):
        if(self._hashOn):
            return self.colourPartitions.__hash__()
        else:
            return super().__hash__()

    def __str__(self):
        result = ""
        for subj, pred, obj in self:
            result += "{0} {1} {2}.\n".format(self.colourPartitions[subj],
                                              self.colourPartitions[pred],
                                              self.colourPartitions[obj])
        return result

    def __repr__(self):
        return "AtomicHashGraph(#IsoPartitions: {})".format(len(self.colourPartitions))

    def switchOnHash(self):
        self._hashOn = True

    @property
    def colourPartitions(self):
        return self._colourPartitions

    @colourPartitions.setter
    def colourPartitions(self, partition):
        self._colourPartitions = partition
        self.store.switchID(self)

from rdflib.plugins import memory


class AtomicStore(memory.IOMemory):
    """The AtomicStore is based on the IOMemory store and implements special methods for the
    AtomicGraph handling.

    It deals with the context -> triple and triples -> context mappings and the obj2int and int2obj
    data structures.
    """
    def switchID(self, graph):
        id = self._IOMemory__obj2int[graph]
        del self._IOMemory__obj2int[graph]
        # The switchOnHash method changes the way __hash__() is implemented
        # So we just rewrite the _IOMemory__obj2int and _IOMemory__int2obj structures
        graph.switchOnHash()
        self._IOMemory__obj2int[graph] = id
        self._IOMemory__int2obj[id] = graph

    def moveStatement(self, triple, source, destination):
        """This method moves a statement within the store between contexts.

        Keyword arguments:
        triple -- the statement to move
        source -- the object of the source context
        destination -- the object of the destination context
        """
        enctriple = self._IOMemory__encodeTriple(triple)
        self._IOMemory__all_contexts.add(destination)
        self._IOMemory__addTripleContext(enctriple, destination, False)
        cid = self._IOMemory__obj2id(source)
        self._IOMemory__removeTripleContext(enctriple, cid)
        if(len(self._IOMemory__contextTriples[cid]) == 0):
            del self._IOMemory__contextTriples[cid]

    def addNewContext(self, context):
        self._IOMemory__all_contexts.add(context)

    def predicate_objects(self, subject, context):
        for (s, p, o), cg in self.triples((subject, None, None), context=context):
            yield (p, o)

    def subject_predicates(self, object, context):
        for (s, p, o), cg in self.triples((None, None, object), context=context):
            yield (s, p)

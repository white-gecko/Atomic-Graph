from rdflib.plugins.stores import memory


class AtomicStore(memory.Memory):
    """The AtomicStore is based on the IOMemory store and implements special methods for the
    AtomicGraph handling.

    It deals with the context -> triple and triples -> context mappings and the obj2int and int2obj
    data structures.
    """

    def switchID(self, graph):
        self._Memory__all_contexts.remove(graph)
        # The switchOnHash method changes the way __hash__() is implemented
        # So we just rewrite the _IOMemory__obj2int and _IOMemory__int2obj structures
        graph.switchOnHash()
        self._Memory__all_contexts.add(graph)

    def moveStatement(self, triple, source, destination):
        """This method moves a statement within the store between contexts.

        Keyword arguments:
        triple -- the statement to move
        source -- the object of the source context
        destination -- the object of the destination context
        """
        self._Memory__all_contexts.add(destination)
        self._Memory__add_triple_context(triple, destination, False)
        ctx = self._Memory__ctx_to_str(source)
        self._Memory__remove_triple_context(triple, ctx)
        if(len(self._Memory__contextTriples[ctx]) == 0):
            del self._Memory__contextTriples[ctx]

    def addNewContext(self, context):
        self._Memory__all_contexts.add(context)

    def predicate_objects(self, subject, context):
        for (s, p, o), cg in self.triples((subject, None, None), context=context):
            yield (p, o)

    def subject_predicates(self, object, context):
        for (s, p, o), cg in self.triples((None, None, object), context=context):
            yield (s, p)

from rdflib.plugins import memory


class AtomicStore(memory.IOMemory):
    def switchID(self, graph):
        id = self._IOMemory__obj2int[graph]
        del self._IOMemory__obj2int[graph]
        # The switchOnHash method changes the way __hash__() is implemented
        # So we just rewrite the _IOMemory__obj2int and _IOMemory__int2obj structures
        graph.switchOnHash()
        self._IOMemory__obj2int[graph] = id
        self._IOMemory__int2obj[id] = graph

    def moveStatement(self, triple, source, destination):
        enctriple = self._IOMemory__encodeTriple(triple)
        self._IOMemory__addTripleContext(enctriple, destination, False)
        cid = self._IOMemory__obj2id(source)
        self._IOMemory__removeTripleContext(enctriple, cid)

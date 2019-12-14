from rdflib.plugins import memory


class AtomicStore(memory.IOMemory):
    def switchID(self, graph):
        id = self._IOMemory__obj2int[graph]
        graph.switchOnHash()
        self._IOMemory__obj2int[graph] = id
        self._IOMemory__int2obj[id] = graph

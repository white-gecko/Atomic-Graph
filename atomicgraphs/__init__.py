import rdflib
from rdflib import store

rdflib.plugin.register('AtomicStore', store.Store, 'atomicgraphs.atomic_store', 'AtomicStore')

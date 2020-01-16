"""
AtomicGraphs
------------
This is a python library to split an RDF Graph into atomic graphs.

With this library using atomic graphs we want to make RDF Graphs containing
blanknodes comparable.
This package implements a colouring algorithm.
"""
from setuptools import setup

setup(
    name='atomicgraphs',
    version='0.1.3',
    description=("This is a library to split an RDF Graph into atomic graphs."),
    long_description=__doc__,
    author='Simaris',
    # author_email='foomail@foo.com',
    packages=['atomicgraphs'],
    install_requires=['rdflib', 'sortedcontainers']
)

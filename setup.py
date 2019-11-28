from setuptools import setup

setup(
    name='atomicgraph',
    version='1.0',
    description=("This package provides a colouring algorithm,"
                 " to make rdf-graphs containing blanknodes comparable."
                 ),
    author='Simaris',
    # author_email='foomail@foo.com',
    packages=['atomicgraph'],
    install_requires=['rdflib', 'sortedcontainers']
)

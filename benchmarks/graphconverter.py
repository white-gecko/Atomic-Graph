import rdflib


def convertGraphToRDF(fileName):
    graphFile = open(fileName, 'r')
    graphFile.readline().split()
    bNodeHash = {}
    graph = rdflib.Graph()
    for line in graphFile:
        tripel = line.split()
        tsubject = "_:" + tripel[1]
        if(tsubject not in bNodeHash):
            bNodeHash[tsubject] = rdflib.BNode()
        tsubject = bNodeHash[tsubject]
        tpredicate = rdflib.URIRef("http://www.rdf.graph.org/edge")
        tobject = "_:" + tripel[2]
        if(tobject not in bNodeHash):
            bNodeHash[tobject] = rdflib.BNode()
        tobject = bNodeHash[tobject]
        graph.add((tsubject, tpredicate, tobject))
    graphFile.close()
    return graph

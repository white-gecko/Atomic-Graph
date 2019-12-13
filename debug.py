from atomicgraphs import comp_graph


graph0 = comp_graph.ComparableGraph()
graph1 = comp_graph.ComparableGraph()
graph0.parse(source="./examples/example1.ttl", format="n3")
graph1.parse(source="./examples/example2.ttl", format="n3")
diffTupel = graph0.diff(graph1)
print("{} {}".format(len(diffTupel[0]), len(diffTupel[1])))
print("--------------------------------------------------")
for aGraph in diffTupel[0]:
    print("-")
    print(aGraph.__repr__())
    for subj, pred, obj in aGraph:
        print("{} {} {}".format(subj, pred, obj))
print("==================================================")
for aGraph in diffTupel[1]:
    print("+")
    print(aGraph.__repr__())
    for subj, pred, obj in aGraph:
        print("{} {} {}".format(subj, pred, obj))
print(graph0 == graph1)

import graph_operation as go

graph_path = "./Graphs/smallRandom.json"


# set up graph
graph, graph_nodes = go.extract_directed_graph(graph_path)
go.transform(graph, graph_nodes)
graph_nodes = [*graph_nodes, "start", "end"]

# set ACO

# blabla bla ACO is collection of Ant_TGE with starting point "start" and objectif "end"

###################################

# Iter on ACO process

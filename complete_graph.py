import itertools
import networkx as nx


def graph_c(graph):
    complete_graph = nx.Graph()
    leaves = graph.nodes
    complete_graph.add_nodes_from(graph.nodes)
    complete_graph.add_edges_from(itertools.combinations(leaves, 2))
    return complete_graph

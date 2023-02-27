import numpy as np
import pandas as pd
import networkx as nx

"""
Transforms the graph so ants can walk on it
"""


def extract_directed_graph(graph_path):
    graph_ds = pd.read_json(graph_path)['nodes']
    graph_nodes = graph_ds.keys()
    graph_edges = []
    graph_data = []
    for node in graph_nodes:
        graph_data.append(graph_ds[node]['Data'])
        for parent in graph_ds[node]['Dependencies']:
            graph_edges.append((parent, node))

    graph = nx.DiGraph()
    graph.add_edges_from(graph_edges)
    graph.add_nodes_from(graph_nodes, process_time=graph_data)
    return graph, graph_nodes


def is_end(graph: nx.DiGraph, node):
    node_successors = []
    for succ in graph.successors(node):
        node_successors.append(succ)
        break

    return node_successors == []


def is_root(graph: nx.DiGraph, node):
    node_successors = []
    for prev in graph.predecessors(node):
        node_successors.append(prev)
        break

    return node_successors == []


def get_root(graph: nx.DiGraph, graph_nodes):
    return [node for node in graph_nodes if is_root(graph, node)]


def get_end(graph: nx.DiGraph, graph_nodes):
    return [node for node in graph_nodes if is_end(graph, node)]


if __name__ == "__main__":

    print("TESTING RANGE")
    print("===============================================")
    graph_path = "./Graphs/smallRandom.json"
    print("getting graph from ", graph_path, " ...")
    graph, graph_nodes = extract_directed_graph(graph_path)

    # works with smallRandom.json only
    # print("The node one is root :", is_root(graph, 1))
    # print("The node ten is end :", is_end(graph, 10))

    print("Roots of our graph are : ", get_root(graph, graph_nodes))
    print("Ends of our graph are :", get_end(graph, graph_nodes))

    print("===============================================")

    print("END")

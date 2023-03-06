import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time

"""
Transforms the graph so ants can walk on it
"""

def convert_to_seconds(ch):
    hh, mm, ss = ch.split(':')
    return 3600*int(hh)+60*int(mm)+float(ss)


<< << << < HEAD
def extract_directed_graph(graph_path):


== == == =


def extract_directed_graph(graph_path: str):


>>>>>> > 4daccf977944c6f9d065fda121a584057949c0d4
graph_ds = pd.read_json(graph_path)['nodes']
graph_nodes = graph_ds.keys()
 graph_edges = []
  graph_data = []
   for node in graph_nodes:
        graph_data.append(convert_to_seconds(graph_ds[node]['Data']))
        for parent in graph_ds[node]['Dependencies']:
            graph_edges.append((parent, node))

    graph = nx.DiGraph()
    graph.add_edges_from(graph_edges)

    for i in range(len(graph_nodes)):
        graph.add_node(graph_nodes[i], process_time=graph_data[i], weight=i)

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


def transform(graph: nx.DiGraph, graph_nodes: list):
    """
    Make a in place transformation of the networkx graph by adding "start" node and "end" node
    """
    roots = get_root(graph, graph_nodes)
    ends = get_end(graph, graph_nodes)
    graph.add_node("start", process_time="00:00:00")
    graph.add_node("end", process_time="00:00:00")
    graph.add_edges_from([(node, "end") for node in ends])
    graph.add_edges_from([("start", node) for node in roots])
    return None


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
    print("test on data storage")
    print("data inside node _1_ :", graph.nodes[graph_nodes[0]])
    print("data inside node _5_ :", graph.nodes[graph_nodes[4]])
    print("===============================================")
    # print(graph.edges, graph.nodes)

    print("starting graph transformation")
    transform(graph, graph_nodes)
    new_nodes = [*graph_nodes, "start", "end"]
    print("New root should be start : ", get_root(graph, new_nodes))
    print("New end should be end :", get_end(graph, new_nodes))
    modelling = input(
        "Do you want to see the small graph modified (y/n) (no by default):")
    try:
        modelling in ["y", "yes", "n", "no", '']
    except:
        print("wrong input !! no is choosen by default")
        modelling = 'n'
    if modelling in ["y", "yes", 'Y', "Yes", "YES"]:
        print("Modelling for the smallRandom...")
        chrono = time.time()
        graph_path = "./Graphs/smallRandom.json"
        graph, graph_nodes = extract_directed_graph(graph_path)
        transform(graph, graph_nodes)
        print("Process as taken :", time.time()-chrono, "s")
        plt.tight_layout()
        nx.draw_networkx(graph, arrows=True)
        plt.show()
        print("end view...")

    print("END")

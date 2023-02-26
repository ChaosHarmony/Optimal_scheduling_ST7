import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

file_path = './Graphs/smallComplex.json'

ds_graph = pd.read_json(file_path)

ds_graph = ds_graph['nodes']
nodes_tag = ds_graph.keys()
directed_graph_edges = []
for tag in nodes_tag:
    for parent in ds_graph[tag]['Dependencies']:
        directed_graph_edges.append((parent, tag))

directed_graph = nx.DiGraph()
directed_graph.add_edges_from(directed_graph_edges)
will_show_label = len(nodes_tag) < 100
nx.draw_networkx(directed_graph, arrows=True, with_labels=will_show_label)
plt.show()

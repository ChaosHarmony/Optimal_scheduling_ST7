from graph_functions import *
import networkx as nx

DAG = create_DAG(import_graph("Graphs/smallRandom.json"))

print(DAG.edges(data=True))

critical_path =  nx.dag_longest_path(DAG)
print(critical_path)
print(sum(map(lambda x: x.get_processing_time(), critical_path)))
import ants
import networkx as nx
import graph_operation as go


def construct_colony(n_ants, ants_class=ants.Ant_TGE, starting_point="start", objectif="end"):
    return [ants_class(starting_point, objectif)]*n_ants


def construct_pheromon_init(graph: nx.DiGraph):
    for edge in graph.edges():
        graph.update((edge, {'pheromon': 1}))


def choose_node(ant: ants.Ant,graph:nx.DiGraph, cost_func : function):
    available_nodes = go.available_set_of_node(graph, graph.nodes(), ant.solution)
    
    


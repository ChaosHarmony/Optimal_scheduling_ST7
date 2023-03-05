import ants
import networkx as nx
import itertools
import graph_operation as go


class AntColony():
    def __init__(self, DAG_scheduling: nx.DiGraph, n_ants: int, start_point: str or int = 'start', objectif_point: str or int = 'end'):
        self.directed_graph = DAG_scheduling
        self.complete_graph = go.generate_complete_graph(DAG_scheduling)
        self.colony_list = [ants.Ant(start_point, objectif_point)
                            for i in range(n_ants)]

    def init_pheromones(self):
        leaves = self.complete_graph.nodes()
        for edge in list(itertools.combinations(leaves, 2)):
            self.complete_graph.update(
                (edge[0], edge[1], {'pheromon trail': 1.}))

    def update_pheromones(self, edge: tuple, pheromon_value: float):
        """
        edge is a tuple (u,v) of the verteces u and v to designat the edge between u and v in
        the complete graph
        pheromon_value will be ADD (+) to the original value for instance :
        pheromon = pheromon - P -> pheromon_value = -P
        in place modification on the complete_graph
        """
        u, v = edge
        new_value = self.complete_graph.edges[u,
                                              v]['pheromon trail']
        self.complete_graph.update((u, v, {'pheromon trail': new_value}))

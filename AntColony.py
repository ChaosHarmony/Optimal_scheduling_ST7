import ants
import networkx as nx
import itertools
import graph_operation as go


class AntColony():
    def __init__(self, DAG_scheduling: nx.DiGraph, n_ants: int, ants: list):
        self.directed_graph = DAG_scheduling
        self.complete_graph = go.generate_complete_graph(DAG_scheduling)
        self.colony_list = ants
        self.n_ants = n_ants

    ####################################################################
    # Pheromon part
    #################################################################

    def init_pheromones(self):
        leaves = self.complete_graph.nodes()
        for edge in list(itertools.combinations(leaves, 2)):
            self.complete_graph.update(
                (edge[0], edge[1], {'pheromon trail': 1.}))

    def get_pheromon(self, u, v):
        """
        the verteces u and v designate the edge between u and v in
        the complete graph
        """
        return self.complete_graph.edges[u, v]['pheromon trail']

    def update_pheromones(self, u, v, pheromon_value: float):
        """
        edge is a tuple (u,v) of the verteces u and v to designate the edge between u and v in
        the complete graph
        pheromon_value will be ADD (+) to the original value for instance :
        pheromon = pheromon - P -> pheromon_value = -P
        in place modification on the complete_graph
        """
        new_value = self.get_pheromon(u, v) - pheromon_value
        self.complete_graph.update((u, v, {'pheromon trail': new_value}))

    #################################################################
    # Generalized ant operations
    #################################################################

    def get_solution_list(self):
        return [self.colony_list[i].solution for i in range(self.n_ants)]

    def get_machine_attribution_list(self):
        """
        Only works if ants are Ant_TGE type
        """
        try:
            type(self.colony_list[0]) == type(ants.Ant_TGE)
        except:
            raise Exception("Ants are of wrong type")

        return [self.colony_list[i].affected_machine for i in range(self.n_ants)]

    ##################################################################
    #

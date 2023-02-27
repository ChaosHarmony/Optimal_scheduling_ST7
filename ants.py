import networkx as nx
import itertools


class Ant():

    def __init__(self, starting_point, objectif_point):
        self.solution = [starting_point]
        self.objectif = objectif_point

    def is_visited(self, node):
        return node in self.solution

    def choose_node(self, node):
        self.solution.append(node)

    def has_finished(self):
        return self.objectif == self.solution[-1]

    def init_pheromones(self, graph):
        pheromones = nx.Graph()
        leaves = graph.nodes
        pheromones.add_nodes_from(graph.nodes)
        for edge in list(itertools.combinations(leaves, 2)):
            pheromones.add_edge(edge[0], edge[1], weight=1)
        return pheromones


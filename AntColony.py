import ants
import networkx as nx
import itertools
import graph_operation as go
import matplotlib.pyplot as plt


class AntColony():
    def __init__(self, DAG_scheduling: nx.DiGraph, ants: list, Q: int, evaporation: float, C: int, alpha: float, beta: float):
        self.directed_graph = DAG_scheduling
        self.complete_graph = go.generate_complete_graph(DAG_scheduling)
        self.colony_list = ants
        self.n_ants = len(ants)
        self.rho = evaporation
        self.Q = Q
        self.alpha = alpha
        self.beta = beta
        self.C = C
    ####################################################################
    # Pheromon part
    #################################################################

    def init_pheromones(self):
        leaves = self.complete_graph.nodes()
        for edge in list(itertools.combinations(leaves, 2)):
            print("inside")
            self.complete_graph.update(
                [(edge[0], edge[1], {'pheromon trail': 100.})])

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
        self.complete_graph.update((u, v, {'pheromon trail': pheromon_value}))

    #################################################################
    # Generalized ant operations
    #################################################################

    def get_solution_list(self):
        return [self.colony_list[i].solution for i in range(self.n_ants)]

    def has_finished(self):
        for i in range(self.n_ants):
            if not self.colony_list[i].has_finished():
                return False
        return True

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
    #   Running the colony
    ##################################################################

    def run(self):
        """
        Works only with ant_TGE
        """

        while not self.has_finished():
            for i in range(self.n_ants):
                ant = self.colony_list[i]
                ant = ants.Ant_TGE
                if True in ant.machine_available():
                    chosen_machine = ant.choose_machine()
                else:
                    min_duration = min(ant.machines_time_track)
                    ant.update_all_time_track(duration=min_duration)

                choosen_node = go.rank_reachable_nodes(ant, self)
                ant.add_node(choosen_node)
                time_elapsed = self.directed_graph.nodes[choosen_node]['process_time']
                ant.add_machine(chosen_machine)
                ant.update_machine_time_track(chosen_machine, time_elapsed)

    def reset(self):
        for i in range(self.n_ants):
            self.colony_list[i].reset()


if __name__ == "__main__":
    print("testing range")
    print("===================================================")
    graph_path = "./Graphs/smallRandom.json"
    print("getting graph from ", graph_path, " ...")
    graph, graph_nodes = go.extract_directed_graph(graph_path)
    print("starting graph transformation")
    go.transform(graph, graph_nodes)
    new_nodes = [*graph_nodes, "start", "end"]

    colony = AntColony(graph, ants=[ants.Ant(
        'start', 'end') for i in range(10)])
    print("colony is based on 10 ants : ", colony.n_ants)
    print("we should have created a complete garph while initializing the colony")
    plt.tight_layout()
    nx.draw_networkx(colony.complete_graph, arrows=False)
    plt.show()

    print('complete graph edeges are ', colony.complete_graph.edges)

    print('initialzing pheromon, should update the complete graph')
    colony.init_pheromones()
    print("pheromones added : ", colony.complete_graph.edges['pheromon trail'])

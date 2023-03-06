import AntColony as AC
import ants
import graph_operation as go


def


def main(n_iteration, graph_path, n_ant, n_machines):
    print("Set up")
    direct_graph, nodes_list = go.extract_directed_graph(graph_path)
    go.transform(direct_graph, nodes_list)
    nodes_list = [*nodes_list, "start", "end"]
    print("Graph ready")

    print("Making Ant colony")

    ant_list = [ants.Ant_TGE('start', "end", n_machines) for i in range(n_ant)]

    colony = AC.AntColony(direct_graph, ant_list)
    print("Pheromon init")
    colony.init_pheromones()

    for iter in range(n_iteration):
        pass

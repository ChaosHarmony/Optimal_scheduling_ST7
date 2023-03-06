import AntColony
import ants
import numpy as np
import itertools
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time


alpha = 0.1
beta = 2
C = 1
Q = 1

###################################################################################
##############              Graph extraction                   ####################
###################################################################################


def convert_to_seconds(ch):
    hh, mm, ss = ch.split(':')
    return 3600*int(hh)+60*int(mm)+float(ss)


def extract_directed_graph(graph_path: str):

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

###################################################################################
############              Graph transformation                   ##################
###################################################################################


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

###################################################################################
###############              Complete graph                   #####################
###################################################################################


def generate_complete_graph(graph):
    complete_graph = nx.Graph()
    leaves = graph.nodes
    complete_graph.add_nodes_from(graph.nodes)
    complete_graph.add_edges_from(itertools.combinations(leaves, 2))
    return complete_graph


###################################################################################
##############              Availibility set                   ####################
###################################################################################


def is_available(graph: nx.DiGraph, node: int or str, visited_nodes: list):
    """
    Tells if node is accessable with the list of visited_nodes, with precedence constraints //
    if node is already visited -> no need to go back to it
    if parent of the node are not visited -> cannot go to this node
    """
    if node in visited_nodes:
        return False
    for parent in graph.predecessors(node):
        if not (parent in visited_nodes):
            return False
    return True


def available_set_of_node(graph: nx.DiGraph, graph_nodes: list, visited_node: list):
    """
    Create a set of every accessible nodes from the visited nodes
    """
    available = set()
    for node in graph_nodes:
        if is_available(graph, node, visited_node):
            available.add(node)
    return available


def weight_nodes(graph: nx.DiGraph, graph_nodes: list):
    weight_nodes = {}
    for node in graph_nodes:
        weight_nodes[node] = graph.nodes[node]['process_time'] + \
            max([graph.nodes[j]['process_time']
                for j in graph.successors[node]])


def rank_reachable_nodes(graph: nx.DiGraph, graph_nodes: list, visited_node: list, ants: list, colony: AntColony.AntColony):
    curr_node = ants.solution[-1]
    reachable_nodes = available_set_of_node(graph, graph_nodes, visited_node)
    ranked_nodes = sorted(reachable_nodes, key=lambda x: (
        C*weight_nodes[x])**alpha*(colony.get_pheromon[curr_node][x])**beta)


def machine_attribution(graph: nx.Digraph, ants: list, colony: AntColony.AntColony, ant_tge: ants.Ant_TGE):
    '''build a machine dictionnary as follows:
    M = {machine_number:[[task1, starting_time1, ending_time1], [task2, starting_time2, ending_time2]]}
    machines are denoted from 0 to nb_machines-1
    '''

    nb_machines = ant_tge.nb_machines
    starting_time = 0
    ending_time = 0
    solution = colony.get_solution_list
    machine_attribution = colony.get_machine_attribution_list
    m = len(solution)
    M = {k: [] for k in range(nb_machines)}
    last_processed_machine = machine_attribution[0]
    for i in range(m):
        ending_time = starting_time + graph.node[solution[i]]['process_time']
        M[machine_attribution[i]].append(
            [solution[i], starting_time, ending_time])
        if last_processed_machine == machine_attribution[i]:
            starting_time = ending_time
        last_processed_machine = machine_attribution[i]
    return M


def path_cost(graph: nx.Digraph, ants: list, colony: AntColony.AntColony, ant_tge: ants.Ant_TGE):
    nb_machines = ant_tge.nb_machines
    M = machine_attribution(graph, ants, colony, ant_tge)
    return max([M[k][-1][2] for k in range(nb_machines)])


def update_pheromone(graph: nx.DiGraph):
    pass


if __name__ == "__main__":

    print("TESTING RANGE")
    print("=========================================")
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

    print("===============================================")

    print("extract and transform small graph...")
    small_graph_path = "./Graphs/smallRandom.json"
    small_graph, small_graph_nodes = extract_directed_graph(
        small_graph_path)
    transform(small_graph, small_graph_nodes)
    small_graph_nodes = [*small_graph_nodes, "start", "end"]

    print('=========================================')
    print("starting test of advailability")
    visited_node = []
    start_set = available_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("Used visited node list :", visited_node)
    print("We should only have start in the returned set :", start_set,
          "   then the test is good :", start_set == set(["start"]))
    visited_node = ["start"]
    start_set = available_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("We should only have 1 in the returned set :", start_set,
          "   then the test is good :", start_set == set([1]))
    visited_node = ["start", 1]
    start_set = available_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("We should only have 2,3,4 in the returned set :", start_set,
          "   then the test is good :", start_set == set([2, 3, 4]))
    visited_node = ["start", 1, 2, 3, 4, 5, 7, 9]
    start_set = available_set_of_node(
        small_graph, small_graph_nodes, visited_node)
    print("\nUsed visited node list :", visited_node)
    print("The returned set is : ", start_set)
    print("end is not in the returned set :", not "end" in start_set)

    print("==========================================================")
    print("END")

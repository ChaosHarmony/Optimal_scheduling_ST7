import AntColony as AC
import ants
import copy
import graph_operation as go


def run(colony: AC.AntColony):
    """
    Works only with ant_TGE
    """

    while not colony.has_finished():
        for i in range(colony.n_ants):
            ant = colony.colony_list[i]

            if True in ant.machine_available():
                chosen_machine = ant.choose_machine()
            else:
                min_duration = min(ant.machines_time_track)
                ant.update_all_time_track(duration=min_duration)
                chosen_machine = ant.choose_machine()

            choosen_node = go.rank_reachable_nodes(ant, colony)
            ant.add_node(choosen_node)
            time_elapsed = colony.directed_graph.nodes[choosen_node]['process_time']
            ant.add_machine(chosen_machine)
            ant.update_machine_time_track(chosen_machine-1, time_elapsed)


def get_ant_path(ant_solution: list):
    """
    Construct the path as a list of edges of each ants in the colony
    """
    ant_path = []
    for i in range(1, len(ant_solution)):
        ant_path.append(
            (ant_solution[i-1], ant_solution[i]))
    return ant_path


def pheromon_value_update(objective_function, colony: AC.AntColony):
    for solution in colony.get_solution_list():
        cost = objective_function(solution)
        path = get_ant_path(solution)
        for edge in path:
            u, v = edge
            trail = colony.get_pheromon(u, v)
            colony.update_pheromones(
                u, v, (1-colony.rho) * trail + colony.Q/cost)


def get_best_solution(objective_function, colony: AC.AntColony):
    best = colony.colony_list[0]
    best_cost = objective_function(best, colony)
    for ant in colony.colony_list:
        curr_cost = objective_function(ant, colony)
        if best_cost > curr_cost:
            best = ant
            best_cost = curr_cost
    return best


def main(n_iteration, graph_path, n_ant, n_machines):
    print("Set up")
    direct_graph, nodes_list = go.extract_directed_graph(graph_path)
    go.transform(direct_graph, nodes_list)
    nodes_list = [*nodes_list, "start", "end"]
    print("Graph ready")

    print("Making Ant colony")

    ant_list = [ants.Ant_TGE('start', "end", n_machines) for i in range(n_ant)]

    colony = AC.AntColony(direct_graph, ant_list, 400, 0.1, 400, 2, 1)
    print("Pheromon init")
    colony.init_pheromones()

    result_dict = {}
    print("================================= START ======================================")

    for iter in range(n_iteration):
        print("iteration number : ", iter+1)
        run(colony)
        result_dict[iter+1] = copy.copy(get_best_solution(
            go.path_cost  # objective_function
            , colony))
        colony.reset()

    print("END")

    return result_dict


result = main(10, './Graphs/smallRandom.json', 10, 2)
print("result = ", result)
print("solution of ant 10 :", result[10].solution)

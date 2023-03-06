import AntColony as AC
import ants
import graph_operation as go


def get_ant_path(ant_solution: list):
    """
    Construct the path as a list of edges of each ants in the colony
    """
    ant_path = []
    for i in range(1, len(ant_solution)):
        ant_path.append(
            (ant_solution[i-1], ant_solution[i]))
    return ant_path


def pheromon_value_update(objective_function: function, colony: AC.AntColony):
    for solution in colony.get_solution_list():
        cost = objective_function(solution)
        path = get_ant_path(solution)
        for edge in path:
            u, v = edge
            trail = colony.get_pheromon(u, v)
            colony.update_pheromones(
                u, v, (1-colony.rho) * trail + colony.Q/cost)


def get_best_solution(objective_function: function, results):
    best = results[0]
    best_cost = objective_function(best)
    for result in results:
        if best_cost > objective_function(result):
            best = result
            best_cost = objective_function
    return best


def main(n_iteration, graph_path, n_ant, n_machines, objective_function, attractive_function):
    global N_MACHINES
    N_MACHINES = n_machines
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

    result_dict = {}
    print("================================= START ======================================")

    for iter in range(n_iteration):
        print("iteration number : ", iter)
        colony.run(attractive_function)
        result_dict[iter] = get_best_solution(
            objective_function, colony.get_solution_list())
        colony.reset()

    print("END")

    return result_dict

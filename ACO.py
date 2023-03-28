import numpy as np
from visibility_func import procces_visibilty_func
from mpi4py import MPI
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from math import floor

# Establishing communication
comm = MPI.COMM_WORLD
# MPI starts here
comm_size = comm.Get_size()
rank = comm.Get_rank()


def test_func_MPI():
    # Establishing communication
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print("Hello from process {0} out of {1}".format(rank, size))


# Objective Functions


def makespan(machines) -> float:  # list[Machine]
    return max(map(lambda x: x.completion_time(), machines))


# Helper Functions
def get_initial_jobs(graph: nx.DiGraph):  # list[Job]
    return list(map(lambda x: x[0], filter(lambda x: x[1] == 0, graph.in_degree())))


def get_next_available_jobs(graph: nx.DiGraph, visited_jobs, completed_job: Job):
    available_jobs = []
    # iterates over the successor of the completed_job
    for successor in graph.successors(completed_job):
        for parent in graph.predecessors(successor):
            if parent not in visited_jobs:
                break
        else:
            available_jobs.append(successor)
    return available_jobs


def probabilites_construction(alpha: float, beta: float, eta: np.array, pheromone_matrix: np.array, jobs_to_index_mapping, current_node: Job = None, available_nodes=None):
    available_idx = list(
        map(lambda x: jobs_to_index_mapping[x], available_nodes))
    available_probabilites = np.ones(len(available_idx))
    if current_node != None:
        current_idx = jobs_to_index_mapping[current_node]
        for idx in range(len(available_idx)):
            available_probabilites[idx] = pheromone_matrix[current_idx,
                                                           available_idx[idx]] ** alpha * eta[current_idx, available_idx[idx]] ** beta
    else:
        for idx in range(len(available_idx)):
            available_probabilites[idx] = pheromone_matrix[available_idx[idx],
                                                           available_idx[idx]] ** alpha * eta[available_idx[idx], available_idx[idx]] ** beta
    available_probabilites /= np.sum(available_probabilites)

    return available_probabilites


def ACO_hybrid_ants(graph: nx.DiGraph, num_machines: int = 2, num_ants: int = 10, alpha: float = 1.0, beta: float = 2.0, evaporation_rate: float = 0.2, q: float = 1.0, n_best: float = 0.10, switching_rate=0.5, visibility_function=procces_visibilty_func, num_iterations: int = 100, normalizing=True):
    '''
    graph : directed graph
    num_machines : number of machines given by the problem
    num_ants : set the number of ants inside each colony
    alpha : exponent coefficient for the pheromons
    beta : exponent coefficient for prior knowledge / visibility
    evaporation_rate : should be between 0 and 1, rate at which the pheronom trail lessen
    q : pheromon laying coefficient
    q_best : pheromon laying for the best ant found yet. The number represents how many ants she equate to.
    num_iteration : number of time the colony will run the graph.

    returns : [best_makespan, best_schedule]

    '''
    local_num_ant = num_ants//comm_size
    print("Hello from process {0} out of {1}. I'm working with {2} ants".format(
        rank, comm_size, local_num_ant))
    # Mappings from Job to Indices of Phermonone/Visibility Matrices
    index_to_jobs_mapping = {idx: job for idx, job in enumerate(graph.nodes())}
    jobs_to_index_mapping = {job: idx for idx, job in enumerate(graph.nodes())}

    # Initialise the Phermonone Matrix and Visbility Matrix
    pheromone_matrix = np.ones((len(graph), len(graph)))
    eta = np.zeros((len(graph), len(graph)))
    if normalizing:
        for i in range(len(graph)):
            for j in range(len(graph)):
                eta[i, j] = visibility_function(index_to_jobs_mapping[j])
        max_eta = np.max(eta)
        eta = eta/max_eta

    else:

        for i in range(len(graph)):
            for j in range(len(graph)):
                eta[i, j] = visibility_function(index_to_jobs_mapping[j])

    best_global_schedule = None
    best_global_makespan = np.inf

    # print("Eta", eta)
    # print("Initial Pheormone Matrix",pheromone_matrix)

    local_iterations_results = {}

    for it in range(num_iterations):
        # Create a list of tuples for ant solutions
        local_ant_solutions = []

        # Completed Job dict to fix scheudling bug
        # [Job] : {Node: ("Machine", "start_time", "end_time"))
        completed_jobs = {}
        # Local process best ant :
        best_local_schedule = None
        best_local_makespan = np.inf

        basic_ants = True

        for ant in range(local_num_ant):

            # initiate variables
            machines = [Machine(i+1) for i in range(num_machines)]
            visited_jobs = set()
            available_nodes = get_initial_jobs(graph=graph)

            # choose the node "start"
            current_node = np.random.choice(available_nodes, p=probabilites_construction(
                alpha, beta, eta, pheromone_matrix, jobs_to_index_mapping, None, available_nodes))
            visited_jobs.add(current_node)

            machines.sort(key=lambda machine: machine.current_job_end_time)
            machines[0].perform_job(current_node, completed_jobs)
            ant_path = [current_node]
            available_nodes.remove(current_node)

            # starting tour

            while len(visited_jobs) < len(graph):
                available_nodes += get_next_available_jobs(
                    graph=graph, visited_jobs=visited_jobs, completed_job=current_node)
                next_node = np.random.choice(
                    available_nodes,
                    p=probabilites_construction(alpha, beta, eta, pheromone_matrix, jobs_to_index_mapping,
                                                current_node=current_node, available_nodes=available_nodes)
                )

                machines.sort(key=lambda machine: machine.current_job_end_time)
                machines[0].perform_job(next_node, completed_jobs)
                visited_jobs.add(next_node)
                ant_path.append(next_node)
                available_nodes.remove(next_node)
                current_node = next_node

            # everything is done
            completed_jobs.clear()
            # get solution localized
            local_ant_solutions.append((ant_path, machines))
            # get the makespan localized
            local_current_makespan = makespan(machines)

            # Update best local ant
            if local_current_makespan < best_global_makespan:
                best_global_makespan = local_current_makespan
                best_global_schedule = machines
            # no more in the ant loop
            # every local ants have done their tour
            local_iterations_results[it] = []
        for ant in range(local_num_ant):
            local_iterations_results[it].append(makespan(
                local_ant_solutions[ant][1]))

        # adding a best ant method
        best_ant_index = np.argmin(
            list(map(lambda x: makespan(x[1]), local_ant_solutions)))
        best_ant_makespan = makespan(local_ant_solutions[best_ant_index][1])

        if basic_ants and (it+1 > floor(num_iterations*switching_rate)) and n_best != 0:
            basic_ants = False

            # Updating the Pheromone Matrix after each ant
            # Evaporation affect all process the same...
        pheromone_matrix *= (1-evaporation_rate)
        # local addition of ants' choice
        local_pheromone_addition_matrix = np.zeros_like(pheromone_matrix)
        if basic_ants:

            for ant_solution in local_ant_solutions:
                for i in range(len(ant_solution[0]) - 1):
                    local_pheromone_addition_matrix[jobs_to_index_mapping[ant_solution[0][i]],
                                                    jobs_to_index_mapping[ant_solution[0][i+1]]] += q*np.exp(100*(best_ant_makespan-makespan(ant_solution[1]))/best_ant_makespan)
            global_addition_matrix = np.zeros_like(
                local_pheromone_addition_matrix)
            comm.Allreduce(
                local_pheromone_addition_matrix, global_addition_matrix, op=MPI.SUM)
            pheromone_matrix += global_addition_matrix

        ########################################################
        else:  # swiching to elite ant strategy
            elite_pheromon = np.zeros_like(local_pheromone_addition_matrix)
            every_ants_solution_gather = comm.gather(
                local_ant_solutions, root=0)
            ############### Gathering in one process ###############
            if comm.Get_rank() == 0:
                every_ants_solution = []
                for process in range(comm.Get_size()):
                    for ant in every_ants_solution_gather[process]:
                        every_ants_solution.append(ant)
                # Exiting gathering loop
                best_ant_indexes = np.argsort(
                    list(map(lambda x: makespan(x[1]), local_ant_solutions)))
                best_ants = []
                for index in range(floor(num_ants*n_best)):
                    best_ants.append(
                        local_ant_solutions[best_ant_indexes[index]])
            ###### Selected best ants ####################

                for ant_solution in best_ants:
                    for i in range(len(ant_solution[0]) - 1):
                        local_pheromone_addition_matrix[jobs_to_index_mapping[ant_solution[0][i]],
                                                        jobs_to_index_mapping[ant_solution[0][i+1]]] += q*np.exp(100*(best_ant_makespan-makespan(ant_solution[1]))/best_ant_makespan)
                # exit 0 process
            # colecting
            comm.Bcast(elite_pheromon, root=0)
            pheromone_matrix += elite_pheromon
        # addition of all resulting matrix

        # print(f'Iteration {it}:', pheromone_matrix)

        # LOCAL RESULT FOR LOCAL SENDING
    return best_global_makespan, best_global_schedule, local_iterations_results


def ACO_elite_ants(graph: nx.DiGraph, num_machines: int = 2, num_ants: int = 10, alpha: float = 1.0, beta: float = 2.0, evaporation_rate: float = 0.2, q: float = 1.0, num_iterations: int = 100):
    '''
    graph : directed graph
    num_machines : number of machines given by the problem
    num_ants : set the number of ants inside each colony
    alpha : exponent coefficient for the pheromons
    beta : exponent coefficient for prior knowledge / heuristic
    evaporation_rate : should be between 0 and 1, rate at which the pheronom trail lessen
    q : pheromon laying coefficient
    num_iteration : number of time the colony will run the graph.

    returns : (best_makespan, best_schedule, iteration_results)

    '''
    # Mappings from Job to Indices of Phermonone/Visibility Matrices
    index_to_jobs_mapping = {idx: job for idx, job in enumerate(graph.nodes())}
    jobs_to_index_mapping = {job: idx for idx, job in enumerate(graph.nodes())}

    # Initialise the Phermonone Matrix and Visbility Matrix
    pheromone_matrix = np.ones((len(graph), len(graph)))
    eta = np.zeros((len(graph), len(graph)))
    for i in range(len(graph)):
        for j in range(len(graph)):
            eta[i, j] = 1 / index_to_jobs_mapping[j].get_processing_time()

    best_global_schedule = None
    best_global_makespan = np.inf

    # print("Eta", eta)
    # print("Initial Pheormone Matrix",pheromone_matrix)

    iterations_results = {}

    for it in range(num_iterations):
        # Create a list of tuples for ant solutions
        ant_solutions = []  # list[(list[Job], list[Machine])]

        # Completed Job dict to fix scheudling bug
        # [Job] : {Node: ("Machine", "start_time", "end_time"))
        completed_jobs = {}

        for ant in range(num_ants):
            machines = [Machine(i+1) for i in range(num_machines)]
            visited_jobs = set()
            available_nodes = get_initial_jobs(graph=graph)

            current_node = np.random.choice(available_nodes, p=probabilites_construction(
                alpha, beta, eta, pheromone_matrix, jobs_to_index_mapping, None, available_nodes))
            visited_jobs.add(current_node)

            machines.sort(key=lambda machine: machine.current_job_end_time)
            machines[0].perform_job(current_node, completed_jobs)
            ant_path = [current_node]
            available_nodes.remove(current_node)

            while len(visited_jobs) < len(graph):
                available_nodes += get_next_available_jobs(
                    graph=graph, visited_jobs=visited_jobs,
                    completed_job=current_node
                )
                next_node = np.random.choice(
                    available_nodes,
                    p=probabilites_construction(alpha, beta, eta, pheromone_matrix, jobs_to_index_mapping,
                                                current_node=current_node, available_nodes=available_nodes)
                )

                machines.sort(key=lambda machine: machine.current_job_end_time)
                machines[0].perform_job(next_node, completed_jobs)
                visited_jobs.add(next_node)
                ant_path.append(next_node)
                available_nodes.remove(next_node)
                current_node = next_node

            completed_jobs.clear()

            ant_solutions.append((ant_path, machines))

        best_ant_index = np.argmin(
            list(map(lambda x: makespan(x[1]), ant_solutions)))
        best_ant_solution = ant_solutions[best_ant_index]
        best_ant_makespan = makespan(best_ant_solution)

        # Updating the Pheromone Matrix using the best ant in each colony
        pheromone_matrix *= (1-evaporation_rate)

        for i in range(len(ant_path) - 1):
            pheromone_matrix[jobs_to_index_mapping[ant_path[i]],
                             jobs_to_index_mapping[ant_path[i+1]]] += q*np.exp((best_ant_makespan-makespan(machines))/best_ant_makespan)

        current_makespan = makespan(best_ant_solution[1])

        iterations_results[it + 1] = {"Makespan": current_makespan,
                                      "Schedule": best_ant_solution[1]}

        if current_makespan < best_global_makespan:
            best_global_makespan = current_makespan
            best_global_schedule = best_ant_solution[1]

    return best_global_makespan, best_global_schedule, iterations_results


if __name__ == "__main__":

    test_func_MPI()

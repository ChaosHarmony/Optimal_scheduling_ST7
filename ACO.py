import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine

# Objective Functions


def makespan(machines: list[Machine]) -> float:
    return max(map(lambda x: x.completion_time(), machines))


# Helper Functions
def get_initial_jobs(graph: nx.DiGraph) -> list[Job]:
    return list(map(lambda x: x[0], filter(lambda x: x[1] == 0, graph.in_degree())))


def get_next_avaiable_jobs(graph: nx.DiGraph, visited_jobs: set[Job], completed_job: Job) -> list[Job]:
    successors: list[Job] = list(graph.successors(completed_job))
    available_jobs = []
    for successor in successors:
        for parent in graph.predecessors(successor):
            if parent not in visited_jobs:
                break
        else:
            available_jobs.append(successor)
    return available_jobs


def probabilites_construction(alpha: float, beta: float, eta: np.array, pheromone_matrix: np.array, jobs_to_index_mapping, current_node: Job = None, available_nodes: list[Job] = None):
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


def ACO_basic_ants(graph: nx.DiGraph, num_machines: int = 2, num_ants: int = 10, alpha: float = 1.0, beta: float = 5.0, evaporation_rate: float = 0.5, q: float = 1.0, num_iterations: int = 100):
    '''
    graph : directed graph
    num_machines : number of machines given by the problem
    num_ants : set the number of ants inside each colony
    alpha : exponent coefficient for the pheromons
    beta : exponent coefficient for prior knowledge / heuristic
    evaporation_rate : should be between 0 and 1, rate at which the pheronom trail lessen
    q : pheromon laying coefficient
    num_iteration : number of time the colony will run the graph.

    returns : [best_makespan, best_schedule]

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

    best_schedule = None
    best_makespan = np.inf

    #print("Eta", eta)
    #print("Initial Pheormone Matrix",pheromone_matrix)

    for it in range(num_iterations):
        # Create a list of tuples for ant solutions
        ant_solutions: list[(list[Job], list[Machine])] = []

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
                available_nodes += get_next_avaiable_jobs(
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

            completed_jobs.clear()
            ant_solutions.append((ant_path, machines))

            # Updating the Pheromone Matrix after each ant tour
            pheromone_matrix *= (1-evaporation_rate)
            for i in range(len(ant_path) - 1):
                pheromone_matrix[jobs_to_index_mapping[ant_path[i]],
                                 jobs_to_index_mapping[ant_path[i+1]]] += q/makespan(machines)

            #print(f'Iteration {it}: Ant {ant}', pheromone_matrix)

            current_makespan = makespan(machines)
            if current_makespan < best_makespan:
                best_makespan = current_makespan
                best_schedule = machines

    return best_makespan, best_schedule


def ACO_elite_ants():
    pass

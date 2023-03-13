import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from queue import PriorityQueue

## Importing from json file and preprocessing
def convert_to_seconds(ch):
    hh, mm, ss = ch.split(':')
    return 3600*int(hh) + 60*int(mm) + float(ss)

def import_graph(filepath: str) -> list[Job]:
    with open(filepath) as data:
        contents = data.read()
    contents = json.loads(contents)
    
    temp_job_dict = {int(node) : Job(int(node)) for node in contents['nodes'].keys()}
    
    for node, value in contents['nodes'].items():
        node = int(node)
        temp_job_dict[node].processing_time = convert_to_seconds(value["Data"])
        temp_job_dict[node].dependencies = [temp_job_dict[node] for node in value["Dependencies"]]
    return list(temp_job_dict.values())

def create_DAG(joblist : list[Job]):
    G = nx.DiGraph()
    G.add_nodes_from(joblist)
    for job in joblist:
        for precendent_job in job.dependencies:
            G.add_edge(precendent_job, job)
    return G

DAG = create_DAG(import_graph("Graphs/testGraph.json"))
print(DAG)


#### ACO - Elitist Ants let's capture all of this into one function

# Mappings
index_to_jobs_mapping = {idx: job for idx, job in enumerate(DAG.nodes())}
jobs_to_index_mapping = {job: idx for idx, job in enumerate(DAG.nodes())}


# Define the problem instance
num_machines = 2


# Define the ACO parameters
num_ants = 10
alpha = 1.0  # controls the importance of pheromone
beta = 5.0  # controls the importance of heuristic information
evaporation_rate = 0.5
q = 1.0  # pheromone deposit amount
num_iterations = 100

# objective function
def makespan(machines: list[Machine]) -> float:
    return max(map(lambda x : x.completion_time(), machines))

# Initialise the Pheromone Matrix and Heurestic Information Matrix
pheromone_matrix = np.ones((len(DAG), len(DAG)))
eta = np.zeros((len(DAG), len(DAG)))
for i in range (len(DAG)):
    for j in range(len(DAG)):
        # if DAG.has_edge(index_to_jobs_mapping[i], index_to_jobs_mapping[j]):
        eta[i,j] = 1 / index_to_jobs_mapping[j].get_processing_time()

## Helper Functions
def get_initial_jobs(graph : nx.DiGraph) -> list[Job]:
    return list(map(lambda x : x[0], filter(lambda x: x[1] == 0, graph.in_degree())))

def get_next_avaiable_jobs(graph: nx.DiGraph, visited_jobs : set[Job], completed_job : Job) -> list[Job]:
    successors: list[Job] = list(graph.successors(completed_job))
    available_jobs = []
    for successor in successors:
        for parent in graph.predecessors(successor):
            if parent not in visited_jobs:
                break
        else:
            available_jobs.append(successor)
    return available_jobs

def probabilites_construction(current_node: Job = None, available_nodes: list[Job] = None):
    available_idx = list(map(lambda x: jobs_to_index_mapping[x], available_nodes))
    available_probabilites = np.ones(len(available_idx))
    if current_node != None:
        current_idx = jobs_to_index_mapping[current_node]
        for idx in range(len(available_idx)):
            available_probabilites[idx] = pheromone_matrix[current_idx, available_idx[idx]] ** alpha * eta[current_idx,available_idx[idx]] ** beta
    else:
        for idx in range(len(available_idx)):
            available_probabilites[idx] = pheromone_matrix[ available_idx[idx], available_idx[idx]] ** alpha * eta[ available_idx[idx],available_idx[idx]] ** beta
    available_probabilites /=np.sum(available_probabilites)

    return available_probabilites
    

# Apply the ACO algorithmn
best_schedule = None
best_makespan = np.inf 




for it in range(num_iterations):
    # Create a set of ant solutions
    ant_solutions: list[(list[Job], list[Machine])] = []
    # Completed Job Dict to fix bug
    # [Job] : {Node: ("Machine", "start_time", "end_time"))
    completed_jobs = {}
    for ant in range (num_ants):
        machines = [Machine(i+1) for i in range(num_machines)]
        visited_jobs = set()
        available_nodes = get_initial_jobs(graph=DAG)
        # print("Initial", probabilites_construction(None, available_nodes))
        current_node = np.random.choice(available_nodes, p=probabilites_construction(None, available_nodes))
        visited_jobs.add(current_node)
        machines.sort(key=lambda machine : machine.current_job_end_time)
        machines[0].perform_job(current_node, completed_jobs)
        ant_path = [current_node]
        available_nodes.remove(current_node)
        
        while len(visited_jobs) < len(DAG):
            available_nodes += get_next_avaiable_jobs(DAG, visited_jobs, current_node)
            # print(current_node, available_nodes)
            # print(probabilites_construction(current_node, available_nodes))
            next_node = np.random.choice(available_nodes, p=probabilites_construction(current_node, available_nodes))
            
            machines.sort(key = lambda machine : machine.current_job_end_time)
            machines[0].perform_job(next_node, completed_jobs)
            visited_jobs.add(next_node)
            ant_path.append(next_node)
            available_nodes.remove(next_node)
            current_node = next_node
        
        print(completed_jobs)
        completed_jobs.clear()
            
        ant_solutions.append((ant_path, machines))
    # print(list(map(lambda x: makespan(x[1]), ant_solutions)))
    # print(np.argmin(list(map(lambda x: makespan(x[1]), ant_solutions))))
    
    
    best_ant_index = np.argmin(list(map(lambda x: makespan(x[1]), ant_solutions)))
    best_ant_solution = ant_solutions[best_ant_index]
    # print(best_ant_index, best_ant_solution)
    pheromone_matrix *= (1-evaporation_rate)
    for i in range(len(best_ant_solution[0])-1):
        if DAG.has_edge(best_ant_solution[0][i], best_ant_solution[0][i+1]):
            pheromone_matrix[jobs_to_index_mapping[best_ant_solution[0][i]], jobs_to_index_mapping[best_ant_solution[0][i+1]]] += q/makespan(best_ant_solution[1])
    
    current_makespan = makespan(best_ant_solution[1])
    if current_makespan < best_makespan:
        best_makespan = current_makespan
        best_schedule = best_ant_solution[1]

print(best_makespan)
print(list(map(lambda x: x.schedule, best_schedule)))
# print(pheromone_matrix)

# print(ant_solutions)
# print(makespan(ant_solutions[0][1]))
# print([job.time_completed for job in jobs_to_index_mapping.keys()])



import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from ACO import *
from graph_functions import *
from time import process_time
from mpi4py import MPI

print("\n==============================================================================\n")
comm = MPI.COMM_WORLD
print("hello main.py from : ", comm.Get_rank(), ' \n')

DAG = create_DAG(import_graph("Graphs/mediumRandom.json"))
print(DAG)

# give result in hour.


print("Basic Ants")

basic_ant_start = process_time()
local_best_makespan, local_best_schedule, local_iterations_results = ACO_basic_ants(
    graph=DAG, num_ants=1000, num_iterations=100)
basic_ant_end = process_time()
print("best makepan of process #{0} : {1}h ".format(
    comm.Get_rank(), local_best_makespan))
# print(best_schedule)
print(
    f"Elapsed time (CPU) for process#{comm.Get_rank()}: {basic_ant_end-basic_ant_start}s")
# print(list(map(lambda x: x["Makespan"], iterations_results.values())))
iterations_results_list = comm.gather(local_iterations_results, root=0)
print("\n==============================================================================\n")
if rank == 0:
    print("\n==============================================================================\n")
    print("gathering of final solutions")
    iterations_results: dict = iterations_results_list[0]
    for i in range(1, comm.Get_size()):
        for key in iterations_results.keys():
            if iterations_results_list[i][key]["Makespan"] < iterations_results[key]["Makespan"]:
                iterations_results[key] = iterations_results_list[i][key]

    plt.plot(iterations_results.keys(), list(
        map(lambda x: x["Makespan"], iterations_results.values())))
    plt.show()
    print("\n==============================================================================\n")
    print("\n====================================      END      ===============================\n")
'''
print("Elite Ants")
elite_ant_start = process_time()
best_makespan, best_schedule, iterations_results = ACO_elite_ants(
    graph=DAG, num_ants=100, num_iterations=10)
elite_ant_end = process_time()
print(best_makespan/3600)
# print(best_schedule)
print(f"Elapsed time (CPU): {elite_ant_end-elite_ant_start}s")
# print(list(map(lambda x: x["Makespan"], iterations_results.values())))


# plt.plot(iterations_results.keys(), list(map(lambda x: x["Makespan"], iterations_results.values())))
'''

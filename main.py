
import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from ACO import *
from graph_functions import *
from time import process_time


DAG = create_DAG(import_graph("Graphs/smallRandom.json"))
print(DAG)

# give result in hour.


print("Basic Ants")

basic_ant_start = process_time()
best_makespan, best_schedule, iterations_results = ACO_basic_ants(
    graph=DAG, num_ants=1000, num_iterations=100)
basic_ant_end = process_time()
print(best_makespan/3600)
# print(best_schedule)
print(f"Elapsed time (CPU): {basic_ant_end-basic_ant_start}s")
# print(list(map(lambda x: x["Makespan"], iterations_results.values())))
plt.plot(iterations_results.keys(), list(
    map(lambda x: x["Makespan"], iterations_results.values())))
plt.show()

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

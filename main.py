
import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from ACO import *
from graph_functions import *


DAG = create_DAG(import_graph("Graphs/smallRandom.json"))
print(DAG)

print("Basic Ants")
best_makespan, best_schedule, iterations_results = ACO_basic_ants(graph=DAG, num_iterations = 5)
print(best_makespan/3600)
print(list(map(lambda x: x["Makespan"], iterations_results.values())))

print("Elite Ants")
best_makespan, best_schedule, iterations_results = ACO_elite_ants(graph=DAG, num_iterations = 5)
print(best_makespan/3600)
print(list(map(lambda x: x["Makespan"], iterations_results.values())))


# plt.plot(iterations_results.keys(), list(map(lambda x: x["Makespan"], iterations_results.values())))
# plt.show()

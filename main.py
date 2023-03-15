import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from ACO import *
from graph_functions import *


DAG = create_DAG(import_graph("Graphs/testGraph.json"))
print(ACO_basic_ants(graph=DAG, num_iterations = 2))
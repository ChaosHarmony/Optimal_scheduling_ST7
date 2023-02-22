# An Optimal Job Scheduling problem (OJS)

This project focus on the optimization of a task graph with precedence constraints. The goal is to minimize the time spent compute and maybe later to minimize the cost of the job computation.

# Problem formalization

Let's considerer that we have m machines with the same feature, same specific there are identical. We need to run a set of n jobs on the m machines optimal to reduce the makespan (= total time of computation) respecting priority orders on the jobs. Using the convenient notation for optimal scheduling problem we can classifie or problem as $P|prec|C_{max}$.

# Depedencies

Code is written in python, you'll need :
Matplotlib,
numpy,
networkx

# Instruction on code

to complete...
requirements:

    m = number of machines

    M = machines dictionnary (machines are denoted from 0 to m-1)

    runtime = runtime dictionnary

    pheromone = matrix of pheromones

    last_used_machine (initialised to 0)

    last_processed_task (initialised to None)

    Machine dictionnary will be as follows:
    M = {machine_number:[[task1, starting_time1, ending_time1], [task2, starting_time2, ending_time2]]}

    nodes_infos = {node : [processed_or_not, node_parents, starting_time, ending_time]} (if not processed starting/ending_time = None)


import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from Job import Job
from Machine import Machine
from ACO import *
from visibility_func import *
from graph_functions import *
from time import process_time
from mpi4py import MPI
import plot_save


def visibility_choice(parameters):
    global visibility_func
    if parameters["visibility function"] == "process":
        visibility_func = procces_visibilty_func
    elif parameters["visibility function"] == "child and process":
        visibility_func = greater_work_free
    else:
        print("visibility function doesn't exist, default to greater work free")
        visibility_func = greater_work_free


def resolution(parameters):
    print("\n==============================================================================\n")
    comm = MPI.COMM_WORLD
    print("hello main.py from : ", comm.Get_rank(), ' \n')

    DAG = create_DAG(import_graph(parameters["DAG_path"]))
    print(DAG)

    # choosing the right function

    visibility_choice(parameters)

    if parameters["Ants type"] == "Basic Ants":
        print("Basic Ants")

        basic_ant_start = process_time()

        local_best_makespan, local_best_schedule, local_iterations_results = ACO_basic_ants(
            graph=DAG, num_machines=parameters["machines number"], num_ants=parameters[
                "ants number"], alpha=parameters["alpha"],
            beta=parameters["beta"], evaporation_rate=parameters["evaporation"], q=parameters["Q"],
            n_best=parameters["nbest"], visibility_function=visibility_func,
            num_iterations=parameters["iteration number"], normalizing=parameters["normalize visibility"])
# magic here ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        basic_ant_end = process_time()

        print("best makepan of process #{0} : {1} ".format(
            comm.Get_rank(), local_best_makespan/parameters["time unit"]))
        # print("best schedule of process #{0} : {1} ".format(
        #    comm.Get_rank(), local_best_schedule))
        print(
            f"Elapsed time (CPU) for process#{comm.Get_rank()}: {basic_ant_end-basic_ant_start}s")

        # print(list(map(lambda x: x["Makespan"], iterations_results.values())))
        iterations_results_list = comm.gather(local_iterations_results, root=0)
        makespan_list = comm.gather(local_best_makespan, root=0)
        print("\n==============================================================================\n")
        if rank == 0:
            print(
                "\n==============================================================================\n")
            print("gathering of final solutions")
            iterations_results: dict = {}
            for iter in range(parameters["iteration number"]):
                local_ant_list = []
                for ant in range(parameters["ants number"]//comm_size):
                    for i in range(0, comm.Get_size()):
                        local_ant_list.append(
                            iterations_results_list[i][iter][ant])

                iterations_results[iter] = local_ant_list
            plot_save.plot_save(iterations_results, parameters)
            print(
                "\n============================    FINAL RESULTS   =================================\n")

            print("best makespan : ", min(
                makespan_list)/parameters["time unit"])
            print(
                "\n====================================      END      ===============================\n")
    if parameters["Ants type"] == "Elite Ants":
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

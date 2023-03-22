import matplotlib.pyplot as plt
import numpy as np


def plot_save(result_dict: dict, parameters: dict):
    iteration = result_dict.keys()
    max_results = np.empty((parameters['iteration number'],))
    min_results = np.empty((parameters['iteration number'],))
    mean_results = np.empty((parameters['iteration number'],))
    standard_deviation = np.empty((parameters['iteration number'],))
    for iter in iteration:
        # extraction

        ants = result_dict[iter].keys()
        num_ant = len(ants)
        iteration_makespan = np.empty((num_ant,))
        for ant in ants:
            iteration_makespan[ant] = result_dict[iter][ant]['Makespan']

        # time unit
        tu = parameters["time unit"]
        # operation
        max_results[iter] = np.max(iteration_makespan)/tu
        min_results[iter] = np.min(iteration_makespan)/tu
        mean_results[iter] = np.mean(iteration_makespan)/tu
        standard_deviation[iter] = np.std(iteration_makespan)/tu

        if parameters['log scale']:
            max_results = np.log10(max_results)
            min_results = np.log10(min_results)
            mean_results = np.log10(mean_results)
            standard_deviation = np.log10(standard_deviation)

        # end of tables

    plt.figure(1)
    plt.plot(iteration, max_results, color="red",
             marker='.', ls='', label='max')
    plt.plot(iteration, min_results, color="red",
             marker='.', ls='', label='min')
    plt.plot(iteration, mean_results, "--g", label="mean")
    # plt.plot(iteration, mean_results+standard_deviation,
    #         color="purple", label="mean + std")
    # plt.plot(iteration, mean_results-standard_deviation,
    #         color="blue", label="mean - std")
    plt.xlabel("Iterations of ant colony")
    plt.ylabel("Makespan (h)")
    plt.title("Optimization of ... with {0} ants and {1} iterations. \n Q = {2}, \rho = {3}, \alpha = {4}, \beta = {5}".format(
        num_ant, parameters['iteration number'], parameters["Q"], parameters["evaporation"], parameters["alpha"], parameters["beta"]))
    plt.legend()
    plt.savefig("./results.png")

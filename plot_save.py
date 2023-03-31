import matplotlib.pyplot as plt
import numpy as np
from ACO import makespan


def select_graph(parameters):
    biggis = parameters['DAG_path'][parameters['DAG_path'].index('/')+1::]
    return biggis[biggis.index('/')+1::]


def plot_save(result_dict: dict, parameters: dict):
    iteration = result_dict.keys()
    graph_name = select_graph(parameters)
    max_results = np.empty((parameters['iteration number'],))
    min_results = np.empty((parameters['iteration number'],))
    mean_results = np.empty((parameters['iteration number'],))
    standard_deviation = np.empty((parameters['iteration number'],))
    median_results = np.empty((parameters['iteration number'],))
    num_ant = len(result_dict[0])
    for iter in iteration:
        # extraction

        iteration_makespan = np.array(result_dict[iter])
        # for ant in range(num_ant):
        #    iteration_makespan[ant] = makespan(result_dict[iter][ant][1])

        # time unit
        tu = parameters["time unit"]
        # operation
        max_results[iter] = np.max(iteration_makespan)/tu
        min_results[iter] = np.min(iteration_makespan)/tu
        mean_results[iter] = np.mean(iteration_makespan)/tu
        standard_deviation[iter] = np.std(iteration_makespan)/tu
        median_results[iter] = np.median(iteration_makespan)/tu

        if parameters['log scale']:
            max_results = np.log10(max_results)
            min_results = np.log10(min_results)
            mean_results = np.log10(mean_results)
            standard_deviation = np.log10(standard_deviation)

        # end of tables

    plt.figure()
    plt.plot(iteration, max_results, color="red",
             marker='.', ls='', label='max')
    plt.plot(iteration, min_results, color="red",
             marker='.', ls='', label='min')
    plt.plot(iteration, mean_results, "--g", label="mean")
    plt.plot(iteration, mean_results+standard_deviation,
             color="purple", label="mean + std")
    plt.plot(iteration, mean_results-standard_deviation,
             color="blue", label="mean - std")
    plt.plot(iteration, median_results, linestyle='-',
             color='black', label='median')
    plt.xlabel("Iterations of ant colony")
    plt.ylabel("Makespan (h)")
    plt.title("Optimization of {0} with {1} ants and {2} iterations. \n Q = {3}, rho = {4}, alpha = {5}, beta = {6}, C = {7}".format(graph_name,
                                                                                                                                     num_ant, parameters['iteration number'], parameters["Q"], parameters["evaporation"], parameters["alpha"], parameters["beta"], parameters['C']))
    plt.legend()
    plt.savefig("{0}{1}_{2}_{3}iter_{4}_{5}.png".format(
        parameters["repo"], graph_name, parameters["Ants type"], parameters["iteration number"], parameters["reward"], np.random.randint(0, 2**8)))
    plt.close()


if __name__ == "__main__":

    parameters = {"DAG_path": "./Graphs/smallmedium"}
    print(select_graph(parameters))

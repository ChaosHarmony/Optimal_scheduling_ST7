from intermediate import resolution

parameters = {
    "DAG_path":
    "./Graphs/mediumRandom.json",
    # "./Graphs/xlargeComplex.json",
    # "./Graphs/mediumComplex.json",

    "Ants type":
    "Hybrid Ants",
    # "Basic Ants",
    # "Elite Ants",


    "machines number":
    "get",  # get to use

    "ants number":
    100,

    "iteration number":
    100,

    # HYPERPARAM
    "alpha":
    1.0,
    "beta":
    2.0,
    "evaporation":
    0.25,
    "Q":
    1,
    "nbest":
    0.10,
    "switching rate":  # sr*nu_it = it with basic ants
    0.5,
    "visibility function":
    # "process",
    "child and process",

    "normalize visibility":
    True,

    # print option :
    "log scale": False,
    "time unit":
    # 1,   #s
    # 60, #min
    3600,  # h

    "txt results": False,

    "repo": "./results/"
}

print("Testing for several Q values")
Q_test = [0.01, 0.1, 0.3, 0.5, 1, 10, 50, 100, 1000]
for Q in Q_test:
    parameters["Q"] = Q
    resolution(parameters)
print("====================== END of Q =============================")
print("\n Testing with 2Q, differente alpha and beta bias values")
alpha_beta = [(1, 1), (0.5, 1), (0.1, 1), (0.1, 0.5),
              (0.5, 0.1), (1, 0.1), (1, 2), (2, 1), (2, 2)]
for alpha, beta in alpha_beta:
    parameters["alpha"] = alpha
    parameters["beta"] = beta
    for Q in [1, 50]:
        parameters["Q"] = Q
        resolution(parameters)
print("========================= END of alpha beta ====================")
print("\n testing differente evaporations")
evap = [0.1, 0.2, 0.25, 0.3, 0.5, 0.7]
parameters["alpha"] = 1
parameters["beta"] = 2
parameters["Q"] = 50
for rho in evap:
    parameters["evaporation"] = rho
    resolution(parameters)
print("=========================== END ==========================")

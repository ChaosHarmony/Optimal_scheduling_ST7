from intermediate import resolution

parameters = {
    "DAG_path":
    #"./Graphs/mediumRandom.json",
     "./Graphs/largeComplex.json",
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
    2.0,
    "beta":
    1.0,
    "evaporation":
    0.3,
    "Q":
    1,
    "reward":
    "exp",
    # "frac",
    "C":
    50,
    # 1,
    # 10,
    "nbest":
    0.10,
    "switching rate":  # sr*nu_it = it with basic ants
    0.5,
    "visibility function":
    "process",
    # "child and process",

    "normalize visibility":
    False,

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
Q_test = [0.001, 0.01, 0.1, 1, 10, 100]
parameters["repo"] = "./results/Q_param/"
for Q in Q_test:
    parameters["Q"] = Q
    resolution(parameters)
print("====================== END of Q =============================")
print("\n Testing with 3Q, different alpha and beta bias values")
parameters["repo"] = "./results/Bias_param/"
alpha_beta = [(1, 1), (0.5, 1), (0.1, 1), (0.1, 0.5),
              (0.5, 0.1), (1, 0.1), (1, 2), (2, 1)]
for alpha, beta in alpha_beta:
    parameters["alpha"] = alpha
    parameters["beta"] = beta
    for Q in [0.01, 0.1, 1]:
        parameters["Q"] = Q
        resolution(parameters)
print("========================= END of alpha beta ====================")
print("\n testing differente evaporations")
parameters["repo"] = "./results/evap/"
evap = [0.1, 0.2, 0.25, 0.3, 0.5, 0.7]
parameters["alpha"] = 1
parameters["beta"] = 2
parameters["Q"] = 50
for rho in evap:
    parameters["evaporation"] = rho
    resolution(parameters)
print("======================= END of evap ==========================")
parameters["repo"] = "resluts/C_param/"
C = [1, 10, 50, 100]
parameters["Q"] = 0.1
parameters["evaporation"] = 0.3
for c in C:
    parameters["C"] = c
    resolution(parameters)

print("=========================== END ==========================")

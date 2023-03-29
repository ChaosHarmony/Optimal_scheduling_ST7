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
    10,

    "iteration number":
    100,

    # HYPERPARAM
    "alpha":
    1.0,
    "beta":
    1.0,
    "evaporation":
    0.975,
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
    0,
    "switching rate":  # sr*nu_it = it with basic ants
    0,
    "visibility function":
    "process",
    # "child and process",

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

results = resolution(parameters)

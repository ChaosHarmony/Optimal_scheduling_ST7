from intermediate import resolution

parameters = {
    "DAG_path":
    "./Graphs/smallRandom.json",
    # "./Graphs/xlargeComplex.json",
    # "./Graphs/mediumComplex.json",

    "Ants type":
    "Hybrid Ants",
    # "Basic Ants",
    # "Elite Ants",


    "machines number":
    2,
    "ants number":
    10,

    "iteration number":
    2,

    # HYPERPARAM
    "alpha":
    1.0,
    "beta":
    2.0,
    "evaporation":
    0.2,
    "Q":
    0.3,
    "nbest":
    0.10,
    "switching rate":  # sr*nu_it = it with basic ants
    0.5,
    "visibility function":
    # "process",
    "child and process",

    "normalize visibility":
    False,

    # print option :
    "log scale": False,
    "time unit":
    # 1,   #s
    # 60, #min
    3600,  # h

    "txt results": False,

    "repo": "./result/"
}


resolution(parameters)

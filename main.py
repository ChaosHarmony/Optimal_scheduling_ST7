from intermediate import resolution

parameters = {
    "DAG_path":
    "./Graphs/smallRandom.json",
    # "./Graphs/xlargeComplex.json",
    #"./Graphs/largeComplex.json",

    "Ants type":
    "Basic Ants",
    # "Elite Ants",


    "machines number":
    2,
    "ants number":
    100,

    "iteration number":
    50,

    # HYPERPARAM
    "alpha":
    1.0,
    "beta":
    2.0,
    "evaporation":
    0.2,
    "Q":
    50,
    "Qbest":
    100,
    "visibility function":
    # "process",
    "child and process",

    # print option :
    "log scale": False,
    "time unit":
    # 1,   #s
    # 60, #min
    3600,  # h

    "txt results": False

}


resolution(parameters)

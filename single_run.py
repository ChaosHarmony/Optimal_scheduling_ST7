from intermediate import resolution

parameters = {
    "DAG_path":
    #"./Graphs/smallRandom.json",
     "./Graphs/largeComplex.json",
    #"./Graphs/xsmallComplex.json",
    #"./Graphs/mediumRandom.json",
    
    "Ants type":
    "Hybrid Ants",
    # "Basic Ants",
    # "Elite Ants",


    "machines number":
    "get",  # get to use

    "ants number":
    20,

    "iteration number":
    50,

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
    #"process",
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

    "repo": "./results/"
}

results = resolution(parameters)

from intermediate import resolution

parameters = {
    "DAG_path":
    "./Graphs/smallRandom.json",
    # "./Graphs/mediumRandom.json",

    "Ants type":
    "Basic Ants",
    # "Elite Ants",


    "machines number":
    2,
    "ants number":
    100,

    "iteration number":
    10,

    # HYPERPARAM
    "alpha":
    1.0,
    "beta":
    2.0,
    "evaporation":
    0.2,
    "Q":
    1,
    "visibility function":
    "process"
    # "child and process"

}


resolution(parameters)

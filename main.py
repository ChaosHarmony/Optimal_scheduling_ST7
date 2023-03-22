from intermediate import resolution

parameters = {
    "DAG_path":
    # "./Graphs/smallComplex.json",
    "./Graphs/mediumRandom.json",

    "Ants type":
    "Basic Ants",
    # "Elite Ants",


    "machines number":
    2,
    "ants number":
    1000,

    "iteration number":
    100,

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

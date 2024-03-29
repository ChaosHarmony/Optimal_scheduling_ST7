import networkx as nx
from Job import Job
import json
from math import floor

# Importing from json file and preprocessing


def convert_to_seconds(ch):
    hh, mm, ss = ch.split(':')
    return 3600*int(hh) + 60*int(mm) + float(ss)


def import_graph(filepath: str):  # List[Job]
    with open(filepath) as data:
        contents = data.read()
    contents = json.loads(contents)

    temp_job_dict = {int(node): Job(int(node))
                     for node in contents['nodes'].keys()}

    for node, value in contents['nodes'].items():
        node = int(node)
        temp_job_dict[node].processing_time = convert_to_seconds(value["Data"])
        temp_job_dict[node].dependencies = [temp_job_dict[node]
                                            for node in value["Dependencies"]]
    return list(temp_job_dict.values())


def create_DAG(joblist):  # List[Job]
    G = nx.DiGraph()
    for job in joblist:
        G.add_node(job, weight=job.get_processing_time())
        for precendent_job in job.dependencies:
            G.add_edge(precendent_job, job,
                       weight=precendent_job.get_processing_time())
    return G


def Get_machines_number(DAG: nx.DiGraph):
    critical_path = nx.dag_longest_path(DAG)
    Tc = sum(map(lambda x: x.get_processing_time(), critical_path))
    T = sum(map(lambda x: x.get_processing_time(), DAG.nodes))
    return max(2, floor(T/Tc))


if __name__ == "__main__":
    path = "./Graphs/MediumComplex.json"
    DAG = create_DAG(import_graph(path))
    print(Get_machines_number(DAG))

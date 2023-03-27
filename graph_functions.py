import networkx as nx
from Job import Job
import json

## Importing from json file and preprocessing
def convert_to_seconds(ch):
    hh, mm, ss = ch.split(':')
    return 3600*int(hh) + 60*int(mm) + float(ss)

def import_graph(filepath: str) -> list[Job]:
    with open(filepath) as data:
        contents = data.read()
    contents = json.loads(contents)
    
    temp_job_dict = {int(node) : Job(int(node)) for node in contents['nodes'].keys()}
    
    for node, value in contents['nodes'].items():
        node = int(node)
        temp_job_dict[node].processing_time = convert_to_seconds(value["Data"])
        temp_job_dict[node].dependencies = [temp_job_dict[node] for node in value["Dependencies"]]
    return list(temp_job_dict.values())

def create_DAG(joblist : list[Job]):
    G = nx.DiGraph()
    G.add_nodes_from(joblist)
    for job in joblist:
        for precendent_job in job.dependencies:
            G.add_edge(precendent_job, job, weight = precendent_job.get_processing_time())
    return G
import numpy as np
from Job import Job
from Machine import Machine


def procces_visibilty_func(job_selected: Job):
    return job_selected.get_processing_time()


def greater_work_free(job_selected: Job):
    return job_selected.get_processing_time() + max([child_job.get_processing_time() for child_job in job_selected.get_dependencies()])

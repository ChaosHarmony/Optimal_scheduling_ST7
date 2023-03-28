import numpy as np
from Job import Job
from Machine import Machine


def procces_visibilty_func(job_selected: Job):
    return 1/job_selected.get_processing_time()


def greater_work_free(job_selected: Job):
    if job_selected.get_dependencies() == []:
        return job_selected.get_processing_time()
    else:
        return job_selected.get_processing_time() + max([child_job.get_processing_time() for child_job in job_selected.get_dependencies()])


def gwf_norm(job_selected: Job):
    if job_selected.get_dependencies() == []:
        return job_selected.get_processing_time()
    else:
        return job_selected.get_processing_time() + max([child_job.get_processing_time() for child_job in job_selected.get_dependencies()])

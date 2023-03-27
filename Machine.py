from Job import Job
from typing import *

class Machine:
    id = 0
    schedule = None # list[(Job, float, float)]
    jobs_performed : int = 0
    current_job_end_time = 0.0
    
    def __init__(self, id):
        self.id = id
        self.schedule = []
    def __repr__(self):
        # return f"M{self.id}: {list(map(lambda x: x[0], self.schedule))}"
        return f"M{self.id}: {self.schedule}"
        # return f"M{self.id}"
    
    def get_schedule(self):
        return self.schedule
    
    def perform_job(self, job: Job, completed_jobs: dict):
        self.jobs_performed += 1
        jobs_details = {}
        jobs_details["Machine"] = self
        end_times_of_precedent_jobs = list(map(lambda x: completed_jobs[x]["end_time"] ,filter(lambda x: x in completed_jobs, job.dependencies)))
        
        start_time : float = max(end_times_of_precedent_jobs + [self.current_job_end_time])
        jobs_details["start_time"] = start_time
        end_time: float  = start_time + job.get_processing_time()
        jobs_details["end_time"] = end_time
        self.current_job_end_time = end_time
        
        self.schedule.append((job, start_time, end_time))
        completed_jobs[job] = jobs_details
        
        
    def completion_time(self):
        return self.current_job_end_time
    
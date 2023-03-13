from Job import Job

class Machine:
    id = 0
    schedule : list[(Job, float, float)] = None
    jobs_performed : int = 0
    current_job_end_time : float = 0.0
    
    def __init__(self, id):
        self.id = id
        self.schedule = []
    def __repr__(self):
        # return f"M{self.id}: {list(map(lambda x: x[0], self.schedule))}"
        return f"M{self.id}: {self.schedule}"
    
    def get_schedule(self):
        return self.schedule
    
    def perform_job(self, job: Job):
        self.jobs_performed += 1
        end_times_of_precedent_jobs = [prec_job.time_completed for prec_job in job.dependencies]
        # print(self.id,end_times_of_precedent_jobs, self.current_job_end_time)
        start_time : float = max(end_times_of_precedent_jobs + [self.current_job_end_time])
        end_time: float  = start_time + job.get_processing_time()
        self.current_job_end_time = end_time
        job.set_time_completed(end_time)
        # print(self.id, job)
        self.schedule.append((job, start_time, end_time))
        
    def completion_time(self):
        return self.current_job_end_time
    
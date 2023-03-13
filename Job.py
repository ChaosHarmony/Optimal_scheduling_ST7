class Job:
    num: int = 0
    processing_time: float = 0.0
    dependencies: list = []
    time_completed: float = None
    
    def __init__(self, num, processing_time, dependencies):
        self.num = num
        self.processing_time = processing_time
        self.dependencies = dependencies
    
    def __init__(self, num):
        self.num = num
        
    def __repr__(self):
        return f"Job {self.num}"
    
    def get_processing_time(self):
        return self.processing_time
    
    def get_dependencies(self):
        return self.dependencies
    
    def set_time_completed(self, time_completed: float):
        self.time_completed = time_completed
    
    def reset_time_completed(self):
        self.time_completed = 0.0
class Job:
    def __init__(self, id, arrival_time, burst_time):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.current_queue = 0#for MLFQ
        self.vruntime = 0  # CFS-specific

    def __repr__(self):
        return f"Job(id={self.id}, arrival={self.arrival_time}, burst={self.burst_time})"
import Job
def FCFSScheduler(jobs: Job):
    # Geliş zamanına göre sırala
    jobs.sort(key=lambda job: job.arrival_time)

    time = 0
    for job in jobs:
        if time < job.arrival_time:
            time = job.arrival_time
        job.start_time = time
        time += job.burst_time
        job.remaining_time = 0
        job.completion_time = time

    return jobs
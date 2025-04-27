import heapq

def CFSScheduler(jobs, time_quantum=2):
    time = 0
    jobs = sorted(jobs, key=lambda job: job.arrival_time)
    job_index = 0
    ready_queue = []
    completed_jobs = []

    while job_index < len(jobs) or ready_queue:
        # Add new arriving jobs
        while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
            heapq.heappush(ready_queue, (jobs[job_index].vruntime, jobs[job_index].id, jobs[job_index]))
            job_index += 1

        if ready_queue:
            _, _, current_job = heapq.heappop(ready_queue)

            if current_job.start_time is None:
                current_job.start_time = time

            exec_time = min(time_quantum, current_job.remaining_time)
            time += exec_time
            current_job.remaining_time -= exec_time
            current_job.vruntime += exec_time  # Increase virtual runtime proportional to execution

            # New arrivals during execution
            while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
                heapq.heappush(ready_queue, (jobs[job_index].vruntime, jobs[job_index].id, jobs[job_index]))
                job_index += 1

            if current_job.remaining_time == 0:
                current_job.completion_time = time
                completed_jobs.append(current_job)
            else:
                heapq.heappush(ready_queue, (current_job.vruntime, current_job.id, current_job))

        else:
            # CPU idle
            time += 1

    return completed_jobs
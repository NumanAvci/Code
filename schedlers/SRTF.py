from collections import deque
import heapq

def SRTFScheduler(jobs, time_quantum=4):
    time = 0
    jobs = sorted(jobs, key=lambda job: job.arrival_time)
    job_index = 0
    ready_queue = []
    completed_jobs = []

    while job_index < len(jobs) or ready_queue:
        # Add jobs that have arrived
        while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
            heapq.heappush(ready_queue, (jobs[job_index].remaining_time, jobs[job_index].id, jobs[job_index]))
            job_index += 1

        if ready_queue:
            _, _, current_job = heapq.heappop(ready_queue)

            if current_job.start_time is None:
                current_job.start_time = time

            exec_time = min(time_quantum, current_job.remaining_time)
            time += exec_time
            current_job.remaining_time -= exec_time

            # New jobs might arrive while executing
            while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
                heapq.heappush(ready_queue, (jobs[job_index].remaining_time, jobs[job_index].id, jobs[job_index]))
                job_index += 1

            if current_job.remaining_time == 0:
                current_job.completion_time = time
                completed_jobs.append(current_job)
            else:
                # Still work to do, push back into ready queue
                heapq.heappush(ready_queue, (current_job.remaining_time, current_job.id, current_job))

        else:
            # CPU is idle, fast-forward time
            time += 1

    return completed_jobs



def min_response_time_scheduler(jobs):
    import copy
    jobs = copy.deepcopy(jobs)
    time = 0
    scheduled_jobs = []
    completed_jobs = []

    while len(completed_jobs) < len(jobs):
        # Hazır işlerin listesi
        ready_jobs = [job for job in jobs if job.arrival_time <= time and job not in completed_jobs]

        if ready_jobs:
            # Response Time minimize etmek için: Arrival time'ı en küçük olanı seç
            # (yeni gelenleri hızlı başlatmak mantıklı)
            ready_jobs.sort(key=lambda job: job.arrival_time)
            current_job = ready_jobs[0]

            if current_job.start_time is None:
                current_job.start_time = time

            time += current_job.burst_time
            current_job.completion_time = time
            completed_jobs.append(current_job)

        else:
            # CPU idle
            time += 1

    return completed_jobs


def min_turnaround_time_scheduler(jobs):
    import copy
    jobs = copy.deepcopy(jobs)
    time = 0
    scheduled_jobs = []
    completed_jobs = []

    while len(completed_jobs) < len(jobs):
        # Hazır işlerin listesi
        ready_jobs = [job for job in jobs if job.arrival_time <= time and job not in completed_jobs]

        if ready_jobs:
            # Turnaround Time minimize etmek için: Burst time'ı en küçük olanı seç
            ready_jobs.sort(key=lambda job: job.burst_time)
            current_job = ready_jobs[0]

            if current_job.start_time is None:
                current_job.start_time = time

            time += current_job.burst_time
            current_job.completion_time = time
            completed_jobs.append(current_job)

        else:
            # CPU idle
            time += 1

    return completed_jobs
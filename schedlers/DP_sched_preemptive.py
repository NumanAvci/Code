import functools
import matplotlib.pyplot as plt
import random
import numpy as np

class Job:
    def __init__(self, id, arrival_time, burst_time, priority):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        #self.executed_intervals = []  # For Gantt chart
        self.priority = priority

    def __repr__(self):
        return f"Job(id={self.id}, arrival={self.arrival_time}, burst={self.burst_time})"

def preemptive_dp_scheduler(jobs, objective='turnaround', time_quantum=1):
    n = len(jobs)
    max_time = sum(job.burst_time for job in jobs) + max(job.arrival_time for job in jobs)
    state_cache = {}

    def dp(time, completed_mask, remaining_times):
        key = (time, completed_mask, tuple(remaining_times))
        if key in state_cache:
            return state_cache[key]

        if completed_mask == (1 << n) - 1:
            return 0, []

        min_cost = float('inf')
        best_schedule = []

        # Identify available jobs
        ready_jobs = [i for i in range(n) if not (completed_mask & (1 << i)) and jobs[i].arrival_time <= time and remaining_times[i] > 0]

        if not ready_jobs:
            # Jump to the next arrival
            next_arrival = min([jobs[i].arrival_time for i in range(n) if jobs[i].arrival_time > time], default=max_time)
            return dp(next_arrival, completed_mask, remaining_times)

        for i in ready_jobs:
            exec_time = min(time_quantum, remaining_times[i])
            new_remaining = list(remaining_times)
            new_remaining[i] -= exec_time
            new_time = time + exec_time
            new_completed = completed_mask

            if new_remaining[i] == 0:
                completion_time = new_time
                if objective == 'turnaround':
                    cost = completion_time - jobs[i].arrival_time
                elif objective == 'response':
                    cost = (time - jobs[i].arrival_time) if jobs[i].start_time is None else 0
                elif objective == 'waiting':
                    cost = (time - jobs[i].arrival_time) - (jobs[i].burst_time - new_remaining[i])
                else:
                    raise ValueError("Unknown objective")
                new_completed |= (1 << i)
            else:
                cost = 0

            next_cost, next_schedule = dp(new_time, new_completed, tuple(new_remaining))
            total_cost = cost + next_cost

            if total_cost < min_cost:
                min_cost = total_cost
                best_schedule = [(jobs[i], time, new_time)] + next_schedule

        state_cache[key] = (min_cost, best_schedule)
        return state_cache[key]

    init_remaining = tuple(job.burst_time for job in jobs)
    total_cost, schedule = dp(0, 0, init_remaining)

    print(f"Optimal Total {objective.capitalize()} Time (Preemptive) = {total_cost}")
    print("\nOptimal Job Schedule:")
    for job, start, finish in schedule:
        print(f"Job {job.id} : Start at {start}, Finish at {finish}")
        job.start_time =start
        job.completion_time = finish

    return schedule, jobs


def generate_random_jobs(n):
    jobs = []
    for i in range(1, n + 1):
        arrival_time = random.randint(0, 20)
        burst_time = random.randint(1, 10)
        job = Job(id=i, arrival_time=arrival_time, burst_time=burst_time, priority=1)
        jobs.append(job)
    jobs.sort(key=lambda job: job.arrival_time)
    return jobs

if __name__ == "__main__":
    random_jobs = generate_random_jobs(4)
    for job in random_jobs:
        print(f"Job {job.id} - Arrival: {job.arrival_time}, Burst: {job.burst_time}")

    print("\n--- Preemptive DP Scheduler (Min Turnaround Time) ---")
    schedule, _ = preemptive_dp_scheduler(random_jobs, objective='turnaround', time_quantum=2)


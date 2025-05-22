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
        self.current_queue = 0
        self.vruntime = 0
        self.priority = priority

    def __repr__(self):
        return f"Job(id={self.id}, arrival={self.arrival_time}, burst={self.burst_time})"

def dp_scheduler(jobs, objective='turnaround'):
    n = len(jobs)
    jobs = sorted(jobs, key=lambda job: job.arrival_time)

    @functools.lru_cache(maxsize=None)
    def dp(time, completed_mask):
        if completed_mask == (1 << n) - 1:
            return (0, [])

        min_cost = float('inf')
        best_schedule = []

        ready_jobs = [
            (i, jobs[i]) for i in range(n)
            if not (completed_mask & (1 << i)) and jobs[i].arrival_time <= time
        ]

        if not ready_jobs:
            next_arrival = min(
                jobs[i].arrival_time for i in range(n) if not (completed_mask & (1 << i))
            )
            return dp(next_arrival, completed_mask)

        for i, job in ready_jobs:
            start_time = max(time, job.arrival_time)
            completion_time = start_time + job.burst_time

            if objective == 'turnaround':
                cost = completion_time - job.arrival_time
            elif objective == 'response':
                cost = start_time - job.arrival_time
            elif objective == 'waiting':
                cost = start_time - job.arrival_time
            else:
                raise ValueError("Unknown objective")

            next_cost, next_schedule = dp(completion_time, completed_mask | (1 << i))
            total_cost = cost + next_cost

            if total_cost < min_cost:
                min_cost = total_cost
                best_schedule = [(job, start_time, completion_time)] + next_schedule

        return (min_cost, best_schedule)

    optimal_cost, schedule = dp(0, 0)

    print(f"Optimal Total {objective.capitalize()} Time = {optimal_cost}")
    print("\nOptimal Job Schedule:")
    for job, start, finish in schedule:
        print(f"Job {job.id} : Start at {start}, Finish at {finish}")
        job.start_time = start
        job.completion_time = finish

    return schedule, jobs

def dp_plot_gantt(schedule):
    fig, ax = plt.subplots(figsize=(12, 3))
    colors = {}
    for job, start, finish in schedule:
        if job.id not in colors:
            colors[job.id] = (random.random(), random.random(), random.random())
        ax.barh(y=job.id, width=finish - start, left=start, height=0.5, color=colors[job.id], edgecolor='black')
        ax.text(x=start + (finish - start) / 2, y=job.id, s=f"J{job.id}", va='center', ha='center', color='white')
    ax.set_xlabel('Time')
    ax.set_ylabel('Job ID')
    ax.set_title('Gantt Chart of Scheduled Jobs')
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.yticks([job.id for job, _, _ in schedule])
    plt.show()

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
    random_jobs = generate_random_jobs(5)
    for job in random_jobs:
        print(f"Job {job.id} - Arrival: {job.arrival_time}, Burst: {job.burst_time}")

    print("\n--- DP Scheduler (Min Turnaround Time) ---")
    schedule, _ = dp_scheduler(random_jobs, objective='turnaround')
    dp_plot_gantt(schedule)

    print("\n--- DP Scheduler (Min Response Time) ---")
    schedule, _ = dp_scheduler(random_jobs, objective='response')
    dp_plot_gantt(schedule)

    print("\n--- DP Scheduler (Min Waiting Time) ---")
    schedule, _ = dp_scheduler(random_jobs, objective='waiting')
    dp_plot_gantt(schedule)



'''
This dynamic programming (DP) algorithm addresses the optimal scheduling of jobs to minimize the total turnaround time. 
Each "state" in the DP is represented by two components:
(1) the current simulation time (`time`), and 
(2) a bitmask (`completed_mask`) indicating which jobs have been completed so far.

Given `n` jobs, the number of possible completed_mask values is `2^n`, since each job can either be completed (1) or not completed (0).
Thus, the total number of different sets of completed jobs is exponential in the number of jobs.

For each `completed_mask`, multiple different `time` values could theoretically occur, 
depending on the scheduling order. However, in this implementation, 
the time is only advanced under two conditions:
1. When a job is scheduled, the time jumps forward by the job’s burst time (execution time).
2. If no jobs are ready at the current time (i.e., no job has arrived yet), 
   the simulation time is advanced to the earliest upcoming arrival time among the uncompleted jobs.

Thanks to these time-jumping optimizations, 
the number of meaningful distinct `time` values is drastically reduced. 
Rather than progressing one unit at a time (which would be computationally infeasible), 
the simulation only processes important discrete time events: job arrivals and job completions.

At each DP state (given by a specific `time` and `completed_mask`), 
the algorithm iterates through all available jobs that have arrived (arrival_time <= current time) and are not yet completed.
For each such available job, it considers scheduling that job next, leading to a recursive call. 
Since there can be at most `n` available jobs at any state, 
the branching factor at each node is up to `n`.

Each recursive decision includes:
- Choosing a job,
- Advancing the time accordingly,
- Updating the `completed_mask`,
- Calculating the turnaround time contribution of that job,
- Recursing to solve the remaining subproblem optimally.

Therefore, the total time complexity of the algorithm is:

O(2^n * n^2)

Explanation:
- `2^n` accounts for all subsets of completed jobs,
- For each subset (completed_mask), we have at most `n` ready jobs to consider at each step,
- For each choice, the cost computation and state transition take `O(1)` time.

Thus, the overall complexity becomes `O(2^n * n^2)`, which is exponential in the number of jobs.
The space complexity is also `O(2^n * n)`, primarily due to memoization (caching of subproblem solutions).

Because of the exponential growth of the state space, 
this approach is only computationally feasible for small `n` (typically up to about 12–15 jobs). 
Beyond that, the algorithm becomes impractical without further optimizations such as pruning, 
state compression, or the use of approximate (heuristic) scheduling algorithms.

In summary, this dynamic programming formulation provides a complete and exact solution 
for minimizing total turnaround time, 
but it is only suitable for relatively small problem sizes due to its exponential time complexity.
'''


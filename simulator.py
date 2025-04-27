from schedlers.FCFS import FCFSScheduler
from schedlers.MLFQ import MLFQScheduler
from schedlers.SRTF import SRTFScheduler
from schedlers.CFS import CFSScheduler

from Job import Job

import copy
import matplotlib.pyplot as plt
import numpy as np
import random

def evaluate_scheduler(scheduler_func, jobs, scheduler_name, **kwargs):
    scheduled_jobs = scheduler_func(jobs, **kwargs)
    n = len(scheduled_jobs)

    total_response_time = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    for job in scheduled_jobs:
        response_time = job.start_time - job.arrival_time
        turnaround_time = job.completion_time - job.arrival_time
        waiting_time = turnaround_time - job.burst_time

        total_response_time += response_time
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time

    avg_response = total_response_time / n
    avg_turnaround = total_turnaround_time / n
    avg_waiting = total_waiting_time / n

    return {
        "Scheduler": scheduler_name,
        "Avg Response Time": avg_response,
        "Avg Turnaround Time": avg_turnaround,
        "Avg Waiting Time": avg_waiting
    }

def plot_scheduler_comparison(results):
    metrics = ["Avg Response Time", "Avg Turnaround Time", "Avg Waiting Time"]
    schedulers = [res["Scheduler"] for res in results]

    x = np.arange(len(schedulers))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, metric in enumerate(metrics):
        values = [res[metric] for res in results]
        ax.bar(x + i*width, values, width, label=metric)

    ax.set_xlabel("Schedulers")
    ax.set_ylabel("Average Time (ms)")
    ax.set_title("Scheduler Comparison")
    ax.set_xticks(x + width)
    ax.set_xticklabels(schedulers)
    ax.legend()
    ax.grid(axis='y')

    plt.tight_layout()
    plt.show()


def calculate_metrics(jobs, scheduler_name):
    total_response_time = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    for job in jobs:
        response_time = job.start_time - job.arrival_time
        turnaround_time = job.completion_time - job.arrival_time
        waiting_time = turnaround_time - job.burst_time

        total_response_time += response_time
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time

        print(f"Job {job.id}: Response={response_time}, Turnaround={turnaround_time}, Waiting={waiting_time}")

    n = len(jobs)
    print("\nAverages:")
    print(f"Avg Response Time = {total_response_time / n:.2f}")
    print(f"Avg Turnaround Time = {total_turnaround_time / n:.2f}")
    print(f"Avg Waiting Time = {total_waiting_time / n:.2f}")

    return {
        "Scheduler": scheduler_name,
        "Avg Response Time": total_response_time / n,
        "Avg Turnaround Time": total_turnaround_time / n,
        "Avg Waiting Time": total_waiting_time / n
    }


def generate_random_jobs(n):
    jobs = []
    for i in range(1, n + 1):
        arrival_time = random.randint(0, 20)
        burst_time = random.randint(1, 10)
        job = Job(id=i, arrival_time=arrival_time, burst_time=burst_time)
        jobs.append(job)
    
    # İstersen sıralı döndür: arrival_time'a göre
    jobs.sort(key=lambda job: job.arrival_time)
    return jobs


if __name__ == "__main__":
    jobs = generate_random_jobs(10)

    results = []
    print("FCFS Scheduler metrics")
    FCFS_scheduled_jobs = FCFSScheduler(copy.deepcopy(jobs))
    FCFS_results = calculate_metrics(FCFS_scheduled_jobs, "FCFS")
    results.append(FCFS_results)

    print("\n\nMLFQ Scheduler metrics")
    MLFQ_scheduled_jobs = MLFQScheduler(copy.deepcopy(jobs), queue_levels=3, time_quantums=[4, 8, None])
    MLFQ_results = calculate_metrics(MLFQ_scheduled_jobs, "MLFQ - QL:3,TQ:[4,8,]")
    results.append(MLFQ_results)

    MLFQ_scheduled_jobs = MLFQScheduler(copy.deepcopy(jobs), queue_levels=5, time_quantums=[2, 3, 4, 5, 6])
    MLFQ_results = calculate_metrics(MLFQ_scheduled_jobs, "MLFQ - QL:5,TQ:[2,3,4]")
    results.append(MLFQ_results)

    print("\n\nSRTF Scheduler metrics")
    SRTF_scheduled_jobs = SRTFScheduler(copy.deepcopy(jobs), time_quantum=3)
    SRTF_results = calculate_metrics(SRTF_scheduled_jobs, "SRTF - TQ:2")
    results.append(SRTF_results)
    SRTF_scheduled_jobs = SRTFScheduler(copy.deepcopy(jobs), time_quantum=4)
    SRTF_results = calculate_metrics(SRTF_scheduled_jobs, "SRTF - TQ:4")
    results.append(SRTF_results)

    print("\n\nCFS Scheduler metrics")
    CFS_scheduled_jobs = CFSScheduler(copy.deepcopy(jobs), time_quantum=2)
    CFS_results = calculate_metrics(CFS_scheduled_jobs, "CFS - TQ:2")
    results.append(CFS_results)
    CFS_scheduled_jobs = CFSScheduler(copy.deepcopy(jobs), time_quantum=4)
    CFS_results = calculate_metrics(CFS_scheduled_jobs, "CFS - TQ:4")
    results.append(CFS_results)

    #plot the results
    plot_scheduler_comparison(results) 
    plot_scheduler_comparison(results) 

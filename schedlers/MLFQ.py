from collections import deque

def MLFQScheduler(jobs, queue_levels=3, time_quantums=[4, 8, None]):
    time = 0
    queues = [deque() for _ in range(queue_levels)]
    jobs = sorted(jobs, key=lambda job: job.arrival_time)  # arrival time göre sırala
    job_index = 0
    completed_jobs = []

    while job_index < len(jobs) or any(queues):
        # Yeni gelen işleri ilk kuyruğa ekle
        while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
            queues[0].append(jobs[job_index])
            job_index += 1

        # Çalışacak iş bul
        current_job = None
        current_queue_level = None
        for level, queue in enumerate(queues):
            if queue:
                current_job = queue.popleft()
                current_queue_level = level
                break

        if current_job:
            if current_job.start_time is None:
                current_job.start_time = time

            quantum = time_quantums[current_queue_level]
            if quantum is None:
                # En düşük seviyede FCFS gibi çalış
                exec_time = current_job.remaining_time
            else:
                exec_time = min(quantum, current_job.remaining_time)

            time += exec_time
            current_job.remaining_time -= exec_time

            # Arada yeni işler gelirse onları ekleyelim
            while job_index < len(jobs) and jobs[job_index].arrival_time <= time:
                queues[0].append(jobs[job_index])
                job_index += 1

            if current_job.remaining_time == 0:
                current_job.completion_time = time
                completed_jobs.append(current_job)
            else:
                # Bir alt seviyeye düşür
                if current_queue_level + 1 < queue_levels:
                    current_job.current_queue += 1
                    queues[current_queue_level + 1].append(current_job)
                else:
                    # Zaten en alttaysa tekrar aynı kuyrukta kalır
                    queues[current_queue_level].append(current_job)

        else:
            # CPU boş, ileri sar
            time += 1

    return completed_jobs
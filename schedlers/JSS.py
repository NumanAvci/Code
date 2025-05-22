import heapq
import matplotlib.pyplot as plt

# -----------------------------
# Operation Class
# -----------------------------
class Operation:
    def __init__(self, job_id, op_index, machine_id, duration):
        self.job_id = job_id
        self.op_index = op_index
        self.machine_id = machine_id
        self.duration = duration
        self.start_time = None
        self.end_time = None

    def __repr__(self):
        return f"Job {self.job_id} - Op {self.op_index} (M{self.machine_id}, {self.duration})"


# -----------------------------
# Job Shop Scheduler
# -----------------------------
class JobShopScheduler:
    def __init__(self, job_operations):
        self.job_operations = job_operations
        self.num_jobs = len(job_operations)
        self.num_machines = max(m for ops in job_operations.values() for (m, _) in ops) + 1

        self.jobs = {
            job_id: [
                Operation(job_id, i, machine_id, duration)
                for i, (machine_id, duration) in enumerate(ops)
            ]
            for job_id, ops in job_operations.items()
        }

        self.machine_available_time = [0] * self.num_machines
        self.job_next_op_index = [0] * self.num_jobs
        self.job_available_time = [0] * self.num_jobs

        self.schedule = []

    def run(self):
        total_operations = sum(len(ops) for ops in self.job_operations.values())
        scheduled_ops = 0

        while scheduled_ops < total_operations:
            ready_ops = []

            for job_id in range(self.num_jobs):
                op_index = self.job_next_op_index[job_id]
                if op_index < len(self.jobs[job_id]):
                    op = self.jobs[job_id][op_index]
                    earliest_start = max(self.machine_available_time[op.machine_id],
                                         self.job_available_time[op.job_id])
                    heapq.heappush(ready_ops, (earliest_start, job_id, op))

            if ready_ops:
                start_time, _, selected_op = heapq.heappop(ready_ops)
                selected_op.start_time = start_time
                selected_op.end_time = start_time + selected_op.duration

                self.machine_available_time[selected_op.machine_id] = selected_op.end_time
                self.job_available_time[selected_op.job_id] = selected_op.end_time
                self.job_next_op_index[selected_op.job_id] += 1

                self.schedule.append(selected_op)
                scheduled_ops += 1

    def print_schedule(self):
        print("Scheduled Operations:\n")
        for op in sorted(self.schedule, key=lambda x: x.start_time):
            print(
                f"Job {op.job_id} - Op {op.op_index} | "
                f"Machine {op.machine_id} | Start: {op.start_time} | End: {op.end_time}"
            )

    def get_makespan(self):
        return max(op.end_time for op in self.schedule)


# -----------------------------
# Gantt Chart Plot Function
# -----------------------------
def plot_gantt_chart(schedule):
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:gray']
    machine_y = {}

    for op in schedule:
        m_id = op.machine_id
        job_label = f"Job {op.job_id}-Op {op.op_index}"
        color = colors[op.job_id % len(colors)]

        if m_id not in machine_y:
            machine_y[m_id] = len(machine_y)

        y = machine_y[m_id]
        ax.barh(y=y,
                width=op.duration,
                left=op.start_time,
                height=0.5,
                align='center',
                color=color,
                edgecolor='black')
        ax.text(op.start_time + op.duration / 2, y,
                job_label,
                ha='center', va='center', color='white', fontsize=8)

    ax.set_yticks(list(machine_y.values()))
    ax.set_yticklabels([f"Machine {m}" for m in machine_y.keys()])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for Job Shop Scheduling")
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()


# -----------------------------
# Example: 5 Jobs, 3 Machines
# -----------------------------
job_operations = {
    0: [(0, 4), (1, 3), (2, 2)],
    1: [(1, 2), (0, 1), (2, 4)],
    2: [(2, 3), (1, 5), (0, 2)],
    3: [(0, 2), (2, 1), (1, 3)],
    4: [(1, 4), (2, 3), (0, 1)],
}

scheduler = JobShopScheduler(job_operations)
scheduler.run()
scheduler.print_schedule()

print(f"\n🧮 Makespan: {scheduler.get_makespan()}")

# Show Gantt chart
plot_gantt_chart(scheduler.schedule)

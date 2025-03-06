import matplotlib.pyplot as plt
import numpy as np

def fifo(processes):
    processes.sort(key=lambda x: x[1])  # Ordenar por tiempo de llegada
    gantt = []
    current_time = 0
    waiting_times = []
    turnaround_times = []
    
    for process in processes:
        pid, arrival, burst, priority = process
        start_time = max(current_time, arrival)
        end_time = start_time + burst
        waiting_times.append(start_time - arrival)
        turnaround_times.append(end_time - arrival)
        gantt.append((pid, start_time, end_time))
        current_time = end_time
    
    return gantt, waiting_times, turnaround_times

def sjf(processes):
    print("eejcutando sjf")
    """
    processes: lista de tuplas (pid, arrival_time, burst_time)
    Retorna:
      - results: lista de tuplas (pid, start_time, completion_time, TAT, WT)
      - avg_waiting_time
      - avg_turnaround_time
    """
    # 1. Ordenar inicialmente por tiempo de llegada
    processes.sort(key=lambda x: x[1])

    n = len(processes)
    completed = 0         # Número de procesos completados
    current_time = 0      # Tiempo actual
    visited = [False]*n   # Para marcar procesos ya ejecutados
    results = []
    total_wt = 0
    total_tat = 0

    while completed < n:
        # 2. Buscar todos los procesos que ya llegaron hasta current_time y no estén completados
        idx_candidates = [
            i for i in range(n)
            if (processes[i][1] <= current_time and not visited[i])
        ]

        if not idx_candidates:
            # Si no hay procesos disponibles, avanzar el tiempo hasta la llegada del siguiente
            next_arrival = min([p[1] for p in processes if not visited[processes.index(p)]])
            current_time = next_arrival
            continue

        # 3. De los procesos candidatos, elegir el de menor ráfaga
        idx_sjf = min(idx_candidates, key=lambda i: processes[i][2])
        pid, arrival, burst = processes[idx_sjf]

        # 4. Ejecutar el proceso (no se interrumpe, es SJF no apropiativo)
        start_time = max(current_time, arrival)
        completion_time = start_time + burst
        tat = completion_time - arrival               # Turnaround time
        wt = start_time - arrival                     # Waiting time

        # 5. Almacenar resultados
        results.append((pid, start_time, completion_time, tat, wt))
        total_wt += wt
        total_tat += tat
        visited[idx_sjf] = True  # Marcar el proceso como completado
        completed += 1

        # 6. Avanzar el tiempo
        current_time = completion_time

    avg_wt = total_wt / n
    avg_tat = total_tat / n

    return results, avg_wt, avg_tat


def priority(processes):
    """
    Simulación por Prioridad no apropiativa:
    - Se ejecuta primero el proceso disponible con menor valor en "priority" (mayor prioridad).
    - Cada proceso tiene: id, arrival, burst y priority.
    """
    processes.sort(key=lambda p: p["arrival"])  # Orden inicial por llegada
    n = len(processes)
    current_time = 0
    bars = []  # [(process_id, start_time, duration)]
    waiting_times = {}  # {process_id: waiting_time}
    turnaround_times = {}  # {process_id: turnaround_time}
    processes_copy = processes.copy()

    while processes_copy:
        # Filtrar procesos que ya llegaron al instante actual
        available = [p for p in processes_copy if p["arrival"] <= current_time]

        # Si no hay procesos disponibles, avanzar al siguiente que llegue
        if not available:
            current_time = min(p["arrival"] for p in processes_copy)
            available = [p for p in processes_copy if p["arrival"] <= current_time]

        # Seleccionar el proceso con **mayor prioridad** (menor número en "priority")
        p = min(available, key=lambda p: p["priority"])
        processes_copy.remove(p)

        start = max(current_time, p["arrival"])
        end = start + p["burst"]
        bars.append((p["id"], start, end - start))

        waiting_times[p["id"]] = start - p["arrival"]
        turnaround_times[p["id"]] = end - p["arrival"]
        current_time = end  # Avanzar el tiempo al final del proceso

    # Cálculo de promedios
    avg_wt = sum(waiting_times.values()) / n
    avg_tat = sum(turnaround_times.values()) / n

    return bars, waiting_times, turnaround_times, avg_wt, avg_tat


def plot_gantt_chart(gantt, title):
    fig, ax = plt.subplots(figsize=(10, 3))
    y_labels = []
    for idx, (pid, start, end) in enumerate(gantt):
        ax.barh(pid, end - start, left=start, height=0.5, align='center')
        ax.text((start + end) / 2, pid, str(pid), va='center', ha='center', color='white', fontsize=10, fontweight='bold')
        y_labels.append(str(pid))
    
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Procesos')
    ax.set_title(title)
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    ax.grid(True)
    plt.show()

processes = [
    (1, 0, 7, 3),
    (2, 2, 4, 1),
    (3, 4, 1, 4),
    (4, 5, 4, 2)
]

gantt_fifo, wt_fifo, tat_fifo = fifo(processes.copy())
gantt_sjf, wt_sjf, tat_sjf = sjf(processes.copy())
gantt_priority, wt_priority, tat_priority = priority(processes.copy())

plot_gantt_chart(gantt_fifo, "Diagrama de Gantt - FIFO")
plot_gantt_chart(gantt_sjf, "Diagrama de Gantt - SJF")
plot_gantt_chart(gantt_priority, "Diagrama de Gantt - Prioridad")

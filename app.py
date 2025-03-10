import matplotlib
matplotlib.use('Agg')  # Evita errores de GUI
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def simulate_fifo(processes):
    processes.sort(key=lambda p: p["arrival"])
    start_time = 0
    bars = []
    waiting_times = {}
    turnaround_times = {}
    
    for process in processes:
        start = max(start_time, process["arrival"])
        end = start + process["burst"]
        bars.append((process["id"], start, end - start))
        waiting_times[process["id"]] = start - process["arrival"]
        turnaround_times[process["id"]] = end - process["arrival"]
        start_time = end

    avg_waiting_time = sum(waiting_times.values()) / len(processes)
    avg_turnaround_time = sum(turnaround_times.values()) / len(processes)
    return bars, waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time

def simulate_sjf(processes):
    processes.sort(key=lambda p: p["arrival"])  # Ordenar por tiempo de llegada
    n = len(processes)
    current_time = 0
    bars = []
    waiting_times = {}
    turnaround_times = {}
    remaining_processes = processes.copy()

    while remaining_processes:
        # Filtrar procesos disponibles
        available = [p for p in remaining_processes if p["arrival"] <= current_time]

        # Si no hay procesos listos, avanzar el tiempo al siguiente proceso más cercano
        if not available:
            current_time = min(p["arrival"] for p in remaining_processes)
            available = [p for p in remaining_processes if p["arrival"] <= current_time]

        # Elegir el proceso con menor ráfaga de CPU
        p = min(available, key=lambda p: p["burst"])
        remaining_processes.remove(p)

        # Determinar inicio y fin del proceso en el diagrama de Gantt
        start = max(current_time, p["arrival"])
        end = start + p["burst"]
        bars.append((p["id"], start, end - start))

        # Calcular tiempos de espera y retorno
        waiting_times[p["id"]] = start - p["arrival"]
        turnaround_times[p["id"]] = end - p["arrival"]

        # Actualizar tiempo actual
        current_time = end

    avg_waiting_time = sum(waiting_times.values()) / n
    avg_turnaround_time = sum(turnaround_times.values()) / n
    return bars, waiting_times, turnaround_times, avg_waiting_time, avg_turnaround_time

def simulate_priority(processes):
    processes.sort(key=lambda p: p["arrival"])
    n = len(processes)
    current_time = 0
    bars = []
    waiting_times = {}
    turnaround_times = {}
    processes_copy = processes.copy()

    while processes_copy:
        available = [p for p in processes_copy if p["arrival"] <= current_time]
        if not available:
            current_time = min(p["arrival"] for p in processes_copy)
            available = [p for p in processes_copy if p["arrival"] <= current_time]
        p = min(available, key=lambda p: p["priority"])
        processes_copy.remove(p)
        start = max(current_time, p["arrival"])
        end = start + p["burst"]
        bars.append((p["id"], start, end - start))
        waiting_times[p["id"]] = start - p["arrival"]
        turnaround_times[p["id"]] = end - p["arrival"]
        current_time = end

    avg_wt = sum(waiting_times.values()) / n
    avg_tat = sum(turnaround_times.values()) / n
    return bars, waiting_times, turnaround_times, avg_wt, avg_tat

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        data = request.json
        processes = data["processes"]
        algorithm = data["algorithm"].strip().upper()

        if algorithm == "FIFO":
            bars, waiting_times, turnaround_times, avg_wt, avg_tat = simulate_fifo(processes)
        elif algorithm == "SJF":
            bars, waiting_times, turnaround_times, avg_wt, avg_tat = simulate_sjf(processes)
        elif algorithm in ["PRIORITY", "PRIORIDAD"]:
            bars, waiting_times, turnaround_times, avg_wt, avg_tat = simulate_priority(processes)
        else:
            return jsonify({"error": f"Algoritmo no reconocido: {algorithm}"}), 400

        if not bars:
            print("No se encontraron procesos")
        else:
            print("bars contiene datos")
        sys.stdout.flush()

        fig, ax = plt.subplots(figsize=(10, 3))
        labels = []
        for i, (pid, start, duration) in enumerate(bars):
            ax.barh(i, duration, left=start, color="blue", edgecolor="black")
            labels.append(pid)
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Procesos")
        ax.grid(True, linestyle="--", alpha=0.5)

        os.makedirs("static", exist_ok=True)
        image_path = "static/gantt_chart.png"
        if os.path.exists(image_path):
            os.remove(image_path)
            print("Se ha eliminado el archivo anterior")
            sys.stdout.flush()

        plt.savefig(image_path)
        print("Gantt chart guardado en")
        sys.stdout.flush()
        plt.close(fig)

        return jsonify({
            "image_path": "/" + image_path,
            "waiting_times": waiting_times,
            "turnaround_times": turnaround_times,
            "avg_waiting_time": avg_wt,
            "avg_turnaround_time": avg_tat
        })
    
    except Exception as e:
        print("Error:", e)
        sys.stdout.flush()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

import matplotlib
matplotlib.use('Agg')  # Evita errores de GUI
import matplotlib.pyplot as plt
import numpy as np
import os
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
        p = min(available, key=lambda p: p["burst"])
        processes_copy.remove(p)
        start = max(current_time, p["arrival"])
        end = start + p["burst"]
        bars.append((p["id"], start, end - start))
        waiting_times[p["id"]] = start - p["arrival"]
        turnaround_times[p["id"]] = end - p["arrival"]
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
        plt.savefig(image_path)
        plt.close(fig)

        return jsonify({
            "image_path": "/" + image_path,
            "waiting_times": waiting_times,
            "turnaround_times": turnaround_times,
            "avg_waiting_time": avg_wt,
            "avg_turnaround_time": avg_tat
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

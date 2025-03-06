import matplotlib.pyplot as plt

def dibujar_gantt(procesos, nombre_archivo="static/images/gantt_chart.png"):
    fig, ax = plt.subplots(figsize=(10, 4))

    # Definir los niveles en el eje Y para cada proceso
    procesos_unicos = sorted(set(p['id'] for p in procesos))
    niveles = {proceso: i + 1 for i, proceso in enumerate(procesos_unicos)}

    # Dibujar cada proceso como una línea horizontal
    for proceso in procesos:
        inicio = proceso['start']
        fin = proceso['start'] + proceso['burst']
        ax.hlines(y=niveles[proceso['id']], xmin=inicio, xmax=fin, linewidth=5, color='blue')

    # Etiquetas y configuración del gráfico
    ax.set_yticks(list(niveles.values()))
    ax.set_yticklabels(list(niveles.keys()))
    ax.set_xticks(range(21))  # Tiempos del 0 al 20
    ax.set_xlim(0, 20)  # Ajustar el eje X
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title("Diagrama de Gantt")

    # Guardar la imagen
    plt.savefig(nombre_archivo)
    plt.close(fig)

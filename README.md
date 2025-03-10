Simulador de Algoritmos de Planificación
Este proyecto es una aplicación web que permite simular diferentes algoritmos de planificación de procesos, generando un diagrama de Gantt y calculando tiempos de espera y turnaround.

Ejecutarlo:
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>

Instalar dependencias:
pip install -r requirements.txt

Ejecutar app:
python app.py
http://127.0.0.1:5000

He usado Flask(Framework web en python), Matplotlib(para el diagrma de gantt), HTML, CSS, JavaScript(Interfaz de usuario)

Características
Simulación de múltiples algoritmos de planificación
Carga de procesos manualmente
Generación automática del diagrama de Gantt
Cálculo de tiempos de espera y turnaround

Estructura del Proyecto
/static  
  ├── styles.css  # Estilos  
  ├── script.js   # Funcionalidad del frontend  
/templates  
  ├── index.html  # Página principal  
app.py            # Código principal de la aplicación  
requirements.txt  # Dependencias necesarias  
README.md         # Documentación  

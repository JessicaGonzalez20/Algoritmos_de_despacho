document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM completamente cargado");

    //Pantalla de carga
    setTimeout(function () {
        let preloader = document.querySelector(".loading-area");
        let content = document.querySelector(".contenido");

        if (preloader) preloader.style.opacity = "0";

        setTimeout(function () {
            if (preloader) preloader.style.display = "none";
            if (content) content.classList.add("mostrar");
        }, 500);
    }, 3000);

    //Verifica si el formulario existe antes de agregar el event listener
    let form = document.getElementById("scheduler-form");
    if (form) {
        console.log("Formulario encontrado");
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            ejecutarSimulacion();
        });
    } else {
        console.error("❌ ERROR: No se encontró #scheduler-form en el DOM");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("newSimulation").addEventListener("click", function() {
        location.reload();
    });
});

function ejecutarSimulacion() {
    let algorithm = document.getElementById("algorithm").value;
    let rows = document.querySelectorAll("#process-table tbody .process-row");
    let processes = [];

    for (let row of rows) {
        let id = row.cells[0].querySelector("input").value.trim();
        let arrival = parseInt(row.cells[1].querySelector("input").value);
        let burst = parseInt(row.cells[2].querySelector("input").value);
        let priorityInput = row.cells[3].querySelector("input");
        let priority = priorityInput ? parseInt(priorityInput.value) : null;
        
        if (!id || isNaN(arrival) || isNaN(burst) || (priorityInput && isNaN(priority))) {
            alert("Por favor, complete todos los campos correctamente.");
            return;
        }

        processes.push({ id, arrival, burst, priority });
    }
    
    fetch("/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm: algorithm.trim().toUpperCase(), processes })
    })
    .then(response => response.json())
    .then(data => {
        let img = document.getElementById("ganttChart");
        let timestamp = new Date().getTime(); 
        img.src = data.image_path + "?t=" + timestamp;
        img.style.display = "block";

        let resultsDiv = document.getElementById("results");
        let resultsHTML = `<h3>Tiempos de los Procesos</h3>
            <table border="1" class="styled-table">
                <tr><th>ID</th><th>Tiempo de Espera</th><th>Tiempo en Sistema</th></tr>`;

        for (let id in data.waiting_times) {
            resultsHTML += `<tr><td>${id}</td><td>${data.waiting_times[id]}</td><td>${data.turnaround_times[id]}</td></tr>`;
        }

        resultsHTML += `</table>`;
        resultsHTML += `<p><strong>Tiempo de Espera Promedio:</strong> ${data.avg_waiting_time}</p>`;
        resultsHTML += `<p><strong>Tiempo de Sistema Promedio:</strong> ${data.avg_turnaround_time}</p>`;

        resultsDiv.innerHTML = resultsHTML;
    })
    .catch(error => console.error("Error en la simulación:", error));
}

function addProcess() {
    const table = document.getElementById("process-table").getElementsByTagName('tbody')[0];
    const row = table.insertRow();
    row.classList.add("process-row");

    row.innerHTML = `
        <td><input type="text" class="id" required placeholder="ID"></td>
        <td><input type="number" class="arrival" required min="0" placeholder="Llegada"></td>
        <td><input type="number" class="burst" required min="1" placeholder="Ráfaga"></td>
        <td><input type="number" class="priority" required min="1" placeholder="Prioridad"></td>
        <td><button type="button" class="delete-btn" onclick="deleteProcess(this)">Eliminar</button></td>
    `;
}

function deleteProcess(button) {
    button.parentElement.parentElement.remove();
}





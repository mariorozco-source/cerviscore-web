// Global State
let currentCategory = 'primaria_baja';

document.addEventListener('DOMContentLoaded', () => {
    console.log("CerviScore Initialized");
    
    // Check if there is a hash for navigation, else load default
    const hash = window.location.hash;
    if(hash && hash.includes('category=')) {
        const cat = hash.split('category=')[1];
        if(cat) currentCategory = cat;
    }

    // Load initial data
    loadCategoryData(currentCategory);
    setupTabListeners();
    setupInputListener();
});

function setupTabListeners() {
    const tabs = document.querySelectorAll('.tournament-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            
            // UI Update
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Logic Update
            currentCategory = tab.dataset.category;
            loadCategoryData(currentCategory);
        });
    });
}

async function loadCategoryData(category) {
    const tableBody = document.querySelector('#standings-table tbody');
    const scorersContainer = document.querySelector('#top-scorers');
    
    // Loading State
    tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 2rem;">Cargando datos...</td></tr>';
    scorersContainer.innerHTML = '<p style="text-align:center; color: #fff;">Cargando goleadores...</p>';

    try {
        const response = await fetch(`/api/standings/${category}`);
        if (!response.ok) throw new Error('Error al cargar datos');
        
        const data = await response.json();
        renderStandings(data.posiciones);
        renderScorers(data.goleadores);
        
    } catch (error) {
        console.error(error);
        tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center; color: red;">Error al cargar los datos. Intenta recargar.</td></tr>';
    }
}

function renderStandings(standings) {
    const tableBody = document.querySelector('#standings-table tbody');
    tableBody.innerHTML = '';

    standings.forEach((team, index) => {
        const row = document.createElement('tr');
        
        // Color coding for top positions (Gold, Silver, Bronze)
        let rankClass = '';
        if (index === 0) rankClass = 'rank-1';
        if (index === 1) rankClass = 'rank-2';
        if (index === 2) rankClass = 'rank-3';

        row.innerHTML = `
            <td class="team-name ${rankClass}">${team.equipo}</td>
            <td>${team.pj}</td>
            <td>${team.pg}</td>
            <td>${team.pe}</td>
            <td>${team.pp}</td>
            <td>${team.GF || 0}</td>
            <td>${team.GC || 0}</td>
            <td>${(team.GF||0) - (team.GC||0)}</td>
            <td class="points">${team.pts}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderScorers(scorers) {
    const container = document.querySelector('#top-scorers');
    container.innerHTML = '';

    if(!scorers || scorers.length === 0) {
        container.innerHTML = '<p style="color: grey;">No hay datos de goleadores aún.</p>';
        return;
    }

    scorers.forEach((player, index) => {
        const card = document.createElement('div');
        card.className = 'player-card fade-in';
        card.style.animationDelay = `${index * 0.1}s`; // Staggered animation
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; gap: 15px;">
                <span class="rank">${index + 1}</span>
                <div class="player-info">
                    <h3>${player.nombre}</h3>
                    <span class="course">${player.curso}</span>
                </div>
            </div>
            <div class="goals">
                <span>${player.goles}</span>
                <small>Goles</small>
            </div>
        `;
        container.appendChild(card);
    });
}

// AI Chat Functionality
function setupInputListener() {
    const input = document.getElementById('ai-input');
    if(!input) return;
    
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            askAI();
        }
    });
}

// Expose askAI globally so the button onclick works
window.askAI = async function() {
    const input = document.getElementById('ai-input');
    const responseBox = document.getElementById('ai-response');
    const contentBox = document.getElementById('ai-content');
    const question = input.value.trim();

    if (!question) return;

    // UI Loading
    responseBox.style.display = 'block';
    contentBox.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Analizando jugadas...';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: question })
        });
        
        const data = await response.json();
        
        // Typewriter Effect
        typeWriterEffect(data.respuesta, contentBox);
        
    } catch (error) {
        contentBox.innerHTML = 'Error al conectar con el asistente. Intenta de nuevo.';
    }
}

function typeWriterEffect(text, element) {
    element.innerHTML = '';
    let i = 0;
    const speed = 20; // ms per char
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

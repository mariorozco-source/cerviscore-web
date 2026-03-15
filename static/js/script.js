document.addEventListener('DOMContentLoaded', () => {
    setupSmoothNavigation();
    setupTournamentTabs();
    setupInputListener();
});

function setupSmoothNavigation() {
    const links = document.querySelectorAll('.nav-item[href^="#"]');
    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            const targetSelector = link.getAttribute('href');
            if (!targetSelector || targetSelector === '#') return;

            const target = document.querySelector(targetSelector);
            if (!target) return;

            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

function setupTournamentTabs() {
    const tabs = document.querySelectorAll('.tournament-tab');
    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            tabs.forEach((t) => t.classList.remove('active'));
            tab.classList.add('active');
            // No prevenimos navegación: Flask carga el torneo seleccionado.
        });
    });
}

function setupInputListener() {
    const input = document.getElementById('ai-input');
    const button = document.getElementById('ai-btn');

    if (button) {
        button.addEventListener('click', askAI);
    }

    if (!input) return;
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            askAI();
        }
    });
}

window.askAI = async function askAI() {
    const input = document.getElementById('ai-input');
    const responseBox = document.getElementById('ai-response');

    if (!input || !responseBox) return;

    const question = input.value.trim();
    if (!question) return;

    responseBox.classList.remove('hidden');
    responseBox.classList.add('loading');
    responseBox.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Analizando estadísticas...';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: question })
        });

        if (!response.ok) {
            throw new Error('Respuesta inválida del servidor');
        }

        const data = await response.json();
        responseBox.classList.remove('loading');
        typeWriterEffect(data.respuesta || 'No hubo respuesta de la IA.', responseBox);
    } catch (error) {
        responseBox.classList.remove('loading');
        responseBox.textContent = 'Error al conectar con el asistente. Intenta de nuevo.';
    }
};

function typeWriterEffect(text, element) {
    element.textContent = '';
    let i = 0;
    const speed = 18;

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i += 1;
            setTimeout(type, speed);
        }
    }

    type();
}

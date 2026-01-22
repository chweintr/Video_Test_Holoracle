/**
 * ECHOES OF INDIANA - KIOSK MENU
 * Handles persona selection and communication with main display
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Kiosk] Initialized');
    
    // Splash screen click handler
    const splash = document.getElementById('splash-screen');
    if (splash) {
        splash.addEventListener('click', () => {
            console.log('[Kiosk] Splash dismissed');
            splash.classList.add('hidden');
        });
    }
    
    // About modal handlers
    const aboutBtn = document.getElementById('about-btn');
    const aboutModal = document.getElementById('about-modal');
    const aboutClose = document.getElementById('about-close');
    
    if (aboutBtn && aboutModal) {
        aboutBtn.addEventListener('click', () => {
            aboutModal.classList.add('visible');
        });
        
        aboutClose?.addEventListener('click', () => {
            aboutModal.classList.remove('visible');
        });
        
        // Click outside to close
        aboutModal.addEventListener('click', (e) => {
            if (e.target === aboutModal) {
                aboutModal.classList.remove('visible');
            }
        });
    }
    
    // Handle persona clicks
    // Track the main display window so we can reuse it
    let mainDisplayWindow = null;
    
    document.querySelectorAll('.persona-circle').forEach(btn => {
        btn.addEventListener('click', () => {
            const personaId = btn.dataset.persona;
            console.log('[Kiosk] Selected persona:', personaId);
            
            // Visual feedback
            btn.classList.add('selected');
            setTimeout(() => btn.classList.remove('selected'), 300);
            
            // Open/reuse the main display window with summon parameter
            const mainDisplayUrl = `../index.html?summon=${personaId}`;
            
            // Check if we have an existing window that's still open
            if (mainDisplayWindow && !mainDisplayWindow.closed) {
                // Window exists - navigate it to the new persona
                mainDisplayWindow.location.href = mainDisplayUrl;
                mainDisplayWindow.focus();
                console.log('[Kiosk] Reusing existing window for:', personaId);
            } else {
                // Open new window (fullscreen for hologram display)
                mainDisplayWindow = window.open(
                    mainDisplayUrl,
                    'EchoesMainDisplay',
                    'fullscreen=yes,menubar=no,toolbar=no,location=no,status=no'
                );
                console.log('[Kiosk] Opened new window for:', personaId);
            }
            
            showFeedback(`Summoning ${personaId}...`);
        });
    });
});

function showFeedback(message) {
    // Create temporary feedback element
    let feedback = document.querySelector('.feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'feedback';
        feedback.style.cssText = `
            position: fixed;
            bottom: 20%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: #d4af37;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.2rem;
            letter-spacing: 0.1em;
            border: 1px solid rgba(212, 175, 55, 0.3);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 100;
        `;
        document.body.appendChild(feedback);
    }
    
    feedback.textContent = message;
    feedback.style.opacity = '1';
    
    setTimeout(() => {
        feedback.style.opacity = '0';
    }, 2000);
}

// Listen for messages from main display (for two-way communication)
window.addEventListener('message', (event) => {
    console.log('[Kiosk] Received message:', event.data);
    
    if (event.data.type === 'persona-active') {
        // Highlight the active persona
        document.querySelectorAll('.persona-circle').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.persona === event.data.persona);
        });
    }
    
    if (event.data.type === 'persona-dismissed') {
        // Clear active state
        document.querySelectorAll('.persona-circle').forEach(btn => {
            btn.classList.remove('active');
        });
    }
});


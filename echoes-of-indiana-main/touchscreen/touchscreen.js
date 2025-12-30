/**
 * ECHOES OF INDIANA — TOUCHSCREEN INTERFACE
 * Single-screen version for transparent OLED displays
 * 
 * States: menu ↔ active
 * Shares config.js with main project
 */

const TouchscreenApp = {
    currentState: 'menu',
    currentPersona: null,
    simliWidget: null,

    // Initialize the app
    init() {
        console.log('[Touchscreen] Initializing...');
        this.renderPersonaGrid();
        this.bindEvents();
        console.log('[Touchscreen] Ready');
    },

    // Render persona buttons from shared config
    renderPersonaGrid() {
        const grid = document.getElementById('persona-grid');
        if (!grid || typeof CONFIG === 'undefined') {
            console.error('[Touchscreen] Missing grid element or CONFIG');
            return;
        }

        // Get active personas from config
        const personas = CONFIG.personas;
        
        Object.entries(personas).forEach(([id, persona]) => {
            // Skip placeholders (no agentId)
            if (!persona.agentId) return;

            const button = document.createElement('button');
            button.className = 'persona-circle';
            button.dataset.persona = id;

            // Try to use menu video, fallback to placeholder
            const menuVideo = persona.menuVideo || `../assets/videos/${persona.name}_Menu.mp4`;
            
            button.innerHTML = `
                <video autoplay loop muted playsinline>
                    <source src="${menuVideo}" type="video/mp4">
                </video>
                <span class="persona-label">${persona.name}</span>
            `;

            grid.appendChild(button);
        });

        console.log(`[Touchscreen] Rendered ${grid.children.length} personas`);
    },

    // Bind event listeners
    bindEvents() {
        // Persona selection
        document.getElementById('persona-grid').addEventListener('click', (e) => {
            const button = e.target.closest('.persona-circle');
            if (button) {
                const personaId = button.dataset.persona;
                this.summonPersona(personaId);
            }
        });

        // Dismiss button
        document.getElementById('dismiss-btn').addEventListener('click', () => {
            this.dismissPersona();
        });
    },

    // Transition to active state with selected persona
    async summonPersona(personaId) {
        const persona = CONFIG.personas[personaId];
        if (!persona) {
            console.error('[Touchscreen] Persona not found:', personaId);
            return;
        }

        console.log('[Touchscreen] Summoning:', persona.name);
        this.currentPersona = personaId;

        // Switch states
        this.setState('active');

        // Create Simli widget
        await this.createSimliWidget(persona);
    },

    // Create and mount Simli widget
    async createSimliWidget(persona) {
        const container = document.getElementById('simli-container');
        container.innerHTML = ''; // Clear any existing widget

        try {
            // Fetch session token
            const tokenUrl = `https://videotestholoracle-production.up.railway.app/simli-token?agentId=${persona.agentId}&faceId=${persona.faceId}`;
            const response = await fetch(tokenUrl);
            
            if (!response.ok) {
                throw new Error(`Token fetch failed: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('[Touchscreen] Token received');

            // Create widget
            const widget = document.createElement('simli-widget');
            widget.setAttribute('session-token', data.token);
            widget.setAttribute('agent-id', persona.agentId);
            widget.setAttribute('face-id', persona.faceId);
            
            container.appendChild(widget);
            this.simliWidget = widget;

            // Auto-click start button if it appears
            setTimeout(() => this.tryClickStart(), 500);
            setTimeout(() => this.tryClickStart(), 1500);

        } catch (error) {
            console.error('[Touchscreen] Simli error:', error);
            this.dismissPersona();
        }
    },

    // Try to click Simli's internal start button
    tryClickStart() {
        if (!this.simliWidget) return;
        
        const buttons = this.simliWidget.querySelectorAll('button');
        buttons.forEach(btn => {
            const text = btn.textContent.toLowerCase();
            if (text.includes('start') || text.includes('begin') || text.includes('connect')) {
                console.log('[Touchscreen] Clicking start button');
                btn.click();
            }
        });
    },

    // Return to menu state
    dismissPersona() {
        console.log('[Touchscreen] Dismissing persona');
        
        // Destroy widget
        const container = document.getElementById('simli-container');
        container.innerHTML = '';
        this.simliWidget = null;
        this.currentPersona = null;

        // Switch states
        this.setState('menu');
    },

    // State transition
    setState(newState) {
        console.log(`[Touchscreen] State: ${this.currentState} → ${newState}`);
        this.currentState = newState;

        document.getElementById('menu-state').classList.toggle('active', newState === 'menu');
        document.getElementById('active-state').classList.toggle('active', newState === 'active');
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    TouchscreenApp.init();
});


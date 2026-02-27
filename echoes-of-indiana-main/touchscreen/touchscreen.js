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

        // Map persona IDs to their actual menu video files
        const menuVideoMap = {
            'mabel': 'Mabel_Menu.mp4',
            'tomaz': 'Tomaz_Menu.mp4',
            'hazel': 'Hazel_Menu.mp4',
            'riley': 'James_Whitcomb_Riley_Menu.mp4',
            'bigfoot': 'Bigfoot_Menu_Better.mp4'
        };

        // Get active personas from config
        const personas = CONFIG.personas;
        
        Object.entries(personas).forEach(([id, persona]) => {
            // Skip placeholders (no agentId)
            if (!persona.agentId) return;

            const button = document.createElement('button');
            button.className = 'persona-circle';
            button.dataset.persona = id;

            // Use mapped video file or fallback
            const videoFile = menuVideoMap[id] || `${id}_Menu.mp4`;
            const menuVideo = `../assets/videos/${videoFile}`;
            
            // Get short name for display
            const shortName = persona.name.split(' ').slice(-1)[0]; // Last word
            const displayName = id === 'bigfoot' ? 'Bigfoot' : 
                               id === 'riley' ? 'Riley' : persona.name;
            
            button.innerHTML = `
                <video autoplay loop muted playsinline>
                    <source src="${menuVideo}" type="video/mp4">
                </video>
                <span class="persona-label">${displayName}</span>
                <span class="persona-role">${persona.fullTitle || ''}</span>
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
            // Fetch session token (same endpoint as main app)
            const tokenUrl = `https://videotestholoracle-production.up.railway.app/simli-token?agentId=${persona.agentId}&faceId=${persona.faceId}`;
            console.log('[Touchscreen] Fetching token for', persona.name, 'agentId:', persona.agentId, 'faceId:', persona.faceId);
            
            const response = await fetch(tokenUrl);
            
            if (!response.ok) {
                throw new Error(`Token fetch failed: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('[Touchscreen] Token received:', data);

            // Create widget - match EXACT format from main simli-integration.js
            const widget = document.createElement('simli-widget');
            
            // Set token (NOT session-token)
            widget.setAttribute('token', data.token);

            // Set ALL possible attribute formats (Simli docs are inconsistent)
            widget.setAttribute('agentid', persona.agentId);
            widget.setAttribute('agent-id', persona.agentId);
            widget.setAttribute('agentId', persona.agentId);
            if (persona.faceId) {
                widget.setAttribute('faceid', persona.faceId);
                widget.setAttribute('face-id', persona.faceId);
                widget.setAttribute('faceId', persona.faceId);
            }
            
            // Also set as properties (belt and suspenders approach)
            widget.agentId = persona.agentId;
            widget.agentid = persona.agentId;
            if (persona.faceId) {
                widget.faceId = persona.faceId;
                widget.faceid = persona.faceId;
            }
            
            console.log('[Touchscreen] Widget configured - agentId:', persona.agentId, 'faceId:', persona.faceId);

            // Force absolute positioning via inline style (highest specificity)
            widget.style.cssText = 'position: absolute !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important; z-index: 1 !important;';
            
            container.appendChild(widget);
            this.simliWidget = widget;

            // Reach into the shadow DOM and force the widget to fill our container
            this.forceWidgetFullscreen(widget);

            // Auto-click start button AGGRESSIVELY - try many times
            setTimeout(() => this.tryClickStart(), 100);
            setTimeout(() => this.tryClickStart(), 300);
            setTimeout(() => this.tryClickStart(), 500);
            setTimeout(() => this.tryClickStart(), 800);
            setTimeout(() => this.tryClickStart(), 1200);
            setTimeout(() => this.tryClickStart(), 2000);
            setTimeout(() => this.tryClickStart(), 3000);
            setTimeout(() => this.tryClickStart(), 5000);

        } catch (error) {
            console.error('[Touchscreen] Simli error:', error);
            this.dismissPersona();
        }
    },

    // Force the Simli widget to fill the entire container by injecting
    // styles into its shadow DOM and overriding its hardcoded 480px width
    forceWidgetFullscreen(widget) {
        const applyStyles = () => {
            const shadow = widget.shadowRoot;
            if (!shadow) {
                console.log('[Touchscreen] No shadow root yet, retrying...');
                return false;
            }

            // Inject a style override into the shadow DOM
            let injectedStyle = shadow.querySelector('#touchscreen-override');
            if (!injectedStyle) {
                injectedStyle = document.createElement('style');
                injectedStyle.id = 'touchscreen-override';
                injectedStyle.textContent = `
                    :host {
                        position: absolute !important;
                        top: 0 !important;
                        left: 0 !important;
                        bottom: 0 !important;
                        right: 0 !important;
                        width: 100% !important;
                        height: 100% !important;
                        z-index: 1 !important;
                    }
                    .widget-container, .widget-container.expanded {
                        width: 100% !important;
                        height: 100% !important;
                        max-width: none !important;
                        align-items: center !important;
                        justify-content: center !important;
                    }
                    .video-container {
                        width: 100% !important;
                        height: 100% !important;
                        border-radius: 0 !important;
                        background-color: transparent !important;
                        box-shadow: none !important;
                    }
                    video {
                        width: 100% !important;
                        height: 100% !important;
                        object-fit: contain !important;
                    }
                    .controls-container, .start-button, button, .logo, .dotted-face, img[alt="Simli"] {
                        display: none !important;
                    }
                `;
                shadow.appendChild(injectedStyle);
                console.log('[Touchscreen] Injected fullscreen styles into shadow DOM');
            }

            // Also directly modify elements we find
            const allDivs = shadow.querySelectorAll('div');
            allDivs.forEach(div => {
                const style = div.style;
                if (style.width === '480px' || getComputedStyle(div).width === '480px') {
                    div.style.width = '100%';
                    div.style.height = '100%';
                    div.style.maxWidth = 'none';
                    console.log('[Touchscreen] Expanded 480px container');
                }
            });

            return true;
        };

        // Try immediately and keep trying as the widget initializes
        applyStyles();
        const interval = setInterval(() => {
            if (this.currentState !== 'active') {
                clearInterval(interval);
                return;
            }
            applyStyles();
        }, 300);

        // Stop after 15 seconds
        setTimeout(() => clearInterval(interval), 15000);
    },

    // Try to click Simli's internal start button
    tryClickStart() {
        if (!this.simliWidget) return;
        
        // Try within shadow DOM if present
        const roots = [this.simliWidget, this.simliWidget.shadowRoot].filter(Boolean);
        
        roots.forEach(root => {
            const buttons = root.querySelectorAll('button');
            buttons.forEach(btn => {
                const text = (btn.textContent || '').toLowerCase();
                const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                
                if (text.includes('start') || text.includes('begin') || text.includes('connect') ||
                    ariaLabel.includes('start') || ariaLabel.includes('begin')) {
                    console.log('[Touchscreen] Clicking start button:', btn.textContent);
                    btn.click();
                    // Also try to hide it after clicking
                    btn.style.display = 'none';
                    btn.style.opacity = '0';
                    btn.style.pointerEvents = 'none';
                }
            });
        });
        
        // Also look for any blue buttons (Simli's default style)
        const allButtons = document.querySelectorAll('#simli-container button');
        allButtons.forEach(btn => {
            console.log('[Touchscreen] Found button, clicking:', btn.textContent);
            btn.click();
            btn.style.display = 'none';
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
    
    // About modal handlers
    const aboutBtn = document.getElementById('about-btn');
    const aboutModal = document.getElementById('about-modal');
    const modalClose = document.getElementById('modal-close');
    
    if (aboutBtn && aboutModal) {
        aboutBtn.addEventListener('click', () => {
            aboutModal.classList.remove('hidden');
        });
        
        modalClose.addEventListener('click', () => {
            aboutModal.classList.add('hidden');
        });
        
        // Close on background click
        aboutModal.addEventListener('click', (e) => {
            if (e.target === aboutModal) {
                aboutModal.classList.add('hidden');
            }
        });
    }
    
    // =========================================
    // MUSIC CONTROLS
    // =========================================
    const bgMusic = document.getElementById('bg-music');
    const volumeToggle = document.getElementById('volume-toggle');
    const volumeSlider = document.getElementById('volume-slider');
    let musicStarted = false;
    
    if (bgMusic && volumeToggle && volumeSlider) {
        bgMusic.volume = 0.05; // Start at 5%
        
        volumeToggle.addEventListener('click', () => {
            if (bgMusic.paused) {
                bgMusic.play();
                volumeToggle.textContent = '🔊';
            } else {
                bgMusic.pause();
                volumeToggle.textContent = '🔇';
            }
        });
        
        volumeSlider.addEventListener('input', (e) => {
            bgMusic.volume = e.target.value / 100;
            volumeToggle.textContent = bgMusic.volume > 0 ? '🔊' : '🔇';
        });
        
        // Start music on first persona click
        document.getElementById('persona-grid').addEventListener('click', () => {
            if (!musicStarted) {
                musicStarted = true;
                bgMusic.play().catch(e => console.log('Music autoplay blocked:', e));
            }
        });
    }
});


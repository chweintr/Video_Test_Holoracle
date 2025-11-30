/**
 * ECHOES OF INDIANA - SIMLI INTEGRATION
 * Manages Simli widget lifecycle, token generation, and event handling
 * 
 * The Simli agent lives in LAYER 3 of the 4-layer sandwich.
 * It appears in the same "head container" space as the transition videos
 * to ensure perfect alignment between video faces and Simli faces.
 */

const SimliManager = {
    currentWidget: null,
    currentPersona: null,
    isCallActive: false,
    widgetReady: false,

    /**
     * Initialize Simli manager
     */
    init() {
        console.log('[SimliManager] Initialized');

        // Listen for state changes to clean up if needed
        document.addEventListener('statechange', (e) => {
            const { state } = e.detail;

            // Clean up widget when transitioning out
            if (state === 'transitioning-out') {
                this.destroyWidget();
            }
        });
    },

    /**
     * Create and attach Simli widget for a persona
     */
    async createWidget(personaId) {
        const persona = CONFIG.personas[personaId];
        if (!persona) {
            console.error(`[SimliManager] Persona "${personaId}" not found`);
            return false;
        }

        console.log(`[SimliManager] Creating widget for ${persona.name}...`);

        try {
            // Step 1: Get token from backend
            const token = await this.getToken(persona.agentId);
            if (!token) {
                throw new Error('Failed to get Simli token');
            }

            // Step 2: Create widget element
            const widget = document.createElement('simli-widget');
            widget.setAttribute('token', token);
            widget.setAttribute('agentid', persona.agentId);

            if (persona.faceId) {
                widget.setAttribute('faceid', persona.faceId);
            }

            // Custom button text (or hide it entirely)
            widget.setAttribute('customtext', CONFIG.ui.summonButtonText);
            
            // Auto-start the call (don't show the start button)
            widget.setAttribute('autostart', 'true');

            // Step 3: Apply head position adjustments if needed
            const mount = document.getElementById('simli-mount');
            this.applyHeadPositioning(mount, persona.headPosition);

            // Step 4: Attach widget to mount
            mount.innerHTML = ''; // Clear any previous content
            mount.appendChild(widget);

            this.currentWidget = widget;
            this.currentPersona = personaId;
            this.widgetReady = false;

            // Step 5: Set up event listeners
            this.setupWidgetListeners(widget, personaId);

            console.log(`[SimliManager] Widget created for ${persona.name}`);

            // Update debug panel
            this.updateDebugPanel('loading');

            return true;

        } catch (error) {
            console.error('[SimliManager] Error creating widget:', error);
            this.updateDebugPanel('error');
            return false;
        }
    },

    /**
     * Get Simli token from backend
     */
    async getToken(agentId) {
        try {
            const url = `${CONFIG.backendUrl}${CONFIG.tokenEndpoint}?agentId=${agentId}`;
            console.log(`[SimliManager] Requesting token from: ${url}`);

            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Token request failed: ${response.status}`);
            }

            const data = await response.json();
            console.log('[SimliManager] Token received');

            return data.token;

        } catch (error) {
            console.error('[SimliManager] Error fetching token:', error);
            return null;
        }
    },

    /**
     * Apply head position adjustments for this persona
     * This allows fine-tuning if a persona's video head is offset
     */
    applyHeadPositioning(mount, headPosition) {
        if (!headPosition) return;

        // Apply offset via transform
        const offsetX = headPosition.offsetX || '0%';
        const offsetY = headPosition.offsetY || '0%';
        const scale = headPosition.scale || 1.0;

        mount.style.transform = `translate(${offsetX}, ${offsetY}) scale(${scale})`;
    },

    /**
     * Set up event listeners on Simli widget
     */
    setupWidgetListeners(widget, personaId) {
        // Listen for widget ready
        widget.addEventListener('ready', (e) => {
            console.log('[SimliManager] Widget ready');
            this.widgetReady = true;
            this.updateDebugPanel('ready');
        });

        // Listen for call start (user clicks summon in widget)
        widget.addEventListener('callstart', (e) => {
            console.log('[SimliManager] Call started');
            this.isCallActive = true;
            this.updateDebugPanel('call-active');

            // Dispatch custom event
            document.dispatchEvent(new CustomEvent('simli-call-start', {
                detail: { persona: personaId }
            }));
        });

        // Listen for call end
        widget.addEventListener('callend', (e) => {
            console.log('[SimliManager] Call ended');
            this.isCallActive = false;
            this.updateDebugPanel('call-ended');

            // Dispatch custom event
            document.dispatchEvent(new CustomEvent('simli-call-end', {
                detail: { persona: personaId }
            }));
        });

        // Listen for user speaking (if supported by widget)
        widget.addEventListener('speaking', (e) => {
            console.log('[SimliManager] User is speaking');
            // When user speaks, we're processing
            if (StateMachine.getState() === 'active') {
                StateMachine.startProcessing();
            }
        });

        // Listen for AI response start (if supported)
        widget.addEventListener('response-start', (e) => {
            console.log('[SimliManager] AI response starting');
            // When AI responds, stop processing state
            StateMachine.stopProcessing();
        });

        // Listen for video stream active
        widget.addEventListener('videoready', (e) => {
            console.log('[SimliManager] Video stream ready');
            this.updateDebugPanel('streaming');
        });

        // Fallback: Monitor for speech activity using a MutationObserver
        this.setupSpeechMonitor(widget);
    },

    /**
     * Monitor widget for speech activity using DOM observation
     * This is a fallback in case the widget doesn't emit proper events
     */
    setupSpeechMonitor(widget) {
        const observer = new MutationObserver((mutations) => {
            // Check if widget is showing processing indicators
            const isProcessing = widget.querySelector('[data-processing="true"]') !== null ||
                                 widget.querySelector('.processing') !== null;

            if (isProcessing && StateMachine.getState() === 'active') {
                StateMachine.startProcessing();
            } else if (!isProcessing && StateMachine.getState() === 'processing') {
                StateMachine.stopProcessing();
            }
        });

        observer.observe(widget, {
            attributes: true,
            childList: true,
            subtree: true
        });
    },

    /**
     * Show Simli mount (fade in or instant)
     * @param {boolean} instant - If true, show immediately without transition
     */
    showWidget(instant = false) {
        const mount = document.getElementById('simli-mount');
        
        if (instant) {
            mount.classList.add('instant-show');
            mount.classList.add('active');
            setTimeout(() => mount.classList.remove('instant-show'), 50);
        } else {
            mount.classList.add('active');
        }
        
        console.log('[SimliManager] Widget shown');
    },

    /**
     * Hide Simli mount (fade out or instant)
     * @param {boolean} instant - If true, hide immediately without transition
     */
    hideWidget(instant = false) {
        const mount = document.getElementById('simli-mount');
        
        if (instant) {
            mount.classList.add('instant-hide');
            mount.classList.remove('active');
            setTimeout(() => mount.classList.remove('instant-hide'), 50);
        } else {
            mount.classList.remove('active');
        }
        
        console.log('[SimliManager] Widget hidden');
    },

    /**
     * Destroy current widget
     */
    destroyWidget() {
        if (!this.currentWidget) return;

        console.log('[SimliManager] Destroying widget...');

        const mount = document.getElementById('simli-mount');

        // Hide mount
        this.hideWidget();

        // Remove widget after fade out
        setTimeout(() => {
            mount.innerHTML = '';
            mount.style.transform = ''; // Reset any positioning adjustments
            this.currentWidget = null;
            this.currentPersona = null;
            this.isCallActive = false;
            this.widgetReady = false;
            this.updateDebugPanel('destroyed');
            console.log('[SimliManager] Widget destroyed');
        }, CONFIG.timing.crossfadeDuration);
    },

    /**
     * Check if call is active
     */
    isActive() {
        return this.isCallActive;
    },

    /**
     * Check if widget is ready
     */
    isReady() {
        return this.widgetReady;
    },

    /**
     * Update debug panel
     */
    updateDebugPanel(status) {
        if (!CONFIG.ui.showDebugPanel) return;

        const simliEl = document.getElementById('debug-simli');
        if (simliEl) simliEl.textContent = status;
    },

    /**
     * Emergency cleanup - force destroy everything
     */
    forceCleanup() {
        console.warn('[SimliManager] Force cleanup');
        
        const mount = document.getElementById('simli-mount');
        mount.classList.remove('active');
        mount.innerHTML = '';
        mount.style.transform = '';
        
        this.currentWidget = null;
        this.currentPersona = null;
        this.isCallActive = false;
        this.widgetReady = false;
        
        this.updateDebugPanel('force-cleaned');
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    SimliManager.init();
});

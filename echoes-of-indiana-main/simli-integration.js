/**
 * ECHOES OF INDIANA - SIMLI INTEGRATION
 * Manages Simli widget lifecycle, token generation, and event handling
 */

const SimliManager = {
    currentWidget: null,
    currentPersona: null,
    isCallActive: false,

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

            // Custom button text
            widget.setAttribute('customtext', CONFIG.ui.summonButtonText);

            // Step 3: Apply custom positioning
            const mount = document.getElementById('simli-mount');
            this.applyPositioning(mount, persona.simliPosition);

            // Step 4: Attach widget to mount
            mount.innerHTML = ''; // Clear any previous content
            mount.appendChild(widget);

            this.currentWidget = widget;
            this.currentPersona = personaId;

            // Step 5: Set up event listeners
            this.setupWidgetListeners(widget, personaId);

            console.log(`[SimliManager] Widget created for ${persona.name}`);

            // Update debug panel
            this.updateDebugPanel('loaded');

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
     * Apply custom positioning to Simli mount
     */
    applyPositioning(mount, position) {
        if (!position) return;

        if (position.top) mount.style.top = position.top;
        if (position.left) mount.style.left = position.left;
        if (position.width) mount.style.width = position.width;
        if (position.height) mount.style.height = position.height;
        if (position.transform) mount.style.transform = position.transform;
    },

    /**
     * Set up event listeners on Simli widget
     */
    setupWidgetListeners(widget, personaId) {
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
            StateMachine.startProcessing();
        });

        // Listen for AI response start (if supported)
        widget.addEventListener('response-start', (e) => {
            console.log('[SimliManager] AI response starting');
            // When AI responds, stop processing state
            StateMachine.stopProcessing();
        });

        // Fallback: Monitor for speech activity using a MutationObserver
        // (in case widget doesn't emit speaking events)
        this.setupSpeechMonitor(widget);
    },

    /**
     * Monitor widget for speech activity using DOM observation
     * This is a fallback in case the widget doesn't emit proper events
     */
    setupSpeechMonitor(widget) {
        // Look for changes in the widget that indicate processing
        // This is implementation-specific and may need adjustment
        const observer = new MutationObserver((mutations) => {
            // Check if widget is showing processing indicators
            const isProcessing = widget.querySelector('[data-processing="true"]') !== null;

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
     * Show Simli mount (fade in)
     */
    showWidget() {
        const mount = document.getElementById('simli-mount');
        mount.classList.add('active');
    },

    /**
     * Hide Simli mount (fade out)
     */
    hideWidget() {
        const mount = document.getElementById('simli-mount');
        mount.classList.remove('active');
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
            this.currentWidget = null;
            this.currentPersona = null;
            this.isCallActive = false;
            this.updateDebugPanel('destroyed');
            console.log('[SimliManager] Widget destroyed');
        }, 500); // Match CSS transition time
    },

    /**
     * Check if call is active
     */
    isActive() {
        return this.isCallActive;
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
        this.destroyWidget();
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    SimliManager.init();
});

/**
 * ECHOES OF INDIANA - STATE MACHINE
 * 
 * Manages state transitions for the 4-layer compositor:
 * 
 * State Flow:
 * ┌──────────┐
 * │   IDLE   │ ← Layers 1+2+4 playing, persona selection visible
 * └────┬─────┘
 *      │ user clicks persona
 *      ▼
 * ┌──────────────────┐
 * │ TRANSITIONING-IN │ ← Layer 2 plays idle-to-persona video
 * └────────┬─────────┘
 *          │ video ends
 *          ▼
 * ┌──────────┐
 * │  ACTIVE  │ ← Layer 3 (Simli) visible, interactive
 * └────┬─────┘
 *      │ user speaks
 *      ▼
 * ┌────────────┐
 * │ PROCESSING │ ← Processing message shown
 * └──────┬─────┘
 *        │ AI responds
 *        ▼
 * ┌──────────┐
 * │  ACTIVE  │ ← Back to interactive
 * └────┬─────┘
 *      │ user clicks dismiss
 *      ▼
 * ┌───────────────────┐
 * │ TRANSITIONING-OUT │ ← Layer 2 plays persona-to-idle video
 * └─────────┬─────────┘
 *           │ video ends
 *           ▼
 * ┌──────────┐
 * │   IDLE   │ ← Back to start
 * └──────────┘
 */

const StateMachine = {
    // Current state
    currentState: 'idle',
    activePersona: null,
    processingMessageInterval: null,

    // State definitions
    states: {
        IDLE: 'idle',
        TRANSITIONING_IN: 'transitioning-in',
        ACTIVE: 'active',
        PROCESSING: 'processing',
        TRANSITIONING_OUT: 'transitioning-out',
    },

    /**
     * Initialize the state machine
     */
    init() {
        console.log('[StateMachine] Initialized');
        this.setState(this.states.IDLE);
    },

    /**
     * Set current state and trigger UI updates
     */
    setState(newState, persona = null) {
        const previousState = this.currentState;
        this.currentState = newState;

        console.log(`[StateMachine] ${previousState} → ${newState}`, persona ? `(${persona})` : '');

        // Update debug panel
        this.updateDebugPanel();

        // Emit state change event for other modules to listen
        document.dispatchEvent(new CustomEvent('statechange', {
            detail: { state: newState, persona, previousState }
        }));
    },

    /**
     * Get current state
     */
    getState() {
        return this.currentState;
    },

    /**
     * Get active persona
     */
    getActivePersona() {
        return this.activePersona;
    },

    /**
     * Transition: idle → transitioning-in
     * User selected a persona, begin summoning
     */
    async summonPersona(personaId) {
        if (this.currentState !== this.states.IDLE) {
            console.warn('[StateMachine] Cannot summon - not in idle state');
            return false;
        }

        const persona = CONFIG.personas[personaId];
        if (!persona) {
            console.error(`[StateMachine] Persona "${personaId}" not found in config`);
            return false;
        }

        this.activePersona = personaId;
        this.setState(this.states.TRANSITIONING_IN, personaId);

        return true;
    },

    /**
     * Transition: transitioning-in → active
     * Called when transition video completes
     */
    transitionComplete() {
        if (this.currentState !== this.states.TRANSITIONING_IN) {
            console.warn('[StateMachine] transitionComplete called but not in transitioning-in state');
            return;
        }

        this.setState(this.states.ACTIVE, this.activePersona);
    },

    /**
     * Transition: active → processing
     * Called when user asks question or Simli starts processing
     */
    startProcessing() {
        if (this.currentState !== this.states.ACTIVE) {
            console.warn('[StateMachine] Cannot start processing - not in active state');
            return false;
        }

        this.setState(this.states.PROCESSING, this.activePersona);

        // Start rotating processing messages
        this.startProcessingMessages();

        return true;
    },

    /**
     * Transition: processing → active
     * Called when Simli finishes processing and starts speaking
     */
    stopProcessing() {
        if (this.currentState !== this.states.PROCESSING) {
            return;
        }

        this.setState(this.states.ACTIVE, this.activePersona);

        // Stop rotating processing messages
        this.stopProcessingMessages();
    },

    /**
     * Transition: active → transitioning-out
     * Called when user clicks dismiss
     */
    dismissPersona() {
        if (this.currentState !== this.states.ACTIVE && this.currentState !== this.states.PROCESSING) {
            console.warn('[StateMachine] Cannot dismiss - not in active or processing state');
            return false;
        }

        // Stop processing messages if any
        this.stopProcessingMessages();

        this.setState(this.states.TRANSITIONING_OUT, this.activePersona);

        return true;
    },

    /**
     * Transition: transitioning-out → idle
     * Called when dismiss transition completes
     */
    returnToIdle() {
        if (this.currentState !== this.states.TRANSITIONING_OUT) {
            console.warn('[StateMachine] returnToIdle called but not in transitioning-out state');
            return;
        }

        this.activePersona = null;
        this.setState(this.states.IDLE);
    },

    /**
     * Emergency reset - force back to idle
     * Use when something goes wrong
     */
    forceReset() {
        console.warn('[StateMachine] FORCE RESET - returning to idle');
        this.stopProcessingMessages();
        this.activePersona = null;
        this.setState(this.states.IDLE);
    },

    /* ============================================
       PROCESSING MESSAGES
       ============================================ */

    /**
     * Start rotating processing messages
     */
    startProcessingMessages() {
        if (!this.activePersona) return;

        const persona = CONFIG.personas[this.activePersona];
        const messages = persona.processingMessages || ['Processing...'];
        let currentIndex = 0;

        // Show first message immediately
        this.showProcessingMessage(messages[currentIndex]);

        // Rotate through messages
        this.processingMessageInterval = setInterval(() => {
            currentIndex = (currentIndex + 1) % messages.length;
            this.showProcessingMessage(messages[currentIndex]);
        }, CONFIG.timing.processingMessageRotateInterval);
    },

    /**
     * Stop rotating processing messages
     */
    stopProcessingMessages() {
        if (this.processingMessageInterval) {
            clearInterval(this.processingMessageInterval);
            this.processingMessageInterval = null;
        }
        this.hideProcessingMessage();
    },

    /**
     * Show processing message
     */
    showProcessingMessage(message) {
        const overlay = document.getElementById('status-overlay');
        const messageEl = overlay.querySelector('.status-message');

        messageEl.textContent = message;
        overlay.classList.remove('hidden');
        overlay.classList.add('visible');
    },

    /**
     * Hide processing message
     */
    hideProcessingMessage() {
        const overlay = document.getElementById('status-overlay');
        overlay.classList.remove('visible');
        overlay.classList.add('hidden');
    },

    /* ============================================
       DEBUG & HELPERS
       ============================================ */

    /**
     * Update debug panel
     */
    updateDebugPanel() {
        if (!CONFIG.ui.showDebugPanel) return;

        const stateEl = document.getElementById('debug-state');
        const personaEl = document.getElementById('debug-persona');

        if (stateEl) stateEl.textContent = this.currentState;
        if (personaEl) personaEl.textContent = this.activePersona || 'none';
    },

    /**
     * Check if we're in an active state (can interact)
     */
    isInteractive() {
        return this.currentState === this.states.ACTIVE || this.currentState === this.states.PROCESSING;
    },

    /**
     * Check if we're idle
     */
    isIdle() {
        return this.currentState === this.states.IDLE;
    },

    /**
     * Check if we're transitioning
     */
    isTransitioning() {
        return this.currentState === this.states.TRANSITIONING_IN ||
               this.currentState === this.states.TRANSITIONING_OUT;
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    StateMachine.init();
});

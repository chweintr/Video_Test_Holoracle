/**
 * ECHOES OF INDIANA - MAIN COMPOSITOR
 * Orchestrates video layers, state machine, and Simli integration
 */

const Compositor = {
    // DOM Elements
    elements: {
        layerBelow: null,
        layerAbove: null,
        simliMount: null,
        personaSelection: null,
        dismissBtn: null,
        borderMask: null,
    },

    /**
     * Initialize the compositor
     */
    init() {
        console.log('[Compositor] Initializing...');

        // Get DOM elements
        this.elements.layerBelow = document.getElementById('layer-below');
        this.elements.layerAbove = document.getElementById('layer-above');
        this.elements.simliMount = document.getElementById('simli-mount');
        this.elements.personaSelection = document.getElementById('persona-selection');
        this.elements.dismissBtn = document.getElementById('dismiss-btn');
        this.elements.borderMask = document.getElementById('border-mask');

        // Apply anti-cropping settings from config
        this.applyAntiCroppingSettings();

        // Set up event listeners
        this.setupEventListeners();

        // Listen for state changes
        this.listenToStateChanges();

        console.log('[Compositor] Ready');
    },

    /**
     * Set up UI event listeners
     */
    setupEventListeners() {
        // Persona selection buttons
        const personaBtns = document.querySelectorAll('.persona-btn');
        personaBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const personaId = btn.getAttribute('data-persona');
                this.onPersonaSelected(personaId);
            });
        });

        // Dismiss button
        this.elements.dismissBtn.addEventListener('click', () => {
            this.onDismissClicked();
        });

        // Listen for transition video end events
        this.elements.layerBelow.addEventListener('ended', () => {
            this.onTransitionVideoEnded('below');
        });

        this.elements.layerAbove.addEventListener('ended', () => {
            this.onTransitionVideoEnded('above');
        });
    },

    /**
     * Listen to state machine changes and respond accordingly
     */
    listenToStateChanges() {
        document.addEventListener('statechange', (e) => {
            const { state, persona, previousState } = e.detail;
            console.log(`[Compositor] State changed: ${previousState} → ${state}`);

            switch (state) {
                case 'idle':
                    this.handleIdleState();
                    break;

                case 'transitioning-in':
                    this.handleTransitionInState(persona);
                    break;

                case 'active':
                    this.handleActiveState(persona);
                    break;

                case 'processing':
                    this.handleProcessingState(persona);
                    break;

                case 'transitioning-out':
                    this.handleTransitionOutState(persona);
                    break;
            }
        });
    },

    /**
     * Handle: User selects a persona
     */
    async onPersonaSelected(personaId) {
        console.log(`[Compositor] Persona selected: ${personaId}`);

        // Trigger state machine
        const success = await StateMachine.summonPersona(personaId);

        if (!success) {
            console.error('[Compositor] Failed to summon persona');
            alert('Failed to load persona. Please try again.');
        }
    },

    /**
     * Handle: User clicks dismiss button
     */
    onDismissClicked() {
        console.log('[Compositor] Dismiss clicked');
        StateMachine.dismissPersona();
    },

    /**
     * Handle: Transition video ended
     */
    onTransitionVideoEnded(layer) {
        console.log(`[Compositor] Transition video ended on layer: ${layer}`);

        const state = StateMachine.getState();

        // If we're transitioning in and the main transition video ended, move to active
        if (state === 'transitioning-in' && layer === 'below') {
            // Transition is complete, move to active state
            StateMachine.transitionComplete();
        }

        // If we're transitioning out and the transition video ended, return to idle
        if (state === 'transitioning-out' && layer === 'below') {
            StateMachine.returnToIdle();
        }
    },

    /* ============================================
       STATE HANDLERS
       ============================================ */

    /**
     * State: IDLE
     * Show persona selection, hide everything else
     */
    handleIdleState() {
        console.log('[Compositor] → IDLE state');

        // Show persona selection
        this.elements.personaSelection.classList.remove('hidden');

        // Hide dismiss button
        this.elements.dismissBtn.classList.remove('visible');
        this.elements.dismissBtn.classList.add('hidden');

        // Clear all video layers
        this.clearVideoLayer('below');
        this.clearVideoLayer('above');

        // Hide Simli mount
        SimliManager.hideWidget();

        // TODO: Optionally play global idle loop video here
        // this.playVideo('below', 'assets/videos/global-idle-loop.mp4', true);
    },

    /**
     * State: TRANSITIONING-IN
     * Play transition video, create Simli widget, hide persona selection
     */
    async handleTransitionInState(personaId) {
        console.log(`[Compositor] → TRANSITIONING-IN state (${personaId})`);

        const persona = CONFIG.personas[personaId];

        // Hide persona selection
        setTimeout(() => {
            this.elements.personaSelection.classList.add('hidden');
        }, CONFIG.ui.autoHideSelectionDelay);

        // Play transition video (idle → persona)
        if (persona.videos.idleToActive) {
            const videoPath = `assets/videos/${persona.videos.idleToActive}`;
            await this.playVideo('below', videoPath, false);
        } else {
            console.warn('[Compositor] No idle-to-active video configured');
            // No transition video, move directly to active
            setTimeout(() => {
                StateMachine.transitionComplete();
            }, 1000);
        }

        // Start loading Simli widget in parallel (while video plays)
        const widgetSuccess = await SimliManager.createWidget(personaId);

        if (!widgetSuccess) {
            console.error('[Compositor] Failed to create Simli widget');
            // Fallback: return to idle
            StateMachine.forceReset();
            alert('Failed to load persona. Please try again.');
        }
    },

    /**
     * State: ACTIVE
     * Show Simli widget, start background/overlay loops, show dismiss button
     */
    handleActiveState(personaId) {
        console.log(`[Compositor] → ACTIVE state (${personaId})`);

        const persona = CONFIG.personas[personaId];

        // Clear transition video from below layer
        this.clearVideoLayer('below');

        // Show Simli widget
        SimliManager.showWidget();

        // Start background loop (if configured)
        if (persona.videos.background) {
            const videoPath = `assets/videos/${persona.videos.background}`;
            this.playVideo('below', videoPath, true);
        }

        // Start overlay loop (if configured)
        if (persona.videos.overlay) {
            const videoPath = `assets/videos/${persona.videos.overlay}`;
            this.playVideo('above', videoPath, true);
        }

        // Show dismiss button
        this.elements.dismissBtn.classList.remove('hidden');
        this.elements.dismissBtn.classList.add('visible');
    },

    /**
     * State: PROCESSING
     * Show processing message overlay (handled by state-machine.js)
     */
    handleProcessingState(personaId) {
        console.log(`[Compositor] → PROCESSING state (${personaId})`);

        // Processing messages are handled by StateMachine
        // Background and overlay videos continue playing
        // Nothing special to do here in compositor
    },

    /**
     * State: TRANSITIONING-OUT
     * Play transition back to idle, clean up
     */
    async handleTransitionOutState(personaId) {
        console.log(`[Compositor] → TRANSITIONING-OUT state (${personaId})`);

        const persona = CONFIG.personas[personaId];

        // Hide dismiss button
        this.elements.dismissBtn.classList.remove('visible');
        this.elements.dismissBtn.classList.add('hidden');

        // Hide Simli widget
        SimliManager.hideWidget();

        // Clear overlay
        this.clearVideoLayer('above');

        // Play transition video (persona → idle)
        if (persona.videos.activeToIdle) {
            const videoPath = `assets/videos/${persona.videos.activeToIdle}`;
            await this.playVideo('below', videoPath, false);
        } else {
            // No transition-out video, just fade and return to idle
            this.clearVideoLayer('below');
            setTimeout(() => {
                StateMachine.returnToIdle();
            }, 1000);
        }

        // Note: transition video 'ended' event will trigger returnToIdle()
    },

    /* ============================================
       VIDEO LAYER CONTROLS
       ============================================ */

    /**
     * Play video on specified layer
     */
    async playVideo(layer, videoPath, loop = false) {
        const videoEl = layer === 'below' ? this.elements.layerBelow : this.elements.layerAbove;

        console.log(`[Compositor] Playing video on ${layer}: ${videoPath} (loop: ${loop})`);

        // Set video source
        videoEl.src = videoPath;
        videoEl.loop = loop;

        // Show video
        videoEl.classList.add('active');

        // Play video
        try {
            await videoEl.play();
            console.log(`[Compositor] Video playing on ${layer}`);
        } catch (error) {
            console.error(`[Compositor] Error playing video on ${layer}:`, error);
        }
    },

    /**
     * Clear video from layer
     */
    clearVideoLayer(layer) {
        const videoEl = layer === 'below' ? this.elements.layerBelow : this.elements.layerAbove;

        console.log(`[Compositor] Clearing video layer: ${layer}`);

        // Fade out
        videoEl.classList.remove('active');

        // Stop and clear after fade
        setTimeout(() => {
            videoEl.pause();
            videoEl.src = '';
            videoEl.currentTime = 0;
        }, 500); // Match CSS transition time
    },

    /**
     * Pause video on layer
     */
    pauseVideo(layer) {
        const videoEl = layer === 'below' ? this.elements.layerBelow : this.elements.layerAbove;
        videoEl.pause();
    },

    /**
     * Resume video on layer
     */
    resumeVideo(layer) {
        const videoEl = layer === 'below' ? this.elements.layerBelow : this.elements.layerAbove;
        videoEl.play();
    },

    /* ============================================
       UTILITY
       ============================================ */

    /**
     * Apply anti-cropping settings from config
     */
    applyAntiCroppingSettings() {
        const stage = document.getElementById('stage');

        // Apply stage inset (prevents cropping at edges)
        if (CONFIG.ui.stageInset && CONFIG.ui.stageInset !== '0%') {
            const inset = CONFIG.ui.stageInset;
            stage.style.width = `calc(100vw - ${inset} * 2)`;
            stage.style.height = `calc(100vh - ${inset} * 2)`;
            stage.style.margin = inset;
            console.log(`[Compositor] Applied stage inset: ${inset}`);
        }

        // Enable border mask if configured
        if (CONFIG.ui.enableBorderMask && this.elements.borderMask) {
            this.elements.borderMask.classList.add('enabled');
            this.elements.borderMask.style.opacity = CONFIG.ui.borderMaskOpacity;
            console.log(`[Compositor] Border mask enabled (opacity: ${CONFIG.ui.borderMaskOpacity})`);
        }

        // Ensure videos use contain (never crop)
        const videoLayers = document.querySelectorAll('.video-layer');
        videoLayers.forEach(video => {
            video.style.objectFit = 'contain';
        });
        console.log('[Compositor] Video layers set to object-fit: contain');
    },

    /**
     * Emergency reset - force everything back to idle
     */
    forceReset() {
        console.warn('[Compositor] FORCE RESET');
        StateMachine.forceReset();
        SimliManager.forceCleanup();
        this.handleIdleState();
    }
};

// Initialize compositor when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Compositor.init();
});

// Expose compositor globally for debugging
window.Compositor = Compositor;
window.StateMachine = StateMachine;
window.SimliManager = SimliManager;

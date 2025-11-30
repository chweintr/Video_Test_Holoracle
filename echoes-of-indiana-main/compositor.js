/**
 * ECHOES OF INDIANA - 4-LAYER COMPOSITOR
 * 
 * The 4-Layer Sandwich (top to bottom):
 * ┌─────────────────────────────────────────┐
 * │  Layer 4: TOP FLOATIES                  │  ← Perpetual loop
 * │  (sparkles, particles, neon wisps)      │
 * ├─────────────────────────────────────────┤
 * │  Layer 3: SIMLI AGENT                   │  ← Only visible during interaction
 * │  (Mabel's face, interactive)            │
 * ├─────────────────────────────────────────┤
 * │  Layer 2: ABSTRACT LOOPS / TRANSITIONS  │  ← The "genie smoke" layer
 * │  - idle: random abstract loops          │
 * │  - idle-to-persona: swirly → face spot  │
 * │  - persona-to-idle: face spot → swirly  │
 * ├─────────────────────────────────────────┤
 * │  Layer 1: BOTTOM FLOATIES               │  ← Perpetual loop
 * │  (smoke, embers, subtle effects)        │
 * └─────────────────────────────────────────┘
 * 
 * The Flow:
 * 1. Resting state: Layers 1 + 2 (random abstract loops) + 4 all playing
 * 2. User invokes Mabel: Let current abstract loop finish → play idle-to-mabel.mp4
 * 3. Transition ends: Simli agent appears in exact spot where smoke resolved → interactive
 * 4. User dismisses: Immediately swap Simli for mabel-to-idle.mp4
 * 5. Transition ends: Return to random abstract loops
 */

const Compositor = {
    // DOM Elements
    elements: {
        // Layer 1: Bottom floaties
        bottomFloaties: null,
        
        // Layer 2: Abstract/Transitions
        idleLoop: null,
        transition: null,
        
        // Layer 3: Simli
        simliMount: null,
        simliWrapper: null,
        
        // Layer 4: Top floaties
        topFloaties: null,
        
        // Other
        borderMask: null,
    },

    // State tracking
    idleLoopIndex: 0,
    isIdleLoopPlaying: false,

    /**
     * Initialize the compositor
     */
    init() {
        console.log('[Compositor] Initializing 4-Layer Compositor...');

        // Get DOM elements
        this.elements.bottomFloaties = document.getElementById('video-bottom-floaties');
        this.elements.idleLoop = document.getElementById('video-idle-loop');
        this.elements.transition = document.getElementById('video-transition');
        this.elements.simliMount = document.getElementById('simli-mount');
        this.elements.simliWrapper = document.getElementById('simli-mount');
        this.elements.topFloaties = document.getElementById('video-top-floaties');
        this.elements.borderMask = document.getElementById('border-mask');

        // Apply anti-cropping settings from config
        this.applyAntiCroppingSettings();

        // Set up event listeners
        this.setupEventListeners();

        // Listen for state changes
        this.listenToStateChanges();

        // Start perpetual floaties
        this.startFloaties();

        // Start idle loop
        this.startIdleLoop();

        console.log('[Compositor] Ready - 4 layers initialized');
    },

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Idle loop ended - play next random loop
        this.elements.idleLoop.addEventListener('ended', () => {
            this.onIdleLoopEnded();
        });

        // Transition video ended
        this.elements.transition.addEventListener('ended', () => {
            this.onTransitionVideoEnded();
        });
    },

    /**
     * PUBLIC API: Invoke a persona from external source
     * Call this from kiosk via postMessage or URL param
     */
    invokePersona(personaId) {
        console.log(`[Compositor] External invoke: ${personaId}`);
        return this.onPersonaSelected(personaId);
    },

    /**
     * PUBLIC API: Dismiss current persona
     */
    dismissPersona() {
        console.log('[Compositor] External dismiss');
        return this.onDismissClicked();
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

        // Listen for Simli video stream becoming ready
        // This triggers the seamless swap from transition video to Simli
        document.addEventListener('simli-video-ready', (e) => {
            console.log('[Compositor] Simli video stream ready - completing swap');
            this.onSimliVideoReady();
        });
    },

    /**
     * Called when Simli's video stream is actually ready
     * NOW we can hide the transition video
     */
    onSimliVideoReady() {
        const state = StateMachine.getState();
        
        // Only do the swap if we're in active state waiting for Simli
        if (state === 'active') {
            console.log('[Compositor] Completing transition video → Simli swap');
            // NOW hide the transition video (Simli is streaming)
            this.clearTransitionVideo(true); // instant hide
        }
    },

    /* ============================================
       FLOATIES (Layers 1 & 4) - Perpetual Loops
       ============================================ */

    /**
     * Start perpetual floaties on layers 1 and 4
     */
    startFloaties() {
        // Bottom floaties (Layer 1)
        if (CONFIG.video.bottomFloaties) {
            const videoPath = `assets/videos/${CONFIG.video.bottomFloaties}`;
            this.elements.bottomFloaties.src = videoPath;
            this.elements.bottomFloaties.loop = true;
            this.elements.bottomFloaties.play()
                .then(() => {
                    this.elements.bottomFloaties.classList.add('active');
                    console.log('[Compositor] Bottom floaties started');
                })
                .catch(e => console.warn('[Compositor] Bottom floaties autoplay blocked:', e));
        }

        // Top floaties (Layer 4)
        if (CONFIG.video.topFloaties) {
            const videoPath = `assets/videos/${CONFIG.video.topFloaties}`;
            this.elements.topFloaties.src = videoPath;
            this.elements.topFloaties.loop = true;
            this.elements.topFloaties.play()
                .then(() => {
                    this.elements.topFloaties.classList.add('active');
                    console.log('[Compositor] Top floaties started');
                })
                .catch(e => console.warn('[Compositor] Top floaties autoplay blocked:', e));
        }
    },

    /* ============================================
       IDLE LOOP (Layer 2) - Random Abstract Videos
       ============================================ */

    /**
     * Start playing idle loop videos
     */
    startIdleLoop() {
        if (!CONFIG.video.idleLoops || CONFIG.video.idleLoops.length === 0) {
            console.log('[Compositor] No idle loops configured');
            return;
        }

        this.isIdleLoopPlaying = true;
        this.playNextIdleLoop();
        this.updateDebugPanel('idle', 'playing');
    },

    /**
     * Play the next idle loop video
     */
    playNextIdleLoop() {
        if (!this.isIdleLoopPlaying) return;

        const idleLoops = CONFIG.video.idleLoops;
        
        // Pick random video (or sequential if configured)
        if (CONFIG.video.randomizeIdleLoops) {
            this.idleLoopIndex = Math.floor(Math.random() * idleLoops.length);
        } else {
            this.idleLoopIndex = (this.idleLoopIndex + 1) % idleLoops.length;
        }

        const videoPath = `assets/videos/${idleLoops[this.idleLoopIndex]}`;
        console.log(`[Compositor] Playing idle loop: ${videoPath}`);

        this.elements.idleLoop.src = videoPath;
        this.elements.idleLoop.loop = false; // Don't loop - we'll pick new one on end
        this.elements.idleLoop.classList.add('active');
        
        this.elements.idleLoop.play()
            .catch(e => console.warn('[Compositor] Idle loop autoplay blocked:', e));
    },

    /**
     * Handle idle loop video ended
     */
    onIdleLoopEnded() {
        if (this.isIdleLoopPlaying) {
            this.playNextIdleLoop();
        }
    },

    /**
     * Stop idle loop
     */
    stopIdleLoop() {
        console.log('[Compositor] Stopping idle loop');
        this.isIdleLoopPlaying = false;
        this.updateDebugPanel('idle', 'stopped');
        
        // Fade out current idle loop
        this.elements.idleLoop.classList.remove('active');
        
        setTimeout(() => {
            this.elements.idleLoop.pause();
        }, 500); // Match CSS fade transition
    },

    /**
     * Resume idle loop
     */
    resumeIdleLoop() {
        console.log('[Compositor] Resuming idle loop');
        this.isIdleLoopPlaying = true;
        this.updateDebugPanel('idle', 'playing');
        this.playNextIdleLoop();
    },

    /* ============================================
       EVENT HANDLERS
       ============================================ */

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
     * Handle: Dismiss persona (from external command)
     */
    onDismissClicked() {
        console.log('[Compositor] Dismiss requested');
        return StateMachine.dismissPersona();
    },

    /**
     * Handle: Transition video ended
     */
    onTransitionVideoEnded() {
        console.log('[Compositor] Transition video ended');

        const state = StateMachine.getState();

        // If we're transitioning in and the transition video ended, move to active
        if (state === 'transitioning-in') {
            StateMachine.transitionComplete();
        }

        // If we're transitioning out and the transition video ended, return to idle
        if (state === 'transitioning-out') {
            StateMachine.returnToIdle();
        }
    },

    /* ============================================
       STATE HANDLERS
       ============================================ */

    /**
     * State: IDLE
     * Play idle loops, hide Simli, wait for external invoke
     */
    handleIdleState() {
        console.log('[Compositor] → IDLE state');

        // Clear transition video
        this.clearTransitionVideo();

        // Hide Simli widget
        SimliManager.hideWidget();

        // Resume idle loop
        this.resumeIdleLoop();
    },

    /**
     * State: TRANSITIONING-IN
     * Play transition video, create Simli widget
     */
    async handleTransitionInState(personaId) {
        console.log(`[Compositor] → TRANSITIONING-IN state (${personaId})`);

        const persona = CONFIG.personas[personaId];

        // Stop idle loop - let it fade out while transition fades in
        this.stopIdleLoop();

        // Play transition video (idle → persona)
        if (persona.videos.idleToActive) {
            await this.playTransitionVideo(persona.videos.idleToActive);
        } else {
            console.warn('[Compositor] No idle-to-active video configured');
            // No transition video, move directly to active after short delay
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
        }
    },

    /**
     * State: ACTIVE
     * Keep transition video visible until Simli video stream is ready!
     */
    handleActiveState(personaId) {
        console.log(`[Compositor] → ACTIVE state (${personaId})`);

        // DON'T hide transition video yet!
        // Keep it visible as a "hold frame" while Simli loads
        // The transition video will be hidden when simli-video-ready event fires
        
        // Check if Simli video is already streaming (in case event fired before state change)
        if (SimliManager.isVideoReady && SimliManager.isVideoReady()) {
            console.log('[Compositor] Simli already streaming - hiding transition');
            this.clearTransitionVideo(true);
            SimliManager.showWidget();
        } else {
            console.log('[Compositor] Waiting for Simli video stream before hiding transition...');
            // Transition video stays visible - Simli widget stays hidden
            // The swap will happen when simli-video-ready fires
        }
    },

    /**
     * State: PROCESSING
     * Show processing message overlay (handled by state-machine.js)
     */
    handleProcessingState(personaId) {
        console.log(`[Compositor] → PROCESSING state (${personaId})`);
        // Processing messages are handled by StateMachine
        // Simli remains visible, nothing to do here
    },

    /**
     * State: TRANSITIONING-OUT
     * Play transition back to idle, clean up
     */
    async handleTransitionOutState(personaId) {
        console.log(`[Compositor] → TRANSITIONING-OUT state (${personaId})`);

        const persona = CONFIG.personas[personaId];

        // Hide Simli widget INSTANTLY (so transition video takes over)
        SimliManager.hideWidget(true); // true = instant

        // Play transition video (persona → idle)
        if (persona.videos.activeToIdle) {
            await this.playTransitionVideo(persona.videos.activeToIdle);
        } else {
            // No transition-out video, just return to idle
            setTimeout(() => {
                StateMachine.returnToIdle();
            }, 500);
        }

        // Note: transition video 'ended' event will trigger returnToIdle()
    },

    /* ============================================
       VIDEO LAYER CONTROLS
       ============================================ */

    /**
     * Play a transition video (Layer 2)
     */
    async playTransitionVideo(videoName) {
        const videoPath = `assets/videos/${videoName}`;
        console.log(`[Compositor] Playing transition video: ${videoPath}`);

        this.elements.transition.src = videoPath;
        this.elements.transition.loop = false;
        this.elements.transition.classList.add('active');

        try {
            await this.elements.transition.play();
            console.log('[Compositor] Transition video playing');
        } catch (error) {
            console.error('[Compositor] Error playing transition video:', error);
        }
    },

    /**
     * Clear transition video
     */
    clearTransitionVideo(instant = false) {
        if (instant) {
            this.elements.transition.classList.add('instant-hide');
            this.elements.transition.classList.remove('active');
            this.elements.transition.pause();
            this.elements.transition.src = '';
            
            // Remove instant class after a tick
            setTimeout(() => {
                this.elements.transition.classList.remove('instant-hide');
            }, 50);
        } else {
            this.elements.transition.classList.remove('active');
            
            setTimeout(() => {
                this.elements.transition.pause();
                this.elements.transition.src = '';
            }, 500); // Match CSS fade transition
        }
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
    },

    /**
     * Update debug panel
     */
    updateDebugPanel(field, value) {
        if (!CONFIG.ui.showDebugPanel) return;

        const el = document.getElementById(`debug-${field}`);
        if (el) el.textContent = value;
    },

    /**
     * Emergency reset - force everything back to idle
     */
    forceReset() {
        console.warn('[Compositor] FORCE RESET');
        StateMachine.forceReset();
        SimliManager.forceCleanup();
        this.clearTransitionVideo();
        this.handleIdleState();
    }
};

// Initialize compositor when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Compositor.init();
});

// Expose globally for debugging
window.Compositor = Compositor;
window.StateMachine = StateMachine;
window.SimliManager = SimliManager;

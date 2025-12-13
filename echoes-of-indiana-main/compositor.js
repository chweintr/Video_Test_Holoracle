/**
 * 4-LAYER COMPOSITOR
 * Idle loop ALWAYS plays - everything layers on top
 */

const Compositor = {
    elements: {},
    idleLoopIndex: 0,
    isIdleLoopPlaying: false,
    transitionComplete: false,  // Track if transition video finished
    simliReady: false,          // Track if Simli is ready

    // Helper: Pick random video from array, or return single string
    pickVideo(videoConfig) {
        if (!videoConfig) return null;
        if (Array.isArray(videoConfig)) {
            if (videoConfig.length === 0) return null;
            const idx = Math.floor(Math.random() * videoConfig.length);
            console.log(`[Compositor] Random pick: ${videoConfig[idx]} (${idx + 1}/${videoConfig.length})`);
            return videoConfig[idx];
        }
        return videoConfig; // Single string
    },

    init() {
        console.log('[Compositor] Initializing...');
        
        this.elements.idleLoop = document.getElementById('video-idle-loop');
        this.elements.transition = document.getElementById('video-transition');
        this.elements.simliMount = document.getElementById('simli-mount');

        this.setupEventListeners();
        this.listenToStateChanges();
        
        console.log('[Compositor] Ready');
    },

    setupEventListeners() {
        // Idle loop ended - play next (ALWAYS continues)
        this.elements.idleLoop.addEventListener('ended', () => {
            this.playNextIdleLoop();
        });

        // Transition ended - NOW we can show Simli
        this.elements.transition.addEventListener('ended', () => {
            console.log('[Compositor] Transition video ENDED');
            this.transitionComplete = true;
            this.tryShowSimli();
        });
    },

    listenToStateChanges() {
        document.addEventListener('statechange', (e) => {
            const { state, persona } = e.detail;
            console.log('[Compositor] State:', state);

            switch (state) {
                case 'idle': this.handleIdle(); break;
                case 'transitioning-in': this.handleTransitionIn(persona); break;
                case 'active': this.handleActive(persona); break;
                case 'transitioning-out': this.handleTransitionOut(persona); break;
            }
        });

        // Simli video ready - but DON'T show yet, wait for transition
        document.addEventListener('simli-video-ready', () => {
            console.log('[Compositor] Simli ready - waiting for transition to end');
            this.simliReady = true;
            this.tryShowSimli();
        });
    },

    // Only show Simli when BOTH transition is done AND Simli is ready
    tryShowSimli() {
        console.log('[Compositor] tryShowSimli - transition:', this.transitionComplete, 'simli:', this.simliReady);
        if (this.transitionComplete && this.simliReady) {
            console.log('[Compositor] BOTH ready - showing Simli now');
            this.hideTransitionVideo();
            SimliManager.showWidget();
            // Move to active state if not already
            if (StateMachine.getState() === 'transitioning-in') {
                StateMachine.transitionComplete();
            }
        }
    },

    // PUBLIC: Start idle loop (called after user click)
    startIdleLoop() {
        console.log('[Compositor] Starting idle loop (runs forever)');
        this.isIdleLoopPlaying = true;
        this.playNextIdleLoop();
    },

    playNextIdleLoop() {
        if (!CONFIG.video.idleLoops || CONFIG.video.idleLoops.length === 0) return;

        const loops = CONFIG.video.idleLoops;
        if (CONFIG.video.randomizeIdleLoops) {
            this.idleLoopIndex = Math.floor(Math.random() * loops.length);
        } else {
            this.idleLoopIndex = (this.idleLoopIndex + 1) % loops.length;
        }

        const path = `assets/videos/${loops[this.idleLoopIndex]}`;
        console.log('[Compositor] Idle loop:', path);
        
        this.elements.idleLoop.src = path;
        this.elements.idleLoop.loop = true;
        this.elements.idleLoop.classList.add('active');
        this.elements.idleLoop.play().catch(e => console.warn('Idle play error:', e));
    },

    // PUBLIC API
    invokePersona(personaId) {
        console.log('[Compositor] Invoking:', personaId);
        return StateMachine.summonPersona(personaId);
    },

    dismissPersona() {
        console.log('[Compositor] Dismissing');
        return StateMachine.dismissPersona();
    },

    // State handlers

    handleIdle() {
        console.log('[Compositor] → IDLE');
        this.transitionComplete = false;
        this.simliReady = false;
        this.hideTransitionVideo();
        SimliManager.destroyWidget();
    },

    async handleTransitionIn(personaId) {
        console.log('[Compositor] → TRANSITIONING-IN');
        const persona = CONFIG.personas[personaId];
        
        // Reset flags
        this.transitionComplete = false;
        this.simliReady = false;

        // Play transition video (picks randomly if array)
        const transitionVideo = this.pickVideo(persona.videos.idleToActive);
        if (transitionVideo) {
            await this.playTransitionVideo(transitionVideo);
        } else {
            // No transition video, mark as complete immediately
            this.transitionComplete = true;
        }

        // Load Simli in background (but don't show until transition ends)
        const success = await SimliManager.createWidget(personaId);
        if (!success) {
            console.error('[Compositor] Simli failed');
            StateMachine.forceReset();
        }
    },

    handleActive(personaId) {
        console.log('[Compositor] → ACTIVE');
        // Simli should already be visible from tryShowSimli()
    },

    handleTransitionOut(personaId) {
        console.log('[Compositor] → TRANSITIONING-OUT');
        const persona = CONFIG.personas[personaId];

        // Destroy Simli widget
        SimliManager.destroyWidget();

        // Play transition out if exists (picks randomly if array)
        const transitionOut = persona && persona.videos ? this.pickVideo(persona.videos.activeToIdle) : null;
        if (transitionOut) {
            this.playTransitionVideo(transitionOut);
        } else {
            setTimeout(() => StateMachine.returnToIdle(), 500);
        }
    },

    async playTransitionVideo(filename) {
        const path = `assets/videos/${filename}`;
        console.log('[Compositor] Playing transition:', path);
        
        this.elements.transition.src = path;
        this.elements.transition.loop = false;
        this.elements.transition.classList.add('active');
        
        // Optional: Speed up transition video (1.0 = normal, 1.5 = 50% faster, 2.0 = double speed)
        const speed = CONFIG.video?.transitionPlaybackRate || 1.0;
        this.elements.transition.playbackRate = speed;
        if (speed !== 1.0) console.log('[Compositor] Transition speed:', speed + 'x');
        
        try {
            await this.elements.transition.play();
        } catch (e) {
            console.warn('Transition play error:', e);
            // If play fails, mark transition as complete
            this.transitionComplete = true;
            this.tryShowSimli();
        }
    },

    hideTransitionVideo() {
        this.elements.transition.classList.remove('active');
        setTimeout(() => {
            this.elements.transition.pause();
            this.elements.transition.src = '';
        }, 500);
    },

    forceReset() {
        console.log('[Compositor] FORCE RESET');
        this.transitionComplete = false;
        this.simliReady = false;
        this.hideTransitionVideo();
        SimliManager.forceCleanup();
        StateMachine.forceReset();
    }
};

document.addEventListener('DOMContentLoaded', () => Compositor.init());
window.Compositor = Compositor;

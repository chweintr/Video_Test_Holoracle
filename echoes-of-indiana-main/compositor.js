/**
 * 4-LAYER COMPOSITOR
 * Idle loop ALWAYS plays - everything layers on top
 */

const Compositor = {
    elements: {},
    idleLoopIndex: 0,
    isIdleLoopPlaying: false,

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

        // Transition ended
        this.elements.transition.addEventListener('ended', () => {
            this.onTransitionEnded();
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

        // Simli video ready - hide transition, show Simli
        document.addEventListener('simli-video-ready', () => {
            console.log('[Compositor] Simli ready - showing');
            this.hideTransitionVideo();
        });
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
        this.elements.idleLoop.loop = true; // Loop continuously
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

    // State handlers - idle loop NEVER stops

    handleIdle() {
        console.log('[Compositor] → IDLE');
        this.hideTransitionVideo();
        SimliManager.hideWidget();
        // Idle loop keeps playing
    },

    async handleTransitionIn(personaId) {
        console.log('[Compositor] → TRANSITIONING-IN');
        const persona = CONFIG.personas[personaId];

        // Play transition ON TOP of idle (idle keeps playing underneath)
        if (persona.videos.idleToActive) {
            await this.playTransitionVideo(persona.videos.idleToActive);
        }

        // Load Simli in background
        const success = await SimliManager.createWidget(personaId);
        if (!success) {
            console.error('[Compositor] Simli failed');
            StateMachine.forceReset();
        }
    },

    onTransitionEnded() {
        const state = StateMachine.getState();
        console.log('[Compositor] Transition ended, state:', state);

        if (state === 'transitioning-in') {
            // Keep transition visible until Simli ready
            console.log('[Compositor] Holding for Simli...');
            StateMachine.transitionComplete();
        }

        if (state === 'transitioning-out') {
            this.hideTransitionVideo();
            StateMachine.returnToIdle();
        }
    },

    handleActive(personaId) {
        console.log('[Compositor] → ACTIVE');
        // Transition stays visible until simli-video-ready fires
        // Idle loop still playing underneath
        if (SimliManager.isVideoReady()) {
            this.hideTransitionVideo();
        }
    },

    handleTransitionOut(personaId) {
        console.log('[Compositor] → TRANSITIONING-OUT');
        const persona = CONFIG.personas[personaId];

        // Hide Simli
        SimliManager.hideWidget();

        // Play transition out (on top of idle which keeps playing)
        if (persona.videos.activeToIdle) {
            this.playTransitionVideo(persona.videos.activeToIdle);
        } else {
            setTimeout(() => StateMachine.returnToIdle(), 500);
        }
    },

    async playTransitionVideo(filename) {
        const path = `assets/videos/${filename}`;
        console.log('[Compositor] Transition:', path);
        
        this.elements.transition.src = path;
        this.elements.transition.loop = false;
        this.elements.transition.classList.add('active');
        
        try {
            await this.elements.transition.play();
        } catch (e) {
            console.warn('Transition play error:', e);
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
        this.hideTransitionVideo();
        SimliManager.forceCleanup();
        StateMachine.forceReset();
    }
};

document.addEventListener('DOMContentLoaded', () => Compositor.init());
window.Compositor = Compositor;

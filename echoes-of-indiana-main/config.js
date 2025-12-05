/**
 * ECHOES OF INDIANA - CONFIGURATION
 * 
 * 4-Layer Compositor Configuration:
 * ┌─────────────────────────────────────────┐
 * │  Layer 4: TOP FLOATIES                  │
 * │  Layer 3: SIMLI AGENT                   │
 * │  Layer 2: ABSTRACT LOOPS / TRANSITIONS  │
 * │  Layer 1: BOTTOM FLOATIES               │
 * └─────────────────────────────────────────┘
 */

const CONFIG = {
    // Backend API endpoint
    backendUrl: window.location.origin,
    tokenEndpoint: '/simli-token',

    /* ============================================
       GLOBAL VIDEO SETTINGS
       These affect multiple personas or global layers
       ============================================ */
    video: {
        // LAYER 1: Bottom Floaties (perpetual loop)
        // Smoke, embers, subtle depth effects behind everything
        bottomFloaties: null, // e.g., 'floaties-bottom.mp4'
        
        // LAYER 4: Top Floaties (perpetual loop)
        // Sparkles, particles, neon wisps on top of everything
        topFloaties: null, // e.g., 'floaties-top.mp4'
        
        // LAYER 2: Idle Loops (random abstract videos)
        // These play when no persona is active
        // The compositor picks randomly from this array
        idleLoops: [
            'idle_1.mp4',
            // Add more idle loops here as you create them:
            // 'idle_2.mp4',
            // 'idle_3.mp4',
        ],
        
        // Randomize idle loop selection (true) or play sequentially (false)
        randomizeIdleLoops: true,
        
        // Default transition duration (ms) - used when no video is configured
        defaultTransitionDuration: 2000,
        
        // Allow user to skip transition by clicking
        allowSkipTransition: false,
        
        // Transition video playback speed (1.0 = normal, 1.5 = 50% faster, 2.0 = double speed)
        // Increase this if your transition video is too long
        transitionPlaybackRate: 1.5,  // ← ADJUST THIS (1.0-2.0)
    },

    /* ============================================
       PERSONAS CONFIGURATION
       Each persona has their own Simli agent, videos, and settings
       ============================================ */
    personas: {
        mabel: {
            name: 'Mabel',
            fullTitle: 'Showers Finishing Worker, 1917',
            quote: '"I sand till the grain lies flat; the whistle tells you what the clock would."',
            description: 'Sanded drawer fronts; helped at the veneer press; counted pieces at the bell during the war years.',

            // Simli Configuration
            agentId: '2c8b6f6d-cb83-4100-a99b-ee33f808069a', // Mabel's Simli Agent ID
            faceId: '33622e5c-6107-4da0-9794-8ea784ccdb43',  // Mabel's Face ID

            // Video Assets (paths relative to assets/videos/)
            videos: {
                // REQUIRED: Transition from idle abstract → persona head appearing
                // Last frame should show head in position where Simli will appear
                idleToActive: 'idle_to_mabel_2.mp4',
                
                // OPTIONAL: Transition from persona → back to abstract
                // If null, will just fade out
                activeToIdle: null, // e.g., 'mabel_to_idle.mp4'
            },

            // Processing Messages (shown during AI latency)
            processingMessages: [
                'Mabel is checking the grain...',
                'Mabel is listening to the whistle...',
                'Mabel is counting the pieces...',
                'Mabel is considering your question...',
            ],

            /* 
             * HEAD POSITIONING
             * 
             * Normally you don't need to adjust this because the CSS 
             * head-container handles uniform sizing. But if your video
             * has the head offset from center, you can fine-tune here.
             * 
             * These values are applied to the head-container for this persona.
             */
            headPosition: {
                // Offset from center (use negative values to move left/up)
                offsetX: '0%',
                offsetY: '0%',
                
                // Scale adjustment (1.0 = no change)
                // Use if Simli head needs to be larger/smaller than video head
                scale: 1.0,
            }
        },

        /* ============================================
           FUTURE PERSONAS - Uncomment and configure as needed
           ============================================ */

        /*
        'hoosier-oracle': {
            name: 'Hoosier Oracle',
            fullTitle: 'Echoes Guide',
            quote: '"Ask your question; I will route you to stone, rail, factory, or code."',
            agentId: 'YOUR_ORACLE_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'idle_to_oracle.mp4',
                activeToIdle: 'oracle_to_idle.mp4',
            },
            processingMessages: [
                'Oracle is routing your query...',
                'Oracle is consulting the echoes...',
                'Oracle is gathering wisdom...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        vonnegut: {
            name: 'Kurt Vonnegut',
            fullTitle: 'Indianapolis Author',
            quote: '"I wanted people to respond as I do to the absurdity."',
            agentId: 'YOUR_VONNEGUT_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'idle_to_vonnegut.mp4',
                activeToIdle: null,
            },
            processingMessages: [
                'Kurt is pondering the absurdity...',
                'Kurt is gathering his thoughts...',
                'So it goes...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },

        bigfoot: {
            name: 'Brown County Bigfoot',
            fullTitle: 'Trail Sage & Cryptid Teller',
            quote: '"Say whether you need miles, water, or a creature tale for the campfire."',
            agentId: 'YOUR_BIGFOOT_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'idle_to_bigfoot.mp4',
                activeToIdle: 'bigfoot_to_idle.mp4',
            },
            processingMessages: [
                'Bigfoot is sniffing the trail...',
                'Bigfoot is consulting the forest...',
                'Bigfoot is gathering a tale...',
            ],
            headPosition: {
                offsetX: '0%',
                offsetY: '0%',
                scale: 1.0,
            }
        },
        */
    },

    /* ============================================
       UI SETTINGS
       ============================================ */
    ui: {
        showDebugPanel: false, // Use ?debug=true in URL to show
        
        // Anti-Cropping Settings for LED Holograms
        stageInset: '0%', // Inset stage from screen edges (e.g., '5%')
        enableBorderMask: false, // Enable vignette border
        borderMaskOpacity: 0.8, // How dark the border mask should be (0-1)
    },

    /* ============================================
       HEAD CONTAINER SETTINGS
       Global settings for the unified head area
       ============================================ */
    head: {
        // These CSS values control the head container size
        // Both transition videos AND Simli render inside this same container
        // Change these to scale all heads uniformly
        
        // Default size (can be overridden in CSS for responsiveness)
        width: '80vmin',
        height: '80vmin',
        maxWidth: '900px',
        maxHeight: '900px',
    },

    /* ============================================
       STATE MACHINE TIMINGS
       ============================================ */
    timing: {
        // How long to wait for transition video to start
        transitionVideoWaitTime: 2000,
        
        // Rotate processing messages every X ms
        processingMessageRotateInterval: 5000,
        
        // Dismiss transition time (if no video)
        dismissTransitionTime: 500,
        
        // Video crossfade duration (ms)
        crossfadeDuration: 500,
    },

    /* ============================================
       AUDIO SETTINGS
       ============================================ */
    audio: {
        enableBackgroundAmbience: false,
        ambienceVolume: 0.3,
    },
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

/**
 * ECHOES OF INDIANA - CONFIGURATION
 * Persona definitions, Simli credentials, video paths, and processing messages
 */

const CONFIG = {
    // Backend API endpoint (reuses existing backend from parent repo)
    backendUrl: window.location.origin, // Same domain, served by Railway
    tokenEndpoint: '/simli-token',

    // Personas Configuration
    // Add new personas here - each entry is completely self-contained
    personas: {
        mabel: {
            name: 'Mabel',
            fullTitle: 'Showers Finishing Worker, 1917',
            quote: '"I sand till the grain lies flat; the whistle tells you what the clock would."',
            description: 'Sanded drawer fronts; helped at the veneer press; counted pieces at the bell during the war years.',

            // Simli Configuration
            agentId: 'YOUR_MABEL_AGENT_ID_HERE', // TODO: Add Mabel's Simli Agent ID
            faceId: null, // Optional: Add if using Compose API

            // Video Assets (paths relative to assets/videos/)
            videos: {
                idleToActive: 'mabel-idle-to-active.mp4', // Transition from idle to Mabel
                activeToIdle: 'mabel-active-to-idle.mp4', // Transition from Mabel back to idle (optional)
                background: null, // Optional: Background smoke/atmosphere loop
                overlay: null, // Optional: Top layer effects
            },

            // Processing Messages (shown during AI latency)
            processingMessages: [
                'Mabel is checking the grain...',
                'Mabel is listening to the whistle...',
                'Mabel is counting the pieces...',
                'Mabel is considering your question...',
            ],

            // Positioning (adjust based on where head appears in video)
            simliPosition: {
                top: '50%',
                left: '50%',
                width: '600px',
                height: '600px',
            }
        },

        // ============================================
        // FUTURE PERSONAS - Uncomment and configure as needed
        // ============================================

        /*
        'hoosier-oracle': {
            name: 'Hoosier Oracle',
            fullTitle: 'Echoes Guide',
            quote: '"Ask your question; I will route you to stone, rail, factory, or code."',
            agentId: 'YOUR_ORACLE_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'oracle-idle-to-active.mp4',
                activeToIdle: 'oracle-active-to-idle.mp4',
                background: 'oracle-background.mp4',
                overlay: 'oracle-overlay.mp4',
            },
            processingMessages: [
                'Oracle is routing your query...',
                'Oracle is consulting the echoes...',
                'Oracle is gathering wisdom...',
            ],
            simliPosition: {
                top: '50%',
                left: '50%',
                width: '600px',
                height: '600px',
            }
        },

        vonnegut: {
            name: 'Kurt Vonnegut',
            fullTitle: 'Indianapolis Author',
            quote: '"I wanted people to respond as I do to the absurdity and wickedness of all that grownups pretend to be."',
            agentId: 'YOUR_VONNEGUT_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'vonnegut-idle-to-active.mp4',
                activeToIdle: 'vonnegut-active-to-idle.mp4',
                background: null,
                overlay: null,
            },
            processingMessages: [
                'Kurt is pondering the absurdity...',
                'Kurt is gathering his thoughts...',
                'Kurt is considering the wickedness...',
            ],
            simliPosition: {
                top: '50%',
                left: '50%',
                width: '600px',
                height: '600px',
            }
        },

        bigfoot: {
            name: 'Brown County Bigfoot',
            fullTitle: 'Trail Sage & Cryptid Teller',
            quote: '"Say whether you need miles, water, or a creature tale for the campfire; I will point you."',
            agentId: 'YOUR_BIGFOOT_AGENT_ID',
            faceId: null,
            videos: {
                idleToActive: 'bigfoot-idle-to-active.mp4',
                activeToIdle: 'bigfoot-active-to-idle.mp4',
                background: 'bigfoot-forest-smoke.mp4',
                overlay: 'bigfoot-mist-overlay.mp4',
            },
            processingMessages: [
                'Bigfoot is sniffing the trail...',
                'Bigfoot is consulting the forest...',
                'Bigfoot is gathering a tale...',
            ],
            simliPosition: {
                top: '50%',
                left: '50%',
                width: '600px',
                height: '600px',
            }
        },
        */
    },

    // Global Video Settings
    video: {
        idleLoop: null, // Optional: Global idle animation (abstract hologram loop)
        defaultTransitionDuration: 2000, // milliseconds
        allowSkipTransition: false, // If true, user can click to skip transition
    },

    // UI Settings
    ui: {
        showDebugPanel: true, // Set to false for production
        dismissButtonText: 'Dismiss',
        summonButtonText: 'Summon',
        autoHideSelectionDelay: 500, // ms after persona selected

        // Anti-Cropping Settings for LED Holograms
        stageInset: '5%', // Inset stage from screen edges (prevents edge cropping)
        enableBorderMask: false, // Enable irregular border to hide potential cropping
        borderMaskOpacity: 0.8, // How dark the border mask should be (0-1)
    },

    // Audio Settings (if needed beyond Simli's built-in)
    audio: {
        enableBackgroundAmbience: false,
        ambienceVolume: 0.3,
    },

    // State Machine Timings
    timing: {
        transitionVideoWaitTime: 2000, // How long to wait for transition video to start
        processingMessageRotateInterval: 5000, // Rotate processing messages every 5s
        dismissTransitionTime: 2000, // Time for dismiss transition
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

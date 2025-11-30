/**
 * ECHOES OF INDIANA - SIMLI INTEGRATION
 * Manages Simli widget lifecycle, token generation, and event handling
 * 
 * The Simli agent lives in LAYER 3 of the 4-layer sandwich.
 * It appears in the same "head container" space as the transition videos
 * to ensure perfect alignment between video faces and Simli faces.
 * 
 * KEY: We don't reveal the Simli widget until its VIDEO STREAM is actually
 * active, not just when the widget loads. This prevents the dotted placeholder
 * from showing.
 */

const SimliManager = {
    currentWidget: null,
    currentPersona: null,
    isCallActive: false,
    widgetReady: false,
    videoStreamActive: false, // NEW: Track if actual video is streaming
    callStartedByUs: false,   // Track if we auto-started the call

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
            widget.setAttribute('customtext', CONFIG.ui.summonButtonText || 'Start');

            // Step 3: Apply head position adjustments if needed
            const mount = document.getElementById('simli-mount');
            this.applyHeadPositioning(mount, persona.headPosition);

            // Step 4: Attach widget to mount (but DON'T show it yet!)
            mount.innerHTML = ''; // Clear any previous content
            mount.appendChild(widget);

            this.currentWidget = widget;
            this.currentPersona = personaId;
            this.widgetReady = false;
            this.videoStreamActive = false;
            this.callStartedByUs = false;

            // Step 5: Set up event listeners
            this.setupWidgetListeners(widget, personaId);

            // Step 6: Try to auto-start the call after widget loads
            this.waitForWidgetAndAutoStart(widget);

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
     * Wait for widget to be ready then auto-start the call
     */
    waitForWidgetAndAutoStart(widget) {
        // Poll for the start button and click it
        let attempts = 0;
        const maxAttempts = 50; // 5 seconds max
        
        const tryAutoStart = () => {
            attempts++;
            
            // Look for the start/summon button within the widget
            const shadowRoot = widget.shadowRoot;
            let startButton = null;
            
            if (shadowRoot) {
                // Try various selectors for the start button
                startButton = shadowRoot.querySelector('button') ||
                              shadowRoot.querySelector('[class*="start"]') ||
                              shadowRoot.querySelector('[class*="summon"]') ||
                              shadowRoot.querySelector('[class*="call"]');
            }
            
            // Also check for button in regular DOM (widget might not use shadow DOM)
            if (!startButton) {
                startButton = widget.querySelector('button') ||
                              document.querySelector('#simli-mount button');
            }
            
            if (startButton && !this.callStartedByUs) {
                console.log('[SimliManager] Found start button, auto-clicking...');
                this.callStartedByUs = true;
                startButton.click();
                this.updateDebugPanel('auto-starting');
            } else if (attempts < maxAttempts) {
                setTimeout(tryAutoStart, 100);
            } else {
                console.warn('[SimliManager] Could not find start button after 5 seconds');
            }
        };
        
        // Start polling after a brief delay for widget to initialize
        setTimeout(tryAutoStart, 500);
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

        // Listen for call start
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
            this.videoStreamActive = false;
            this.updateDebugPanel('call-ended');

            // Dispatch custom event
            document.dispatchEvent(new CustomEvent('simli-call-end', {
                detail: { persona: personaId }
            }));
        });

        // Listen for user speaking
        widget.addEventListener('speaking', (e) => {
            console.log('[SimliManager] User is speaking');
            if (StateMachine.getState() === 'active') {
                StateMachine.startProcessing();
            }
        });

        // Listen for AI response start
        widget.addEventListener('response-start', (e) => {
            console.log('[SimliManager] AI response starting');
            StateMachine.stopProcessing();
        });

        // Listen for video stream becoming active
        widget.addEventListener('videoready', (e) => {
            console.log('[SimliManager] Video stream ready!');
            this.videoStreamActive = true;
            this.updateDebugPanel('streaming');
            
            // NOW we can reveal the widget and hide the transition video
            this.onVideoStreamReady();
        });

        // Monitor for video element appearing (backup detection)
        this.setupVideoDetection(widget);
        
        // Monitor for speech activity
        this.setupSpeechMonitor(widget);
    },

    /**
     * Monitor for actual video element with a stream
     * This is a backup in case 'videoready' event isn't fired
     */
    setupVideoDetection(widget) {
        let checkCount = 0;
        const maxChecks = 100; // 10 seconds max
        
        const checkForVideo = () => {
            checkCount++;
            
            // Look for video element with actual content
            let videoEl = widget.querySelector('video');
            
            // Also check shadow DOM
            if (!videoEl && widget.shadowRoot) {
                videoEl = widget.shadowRoot.querySelector('video');
            }
            
            if (videoEl) {
                // Check if video has actual content (not just placeholder)
                const hasSource = videoEl.src || videoEl.srcObject;
                const isPlaying = !videoEl.paused && videoEl.readyState >= 2;
                const hasSize = videoEl.videoWidth > 0 && videoEl.videoHeight > 0;
                
                if ((hasSource || isPlaying) && hasSize) {
                    console.log('[SimliManager] Video stream detected via polling!', {
                        src: !!videoEl.src,
                        srcObject: !!videoEl.srcObject,
                        playing: isPlaying,
                        size: `${videoEl.videoWidth}x${videoEl.videoHeight}`
                    });
                    
                    if (!this.videoStreamActive) {
                        this.videoStreamActive = true;
                        this.onVideoStreamReady();
                    }
                    return; // Stop polling
                }
            }
            
            if (checkCount < maxChecks) {
                setTimeout(checkForVideo, 100);
            }
        };
        
        setTimeout(checkForVideo, 1000); // Start checking after 1 second
    },

    /**
     * Called when video stream is actually ready
     * This triggers the seamless swap from transition video to Simli
     */
    onVideoStreamReady() {
        console.log('[SimliManager] Video stream ready - revealing Simli!');
        this.updateDebugPanel('streaming');
        
        // Dispatch event for compositor to handle the swap
        document.dispatchEvent(new CustomEvent('simli-video-ready', {
            detail: { persona: this.currentPersona }
        }));
        
        // Show the widget now that video is streaming
        this.showWidget();
    },

    /**
     * Monitor widget for speech activity using DOM observation
     */
    setupSpeechMonitor(widget) {
        const observer = new MutationObserver((mutations) => {
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
     * Check if video stream is active
     */
    isVideoReady() {
        return this.videoStreamActive;
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
            this.videoStreamActive = false;
            this.callStartedByUs = false;
            this.updateDebugPanel('destroyed');
            console.log('[SimliManager] Widget destroyed');
        }, CONFIG.timing.crossfadeDuration || 500);
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
        if (!CONFIG.ui || !CONFIG.ui.showDebugPanel) return;

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
        this.videoStreamActive = false;
        this.callStartedByUs = false;
        
        this.updateDebugPanel('force-cleaned');
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    SimliManager.init();
});

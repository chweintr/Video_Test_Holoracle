/**
 * SIMLI INTEGRATION - with fallback timeout
 */

const SimliManager = {
    currentWidget: null,
    currentPersona: null,
    videoStreamActive: false,
    detectionTimeout: null,

    init() {
        console.log('[SimliManager] Initialized');
    },

    async createWidget(personaId) {
        const persona = CONFIG.personas[personaId];
        if (!persona) {
            console.error('[SimliManager] Persona not found:', personaId);
            return false;
        }

        console.log('[SimliManager] Creating widget for', persona.name);
        this.updateDebug('fetching token...');

        try {
            const token = await this.getToken(persona.agentId);
            if (!token) throw new Error('No token');

            console.log('[SimliManager] Token received, creating widget');
            this.updateDebug('creating widget...');

            const widget = document.createElement('simli-widget');
            widget.setAttribute('token', token);
            widget.setAttribute('agentid', persona.agentId);
            if (persona.faceId) widget.setAttribute('faceid', persona.faceId);

            const mount = document.getElementById('simli-mount');
            mount.innerHTML = '';
            mount.appendChild(widget);

            this.currentWidget = widget;
            this.currentPersona = personaId;
            this.videoStreamActive = false;

            // Try to auto-start after widget loads
            setTimeout(() => this.autoStart(widget), 1000);
            
            // Start detecting video stream
            this.detectVideoStream(widget);
            
            // FALLBACK: After 8 seconds, show Simli anyway
            this.detectionTimeout = setTimeout(() => {
                if (!this.videoStreamActive) {
                    console.log('[SimliManager] FALLBACK: Forcing show after timeout');
                    this.updateDebug('fallback show');
                    this.onVideoReady();
                }
            }, 8000);

            return true;

        } catch (error) {
            console.error('[SimliManager] Error:', error);
            this.updateDebug('error: ' + error.message);
            return false;
        }
    },

    async getToken(agentId) {
        const url = `${CONFIG.backendUrl}${CONFIG.tokenEndpoint}?agentId=${agentId}`;
        console.log('[SimliManager] Fetching token from:', url);
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Token fetch failed: ' + response.status);
        
        const data = await response.json();
        console.log('[SimliManager] Token response:', data);
        return data.token;
    },

    autoStart(widget) {
        console.log('[SimliManager] Looking for start button...');
        this.updateDebug('looking for button...');
        
        let attempts = 0;
        const tryClick = () => {
            attempts++;
            
            // Try various ways to find the button
            let btn = widget.querySelector('button');
            if (!btn) btn = document.querySelector('#simli-mount button');
            if (!btn && widget.shadowRoot) btn = widget.shadowRoot.querySelector('button');
            
            if (btn) {
                console.log('[SimliManager] Found button, clicking');
                this.updateDebug('clicking start...');
                btn.click();
                return;
            }
            
            if (attempts < 30) {
                setTimeout(tryClick, 200);
            } else {
                console.log('[SimliManager] No button found after 30 attempts');
                this.updateDebug('no button found');
            }
        };
        tryClick();
    },

    detectVideoStream(widget) {
        console.log('[SimliManager] Starting video detection');
        let checks = 0;
        
        const check = () => {
            checks++;
            
            // Look for video element
            let video = widget.querySelector('video');
            if (!video) video = document.querySelector('#simli-mount video');
            if (!video && widget.shadowRoot) video = widget.shadowRoot.querySelector('video');
            
            if (video) {
                const playing = !video.paused && video.readyState >= 2;
                const hasSize = video.videoWidth > 0;
                const hasSrc = video.src || video.srcObject;
                
                console.log('[SimliManager] Video check:', { playing, hasSize, hasSrc, readyState: video.readyState });
                
                if (hasSrc && (playing || hasSize)) {
                    console.log('[SimliManager] Video stream detected!');
                    this.onVideoReady();
                    return;
                }
            }
            
            if (checks < 80) { // 8 seconds
                setTimeout(check, 100);
            }
        };
        
        setTimeout(check, 1500);
    },

    onVideoReady() {
        if (this.videoStreamActive) return;
        this.videoStreamActive = true;
        
        console.log('[SimliManager] Video ready - revealing');
        this.updateDebug('streaming');
        
        // Clear fallback timeout
        if (this.detectionTimeout) {
            clearTimeout(this.detectionTimeout);
            this.detectionTimeout = null;
        }
        
        // FIX: Force state to active if still transitioning
        if (StateMachine.getState() === 'transitioning-in') {
            console.log('[SimliManager] Forcing state transition to active');
            StateMachine.transitionComplete();
        }
        
        // Tell compositor
        document.dispatchEvent(new CustomEvent('simli-video-ready'));
        
        // Show widget
        this.showWidget();
    },

    showWidget() {
        document.getElementById('simli-mount').classList.add('active');
    },

    hideWidget() {
        document.getElementById('simli-mount').classList.remove('active');
    },

    isVideoReady() {
        return this.videoStreamActive;
    },

    destroyWidget() {
        if (this.detectionTimeout) {
            clearTimeout(this.detectionTimeout);
        }
        this.hideWidget();
        setTimeout(() => {
            document.getElementById('simli-mount').innerHTML = '';
            this.currentWidget = null;
            this.videoStreamActive = false;
            this.updateDebug('-');
        }, 500);
    },

    updateDebug(msg) {
        const el = document.getElementById('debug-simli');
        if (el) el.textContent = msg;
    },

    forceCleanup() {
        if (this.detectionTimeout) clearTimeout(this.detectionTimeout);
        document.getElementById('simli-mount').classList.remove('active');
        document.getElementById('simli-mount').innerHTML = '';
        this.videoStreamActive = false;
    }
};

document.addEventListener('DOMContentLoaded', () => SimliManager.init());

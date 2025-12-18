/**
 * SIMLI INTEGRATION
 * Loads Simli widget but does NOT auto-show
 * Compositor controls when to show based on transition video
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
            const token = await this.getToken(persona.agentId, persona.faceId);
            if (!token) throw new Error('No token');

            console.log('[SimliManager] Token received, creating widget');
            this.updateDebug('creating widget...');

            const widget = document.createElement('simli-widget');
            widget.setAttribute('token', token);
            
            // Set ALL possible attribute formats (Simli docs are inconsistent)
            widget.setAttribute('agentid', persona.agentId);
            widget.setAttribute('agent-id', persona.agentId);
            widget.setAttribute('agentId', persona.agentId);
            if (persona.faceId) {
                widget.setAttribute('faceid', persona.faceId);
                widget.setAttribute('face-id', persona.faceId);
                widget.setAttribute('faceId', persona.faceId);
            }
            
            // Also try setting as properties
            widget.agentId = persona.agentId;
            widget.agentid = persona.agentId;
            if (persona.faceId) {
                widget.faceId = persona.faceId;
                widget.faceid = persona.faceId;
            }
            
            console.log('[SimliManager] Widget set - agentId:', persona.agentId, 'faceId:', persona.faceId);

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
            
            // AGGRESSIVELY remove any buttons that appear
            this.hideSimliButtons();
            
            // FALLBACK: After 10 seconds, mark as ready anyway
            this.detectionTimeout = setTimeout(() => {
                if (!this.videoStreamActive) {
                    console.log('[SimliManager] FALLBACK: Marking ready after timeout');
                    this.updateDebug('fallback ready');
                    this.onVideoReady();
                }
            }, 10000);

            return true;

        } catch (error) {
            console.error('[SimliManager] Error:', error);
            this.updateDebug('error: ' + error.message);
            return false;
        }
    },

    async getToken(agentId, faceId) {
        // Include faceId in token request - Simli may require it
        let url = `${CONFIG.backendUrl}${CONFIG.tokenEndpoint}?agentId=${agentId}`;
        if (faceId) {
            url += `&faceId=${faceId}`;
        }
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
            
            let video = widget.querySelector('video');
            if (!video) video = document.querySelector('#simli-mount video');
            if (!video && widget.shadowRoot) video = widget.shadowRoot.querySelector('video');
            
            if (video) {
                const playing = !video.paused && video.readyState >= 2;
                const hasSize = video.videoWidth > 0;
                const hasSrc = video.src || video.srcObject;
                
                if (hasSrc && (playing || hasSize)) {
                    console.log('[SimliManager] Video stream detected!');
                    this.onVideoReady();
                    return;
                }
            }
            
            if (checks < 100) { // 10 seconds
                setTimeout(check, 100);
            }
        };
        
        setTimeout(check, 1500);
    },

    onVideoReady() {
        if (this.videoStreamActive) return;
        this.videoStreamActive = true;
        
        console.log('[SimliManager] Video ready - notifying compositor');
        this.updateDebug('ready (waiting)');
        
        // Clear fallback timeout
        if (this.detectionTimeout) {
            clearTimeout(this.detectionTimeout);
            this.detectionTimeout = null;
        }
        
        // Just notify - don't show yet! Compositor will decide when
        document.dispatchEvent(new CustomEvent('simli-video-ready'));
    },

    // Called by Compositor when it's time to show
    showWidget() {
        console.log('[SimliManager] Showing widget');
        this.updateDebug('streaming');
        document.getElementById('simli-mount').classList.add('active');
        
        // Focus the widget to enable audio (browser requirement)
        if (this.currentWidget) {
            this.currentWidget.focus();
            this.currentWidget.click();
            console.log('[SimliManager] Widget focused for audio');
        }
    },

    hideWidget() {
        document.getElementById('simli-mount').classList.remove('active');
    },

    isVideoReady() {
        return this.videoStreamActive;
    },

    destroyWidget() {
        console.log('[SimliManager] Destroying widget');
        if (this.detectionTimeout) {
            clearTimeout(this.detectionTimeout);
        }
        
        const mount = document.getElementById('simli-mount');
        
        // IMMEDIATELY hide AND clear - no delay, no chance for dotted face
        mount.classList.remove('active');
        mount.style.opacity = '0';
        mount.style.visibility = 'hidden';
        mount.innerHTML = ''; // Clear immediately
        
        this.currentWidget = null;
        this.videoStreamActive = false;
        this.updateDebug('-');
        
        // Reset styles after a moment
        setTimeout(() => {
            mount.style.opacity = '';
            mount.style.visibility = '';
        }, 500);
    },

    updateDebug(msg) {
        const el = document.getElementById('debug-simli');
        if (el) el.textContent = msg;
    },

    forceCleanup() {
        if (this.detectionTimeout) clearTimeout(this.detectionTimeout);
        if (this.buttonHideInterval) clearInterval(this.buttonHideInterval);
        
        const mount = document.getElementById('simli-mount');
        
        // IMMEDIATELY hide everything
        mount.classList.remove('active');
        mount.style.opacity = '0';
        mount.style.visibility = 'hidden';
        mount.innerHTML = '';
        
        this.currentWidget = null;
        this.videoStreamActive = false;
        this.updateDebug('-');
        
        // Reset styles after transition
        setTimeout(() => {
            mount.style.opacity = '';
            mount.style.visibility = '';
        }, 500);
    },

    // AGGRESSIVELY hide any buttons that Simli might inject
    hideSimliButtons() {
        const hideButtons = () => {
            const mount = document.getElementById('simli-mount');
            if (!mount) return;
            
            // Find ALL buttons
            const buttons = mount.querySelectorAll('button');
            buttons.forEach(btn => {
                // Skip start button on first click
                const text = btn.textContent?.toLowerCase() || '';
                if (text.includes('close') || text.includes('stop') || text.includes('end')) {
                    btn.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;position:absolute!important;left:-9999px!important;';
                    btn.remove(); // Actually remove it
                    console.log('[SimliManager] Removed button:', text);
                }
            });
        };
        
        // Run immediately and repeatedly
        hideButtons();
        this.buttonHideInterval = setInterval(hideButtons, 500);
        
        // Stop after 30 seconds
        setTimeout(() => {
            if (this.buttonHideInterval) {
                clearInterval(this.buttonHideInterval);
            }
        }, 30000);
    }
};

document.addEventListener('DOMContentLoaded', () => SimliManager.init());

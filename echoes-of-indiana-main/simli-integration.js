/**
 * SIMLI INTEGRATION
 * Manages Simli widget - keeps it HIDDEN until video stream is active
 * The transition video stays visible until we detect actual video
 */

const SimliManager = {
    currentWidget: null,
    currentPersona: null,
    isCallActive: false,
    videoStreamActive: false,

    init() {
        console.log('[SimliManager] Initialized');
        document.addEventListener('statechange', (e) => {
            if (e.detail.state === 'transitioning-out') {
                this.destroyWidget();
            }
        });
    },

    async createWidget(personaId) {
        const persona = CONFIG.personas[personaId];
        if (!persona) {
            console.error('[SimliManager] Persona not found:', personaId);
            return false;
        }

        console.log('[SimliManager] Creating widget for', persona.name);

        try {
            const token = await this.getToken(persona.agentId);
            if (!token) throw new Error('Failed to get token');

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

            // Set up listeners and auto-start
            this.setupWidgetListeners(widget);
            this.autoStartCall(widget);
            this.detectVideoStream(widget);

            console.log('[SimliManager] Widget created');
            this.updateDebug('loading');
            return true;

        } catch (error) {
            console.error('[SimliManager] Error:', error);
            this.updateDebug('error');
            return false;
        }
    },

    async getToken(agentId) {
        try {
            const url = `${CONFIG.backendUrl}${CONFIG.tokenEndpoint}?agentId=${agentId}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error('Token request failed');
            const data = await response.json();
            return data.token;
        } catch (error) {
            console.error('[SimliManager] Token error:', error);
            return null;
        }
    },

    setupWidgetListeners(widget) {
        widget.addEventListener('callstart', () => {
            console.log('[SimliManager] Call started');
            this.isCallActive = true;
            this.updateDebug('call-active');
        });

        widget.addEventListener('callend', () => {
            console.log('[SimliManager] Call ended');
            this.isCallActive = false;
            this.videoStreamActive = false;
            this.updateDebug('call-ended');
        });
    },

    autoStartCall(widget) {
        let attempts = 0;
        const tryClick = () => {
            attempts++;
            const btn = widget.querySelector('button') || 
                        document.querySelector('#simli-mount button');
            if (btn) {
                console.log('[SimliManager] Auto-clicking start button');
                btn.click();
                return;
            }
            if (attempts < 50) setTimeout(tryClick, 100);
        };
        setTimeout(tryClick, 500);
    },

    // KEY: Detect when actual video stream starts
    detectVideoStream(widget) {
        let checks = 0;
        const checkVideo = () => {
            checks++;
            
            // Look for video element with actual content
            const video = widget.querySelector('video') || 
                         document.querySelector('#simli-mount video');
            
            if (video) {
                const hasStream = video.srcObject || video.src;
                const isPlaying = !video.paused && video.readyState >= 2;
                const hasSize = video.videoWidth > 0;
                
                if (hasStream && (isPlaying || hasSize)) {
                    console.log('[SimliManager] Video stream detected!');
                    this.videoStreamActive = true;
                    this.onVideoReady();
                    return;
                }
            }
            
            if (checks < 100) setTimeout(checkVideo, 100);
        };
        setTimeout(checkVideo, 1000);
    },

    // Called when video stream is actually ready
    onVideoReady() {
        console.log('[SimliManager] Video ready - showing Simli, hiding transition');
        this.updateDebug('streaming');
        
        // Tell compositor to do the swap
        document.dispatchEvent(new CustomEvent('simli-video-ready'));
        
        // NOW show the Simli mount
        this.showWidget();
    },

    showWidget() {
        const mount = document.getElementById('simli-mount');
        mount.classList.add('active');
        console.log('[SimliManager] Widget shown');
    },

    hideWidget() {
        const mount = document.getElementById('simli-mount');
        mount.classList.remove('active');
        console.log('[SimliManager] Widget hidden');
    },

    isVideoReady() {
        return this.videoStreamActive;
    },

    destroyWidget() {
        if (!this.currentWidget) return;
        console.log('[SimliManager] Destroying widget');
        this.hideWidget();
        setTimeout(() => {
            const mount = document.getElementById('simli-mount');
            mount.innerHTML = '';
            this.currentWidget = null;
            this.currentPersona = null;
            this.isCallActive = false;
            this.videoStreamActive = false;
            this.updateDebug('destroyed');
        }, 500);
    },

    updateDebug(status) {
        const el = document.getElementById('debug-simli');
        if (el) el.textContent = status;
    },

    forceCleanup() {
        const mount = document.getElementById('simli-mount');
        mount.classList.remove('active');
        mount.innerHTML = '';
        this.currentWidget = null;
        this.videoStreamActive = false;
    }
};

document.addEventListener('DOMContentLoaded', () => SimliManager.init());

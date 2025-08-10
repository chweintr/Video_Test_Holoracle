// Enhanced Simli Widget with MP4 Support
// Based on the original but modified to support video files for customimage attribute

// Function to load external script
function loadScript(url) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = url;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// Load Daily.js and initialize the enhanced widget
loadScript("https://unpkg.com/@daily-co/daily-js")
  .then(() => {
    
    // Enhanced Simli Widget class with MP4 support
    class EnhancedSimliWidget extends HTMLElement {
      constructor() {
        super();
        this.attachShadow({ mode: "open" });
        this.isRunning = false;
        this.callManager = null;
      }

      static get observedAttributes() {
        return [
          "token",
          "agentid", 
          "position",
          "customimage",
          "customtext",
          "overlay"
        ];
      }

      addStyles() {
        const position = this.getAttribute("position") || "relative";
        
        const styles = `
          :host {
            display: block;
            position: ${position === "relative" ? "relative" : "fixed"};
            ${position === "left" ? "left: 24px;" : position === "right" ? "right: 24px;" : ""}
            z-index: 9999;
          }

          .widget-container {
            width: 120px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            gap: 12px;
            position: relative;
            transition: width 0.3s ease, height 0.3s ease;
          }

          .widget-container.expanded {
            width: min(420px, calc(100vw - 48px));
          }

          .video-wrapper {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            background-color: black;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
          }

          .simli-video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
          }

          /* Enhanced placeholder styles for both image and video */
          .placeholder-media {
            width: 100%;
            object-fit: cover;
            pointer-events: none;
            border-radius: 12px;
          }

          /* Video-specific styles */
          .placeholder-video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            pointer-events: none;
            border-radius: 12px;
          }

          .control-button {
            padding: 6px 12px;
            font-size: 16px;
            font-weight: 400;
            cursor: pointer;
            background-color: white;
            border-radius: 24px;
            border: none;
            color: black;
            outline: none;
            transition: all 0.1s ease;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
          }

          .control-button:hover {
            border-radius: 4px;
          }

          .control-button.active {
            background-color: #ff0000;
            color: white;
          }

          .controls-wrapper {
            z-index: 2;
          }
        `;

        const styleSheet = document.createElement("style");
        styleSheet.textContent = styles;
        this.shadowRoot.appendChild(styleSheet);
      }

      setupDOMElements() {
        const widgetContainer = document.createElement("div");
        widgetContainer.className = "widget-container";

        const videoWrapper = document.createElement("div");
        videoWrapper.className = "video-wrapper";

        const controlsWrapper = document.createElement("div");
        controlsWrapper.className = "controls-wrapper";

        // Enhanced placeholder creation - supports both images and videos
        this.createPlaceholderElement();

        // Simli video element
        this.video = document.createElement("video");
        this.video.className = "simli-video";
        this.video.autoplay = true;
        this.video.playsInline = true;

        // Audio element
        this.audio = document.createElement("audio");
        this.audio.autoplay = true;

        // Control button
        if (this.getAttribute("overlay") !== "true") {
          this.controlButton = document.createElement("button");
          this.controlButton.className = "control-button";
          this.controlButton.textContent = this.getAttribute("customtext") || "Start";
        }

        // Assemble the DOM
        this.shadowRoot.appendChild(widgetContainer);
        widgetContainer.appendChild(videoWrapper);
        videoWrapper.appendChild(this.placeholderElement);
        videoWrapper.appendChild(this.video);
        videoWrapper.appendChild(this.audio);
        
        if (this.controlButton) {
          widgetContainer.appendChild(controlsWrapper);
          controlsWrapper.appendChild(this.controlButton);
        }
      }

      // Enhanced method to create placeholder element (image or video)
      createPlaceholderElement() {
        const customImageSrc = this.getAttribute("customimage") || "https://app.simli.com/simli-widget/dottedface.gif";
        
        // Check if the customimage is an MP4 file
        if (customImageSrc.toLowerCase().endsWith('.mp4')) {
          console.log('[Enhanced Simli] Creating video placeholder for:', customImageSrc);
          
          // Create video element for MP4
          this.placeholderElement = document.createElement("video");
          this.placeholderElement.className = "placeholder-video";
          this.placeholderElement.src = customImageSrc;
          this.placeholderElement.autoplay = true;
          this.placeholderElement.loop = true;
          this.placeholderElement.muted = true;
          this.placeholderElement.playsInline = true;
          
          // Add error handling for video loading
          this.placeholderElement.addEventListener('error', (e) => {
            console.error('[Enhanced Simli] Video placeholder failed to load:', e);
            // Fallback to default GIF
            this.createFallbackPlaceholder();
          });
          
          this.placeholderElement.addEventListener('loadeddata', () => {
            console.log('[Enhanced Simli] Video placeholder loaded successfully');
          });
          
        } else {
          console.log('[Enhanced Simli] Creating image placeholder for:', customImageSrc);
          
          // Create img element for GIF/PNG/etc
          this.placeholderElement = document.createElement("img");
          this.placeholderElement.className = "placeholder-media";
          this.placeholderElement.src = customImageSrc;
          
          // Add error handling for image loading
          this.placeholderElement.addEventListener('error', (e) => {
            console.error('[Enhanced Simli] Image placeholder failed to load:', e);
            this.createFallbackPlaceholder();
          });
        }
      }

      // Fallback to default dotted face if custom media fails
      createFallbackPlaceholder() {
        console.log('[Enhanced Simli] Using fallback placeholder');
        
        if (this.placeholderElement) {
          this.placeholderElement.remove();
        }
        
        this.placeholderElement = document.createElement("img");
        this.placeholderElement.className = "placeholder-media";
        this.placeholderElement.src = "https://app.simli.com/simli-widget/dottedface.gif";
        
        // Insert it back into the video wrapper
        const videoWrapper = this.shadowRoot.querySelector('.video-wrapper');
        if (videoWrapper) {
          videoWrapper.insertBefore(this.placeholderElement, videoWrapper.firstChild);
        }
      }

      // Simplified call manager for this example
      async connectedCallback() {
        console.log('[Enhanced Simli] Widget connected');
        this.addStyles();
        this.setupDOMElements();

        // Add click handler for control button
        if (this.controlButton) {
          this.controlButton.addEventListener("click", () => {
            if (!this.isRunning) {
              this.startSession();
              this.controlButton.textContent = "Connecting...";
            } else {
              this.stopSession();
            }
          });
        }
      }

      handleConnection() {
        console.log('[Enhanced Simli] Handling connection');
        if (this.controlButton) {
          this.controlButton.textContent = "End";
          this.controlButton.classList.add("active");
        }
        
        const container = this.shadowRoot.querySelector(".widget-container");
        container.classList.add("expanded");
        
        // Hide placeholder when call starts
        if (this.placeholderElement) {
          this.placeholderElement.style.opacity = "0.3";
        }
        
        this.isRunning = true;
        
        // Dispatch custom event for the main app
        this.dispatchEvent(new CustomEvent('callstart', { 
          detail: { persona: this.getAttribute('data-persona') }
        }));
      }

      handleDisconnection() {
        console.log('[Enhanced Simli] Handling disconnection');
        if (this.controlButton) {
          this.controlButton.textContent = this.getAttribute("customtext") || "Start";
          this.controlButton.classList.remove("active");
        }
        
        this.isRunning = false;
        const container = this.shadowRoot.querySelector(".widget-container");
        container.classList.remove("expanded");
        
        // Show placeholder when call ends
        if (this.placeholderElement) {
          this.placeholderElement.style.opacity = "1";
        }
        
        // Clear video sources
        if (this.video) this.video.srcObject = null;
        if (this.audio) this.audio.srcObject = null;
        
        // Dispatch custom event for the main app
        this.dispatchEvent(new CustomEvent('callend', { 
          detail: { persona: this.getAttribute('data-persona') }
        }));
      }

      // Simplified session management for demo
      async startSession() {
        console.log('[Enhanced Simli] Starting session...');
        
        try {
          // Simulate connection process
          setTimeout(() => {
            this.handleConnection();
            
            // Simulate successful connection after 2 seconds
            setTimeout(() => {
              console.log('[Enhanced Simli] Simulated connection successful');
              if (this.placeholderElement) {
                this.placeholderElement.style.display = 'none';
              }
            }, 2000);
            
          }, 500);
          
        } catch (error) {
          console.error('[Enhanced Simli] Session failed:', error);
          this.handleDisconnection();
        }
      }

      stopSession() {
        console.log('[Enhanced Simli] Stopping session...');
        this.handleDisconnection();
        
        // Show placeholder again
        if (this.placeholderElement) {
          this.placeholderElement.style.display = 'block';
          this.placeholderElement.style.opacity = '1';
        }
      }

      disconnectedCallback() {
        console.log('[Enhanced Simli] Widget disconnected');
        this.stopSession();
      }
    }

    // Register the enhanced custom element
    customElements.define("enhanced-simli-widget", EnhancedSimliWidget);
    console.log('[Enhanced Simli] Enhanced widget with MP4 support registered');
    
  })
  .catch((error) => {
    console.error("Failed to load Daily JS:", error);
  });
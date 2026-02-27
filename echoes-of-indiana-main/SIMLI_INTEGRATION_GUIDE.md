# Simli Integration Guide

Based on official Simli documentation research (Nov 2024).

---

## Key Findings

### What Simli Provides

| Feature | Available? | Notes |
|---------|------------|-------|
| Video stream | ✅ Yes | WebRTC or HLS/MP4 |
| Aspect ratio control | ❌ No | Always 16:9 |
| Background color | ❌ No | Must use CSS |
| Transparency/alpha | ❌ No | No alpha channel |
| Pre-built widget | ❌ No | Only raw stream |
| Custom UI | ✅ Yes | You build it |

### Integration Methods

1. **SimliClient (JavaScript SDK)** - Recommended
   - Raw video/audio stream
   - Full control over UI
   - Events for state tracking
   
2. **REST/WebRTC API** - Advanced
   - Returns HLS/MP4 URLs
   - Use with any video player

3. **simli-widget (Marketing Embed)** - NOT recommended
   - For non-technical users
   - Limited control
   - Has unwanted UI elements

---

## Proper Integration (SimliClient)

### Installation

```html
<script src="https://cdn.simli.com/simli-client.js"></script>
```

### Basic Setup

```javascript
const simli = new SimliClient();

// Configure
simli.Initialize({
    apiKey: 'your-api-key',
    faceID: 'face-uuid-here',
    handleSilence: true,
    maxSessionLength: 300,  // seconds
    maxIdleTime: 60,
    videoRef: document.getElementById('simli-video'),
    audioRef: document.getElementById('simli-audio')
});

// Start the session
simli.start();
```

### Available Events

```javascript
simli.on('connected', () => {
    console.log('Session connected, video ready');
});

simli.on('disconnected', () => {
    console.log('Session ended');
});

simli.on('failed', () => {
    console.log('Connection failed');
});

simli.on('speaking', () => {
    console.log('Avatar is speaking');
});

simli.on('silent', () => {
    console.log('Avatar stopped speaking');
});
```

### HTML Structure

```html
<div class="avatar-container">
    <video id="simli-video" autoplay playsinline></video>
    <audio id="simli-audio" autoplay></audio>
</div>
```

### CSS for Square Output (Crop 16:9 → 1:1)

```css
.avatar-container {
    width: 600px;
    height: 600px;
    background: #000000;
    overflow: hidden;
}

#simli-video {
    width: 100%;
    height: 100%;
    object-fit: cover;  /* CROPS to fill container */
    background: #000000;
}
```

---

## Face ID vs Agent ID

| ID Type | Purpose | Used For |
|---------|---------|----------|
| `face_id` | 3D avatar model | Video rendering |
| `agent_id` | Conversational backend | LLM/voice config |

- **Face ID**: Specifies which avatar face to render (UUID)
- **Agent ID**: References your agent config (prompt, voice, etc.)
- Neither controls video dimensions

---

## Making Black Transparent (for LED hologram)

Since Simli has no alpha channel, we use CSS blending:

```css
#simli-video {
    mix-blend-mode: screen;  /* Black becomes transparent */
    background: #000000;
}
```

This works because `screen` blend mode:
- Black (0,0,0) → Transparent
- White (255,255,255) → Fully visible
- Colors → Partially visible

---

## Centering & Scaling the simli-widget (SOLVED)

The `simli-widget` custom element uses Shadow DOM with aggressive internal styling
that makes it very difficult to position/size from the outside. Here's what we
learned and the fix that works.

### The Problem

The widget's shadow DOM sets:
- `:host { position: fixed; bottom: 24px; z-index: 9999; }` — locks to viewport
- `.widget-container { width: 480px; }` — hardcoded container width
- `.video-wrapper { overflow: hidden; border-radius: 12px; }` — clips content

External CSS **cannot** reach into shadow DOM to change these internal styles.
You CAN override `:host` styles by targeting the host element directly from
external CSS (author styles beat `:host` rules per the CSS spec).

### What Does NOT Work

1. **Wrapper div with scale transform** — The widget's `position: fixed` breaks
   out of any wrapper. Even if you override to `position: absolute`, if the wrapper
   has no explicit dimensions, `width: 100%` on the widget resolves to 0.

2. **Shadow DOM style injection** (`widget.shadowRoot.appendChild(style)`) — This
   CAN access the shadow DOM (mode is "open"), but changing the 480px container
   to 100% width breaks the internal layout. The video-wrapper collapses to 0
   height because the video element is `position: absolute` (out of flow).

3. **`position="relative"` attribute** — The widget accepts this and changes
   `:host` to `position: relative`, but it doesn't help with sizing.

### The Fix That Works

**Match the host element's dimensions to the internal 480px container, center it
with translate, and scale it up with CSS transform.**

```css
#simli-container {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

#simli-container simli-widget {
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    width: 480px !important;      /* Match internal container width */
    height: 480px !important;     /* Match internal container height */
    transform: translate(-50%, -50%) scale(2) !important;
    transform-origin: center center !important;
    background: #000 !important;
    mix-blend-mode: screen !important;  /* Black = transparent on OLED */
    overflow: visible !important;
}
```

**Why this works:**
- `position: absolute !important` overrides the shadow DOM's `position: fixed`
  (external author styles beat `:host` rules)
- `width: 480px` matches the internal container, so content isn't clipped or collapsed
- `top: 50%; left: 50%; translate(-50%, -50%)` centers it on screen
- `scale(2)` visually doubles the size (960px rendered)
- No shadow DOM injection needed — pure external CSS

**To adjust size:** Change the `scale()` value:
- `scale(1)` = native 480px
- `scale(1.5)` = 720px
- `scale(2)` = 960px (current touchscreen setting)
- `scale(2.5)` = 1200px

**To adjust position:** Change `top` and `left` percentages, or add
`translateX`/`translateY` to the transform.

### Main Display vs Touchscreen

The main display (`styles.css`) uses a similar pattern but with translate offsets
to position the face off-center (for the layered atmospheric effect):

```css
simli-widget {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    transform: translateX(20%) translateY(6%) scale(1.6) !important;
    transform-origin: center center !important;
}
```

### Alternative: Canvas Approach (Future Option)

For maximum control, hide the original video and draw to your own canvas:

```javascript
const video = widget.shadowRoot.querySelector('video');
video.style.opacity = '0';

const canvas = document.createElement('canvas');
canvas.style.cssText = `
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80vw; height: 80vh;
    object-fit: contain;
`;
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
function draw() {
    if (video.videoWidth) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);
    }
    requestAnimationFrame(draw);
}
draw();
```

This gives complete control over size/position and is the approach used by
HEARSAY (with BlackRemover for background removal). Consider migrating to
this if the CSS transform approach ever breaks due to Simli widget updates.

### Key Simli Widget Facts

- Source: `https://app.simli.com/simli-widget/index.js`
- Shadow DOM mode: **open** (accessible via `.shadowRoot`)
- Observed attributes: `token`, `agentid`, `position`, `customimage`, `customtext`, `overlay`
- Internal classes: `.widget-container`, `.video-wrapper`, `.controls-wrapper`
- Position attribute values: `"left"`, `"right"`, `"relative"` (default = fixed bottom-right)

---

## Current Implementation Status

### What We're Using Now
- `simli-widget` marketing embed with CSS transform overrides
- CSS `mix-blend-mode: screen` for transparent OLED displays
- Auto-click of internal Start button via `tryClickStart()` in JS

### Recommended Migration
1. Switch to SimliClient SDK for full control
2. Or use the canvas approach above for intermediate control
3. Proper event handling for connection states

### TODO
- [ ] Replace simli-widget with SimliClient (or canvas approach)
- [ ] Implement proper event listeners
- [ ] Auto-start on page load
- [ ] Implement idle videos leading in/out of Simli interactions
- [ ] Add atmospheric layers to touchscreen

---

## API Parameters Reference

### Session Start (WebRTC)
- `apiKey` - Your Simli API key
- `faceId` - UUID of avatar face
- `handleSilence` - Handle silent periods
- `maxSessionLength` - Max session duration (seconds)
- `maxIdleTime` - Max idle time before disconnect
- `batchSize` - Audio batch size
- `disableSuperRes` - Disable super resolution

### NOT Available
- aspectRatio ❌
- videoWidth/videoHeight ❌
- backgroundColor ❌
- transparency ❌
- frameRate ❌

---

## Resources

- [Simli Docs](https://docs.simli.com)
- [SimliClient SDK](https://docs.simli.com/javascript-sdk)
- [WebRTC API](https://docs.simli.com/webrtc)
- [Sample Projects](https://github.com/simliai)

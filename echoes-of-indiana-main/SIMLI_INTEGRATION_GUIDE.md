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

## Current Implementation Status

### What We're Using Now
- `simli-widget` marketing embed (not ideal)
- CSS overrides to hide UI elements

### Recommended Migration
1. Switch to SimliClient SDK
2. Use our own `<video>` element
3. Full CSS control without Shadow DOM issues
4. Proper event handling

### TODO
- [ ] Replace simli-widget with SimliClient
- [ ] Implement proper event listeners
- [ ] Auto-start on page load
- [ ] Remove gray bar workarounds

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

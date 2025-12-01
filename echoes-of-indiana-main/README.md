# Echoes of Indiana - Hologram Display System

## Overview

A 4-layer video compositor for LED holographic fan arrays featuring interactive AI personas (powered by Simli).

**Two-Screen Setup:**
- **Hologram Display** (`index.html`) - Pure video output for LED fan array, no UI
- **Kiosk Interface** (TODO) - Touch screen with persona selection grid

---

## 4-Layer Architecture

```
┌─────────────────────────────────────────┐
│  Layer 4: TOP FLOATIES                  │  ← Sparkles, particles (perpetual loop)
├─────────────────────────────────────────┤
│  Layer 3: SIMLI AGENT                   │  ← AI avatar (only during interaction)
├─────────────────────────────────────────┤
│  Layer 2: ABSTRACT LOOPS / TRANSITIONS  │  ← Idle smoke loops + transition videos
├─────────────────────────────────────────┤
│  Layer 1: BOTTOM FLOATIES               │  ← Smoke, embers (perpetual loop)
└─────────────────────────────────────────┘
```

**Key Principle:** All black pixels become transparent via `mix-blend-mode: screen`

---

## File Structure

```
echoes-of-indiana-main/
├── index.html              # Hologram display (pure output)
├── styles.css              # 4-layer styling, black=transparent
├── compositor.js           # Layer orchestration
├── config.js               # Persona configs, video paths
├── state-machine.js        # State management
├── simli-integration.js    # Simli widget/SDK handling
└── assets/videos/
    ├── idle_1.mp4          # Idle loop (abstract smoke)
    └── idle_to_mabel_2.mp4 # Transition: idle → Mabel
```

---

## State Flow

```
IDLE → TRANSITIONING-IN → ACTIVE → TRANSITIONING-OUT → IDLE
        (play video)      (Simli)    (play video)
```

1. **IDLE**: Idle loop videos playing, waiting for invoke
2. **TRANSITIONING-IN**: Play idle-to-persona video while loading Simli
3. **ACTIVE**: Simli agent visible and interactive
4. **TRANSITIONING-OUT**: Play persona-to-idle video, cleanup Simli
5. Back to **IDLE**

---

## Controlling the Hologram Display

### URL Parameters

| Parameter | Effect |
|-----------|--------|
| `?persona=mabel` | Auto-invoke Mabel on load |
| `?debug=true` | Show debug panel |
| `?hidecontrols=true` | Hide Summon/Dismiss buttons |
| `?autostart=true` | Skip "Touch to Begin" overlay |

### JavaScript API

```javascript
Compositor.invokePersona('mabel')  // Start a persona
Compositor.dismissPersona()         // End current session
Compositor.forceReset()             // Emergency reset
```

### PostMessage (from Kiosk)

```javascript
// From kiosk iframe or window:
hologramWindow.postMessage({action: 'invoke', persona: 'mabel'}, '*')
hologramWindow.postMessage({action: 'dismiss'}, '*')
hologramWindow.postMessage({action: 'reset'}, '*')
```

---

## Simli Integration Notes

### Important Constraints (from Simli docs)

- **Video is FIXED 16:9** - No server-side aspect ratio control
- **No transparency** - Must use CSS to handle background
- **No background color control** - Gray bars appear on sides
- **Widget has minimal UI** - Raw stream, we control the interface

### Our Solution

1. Use `object-fit: cover` to crop 16:9 → square (cuts sides slightly)
2. Force black background on all containers
3. `mix-blend-mode: screen` makes black transparent
4. Hide any widget buttons via CSS

### Simli Events (SDK)

- `connected` - Call established
- `disconnected` - Call ended
- `failed` - Connection failed
- `speaking` - Agent is talking
- `silent` - Agent is listening

---

## Adding New Personas

### 1. Create Videos

```
assets/videos/
├── idle_to_[persona].mp4    # Required: transition in
└── [persona]_to_idle.mp4    # Optional: transition out
```

### 2. Add to Config

```javascript
// config.js
personas: {
    newpersona: {
        name: 'Display Name',
        agentId: 'simli-agent-id-here',
        faceId: 'simli-face-id-here',
        videos: {
            idleToActive: 'idle_to_newpersona.mp4',
            activeToIdle: 'newpersona_to_idle.mp4'  // optional
        },
        processingMessages: ['Thinking...', 'Processing...']
    }
}
```

### 3. Add to Kiosk (when built)

Add button to kiosk interface that calls `invokePersona('newpersona')`

---

## Known Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Gray bars on Simli | 16:9 in square container | Use `object-fit: cover` |
| Videos don't autoplay | Browser policy | "Touch to Begin" overlay |
| Mic not working | Permission denied | Grant mic permission in browser |
| Dotted face placeholder | Simli loading state | Hide with CSS or wait for stream |

---

## Production Deployment

### Railway

- Deployed via GitHub push to `main` branch
- URL: `https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/`

### Environment Variables (Railway)

```
SIMLI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # if using voice
```

### For LED Hologram Display

1. Open hologram URL on display computer
2. Grant microphone permissions
3. Use `?autostart=true&hidecontrols=true` for clean output
4. Control via kiosk postMessage or URL params

---

## TODO

- [ ] Build kiosk touch interface
- [ ] Add more personas (Vonnegut, Oracle, Bigfoot)
- [ ] Create persona-to-idle transition videos
- [ ] Add floaties videos (layers 1 & 4)
- [ ] Test on actual LED fan array
- [ ] Fine-tune head positioning/scaling

---

## Quick Test

1. Open: `https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/?debug=true`
2. Click "Touch to Begin"
3. Click "Summon Mabel"
4. Talk to Mabel!
5. Click "Dismiss" to end

# 🚨 CRITICAL - WORKING CONFIGURATION REFERENCE 🚨
**DO NOT LOSE THIS - USE AS PREAMBLE FOR FUTURE CONVERSATIONS**

## 📍 PROJECT LOCATION & SETUP
- **Git Repository**: `E:\Interactive\interactive_project\indiana-oracle-grpc-face\Video_Test_Holoracle`
- **Main Working File**: `main_kiosk.html` (THIS IS THE ACTIVE FILE - NOT index.html)
- **Branch**: `main` 
- **Remote**: `https://github.com/chweintr/Video_Test_Holoracle.git`
- **Deployment**: Railway auto-deploys from main branch

## Current Working State (Updated Aug 12, 2025 - 4 Personas)
- **URL**: https://videotestholoracle-production.up.railway.app/main  
- **Status**: Perfect cube positioning ✅, All 4 personas ✅, Clean mount ✅, Simli sizing fixed ✅
- **Widget Sizing**: Fixed to fill 363x363 mount box (not native size) ✅
- **Last Updated**: Widget position/sizing fixes deployed Aug 12 22:15

## 🔥 WORKING SIMLI CONFIGURATION

### 4 WORKING PERSONAS (CURRENT CONFIG)
```javascript
const CONFIG = {
  personas: {
    bigfoot: {
      name: 'Brown County Bigfoot',
      agentId: '4a857f92-feee-4b70-b973-290baec4d545',
      enhanced: false,
      description: 'Indiana base LM + folklore prompt; SIMLI stock voice/head'
    },
    indiana: {
      name: 'Hoosier Oracle', 
      agentId: 'cd04320d-987b-4e26-ba7f-ba4f75701ebd',  // ✅ WORKING AGENT ID
      faceId: 'd21a631c-28f8-4220-8da3-ea89bc4e5487',   // ✅ WORKING FACE ID
      enhanced: false,
      description: 'Hoosier Oracle with custom agent and face'
    },
    vonnegut: {
      name: 'Kurt Vonnegut',
      agentId: '2970497b-880f-46bb-b5bf-3203dc196db1',
      faceId: 'fde520ba-106d-4529-91b2-fecb04da5257',
      enhanced: true,
      description: 'Vonnegut custom face with comprehensive system prompt and ElevenLabs voice'
    },
    larrybird: {
      name: 'Larry Bird',
      agentId: '126ac401-aaf7-46c3-80ec-02b89e781f25',
      faceId: '1b0eef6f-2650-49ce-a7cd-296d1af0e339',
      enhanced: true,
      description: 'Larry Bird persona with basketball wisdom and Indiana pride'
    }
  }
};
```

### ✅ WORKING SIMLI WIDGET PATTERN (UPDATED AUG 12, 2025)
```javascript
// CRITICAL: This exact pattern works for 363x363 mount sizing
widget.setAttribute('position', 'relative');  // Position relative works best
widget.setAttribute('customtext', ' ');      // Single space instead of empty
widget.setAttribute('customimage', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
widget.setAttribute('hidetrigger', 'true');
widget.setAttribute('autostart', 'true');    // Auto-start to skip buttons

// FORCE sizing with inline styles to override Simli defaults
widget.style.cssText = `
    position: relative !important;
    width: 363px !important;
    height: 363px !important;
    max-width: 363px !important;
    max-height: 363px !important;
    min-width: 363px !important;
    min-height: 363px !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    overflow: hidden !important;
    background: transparent !important;
`;
```

### 🔧 STATUS ELEMENT FIX (CRITICAL)
```javascript
function updateStatus(msg) {
    const statusElement = document.getElementById('status');
    if (statusElement) {
        statusElement.textContent = `System: ${msg}`;
    }
    console.log('[Main Kiosk]', msg);
}
```

## 🚨 KNOWN ISSUES TO FIX

### 1. ✅ Hoosier Oracle Agent ID - FIXED AUG 12, 2025
- **Working Agent ID**: `cd04320d-987b-4e26-ba7f-ba4f75701ebd` (confirmed working)
- **Working Face ID**: `d21a631c-28f8-4220-8da3-ea89bc4e5487` (confirmed working)
- **Status**: Functioning properly as of latest deployment

### 2. ✅ Widget Sizing & Layout Issues - FIXED Aug 12, 2025
- ✅ Mount position: Fixed at 363x363px, top: 206px (full-screen tested)
- ✅ Background scaling: Fixed with `center/100% no-repeat` (no more responsive scaling)
- ✅ Cube alignment: Perfect fit inside glowing cube boundaries
- ✅ Widget sizing: FIXED - widgets now fill 363x363 mount (not native size)
- ✅ Widget position: FIXED - position='relative' prevents right-side drift
- ✅ Clean mount: Removed old spinner/text from center
- ✅ Forced sizing: Inline styles + CSS + post-load enforcement

### 3. Vonnegut Voice Issue
- Agent loads but doesn't respond to voice
- ElevenLabs custom voice blocked by VPN detection
- **Solution**: Use Simli's voice cloning or proxy method

### 4. Widget Sizing Challenge
- Widgets contained in 363x363 mount but getting cropped
- Need same positioning logic as particle video (object-fit: cover)
- **Current approach**: Using particle video methodology with 100% fill + object-fit
- **Fallback**: May need to accept current state if too complex

### 5. Latency Messages - IMPLEMENTATION NOTES
- **Ideal Trigger**: Between user stops talking and agent starts reply
- **Current**: Shows when speechend event fires, hides on audiostart
- **Custom Messages**:
  - Bigfoot: "mulling it over", "pondering in the woods", "considering the question"
  - Hoosier: "hatching an idea", "consulting the corn fields", "gathering wisdom"  
  - Vonnegut: "cooking up a thought", "considering the absurdity", "crafting a response"
  - Larry Bird: "lining up a shot", "sizing up the play", "reading the court"
- **Animation**: Blinking with cycling ellipses, 2-second message rotation

## 🛡️ PRESERVATION STRATEGY

### For Future Claude Instances:
1. **Always read this file first** before making changes
2. **Never modify working agent IDs** without explicit user request
3. **Test on Railway** before pushing changes
4. **Keep backup of working version** in separate file

### Quick Recovery Commands:
```bash
# If buttons stop working, check for status element error
grep -n "updateStatus" main_kiosk.html

# If widgets don't load, verify agent IDs match CONFIG
grep -A 20 "const CONFIG" main_kiosk.html

# If routes don't work, check FastAPI backend
python simli_voice_backend.py  # Should start on port 8083
```

## 🎯 IMMEDIATE NEXT STEPS

1. **Fix Hoosier Oracle agent ID** - Get correct ID from Simli dashboard
2. **Fix visual alignment** - Adjust mount position and screen fit
3. **Document visual fixes** - So they don't get lost in future changes
4. **Test all three personas** - Ensure full functionality

## 📋 WORKING FEATURES (DO NOT BREAK) - 4 PERSONAS
- ✅ Button clicks trigger Simli widgets
- ✅ Bigfoot agent works and responds
- ✅ Hoosier Oracle agent works and responds (FIXED Aug 12)
- ✅ Larry Bird agent works and responds  
- ✅ Vonnegut agent loads (face appears, voice issues remain)
- ✅ Widget sizing constrained to 363x363 mount (FIXED Aug 12)
- ✅ Widget positioning relative (FIXED Aug 12)
- ✅ Status element error fixed
- ✅ Transition animations work
- ✅ Custom UI overlay system
- ✅ Press-to-talk / disconnect buttons

## 🎯 PERFECT MOUNT POSITIONING - GPT-5'S METHODOLOGY ✅

### The Problem
- Original system worked with 2560×1440 background (37.66%, 24.86%, 24.53%)
- Outpainting to eliminate black borders broke positioning
- Different aspect ratios caused mount drift from target cube

### GPT-5's Solution - 3 Cases

**Case 1: Pure Upscale** - Use original percentages
**Case 2: Outpaint with Padding** - Use padding formula  
**Case 3: Recomposition (Most Common)** - Measure directly

### ✅ WORKING SOLUTION: Case 3 Formula
```
For any outpainted image:
1. Measure target area in pixels:
   - x1_px = left edge to target
   - y1_px = top edge to target  
   - w1_px = target width
   
2. Calculate percentages:
   - left% = x1_px / image_width × 100%
   - top% = y1_px / image_height × 100%
   - size% = w1_px / image_width × 100%
```

### 🎯 CURRENT WORKING VALUES (4K Image)
```css
/* 4K Image: new-back-4k.png.png (3840×2160) */
--target-left: 42.08%;  /* 1616px / 3840px × 100% */
--target-top: 33.56%;   /* 725px / 2160px × 100% */
--target-size: 15.86%;  /* 609px / 3840px × 100% */
--design-w: 16; --design-h: 9;  /* Match image aspect ratio */
```

### 📐 Mount System Architecture
```css
/* 16:9 FRAME - Scales perfectly with viewport */
.stage-frame {
    position: fixed;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    width: min(100vw, calc(100vh * (16 / 9)));
    aspect-ratio: 16 / 9;
}

/* MOUNT - Perfect percentage positioning */
.hologram-window {
    position: absolute;
    left: var(--target-left);
    top: var(--target-top);
    width: var(--target-size);
    aspect-ratio: 1 / 1;  /* Perfect square */
    overflow: hidden;
}
```

### 🔑 Key Success Factors
1. **Match container aspect ratio to image** (16:9 for 16:9 image)
2. **Use `object-fit: cover`** for responsive scaling
3. **Measure target precisely** in image editor
4. **Apply Case 3 formula** for pixel-perfect positioning
5. **All child elements inherit mount constraints**

### 🎯 BENEFITS ACHIEVED
- ✅ **No black borders** (4K image fills all screens)  
- ✅ **Perfect mount alignment** (mathematically calculated)
- ✅ **Universal scaling** (works on any screen size)
- ✅ **Element containment** (all layers stay within mount)

## 🚨 CRITICAL REMINDER
**This configuration represents 9+ days of debugging work. Do not modify agent IDs or core widget creation logic without testing on a copy first.**

### 🎯 FOR NEW CLAUDE INSTANCES:
1. **Project Path**: `E:\Interactive\interactive_project\indiana-oracle-grpc-face\Video_Test_Holoracle`
2. **Main File**: `main_kiosk.html` (not index.html)
3. **Current Status**: 4 working personas, widget sizing fixed
4. **Deployment**: Railway auto-deploys from main branch
5. **Always read this file first** to understand current state

---
*Updated: 2025-08-12 22:30 - Updated for 4 personas, current agent IDs, and widget sizing fixes*
*Updated: 2025-08-12 - Added GPT-5's outpaint positioning methodology*
*Keep this file updated with any successful changes*

---

## ✅ Square‑Mount UI (Layout-Only) – Working Positioning Logic

- Route: `/square-mount-ui`
- File: `square_mount_ui.html`
- Backend: `simli_voice_backend.py` → `@app.get("/square-mount-ui")`
- Deployment: Railway main service (same as `/main`), open
  `https://videotestholoracle-production.up.railway.app/square-mount-ui`

What works here
- Unified 16:9 cover stage fills the viewport (no borders), crops edges intentionally
- Background and mount share the same coordinate space; mount stays locked via percentages
- Title, subtitle, persona buttons centered relative to the mount center using
  `--mount-center-x: calc(var(--target-left) + var(--target-size)/2)`
- Text scales with container query units (`cqh/cqw`) so it tracks the stage height on Mac/PC
- Live control panel to tune left/top/size/text scale and copy the resulting CSS

Key CSS (essentials)
```css
.stage { /* 16:9 cover */
  position: fixed; left: 50%; top: 50%; transform: translate(-50%,-50%);
  width: max(100vw, calc(100dvh * 16/9)); aspect-ratio: 16/9;
  container-type: size; overflow: hidden; /* crop edges */
}
.stage > img.bg { width: 100%; height: 100%; object-fit: cover; object-position: center; }
:root {
  --target-left: 37.66%; --target-top: 24.86%; --target-size: 24.53%;
  --mount-center-x: calc(var(--target-left) + var(--target-size)/2);
}
.mount { position: absolute; left: var(--target-left); top: var(--target-top); width: var(--target-size); aspect-ratio: 1/1; }
.title { left: var(--mount-center-x); transform: translateX(-50%); top: 9cqh; }
.subtitle { left: var(--mount-center-x); transform: translateX(-50%); top: 14.5cqh; }
.persona-controls { left: var(--mount-center-x); transform: translateX(-50%); bottom: 10cqh; }
```

How to adjust on any device
1) Open `/square-mount-ui`
2) Use the control panel (top-right) to tweak Left/Top/Size/Text ×
3) Click Copy CSS and paste the variables into `:root` in your layout

Important
- This route is layout-only. It does NOT wire Simli widgets or transitions. The working, fully
  functional system remains at `/main` (`main_kiosk.html`).
- Do not change `/main` for the pitch. Integrate new styling/percentages by copying variables and
  styles from `square_mount_ui.html` when ready.

Open items to integrate later
- Port holographic styles (fonts, buttons, glow) are partially applied; finish tightening to match `/main`
- Wire persona buttons to real actions (current UI route has no widget logic)
- Unify background assets (ensure 16:9 variants to avoid extra math)

---

## Triggers & Overlays Integration Notes (Aug 14, 2025)

- Context: `/transitions` route is the sandbox. `/main` must remain untouched for pitch.
- Stable baseline:
  - 16:9 stage with background image using object-fit: cover
  - Square mount anchored via percentages to the background image
  - Simli widget fills the mount (absolute positioning)
  - Default Simli launcher/flow preserved
  - Gentle feather mask only on the widget container (radial 80%/97%)
  - Overlays (loop/transition) and custom messages currently disabled

- Problems observed when pushing further:
  - Suppressing or auto-starting the widget (hidetrigger/autostart/customimage/customtext) can break initialization due to user-gesture/mic policies and Shadow DOM encapsulation.
  - Overlay layers (loop/transition) can obscure the widget if alpha/blend/z-index aren’t perfect.
  - Aggressive masks (small inner radius) appear as cropping/offset on certain personas.
  - Persona variance: Vonnegut/Larry sometimes show gutters due to internal aspect/padding; mild scale(1.04–1.06) can hide gutters if needed.

- Working constraints:
  - Keep default Simli trigger to satisfy browser gesture requirements
  - Avoid synthetic clicks; no documented start() API
  - Avoid relying on ::part for internal styling
  - Introduce effects incrementally with guardrails

- Safe reintroduction plan:
  1) Feather only: mask inner 80%, outer 97% (no visible cropping). Verify all personas.
  2) Overlay loop: show only after canplay; mix-blend-mode: screen; low opacity (0.3–0.4); pointer-events: none.
  3) Transition overlay: enable after step 2 is stable; preflight asset; hide by timeout/ended; pointer-events: none.
  4) Persona-specific tuning: optional scale(1.04–1.06) for Vonnegut/Larry if gutters seen.
  5) Trigger customization: if desired, set customimage/customtext without suppression; test per persona.

- Current state on `/transitions`:
  - Feather-only mode ON
  - Overlays/messages OFF
  - Default triggers ON

- Action items for coders:
  - If exposing a reliable public start() API or event hooks from the widget is possible, it would simplify choreography.
  - Consider exposing an internal container size/aspect to reduce the need for external scale hacks.
  - Provide guidance on safe use of customimage/customtext with default trigger (timing/ordering).

---

## 🎭 Two-Stage Mystical Flow - PLANNED IMPLEMENTATION (Aug 14, 2025)

**Current Status**: Tagged as `working-proof-of-concept` (stable baseline) before attempting mystical flow

### Concept Overview
Transform the technical limitation of two required clicks into an intentional mystical ritual:

**Stage 1: Summoning Ritual** (when clicking persona button e.g. "Bigfoot")
- ✨ Plays `particles-to-bigfoot.gif` transition overlay 
- 🔮 Shows "Summoning Bigfoot from the ancient forest..." (orange text)
- 🌫️ Base particles fade to 40% opacity during ritual
- ⏱️ Lasts ~2 seconds

**Stage 2: Communion Ready** (after transition)
- 🎯 Simli widget appears with custom trigger: **"Enter Trance"**
- 🌟 Custom trigger image: `distant_light.mp4` (if Simli supports MP4)
- 💫 Shows "Bigfoot awaits... Touch to enter trance" (cyan text, persistent)
- 👆 User clicks the mystical trigger to begin communion

**Stage 3: Thinking Phase** (when widget activates)
- 🧠 Auto-detects when widget starts (experimental polling for video element)
- 💭 Shows "Bigfoot is coming to his senses..." (yellow text)
- 🎭 Alpha overlay provides floating head illusion

### Implementation Notes
- **Benefits**: Makes technical limitation feel like intentional mystical process
- **Failed Attempt**: Undefined `TRANSITIONS` variable caused errors, rolled back
- **Assets Available**: `distant_light.mp4`, `particles-to-bigfoot.gif`, etc. in `/assets`
- **Strategy**: Implement incrementally, test each piece, avoid breaking stable functionality

### Persona-Specific Communion Text
```javascript
const COMMUNION_TEXT = {
  bigfoot: 'Enter Trance',
  indiana: 'Begin Communion', 
  vonnegut: 'Connect Soul',
  larrybird: 'Touch Oracle'
};
```

### Problems Solved vs Outstanding
- ✅ **Mount Alignment**: Square mount perfectly aligned to background target
- ✅ **Alpha Overlay**: Floating head illusion working
- ✅ **Basic Functionality**: Default Simli triggers stable  
- ❌ **Transition Videos**: Need to define `TRANSITIONS` variable properly
- ❌ **Event Detection**: Polling for widget activation needs testing
- ❌ **MP4 Support**: Unknown if Simli `customimage` supports MP4 files

### Next Steps
1. **Define `TRANSITIONS` variable** mapping personas to asset paths
2. **Test minimal mystical trigger text** without transition videos first  
3. **Verify `distant_light.mp4`** works as custom trigger image
4. **Implement incremental pieces** to avoid breaking stable baseline
5. **Document working configuration** for future reference

**Priority**: Keep `/main` untouched for pitch, experiment only on `/transitions` route
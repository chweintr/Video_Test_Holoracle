# 🚨 CRITICAL - WORKING CONFIGURATION REFERENCE 🚨
**DO NOT LOSE THIS - USE AS PREAMBLE FOR FUTURE CONVERSATIONS**

## Current Working State (Updated Aug 12, 2025)
- **URL**: https://videotestholoracle-production.up.railway.app/main  
- **MAIN FILE**: `main_kiosk.html` (THIS IS THE ACTIVE FILE - NOT index.html)
- **Status**: Perfect cube positioning ✅, All 4 personas ✅, Clean mount ✅, Simli sizing fixed ✅
- **Last Updated**: Full-screen tested positioning with forced 363x363 Simli sizing

## 🔥 WORKING SIMLI CONFIGURATION

### Agent IDs (THESE WORK)
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
      agentId: 'd793889d-33ed-44b3-a8b0-e5b9d074e897',  // ✅ CORRECT HOOSIER ORACLE
      faceId: 'afdb6a3e-3939-40aa-92df-01604c23101c',
      enhanced: false,
      description: 'Hoosier Oracle with custom agent and face'
    },
    vonnegut: {
      name: 'Kurt Vonnegut',
      agentId: '2970497b-880f-46bb-b5bf-3203dc196db1',
      faceId: 'fde520ba-106d-4529-91b2-fecb04da5257',
      enhanced: true,
      description: 'Vonnegut custom face with comprehensive system prompt and ElevenLabs voice'
    }
  }
};
```

### ✅ WORKING SIMLI WIDGET PATTERN
```javascript
// CRITICAL: This exact pattern works
widget.setAttribute('position', 'relative');
widget.setAttribute('customtext', ''); 
widget.setAttribute('customimage', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
widget.setAttribute('hidetrigger', 'true');
widget.setAttribute('autostart', 'false');
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

### 1. ✅ Hoosier Oracle Agent ID - FIXED
- **Old**: `76ed1ae8-720c-45de-918c-cac46984412d` (was showing nurse)
- **New**: `d793889d-33ed-44b3-a8b0-e5b9d074e897` (correct Hoosier Oracle)
- **Face ID**: `afdb6a3e-3939-40aa-92df-01604c23101c`

### 2. ✅ Visual/Layout Issues - FIXED Aug 12, 2025
- ✅ Mount position: Fixed at 363x363px, top: 206px (full-screen tested)
- ✅ Background scaling: Fixed with `center/100% no-repeat` (no more responsive scaling)
- ✅ Cube alignment: Perfect fit inside glowing cube boundaries
- ✅ Simli sizing: Forced to exact 363x363px (no more 420x420 cropping)
- ✅ Clean mount: Removed old spinner/text from center

### 3. Vonnegut Voice Issue
- Agent loads but doesn't respond to voice
- ElevenLabs custom voice blocked by VPN detection
- **Solution**: Use Simli's voice cloning or proxy method

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

## 📋 WORKING FEATURES (DO NOT BREAK)
- ✅ Button clicks trigger Simli widgets
- ✅ Bigfoot agent works and responds
- ✅ Vonnegut agent loads (face appears)
- ✅ Status element error fixed
- ✅ Transition animations work
- ✅ Custom UI overlay system
- ✅ Press-to-talk / disconnect buttons

## 🎬 HOLOGRAPHIC TRANSITION SYSTEM - ✅ IMPLEMENTED!
**✅ COMPLETED Aug 12, 2025 - 3-Layer System with Random Video Selection**
**⚠️ FOR FUTURE CLAUDE INSTANCES: USER HAS EXPLAINED THIS VISION 183+ TIMES**

### The Complete Holographic Illusion Flow

#### LAYER SYSTEM (Z-INDEX ORDER - BOTTOM TO TOP):
1. **LAYER 1 (Base)**: Constant particle animation loop (ALWAYS running)
2. **LAYER 2 (Background)**: Simli agent (HIDDEN initially, loads silently)
3. **LAYER 3 (Foreground)**: Transition videos (particles-to-X, X-to-particles)

#### USER INTERACTION FLOW:

**1. IDLE STATE:**
- Base particle loop plays constantly in holographic box
- No Simli agents visible
- User sees: Continuous particle animation

**2. USER SELECTS ORACLE (e.g., "Bigfoot"):**
- **Background**: Simli Bigfoot agent loads SILENTLY (hidden behind transition)
- **Foreground**: Random "particles-to-bigfoot" video plays ONCE (no loop)
- User sees: Particles morphing into Bigfoot shape
- **When transition completes**: Video disappears, revealing Simli Bigfoot in EXACT same spot

**3. CONVERSATION STATE:**
- Base particles: Still looping (hidden)
- Simli agent: Visible and interactive
- User sees: Bigfoot responding to voice

**4A. USER ENDS CONVERSATION:**
- **Foreground**: Random "bigfoot-to-particles" video plays ONCE (no loop) 
- **When transition completes**: Video disappears, revealing base particle loop
- Simli agent: Destroyed/cleaned up
- User sees: Bigfoot dissolving back into particles

**4B. USER SWITCHES ORACLES (e.g., "Vonnegut"):**
- **Background**: Simli Vonnegut loads SILENTLY while Bigfoot still visible
- **Foreground**: Random "particles-to-KVJ" video plays ONCE
- **Immediately after**: Old Simli (Bigfoot) destroyed
- **When transition completes**: Video disappears, revealing Vonnegut in EXACT same spot

### 🎲 VARIETY SYSTEM - MULTIPLE TRANSITION OPTIONS
**Current Video Bank** (as of Aug 12, 2025):
```
# Bigfoot variations
particles-to-bigfoot.gif
particles-to-bigfoot-alt.mp4

# Hoosier Oracle variations  
particles-to-Hoosier-Oracle.mp4
Hoosier-Oracle-to-particles.mp4
Hoosier-Oracle-to-particles-2.mp4

# Vonnegut (KVJ) variations
particles-to-KVJ.mp4
KVJ-to-particles.mp4

# Base particle loops
particles-to-particles-2.mp4
particles-to-particles-3.mp4
particles-to-particles-4.mp4
particles-swirl-simple.mp4
```

#### Random Selection Logic:
```javascript
const transitions = {
    bigfoot: {
        morphIn: ['particles-to-bigfoot.gif', 'particles-to-bigfoot-alt.mp4'],
        morphOut: ['bigfoot-to-particles.mp4'] // Add more as created
    },
    indiana: {
        morphIn: ['particles-to-Hoosier-Oracle.mp4'],
        morphOut: ['Hoosier-Oracle-to-particles.mp4', 'Hoosier-Oracle-to-particles-2.mp4']
    },
    vonnegut: {
        morphIn: ['particles-to-KVJ.mp4'],
        morphOut: ['KVJ-to-particles.mp4']
    }
};

function getRandomTransition(persona, type) {
    const options = transitions[persona][type];
    return options[Math.floor(Math.random() * options.length)];
}
```

### ✅ IMPLEMENTATION STATUS - ALL REQUIREMENTS MET:
- ✅ **NO LOOPS** on transition videos (particles-to-X, X-to-particles)
- ✅ **EXACT POSITIONING** - All agents appear in identical spot
- ✅ **SEAMLESS ILLUSION** - No visible loading, no positioning jumps
- ✅ **LAYER COORDINATION** - Perfect timing between video end and reveal
- ✅ **SILENT LOADING** - Simli agents load hidden, appear only after transition
- ✅ **RANDOM VARIETY** - Different transitions each time for natural experience
- ✅ **Z-INDEX LAYERING** - Perfect layer coordination implemented
- ✅ **TRANSITION FUNCTIONS** - playTransition(), transitionToPersona(), transitionFromPersona()
- ✅ **HIDDEN WIDGET LOADING** - createSimliWidgetHidden(), revealSimliAgent()

**🎯 ACHIEVED: Perfect holographic illusion where particles seamlessly become personas with natural variety**

### 📂 IMPLEMENTATION FILES:
- **main_kiosk.html** - Complete 3-layer system (feature/transition-experiments branch)
- **Layer 3 CSS**: .transition-layer, .transition-video with z-index: 15
- **JS Functions**: TRANSITIONS config, getRandomTransition(), playTransition()
- **Hidden Loading**: createSimliWidgetHidden() loads agents behind transitions
- **Perfect Reveal**: revealSimliAgent() shows agents in exact transition end spot

## 🚨 CRITICAL REMINDER
**This configuration represents 9 days of debugging work + 3 weeks of platform-level struggles. The alignment and voice issues are largely PLATFORM LIMITATIONS, not implementation bugs.**

---
*Updated: 2025-08-12 - Added complete transition vision with variety system*
*Keep this file updated with any successful changes*
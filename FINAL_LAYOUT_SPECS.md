# Echoes of Indiana - Final Layout Specifications

## Project Overview
**Echoes of Indiana** is a holographic oracle kiosk featuring 3 AI personas with interactive avatars powered by Simli SDK and deep RAG systems. This document captures the final working configuration after extensive testing and positioning adjustments.

## Final Perfect Layout Values ✅

### CSS Positioning (Full-screen tested absolute positioning)
```css
.title { top: 45px; } /* "Echoes of Indiana" */
.subtitle { top: 105px; } /* "Holographic Conversations Powered by Research" */
/* NEW TAGLINE */ { top: 130px; } /* "Compelled by Curiosity" */
/* BOTTOM TAGLINE */ { top: 150px; } /* "Brought to you by Past Presence" */
.hologram-window { top: 206px; width: 363px; height: 363px; } /* PERFECT: Full-screen tested cube fit */
.persona-controls { top: 720px; }
#selectOracleText { top: 770px; }
```

### Element Specifications (Updated Aug 12, 2025)
- **Title**: "Echoes of Indiana" at 45px from top
- **Subtitle**: "Holographic Conversations Powered by Research" at 105px
- **Tagline 1**: "Compelled by Curiosity" at 130px (ADDED)
- **Tagline 2**: "Brought to you by Past Presence" at 150px (MOVED)
- **Mount**: Fixed 363x363px hologram display at 206px (full-screen tested perfect fit)
- **Buttons**: 4 persona controls at 720px (added Larry Bird)
- **Select Text**: "Select Oracle" prompt at 770px (bottom guide only - removed from mount center)

## Persona Configuration

### Agent IDs and Face IDs (Working Configuration)
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
            agentId: 'cd04320d-987b-4e26-ba7f-ba4f75701ebd',  // Updated Dec 2024
            faceId: 'd21a631c-28f8-4220-8da3-ea89bc4e5487',
            enhanced: false,
            description: 'Hoosier KB with system prompt; SIMLI stock voice/head'
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

## CSS Adjuster Tool Pattern 🛠️

### Problem Solved
During development, we encountered a critical issue where the local cached version showed perfect layout while the deployed version showed broken positioning. This led to time-consuming trial-and-error deployment cycles.

### Solution: Live CSS Adjustment Tool
Created a toggleable CSS adjuster that allows real-time positioning changes without deployments:

```html
<!-- LIGHTWEIGHT CSS ADJUSTER - Press 'C' to toggle -->
<div id="cssAdjuster" style="
    position: fixed;
    top: 10px;
    right: 10px;
    background: rgba(0,0,0,0.95);
    color: #00ffff;
    padding: 15px;
    border: 2px solid #00ffff;
    border-radius: 8px;
    font-family: monospace;
    font-size: 12px;
    z-index: 9999;
    display: none;
    width: 200px;
">
    <div style="font-weight: bold; margin-bottom: 8px; font-size: 13px;">🎯 Live Adjuster</div>
    Title: <input type="number" id="titleAdjust" value="45" style="width: 50px; padding: 2px;"><br>
    Subtitle: <input type="number" id="subtitleAdjust" value="105" style="width: 50px; padding: 2px;"><br>
    Mount: <input type="number" id="mountAdjust" value="195" style="width: 50px; padding: 2px;"><br>
    Buttons: <input type="number" id="buttonsAdjust" value="720" style="width: 50px; padding: 2px;"><br><br>
    <button onclick="applyQuickFix()" style="background: #00ffff; color: black; padding: 5px 10px; border: none; font-size: 11px; font-weight: bold;">APPLY ALL</button>
    <div style="margin-top: 8px; font-size: 9px; color: #888;">Press 'C' to hide</div>
</div>
```

### JavaScript Implementation
```javascript
// Enhanced CSS adjuster function
function applyQuickFix() {
    const titleTop = document.getElementById('titleAdjust').value;
    const subtitleTop = document.getElementById('subtitleAdjust').value;
    const mountTop = document.getElementById('mountAdjust').value;
    const buttonsTop = document.getElementById('buttonsAdjust').value;
    
    document.querySelector('.title').style.top = titleTop + 'px';
    document.querySelector('.subtitle').style.top = subtitleTop + 'px';
    document.querySelector('.hologram-window').style.top = mountTop + 'px';
    document.querySelector('.persona-controls').style.top = buttonsTop + 'px';
    document.getElementById('selectOracleText').style.top = (parseInt(buttonsTop) + 50) + 'px';
    
    console.log(`🎯 Applied: Title=${titleTop}, Subtitle=${subtitleTop}, Mount=${mountTop}, Buttons=${buttonsTop}`);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'C' to toggle CSS adjuster
    if (e.key.toLowerCase() === 'c') {
        const adjuster = document.getElementById('cssAdjuster');
        adjuster.style.display = adjuster.style.display === 'none' ? 'block' : 'none';
    }
});
```

### Benefits of This Pattern
1. **No Deployment Cycles**: Test positioning changes instantly
2. **Multiple Device Testing**: Adjust layout while viewing on different devices
3. **Rapid Iteration**: Find perfect values through real-time adjustment
4. **Cache-Independent**: Works regardless of browser caching issues
5. **Lightweight**: Minimal code footprint, toggleable visibility

## Technical Architecture

### Key Design Decisions
- **Absolute Positioning**: Enables independent control of each element
- **Fixed Mount Size**: 380x380px prevents scaling issues
- **Simli Widget Integration**: Let Simli handle its own positioning within the mount
- **Background**: `assets/new-back.png` - holographic cube with neon glow
- **Cache Busting**: Meta tags prevent browser caching during development

### Deployment Notes
- **Platform**: Railway (https://videotestholoracle-production.up.railway.app/)
- **Branch**: main
- **Cache Issues**: Local vs deployed versions may differ due to browser caching
- **Testing**: Always verify on multiple devices/browsers after deployment

## Scaling Vision: Past Presence Business Model

### Future Implementations
- **Echoes of Uppsala**: Swedish historical figures and locations
- **Echoes of Appalachia**: Regional folklore and cultural figures  
- **Institutional Applications**: Universities, museums, cultural centers

### Technology Stack
- **Physical Holograms**: Holographic display hardware
- **Interactive Avatars**: Simli SDK for realistic AI personas
- **Deep RAG Systems**: Location-specific knowledge bases
- **Responsive Design**: Multi-device compatibility

## File Structure
```
Video_Test_Holoracle/
├── main_kiosk.html                 # Primary interface
├── assets/
│   ├── new-back.png               # Holographic background
│   ├── bigfoot-overlay.png        # Bigfoot persona overlay
│   └── [video assets]             # Particle transition videos
├── measure_layout.html            # Layout measurement tool
└── FINAL_LAYOUT_SPECS.md         # This documentation
```

## Critical: ElevenLabs API Key for Custom Voices

### The Problem
Custom voices (Hoosier Oracle, Larry Bird) won't work without including the ElevenLabs API key in Simli session tokens.

### The Solution
The backend must send BOTH keys when creating tokens:
```json
{
    "simliAPIKey": "your-simli-key",
    "ttsAPIKey": "your-elevenlabs-key"  // REQUIRED for custom voices
}
```

### Environment Setup
1. **Railway**: Set `ELEVENLABS_API_KEY` environment variable
2. **Use Same Key**: Use the exact same ElevenLabs API key you use in Simli
3. **Backend Fix**: `simli_voice_backend.py` now includes ttsAPIKey in token creation

### Why This Matters
Per Simli support: "The elevenlabs api key and the LLM api key are not stored with the agent config, they're stored in the session token."

## Troubleshooting

### Common Issues
1. **Widget appears tiny on side**: Remove forced Simli positioning, let widget self-position
2. **Layout broken after changes**: Use CSS adjuster to find correct values
3. **Cache showing old version**: Clear browser cache or test incognito
4. **Mount positioning off**: Use absolute positioning with fixed pixel values

### Debug Tools
- CSS Adjuster (Press 'C' to toggle)
- Console logging for persona switching
- Layout measurement tool (`measure_layout.html`)

---

## 🚨 CRITICAL RECENT FIXES (Aug 12, 2025)

### Background Scaling Issue FIXED
- **Problem**: Mount stayed fixed pixels while background image scaled with window resize
- **Solution**: Changed background from `center/cover` to `center/100% no-repeat fixed`
- **Result**: Both background and mount now stay perfectly aligned

### Simli Widget Sizing Issue FIXED  
- **Problem**: Simli agents naturally 420x420, causing cropping in 363x363 mount
- **Solution**: Force exact sizing with `width: 363px !important` and `object-fit: fill`
- **Result**: No more cropping, perfect fit within cube boundaries

### Mount Center Cleanup
- **Removed**: Old spinning icon and "Select Oracle" text from mount center
- **Kept**: Clean particle background and bottom guide text only
- **Result**: Unobstructed mount for Simli content

### Complete Tagline Sequence
1. "Echoes of Indiana"
2. "Holographic Conversations Powered by Research"  
3. "Compelled by Curiosity" (was missing)
4. "Brought to you by Past Presence"

---
*This document represents the final working configuration after extensive testing and user feedback. The CSS adjuster pattern proved invaluable for rapid iteration and should be considered for similar projects requiring precise positioning.*

**⚠️ IMPORTANT FOR FUTURE CLAUDE INSTANCES:**
- **Main file is `main_kiosk.html`** (not index.html)
- **Always test in full-screen mode** for accurate positioning
- **Use live CSS adjuster (press 'C')** before making code changes
- **Current positioning is optimized for full-screen demo presentation**
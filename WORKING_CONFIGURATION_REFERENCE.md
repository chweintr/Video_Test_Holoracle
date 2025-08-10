# 🚨 CRITICAL - WORKING CONFIGURATION REFERENCE 🚨
**DO NOT LOSE THIS - USE AS PREAMBLE FOR FUTURE CONVERSATIONS**

## Current Working State (Railway Rollback)
- **URL**: https://videotestholoracle-production.up.railway.app/main
- **Status**: Buttons working, Bigfoot ✅, Vonnegut ✅, Hoosier ✅ (FIXED with correct agent)
- **Date Rolled Back To**: Earlier today when buttons were functional

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

### 2. Visual/Layout Issues
- Mount position wrong (too high/low)
- Website doesn't fit screen properly
- Background alignment issues

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

## 🚨 CRITICAL REMINDER
**This configuration represents 9 days of debugging work. Do not modify agent IDs or core widget creation logic without testing on a copy first.**

---
*Generated: 2025-08-10 - Rolled back to working state*
*Keep this file updated with any successful changes*
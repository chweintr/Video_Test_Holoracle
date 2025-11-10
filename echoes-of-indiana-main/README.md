# Echoes of Indiana - LED Hologram Compositor

**Trades District - Bloomington, Indiana**

A 3-layer video compositor system for LED fan array holograms featuring historical Indiana personas.

---

## 🎯 Project Overview

This system creates interactive holographic experiences using:
- **Layer 1 (Below)**: Transition videos & background atmosphere
- **Layer 2 (Middle)**: Simli AI avatar (interactive)
- **Layer 3 (Above)**: Overlay effects (smoke, holographic elements)

All layers use **black backgrounds with alpha transparency** for LED hologram compositing.

---

## 📁 File Structure

```
echoes-of-indiana-main/
├── index.html              # Main HTML structure
├── styles.css              # Black/alpha compositor styling
├── config.js               # Persona configurations
├── state-machine.js        # State management
├── simli-integration.js    # Simli widget management
├── compositor.js           # Main orchestration
├── README.md               # This file
└── assets/
    ├── videos/             # Your alpha video files go here
    │   ├── mabel-idle-to-active.mp4
    │   ├── mabel-active-to-idle.mp4
    │   ├── mabel-background.mp4 (optional)
    │   └── mabel-overlay.mp4 (optional)
    └── audio/              # Optional audio assets
```

---

## 🎬 State Flow

1. **IDLE**: User sees persona selection screen
2. **TRANSITIONING-IN**: Plays `idle-to-active` video, loads Simli widget
3. **ACTIVE**: Simli avatar appears, background/overlay loops play, user can interact
4. **PROCESSING**: While AI thinks, shows processing message overlay
5. **TRANSITIONING-OUT**: Plays `active-to-idle` video, cleans up
6. **Back to IDLE**

---

## ⚙️ Setup Instructions

### 1. Add Your Videos

Drop your alpha-channel videos into `assets/videos/`:

**Required:**
- `mabel-idle-to-active.mp4` - Transition from idle to Mabel

**Optional:**
- `mabel-active-to-idle.mp4` - Transition back to idle
- `mabel-background.mp4` - Background atmosphere loop
- `mabel-overlay.mp4` - Top layer effects

### 2. Configure Mabel's Simli Credentials

Edit `config.js` and update:

```javascript
personas: {
    mabel: {
        agentId: 'YOUR_MABEL_AGENT_ID_HERE',  // ← Replace this
        faceId: null,  // ← Add if using Compose API
        // ...
    }
}
```

**Where to find your Agent ID:**
- Log into Simli dashboard
- Find Mabel's agent
- Copy the Agent ID (looks like: `4a857f92-feee-4b70-b973-290baec4d545`)

### 3. Set Railway Environment Variables

In your Railway project settings, add:

```
SIMLI_API_KEY=your_simli_api_key_here
OPENAI_API_KEY=your_openai_key_here  (if using voice)
```

### 4. Backend Integration

This project reuses the existing backend from the parent repo:
- Backend: `/simli_voice_backend.py`
- Token endpoint: `GET /simli-token?agentId={agentId}`

**If deploying separately**, update `config.js`:

```javascript
backendUrl: 'https://your-backend-url.railway.app',
```

### 5. Deploy to Railway

**Option A: Deploy with existing backend**
- Place this folder inside `Video_Test_Holoracle/`
- Railway will serve both projects
- Access at: `https://your-app.railway.app/echoes-of-indiana-main/`

**Option B: Deploy as separate project**
- Create new Railway project
- Include `simli_voice_backend.py` in this folder
- Update `backendUrl` in `config.js`

---

## 🎨 Adding More Personas

### Step 1: Add Videos

Create videos with alpha channels:
- `[persona]-idle-to-active.mp4`
- `[persona]-active-to-idle.mp4` (optional)
- `[persona]-background.mp4` (optional)
- `[persona]-overlay.mp4` (optional)

Place in `assets/videos/`

### Step 2: Add to Config

Edit `config.js` and add persona:

```javascript
personas: {
    mabel: { /* ... */ },

    // New persona:
    'hoosier-oracle': {
        name: 'Hoosier Oracle',
        fullTitle: 'Echoes Guide',
        quote: '"Ask your question; I will route you to stone, rail, factory, or code."',
        agentId: 'YOUR_ORACLE_AGENT_ID',
        faceId: null,
        videos: {
            idleToActive: 'oracle-idle-to-active.mp4',
            activeToIdle: 'oracle-active-to-idle.mp4',
            background: null,
            overlay: null,
        },
        processingMessages: [
            'Oracle is routing your query...',
            'Oracle is consulting the echoes...',
        ],
        simliPosition: {
            top: '50%',
            left: '50%',
            width: '600px',
            height: '600px',
        }
    }
}
```

### Step 3: Add Button to HTML

Edit `index.html` and uncomment/add button:

```html
<button class="persona-btn" data-persona="hoosier-oracle">
    <span class="persona-name">Hoosier Oracle</span>
    <span class="persona-title">Echoes Guide</span>
    <span class="persona-quote">"Ask your question..."</span>
</button>
```

---

## 🐛 Debugging

### Debug Panel

The debug panel (top-left corner) shows:
- Current state
- Active persona
- Simli widget status

**To hide in production**: Set in `config.js`:

```javascript
ui: {
    showDebugPanel: false,
}
```

### Browser Console

Open DevTools Console to see detailed logs:
- `[StateMachine]` - State transitions
- `[SimliManager]` - Widget lifecycle
- `[Compositor]` - Video layer management

### Common Issues

**Video not playing:**
- Check file path in `config.js`
- Verify video exists in `assets/videos/`
- Check browser console for errors

**Simli not loading:**
- Verify Agent ID in `config.js`
- Check Railway environment variables
- Check backend token endpoint is responding

**Black screen:**
- Ensure videos have alpha channels
- Check video codec (H.264 with alpha recommended)

---

## 🎛️ Customization

### Positioning Simli Avatar

Adjust where Simli appears in `config.js`:

```javascript
simliPosition: {
    top: '40%',       // Vertical position
    left: '50%',      // Horizontal position
    width: '800px',   // Avatar size
    height: '800px',
}
```

### Processing Messages

Customize what users see while AI is thinking:

```javascript
processingMessages: [
    'Mabel is checking the grain...',
    'Mabel is counting the pieces...',
    // Add more variations
]
```

Messages rotate every 5 seconds (configurable in `timing.processingMessageRotateInterval`)

### Styling

Edit `styles.css` to customize:
- Persona selection UI
- Processing message appearance
- Video layer blend modes
- Button styles

---

## 🚀 Current Status

### ✅ Completed
- 3-layer video compositor
- State machine (idle → transition → active → dismiss)
- Simli integration with token generation
- Processing message system
- Persona selection interface
- Debug panel

### 📋 To Do
- [ ] Add Mabel's Agent ID to `config.js`
- [ ] Upload Mabel's videos to `assets/videos/`
- [ ] Test with actual hologram hardware
- [ ] Add remaining personas (Vonnegut, Hoosier Oracle, etc.)
- [ ] Fine-tune Simli positioning based on video alignment

---

## 📞 Personas Palette

**Currently Implemented:**
- ✅ Mabel (Showers Finishing Worker, 1917)

**Planned:**
- Hoosier Oracle (Echoes Guide)
- Kurt Vonnegut (Author)
- Brown County Bigfoot (Trail Sage)
- Larry Bird (Basketball Legend)
- Madam C.J. Walker (Entrepreneur)
- And 10+ more...

---

## 🔧 Technical Notes

### Video Requirements
- **Codec**: H.264 with alpha channel (or VP9/WebM)
- **Background**: Pure black (#000000) or transparent
- **Resolution**: 1080x1080 or higher (square recommended)
- **Frame rate**: 30fps or 60fps

### Browser Compatibility
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ⚠️ May need WebM format for alpha

### Performance
- LED holograms require smooth 60fps playback
- Use compressed videos (H.264 High Profile)
- Preload critical videos

---

## 📝 License & Credits

**Project**: Echoes of Indiana
**Location**: Trades District, Bloomington, Indiana
**Technology**: Simli AI, LED Fan Array Holograms

---

## 🆘 Support

For issues or questions:
1. Check browser console for errors
2. Verify all videos are in place
3. Confirm Simli Agent IDs are correct
4. Check Railway environment variables

---

**Ready to bring history to life! 🎭**

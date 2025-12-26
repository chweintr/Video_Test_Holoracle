# Echoes of Indiana

> *History is not just what happened. It is who was there.*

---

## 🌐 Vision

**Echoes of Indiana** is an interactive heritage installation where visitors converse with holographic personas from the state's layered past. Rather than reading plaques or watching videos, people engage in real-time dialogue — asking questions that textbooks cannot answer: *What did the sawdust smell like? Were you afraid? What did you dream about?*

Each persona is powered by contextual AI, period-accurate voice synthesis, and expressive avatar technology. The result is not a chatbot. It is an **encounter**.

### Part of PastPresence

Echoes of Indiana is the flagship installation of **PastPresence**, a platform for history through encounter, not observation. The framework is designed to scale regionally — *Echoes of Uppsala*, *Echoes of Appalachia*, and other installations can deploy the same architecture with localized personas and narratives.

**Companion projects** like **VonneBot** extend the model to literature, letting readers engage with AI embodiments of authors while reading their work.

---

## 🎭 Persona Categories

The roster spans four categories, capturing the full spectrum of Hoosier experience:

| Category | Description |
|----------|-------------|
| **Archetypes** | Composite everyday Hoosiers — working lives, local voices, the people history often forgets |
| **Historical Figures** | Notable Hoosiers who have passed — artists, activists, innovators, icons |
| **Living Legends** | Famous Hoosiers still with us — their stories ongoing |
| **Lore** | Folklore, curiosities, the unexplained — the stories whispered, not written |

---

## 👥 Current Roster

### ✅ Active (Simli-powered, ready to converse)

| Name | Role | Category |
|------|------|----------|
| **Mabel** | Showers Brothers Furniture Worker, 1917 | Archetype |
| **Tomaz** | Limestone Channeler, 1923 | Archetype |
| **Hazel** | RCA Quality Control Inspector, 1958 | Archetype |
| **James Whitcomb Riley** | The Hoosier Poet, 1849-1916 | Historical |
| **Brown County Bigfoot** | Trail Sage & Cryptid Teller | Lore |

### 📋 Planned Personas

**ARCHETYPES**
- Nell — Showers Tube Runner, 1918
- Mae — Monon Depot Clerk, 1918
- Eddie — Showers Pond Kid, 1910s
- Cyril — Town Rider, Late 1970s
- Elsie — Switchyard Hostler, Mid Century
- CCC Worker — Brown County Conservation, 1930s

**HISTORICAL FIGURES**
- Kurt Vonnegut — Indianapolis Author
- Hoagy Carmichael — Stardust Composer
- James Dean — Rebel from Fairmount
- Madam C.J. Walker — Entrepreneur
- Wes Montgomery — Jazz Guitarist
- Alfred Kinsey — IU Sexologist
- Herman B Wells — IU President
- Elinor Ostrom — Nobel Economist
- Carole Lombard — Screwball Actress
- Vivian Carter — Vee-Jay Records
- Ryan White — AIDS Activist
- George Rogers Clark — Revolutionary War Hero
- Ernie Pyle — War Correspondent
- Oscar Charleston — Negro League Legend

**LIVING LEGENDS**
- Larry Bird — French Lick Legend
- John Mellencamp — Seymour Rocker
- David Letterman — Late-Night Legend
- Angela Brown — Opera Singer

**LORE**
- Lil Bub — Internet Sensation
- Hoosier Oracle — Echoes Guide/Router (meta-persona)

---

## 🖥️ How It Works

1. **Kiosk Interface** — Visitors select a persona from animated circular portraits
2. **Transition Video** — A cinematic reveal as the persona materializes
3. **Holographic Conversation** — Real-time AI dialogue via Simli talking-head technology
4. **Dismiss & Return** — End the encounter, return to selection

The display architecture uses a **video sandwich** — idle loops, transition animations, and the Simli avatar layered with blend modes for a seamless holographic effect.

---

## 🎨 Aesthetic

Baroque. Theatrical. Neon tubing on velvet curtains. Tom Waits meets Thom Browne meets Delicatessen. Not clean, not minimal — stylized strangeness that honors the uncanny nature of talking to the past.

---

# Technical Documentation

---

## 🤖 FOR FUTURE AI ASSISTANTS (READ THIS FIRST!)

**Last Updated:** December 6, 2025

### Current Status: ✅ MOSTLY WORKING
- Mabel loads and streams correctly
- State machine works (idle → transitioning-in → active → idle)
- Dismiss button works
- No gray bars on Simli output
- Video sandwich layers working (idle visible under Simli)

### What We're Working On NOW:
1. **HEAD POSITIONING** - Aligning Simli head with transition video's final frame
   - Use the **CALIBRATION TOOL**: `?calibrate` URL parameter
   - Current calibrated values: `translateX(22%) translateY(6%) scale(1.6)`
   - This is still approximate - video disappears when Simli loads, making exact alignment tricky

### 🔧 CALIBRATION TOOL (IMPORTANT!)

To align Simli head with video head:

```
https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/?calibrate
```

This shows an interactive panel:
- **Scale [−] [+]** → Make Simli bigger/smaller
- **Move X [←] [→]** → Move left/right  
- **Move Y [↑] [↓]** → Move up/down

After adjusting, copy the CSS transform value and update `styles.css` → `simli-widget` selector.

### Key Files:
| File | Purpose |
|------|---------|
| `styles.css` | **HEAD POSITIONING** - `simli-widget` transform values |
| `config.js` | Mabel's agentId, faceId, video paths |
| `compositor.js` | Layer orchestration, video playback |
| `simli-integration.js` | Simli widget creation |

### Current Mabel Config (config.js):
```javascript
agentId: '2c8b6f6d-cb83-4100-a99b-ee33f808069a'
faceId: '33622e5c-6107-4da0-9794-8ea784ccdb43'
```

### Current Simli Transform (styles.css):
```css
simli-widget {
    transform: translateX(22%) translateY(6%) scale(1.6) !important;
}
```

### Railway Quirk ⚠️
Railway sometimes adds trailing spaces to env var names. The backend has a workaround (`get_simli_api_key()` function) that handles this. If API key issues occur, check `/debug-env` endpoint.

### Test URLs:
- **Normal**: `https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/`
- **With calibration panel**: `...?calibrate`
- **With measurement grid**: `...?measure`

---

## Simli Integration Approach

We use the **Simli Widget** method (simplest approach):

### 1. Load Widget Script (index.html)
```html
<script src="https://app.simli.com/simli-widget/index.js" defer></script>
```

### 2. Backend: Generate Token (simli_voice_backend.py)
```python
response = requests.post(
    "https://api.simli.ai/getToken",
    json={"apiKey": SIMLI_API_KEY}
)
token = response.json()["token"]
```

### 3. Frontend: Create Widget (simli-integration.js)
```javascript
const widget = document.createElement('simli-widget');
widget.setAttribute('token', token);
widget.setAttribute('agent-id', persona.agentId);  // kebab-case!
widget.setAttribute('face-id', persona.faceId);    // kebab-case!
document.getElementById('simli-mount').appendChild(widget);
```

### 4. Auto-Start Session
```javascript
const startBtn = widget.querySelector('button');
if (startBtn) startBtn.click();
```

### Required IDs from Simli Dashboard:
- **Agent ID** - The conversational AI agent
- **Face ID** - The avatar/face to render
- **API Key** - For generating tokens (keep secret on backend!)

---

## 4-Layer Architecture (Video Sandwich)

```
┌─────────────────────────────────────────┐
│  Layer 5: TOP FLOATIES (future)         │  ← Sparkles, particles
├─────────────────────────────────────────┤
│  Layer 4: SIMLI AGENT                   │  ← AI avatar (mix-blend-mode: screen)
├─────────────────────────────────────────┤
│  Layer 3: TRANSITION VIDEO              │  ← Idle-to-persona videos
├─────────────────────────────────────────┤
│  Layer 2: IDLE LOOP (always visible)    │  ← Abstract smoke, platform
├─────────────────────────────────────────┤
│  Layer 1: BOTTOM FLOATIES (future)      │  ← Smoke, embers
└─────────────────────────────────────────┘
```

**Key Principle:** Black pixels → transparent via `mix-blend-mode: screen`

The idle loop (Layer 2) is ALWAYS playing underneath everything, creating depth illusion.

---

## File Structure

```
echoes-of-indiana-main/
├── index.html              # Hologram display (pure output)
├── styles.css              # Layer styling, head positioning
├── compositor.js           # Layer orchestration
├── config.js               # Persona configs, video paths
├── state-machine.js        # State management
├── simli-integration.js    # Simli widget handling
└── assets/
    ├── videos/
    │   ├── idle_1.mp4          # Idle loop (abstract smoke)
    │   └── idle_to_mabel_2.mp4 # Transition: idle → Mabel
    └── images and ideas/
        └── for menu/           # Thumbnail videos for menu
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
4. **TRANSITIONING-OUT**: Play persona-to-idle video, cleanup Simli (TODO)
5. Back to **IDLE**

---

## URL Parameters

| Parameter | Effect |
|-----------|--------|
| `?calibrate` | **Show calibration panel** for head positioning |
| `?measure` | Show measurement grid overlay |
| `?debug=borders` | Show colored borders on all layers |
| `?persona=mabel` | Auto-invoke Mabel on load |
| `?autostart=true` | Skip "Touch to Begin" overlay |

---

## JavaScript API

```javascript
Compositor.invokePersona('mabel')  // Start a persona
Compositor.dismissPersona()         // End current session
Compositor.forceReset()             // Emergency reset
Compositor.startIdleLoop()          // Start idle videos
```

---

## Adding New Personas

### 1. Create Videos

Transition video should end with head positioned:
- Top of head: ~25% from top of frame
- Chin: ~50-55% from top
- Centered horizontally

```
assets/videos/
├── idle_to_[persona].mp4    # Required: transition in
└── [persona]_to_idle.mp4    # Optional: transition out
```

### 2. Create Simli Agent

1. Go to Simli dashboard
2. Create new agent with system prompt for the character
3. Create or upload face/avatar
4. Note the **Agent ID** and **Face ID**

### 3. Add to Config

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

### 4. Calibrate Head Position

1. Open `?calibrate` URL
2. Summon the new persona
3. Adjust Scale, X, Y until head matches video
4. Copy CSS transform value
5. If significantly different from Mabel, may need per-persona transforms

---

## Known Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Simli head wrong size/position | Transform values off | Use `?calibrate` tool |
| Video disappears before can compare | Normal behavior | Guess & iterate with calibration |
| Gray bars on Simli | 16:9 in square container | Use `object-fit: cover` + scale up |
| Videos don't autoplay | Browser policy | "Touch to Begin" overlay |
| Dotted face placeholder | Simli loading state | CSS hides it, aggressive cleanup |
| Simli Close button visible | Simli's internal UI | CSS moves it off-screen |

---

## Production Deployment

### Railway

- Deployed via GitHub push
- URL: `https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/`

### Environment Variables (Railway)

```
SIMLI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # if using voice/RAG
```

---

## TODO / ROADMAP

### Phase 1: Mabel Polish (Current)
- [ ] **Perfect head alignment** with transition video (close but not exact)
- [ ] Shorten transition video if needed
- [ ] Test full conversation flow

### Phase 2: More Content
- [ ] Add floaties videos (layers 1 & 5) for depth
- [ ] Create more idle loop variations
- [ ] **Add music and sound effects** (ambient, transitions, interactions)
- [ ] Create persona-to-idle transition videos

### Phase 3: More Personas
All 21 personas are defined in `config.js` - each needs: Agent ID, Face ID, transition video

**Working-Class Indiana:**
- [ ] Nell (Showers tube runner, 1918)
- [ ] Mae (Monon depot clerk, 1918)
- [ ] Tomaz (Limestone channeler, 1920s)
- [ ] Cyril (Breaking Away cyclist, 1970s)
- [ ] Louise (RCA color-TV assembler, 1954)
- [ ] Frank (RCA shop steward, 1960s)
- [ ] Elsie (Switchyard hostler)
- [ ] Mrs Johnson (Community guide)
- [ ] Eddie (Showers pond kid, 1910s)

**Famous Hoosiers:**
- [ ] Kurt Vonnegut (Author)
- [ ] Hoagy Carmichael (Composer)
- [ ] James Whitcomb Riley (Poet)
- [ ] James Dean (Actor)
- [ ] Larry Bird (Basketball)
- [ ] Alfred Kinsey (IU Professor)
- [ ] John Mellencamp (Rocker)
- [ ] Vivian Carter (Vee-Jay Records)
- [ ] Angela Brown (Opera)
- [ ] Ryan White (AIDS activist)
- [ ] Elinor Ostrom (Nobel economist)
- [ ] Madam C.J. Walker (Entrepreneur)
- [ ] David Letterman (Late-night)
- [ ] Lil Bub (Internet cat!)
- [ ] Wes Montgomery (Jazz guitar)
- [ ] Carole Lombard (Actress)
- [ ] George Rogers Clark (Revolutionary War)
- [ ] Hoosier Oracle (Guide/Router)

### Phase 4: Kiosk Interface
- [ ] Separate page for touch screen menu
- [ ] Persona selection grid with thumbnails
- [ ] PostMessage communication to hologram display

### Phase 5: Production
- [ ] Test on actual LED fan array
- [ ] Optimize video encoding
- [ ] Final calibration on actual hardware

### COMPLETED ✅
- [x] Mabel Simli integration working
- [x] State machine (idle → active → idle)
- [x] Dismiss button functionality
- [x] Video sandwich architecture (idle always visible)
- [x] Calibration tool built (`?calibrate`)
- [x] Measurement grid (`?measure`)
- [x] Railway API key quirks fixed
- [x] Dotted face placeholder hidden
- [x] Simli Close button hidden

---

## Quick Test

1. Open: `https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/`
2. Click "Touch to Begin"
3. Click Mabel in the menu
4. Watch transition video
5. Talk to Mabel!
6. Click "Dismiss" to end

For calibration: Add `?calibrate` to URL

---

# 📄 Report-Ready Descriptions

## Public Version (for Elements)

**Echoes of Indiana — A PastPresence Installation**

Echoes of Indiana is an interactive heritage installation where visitors converse with holographic personas from the state's past. Users select a character—a 1917 furniture worker, a Hoosier poet, a limestone channeler—and engage in real-time voice dialogue powered by AI. Each persona draws from researched historical context and period-appropriate speech, creating encounters rather than exhibits.

The project is the flagship installation of PastPresence, a platform for experiencing history through dialogue. Five personas are currently active, with 25+ planned across four categories: everyday Archetypes, Historical Figures, Living Legends, and regional Lore.

Sole creator: Caleb Weintraub

**Demo:**
- Kiosk interface: https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/kiosk/
- Hologram display: https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/

*(Development deployment — full installation hardware pending)*

**Period:** 2024–2025

---

## Technical Version (for Projects Doc)

**Echoes of Indiana — A PastPresence Installation**

**Overview:** Interactive hologram installation using AI-driven talking-head avatars. Visitors select personas via touch kiosk; selected persona appears on holographic display for real-time voice conversation.

**Tech Stack:**
- Frontend: Vanilla JavaScript, CSS (no framework)
- Avatar engine: Simli widget SDK (WebRTC-based talking heads)
- Voice: ElevenLabs TTS integration via Simli
- Hosting: Railway (Python FastAPI backend for token generation)
- Architecture: State machine + video compositor pattern

**Current Status:**
- 5 personas active (Mabel, Tomaz, Hazel, James Whitcomb Riley, Brown County Bigfoot)
- Kiosk interface complete with animated thumbnails
- Hologram display functional with transition video system
- Video sandwich architecture working (layered compositing)

**Known Issues:**
- Simli WebRTC transport occasionally disconnects ("send transport changed to disconnected")
- Alignment between transition video and Simli avatar requires per-persona calibration

**Dependencies:**
- Simli API key (for avatar sessions)
- ElevenLabs API key (for voice synthesis)
- Railway environment variables for key management

**Roadmap:**
- 25+ additional personas planned across 4 categories
- Kiosk → display auto-summon integration
- Physical installation on LED fan array / pepper's ghost display
- Regional expansion framework (Echoes of Uppsala, etc.)

**URLs:**
- Kiosk: https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/kiosk/
- Display: https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/

**Period:** 2024–2025

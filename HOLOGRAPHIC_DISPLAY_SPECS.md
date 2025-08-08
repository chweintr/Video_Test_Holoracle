# Holographic Display Production Pipeline Specs

## Target Display: 3×3 Fan Wall
- Each fan: 1536px
- Total canvas: 4608×4608 effective
- "Smart box" may expect 4K/1080p and scale internally

## Master Resolutions (render all 3, test which works best)
1. **2160×2160** (safe, light)
2. **3840×3840** (4K square) 
3. **4608×4608** (native tile, ideal if supported)

**FPS**: 30 fps for reliability (60 only if wall proves rock solid)

## Layering Model (no real alpha, all on black)
1. **Underlay**: idle particle loop on black (`idle.mp4`)
2. **Bookend transitions**: `transition_{persona}.mp4` and `reverse_{persona}.mp4` on black
3. **Live layer**: Simli window (keep native size; do not upscale if 420/512)
4. **Overlay**: soft "particle shell" (`shell_overlay_alpha.mp4` rendered on black with circular hole where face sits)

## Composition Rules
- **Face box**: Fixed square (same pixel rect across states), centered
- **Feather**: 12–24px feather on overlay hole to hide Simli edges/compression
- **Vignette**: Underlay to avoid hard bezel/gap lines in rotor array
- **Black crush**: Avoid full-black crush in faces (2–3% lift) or wall will "eat" edges

## File Formats
- **Master renders**: ProRes 422 HQ (or DNxHR HQX) on pure black
- **Delivery to OBS**: H.264/H.265 at high bitrate if small files needed
- **No true alpha**: Wall's "black = invisible" illusion does the work

## Audio
- Route ElevenLabs/Gemini audio to OBS
- Set audio offset if Simli adds delay (start at ~+80–120ms and tune)

## Video Pack Export Requirements
Export at 2160² and 3840² (do 4608² if box accepts it):

### Required Files:
- `idle.mp4` (20–30s loop)
- `transition_bigfoot.mp4` (2–3s)
- `transition_hoosier.mp4` (2–3s) 
- `transition_vonnegut.mp4` (2–3s)
- `reverse_bigfoot.mp4` (1–2s)
- `reverse_hoosier.mp4` (1–2s)
- `reverse_vonnegut.mp4` (1–2s)
- `shell_overlay.mp4` (full duration loop, black with feathered hole)

## OBS Scene Setup (No TouchDesigner needed)
- **Scene: IDLE** → plays `idle.mp4` + `shell_overlay.mp4`
- **Scene: LIVE_{persona}** → pauses idle, plays `transition_{persona}`, shows Browser Source (Simli) in face window + shell_overlay
- **Scene: OUTRO** → hides Simli, plays `reverse_{persona}`, returns to IDLE
- **Control**: Hotkeys or OSC to switch scenes when kiosk buttons fire

## Wall Testing Process
1. Send 2160² first
2. If scaler blurs/letterboxes, try 3840²
3. If vendor allows true tile resolution, try 4608² and lock it
4. **Check for**: moiré, bezel readability, edge lift, particle density, tear/stutter

## Why This Works
- Reads as "hologram" because black disappears on fans
- Overlay sells depth perception
- No 3D engine risk
- Maintains summon → talk → dissolve grammar for pitch
- Can swap Simli later without touching video pack

---
*Production pipeline for Indiana Oracle holographic kiosk display*
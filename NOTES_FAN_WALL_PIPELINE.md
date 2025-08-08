# Minimal, Robust Pipeline (for a 3×3 fan wall)

## Target canvas + mastering
- Assumption from vendor mail: each fan = 1536 px; 3×3 wall ≈ 4608×4608 effective canvas.
- Reality: the “smart box” may expect 4K or 1080p and scale internally.
- Make three masters so you can pick what looks best on their scaler:
  - 2160×2160 (safe, light)
  - 3840×3840 (4K square)
  - 4608×4608 (native tile, ideal if supported)
- FPS: 30 fps for reliability. Use 60 only if their wall proves rock solid.

## Layering model (no real alpha, all on black)
- Underlay: idle particle loop on black (`idle.mp4`)
- Bookend transitions: `transition_{persona}.mp4` and `reverse_{persona}.mp4` on black
- Live layer: your Simli window (keep it native size; do not upscale if it’s 420/512)
- Overlay: soft “particle shell” (`shell_overlay_alpha.mp4` but rendered on black with a circular hole where the face sits)
- Composite these four into one HDMI feed (OBS is fine). No keying, no shaders.

## Composition rules
- Face box: keep a fixed square (same pixel rect across states). Center it.
- Feather the overlay hole by ~12–24 px to hide Simli edges/compression.
- Vignette the underlay so bezels/gaps in the rotor array don’t show as hard lines.
- Avoid full-black crush in faces (2–3% lift) or the wall may “eat” the edges.

## File formats
- Master renders: ProRes 422 HQ (or DNxHR HQX) on pure black.
- Delivery to OBS: H.264/H.265 at high bitrate if you need to keep files small.
- No true alpha—the wall’s “black = invisible” illusion is doing the work.

## Audio
- Route 11Labs/Gemini audio to OBS; set audio offset if Simli adds delay (start at ~+80–120 ms and tune).

## “Do it today” checklist (merges yesterday + today)

### 1) Web kiosk (3 personas live)
- Switcher works: Bigfoot, Hoosier, Vonnegut in the same box.
- Voices/RAG wired as discussed (Bigfoot→Indiana folklore, Hoosier→Hoosier KB, Vonnegut→Vonnegut KB + ElevenLabs).
- Simli teaser icon hidden or moved; widget mounted programmatically.
- Do not upscale Simli. Keep it native, pad with particles.

### 2) Video pack (export now)
- Export at 2160² and 3840² today (do 4608² if your box accepts it):
  - `idle.mp4` (20–30 s loop)
  - `transition_bigfoot.mp4`, `transition_hoosier.mp4`, `transition_vonnegut.mp4` (2–3 s)
  - `reverse_bigfoot.mp4`, `reverse_hoosier.mp4`, `reverse_vonnegut.mp4` (1–2 s)
  - `shell_overlay.mp4` (full duration loop, black with a feathered hole)

### 3) OBS scenes (no TouchDesigner needed)
- Scene: IDLE → plays `idle.mp4` + `shell_overlay.mp4`
- Scene: LIVE_{persona} → pauses idle, plays `transition_{persona}`, then shows Browser Source (Simli) in the face window + shell_overlay
- Scene: OUTRO → hides Simli, plays `reverse_{persona}`, returns to IDLE
- Hotkeys or OSC to switch scenes when your kiosk buttons fire.

### 4) Wall tests (fast)
- Send 2160² first. If scaler blurs or letterboxes, try 3840².
- If the vendor lets you feed true tile resolution, try 4608² and lock it.
- Check: moiré, bezel readability, edge lift, particle density, tear/stutter.

## Why this is enough
- It reads as “hologram” because black disappears on the fans and your overlay sells depth.
- No 3D engine risk. You still get the summon → talk → dissolve grammar the pitch needs.
- You can swap Simli later without touching the video pack.

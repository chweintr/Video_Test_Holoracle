# Video Assets Folder

Place your alpha-channel videos here!

## 📁 Naming Convention

For each persona, use this naming pattern:

```
[persona-id]-idle-to-active.mp4   ← Required: Transition into persona
[persona-id]-active-to-idle.mp4   ← Optional: Transition back to idle
[persona-id]-background.mp4       ← Optional: Background atmosphere loop
[persona-id]-overlay.mp4          ← Optional: Foreground effects
```

## Example: Mabel

```
mabel-idle-to-active.mp4    ← Shows Mabel appearing from abstract hologram
mabel-active-to-idle.mp4    ← Mabel fading back to abstract
mabel-background.mp4        ← Smoke/particles behind Mabel (loops)
mabel-overlay.mp4           ← Holographic effects in front (loops)
```

## 🎬 Video Specifications

**Requirements:**
- **Background**: Pure black (#000000) or transparent alpha
- **Codec**: H.264 with alpha OR VP9/WebM
- **Resolution**: 1080x1080 minimum (square recommended for LED fans)
- **Frame Rate**: 30fps or 60fps
- **Audio**: Optional (usually silent for compositing)

**File Size Tips:**
- Keep under 10MB per video if possible
- Use H.264 High Profile for compression
- Alpha videos will be larger - that's expected

## 🔄 Video Types

### 1. Idle-to-Active (Required)
- **Purpose**: Transition from idle state to active persona
- **Duration**: 2-5 seconds
- **Loop**: No (plays once)
- **Content**: Abstract → recognizable persona head
- **Key Frame**: Last frame should show head in position where Simli will appear

### 2. Active-to-Idle (Optional)
- **Purpose**: Transition from persona back to idle
- **Duration**: 2-5 seconds
- **Loop**: No (plays once)
- **Content**: Persona head → abstract/fade out

### 3. Background (Optional)
- **Purpose**: Atmospheric layer behind Simli avatar
- **Duration**: 5-30 seconds
- **Loop**: Yes (seamless loop)
- **Content**: Smoke, particles, haze, subtle movement
- **Opacity**: Can be full or semi-transparent

### 4. Overlay (Optional)
- **Purpose**: Effects layer in front of Simli avatar
- **Duration**: 5-30 seconds
- **Loop**: Yes (seamless loop)
- **Content**: Holographic glitches, light streaks, sparkles
- **Opacity**: Should be semi-transparent (50-80%)

## 🎨 Current Persona List

**Ready to Add:**
- [ ] Mabel (Showers Worker)
- [ ] Hoosier Oracle (Guide)
- [ ] Kurt Vonnegut (Author)
- [ ] Brown County Bigfoot (Trail Sage)
- [ ] Larry Bird (Basketball)
- [ ] Hoagy Carmichael (Composer)
- [ ] And more...

## 💡 Tips

1. **Test videos first**: Play them in a browser before deploying
2. **Alpha channels**: Use After Effects, Premiere, or Blender to export alpha
3. **Black backgrounds**: If no alpha support, use pure black #000000
4. **Position matching**: The head position in the last frame of idle-to-active should match where Simli appears
5. **Seamless loops**: For background/overlay, make sure first and last frames match

---

**Drop your videos here and update config.js!** 🎥

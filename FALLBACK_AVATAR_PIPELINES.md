# Fallback Avatar Pipeline Options

## If Simli Proves Too Inflexible

### Option 1: NVIDIA Audio2Face Pipeline
**Status**: Partially implemented in `grpc_pipeline/` folder

**Architecture**:
```
Voice Input → GPT-4o + RAG → TTS → Audio2Face (Docker) → Blendshapes → TouchDesigner/Unity
```

**Pros**:
- Professional quality facial animation
- Full control over output
- Can stream via OBS/NDI to HDMI

**Cons**:
- Requires Docker with admin rights
- GPU intensive
- Complex setup

**Implementation**:
1. Start Audio2Face container: `./docker-scripts/start-audio2face.ps1`
2. Run pipeline: `python run_pipeline.py`
3. Stream output via OBS Virtual Camera

---

### Option 2: Custom WebRTC Pipeline
**Components**: SadTalker + Coqui TTS + TouchDesigner

**Architecture**:
```
Voice → Coqui TTS (local) → SadTalker → WebRTC Stream → TouchDesigner particles
```

**Pros**:
- Fully local, no API dependencies
- Free and open source
- Can customize appearance

**Cons**:
- Lower quality than commercial solutions
- Requires model downloads (2-3GB)
- Higher latency (1-2 seconds)

**Quick Setup**:
```bash
pip install TTS
pip install sadtalker
python custom_avatar_pipeline.py
```

---

### Option 3: HeyGen Streaming API
**Status**: Code ready in `stream_test.py`

**Pros**:
- High quality avatars
- Low latency (<500ms)
- Professional features

**Cons**:
- Paid API ($99/month minimum)
- Still uses iframe embed
- Limited customization

**Implementation**:
```python
python stream_test.py --api-key YOUR_HEYGEN_KEY --persona assets/personas/hoosier.jpg
```

---

### Option 4: D-ID Streaming API
**Status**: 95% complete in `stream_test_did.py`

**Pros**:
- Good quality
- Credits available (12 remaining)
- Established platform

**Cons**:
- WebRTC handshake issues with aiortc
- Paid after credits exhausted
- iframe limitations

**Fix Required**:
Replace aiortc with alternative WebRTC library

---

### Option 5: LivePortrait + Local TTS
**New Option - Highly Recommended**

**Architecture**:
```
Voice → Local TTS → LivePortrait (real-time) → Canvas/WebGL → Particles
```

**Pros**:
- Completely free
- Runs locally
- Good quality for static images
- No iframe constraints

**Setup**:
```bash
git clone https://github.com/KwaiVGI/LivePortrait
cd LivePortrait
pip install -r requirements.txt
python inference.py --source hoosier.jpg --driving audio.wav
```

---

## Recommendation Priority

1. **Continue with Simli** for now (simplest path)
2. **LivePortrait** as backup (free, local, good quality)
3. **HeyGen** if budget allows (professional, reliable)
4. **Audio2Face** if Docker issues resolved (best quality)
5. **Custom WebRTC** as last resort (most complex)

---

## Quick Decision Matrix

| Solution | Cost | Quality | Latency | Complexity | Control |
|----------|------|---------|---------|------------|---------|
| Simli | $$/mo | Good | <500ms | Low | Limited |
| Audio2Face | Free* | Excellent | <200ms | High | Full |
| LivePortrait | Free | Good | <1s | Medium | Full |
| HeyGen | $$$/mo | Excellent | <500ms | Low | Limited |
| D-ID | $$/mo | Good | <500ms | Medium | Limited |
| Custom WebRTC | Free | Fair | 1-2s | High | Full |

*Requires NVIDIA GPU

---

## Emergency Fallback (If Everything Fails)

**Pre-rendered Video Loops**:
1. Record 10-15 response videos for each persona
2. Use GPT-4o to select best match
3. Play pre-rendered video
4. Acceptable for demo/pitch purposes

```javascript
const responses = {
    'greeting': 'videos/hoosier_greeting.mp4',
    'indiana_history': 'videos/hoosier_history.mp4',
    'basketball': 'videos/hoosier_basketball.mp4'
};
```

---
*Save this document for quick reference if Simli limitations become blocking*
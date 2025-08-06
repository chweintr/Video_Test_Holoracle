# AVATAR PIPELINE PLANNING (SIMLI + PARTICLE LOOPS)

## Current Status
We are currently building a prototype to demonstrate the interactive avatar logic for a web-based hologram simulation. For the short term (and possibly for the upcoming pitch), we will use Simli as the speaking avatar layer—even though it's constrained by its iframe/web widget format and small fixed size. The goal right now is functional proof of concept.

## Technical Architecture

### Current Setup
- **Repository**: `chweintr/Video_Test_Holoracle`
- **Deployment**: Railway (port 8083)
- **Avatar System**: Simli widget integration
- **Voice System**: GPT-4o + RAG + ElevenLabs (copied from Echoes_Test)
- **Knowledge Base**: Indiana Oracle dataset (138KB .pkl file)

### File Structure
```
Video_Test_Holoracle/
├── working_simli_integration.html    # Current Simli interface
├── voice_system.py                   # Voice conversation system
├── rag_system.py                     # RAG for Indiana knowledge
├── indiana_knowledge_base.pkl        # Knowledge base data
├── personas/                         # Persona definitions
├── assets/                           # Visual assets
├── test_server.py                    # Railway deployment server
├── index.html                        # Landing page
└── requirements.txt                  # Dependencies
```

## Avatar Pipeline Plan

### 1. Startup State / Idle
- **Looping pre-rendered video** of idle particles plays in a **1:1 square region (420x420)**
- This video simulates the background "particle cloud" while no interaction is taking place
- **Persistent alpha-layer video** plays in the foreground — a transparent particle shell with a vacant center
- This helps simulate continuity and makes the Simli avatar feel embedded in a particle system or "hologram"

### 2. Trigger Event
When a user clicks "Vonnegut" (or another entity name), the following sequence occurs:

1. **Idle particles video is paused or removed**
2. **Transition video plays** in the same spot — a short clip where particles assemble into Vonnegut's head in a static/bookend pose
3. **After transition finishes**, the Simli avatar loads in the same location, replacing the video
4. **Simli provides voice output** (from 11Labs) and animation
5. **Currently using free stock "Bigfoot" avatar** just to test embedding, audio sync, and placement

### 3. Live Interaction
- The Simli avatar engages in a **voice-based interaction** with the user
- This is the main "talking oracle" moment
- The Simli embed must:
  - Be placed precisely in the same **420x420 region**
  - Sit beneath the alpha-layer particles and above the previous particle loop

### 4. End Chat → Return to Idle
When the chat ends, the following reverse sequence plays:

1. **Simli disappears**
2. **Transition video plays** of Vonnegut particles dissolving back into idle particles
3. **Once complete**, the original idle particle loop resumes
4. The **persistent outer alpha-particle video layer** remains throughout, giving the illusion of continuity

## Technical Requirements

### Positioning & Sizing
- **Consistent 420x420 square zone** for all avatar elements
- **Precise layering**: Alpha particles > Simli avatar > Background particles
- **Responsive design** that maintains aspect ratio

### Video Assets Needed
1. **Idle particle loop** (420x420, seamless loop)
2. **Alpha particle overlay** (transparent, persistent)
3. **Transition videos**:
   - Particles → Vonnegut head assembly
   - Vonnegut head → Particles dissolution
4. **Bookend poses** for each avatar

### Integration Points
- **Simli widget positioning** within 420x420 container
- **Video transition timing** with Simli loading
- **Audio synchronization** between ElevenLabs and Simli
- **State management** for idle/interaction/transition states

## Development Phases

### Phase 1: Foundation ✅ (COMPLETED)
- [x] Working Simli integration
- [x] Voice system components copied
- [x] Railway deployment working
- [x] Basic HTML interface

### Phase 2: Video Integration (NEXT)
- [ ] Create 420x420 video container
- [ ] Implement idle particle loop
- [ ] Add alpha particle overlay
- [ ] Create transition video system

### Phase 3: Avatar Pipeline (PLANNED)
- [ ] Implement trigger events
- [ ] Add transition video sequences
- [ ] Integrate Simli with video transitions
- [ ] Create end-of-chat dissolution

### Phase 4: Polish (FUTURE)
- [ ] Multiple avatar heads (2-3 distinct Simli heads)
- [ ] Smooth timing optimization
- [ ] Enhanced particle effects
- [ ] Pitch-ready presentation

## Additional Notes

### Avatar Switching
- For now, using one avatar head
- By pitch day, hope to have **2–3 distinct Simli heads** ready and switchable by name
- Each avatar needs its own transition videos and bookend poses

### Performance Considerations
- **Timing must feel smooth** even if there is slight latency between events
- **Asset-swapping logic** (loop → transition → Simli → reverse) must be clearly defined
- **Alpha video overlay** must allow visibility of the Simli head while still giving the appearance of a dynamic hologram

### Current Limitations
- **Simli widget size constraints** (small fixed size)
- **Iframe/web widget format** limitations
- **Positioning precision** requirements

## Next Immediate Steps

1. **Test Railway deployment** - Verify current setup works
2. **Create video container** - 420x420 square region
3. **Implement idle particle loop** - Background animation
4. **Add alpha particle overlay** - Persistent hologram effect
5. **Design transition system** - Video state management

---

**Last Updated**: August 5, 2025
**Status**: Phase 1 Complete, Phase 2 Ready to Begin 
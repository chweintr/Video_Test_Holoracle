# Indiana Oracle Project Context & Status

## 🎯 Project Overview
**Goal**: Create a holographic oracle kiosk experience with voice-driven AI avatars representing Indiana personas (Hoosier Oracle, Kurt Vonnegut, etc.)

## 📁 Key Locations
- **Main Project**: `E:\Interactive\interactive_project\indiana-oracle-grpc-face\`
- **Active Development**: `E:\Interactive\interactive_project\indiana-oracle-grpc-face\Video_Test_Holoracle\`
- **GitHub Repo**: `https://github.com/chweintr/Video_Test_Holoracle.git`
- **Railway Deployment**: Currently running with initialized backend

## 🔧 Current Technical Stack

### Backend (Working on Railway)
- **GPT-4o**: AI responses with persona-specific prompts
- **RAG System**: Indiana knowledge base (`indiana_knowledge_base.pkl`)
- **ElevenLabs TTS**: 
  - Hoosier Oracle: `KoVIHoyLDrQyd4pGalbs`
  - Vonnegut: `J80PasKsbR4AWMLiAQ0j`
- **FastAPI Backend**: `simli_voice_backend.py`

### Frontend
- **Simli Avatar**: 420x420 iframe embed
- **Current Issue**: Shows in upper-left corner, needs centering
- **Placeholder**: "Bigfoot" stock head (working)

## 🔑 API Keys & Environment Variables
Set these in Railway dashboard:
- `OPENAI_API_KEY` - For GPT-4o responses
- `ELEVENLABS_API_KEY` - For voice synthesis  
- `SIMLI_API_KEY` - For avatar streaming
- `SIMLI_FACE_ID` - Avatar face ID

## 🎭 Three Personas System

### 1. Bigfoot (Stock - Working)
- Simli stock head and voice
- Uses Indiana RAG knowledge
- Fallback/reference configuration

### 2. Hoosier Oracle
- Will use custom Sinking head (pending)
- Indiana RAG + OpenAI woman's voice
- ElevenLabs voice ID: `KoVIHoyLDrQyd4pGalbs`

### 3. Kurt Vonnegut
- Will use custom Sinking head (pending)
- Vonnegut corpus + custom voice
- ElevenLabs voice ID: `J80PasKsbR4AWMLiAQ0j`

## 🎬 Visual Pipeline Design

### Layer Structure (z-index):
1. **Background**: Idle/transition videos (420x420)
2. **Middle**: Simli iframe (420x420)
3. **Foreground**: Alpha particle overlay (persistent)

### State Machine:
1. **Idle**: Loop `idle.mp4` + `shell_overlay_alpha.mp4`
2. **Trigger**: User clicks persona → stop idle → play `transition_[persona].mp4`
3. **Live**: Load Simli iframe in same region + maintain overlay
4. **End**: Unload Simli → play `reverse_[persona].mp4` → return to idle

## ⚠️ Known Issues & Constraints

### Simli Limitations:
- Fixed 420x420 size
- Teaser icon interference (bottom constellation)
- Upper-left positioning (needs centering)
- Widget approach vs direct API challenges

### Solutions Needed:
1. Center Simli iframe in viewport
2. Suppress/relocate teaser icon
3. Maintain consistent positioning across all states

## 🔄 Future Enhancements

### Chatterbox TTS (Replace ElevenLabs):
- Repository: `https://github.com/resemble-ai/chatterbox.git`
- Free voice cloning to eliminate API costs
- Documented in `CHATTERBOX_INTEGRATION_PLAN.md`

### Fallback Avatar Systems:
1. **NVIDIA Audio2Face** (Docker/gRPC pipeline)
2. **Custom WebRTC** (SadTalker + Coqui + TouchDesigner)
3. **HeyGen/D-ID APIs** (streaming alternatives)

## 📝 Current Status (As of Session)
- ✅ Backend deployed on Railway with all systems initialized
- ✅ Environment variables working
- ✅ Basic Simli integration functional
- 🔧 Need persona switching implementation
- 🔧 Need video sequencing system
- 🔧 Need layout/positioning fixes

## 🚀 Next Actions
1. Implement 3-persona switching system
2. Center Simli iframe (420x420)
3. Add video sequencing logic
4. Handle teaser icon issue
5. Implement alpha overlay system

---
*Last Updated: Current Session*
*For questions: Review this doc + check Railway deployment status*
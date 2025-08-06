# Pipeline Options Analysis for Indiana Oracle Voice System

## Current Situation Assessment
- **Current Setup**: Simli widget + custom voice backend (GPT-4o + RAG + ElevenLabs)
- **Issue**: Simli widget not connecting to custom backend properly
- **Goal**: Get Indiana Oracle working with custom voice system
- **Available Resources**: E: drive space, Railway deployment, existing voice system

## 🗂️ **E: Drive Space Analysis**
- **Total Space**: ~8TB (8,001,528,266,752 bytes)
- **Free Space**: ~7.8TB (7,811,357,474,816 bytes)
- **Used Space**: ~190GB
- **Available for Models**: **PLENTY** (7.8TB free!)

---

## Pipeline 1: FastRTC Voice Assistant (Simplest - 5 minutes)

### ✅ **Pros**
- **Fastest setup** (5 minutes)
- **Minimal dependencies** (just UV package manager)
- **Auto-installs** all dependencies from pyproject.toml
- **CPU-only** operation (16GB RAM)
- **No GPU required**
- **Local LLM** (Gemma 3 1B or Qwen 2.5 1.5B)

### ❌ **Cons**
- **No avatar** (just voice interface)
- **Smaller models** (1-1.5B parameters)
- **Less sophisticated** than current GPT-4o setup
- **No RAG system** for Indiana knowledge

### 🎯 **Best For**
- Quick proof of concept
- Testing voice interaction
- Minimal resource usage
- When avatar isn't critical

---

## Pipeline 2: LiveKit + QTI + Ollama (Fully Offline)

### ✅ **Pros**
- **Completely offline** (no API costs)
- **High-quality TTS/STT** (QTI models)
- **Customizable** LLM (any Ollama model)
- **Professional setup** with LiveKit
- **GPU acceleration** available
- **Space is NOT an issue** (7.8TB available!)

### ❌ **Cons**
- **Complex setup** (multiple components)
- **Nvidia GPU required** for best performance
- **Docker dependencies**
- **No avatar** (voice only)
- **Resource intensive**

### 🎯 **Best For**
- Production deployment
- Privacy-focused applications
- When you have good GPU
- Long-term cost savings

---

## Pipeline 3: Speeches + Simli Avatar (Free with Avatar)

### ✅ **Pros**
- **Includes avatar** (Simli integration)
- **Free tier** available (50 minutes/month)
- **Local TTS/STT** (Speeches)
- **CPU capable** (GPU optional)
- **Avatar + voice** combination
- **Space is NOT an issue** (7.8TB available!)

### ❌ **Cons**
- **Complex integration** (multiple services)
- **Limited free tier** (50 minutes)
- **Docker required**
- **Still need LLM** (Ollama or API)

### 🎯 **Best For**
- Avatar-focused applications
- When visual presence is important
- Budget-conscious projects
- Hybrid local/cloud approach

---

## Resource Requirements Comparison

| Pipeline | CPU | RAM | GPU | Storage | Setup Time | E: Drive Feasible |
|----------|-----|-----|-----|---------|------------|-------------------|
| FastRTC | Any | 16GB | No | 2-3GB | 5 min | ✅ **YES** |
| LiveKit+QTI | Any | 8GB+ | Yes* | 5-10GB | 30-60 min | ✅ **YES** |
| Speeches+Simli | Any | 8GB+ | Optional | 3-5GB | 20-30 min | ✅ **YES** |

*GPU required for optimal performance

---

## 🎯 **Updated Recommendation for Current Situation**

### **Space is NOT a constraint!** (7.8TB available)

### **Immediate Action: Try Pipeline 1 (FastRTC) FIRST**

**Why this makes sense:**
1. **Quick validation** - Test if voice interaction works at all
2. **Minimal disruption** - Doesn't break current setup
3. **Baseline comparison** - Compare with current GPT-4o performance
4. **Fast feedback** - 5 minutes to know if it works

### **If FastRTC Works Well:**
- **Option A**: Enhance with avatar (integrate Simli widget)
- **Option B**: Scale up to Pipeline 3 (Speeches + Simli) - **RECOMMENDED**
- **Option C**: Keep current GPT-4o + RAG system

### **If FastRTC Doesn't Meet Needs:**
- **Fallback**: Continue debugging current Simli + custom backend
- **Alternative**: Try Pipeline 3 for avatar + local voice

---

## Implementation Strategy

### Phase 1: Quick Test (Today)
1. **Install FastRTC** (5 minutes)
2. **Test voice interaction** 
3. **Compare quality** with current system
4. **Check resource usage**

### Phase 2: Decision Point
- **If satisfied**: Enhance with avatar integration
- **If not satisfied**: Continue current approach or try Pipeline 3

### Phase 3: Production Setup
- **Choose best performing option**
- **Deploy to Railway**
- **Add video transitions** and particle effects

---

## Current System Status

### ✅ **What We Have Working**
- GPT-4o + RAG system (Indiana knowledge base)
- ElevenLabs TTS (high quality)
- Railway deployment infrastructure
- Simli widget (loads but not connecting to backend)

### 🔧 **What Needs Fixing**
- Simli widget ↔ custom backend connection
- Audio flow between systems
- Avatar integration with voice system

### 🎯 **Priority**
1. **Fix current Simli integration** (if possible)
2. **Test FastRTC** as backup option
3. **Choose best path forward**

---

## 🚀 **Final Recommendation**

### **Given 7.8TB of free space, here's the optimal path:**

1. **Start with FastRTC** (5-minute test)
   - Quick validation of voice interaction
   - Minimal risk, fast feedback

2. **If FastRTC works**: **Go with Pipeline 3 (Speeches + Simli)**
   - Best of both worlds: avatar + local voice
   - Space is not an issue
   - Can use larger models if needed

3. **If FastRTC doesn't work**: **Continue current approach**
   - Keep debugging Simli + custom backend
   - We have the space for any solution

### **Why Pipeline 3 is the winner:**
- ✅ **Avatar included** (Simli)
- ✅ **Local voice processing** (Speeches)
- ✅ **Space available** (7.8TB)
- ✅ **Flexible LLM** (Ollama or API)
- ✅ **Budget friendly** (free tier available)

---

## Next Steps

1. ✅ **Check E: drive space** - **DONE** (7.8TB available)
2. **Try FastRTC** (5-minute test)
3. **Compare performance** with current system
4. **Decide on path forward**
5. **Implement chosen solution**

---

*Last Updated: Current session*
*Status: Ready for implementation - Space is NOT a constraint!* 
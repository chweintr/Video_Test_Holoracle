# Simli Troubleshooting Guide

## 🔍 The Avatar Pipeline

When you click a persona, this happens:

```
1. TOKEN      → Backend generates Simli session token
2. WIDGET     → Browser creates simli-widget element  
3. WEBRTC     → Widget connects to Simli's Daily.co room
4. VIDEO      → Avatar face renders (WebRTC video stream)
5. AUDIO IN   → Your microphone captures speech
6. STT        → Simli/Whisper transcribes speech to text
7. LLM        → Agent's AI brain generates response
8. TTS        → ElevenLabs/Simli generates speech audio
9. AUDIO OUT  → Response plays through speakers
10. LIP SYNC  → Avatar lips move to match audio
```

## 🚦 Diagnostic Checklist

### Step 1: Check Browser Console
Open DevTools (F12) → Console tab. Look for:

| Message | Means |
|---------|-------|
| `Token received` | ✅ Backend working |
| `Successfully joined` | ✅ WebRTC connected |
| `Video stream detected` | ✅ Avatar rendering |
| `Successfully left the call` | ❌ Session terminated unexpectedly |
| `Token fetch failed` | ❌ Backend/API key issue |

### Step 2: Check What's Working

| Symptom | Likely Cause |
|---------|--------------|
| Dotted face placeholder | Simli service down, face ID invalid, or WebRTC blocked |
| Face shows but no response | Mic permission, STT, LLM, or TTS issue |
| Face + audio but no lip sync | Video rendering issue |
| Works sometimes, not others | Rate limiting, quota, or service instability |

### Step 3: Check Each Component

#### Token Generation
```
https://videotestholoracle-production.up.railway.app/debug-env
```
- Verify `SIMLI_API_KEY` is set
- Verify `ELEVENLABS_API_KEY` is set (for some personas)

#### Simli Dashboard
1. Go to Simli dashboard
2. Test the SAME agent there
3. If broken there too → Simli's problem
4. If works there → Our integration problem

#### Microphone
1. Click lock icon in URL bar
2. Verify microphone is allowed
3. Try speaking - does audio indicator move?

#### ElevenLabs
1. Go to ElevenLabs dashboard
2. Check API key is valid
3. Check usage quota
4. Verify voice IDs exist

### Step 4: Railway Logs
Check Railway deployment logs for backend errors:
- Go to Railway dashboard
- Click on deployment
- View logs for error messages

## 🔧 Common Fixes

### "Dotted Face" / Avatar Won't Load
- Hard refresh: Cmd+Shift+R
- Clear browser cache
- Try different browser
- Check if works on Simli dashboard
- Verify face ID is correct

### "No Voice Response"
- Check microphone permission
- Check ElevenLabs API key & quota
- Test agent on Simli dashboard
- Check browser console for errors

### "Sometimes Works, Sometimes Doesn't"
- Rate limiting on Simli/ElevenLabs
- Network connectivity issues
- Service instability (report to Simli)

### "Works on Simli, Not on Our Site"
- Token generation issue
- Check Railway env vars
- CORS or network issue
- faceId/agentId mismatch

## 📊 Debug Endpoints

| Endpoint | What It Shows |
|----------|---------------|
| `/debug-env` | Environment variables (masked) |
| `/api/status` | Backend system status |
| `/health` | Simple health check |

## 📝 When Reporting to Simli Support

Include:
1. Agent ID(s) affected
2. Face ID(s) affected
3. Timestamp of when it stopped working
4. Browser console errors (screenshot)
5. Does it work on Simli dashboard? (yes/no)
6. What symptom? (dotted face / no voice / etc)

## 🧪 Test Matrix

Keep track of what's working:

| Persona | Face Loads | Voice Works | On Simli Dash | Notes |
|---------|------------|-------------|---------------|-------|
| Mabel | ? | ? | ? | |
| Bigfoot | ? | ? | ? | |
| Riley | ? | ? | ? | |
| Tomaz | ? | ? | ? | |
| Hazel | ? | ? | ? | |

Fill this in when debugging to find patterns!


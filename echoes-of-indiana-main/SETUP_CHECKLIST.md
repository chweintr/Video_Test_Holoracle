# 🚀 Setup Checklist for Echoes of Indiana

Follow these steps to get your hologram system running!

## ✅ Step 1: Add Videos

- [ ] Place `mabel-idle-to-active.mp4` in `assets/videos/`
- [ ] (Optional) Place `mabel-active-to-idle.mp4` in `assets/videos/`
- [ ] (Optional) Place `mabel-background.mp4` in `assets/videos/`
- [ ] (Optional) Place `mabel-overlay.mp4` in `assets/videos/`

**How:** Just drag and drop your video files into the `assets/videos/` folder!

---

## ✅ Step 2: Configure Mabel's Simli Agent

Open `config.js` and find this section:

```javascript
mabel: {
    name: 'Mabel',
    fullTitle: 'Showers Finishing Worker, 1917',

    // ⬇️ UPDATE THESE:
    agentId: 'YOUR_MABEL_AGENT_ID_HERE',  // Replace with actual Agent ID
    faceId: null,  // Add Face ID if using Compose API
```

**Update:**
- [ ] Replace `YOUR_MABEL_AGENT_ID_HERE` with Mabel's actual Simli Agent ID
- [ ] Add Face ID if you're using Simli Compose API (optional)

**Where to find Agent ID:**
1. Log into Simli dashboard at https://app.simli.com
2. Go to your agents list
3. Find Mabel
4. Copy the Agent ID (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## ✅ Step 3: Set Railway Environment Variables

In your Railway project dashboard:

**Go to:** Settings → Variables

**Add these:**

```
SIMLI_API_KEY=your_simli_api_key_here
OPENAI_API_KEY=your_openai_key_here
```

- [ ] Add `SIMLI_API_KEY`
- [ ] Add `OPENAI_API_KEY` (if using voice features)

**Where to find Simli API Key:**
1. Log into Simli dashboard
2. Go to Settings → API Keys
3. Copy your API key

---

## ✅ Step 4: Test Backend Connection

Make sure the backend is running and accessible:

- [ ] Backend file exists: `simli_voice_backend.py` in parent folder
- [ ] Backend is deployed to Railway
- [ ] Token endpoint works: `GET /simli-token?agentId=test`

**Test it:**
```bash
curl https://your-app.railway.app/simli-token?agentId=test
```

Should return:
```json
{"token": "gAAAAABo..."}
```

If using a **separate backend URL**, update `config.js`:

```javascript
backendUrl: 'https://your-backend.railway.app',
```

---

## ✅ Step 5: Deploy to Railway

**Option A: Deploy with existing parent repo**
- [ ] Parent repo already deployed to Railway
- [ ] This folder is inside `Video_Test_Holoracle/`
- [ ] Access at: `https://your-app.railway.app/echoes-of-indiana-main/`

**Option B: Deploy as new Railway project**
- [ ] Create new Railway project
- [ ] Copy `simli_voice_backend.py` into this folder
- [ ] Link to GitHub repo
- [ ] Set environment variables
- [ ] Deploy!

---

## ✅ Step 6: Test It!

Open in browser and test:

- [ ] Page loads successfully
- [ ] Persona selection screen appears
- [ ] Click "Mabel" button
- [ ] Transition video plays
- [ ] Simli widget loads
- [ ] Click "Summon" in widget
- [ ] Microphone input works
- [ ] Processing message appears while AI thinks
- [ ] AI responds with audio/video
- [ ] Click "Dismiss" button
- [ ] Returns to persona selection

---

## ✅ Step 7: Customize (Optional)

Fine-tune the experience:

- [ ] Adjust Simli position in `config.js` (`simliPosition`)
- [ ] Customize processing messages
- [ ] Adjust video layer opacity in `styles.css`
- [ ] Test on actual LED hologram hardware
- [ ] Turn off debug panel: `showDebugPanel: false`

---

## 🐛 Troubleshooting

### Videos Not Playing
- ✅ Check file names match exactly in `config.js`
- ✅ Check files exist in `assets/videos/`
- ✅ Check video format (H.264 or WebM)
- ✅ Check browser console for errors

### Simli Not Loading
- ✅ Verify Agent ID is correct
- ✅ Check Railway environment variables
- ✅ Test token endpoint manually
- ✅ Check browser console for network errors

### Black Screen
- ✅ Ensure videos have alpha channel or black background
- ✅ Check video codec compatibility
- ✅ Try different browser (Chrome recommended)

---

## 🎉 When Everything Works

You should see:
1. **Idle**: Clean persona selection interface
2. **Click Mabel**: Transition video plays
3. **Active**: Simli avatar appears, ready to interact
4. **Speak**: Processing message shows, then AI responds
5. **Dismiss**: Smooth transition back to selection

---

## 📞 Next Steps

Once Mabel is working:

1. Add more personas following the same pattern
2. Upload their videos
3. Add their Agent IDs to `config.js`
4. Uncomment their buttons in `index.html`

See `README.md` for full persona addition guide!

---

**Ready to launch! 🚀**

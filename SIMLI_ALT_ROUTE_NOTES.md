# Echoes of Indiana – Simli Alt Route (Widget-Only) Handoff Notes

Purpose: Reliable demo path for the pitch using Simli’s Widget SDK only (Agent ID + e2e token), while we pause the custom Compose/WebRTC + RAG + TTS integration. This document catches a new agent up fast and avoids starting from scratch.

## Project goal (short)
- Kiosk web demo with 3 personas in a 420×420 mount: Bigfoot, Hoosier Oracle, Vonnegut
- Visual flow: idle → transition → live → outro → idle (later overlay/video polish)
- Long-term: Compose/WebRTC with our RAG + ElevenLabs; today: show something working and switchable

## Current state (truthful)
- /master: Compose visuals + some RAG utilities. Compose streaming not working yet. CSP warnings for Daily JS appear. Keep for design only.
- /widget: New, separate Simli Widget page intended to be simple and stable. As of now:
  - Bigfoot button should request a token with the provided agentId, but the front end shows no result (user report). Treat as NOT working until verified.
  - Indiana/Vonnegut 400 because we haven’t set their Agent IDs (or the backend env mapping isn’t present). Do not assume they work.

## Why switch to Widget-only (for demo)
- Widget path is the simplest: Agent ID + e2e session token → <simli-widget> embed
- Compose path requires official SDK signaling (Daily-based); our hand-rolled WS approach failed

## Repo locations (pages and backend)
- Pages (directory: `Video_Test_Holoracle/`)
  - `oracle_kiosk_master.html` → Compose visuals/RAG (design sandbox)
  - `oracle_kiosk_widget.html` → Widget page (new alt route)
  - `oracle_kiosk_preview.html` → visual-only
- Backend: `simli_voice_backend.py` (FastAPI)
  - Routes in use:
    - `GET /widget` → serves `oracle_kiosk_widget.html`
    - `GET /master` → serves `oracle_kiosk_master.html`
    - `GET /preview` → serves `oracle_kiosk_preview.html`
    - `GET|POST /simli-token` → returns { token, agentId } for Widget
      - Accepts `agentId` (preferred) or `persona`
      - Sanitizes `SIMLI_API_KEY`
    - `GET|POST /simli-compose/session` → Compose session (Face ID). Not used for widget path

## Environment needed (Railway service-level) – Widget path
- `SIMLI_API_KEY` (string) → required for e2e token creation
- Provide Agent IDs one of two ways:
  - Send explicit `agentId` in the request (frontend 
    uses `/simli-token?agentId=...`)
  - Or set per-persona envs so `/simli-token?persona=x` works:
    - `SIMLI_AGENT_ID_BIGFOOT`
    - `SIMLI_AGENT_ID_INDIANA`
    - `SIMLI_AGENT_ID_VONNEGUT`
  - Optional global fallback: `SIMLI_AGENT_ID`

Important: After changing envs, use Railway “Rebuild image/Deploy”, not just Restart.

## How the widget page is wired (intended)
File: `oracle_kiosk_widget.html`
- Visuals: user’s background/parallax, 420×420 mount
- Buttons call `loadPersona(persona)`:
  1) If we have an explicit Agent ID in page config, request `/simli-token?agentId=...`
  2) Else request `/simli-token?persona=...` (backend uses env mapping)
  3) Expect `{ token, agentId }`
  4) Create `<simli-widget token="..." agentid="..."></simli-widget>` and append in the 420×420 mount

## What’s broken right now (user report)
- Bigfoot button: “does nothing” in /widget. Treat as failed.
  - Likely causes (verify in this order):
    1) `/simli-token?agentId=<bigfoot>` returns 400 (env/API key issue). Test the endpoint directly in browser.
    2) The custom element isn’t defined when we try to append. Fix by awaiting `customElements.whenDefined('simli-widget')` before mount and surfacing on-page errors.
    3) CSP blocks. Current CSP allows app.simli.com and api.simli.ai for /widget; verify no console CSP blocks for the widget.
- Indiana/Vonnegut: 400 on `/simli-token?persona=…` because their Agent IDs are not set (env) and we didn’t pass explicit agent ids.

## Minimal debug checklist (Widget)
1) Direct endpoint test in browser:
   - `/simli-token?agentId=<KnownAgentId>`
   - Expect 200 JSON with `token` and `agentId`. If 400, fix env (`SIMLI_API_KEY`; correct Agent ID) and Redeploy.
2) If endpoint returns 200 but UI doesn’t render:
   - Add `await customElements.whenDefined('simli-widget')` before creating the element
   - Add a visible error div if any step throws
3) Confirm CSP in the page meta includes:
   - `script-src https://app.simli.com https://cdn.tailwindcss.com 'unsafe-inline'`
   - `connect-src https://api.simli.ai https://app.simli.com wss:`
   - `frame-src https://app.simli.com`

## Local testing
```
cd Video_Test_Holoracle
python simli_voice_backend.py
# Then open http://localhost:8083/widget (and /master, /preview)
```

## Railway testing
- Ensure latest commit deployed (Rebuild)
- Open:
  - `https://<your-railway>/widget` (Widget path)
  - `https://<your-railway>/master` (Compose visuals sandbox)

## Decisions to keep us organized
- /widget = Widget SDK only (Agent ID + e2e token). No Compose code here.
- /master = Compose sandbox (design + future SDK integration). No widget here.
- Do not mix paths.

## What I need from the user to finish /widget quickly
- Agent IDs for Hoosier and Vonnegut (paste from Simli dashboard)
- Or set envs `SIMLI_AGENT_ID_INDIANA`, `SIMLI_AGENT_ID_VONNEGUT` (and Rebuild)

## Near-term tasks (doable today)
1) Fix /widget mount robustness:
   - Wait for `customElements.whenDefined('simli-widget')`
   - Show visible error text on token failure (not just console)
2) Wire explicit Agent IDs for all 3 personas
3) Add a root link hub with clear navigation: /widget (live) and /master (design)

## After the pitch (return to full stack)
- Implement Compose correctly using Simli’s official JS SDK (or bundle example)
- Reintroduce RAG + ElevenLabs via our backend; use Compose to stream A/V
- Replace Tailwind CDN with compiled CSS (CI step)

## Why earlier attempts failed (summary)
- Mixed Widget (Agent+Token) with Compose (Face+API key) semantics
- CSP blocked Daily JS on pages not intended for Compose
- Hand-rolled WebSocket signaling incompatible with Simli’s Compose server
- Env propagation mismatch on Railway (token endpoint 400s)

## Single-sentence status
Widget-only alt route is in place (/widget) but currently not rendering Bigfoot; fix token call and mount timing, add the other Agent IDs, and this becomes a dependable demo while the Compose stack is finished later.




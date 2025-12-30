# Echoes of Indiana — Touchscreen Interface

Single-screen version for transparent OLED displays and touchscreen kiosks.

## Target Display

| Spec | Value |
|------|-------|
| Resolution | 1366 × 768 (16:9) |
| Type | Transparent OLED |
| Transparency | Pure black (#000000) = transparent |
| Input | Touch (works with mouse too) |

## How It Works

```
[Menu State]                    [Active State]
┌─────────────────────┐         ┌─────────────────────┐
│  Echoes of Indiana  │         │                     │
│  Commune with past  │         │    [Simli Avatar]   │
│                     │  tap    │                     │
│  ○ ○ ○ ○ ○         │ ───→   │                     │
│  Personas           │         │     [Return]        │
│                     │  ←───   │                     │
│  Touch to begin     │ dismiss │                     │
└─────────────────────┘         └─────────────────────┘
```

## URL

```
https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/touchscreen/
```

## Files

| File | Purpose |
|------|---------|
| `index.html` | Single page with menu + active states |
| `styles.css` | Responsive 16:9, portrait/landscape support |
| `touchscreen.js` | State management, Simli integration |

## Shared Resources

This interface shares with the main project:
- `../config.js` — Persona definitions (add once, appears everywhere)
- `../kiosk/start.png` — Background image
- `../assets/videos/*_Menu.mp4` — Persona thumbnail videos

## Layout System

All layout uses **percentage-based regions**, not fixed pixels:

```css
:root {
    --safe-inset: 5%;        /* Edge padding */
    --avatar-width: 50%;      /* Simli container width */
    --avatar-height: 60%;     /* Simli container height */
    --persona-size: min(18vw, 18vh);  /* Responsive circles */
}
```

## Orientation Support

- **Landscape** (default): Optimized for 16:9 OLED
- **Portrait**: Same code, CSS adjusts layout
- Optional: Add `start-portrait.png` for custom vertical background

## Adding Personas

Just add to `../config.js` — they auto-appear here:

```javascript
newpersona: {
    name: 'New Person',
    agentId: 'xxx',
    faceId: 'xxx',
    menuVideo: '../assets/videos/NewPerson_Menu.mp4'
}
```

## iPad / Tablet Testing

Works on any device with a browser:
- iPad Safari ✓
- Android Chrome ✓
- Desktop browsers ✓

For best experience, use full-screen mode (Add to Home Screen on iPad).


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

---

## FUTURE: Rolodex/Slot Machine Interface (30+ Personas)

When the persona count grows beyond what fits on screen (20-30+), consider a **cylinder/rolodex** navigation pattern inspired by slot machines.

### Concept

```
Current:  ○ ○ ○ ○ ○  (all visible, gets crowded)

Future:   ┌─────────────────────────────┐
          │  ↑ Scroll/Spin indicators ↑ │
          │  ○   ○   ○   ○   ○   ○     │  ← 6 visible slots
          │  ↓                       ↓ │
          └─────────────────────────────┘
          (30 total, 5 per "reel", 6 reels)
```

### Design Goals

| Goal | Solution |
|------|----------|
| Show many personas | 6 visible "slots", others scroll into view |
| Don't cover title | Personas stay in bottom zone |
| Fun interaction | Swipe to "spin" or auto-rotate |
| Visual continuity | Invisible cylinder core (just floating circles) |

### Implementation Options

1. **Vertical Reels** (slot machine style)
   - 6 columns, each scrolls independently
   - 5 personas per column = 30 total
   - Swipe or tap arrows to cycle
   - Could add "spin" animation for discovery mode

2. **Horizontal Carousel** (simpler)
   - Single row of 5-6 visible personas
   - Swipe left/right to see more
   - Pagination dots below

3. **Grid with Pagination**
   - Show 6-9 at a time
   - Swipe to next "page" of personas
   - Category tabs (Archetypes, Historical, Living, Lore)

### Technical Notes

```javascript
// Pseudo-code for reel system
const reels = [
    ['mabel', 'tomaz', 'hazel', 'eddie', 'cyril'],      // Reel 1: Archetypes
    ['riley', 'vonnegut', 'wells', 'kinsey', 'walker'], // Reel 2: Historical
    ['bird', 'mellencamp', 'letterman', 'carter'],      // Reel 3: Living
    ['bigfoot', 'oracle', 'ghostlight'],                // Reel 4: Lore
    // etc.
];

// Each reel loops independently
// Touch/swipe triggers smooth scroll animation
// Only center persona per reel is "active" (larger, glowing)
```

### Visual Inspiration

- Classic slot machines (but personas not symbols)
- Contact picker wheels (iOS style)
- Carousel menus in streaming apps
- Physical rolodex rotating cards

### Priority

**LOW** — Current grid works well for 5-10 personas. Implement when:
- Roster exceeds 15-20 active personas
- User testing shows discovery issues
- Want to add "random encounter" / spin-for-persona feature

### References

- CSS Scroll Snap for smooth carousel
- Framer Motion / GSAP for reel animations
- Swiper.js for touch carousels


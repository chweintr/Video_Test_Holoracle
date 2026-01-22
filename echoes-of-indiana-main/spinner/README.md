# Echoes of Indiana — Persona Spinner

**Status: PROTOTYPE — Not yet connected to main app**

A slot-machine-style persona selector for when we have 20-30+ personas. Features 3D cylindrical reels with smooth animations.

## Preview

```
https://videotestholoracle-production.up.railway.app/echoes-of-indiana-main/spinner/
```

## Two Modes

### 🎰 Spin Mode (Discovery)
- 5 vertical reels, each a 3D rotating cylinder
- 6 personas per reel = 30 total capacity
- Staggered stop timing with ease-out
- Payline shows 5 random personas
- Click any payline result to select

### 📋 Browse Mode (Deliberate)
- Dropdown category filter
- Grid view of all personas
- Quick selection for known targets

## Categories

| Category | Color | Count |
|----------|-------|-------|
| Composite Archetypes | Purple | 8 |
| Historical Figures | Cyan | 12 |
| Living Legends | Green | 5 |
| Local Lore | Red | 4 |

## Files

| File | Purpose |
|------|---------|
| `index.html` | Standalone prototype (no build step) |
| `PersonaSpinner.jsx` | React component (for build integration) |
| `personas.js` | Persona data with categories |

## Technical Details

### 3D Reel Effect
```css
perspective: 900px;
transform-style: preserve-3d;
transform: translateZ(-radius) rotateX(rotation);
```

### Animation
- `requestAnimationFrame` for 60fps
- Cubic ease-out: `1 - pow(1-t, 3)`
- Staggered duration per reel: `900 + r*100 + random`

### Persona Schema
```javascript
{
    id: 'mabel',
    name: 'Mabel',
    category: 'archetypes',  // | 'historical' | 'living' | 'lore'
    title: 'Showers Worker, 1917',
    quote: 'I sand till the grain lies flat.',
    status: 'active',        // | 'placeholder'
    agentId: 'xxx',          // Simli agent (if active)
    faceId: 'xxx',           // Simli face (if active)
    menuVideo: 'Mabel_Menu.mp4'
}
```

## When to Connect

This spinner should replace the current grid when:
1. Active persona count exceeds 15-20
2. User testing shows discovery is fun
3. All persona menu videos are ready

## Integration Plan

1. Import `PersonaSpinner` component
2. Wire `onSelectPersona` callback to Simli invocation
3. Replace menu-state in touchscreen/kiosk with spinner
4. Add audio hooks for spin sounds (optional)

## Customization

### Number of Reels
```javascript
const REELS = 5;  // Change to 6 for 36 persona capacity
```

### Symbols Per Reel
```javascript
const SYMBOLS_PER_REEL = 6;  // Adjust for persona count
```

### Cell Size
```javascript
const CELL = 100;  // px per persona card
```

## Future Enhancements

- [ ] Sound effects (spin, stop, win)
- [ ] Category-filtered spin mode
- [ ] "Lucky spin" animation for first-time visitors
- [ ] Persona preview on hover
- [ ] Swipe gestures for manual reel control
- [ ] Accessibility: keyboard navigation, screen reader

---

*Prototype based on Grok's 3D reel design*



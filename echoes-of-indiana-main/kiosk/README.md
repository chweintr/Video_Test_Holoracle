# Echoes of Indiana - Kiosk/Menu Interface

## 🎯 Purpose

This is a **separate touch-screen interface** for selecting personas. It displays on a kiosk/tablet while the hologram display runs on a separate screen (LED fan array).

## 📋 Design Spec

### Layout
- Grid of persona cards (3-4 per row on tablet, responsive)
- Each card has:
  - **Animated video thumbnail** in circular frame (looping)
  - **Full name** below
  - **Short title/era** 
  - **Quote snippet** in italics
  - Glow effect on hover/touch

### Visual Style
- Dark background (matches hologram aesthetic)
- Cyan/magenta accent colors
- Cards similar to the reference images in `/assets/images and ideas/`

### Categories (Optional)
Consider tabs or sections:
- **Working-Class Indiana** (Mabel, Nell, Mae, Tomaz, etc.)
- **Famous Hoosiers** (Vonnegut, Bird, Letterman, etc.)
- **All Personas**

## 📁 Data Source

All persona data lives in `../config.js`. The kiosk should import/read from there:

```javascript
// Each persona has:
{
    name: 'Mabel',
    fullTitle: 'Showers Brothers Furniture Worker, 1917',
    quote: '"I sand till the grain lies flat..."',
    description: 'Sanded drawer fronts; helped at the veneer press...',
    // ... agent IDs, videos, etc.
}
```

## 🎬 Video Assets

Menu thumbnail videos are in `../assets/videos/`:
- `Mabel_Menu.mp4`
- `Bigfoot_Menu_Better.mp4`
- `James_Whitcomb_Riley_Menu.mp4`
- (More to come as personas are added)

Naming convention: `[PersonaName]_Menu.mp4`

## 🔗 Communication with Hologram Display

Two options:

### Option A: PostMessage (if same browser, different tabs/iframes)
```javascript
// Kiosk sends:
window.opener.postMessage({ action: 'summon', persona: 'mabel' }, '*');

// Hologram listens:
window.addEventListener('message', (e) => {
    if (e.data.action === 'summon') {
        Compositor.invokePersona(e.data.persona);
    }
});
```

### Option B: URL Navigation (simpler)
Kiosk links directly to hologram with query param:
```
https://[hologram-url]/?persona=mabel&autostart=true
```

### Option C: WebSocket/Server (for separate devices)
If kiosk and hologram are on different machines, use a simple WebSocket relay.

## 🖼️ Reference Images

See screenshots in `../assets/images and ideas/` for the visual style we're going for.

## 📐 Current Persona Roster

### Active (have Simli agent + face IDs):
- ✅ Mabel - Showers Brothers Furniture Worker, 1917
- ✅ Brown County Bigfoot - Trail Sage & Cryptid Teller  
- ✅ James Whitcomb Riley - The Hoosier Poet, 1849-1916
- ✅ Tomaz - Limestone Channeler, 1923
- ✅ Hazel - RCA Quality Control Inspector, 1958

### Placeholders (need Simli setup):

**Working-Class Indiana:**
- Nell - Showers Office Tube Runner, 1918
- Mae - Monon Depot Clerk, 1918
- Cyril - Town Rider, Late 1970s
- Louise - RCA Color-TV Assembler, 1954
- Frank - RCA Shop Steward, Mid 1960s
- Elsie - Switchyard Hostler, Mid Century
- Mrs Johnson - Community Guide, Mid Century
- Eddie - Showers Pond Kid, 1910s

**Famous Hoosiers:**
- Kurt Vonnegut - Indianapolis Author
- Hoagy Carmichael - Stardust Composer
- James Dean - Rebel from Fairmount
- Larry Bird - French Lick Legend
- Alfred Kinsey - IU Sexologist
- John Mellencamp - Seymour Rocker
- Vivian Carter - Vee-Jay Records
- Angela Brown - Opera Singer
- Ryan White - AIDS Activist
- Elinor Ostrom - Nobel Economist
- Madam C.J. Walker - Entrepreneur
- David Letterman - Late-Night Legend
- Lil Bub - Internet Sensation
- Wes Montgomery - Jazz Guitarist
- Carole Lombard - Screwball Actress
- George Rogers Clark - Revolutionary War Hero
- Herman B Wells - IU President, 1938-1962
- Hoosier Oracle - Echoes Guide/Router

## 🛠️ Tech Stack Suggestion

- Plain HTML/CSS/JS (keep it simple, matches main project)
- Or React if preferred
- Touch-friendly (large tap targets, no hover-dependent interactions)
- Works offline once loaded (all assets local)

## 🚀 Getting Started

1. Create `kiosk.html` in this folder
2. Import persona data from `../config.js`
3. Render grid of persona cards
4. On card tap: communicate with hologram display
5. Style to match the dark/neon aesthetic

## 📝 Notes

- The main hologram display is at `../index.html`
- Don't modify `../config.js` structure - just read from it
- Menu videos are ~2-5 second loops, keep them small
- Test on actual touch screen if possible

---

**Parent Project:** See `../README.md` for full system documentation.


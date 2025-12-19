# Echoes of Indiana - Kiosk/Menu Interface

## 🌐 About PastPresence

**PastPresence** is an interactive heritage platform that lets visitors talk with the past. Rather than passive exhibits or static text, people engage in real-time dialogue with historical figures, each powered by contextual AI, period-accurate voice synthesis, and expressive avatar technology.

### Echoes of Indiana

The flagship installation surfaces voices from Indiana's layered history. Visitors summon holographic personas and converse with them directly. A 1917 furniture factory worker. A Hoosier poet. A limestone quarry channeler. An RCA quality inspector. Even the legendary Brown County Bigfoot.

Each persona draws from researched historical context, regional dialect, and period-specific knowledge. The result is not a chatbot. It is an **encounter**. A chance to ask questions that textbooks cannot answer: *What did the sawdust smell like? Were you afraid? What did you dream about?*

The framework is designed to scale. Echoes of Uppsala, Echoes of Appalachia, and other regional installations can deploy the same architecture with localized personas and narratives.

### Core Thesis

> *History is not just what happened. It is who was there. PastPresence makes that encounter possible.*

### Companion Projects

- **VonneBot** and similar author-proxy applications extend the PastPresence model to literature. Readers engage with an AI embodiment of an author while reading their work.

---

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

---

### Category System

| Category | Description |
|----------|-------------|
| **Archetypes** | Composite everyday Hoosiers - working lives, local voices |
| **Historical Figures** | Notable Hoosiers who have passed |
| **Living Legends** | Famous Hoosiers still with us |
| **Lore** | Folklore, curiosities, the unexplained |

---

### By Category:

**ARCHETYPES** *(Everyday Hoosiers)*
| Name | Role | Status |
|------|------|--------|
| Mabel | Showers Finishing Worker, 1917 | ✅ Active |
| Tomaz | Limestone Channeler, 1923 | ✅ Active |
| Hazel | RCA Quality Control Inspector, 1958 | ✅ Active |
| Nell | Showers Tube Runner, 1918 | Placeholder |
| Mae | Monon Depot Clerk, 1918 | Placeholder |
| Eddie | Showers Pond Kid, 1910s | Placeholder |
| Cyril | Town Rider, Late 1970s | Placeholder |
| Elsie | Switchyard Hostler, Mid Century | Placeholder |
| CCC Worker | Brown County Conservation, 1930s | Suggested |

**HISTORICAL FIGURES** *(Notable Hoosiers)*
| Name | Role | Status |
|------|------|--------|
| James Whitcomb Riley | The Hoosier Poet, 1849-1916 | ✅ Active |
| Kurt Vonnegut | Indianapolis Author | Placeholder |
| Hoagy Carmichael | Stardust Composer | Placeholder |
| Alfred Kinsey | IU Sexologist | Placeholder |
| Herman B Wells | IU President | Placeholder |
| Elinor Ostrom | Nobel Economist | Placeholder |
| Wes Montgomery | Jazz Guitarist | Placeholder |
| James Dean | Rebel from Fairmount | Placeholder |
| Carole Lombard | Screwball Actress | Placeholder |
| Madam C.J. Walker | Entrepreneur | Placeholder |
| Vivian Carter | Vee-Jay Records | Placeholder |
| Ryan White | AIDS Activist | Placeholder |
| George Rogers Clark | Revolutionary War Hero | Placeholder |
| Ernie Pyle | War Correspondent | Suggested |
| Oscar Charleston | Negro League Legend | Suggested |

**LIVING LEGENDS** *(Still With Us)*
| Name | Role | Status |
|------|------|--------|
| Larry Bird | French Lick Legend | Placeholder |
| John Mellencamp | Seymour Rocker | Placeholder |
| David Letterman | Late-Night Legend | Placeholder |
| Angela Brown | Opera Singer | Placeholder |

**LORE** *(Folklore & Curiosities)*
| Name | Role | Status |
|------|------|--------|
| Brown County Bigfoot | Trail Sage & Cryptid Teller | ✅ Active |
| Lil Bub | Internet Sensation | Placeholder |

---

**Special:**
- Hoosier Oracle - Echoes Guide/Router (meta-persona for navigation)

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


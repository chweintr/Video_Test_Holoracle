/**
 * ECHOES OF INDIANA — PERSONA SPINNER
 * 
 * Two modes:
 * - SPIN: 5 cylindrical reels, slot machine style discovery
 * - BROWSE: Category dropdown + grid selection
 * 
 * Based on the 3D reel prototype by Grok
 */

import React, { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { PERSONAS, CATEGORIES, getPersonasByCategory, shuffleArray } from "./personas";

// ═══════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════
const REELS = 5;
const SYMBOLS_PER_REEL = 6; // 6 personas per reel = 30 total
const CELL = 110; // px per symbol

// ═══════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════
function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

function mod(n, m) {
  return ((n % m) + m) % m;
}

function radiusFor(n, cell) {
  return Math.round((cell / 2) / Math.tan(Math.PI / n));
}

// Generate placeholder color from persona id
function colorFromId(id) {
  let hash = 0;
  for (let i = 0; i < id.length; i++) {
    hash = id.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue} 60% 45%)`;
}

// ═══════════════════════════════════════════
// PERSONA CARD COMPONENT
// ═══════════════════════════════════════════
function PersonaCard({ persona, size = CELL, onClick, isPayline = false }) {
  const categoryColor = CATEGORIES[persona.category]?.color || '#666';
  const isActive = persona.status === 'active';
  
  return (
    <div
      onClick={() => onClick?.(persona)}
      className={`
        relative rounded-2xl overflow-hidden cursor-pointer
        transition-all duration-200
        ${isPayline ? 'ring-2 ring-amber-400 shadow-lg shadow-amber-400/30' : ''}
        ${!isActive ? 'opacity-60' : ''}
      `}
      style={{
        width: size,
        height: size,
        background: colorFromId(persona.id),
        boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
      }}
    >
      {/* Category indicator */}
      <div 
        className="absolute top-2 left-2 w-3 h-3 rounded-full"
        style={{ background: categoryColor }}
        title={CATEGORIES[persona.category]?.name}
      />
      
      {/* Placeholder icon / future: actual image */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-4xl opacity-30">👤</div>
      </div>
      
      {/* Name overlay */}
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-2">
        <div className="text-white text-xs font-semibold truncate">
          {persona.name}
        </div>
        {isPayline && (
          <div className="text-white/60 text-[10px] truncate">
            {persona.title}
          </div>
        )}
      </div>
      
      {/* Status badge */}
      {!isActive && (
        <div className="absolute top-2 right-2 px-1.5 py-0.5 bg-zinc-800/80 rounded text-[8px] text-zinc-400">
          SOON
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════
// 3D REEL COMPONENT
// ═══════════════════════════════════════════
function Reel({ symbols, rotation, radius, step, onSymbolClick }) {
  const frameH = Math.round(CELL * 2.6);
  
  return (
    <div
      className="relative border-r border-zinc-800 last:border-r-0"
      style={{ width: CELL, height: frameH, perspective: 900 }}
    >
      <div
        className="absolute inset-0"
        style={{
          transformStyle: "preserve-3d",
          transform: `translateZ(${-radius}px) rotateX(${rotation}deg)`,
          willChange: "transform",
        }}
      >
        {symbols.map((persona, i) => {
          const a = i * step;
          return (
            <div
              key={persona.id}
              className="absolute left-0"
              style={{
                width: CELL,
                height: CELL,
                top: "50%",
                transformStyle: "preserve-3d",
                transform: `translateY(${-CELL / 2}px) rotateX(${a}deg) translateZ(${radius}px)`,
                backfaceVisibility: "hidden",
              }}
            >
              <PersonaCard 
                persona={persona} 
                size={CELL - 4}
                onClick={onSymbolClick}
              />
            </div>
          );
        })}
      </div>
      
      {/* Vignette overlay */}
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(closest-side, rgba(0,0,0,0.0), rgba(0,0,0,0.55)), linear-gradient(to bottom, rgba(9,9,11,0.9), rgba(9,9,11,0.05) 35%, rgba(9,9,11,0.05) 65%, rgba(9,9,11,0.9))",
        }}
      />
    </div>
  );
}

// ═══════════════════════════════════════════
// SPIN MODE COMPONENT
// ═══════════════════════════════════════════
function SpinMode({ onSelectPersona, categoryFilter = 'all' }) {
  const step = 360 / SYMBOLS_PER_REEL;
  const radius = useMemo(() => radiusFor(SYMBOLS_PER_REEL, CELL), []);
  
  // Distribute personas across reels
  const reelsSymbols = useMemo(() => {
    const filtered = getPersonasByCategory(categoryFilter);
    const shuffled = shuffleArray(filtered);
    
    const out = [];
    for (let r = 0; r < REELS; r++) {
      const reel = [];
      for (let s = 0; s < SYMBOLS_PER_REEL; s++) {
        const idx = (r * SYMBOLS_PER_REEL + s) % shuffled.length;
        reel.push(shuffled[idx]);
      }
      out.push(reel);
    }
    return out;
  }, [categoryFilter]);

  const [rotations, setRotations] = useState(() => Array(REELS).fill(0));
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(() => Array(REELS).fill(null));
  const animRef = useRef(null);
  const spinPlanRef = useRef(null);

  function frontIndexFromRotation(rotDeg) {
    const r = mod(rotDeg, 360);
    const raw = -r / step;
    return mod(Math.round(raw), SYMBOLS_PER_REEL);
  }

  function getPaylineSymbols(rotArr) {
    return rotArr.map((rot, r) => {
      const idx = frontIndexFromRotation(rot);
      return reelsSymbols[r][idx];
    });
  }

  function stopAll() {
    if (animRef.current) cancelAnimationFrame(animRef.current);
    animRef.current = null;
    spinPlanRef.current = null;
    setSpinning(false);
    setResult(getPaylineSymbols(rotations));
  }

  function spin() {
    if (spinning) return;
    const now = performance.now();
    const plan = Array.from({ length: REELS }, (_, r) => {
      const startRot = rotations[r];
      const stopIdx = Math.floor(Math.random() * SYMBOLS_PER_REEL);
      const target = -stopIdx * step;
      const startMod = mod(startRot, 360);
      const targetMod = mod(target, 360);
      const delta = mod(targetMod - startMod, 360);
      const extraCycles = 3 + Math.floor(Math.random() * 3);
      const endRot = startRot + extraCycles * 360 + delta;
      const duration = 1000 + r * 120 + Math.floor(Math.random() * 300);
      return { startRot, endRot, stopIdx, duration, startTime: now };
    });

    setSpinning(true);
    setResult(Array(REELS).fill(null));
    spinPlanRef.current = plan;

    const tick = (t) => {
      const p = spinPlanRef.current;
      if (!p) return;
      let allDone = true;
      const next = rotations.slice();
      for (let r = 0; r < REELS; r++) {
        const { startRot, endRot, duration, startTime } = p[r];
        const elapsed = t - startTime;
        const u = Math.min(Math.max(elapsed / duration, 0), 1);
        const e = easeOutCubic(u);
        next[r] = startRot + (endRot - startRot) * e;
        if (u < 1) allDone = false;
      }
      setRotations(next);
      if (!allDone) {
        animRef.current = requestAnimationFrame(tick);
      } else {
        animRef.current = null;
        spinPlanRef.current = null;
        setSpinning(false);
        setResult(getPaylineSymbols(next));
      }
    };
    animRef.current = requestAnimationFrame(tick);
  }

  // Initialize with offset positions
  useEffect(() => {
    setRotations((prev) => {
      const init = prev.slice();
      for (let r = 0; r < REELS; r++) init[r] = -(r % SYMBOLS_PER_REEL) * step;
      return init;
    });
  }, [step]);

  // Keyboard handler
  useEffect(() => {
    const onKeyDown = (e) => {
      if (e.code === "Space") {
        e.preventDefault();
        spin();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [spinning, rotations]);

  // Cleanup
  useEffect(() => {
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, []);

  const frameW = REELS * CELL;
  const frameH = Math.round(CELL * 2.6);

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Spin controls */}
      <div className="flex gap-2">
        <button
          onClick={spin}
          disabled={spinning}
          className="px-6 py-3 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {spinning ? "Spinning..." : "🎰 SPIN"}
        </button>
        <button
          onClick={stopAll}
          className="px-4 py-3 rounded-xl border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-300"
        >
          Stop
        </button>
      </div>
      
      <div className="text-sm text-zinc-500">Press SPACE or click Spin</div>

      {/* Reel container */}
      <div className="relative rounded-3xl border border-zinc-800 bg-zinc-900/50 shadow-2xl overflow-hidden">
        <div className="mx-auto relative" style={{ width: frameW, height: frameH }}>
          <div className="absolute inset-0 flex">
            {reelsSymbols.map((reel, r) => (
              <Reel
                key={r}
                symbols={reel}
                rotation={rotations[r]}
                radius={radius}
                step={step}
                onSymbolClick={onSelectPersona}
              />
            ))}
          </div>
          
          {/* Payline overlay */}
          <div
            className="pointer-events-none absolute left-0 right-0"
            style={{ top: (frameH - CELL) / 2, height: CELL }}
          >
            <div className="absolute inset-0 border-y-2 border-amber-400/80" />
            <div
              className="absolute inset-0"
              style={{
                background: "linear-gradient(to right, rgba(245,158,11,0.05), rgba(245,158,11,0.15), rgba(245,158,11,0.05))",
              }}
            />
          </div>
        </div>
      </div>

      {/* Result display */}
      <div className="w-full max-w-2xl rounded-2xl border border-zinc-800 bg-zinc-950/60 p-4">
        <div className="text-sm text-zinc-400 mb-3">✨ Payline Result</div>
        {result[0] ? (
          <div className="flex flex-wrap gap-2 justify-center">
            {result.map((persona, i) => (
              <button
                key={i}
                onClick={() => persona.status === 'active' && onSelectPersona?.(persona)}
                className={`px-3 py-2 rounded-xl border transition-colors ${
                  persona.status === 'active' 
                    ? 'border-amber-600/50 bg-amber-900/30 hover:bg-amber-800/40 cursor-pointer' 
                    : 'border-zinc-700 bg-zinc-800/50 cursor-not-allowed opacity-60'
                }`}
              >
                <span className="font-semibold text-white">{persona.name}</span>
                {persona.status !== 'active' && (
                  <span className="ml-2 text-xs text-zinc-500">(soon)</span>
                )}
              </button>
            ))}
          </div>
        ) : (
          <div className="text-zinc-500 text-center">Spin to discover personas!</div>
        )}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// BROWSE MODE COMPONENT
// ═══════════════════════════════════════════
function BrowseMode({ onSelectPersona, activeCategory, setActiveCategory }) {
  const personas = useMemo(() => getPersonasByCategory(activeCategory), [activeCategory]);
  
  return (
    <div className="flex flex-col gap-6">
      {/* Category dropdown */}
      <div className="flex items-center gap-3">
        <label className="text-zinc-400 text-sm">Category:</label>
        <select
          value={activeCategory}
          onChange={(e) => setActiveCategory(e.target.value)}
          className="px-4 py-2 rounded-xl bg-zinc-800 border border-zinc-700 text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
        >
          <option value="all">All ({PERSONAS.length})</option>
          {Object.values(CATEGORIES).map(cat => (
            <option key={cat.id} value={cat.id}>
              {cat.name} ({getPersonasByCategory(cat.id).length})
            </option>
          ))}
        </select>
      </div>

      {/* Persona grid */}
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4">
        {personas.map(persona => (
          <div key={persona.id} className="flex flex-col items-center gap-2">
            <PersonaCard
              persona={persona}
              size={100}
              onClick={(p) => p.status === 'active' && onSelectPersona?.(p)}
            />
            <div className="text-center">
              <div className="text-xs text-white font-medium truncate max-w-[100px]">
                {persona.name}
              </div>
              <div className="text-[10px] text-zinc-500 truncate max-w-[100px]">
                {persona.title?.split(',')[0]}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// MAIN SPINNER COMPONENT
// ═══════════════════════════════════════════
export default function PersonaSpinner({ onSelectPersona }) {
  const [mode, setMode] = useState('spin'); // 'spin' | 'browse'
  const [activeCategory, setActiveCategory] = useState('all');
  const [selectedPersona, setSelectedPersona] = useState(null);

  const handleSelectPersona = useCallback((persona) => {
    setSelectedPersona(persona);
    onSelectPersona?.(persona);
  }, [onSelectPersona]);

  return (
    <div className="min-h-screen w-full bg-zinc-950 text-zinc-100 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-semibold">Echoes of Indiana</h1>
            <p className="text-zinc-400 text-sm">Select a persona to commune with</p>
          </div>
          
          {/* Mode toggle */}
          <div className="flex rounded-xl overflow-hidden border border-zinc-700">
            <button
              onClick={() => setMode('spin')}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                mode === 'spin' 
                  ? 'bg-amber-600 text-white' 
                  : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              🎰 Spin
            </button>
            <button
              onClick={() => setMode('browse')}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                mode === 'browse' 
                  ? 'bg-amber-600 text-white' 
                  : 'bg-zinc-800 text-zinc-400 hover:text-white'
              }`}
            >
              📋 Browse
            </button>
          </div>
        </div>

        {/* Mode content */}
        <div className="mt-4">
          {mode === 'spin' ? (
            <SpinMode 
              onSelectPersona={handleSelectPersona}
              categoryFilter={activeCategory}
            />
          ) : (
            <BrowseMode
              onSelectPersona={handleSelectPersona}
              activeCategory={activeCategory}
              setActiveCategory={setActiveCategory}
            />
          )}
        </div>

        {/* Selected persona indicator */}
        {selectedPersona && (
          <div className="fixed bottom-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-2xl bg-amber-600 text-white shadow-lg">
            Selected: <strong>{selectedPersona.name}</strong>
            {selectedPersona.status !== 'active' && (
              <span className="ml-2 text-amber-200">(coming soon)</span>
            )}
          </div>
        )}

        {/* Stats */}
        <div className="mt-8 text-center text-xs text-zinc-600">
          {PERSONAS.filter(p => p.status === 'active').length} active / {PERSONAS.length} total personas
        </div>
      </div>
    </div>
  );
}



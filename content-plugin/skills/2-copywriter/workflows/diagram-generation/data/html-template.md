# HTML Template — Diagram Generation

Generate the complete HTML file below, substituting the `/* === DIAGRAM CONTENT === */` section with the diagram-specific `TitleBlock` and `App()` components.

The JSX components are inlined verbatim from the design system UI kit. The only modification is `ScreenshotNode`, which now accepts a `src` prop to render real images.

---

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{VIDEO_TITLE} — @{YOUR_HANDLE_PERSONAL}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; font-family: Inter, sans-serif; background: #f5f0e8; }
  #root { height: 100%; }
  button { font-family: inherit; }
</style>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
</head>
<body>
<div id="root"></div>

<script type="text/babel">
/* global React, ReactDOM */

// ============================================================
// MapCanvas.jsx — pan + zoom workbench
// ============================================================
const WORLD_W = {WORLD_W};
const WORLD_H = {WORLD_H};

function MapCanvas({ children, worldW = WORLD_W, worldH = WORLD_H }) {
  const containerRef = React.useRef(null);

  const computeFit = React.useCallback(() => {
    const el = containerRef.current;
    const vw = el ? el.clientWidth : window.innerWidth;
    const targetW = 2600;
    const z = Math.max(0.35, Math.min(0.7, vw / targetW));
    return { tx: 40, ty: 40, zoom: z };
  }, []);

  const [tx, setTx] = React.useState(40);
  const [ty, setTy] = React.useState(40);
  const [zoom, setZoom] = React.useState(0.55);
  const draggingRef = React.useRef(null);

  React.useEffect(() => {
    const saved = localStorage.getItem("ag_map_view");
    if (saved) {
      try {
        const v = JSON.parse(saved);
        if (typeof v.tx === "number") setTx(v.tx);
        if (typeof v.ty === "number") setTy(v.ty);
        if (typeof v.zoom === "number") setZoom(v.zoom);
        return;
      } catch {}
    }
    const fit = computeFit();
    setTx(fit.tx); setTy(fit.ty); setZoom(fit.zoom);
  }, [computeFit]);

  React.useEffect(() => {
    localStorage.setItem("ag_map_view", JSON.stringify({ tx, ty, zoom }));
  }, [tx, ty, zoom]);

  const onMouseDown = (e) => {
    if (e.button !== 0) return;
    draggingRef.current = { x: e.clientX, y: e.clientY, tx, ty };
    e.preventDefault();
  };
  const onMouseMove = React.useCallback((e) => {
    if (!draggingRef.current) return;
    const d = draggingRef.current;
    setTx(d.tx + (e.clientX - d.x));
    setTy(d.ty + (e.clientY - d.y));
  }, []);
  const onMouseUp = React.useCallback(() => { draggingRef.current = null; }, []);

  React.useEffect(() => {
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, [onMouseMove, onMouseUp]);

  const onWheel = (e) => {
    e.preventDefault();
    const rect = containerRef.current.getBoundingClientRect();
    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;
    const delta = -e.deltaY;
    const factor = Math.exp(delta * 0.0015);
    const newZoom = Math.max(0.25, Math.min(2.5, zoom * factor));
    const wx = (cx - tx) / zoom;
    const wy = (cy - ty) / zoom;
    setZoom(newZoom);
    setTx(cx - wx * newZoom);
    setTy(cy - wy * newZoom);
  };

  const resetView = () => {
    const fit = computeFit();
    setTx(fit.tx); setTy(fit.ty); setZoom(fit.zoom);
    localStorage.removeItem("ag_map_view");
  };
  const zoomBtn = (dir) => {
    const rect = containerRef.current.getBoundingClientRect();
    const cx = rect.width / 2, cy = rect.height / 2;
    const factor = dir > 0 ? 1.2 : 1 / 1.2;
    const newZoom = Math.max(0.25, Math.min(2.5, zoom * factor));
    const wx = (cx - tx) / zoom, wy = (cy - ty) / zoom;
    setZoom(newZoom);
    setTx(cx - wx * newZoom);
    setTy(cy - wy * newZoom);
  };

  const dotSpacing = 28;
  const bgStyle = {
    position: "absolute", inset: 0,
    backgroundColor: "#f5f0e8",
    backgroundImage: "radial-gradient(circle, #c9bfb2 1.3px, transparent 1.6px)",
    backgroundSize: `${dotSpacing * zoom}px ${dotSpacing * zoom}px`,
    backgroundPosition: `${tx}px ${ty}px`,
  };

  return (
    <div
      ref={containerRef}
      onMouseDown={onMouseDown}
      onWheel={onWheel}
      style={{
        width: "100vw", height: "100vh",
        overflow: "hidden", position: "relative",
        cursor: draggingRef.current ? "grabbing" : "grab",
        userSelect: "none", fontFamily: "Inter, sans-serif", background: "#f5f0e8",
      }}>
      <div style={bgStyle} />
      <div style={{
        position: "absolute", left: 0, top: 0,
        width: worldW, height: worldH,
        transform: `translate(${tx}px, ${ty}px) scale(${zoom})`,
        transformOrigin: "0 0",
      }}>
        {children}
      </div>
      <div style={{
        position: "absolute", top: 16, left: 16,
        display: "inline-flex", gap: 10, alignItems: "center",
        fontFamily: "JetBrains Mono, monospace", fontSize: 11,
        letterSpacing: "0.14em", textTransform: "uppercase", color: "#7a726b",
        pointerEvents: "none",
        background: "rgba(250, 250, 248, 0.92)", border: "1px solid #d8d2cc",
        borderRadius: 6, padding: "7px 12px",
        boxShadow: "0 1px 3px rgba(26,22,20,0.06)",
        whiteSpace: "nowrap", maxWidth: "calc(100vw - 32px)",
        overflow: "hidden", textOverflow: "ellipsis",
      }}>
        <span style={{ color: "#d97757", fontWeight: 700 }}>@{YOUR_HANDLE_PERSONAL}</span>
        <span style={{ color: "#c9bfb2" }}>/</span>
        <span>map</span>
        <span style={{ color: "#c9bfb2" }}>·</span>
        <span>drag to pan · scroll to zoom</span>
      </div>
      <div style={{
        position: "absolute", bottom: 24, right: 24,
        display: "flex", flexDirection: "column", gap: 6,
        background: "#fafaf8", border: "1px solid #d8d2cc",
        borderRadius: 10, padding: 6,
        boxShadow: "0 2px 6px rgba(26,22,20,0.08)",
      }}>
        <CtrlBtn onClick={() => zoomBtn(1)}>+</CtrlBtn>
        <div style={{
          textAlign: "center", fontFamily: "JetBrains Mono, monospace",
          fontSize: 11, color: "#7a726b", padding: "2px 0",
        }}>{Math.round(zoom * 100)}%</div>
        <CtrlBtn onClick={() => zoomBtn(-1)}>−</CtrlBtn>
        <div style={{ height: 1, background: "#e8e1d9", margin: "4px 2px" }}/>
        <CtrlBtn onClick={resetView} small>⟲</CtrlBtn>
      </div>
    </div>
  );
}

function CtrlBtn({ children, onClick, small }) {
  const [hovered, setHovered] = React.useState(false);
  return (
    <button
      onClick={(e) => { e.stopPropagation(); onClick(); }}
      onMouseDown={(e) => e.stopPropagation()}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        width: 34, height: 34, borderRadius: 6, border: "none",
        background: hovered ? "#f2ede8" : "transparent",
        color: "#1a1614",
        fontFamily: small ? "Inter, sans-serif" : "JetBrains Mono, monospace",
        fontSize: small ? 18 : 20, fontWeight: 700, cursor: "pointer",
        display: "flex", alignItems: "center", justifyContent: "center",
      }}>
      {children}
    </button>
  );
}

// ============================================================
// Connector.jsx — SVG arrow layer
// ============================================================
function ConnectorLayer({ children, worldW = WORLD_W, worldH = WORLD_H }) {
  return (
    <svg
      width={worldW} height={worldH}
      viewBox={`0 0 ${worldW} ${worldH}`}
      style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
      <defs>
        <marker id="arrowhead-orange" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="8" markerHeight="8" orient="auto-start-reverse">
          <path d="M 0 0 L 12 6 L 0 12 z" fill="#d97757"/>
        </marker>
        <marker id="arrowhead-grey" viewBox="0 0 12 12" refX="10" refY="6"
          markerWidth="8" markerHeight="8" orient="auto-start-reverse">
          <path d="M 0 0 L 12 6 L 0 12 z" fill="#7a726b"/>
        </marker>
      </defs>
      {children}
    </svg>
  );
}

function Connector({ from, to, kind = "curve", curvature = 0.35, label, dashed = false, stroke = "#d97757", strokeWidth = 3 }) {
  let d;
  if (kind === "straight") {
    d = `M ${from.x} ${from.y} L ${to.x} ${to.y}`;
  } else if (kind === "elbow") {
    const midX = (from.x + to.x) / 2;
    d = `M ${from.x} ${from.y} L ${midX} ${from.y} L ${midX} ${to.y} L ${to.x} ${to.y}`;
  } else {
    const dx = to.x - from.x, dy = to.y - from.y;
    const len = Math.max(1, Math.hypot(dx, dy));
    const perpX = -dy / len, perpY = dx / len;
    const bulge = len * curvature;
    const c1x = from.x + dx * 0.25 + perpX * bulge;
    const c1y = from.y + dy * 0.25 + perpY * bulge;
    const c2x = from.x + dx * 0.75 + perpX * bulge;
    const c2y = from.y + dy * 0.75 + perpY * bulge;
    d = `M ${from.x} ${from.y} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${to.x} ${to.y}`;
  }
  const midX = (from.x + to.x) / 2;
  const midY = (from.y + to.y) / 2;
  const arrowId = stroke === "#d97757" ? "arrowhead-orange" : "arrowhead-grey";
  return (
    <g>
      <path d={d} fill="none" stroke={stroke} strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={dashed ? "8 8" : undefined}
        markerEnd={`url(#${arrowId})`}
      />
      {label && (
        <g transform={`translate(${midX}, ${midY - 14})`}>
          <rect x={-label.length * 4.4} y={-14} width={label.length * 8.8} height={24}
            fill="#fafaf8" stroke="#d8d2cc" strokeWidth="1" rx="4" />
          <text x="0" y="2" textAnchor="middle" dominantBaseline="middle"
            fontFamily="JetBrains Mono, monospace" fontSize="13" fontWeight="700"
            letterSpacing="0.08em" fill="#1a1614">
            {label.toUpperCase()}
          </text>
        </g>
      )}
    </g>
  );
}

// ============================================================
// Nodes.jsx — all node primitives
// ============================================================

function ConceptNode({ x, y, w = 360, tag, title, body, accent }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      background: "#fafaf8", border: "1.5px solid #1a1614",
      borderRadius: 10, padding: "22px 24px 24px",
      boxShadow: "4px 4px 0 #1a1614", fontFamily: "Inter, sans-serif",
    }}>
      {tag && (
        <div style={{
          fontFamily: "JetBrains Mono, monospace", fontSize: 11, color: "#d97757",
          fontWeight: 700, letterSpacing: "0.16em", textTransform: "uppercase", marginBottom: 10,
        }}>{tag}</div>
      )}
      <div style={{
        fontFamily: "Inter, sans-serif", fontSize: 26, fontWeight: 900,
        letterSpacing: "-0.02em", lineHeight: 1.1, color: "#1a1614",
        marginBottom: body ? 10 : 0,
      }}>
        {title}
        {accent && <> <span style={{ color: "#d97757" }}>{accent}</span></>}
      </div>
      {body && (
        <div style={{ fontSize: 15, lineHeight: 1.45, color: "#3d3833", letterSpacing: "-0.005em" }}>
          {body}
        </div>
      )}
    </div>
  );
}

function CodeNode({ x, y, w = 460, title, lines = [] }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      background: "#1c2128", border: "1.5px solid #1a1614",
      borderRadius: 10, boxShadow: "4px 4px 0 #1a1614", overflow: "hidden",
    }}>
      <div style={{
        background: "#15191f", padding: "10px 14px",
        display: "flex", alignItems: "center", gap: 8,
        borderBottom: "1px solid #30363d",
      }}>
        <span style={{ width: 10, height: 10, borderRadius: 999, background: "#d97757" }}/>
        <span style={{ width: 10, height: 10, borderRadius: 999, background: "#f4a387" }}/>
        <span style={{ width: 10, height: 10, borderRadius: 999, background: "#30363d" }}/>
        {title && (
          <span style={{
            marginLeft: 12, fontFamily: "JetBrains Mono, monospace",
            fontSize: 11, color: "#7a726b", letterSpacing: "0.08em",
          }}>{title}</span>
        )}
      </div>
      <div style={{
        padding: "18px 20px", fontFamily: "JetBrains Mono, monospace",
        fontSize: 14, lineHeight: 1.65, color: "#c9d1d9",
      }}>
        {lines.map((line, i) => {
          if (typeof line === "string") {
            return <div key={i} style={{ minHeight: "1.5em" }}>{line || "\u00a0"}</div>;
          }
          return (
            <div key={i} style={{ minHeight: "1.5em" }}>
              {line.parts.map((p, j) => (
                <span key={j} style={{ color: p.c || "#c9d1d9" }}>{p.t}</span>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ScreenshotNode({ x, y, w = 420, h = 280, caption, src, label = "SCREENSHOT HERE", rotate = -1.5, pin = "tape" }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      transform: `rotate(${rotate}deg)`, transformOrigin: "50% 0%",
    }}>
      {pin === "tape" ? (
        <div style={{
          position: "absolute", top: -12, left: "50%",
          transform: "translateX(-50%) rotate(-3deg)",
          width: 90, height: 24,
          background: "rgba(217, 119, 87, 0.35)",
          border: "1px solid rgba(217, 119, 87, 0.5)",
          borderRadius: 2, zIndex: 2,
        }}/>
      ) : (
        <div style={{
          position: "absolute", top: -8, left: "50%",
          transform: "translateX(-50%)",
          width: 18, height: 18, borderRadius: 999,
          background: "#d97757",
          boxShadow: "inset -2px -2px 0 rgba(0,0,0,0.2), 0 2px 4px rgba(0,0,0,0.25)",
          zIndex: 2,
        }}/>
      )}
      <div style={{
        background: "#fafaf8", border: "1.5px solid #1a1614",
        boxShadow: "4px 4px 0 #1a1614", padding: 10,
      }}>
        {src ? (
          <img src={src} alt={caption || label} style={{
            width: "100%", height: h, objectFit: "cover",
            border: "none", display: "block", borderRadius: 2,
          }} />
        ) : (
          <div style={{
            width: "100%", height: h,
            background: "#f2ede8", border: "2px dashed #b9b2ab",
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center", gap: 6,
          }}>
            <div style={{
              fontFamily: "JetBrains Mono, monospace", fontSize: 13, fontWeight: 700,
              letterSpacing: "0.14em", color: "#9a928c",
            }}>[{label}]</div>
            <div style={{
              fontFamily: "JetBrains Mono, monospace", fontSize: 10,
              color: "#b9b2ab", letterSpacing: "0.06em",
            }}>drop image into assets/</div>
          </div>
        )}
        {caption && (
          <div style={{
            marginTop: 10, padding: "4px 2px",
            fontFamily: "Inter, sans-serif", fontSize: 14,
            color: "#3d3833", textAlign: "center", fontStyle: "italic",
          }}>{caption}</div>
        )}
      </div>
    </div>
  );
}

function PromptNode({ x, y, w = 260, label = "PROMPT", text }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      background: "#1a1614", color: "#fafaf8",
      borderRadius: 12, padding: "14px 18px",
      fontFamily: "JetBrains Mono, monospace",
      boxShadow: "3px 3px 0 #d97757",
    }}>
      <div style={{
        fontSize: 10, fontWeight: 700, letterSpacing: "0.2em",
        color: "#d97757", marginBottom: 6,
      }}>{label}</div>
      <div style={{ fontSize: 14, lineHeight: 1.45, letterSpacing: "-0.005em" }}>{text}</div>
    </div>
  );
}

function SectionSign({ x, y, w = 320, number, label }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      display: "flex", alignItems: "center", gap: 14,
    }}>
      <div style={{
        width: 72, height: 72, background: "#d97757",
        border: "2px solid #1a1614", boxShadow: "3px 3px 0 #1a1614",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: "JetBrains Mono, monospace", fontSize: 28, fontWeight: 700,
        color: "#1a1614", letterSpacing: "-0.02em", flexShrink: 0,
      }}>{number}</div>
      <div style={{
        fontFamily: "Inter, sans-serif", fontSize: 34, fontWeight: 900,
        letterSpacing: "-0.025em", color: "#1a1614", lineHeight: 1,
      }}>{label}</div>
    </div>
  );
}

function DecisionNode({ x, y, w = 200, h = 140, question, yes = "yes", no = "no" }) {
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h }}>
      <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ position: "absolute", inset: 0 }}>
        <polygon points={`${w/2},4 ${w-4},${h/2} ${w/2},${h-4} 4,${h/2}`}
          fill="#fafaf8" stroke="#1a1614" strokeWidth="2" />
        <polygon points={`${w/2},8 ${w-8},${h/2} ${w/2},${h-8} 8,${h/2}`}
          fill="none" stroke="#d97757" strokeWidth="1.5" strokeDasharray="5 4" />
      </svg>
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: "0 30px", textAlign: "center",
        fontFamily: "Inter, sans-serif", fontSize: 15, fontWeight: 700,
        letterSpacing: "-0.01em", lineHeight: 1.15, color: "#1a1614",
      }}>{question}</div>
      <div style={{
        position: "absolute", right: -8, top: h/2 - 10,
        transform: "translateX(100%)",
        fontFamily: "JetBrains Mono, monospace", fontSize: 11, fontWeight: 700,
        letterSpacing: "0.16em", color: "#d97757",
      }}>{yes.toUpperCase()} →</div>
      <div style={{
        position: "absolute", left: w/2 - 14, top: h + 2,
        fontFamily: "JetBrains Mono, monospace", fontSize: 11, fontWeight: 700,
        letterSpacing: "0.16em", color: "#7a726b",
      }}>↓ {no.toUpperCase()}</div>
    </div>
  );
}

function StepMarker({ x, y, number, label }) {
  const size = 64;
  return (
    <div style={{ position: "absolute", left: x - size/2, top: y - size/2, width: size, height: size }}>
      <div style={{
        width: size, height: size, borderRadius: 999,
        background: "#fafaf8", border: "2.5px solid #d97757",
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: "0 2px 4px rgba(26,22,20,0.15)",
        fontFamily: "JetBrains Mono, monospace", fontSize: 20, fontWeight: 700, color: "#1a1614",
      }}>{String(number).padStart(2,"0")}</div>
      {label && (
        <div style={{
          position: "absolute", top: size + 6, left: "50%", transform: "translateX(-50%)",
          whiteSpace: "nowrap",
          fontFamily: "JetBrains Mono, monospace", fontSize: 12, fontWeight: 700,
          letterSpacing: "0.1em", textTransform: "uppercase", color: "#1a1614",
          background: "#fafaf8", padding: "3px 8px", borderRadius: 4, border: "1px solid #d8d2cc",
        }}>{label}</div>
      )}
    </div>
  );
}

function QuoteNode({ x, y, w = 360, quote, attribution }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w,
      padding: "22px 26px 22px 32px",
      fontFamily: "Inter, sans-serif", background: "transparent",
      borderLeft: "4px solid #d97757",
    }}>
      <div style={{
        fontSize: 24, fontWeight: 500, lineHeight: 1.3,
        letterSpacing: "-0.015em", color: "#1a1614",
      }}>
        <span style={{ color: "#d97757", fontWeight: 900 }}>"</span>
        {quote}
        <span style={{ color: "#d97757", fontWeight: 900 }}>"</span>
      </div>
      {attribution && (
        <div style={{
          marginTop: 10, fontFamily: "JetBrains Mono, monospace",
          fontSize: 12, color: "#7a726b",
          letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 700,
        }}>— {attribution}</div>
      )}
    </div>
  );
}

// ============================================================
// === DIAGRAM CONTENT ===
// Replace this section with the diagram-specific components.
// Keep everything above unchanged.
// ============================================================

function TitleBlock({ x, y }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: 760,
      fontFamily: "Inter, sans-serif",
    }}>
      <div style={{
        fontFamily: "JetBrains Mono, monospace", fontSize: 14, color: "#d97757",
        fontWeight: 700, letterSpacing: "0.22em", textTransform: "uppercase", marginBottom: 14,
      }}>The Map · 01</div>
      <h1 style={{
        fontSize: 68, fontWeight: 900, lineHeight: 0.95,
        letterSpacing: "-0.035em", color: "#1a1614", margin: 0,
      }}>
        {/* VIDEO TITLE: replace accent word below */}
        How I build things <span style={{ position: "relative", display: "inline-block" }}>
          <span style={{ color: "#d97757" }}>end-to-end</span>
          <span style={{
            position: "absolute", left: 0, right: 0, bottom: -4,
            height: 8, background: "#d97757", borderRadius: 2,
          }}/>
        </span>
        <br/>with Claude.
      </h1>
      <div style={{
        marginTop: 20, fontSize: 20, color: "#3d3833", maxWidth: 640, lineHeight: 1.45,
      }}>
        {/* SUBTITLE */}
        Drag to explore · scroll to zoom.
      </div>
    </div>
  );
}

function App() {
  return (
    <MapCanvas worldW={WORLD_W} worldH={WORLD_H}>
      <ConnectorLayer worldW={WORLD_W} worldH={WORLD_H}>
        {/* CONNECTORS GO HERE */}
      </ConnectorLayer>

      <TitleBlock x={140} y={140} />

      {/* NODES GO HERE */}

      {/* Legend — always bottom-left */}
      <div style={{
        position: "absolute", left: 160, top: WORLD_H - 280, width: 560,
        padding: "14px 18px",
        background: "#fafaf8", border: "1px solid #d8d2cc",
        borderRadius: 8, fontFamily: "JetBrains Mono, monospace",
        fontSize: 12, color: "#3d3833", letterSpacing: "0.06em",
        display: "flex", flexDirection: "column", gap: 6,
      }}>
        <div style={{ fontWeight: 700, color: "#d97757", letterSpacing: "0.18em", fontSize: 11 }}>LEGEND</div>
        <div>—— solid : the flow (happy path)</div>
        <div>- - dashed : iteration · loopback · compounding memory</div>
        <div>● numbered circle : a waypoint · something on disk</div>
        <div>◆ diamond : a decision</div>
      </div>

    </MapCanvas>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body>
</html>
```

---

## Substitution Instructions

When generating a diagram, replace these placeholders:

| Placeholder | Replace with |
|-------------|--------------|
| `{WORLD_W}` | World width (e.g., `3000` or `3600`) |
| `{WORLD_H}` | World height (e.g., `2000` or `2200`) |
| `{VIDEO_TITLE}` | The video title in `<title>` tag |
| `The Map · 01` | The map series label (keep format) |
| The H1 content | The actual video title with accent word |
| `Drag to explore · scroll to zoom.` | The subtitle explaining the map's scope |
| `{/* CONNECTORS GO HERE */}` | All `<Connector>` elements |
| `{/* NODES GO HERE */}` | All node elements (SectionSign, ConceptNode, etc.) |
| `WORLD_H - 280` | Adjust legend Y if needed (always near bottom) |

## Output path

Save to: `{project_path}/copywriter/diagrams/diagram-{slug}.html`

Create the `diagrams/` folder if it doesn't exist.

## After generating

Tell the user:
```
Open in browser: double-click the HTML file (Chrome/Safari work best)
Pan: drag anywhere on the canvas
Zoom: scroll wheel or pinch
Reset view: click the ⟲ button (bottom-right)
```

/* global React */
// SlideFrame.jsx v2 — three background variants: paper / dark / hero.
// All slides are 1080×1350. Footer: @{YOUR_HANDLE_PERSONAL} (left) + save for later › (right). Slide counter mono top-right.

function SlideFrame({
  children,
  bg = "paper",          // "paper" | "dark" | "hero"
  heroSrc,               // required if bg === "hero"
  showCounter = true,
  showNextHint = true,
  darkFooter = false,    // override footer color on paper when overlaying dark block
  index, total,
}) {
  const isDark = bg === "dark" || bg === "hero" || darkFooter;
  const footerColor = isDark ? "#fafaf8" : "#1a1614";
  const accentColor = "#d97757";

  // background styles
  let bgStyle = {};
  if (bg === "paper") {
    bgStyle = {
      background: "#f5f0e8",
      backgroundImage: "radial-gradient(circle, #d8cfc0 1.4px, transparent 1.6px)",
      backgroundSize: "28px 28px",
      backgroundPosition: "14px 14px",
    };
  } else if (bg === "dark") {
    bgStyle = {
      background: "#0f0d0b",
      backgroundImage:
        "radial-gradient(circle at 20% 10%, rgba(217,119,87,0.12), transparent 45%)," +
        "radial-gradient(circle at 90% 90%, rgba(217,119,87,0.08), transparent 50%)," +
        "linear-gradient(#0f0d0b, #0a0706)",
    };
  } else if (bg === "hero" && heroSrc) {
    bgStyle = {
      background: `linear-gradient(180deg, rgba(10,7,6,0.35) 0%, rgba(10,7,6,0.15) 45%, rgba(10,7,6,0.9) 100%), url(${heroSrc}) center/cover no-repeat`,
    };
  }

  return (
    <div style={{
      width: 1080,
      height: 1350,
      position: "relative",
      padding: "64px 72px 104px",
      boxSizing: "border-box",
      fontFamily: "Inter, sans-serif",
      color: isDark ? "#fafaf8" : "#1a1614",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
      ...bgStyle,
    }}>
      {/* grain overlay for dark */}
      {bg === "dark" && (
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none", opacity: 0.35,
          backgroundImage: "radial-gradient(#fafaf8 0.5px, transparent 0.8px)",
          backgroundSize: "3px 3px",
          mixBlendMode: "overlay",
        }}/>
      )}

      {/* top-right save icon */}
      <div style={{
        position: "absolute", top: 32, right: 40,
        width: 36, height: 40,
        border: `2px solid ${isDark ? "rgba(250,250,248,0.8)" : "rgba(26,22,20,0.8)"}`,
        borderBottom: "none",
        borderTop: isDark ? "2px solid rgba(250,250,248,0.8)" : "2px solid rgba(26,22,20,0.8)",
      }}>
        <div style={{
          position: "absolute", bottom: -2, left: "50%",
          transform: "translateX(-50%) rotate(45deg)",
          width: 18, height: 18,
          background: "transparent",
          borderRight: `2px solid ${isDark ? "rgba(250,250,248,0.8)" : "rgba(26,22,20,0.8)"}`,
          borderBottom: `2px solid ${isDark ? "rgba(250,250,248,0.8)" : "rgba(26,22,20,0.8)"}`,
        }}/>
      </div>

      {/* content */}
      <div style={{ position: "relative", flex: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
        {children}
      </div>

      {/* footer */}
      <div style={{
        position: "absolute",
        left: 72, right: 72, bottom: 44,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        fontFamily: "JetBrains Mono, monospace",
        fontSize: 18,
        letterSpacing: "0.04em",
      }}>
        <span style={{ color: footerColor, opacity: isDark ? 0.75 : 0.6 }}>@{YOUR_HANDLE_PERSONAL}</span>
        <span style={{ color: footerColor, opacity: isDark ? 0.85 : 0.7, display: "inline-flex", alignItems: "center", gap: 10, whiteSpace: "nowrap" }}>
          {showNextHint ? (
            <>
              save for later
              <span style={{
                display: "inline-flex", alignItems: "center", justifyContent: "center",
                width: 34, height: 34, borderRadius: 4,
                border: `1.5px solid ${footerColor}`,
                color: footerColor,
                fontSize: 16, fontWeight: 700,
                opacity: 0.9,
              }}>→</span>
            </>
          ) : null}
        </span>
      </div>

      {/* slide counter — sits above the footer line to avoid colliding with @{YOUR_HANDLE_PERSONAL} */}
      {showCounter && (
        <div style={{
          position: "absolute", bottom: 92, left: "50%", transform: "translateX(-50%)",
          fontFamily: "JetBrains Mono, monospace",
          fontSize: 11,
          color: footerColor,
          opacity: 0.35,
          letterSpacing: "0.25em",
          whiteSpace: "nowrap",
        }}>{String(index).padStart(2,"0")} / {String(total).padStart(2,"0")}</div>
      )}
    </div>
  );
}

// Helper: the signature orange-underlined accent word
function Accent({ children, size = 8, color = "#d97757" }) {
  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      <span style={{ color }}>{children}</span>
      <span style={{
        position: "absolute", left: 0, right: 0, bottom: -4,
        height: size, background: color, borderRadius: 2,
      }}/>
    </span>
  );
}

// Helper: italic serif accent (for hero slides, like the refs)
function SerifAccent({ children, color = "#d97757" }) {
  return (
    <span style={{
      fontFamily: "'Instrument Serif', Georgia, serif",
      fontStyle: "italic",
      fontWeight: 400,
      color,
    }}>{children}</span>
  );
}

// Helper: huge ghost word behind a headline
function GhostWord({ children, top = -20, left = -20, opacity = 0.06, color = "#fafaf8" }) {
  return (
    <div style={{
      position: "absolute",
      top, left,
      fontFamily: "'Instrument Serif', Georgia, serif",
      fontStyle: "italic",
      fontWeight: 400,
      fontSize: 280,
      color,
      opacity,
      lineHeight: 0.9,
      letterSpacing: "-0.04em",
      pointerEvents: "none",
      whiteSpace: "nowrap",
      userSelect: "none",
      whiteSpace: "nowrap",
    }}>{children}</div>
  );
}

window.SlideFrame = SlideFrame;
window.Accent = Accent;
window.SerifAccent = SerifAccent;
window.GhostWord = GhostWord;

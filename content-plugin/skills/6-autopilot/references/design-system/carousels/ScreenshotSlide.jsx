/* global React, SlideFrame, Accent */
// ScreenshotSlide v2 — dark or paper. Titled placeholder with terminal/screenshot feel.

function ScreenshotSlide({ bg = "dark", eyebrow, title, accent, caption, label = "SCREENSHOT HERE", index, total }) {
  const isDark = bg === "dark";
  return (
    <SlideFrame bg={bg} index={index} total={total}>
      <div style={{
        fontFamily: "JetBrains Mono, monospace",
        fontWeight: 700,
        fontSize: 18,
        color: "#d97757",
        textTransform: "uppercase",
        letterSpacing: "0.22em",
        marginBottom: 16,
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        whiteSpace: "nowrap",
        alignSelf: "flex-start",
      }}>
        <span>▶</span>{eyebrow}
      </div>

      <h2 style={{
        fontFamily: "Inter, sans-serif",
        fontWeight: 900,
        fontSize: 72,
        lineHeight: 1.0,
        letterSpacing: "-0.03em",
        margin: 0,
        color: isDark ? "#fafaf8" : "#1a1614",
      }}>
        {title}
        {accent && <> <Accent size={8}>{accent}</Accent></>}
      </h2>

      {/* framed screenshot — flex-fills remaining vertical space */}
      <div style={{
        marginTop: 32,
        flex: 1,
        minHeight: 0,
        display: "flex",
        flexDirection: "column",
        background: isDark ? "#15110e" : "#fafaf8",
        border: isDark ? "2px solid rgba(217,119,87,0.4)" : "2px solid #1a1614",
        borderRadius: 14,
        padding: 14,
        boxShadow: isDark ? "0 0 40px rgba(217,119,87,0.15)" : "8px 8px 0 #1a1614",
      }}>
        {/* fake title bar */}
        <div style={{
          display: "flex", gap: 8, alignItems: "center",
          padding: "6px 4px 14px",
        }}>
          <span style={{ width: 12, height: 12, borderRadius: 999, background: "#d97757" }}/>
          <span style={{ width: 12, height: 12, borderRadius: 999, background: "#f4a387" }}/>
          <span style={{ width: 12, height: 12, borderRadius: 999, background: isDark ? "#2a1f18" : "#d8d2cc" }}/>
          <span style={{
            marginLeft: 14,
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 13,
            color: isDark ? "#7a6b5a" : "#7a726b",
            letterSpacing: "0.06em",
          }}>~/claude-code · preview</span>
        </div>

        <div style={{
          width: "100%",
          flex: 1,
          minHeight: 0,
          position: "relative",
          background: isDark
            ? "repeating-linear-gradient(45deg, #1c1611, #1c1611 12px, #201913 12px, #201913 24px)"
            : "repeating-linear-gradient(45deg, #f2ede8, #f2ede8 12px, #ece5db 12px, #ece5db 24px)",
          border: isDark ? "1px dashed rgba(217,119,87,0.35)" : "1px dashed #b9b2ab",
          borderRadius: 8,
          display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center",
        }}>
          <div style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 22,
            color: isDark ? "#d97757" : "#8a7e6c",
            letterSpacing: "0.2em",
            fontWeight: 700,
            textAlign: "center",
            padding: "0 32px",
            lineHeight: 1.4,
          }}>[{label}]</div>

          <div style={{
            position: "absolute",
            bottom: 18, left: 0, right: 0,
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 13,
            color: isDark ? "#7a6b5a" : "#b9b2ab",
            letterSpacing: "0.06em",
            textAlign: "center",
          }}>drop image into assets/ when ready</div>
        </div>
      </div>

      {caption && (
        <div style={{
          marginTop: 24,
          fontFamily: "Inter, sans-serif",
          fontSize: 26,
          color: isDark ? "#c9c0b3" : "#3d3833",
          lineHeight: 1.4,
          letterSpacing: "-0.005em",
          maxWidth: 900,
        }}>{caption}</div>
      )}
    </SlideFrame>
  );
}

window.ScreenshotSlide = ScreenshotSlide;

/* global React, SlideFrame, Accent, GhostWord, SerifAccent */
// ContentSlide v4 — supports "dark" or "paper". Ghost word low-right, content centered vertically,
// paper variant uses dark mono chip on cream for pop.

function ContentSlide({
  bg = "dark",
  badge,
  ghost,
  title,
  accent,
  serifAccent,
  body,
  mono,
  index, total,
}) {
  const isDark = bg === "dark";
  const bodyColor = isDark ? "#c9c0b3" : "#3d3833";
  const titleColor = isDark ? "#fafaf8" : "#1a1614";
  // Paper gets a DARK chip (inverted); dark gets subtle orange-tinted chip
  const monoBg = isDark ? "rgba(217,119,87,0.08)" : "#1a1614";
  const monoBorder = isDark ? "1px solid rgba(217,119,87,0.4)" : "1px solid #1a1614";
  const monoColor = isDark ? "#f4a387" : "#f5f0e8";
  const ghostColor = isDark ? "#fafaf8" : "#1a1614";

  return (
    <SlideFrame bg={bg} index={index} total={total}>
      {/* MASSIVE ghost word — bleeds off bottom-right */}
      {ghost && (
        <div style={{
          position: "absolute",
          bottom: -120,
          right: -80,
          fontFamily: "'Instrument Serif', Georgia, serif",
          fontStyle: "italic",
          fontWeight: 400,
          fontSize: 540,
          color: ghostColor,
          opacity: isDark ? 0.07 : 0.06,
          lineHeight: 0.85,
          letterSpacing: "-0.04em",
          pointerEvents: "none",
          whiteSpace: "nowrap",
          userSelect: "none",
          zIndex: 0,
        }}>{ghost}</div>
      )}

      <div style={{
        position: "relative", zIndex: 1,
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}>
        {badge && (
          <div style={{
            fontFamily: "JetBrains Mono, monospace",
            fontWeight: 700,
            fontSize: 18,
            color: "#d97757",
            textTransform: "uppercase",
            letterSpacing: "0.22em",
            marginBottom: 28,
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            whiteSpace: "nowrap",
            alignSelf: "flex-start",
          }}>
            <span style={{ color: "#d97757" }}>▶</span>
            {badge}
          </div>
        )}

        <h2 style={{
          fontFamily: "Inter, sans-serif",
          fontWeight: 900,
          fontSize: 112,
          lineHeight: 0.94,
          letterSpacing: "-0.04em",
          margin: 0,
          color: titleColor,
          maxWidth: 940,
        }}>
          {title}
          {accent && <> <Accent size={12}>{accent}</Accent></>}
          {serifAccent && <> <SerifAccent color="#ffb089">{serifAccent}</SerifAccent></>}
        </h2>

        {body && (
          <div style={{
            marginTop: 44,
            fontFamily: "Inter, sans-serif",
            fontSize: 36,
            fontWeight: 400,
            color: bodyColor,
            lineHeight: 1.35,
            letterSpacing: "-0.008em",
            maxWidth: 900,
          }}>{body}</div>
        )}

        {mono && (
          <div style={{
            marginTop: 44,
            background: monoBg,
            border: monoBorder,
            borderRadius: 8,
            padding: "22px 28px",
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 24,
            color: monoColor,
            alignSelf: "flex-start",
            maxWidth: "100%",
          }}>{mono}</div>
        )}
      </div>
    </SlideFrame>
  );
}

window.ContentSlide = ContentSlide;

/* global React, SlideFrame, Accent, SerifAccent, GhostWord */
// CTASlide v3 — supports "dark", "paper", or "hero" bg. Ghost word behind headline for drama.

function CTASlide({ bg = "dark", heroSrc, eyebrow, head1, accent, serifAccent, head2, sub, cta, ghost, index, total }) {
  const isHero = bg === "hero";
  const isDark = bg === "dark";
  const isPaper = bg === "paper";

  const titleColor = isPaper ? "#1a1614" : "#fafaf8";
  const subColor = isPaper ? "#3d3833" : "#fafaf8";
  const subOpacity = isPaper ? 1 : 0.92;
  const ghostColor = isPaper ? "#1a1614" : "#fafaf8";
  const ghostOpacity = isPaper ? 0.05 : 0.07;

  return (
    <SlideFrame bg={bg} heroSrc={heroSrc} index={index} total={total} showNextHint={false}>
      {/* big ghost word in bottom half (skip for hero — image does that job) */}
      {ghost && !isHero && (
        <div style={{
          position: "absolute",
          bottom: -120,
          right: -80,
          fontFamily: "'Instrument Serif', Georgia, serif",
          fontStyle: "italic",
          fontWeight: 400,
          fontSize: 540,
          color: ghostColor,
          opacity: ghostOpacity,
          lineHeight: 0.85,
          letterSpacing: "-0.04em",
          pointerEvents: "none",
          whiteSpace: "nowrap",
          userSelect: "none",
          zIndex: 0,
        }}>{ghost}</div>
      )}

      {isHero && <div style={{ flex: 1 }} />}

      <div style={{
        position: "relative", zIndex: 1,
        flex: isHero ? 0 : 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: isHero ? "flex-end" : "center",
      }}>
        <div style={{
          fontFamily: "JetBrains Mono, monospace",
          fontWeight: 700,
          fontSize: 18,
          color: "#d97757",
          textTransform: "uppercase",
          letterSpacing: "0.22em",
          marginBottom: 24,
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
          fontSize: 108,
          lineHeight: 1.02,
          letterSpacing: "-0.04em",
          margin: 0,
          color: titleColor,
          textShadow: isHero ? "0 4px 24px rgba(0,0,0,0.5)" : undefined,
          maxWidth: 940,
        }}>
          {head1}
          {(accent || serifAccent) && <br/>}
          {accent && <Accent size={12}>{accent}</Accent>}
          {serifAccent && <SerifAccent color={isPaper ? "#d97757" : "#ffb089"}>{serifAccent}</SerifAccent>}
          {head2 && <><br/>{head2}</>}
        </h2>

        {sub && (
          <div style={{
            marginTop: 64,
            fontFamily: "'Instrument Serif', Georgia, serif",
            fontStyle: "italic",
            fontSize: 34,
            color: subColor,
            opacity: subOpacity,
            lineHeight: 1.3,
            maxWidth: 880,
            textShadow: isHero ? "0 2px 12px rgba(0,0,0,0.5)" : undefined,
          }}>{sub}</div>
        )}

        {cta && (
          <div style={{
            marginTop: 48,
            display: "inline-flex",
            alignItems: "center",
            gap: 14,
            background: "#d97757",
            color: "#0a0706",
            padding: "26px 34px",
            borderRadius: 12,
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 28,
            fontWeight: 700,
            letterSpacing: "0.04em",
            alignSelf: "flex-start",
            boxShadow: "0 12px 32px rgba(217,119,87,0.4)",
          }}>
            {cta}
            <span>→</span>
          </div>
        )}
      </div>
    </SlideFrame>
  );
}

window.CTASlide = CTASlide;

/* global React, SlideFrame, SerifAccent */
// HookSlide v3 — full-bleed hero. `anchor` controls where the headline stack sits relative to
// the image's focal point. Options: "bottom-left" (default), "top-left", "top-right",
// "bottom-right", "center-left". Sub text + tag follow the anchor.

function HookSlide({
  heroSrc, tab, head1, accent, head2, sub,
  anchor = "bottom-left",
  index, total,
}) {
  const [vAlign, hAlign] = anchor.split("-"); // "top"/"center"/"bottom", "left"/"right"
  const textAlign = hAlign === "right" ? "right" : "left";
  const alignItems = hAlign === "right" ? "flex-end" : "flex-start";

  const justifyContent =
    vAlign === "top" ? "flex-start" :
    vAlign === "center" ? "center" : "flex-end";

  return (
    <SlideFrame bg="hero" heroSrc={heroSrc} index={index} total={total}>
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent,
        alignItems,
        textAlign,
      }}>
        {tab && (
          <div style={{
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: 96,
            color: "#d97757",
            letterSpacing: "-0.04em",
            lineHeight: 1,
            textShadow: "0 4px 24px rgba(0,0,0,0.4)",
            marginBottom: 8,
          }}>{tab}</div>
        )}

        <h1 style={{
          fontFamily: "Inter, sans-serif",
          fontWeight: 900,
          fontSize: 92,
          lineHeight: 0.98,
          letterSpacing: "-0.035em",
          margin: 0,
          color: "#fafaf8",
          textShadow: "0 4px 24px rgba(0,0,0,0.45)",
        }}>
          {head1 && <>{head1}<br/></>}
          {accent && <><SerifAccent color="#ffb089">{accent}</SerifAccent><br/></>}
          {head2 && <>{head2}</>}
        </h1>

        {sub && (
          <div style={{
            marginTop: 24,
            fontFamily: "'Instrument Serif', Georgia, serif",
            fontStyle: "italic",
            fontSize: 32,
            color: "#fafaf8",
            opacity: 0.92,
            lineHeight: 1.25,
            maxWidth: 820,
            textShadow: "0 2px 12px rgba(0,0,0,0.5)",
          }}>{sub}</div>
        )}
      </div>
    </SlideFrame>
  );
}

window.HookSlide = HookSlide;

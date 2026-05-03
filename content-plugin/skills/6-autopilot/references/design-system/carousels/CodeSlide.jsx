/* global React, SlideFrame, Accent, SerifAccent */
// CodeSlide v4 — supports "dark" or "paper" bg. On paper, the terminal is dark-on-cream
// (inverted, with the same orange border) so it still pops as the hero of the slide.

function CodeSlide({ bg = "dark", eyebrow = "Send this to Claude", head1, accent, serifAccent, head2, code, index, total }) {
  const isDark = bg === "dark";
  const titleColor = isDark ? "#fafaf8" : "#1a1614";

  // Terminal card: dark on BOTH variants (inverted on paper) — that's the look the user likes
  const cardBg = isDark ? "rgba(10,7,6,0.6)" : "#1a1614";
  const cardBorder = "2px solid #d97757";
  const cardShadow = isDark
    ? "0 0 50px rgba(217,119,87,0.18), inset 0 0 80px rgba(217,119,87,0.05)"
    : "0 20px 50px rgba(26,22,20,0.18), 0 0 0 1px rgba(26,22,20,0.04)";

  return (
    <SlideFrame bg={bg} index={index} total={total}>
      <div style={{
        fontFamily: "JetBrains Mono, monospace",
        fontWeight: 700,
        fontSize: 18,
        color: "#d97757",
        textTransform: "uppercase",
        letterSpacing: "0.22em",
        marginBottom: 20,
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        whiteSpace: "nowrap",
        alignSelf: "flex-start",
      }}>
        <span>▶</span>
        {eyebrow}
      </div>

      <h2 style={{
        fontFamily: "Inter, sans-serif",
        fontWeight: 900,
        fontSize: 88,
        lineHeight: 0.98,
        letterSpacing: "-0.035em",
        margin: 0,
        color: titleColor,
        maxWidth: 940,
      }}>
        {head1}
        {accent && <> <Accent size={10}>{accent}</Accent></>}
        {serifAccent && <> <SerifAccent color={isDark ? "#ffb089" : "#d97757"}>{serifAccent}</SerifAccent></>}
        {head2 && <><br/>{head2}</>}
      </h2>

      {/* terminal — flex-fills remaining vertical space; larger type */}
      <div style={{
        marginTop: 36,
        flex: 1,
        minHeight: 0,
        background: cardBg,
        border: cardBorder,
        borderRadius: 20,
        padding: "44px 48px",
        fontFamily: "JetBrains Mono, monospace",
        fontSize: 30,
        lineHeight: 1.5,
        color: "#e8ddc8",
        boxShadow: cardShadow,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}>
        {code.map((line, i) => {
          if (typeof line === "string") {
            return <div key={i} style={{ minHeight: "1.5em" }}>{line || "\u00a0"}</div>;
          }
          return (
            <div key={i} style={{ minHeight: "1.5em" }}>
              {line.parts.map((p, j) => (
                <span key={j} style={{ color: p.c || "#e8ddc8" }}>{p.t}</span>
              ))}
            </div>
          );
        })}
      </div>
    </SlideFrame>
  );
}

window.CodeSlide = CodeSlide;

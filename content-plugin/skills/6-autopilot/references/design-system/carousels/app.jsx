/* global React, ReactDOM, CAROUSEL_1, CAROUSEL_2, renderSlide */

const CAROUSELS = {
  skills: { title: "My top 5 Claude skills", slides: CAROUSEL_1 },
  designer: { title: "Claude replaced my designer", slides: CAROUSEL_2 },
};

const SLIDE_W = 1080, SLIDE_H = 1350;

function useFit() {
  const [scale, setScale] = React.useState(0.5);
  React.useEffect(() => {
    const calc = () => {
      const availW = window.innerWidth - 240; // room for arrows + chrome
      const availH = window.innerHeight - 180;
      const s = Math.min(availW / SLIDE_W, availH / SLIDE_H, 1);
      setScale(s);
    };
    calc();
    window.addEventListener("resize", calc);
    return () => window.removeEventListener("resize", calc);
  }, []);
  return scale;
}

function App() {
  const [carouselKey, setCarouselKey] = React.useState(() => localStorage.getItem("ag_carousel") || "skills");
  const [idx, setIdx] = React.useState(() => parseInt(localStorage.getItem("ag_slide_" + (localStorage.getItem("ag_carousel") || "skills")) || "0", 10));

  const carousel = CAROUSELS[carouselKey];
  const total = carousel.slides.length;
  const scale = useFit();

  React.useEffect(() => { localStorage.setItem("ag_carousel", carouselKey); }, [carouselKey]);
  React.useEffect(() => { localStorage.setItem("ag_slide_" + carouselKey, String(idx)); }, [idx, carouselKey]);

  const go = (d) => setIdx(i => Math.max(0, Math.min(total - 1, i + d)));

  React.useEffect(() => {
    const onKey = (e) => {
      if (e.key === "ArrowRight") go(1);
      if (e.key === "ArrowLeft") go(-1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const switchCarousel = (key) => {
    setCarouselKey(key);
    setIdx(parseInt(localStorage.getItem("ag_slide_" + key) || "0", 10));
  };

  return (
    <div style={{
      width: "100vw", height: "100vh",
      background: "#1a1614",
      display: "flex", flexDirection: "column",
      fontFamily: "Inter, sans-serif",
      color: "#fafaf8",
      overflow: "hidden",
    }}>
      {/* top bar */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "18px 28px",
        borderBottom: "1px solid #2a2522",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 13, letterSpacing: "0.18em",
            color: "#d97757", textTransform: "uppercase", fontWeight: 700,
          }}>@{YOUR_HANDLE_PERSONAL} · carousels</div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {Object.entries(CAROUSELS).map(([key, c]) => (
            <button
              key={key}
              onClick={() => switchCarousel(key)}
              style={{
                fontFamily: "JetBrains Mono, monospace",
                fontSize: 12,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                padding: "10px 16px",
                borderRadius: 6,
                border: "1px solid " + (carouselKey === key ? "#d97757" : "#2a2522"),
                background: carouselKey === key ? "#d97757" : "transparent",
                color: carouselKey === key ? "#1a1614" : "#fafaf8",
                cursor: "pointer",
                fontWeight: 700,
              }}>
              {c.title}
            </button>
          ))}
        </div>
      </div>

      {/* stage */}
      <div style={{
        flex: 1,
        position: "relative",
        display: "flex", alignItems: "center", justifyContent: "center",
      }}>
        {/* prev */}
        <button
          onClick={() => go(-1)}
          disabled={idx === 0}
          style={arrowStyle(idx === 0, "left")}
          aria-label="Previous">‹</button>

        {/* slide */}
        <div style={{
          width: SLIDE_W * scale,
          height: SLIDE_H * scale,
          position: "relative",
        }}>
          <div style={{
            width: SLIDE_W, height: SLIDE_H,
            transform: `scale(${scale})`,
            transformOrigin: "top left",
            position: "absolute",
            top: 0, left: 0,
          }}>
            {renderSlide(carousel.slides[idx], idx, total)}
          </div>
        </div>

        {/* next */}
        <button
          onClick={() => go(1)}
          disabled={idx === total - 1}
          style={arrowStyle(idx === total - 1, "right")}
          aria-label="Next">›</button>
      </div>

      {/* dots */}
      <div style={{
        display: "flex", gap: 8, justifyContent: "center",
        padding: "18px 0 24px",
      }}>
        {carousel.slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setIdx(i)}
            style={{
              width: i === idx ? 28 : 8, height: 8,
              borderRadius: 999,
              background: i === idx ? "#d97757" : "#3a332e",
              border: "none",
              cursor: "pointer",
              transition: "width 0.2s, background 0.2s",
              padding: 0,
            }}
            aria-label={`Go to slide ${i+1}`}/>
        ))}
      </div>
    </div>
  );
}

function arrowStyle(disabled, side) {
  return {
    position: "absolute",
    [side]: 40,
    top: "50%", transform: "translateY(-50%)",
    width: 56, height: 56,
    borderRadius: 999,
    border: "1px solid #2a2522",
    background: disabled ? "#1f1a17" : "#fafaf8",
    color: disabled ? "#3a332e" : "#1a1614",
    fontSize: 32,
    fontFamily: "Inter, sans-serif",
    fontWeight: 400,
    cursor: disabled ? "default" : "pointer",
    lineHeight: 1,
    display: "flex", alignItems: "center", justifyContent: "center",
    paddingBottom: 4,
    opacity: disabled ? 0.4 : 1,
    zIndex: 10,
  };
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);

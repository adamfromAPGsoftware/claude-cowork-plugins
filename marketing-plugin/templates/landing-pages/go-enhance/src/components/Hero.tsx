import { useEffect, useRef } from "react";
import { ArrowRight, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuiz } from "@/contexts/QuizContext";
import { track } from "@/lib/analytics";

declare global {
  interface Window {
    Stream: (iframe: HTMLIFrameElement) => {
      addEventListener: (event: string, callback: () => void) => void;
      currentTime: number;
      duration: number;
    };
    gtag: (...args: unknown[]) => void;
  }
}

const Hero = () => {
  const { openQuiz } = useQuiz();
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const milestonesHit = useRef(new Set<number>());

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe || !window.Stream) return;

    const player = window.Stream(iframe);
    const milestones = [25, 50, 75, 100];

    player.addEventListener("play", () => {
      window.gtag?.("event", "video_start", {
        event_category: "VSL",
        event_label: "Homepage VSL",
      });
    });

    player.addEventListener("timeupdate", () => {
      if (!player.duration) return;
      const percent = Math.round((player.currentTime / player.duration) * 100);

      for (const milestone of milestones) {
        if (percent >= milestone && !milestonesHit.current.has(milestone)) {
          milestonesHit.current.add(milestone);
          window.gtag?.("event", "video_progress", {
            event_category: "VSL",
            event_label: "Homepage VSL",
            video_percent: milestone,
          });
        }
      }
    });

    player.addEventListener("ended", () => {
      window.gtag?.("event", "video_complete", {
        event_category: "VSL",
        event_label: "Homepage VSL",
      });
    });
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-hero">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-primary/5 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-primary/5 to-transparent rounded-full blur-2xl" />
      </div>

      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px]" />

      <div className="container relative z-10 px-4 py-20">
        <div className="max-w-5xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-full bg-secondary/50 border border-border/50 mb-8 animate-fade-in">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse flex-shrink-0" />
            <span className="text-sm text-muted-foreground text-center">
              ATTENTION AGENCY FOUNDERS & PMs DROWNING IN <span className="text-primary/70 font-medium">MANUAL SCOPING</span>
            </span>
          </div>

          {/* Headline */}
          <h1 className="text-3xl md:text-5xl lg:text-6xl xl:text-7xl font-extrabold leading-tight mb-6 animate-slide-up">
            Drop Your Scoping Process From{" "}
            <span className="text-gradient">Months to Days</span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-4 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <span className="text-gradient font-semibold">Saves 180+ hours</span> per engagement with{" "}
            <span className="text-gradient font-semibold">90% faster scoping</span>
          </p>

          <p className="text-lg text-muted-foreground mb-10 animate-slide-up" style={{ animationDelay: '0.15s' }}>
            Or we'll refund every cent. No questions asked.
          </p>

          {/* Video Player - Cloudflare Stream */}
          <div id="vsl" className="relative max-w-4xl mx-auto animate-slide-up scroll-mt-24 mb-10" style={{ animationDelay: '0.2s' }}>
            <div className="aspect-video rounded-2xl overflow-hidden glass-card shadow-elevated">
              <iframe
                ref={iframeRef}
                src="https://customer-96dey70a994gv78z.cloudflarestream.com/1e487ffc3987f5e09d3beba62ff99924/iframe?poster=https%3A%2F%2Fcustomer-96dey70a994gv78z.cloudflarestream.com%2F1e487ffc3987f5e09d3beba62ff99924%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600&primaryColor=%239ae660"
                loading="lazy"
                className="w-full h-full border-0"
                allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
                allowFullScreen
              />
            </div>
            {/* Decorative glow under video */}
            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 w-3/4 h-16 bg-primary/20 blur-3xl rounded-full" />
          </div>

          {/* CTA Buttons - Below Video */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 mt-12 sm:mt-16 px-4 animate-slide-up" style={{ animationDelay: '0.4s' }}>
            <Button variant="hero" size="lg" className="group h-12 sm:h-14 md:h-16 w-full sm:w-auto text-sm sm:text-base" onClick={() => { track.ctaClick("hero"); openQuiz(); }}>
              See If You Qualify
              <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="heroOutline" size="lg" className="group h-12 sm:h-14 md:h-16 w-full sm:w-auto text-sm sm:text-base" asChild>
              <a href="#calculator">
                <Play className="w-4 h-4 sm:w-5 sm:h-5" />
                Calculate My Savings
              </a>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

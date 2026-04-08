import { ArrowRight, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuiz } from "@/contexts/QuizContext";
import { track } from "@/lib/analytics";

const CTA = () => {
  const { openQuiz } = useQuiz();
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-primary/5 to-background" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl" />
      </div>

      <div className="container px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Icon */}
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/20 mb-8 animate-glow-pulse">
            <Zap className="w-8 h-8 text-primary" />
          </div>

          {/* Headline */}
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            Ready to Transform Your{" "}
            <span className="text-gradient">Scoping Process</span>?
          </h2>

          {/* Subheadline */}
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Take the 60-second qualification quiz and see if the AI Scoping Engine is right for your agency.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button variant="hero" size="xl" className="group" onClick={() => { track.ctaClick("footer"); openQuiz(); }}>
              See If You Qualify
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>

          {/* Trust indicator */}
          <p className="mt-8 text-sm text-muted-foreground">
            Built by <span className="text-primary font-semibold">APG Software</span> — the agency that runs 5 client discoveries a month on this system
          </p>
        </div>
      </div>
    </section>
  );
};

export default CTA;

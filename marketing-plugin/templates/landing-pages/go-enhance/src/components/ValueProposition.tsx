import { Clock, Layers, Link, Shield, Zap } from "lucide-react";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuiz } from "@/contexts/QuizContext";
import { track } from "@/lib/analytics";

const benefits = [
  {
    icon: Clock,
    title: "90% Less Scoping Time",
    description: "200 hours of manual discovery compressed to 20. Four AI agents handle extraction, analysis, documentation, and prototype generation."
  },
  {
    icon: Layers,
    title: "Auto-Generated Deliverables",
    description: "Meeting transcripts become process maps, findings reports, strategic approaches, and clickable prototypes."
  },
  {
    icon: Link,
    title: "Fathom.ai Connected",
    description: "Auto-pulls your meeting transcripts. Zero manual upload, zero lost insights between sessions."
  },
  {
    icon: Shield,
    title: "Scope Accuracy That Prevents Blowouts",
    description: "Structured extraction with citation-backed confidence scores means fewer errors in your build phase."
  },
  {
    icon: Zap,
    title: "One-Click Install",
    description: "Up and running via Claude Code or Cowork in minutes. No infrastructure to manage."
  }
];

const ValueProposition = () => {
  const { openQuiz } = useQuiz();

  return (
    <section id="benefits" className="py-24 relative overflow-hidden">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              <span className="text-gradient">5 Reasons</span> Agency Teams Are{" "}
              <span className="whitespace-nowrap">Switching to <span className="text-gradient">AI Scoping</span></span>
            </h2>
            <p className="text-xl text-muted-foreground">
              Stop losing billable hours to manual discovery work
            </p>
          </div>

          {/* Benefits list */}
          <div className="space-y-6 mb-12">
            {benefits.map((benefit, index) => (
              <div
                key={index}
                className="glass-card p-6 md:p-8 hover:border-primary/50 transition-all duration-300 group"
              >
                <div className="flex gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center group-hover:bg-primary/30 transition-colors">
                      <benefit.icon className="w-5 h-5 text-primary" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-lg md:text-xl font-bold mb-2 text-foreground">
                      {benefit.title}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {benefit.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Quote highlight */}
          <div className="glass-card p-8 text-center mb-12 border-primary/30">
            <p className="text-lg md:text-xl italic text-muted-foreground mb-2">
              *Most agency founders walk away from the demo saying:
            </p>
            <p className="text-base md:text-lg lg:text-xl font-semibold text-foreground lg:whitespace-nowrap">
              "I didn't realise how much time we were losing to manual scoping."
            </p>
          </div>

          {/* CTA */}
          <div className="text-center px-4">
            <Button variant="hero" size="xl" className="group w-auto max-w-full" onClick={() => { track.ctaClick("mid_page"); openQuiz(); }}>
              See If You Qualify
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ValueProposition;

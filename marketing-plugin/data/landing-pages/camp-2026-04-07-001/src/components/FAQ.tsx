import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "What exactly is the AI Scoping Engine?",
    answer: "It's a system of 4 specialised AI agents: Process Mapper extracts structured data from meeting transcripts, Process Analyst researches solutions and calculates ROI, Generator builds deliverables (process maps, portals, reports), and Solution Architect creates clickable prototypes. It installs in one click via Claude Code or Cowork."
  },
  {
    question: "How does it connect to my meetings?",
    answer: "It integrates directly with Fathom.ai to auto-pull meeting transcripts. You can also upload transcripts manually from any meeting tool."
  },
  {
    question: "What deliverables does it generate?",
    answer: "Process maps with waste heatmaps, client-facing portals, findings reports, strategic approaches with tool recommendations, transformation blueprints, priority matrices, and clickable prototypes."
  },
  {
    question: "How long does it take to set up?",
    answer: "The self-install option takes about an hour with a scoping call from our founder. The done-for-you option is fully configured by our team."
  },
  {
    question: "What if it doesn't work for my agency?",
    answer: "We're confident it will — our own agency runs 5 client engagements a month on this system. We offer a satisfaction guarantee and the scoping call ensures it's configured for your needs."
  },
  {
    question: "Can I try it before committing?",
    answer: "Yes — we offer an interactive demo so you can see actual output. Take the qualification quiz and we'll walk you through a live demo on the call."
  }
];

const FAQ = () => {
  return (
    <section id="faq" className="py-24 relative overflow-hidden">
      <div className="container px-4">
        <div className="max-w-3xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
              FAQ
            </span>
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-lg text-muted-foreground">
              Everything you need to know about the AI Scoping Engine
            </p>
          </div>

          {/* FAQ Accordion */}
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="glass-card px-6 border-border/50 data-[state=open]:border-primary/50 transition-colors"
              >
                <AccordionTrigger className="text-left text-lg font-semibold hover:text-primary transition-colors py-6">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground leading-relaxed pb-6">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
};

export default FAQ;

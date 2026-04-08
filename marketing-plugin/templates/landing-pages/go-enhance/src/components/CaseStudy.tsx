import { FileSpreadsheet, LayoutGrid, MapPin, TrendingUp, Users, DollarSign } from "lucide-react";

const CaseStudy = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="container px-4">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Case Study
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            What Happens When You Inject a System Behind a Team
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-2">
            <a
              href="https://flawlessgardens.com.au/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary font-semibold hover:underline"
            >
              Flawless Gardens & Landscaping
            </a>{" "}
            — Sydney's Northern Beaches
          </p>
          <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
            We audited their entire operation and found they were running everything through Excel, phone calls, and Outlook — no CRM, no system for tracking leads or follow-up times, and zero visibility over their pipeline. Here's what changed.
          </p>
        </div>

        <div className="max-w-5xl mx-auto">
          <div className="glass-card border border-border/50 overflow-hidden">
            {/* Hero image */}
            <div className="relative">
              <img
                src="https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/flawless%20gardens%20image.png"
                alt="Flawless Gardens & Landscaping team at work"
                className="w-full h-64 md:h-80 object-cover"
              />
              <div className="absolute bottom-4 left-4 glass-card px-4 py-2 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-sm">
                  HM
                </div>
                <div>
                  <p className="text-sm font-bold text-foreground">Hamish M</p>
                  <p className="text-xs text-muted-foreground">Operations Manager & Head of Landscaping</p>
                </div>
              </div>
            </div>

            {/* Before / After split */}
            <div className="grid md:grid-cols-2">
              {/* Before */}
              <div className="p-8 border-b md:border-b-0 md:border-r border-border/50">
                <p className="text-xs font-bold uppercase tracking-wider text-red-400 mb-4">July 2025 — Before</p>
                <p className="text-4xl font-bold text-foreground mb-1">
                  $200K<span className="text-lg text-muted-foreground font-semibold">/year</span>
                </p>
                <p className="text-sm text-muted-foreground mb-6">70 maintenance contracts</p>

                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <FileSpreadsheet className="w-5 h-5 text-muted-foreground mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground">Excel spreadsheets — <strong className="text-foreground">no modern CRM</strong></p>
                  </div>
                  <div className="flex items-start gap-3">
                    <LayoutGrid className="w-5 h-5 text-muted-foreground mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground"><strong className="text-foreground">No business system</strong> — phone, Outlook, and memory</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 text-muted-foreground mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground">All IP lived <strong className="text-foreground">in the owner's head</strong></p>
                  </div>
                </div>
              </div>

              {/* After */}
              <div className="p-8">
                <p className="text-xs font-bold uppercase tracking-wider text-primary mb-4">March 2026 — After</p>
                <p className="text-4xl font-bold text-gradient mb-1">
                  $2M<span className="text-lg text-muted-foreground font-semibold">/year</span>
                </p>
                <p className="text-sm text-muted-foreground mb-6">$200K/month run-rate</p>

                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <TrendingUp className="w-5 h-5 text-primary mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground"><strong className="text-primary">10x revenue growth</strong> in 9 months</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Users className="w-5 h-5 text-primary mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground"><strong className="text-foreground">Centralised system</strong> with full visibility</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <DollarSign className="w-5 h-5 text-primary mt-0.5 shrink-0" />
                    <p className="text-sm text-muted-foreground"><strong className="text-foreground">Scalable operations</strong> replacing manual processes</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CaseStudy;

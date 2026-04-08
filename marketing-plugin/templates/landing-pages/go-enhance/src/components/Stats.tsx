import { Clock, TrendingDown, Users, Bot } from "lucide-react";

const stats = [
  {
    icon: Clock,
    value: "200 → 20",
    label: "Hours of Scoping Reduced",
    description: "Per client engagement, from manual discovery to AI-assisted extraction"
  },
  {
    icon: TrendingDown,
    value: "90%",
    label: "Reduction in Discovery Time",
    description: "Four AI agents handle extraction, analysis, documentation, and prototyping"
  },
  {
    icon: Users,
    value: "5",
    label: "Concurrent Client Engagements",
    description: "Run multiple discoveries simultaneously without hiring additional PMs"
  },
  {
    icon: Bot,
    value: "4",
    label: "Specialised AI Agents",
    description: "Process Mapper, Process Analyst, Generator, and Solution Architect"
  }
];

const Stats = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-secondary/20 to-background" />

      <div className="container px-4 relative z-10">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Proven Results
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Transform Your Scoping Process
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            The same system our agency uses to run 5 client discoveries simultaneously
          </p>
        </div>

        {/* Stats grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {stats.map((stat, index) => (
            <div
              key={index}
              className="glass-card p-8 text-center group border border-primary/40 shadow-[0_0_25px_rgba(154,230,96,0.12)] hover:shadow-[0_0_35px_rgba(154,230,96,0.25)] transition-all duration-300"
            >
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary/10 mb-6 group-hover:bg-primary/20 transition-colors">
                <stat.icon className="w-7 h-7 text-primary" />
              </div>
              <p className="text-4xl md:text-5xl font-bold text-gradient mb-2">
                {stat.value}
              </p>
              <p className="font-semibold text-foreground mb-2">
                {stat.label}
              </p>
              <p className="text-sm text-muted-foreground">
                {stat.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Stats;

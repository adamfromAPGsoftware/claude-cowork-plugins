
const projects = [
  {
    name: "Process Maps",
    description: "Colour-coded waste heatmaps generated from meeting transcripts",
    tags: ["AI", "Extraction"],
    result: "Auto-generated from transcripts",
    image: "/aeon.png"
  },
  {
    name: "Client Portal",
    description: "Progressive-unlock portal with findings, solutions, and strategies",
    tags: ["Portal", "Deliverable"],
    result: "Live client-facing dashboard",
    image: "/connectedai.png"
  },
  {
    name: "Clickable Prototype",
    description: "Interactive prototype built from extracted requirements",
    tags: ["Prototype", "Design"],
    result: "Closes deals faster than decks",
    image: "/scriptioai.png"
  },
  {
    name: "Strategic Analysis",
    description: "Multi-strategy comparison with ROI projections",
    tags: ["Analysis", "ROI"],
    result: "Data-driven recommendations",
    image: "/aeon.png"
  }
];

const Portfolio = () => {
  return (
    <section id="portfolio" className="py-24 bg-gradient-hero relative overflow-hidden">
      {/* Background accent */}
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />

      <div className="container px-4">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            See It In Action
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            See the AI Scoping Engine in Action
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Real deliverables from real client engagements
          </p>
        </div>

        {/* Portfolio grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {projects.map((project, index) => (
            <div
              key={index}
              className="group glass-card p-4 border border-primary/50 shadow-[0_0_30px_rgba(154,230,96,0.2)] hover:shadow-[0_0_40px_rgba(154,230,96,0.35)] transition-all duration-300"
            >
              {/* Project image */}
              <div className="w-full aspect-video rounded-xl overflow-hidden mb-4 bg-white">
                <img
                  src={project.image}
                  alt={project.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Project header */}
              <h3 className="text-xl font-bold text-foreground mb-2">
                {project.name}
              </h3>

              {/* Description */}
              <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
                {project.description}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                {project.tags.map((tag, tagIndex) => (
                  <span
                    key={tagIndex}
                    className="px-3 py-1 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Result */}
              <p className="text-base font-semibold text-gradient">
                {project.result}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Portfolio;

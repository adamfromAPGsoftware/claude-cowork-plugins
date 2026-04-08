import { ExternalLink, Star, CheckCircle } from "lucide-react";

const proofPanels = [
  {
    title: "Upwork Profile",
    stat: "60+ projects \u00b7 100% Job Success \u00b7 Expert-Vetted",
    linkText: "View on Upwork",
    url: "https://www.upwork.com/freelancers/adamgoodyer",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Adam%20Upwork%20Screenshot.png"
  },
  {
    title: "YouTube Channel",
    stat: "6,000+ subscribers \u00b7 100+ videos \u00b7 200,000+ views",
    linkText: "View on YouTube",
    url: "https://www.youtube.com/@AdamGoodyer",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Adam%20Goodyer%20Youtube%20Channel%20Screenshot.png"
  },
  {
    title: "AI Builders Hub",
    stat: "400+ members \u00b7 Skool community",
    linkText: "View on Skool",
    url: "https://www.skool.com/ai-builders-hub",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Skool%20Screenshot.png"
  },
  {
    title: "Client Reviews",
    stat: "60+ third-party verified reviews",
    linkText: "View reviews",
    url: "https://www.upwork.com/freelancers/adamgoodyer",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/upwork_reviews_collage.png"
  }
];

const speakingEvents = [
  {
    title: "Africa AI Summit \u2014 Cape Town",
    subtitle: "n8n sponsored event \u00b7 Combined audience 3.5M+",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Adam%20Africa%20AI.JPEG",
    links: []
  },
  {
    title: "AAA AI Event \u2014 Sydney",
    subtitle: "Australia\u2019s leading AI community event",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Adam%20Sydney%20AAA%20Event.png",
    links: []
  },
  {
    title: "Podcast & Media",
    subtitle: "Featured on n8n, Liam Ottley (800K+), and more",
    image: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Adam%20Portugal%20Pod.png",
    links: [
      { label: "n8n", url: "https://www.youtube.com/watch?v=OrV7SZrxufk&t=327s" },
      { label: "Liam Ottley", url: "https://www.youtube.com/watch?v=IyrSfHizvWc&t=159s" }
    ]
  }
];

const SocialProof = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      <div className="container px-4">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Proof
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            See for Yourself
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Seven years of results. Verified everywhere.
          </p>
        </div>

        {/* Proof panels grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto mb-16">
          {proofPanels.map((panel, index) => (
            <a
              key={index}
              href={panel.url}
              target="_blank"
              rel="noopener noreferrer"
              className="glass-card border border-border/50 hover:border-primary/40 transition-all duration-300 shadow-[0_0_20px_rgba(255,255,255,0.08)] hover:shadow-[0_0_30px_rgba(154,230,96,0.2)] overflow-hidden group"
            >
              <div className="aspect-video overflow-hidden">
                <img
                  src={panel.image}
                  alt={panel.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-4">
                <p className="font-bold text-foreground text-sm mb-1">{panel.title}</p>
                <p className="text-xs text-muted-foreground mb-2">{panel.stat}</p>
                <p className="text-xs text-primary font-medium flex items-center gap-1">
                  <ExternalLink className="w-3 h-3" />
                  {panel.linkText}
                </p>
              </div>
            </a>
          ))}
        </div>

        {/* Speaking & Recognition */}
        <div className="max-w-5xl mx-auto mb-16">
          <h3 className="text-xl font-bold text-center mb-8">Speaking & Recognition</h3>
          <div className="grid md:grid-cols-3 gap-6">
            {speakingEvents.map((event, index) => (
              <div
                key={index}
                className="glass-card border border-border/50 overflow-hidden hover:border-primary/30 transition-all duration-300"
              >
                <div className="aspect-video overflow-hidden">
                  <img
                    src={event.image}
                    alt={event.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-4">
                  <p className="font-bold text-foreground text-sm mb-1">{event.title}</p>
                  <p className="text-xs text-muted-foreground mb-2">{event.subtitle}</p>
                  {event.links.length > 0 && (
                    <div className="flex gap-3">
                      {event.links.map((link, linkIndex) => (
                        <a
                          key={linkIndex}
                          href={link.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-primary font-medium flex items-center gap-1 hover:underline"
                        >
                          <ExternalLink className="w-3 h-3" />
                          {link.label}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Trust strip */}
        <div className="flex flex-wrap items-center justify-center gap-4 md:gap-8 text-sm text-muted-foreground max-w-3xl mx-auto">
          <a
            href="https://www.upwork.com/freelancers/adamgoodyer"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-primary transition-colors"
          >
            <Star className="w-4 h-4 fill-primary text-primary" />
            <span className="font-semibold text-foreground">60+ verified reviews</span>
          </a>
          <span className="text-border hidden md:inline">&bull;</span>
          <span className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-primary" />
            <span className="font-semibold text-foreground">300+ projects completed</span>
          </span>
          <span className="text-border hidden md:inline">&bull;</span>
          <a
            href="https://www.trustpilot.com/review/apgsoftware.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-primary transition-colors"
          >
            <Star className="w-4 h-4 fill-[#00B67A] text-[#00B67A]" />
            <span className="font-semibold text-foreground">Rated Excellent on Trustpilot</span>
          </a>
        </div>
      </div>
    </section>
  );
};

export default SocialProof;

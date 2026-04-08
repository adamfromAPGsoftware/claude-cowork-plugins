import { Star, Linkedin } from "lucide-react";

const testimonials = [
  {
    quoteBefore: "\"Adam genuinely understands the tech, the business side, and how to connect the two. He built our entire platform from vision to MVP — ",
    quoteHighlight: "on time, under budget, and exactly how we imagined it",
    quoteAfter: ". If you need someone who actually delivers, this is the guy.\"",
    name: "Gavin Tye",
    role: "Founder, DealBuddi",
    avatar: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Gavin%20Tye.jpeg",
    linkedin: "https://au.linkedin.com/in/gavintye",
    hasVideo: true,
    videoUrl: "https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Gavin%20Tye%20Testimonial%20Video.mp4"
  },
  {
    quoteBefore: "\"Adam delivered outstanding work on our project. His communication was clear and timely, making collaboration seamless. He adhered to all specifications meticulously, ensuring the project met our exact requirements. ",
    quoteHighlight: "His creative problem-solving skills were exceptional",
    quoteAfter: ", allowing us to overcome unexpected challenges efficiently.\"",
    name: "CampaignCompassAI",
    role: "Application Development — Upwork",
    avatar: null,
    linkedin: null,
    hasVideo: false,
    videoUrl: null
  },
  {
    quoteBefore: "\"Adam built a prototype of a CRM style app in Bubble for us (very quickly) and it turned out really well. He was ",
    quoteHighlight: "extremely knowledgeable and easy to work with",
    quoteAfter: ". He was also very thorough in terms of walking through the design and the finished prototype.\"",
    name: "App Design Client",
    role: "App Design & Development — Upwork",
    avatar: null,
    linkedin: null,
    hasVideo: false,
    videoUrl: null
  }
];

const Testimonials = () => {
  return (
    <section id="testimonials" className="py-24 bg-gradient-hero relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />

      <div className="container px-4">
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Testimonials
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Built by an Agency, for Agencies
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Real reviews from real clients — verified on Upwork and LinkedIn
          </p>
        </div>

        {/* Video testimonial — featured */}
        {testimonials.filter(t => t.hasVideo).map((testimonial, index) => (
          <div key={`video-${index}`} className="max-w-4xl mx-auto mb-16">
            <div className="glass-card border border-primary/40 shadow-[0_0_30px_rgba(154,230,96,0.15)] overflow-hidden">
              <div className="grid md:grid-cols-2 gap-0">
                <div className="aspect-video md:aspect-auto">
                  <video
                    controls
                    preload="metadata"
                    className="w-full h-full object-cover"
                    poster={testimonial.avatar || undefined}
                  >
                    <source src={testimonial.videoUrl!} type="video/mp4" />
                  </video>
                </div>
                <div className="p-8 flex flex-col justify-center">
                  <div className="flex gap-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                    ))}
                  </div>
                  <p className="text-foreground/70 text-sm leading-relaxed mb-6 italic">
                    {testimonial.quoteBefore}
                    <span className="text-primary font-semibold not-italic">{testimonial.quoteHighlight}</span>
                    {testimonial.quoteAfter}
                  </p>
                  <div className="flex items-center gap-3">
                    {testimonial.avatar && (
                      <img
                        src={testimonial.avatar}
                        alt={testimonial.name}
                        className="w-10 h-10 rounded-full object-cover border border-border"
                      />
                    )}
                    <div className="flex-1">
                      <p className="font-bold text-foreground flex items-center gap-2">
                        {testimonial.name}
                        {testimonial.linkedin && (
                          <a href={testimonial.linkedin} target="_blank" rel="noopener noreferrer" className="text-[#0A66C2] hover:opacity-80">
                            <Linkedin className="w-4 h-4" />
                          </a>
                        )}
                      </p>
                      <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Written testimonials */}
        <div className="grid md:grid-cols-2 gap-10 max-w-4xl mx-auto justify-items-center">
          {testimonials.filter(t => !t.hasVideo).map((testimonial, index) => (
            <div
              key={index}
              className="glass-card p-6 border border-primary/40 shadow-[0_0_25px_rgba(154,230,96,0.12)] w-full"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex gap-1 justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                ))}
              </div>
              <p className="text-foreground/70 text-sm leading-relaxed mb-6 italic text-left px-2">
                {testimonial.quoteBefore}
                <span className="text-primary font-semibold not-italic">{testimonial.quoteHighlight}</span>
                {testimonial.quoteAfter}
              </p>
              <p className="font-bold text-foreground text-center">{testimonial.name}</p>
              <p className="text-sm text-muted-foreground text-center">{testimonial.role}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;

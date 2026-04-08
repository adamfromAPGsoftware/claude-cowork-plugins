import { Star } from "lucide-react";

const testimonials = [
  {
    quoteBefore: "\"Our agency has run 5 client scoping engagements this month using this exact system. ",
    quoteHighlight: "What used to take weeks now takes days",
    quoteAfter: ".\"",
    name: "Adam Goodyer",
    role: "Founder, APG Software"
  },
  {
    quoteBefore: "\"200 hours of manual discovery work compressed to 20. ",
    quoteHighlight: "The prototypes it generates close deals faster than any proposal deck",
    quoteAfter: ".\"",
    name: "APG Internal",
    role: "Agency Operations"
  },
  {
    quoteBefore: "\"The system caught requirements our senior PM missed. ",
    quoteHighlight: "That alone saved us from a $60K scope creep incident",
    quoteAfter: ".\"",
    name: "APG Internal",
    role: "Project Delivery"
  }
];

const Testimonials = () => {
  return (
    <section id="testimonials" className="py-24 bg-gradient-hero relative overflow-hidden">
      {/* Background accent */}
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />

      <div className="container px-4">
        {/* Section header */}
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Testimonials
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            Built by an Agency, for Agencies
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            This isn't theory — it's the system we use every day to run our own client engagements
          </p>
        </div>

        {/* Testimonial cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10 max-w-7xl mx-auto justify-items-center">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="glass-card p-6 border border-primary/40 shadow-[0_0_25px_rgba(154,230,96,0.12)] w-full max-w-[380px]"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* 5 Stars */}
              <div className="flex gap-1 justify-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                ))}
              </div>

              {/* Quote with highlighted text */}
              <p className="text-foreground/70 text-sm leading-relaxed mb-6 italic text-left px-2">
                {testimonial.quoteBefore}
                <span className="text-primary font-semibold not-italic">{testimonial.quoteHighlight}</span>
                {testimonial.quoteAfter}
              </p>

              {/* Name and role */}
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

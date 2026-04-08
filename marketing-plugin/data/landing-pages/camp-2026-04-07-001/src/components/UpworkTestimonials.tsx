const testimonialImages = [
  "/upwork/Screenshot_1.png",
  "/upwork/Screenshot_2.png",
  "/upwork/Screenshot_3.png",
  "/upwork/Screenshot_4.png",
  "/upwork/Screenshot_5.png",
  "/upwork/Screenshot_6.png",
  "/upwork/Screenshot_7.png",
  "/upwork/Screenshot_8.png",
  "/upwork/Screenshot_9.png",
  "/upwork/Screenshot_10.png",
];

const UpworkTestimonials = () => {
  return (
    <section className="pt-8 sm:pt-16 pb-24 relative overflow-hidden">
      <div className="container px-4">
        {/* Section header */}
        <div className="text-center mb-16 max-w-4xl mx-auto">
          <h2 className="text-xl md:text-2xl lg:text-3xl font-bold leading-tight">
            APG Software Solutions is a <span className="text-gradient">leading Upwork specialist</span> with <span className="text-gradient">300+ completed projects</span> and a perfect success rate
          </h2>
        </div>

        {/* Testimonials grid */}
        <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto items-stretch">
          {testimonialImages.map((image, index) => (
            <div
              key={index}
              className="rounded-xl overflow-hidden border border-border/50 hover:border-primary/30 transition-all duration-300 shadow-[0_0_40px_rgba(255,255,255,0.25)] hover:shadow-[0_0_50px_rgba(154,230,96,0.35)] bg-white"
            >
              <img
                src={image}
                alt={`Upwork testimonial ${index + 1}`}
                className="w-full h-auto"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default UpworkTestimonials;

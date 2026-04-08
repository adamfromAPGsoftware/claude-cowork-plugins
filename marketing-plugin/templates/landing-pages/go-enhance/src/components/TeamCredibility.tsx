import { Youtube, Linkedin, Star, ExternalLink } from "lucide-react";

const TeamCredibility = () => {
  return (
    <section className="py-24 bg-gradient-hero relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />

      <div className="container px-4">
        <div className="text-center mb-16">
          <span className="inline-block text-primary font-semibold text-sm tracking-wider uppercase mb-4">
            Who you're working with
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            A Team You Won't Find at Another Tech Agency
          </h2>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            One founder has presented to audiences of over five million and educates hundreds of thousands through a dedicated research & education branch. The other was CTO scaling systems for some of Australia and America's fastest-growing companies. Combined: <span className="text-primary font-semibold">300+ projects</span> across every major platform.
          </p>
        </div>

        <div className="max-w-5xl mx-auto space-y-12">
          {/* Adam */}
          <div className="glass-card border border-border/50 p-8 md:p-10">
            <div className="grid md:grid-cols-[200px_1fr] gap-8">
              <div className="flex flex-col items-center text-center">
                <img
                  src="https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/adam.png"
                  alt="Adam — Founder, APG Software"
                  className="w-32 h-32 rounded-2xl object-cover border border-border mb-4"
                />
                <p className="font-bold text-lg text-foreground">Adam</p>
                <p className="text-sm text-muted-foreground mb-4">Founder, APG Software</p>

                <div className="flex gap-2 flex-wrap justify-center">
                  <a href="https://www.youtube.com/@AdamGoodyer" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors">
                    <Youtube className="w-3.5 h-3.5" />
                    YouTube
                  </a>
                  <a href="https://www.upwork.com/freelancers/adamgoodyer" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors">
                    <Star className="w-3.5 h-3.5" />
                    Upwork
                  </a>
                  <a href="https://www.linkedin.com/in/adam-goodyer/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors">
                    <Linkedin className="w-3.5 h-3.5" />
                    LinkedIn
                  </a>
                </div>

                <div className="flex gap-2 mt-3 flex-wrap justify-center">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    <Star className="w-3 h-3 fill-primary" />
                    100+ projects
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    <Star className="w-3 h-3 fill-primary" />
                    60+ reviews
                  </span>
                </div>
              </div>

              <div>
                <p className="text-xs font-bold text-foreground uppercase tracking-wider mb-3">Speaking & Recognition</p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex gap-2">
                    <span className="text-primary mt-1 shrink-0">&bull;</span>
                    <span>Presented at the <strong className="text-foreground">Africa AI Summit</strong> in Cape Town — n8n sponsored event with a combined audience of 3.5M+, presenting on this exact audit methodology</span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-primary mt-1 shrink-0">&bull;</span>
                    <span>Speaker at the <strong className="text-foreground">AAA AI Event</strong> in Sydney, Australia</span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-primary mt-1 shrink-0">&bull;</span>
                    <span>
                      Appeared on <strong className="text-foreground">n8n's official channel</strong>, <strong className="text-foreground">Liam Ottley's channel</strong> (800K+ subscribers), and various other leading AI podcasts — widely recognised as an expert in the space
                    </span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-primary mt-1 shrink-0">&bull;</span>
                    <span><strong className="text-foreground">Top 1% on Upwork</strong> — Expert-Vetted in the world's largest freelancing marketplace</span>
                  </li>
                </ul>

                <div className="flex gap-3 mt-4">
                  <a href="https://www.youtube.com/watch?v=OrV7SZrxufk&t=327s" target="_blank" rel="noopener noreferrer" className="text-xs text-primary font-medium flex items-center gap-1 hover:underline">
                    <ExternalLink className="w-3 h-3" /> n8n appearance
                  </a>
                  <a href="https://www.youtube.com/watch?v=IyrSfHizvWc&t=159s" target="_blank" rel="noopener noreferrer" className="text-xs text-primary font-medium flex items-center gap-1 hover:underline">
                    <ExternalLink className="w-3 h-3" /> Liam Ottley
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Patrick */}
          <div className="glass-card border border-border/50 p-8 md:p-10">
            <div className="grid md:grid-cols-[200px_1fr] gap-8">
              <div className="flex flex-col items-center text-center">
                <img
                  src="https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/Pat%20Headshot.avif"
                  alt="Patrick — Co-Founder, APG Software"
                  className="w-32 h-32 rounded-2xl object-cover border border-border mb-4"
                />
                <p className="font-bold text-lg text-foreground">Patrick</p>
                <p className="text-sm text-muted-foreground mb-4">Co-Founder, APG Software</p>

                <div className="flex gap-2 flex-wrap justify-center">
                  <a href="https://www.linkedin.com/in/patrick-goodyer/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors">
                    <Linkedin className="w-3.5 h-3.5" />
                    LinkedIn
                  </a>
                </div>

                <div className="flex gap-2 mt-3 flex-wrap justify-center">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    <Star className="w-3 h-3 fill-primary" />
                    200+ projects
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    Make.com
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    Monday.com
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    HubSpot
                  </span>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full bg-primary/10 text-primary border border-primary/20">
                    Former CTO
                  </span>
                </div>
              </div>

              <div>
                <div className="text-sm text-muted-foreground space-y-3 leading-relaxed">
                  <p>
                    <strong className="text-foreground">200+ projects</strong> in process automation and CRM optimisation across Salesforce, HubSpot, PipeDrive, and every major platform. A registered <strong className="text-foreground">Make.com</strong>, <strong className="text-foreground">Monday.com</strong>, and <strong className="text-foreground">HubSpot</strong> integration partner — Patrick doesn't just know these tools, he's certified to build on them.
                  </p>
                  <p>
                    Before APG, Patrick was <strong className="text-foreground">CTO at Pittsburgh's fastest-growing solar company</strong>, where he built the systems that powered that growth from the ground up. He went on to build operational systems for <strong className="text-foreground">one of Australia's biggest TV shows</strong> and <strong className="text-foreground">one of Australia's biggest solar companies</strong> out of Byron Bay — bringing deep, real-world experience in scaling the exact kind of operations we audit.
                  </p>
                </div>

                <div className="mt-6 rounded-xl overflow-hidden border border-border/50">
                  <img
                    src="https://pub-66c549f8c8d44c16ab441b6668d7a12a.r2.dev/pat_upwork_profile_.jpeg"
                    alt="Patrick's Upwork profile — 200+ projects, top-rated freelancer"
                    className="w-full h-auto"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TeamCredibility;

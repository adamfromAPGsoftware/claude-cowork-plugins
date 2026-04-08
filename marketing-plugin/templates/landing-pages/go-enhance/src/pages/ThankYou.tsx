import { useEffect } from "react";
import { CheckCircle, Calendar, Clock, ArrowRight, Youtube } from "lucide-react";
import { Button } from "@/components/ui/button";

const ThankYou = () => {
  useEffect(() => {
    // Only fire browser-side events if they came from a real booking
    // GHL redirect URL: /thank-you?booked=true
    // Server-side CAPI with email/phone is handled by GHL webhook → /api/ghl-booked
    const params = new URLSearchParams(window.location.search);
    if (params.get("booked") === "true") {
      // Meta CompleteRegistration is handled server-side only via GHL webhook → /api/ghl-booked
      window.gtag?.("event", "booking_complete", {
        event_category: "Conversion",
        event_label: "GHL Booking",
      });
    }
  }, []);
  return (
    <div className="min-h-screen bg-gradient-hero flex flex-col">
      {/* Header */}
      <header className="py-4 px-4 border-b border-border/50">
        <div className="container">
          <div className="flex items-center">
            <img
              src="/logo.png"
              alt="APG Software Solutions"
              className="h-10"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-start justify-center px-4 py-8 md:py-12">
        <div className="w-full max-w-5xl mx-auto text-center">
          {/* Success Icon */}
          <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-primary/20 mb-6 sm:mb-8">
            <CheckCircle className="w-8 h-8 sm:w-10 sm:h-10 text-primary" />
          </div>

          {/* Heading */}
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
            You're All Set!
          </h1>

          <p className="text-lg sm:text-xl text-muted-foreground mb-8 sm:mb-12 max-w-xl mx-auto">
            Your consultation has been booked. Watch the short video below to see what happens next.
          </p>

          {/* Video */}
          <div className="relative mx-auto mb-8 sm:mb-12">
            <div className="aspect-video rounded-2xl overflow-hidden glass-card shadow-elevated">
              <iframe
                src="https://customer-96dey70a994gv78z.cloudflarestream.com/a7369f7587605a2c20a852a0d7a73385/iframe?poster=https%3A%2F%2Fcustomer-96dey70a994gv78z.cloudflarestream.com%2Fa7369f7587605a2c20a852a0d7a73385%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600&primaryColor=%239ae660"
                loading="lazy"
                className="w-full h-full border-0"
                allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture"
                allowFullScreen
              />
            </div>
            {/* Decorative glow */}
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 w-3/4 h-12 bg-primary/20 blur-3xl rounded-full" />
          </div>

          {/* What to Expect */}
          <div className="glass-card p-6 sm:p-8 max-w-2xl mx-auto mb-8 sm:mb-12 text-left">
            <h2 className="text-lg sm:text-xl font-semibold mb-6 text-center">What Happens Next</h2>

            <div className="space-y-4 sm:space-y-6">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0">
                  <Calendar className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Check Your Email</h3>
                  <p className="text-sm text-muted-foreground">You'll receive a calendar invite with the meeting link and details.</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0">
                  <Clock className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Prepare for the Call</h3>
                  <p className="text-sm text-muted-foreground">Think about your current tools, pain points, and goals for your custom CRM.</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-primary/15 flex items-center justify-center flex-shrink-0">
                  <ArrowRight className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">We'll Handle the Rest</h3>
                  <p className="text-sm text-muted-foreground">On our call, we'll map out your custom CRM blueprint together.</p>
                </div>
              </div>
            </div>
          </div>

          {/* YouTube CTA */}
          <div className="glass-card p-6 sm:p-8 max-w-2xl mx-auto text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-500/20 mb-4">
              <Youtube className="w-6 h-6 text-red-500" />
            </div>
            <h2 className="text-lg sm:text-xl font-semibold mb-2">Want to Learn More?</h2>
            <p className="text-sm text-muted-foreground mb-6">
              Check out our YouTube channel for tips on automation, CRMs, and scaling your business.
            </p>
            <Button variant="outline" className="group" asChild>
              <a href="https://www.youtube.com/@AdamGoodyer" target="_blank" rel="noopener noreferrer">
                <Youtube className="w-4 h-4 mr-2 text-red-500" />
                Visit Our YouTube Channel
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </a>
            </Button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-6 px-4 border-t border-border/50">
        <div className="container text-center">
          <p className="text-sm text-muted-foreground">
            Questions? Email us at <a href="mailto:hello@apgsoftware.com" className="text-primary hover:underline">hello@apgsoftware.com</a>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default ThankYou;

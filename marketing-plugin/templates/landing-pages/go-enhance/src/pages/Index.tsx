import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Testimonials from "@/components/Testimonials";
import Stats from "@/components/Stats";
import ValueProposition from "@/components/ValueProposition";
import ROICalculator from "@/components/ROICalculator";
import SocialProof from "@/components/SocialProof";
import TeamCredibility from "@/components/TeamCredibility";
import CaseStudy from "@/components/CaseStudy";
import FAQ from "@/components/FAQ";
import CTA from "@/components/CTA";
import Footer from "@/components/Footer";
import QualificationQuiz from "@/components/QualificationQuiz";
import { useQuiz } from "@/contexts/QuizContext";

const Index = () => {
  const { isQuizOpen, closeQuiz } = useQuiz();

  return (
    <main className="min-h-screen bg-background">
      <Header />
      <Hero />
      <section id="testimonials">
        <Testimonials />
      </section>
      <Stats />
      <ValueProposition />
<ROICalculator />
      <SocialProof />
      <TeamCredibility />
      <CaseStudy />
      <section id="faq">
        <FAQ />
      </section>
      <CTA />
      <Footer />
      <QualificationQuiz isOpen={isQuizOpen} onClose={closeQuiz} />
    </main>
  );
};

export default Index;

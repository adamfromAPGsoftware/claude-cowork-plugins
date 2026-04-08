import { useState, useEffect } from "react";
import { X, Youtube, Users, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { trackMetaEvent } from "@/lib/meta-events";
import { track } from "@/lib/analytics";

interface Question {
  id: number;
  question: string;
  options: { label: string; value: string }[];
}

const questions: Question[] = [
  {
    id: 1,
    question: "How many people are involved in scoping/discovery at your agency?",
    options: [
      { label: "Just me", value: "1" },
      { label: "2-3 people", value: "2-3" },
      { label: "4-6 people", value: "4-6" },
      { label: "7+ people", value: "7+" },
    ],
  },
  {
    id: 2,
    question: "How many hours does a typical client scoping engagement take?",
    options: [
      { label: "Less than 40 hours", value: "under40" },
      { label: "40-100 hours", value: "40-100" },
      { label: "100-200 hours", value: "100-200" },
      { label: "200+ hours", value: "200+" },
    ],
  },
  {
    id: 3,
    question: "How many new client engagements do you scope per month?",
    options: [
      { label: "1-2", value: "1-2" },
      { label: "3-5", value: "3-5" },
      { label: "6-10", value: "6-10" },
      { label: "10+", value: "10+" },
    ],
  },
  {
    id: 4,
    question: "What is your company's annual revenue?",
    options: [
      { label: "Less than $100,000", value: "under100k" },
      { label: "$100,000-$500,000", value: "100k-500k" },
      { label: "$500,000-$1M", value: "500k-1m" },
      { label: "$1M-$5M", value: "1m-5m" },
      { label: "$5M+", value: "5m+" },
    ],
  },
  {
    id: 5,
    question: "What best describes your current scoping process?",
    options: [
      { label: "Mostly manual (docs, spreadsheets)", value: "manual" },
      { label: "Some tools but still manual heavy", value: "semi-manual" },
      { label: "Structured process but slow", value: "structured" },
      { label: "Tried AI tools but they didn't work", value: "tried-ai" },
    ],
  },
];

const qualifiedRevenues = ["100k-500k", "500k-1m", "1m-5m", "5m+"];

interface QualificationQuizProps {
  isOpen: boolean;
  onClose: () => void;
}

const QualificationQuiz = ({ isOpen, onClose }: QualificationQuizProps) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [quizState, setQuizState] = useState<"quiz" | "qualified" | "not-qualified">("quiz");
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  // Fire quiz_open when the modal opens
  useEffect(() => {
    if (isOpen) track.quizOpen("other");
  }, [isOpen]);

  const buildBookingUrl = (quizAnswers: Record<number, string>) => {
    const baseUrl = "https://link.nilsdigital.com/widget/booking/ntxYdQyeowzIQuPIVeJu";

    // Map question index to GHL field Query Keys and get human-readable labels
    const fieldMapping: Record<number, { key: string; getLabel: (val: string) => string }> = {
      0: {
        key: "quiz_-_scoping_team_size",
        getLabel: (v) => questions[0].options.find(o => o.value === v)?.label || v
      },
      1: {
        key: "quiz_-_scoping_hours",
        getLabel: (v) => questions[1].options.find(o => o.value === v)?.label || v
      },
      2: {
        key: "quiz_-_engagements_per_month",
        getLabel: (v) => questions[2].options.find(o => o.value === v)?.label || v
      },
      3: {
        key: "quiz_-_annual_revenue",
        getLabel: (v) => questions[3].options.find(o => o.value === v)?.label || v
      },
      4: {
        key: "quiz_-_current_process",
        getLabel: (v) => questions[4].options.find(o => o.value === v)?.label || v
      },
    };

    const params = new URLSearchParams();
    Object.entries(quizAnswers).forEach(([questionIndex, value]) => {
      const mapping = fieldMapping[parseInt(questionIndex)];
      if (mapping) {
        params.append(mapping.key, mapping.getLabel(value));
      }
    });

    return `${baseUrl}?${params.toString()}`;
  };

  const handleAnswer = (value: string) => {
    if (selectedOption) return; // Prevent double-clicks
    setSelectedOption(value);

    const newAnswers = { ...answers, [currentQuestion]: value };
    setAnswers(newAnswers);

    // Track each answered step (1-indexed)
    track.quizAnswer(currentQuestion + 1, questions[currentQuestion].question, value);

    setTimeout(() => {
      setSelectedOption(null);
      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
      } else {
        // Last question — check qualification based on revenue (question index 3)
        const revenueAnswer = newAnswers[3];
        const isQualified = qualifiedRevenues.includes(revenueAnswer);
        track.quizComplete(isQualified);
        if (isQualified) {
          setQuizState("qualified");
          trackMetaEvent({ eventName: "Lead" });
          track.generateLead({
            scoping_team_size: newAnswers[0],
            scoping_hours: newAnswers[1],
            revenue_band: newAnswers[3],
            qualified: true,
          });
          const bookingUrl = buildBookingUrl(newAnswers);
          window.open(bookingUrl, "_blank");
          onClose();
          resetQuiz();
        } else {
          setQuizState("not-qualified");
        }
      }
    }, 300);
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setQuizState("quiz");
    setSelectedOption(null);
  };

  const handleClose = () => {
    // Fire abandon if user closes mid-quiz (answered something but didn't finish)
    if (quizState === "quiz" && Object.keys(answers).length > 0) {
      track.quizAbandon(currentQuestion + 1);
    }
    onClose();
    resetQuiz();
  };

  if (!isOpen) return null;

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={handleClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl mx-4 bg-background border border-border/50 rounded-2xl shadow-2xl overflow-hidden max-h-[90vh] overflow-y-auto">
        {/* Close button */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 p-2 rounded-full hover:bg-secondary/50 transition-colors z-10"
        >
          <X className="w-5 h-5 text-muted-foreground" />
        </button>

        {quizState === "quiz" && (
          <>
            {/* Progress bar */}
            <div className="h-1 bg-secondary">
              <div
                className="h-full bg-primary transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>

            <div className="p-4 md:p-8">
              {/* Question number */}
              <div className="flex items-center gap-2 mb-4 md:mb-6">
                <span className="text-primary font-semibold">{currentQuestion + 1}</span>
                <span className="text-primary">→</span>
                <span className="text-sm text-muted-foreground">
                  Question {currentQuestion + 1} of {questions.length}
                </span>
              </div>

              {/* Question */}
              <h2 className="text-xl md:text-2xl lg:text-3xl font-bold mb-6 md:mb-8">
                {questions[currentQuestion].question}
              </h2>

              {/* Options */}
              <div className="space-y-2 md:space-y-3">
                {questions[currentQuestion].options.map((option, index) => (
                  <button
                    key={option.value}
                    onClick={() => handleAnswer(option.value)}
                    className={`w-full flex items-center gap-3 md:gap-4 p-3 md:p-4 rounded-xl border-2 transition-all duration-150 text-left group ${
                      selectedOption === option.value
                        ? 'border-primary bg-primary/20 scale-[0.97]'
                        : 'border-border/50 bg-secondary/30 hover:bg-primary/10 hover:border-primary/50 active:scale-[0.97] active:bg-primary/20 active:border-primary'
                    }`}
                  >
                    <span className={`flex-shrink-0 w-7 h-7 md:w-8 md:h-8 rounded-lg border-2 flex items-center justify-center text-xs md:text-sm font-semibold transition-colors ${
                      selectedOption === option.value
                        ? 'bg-primary border-primary text-primary-foreground'
                        : 'border-muted-foreground/30 text-muted-foreground group-hover:border-primary group-hover:text-primary group-hover:bg-primary/10 group-active:bg-primary group-active:border-primary group-active:text-primary-foreground'
                    }`}>
                      {String.fromCharCode(65 + index)}
                    </span>
                    <span className="text-base md:text-lg text-foreground">{option.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </>
        )}

        {quizState === "not-qualified" && (
          <div className="p-4 md:p-8 text-center">
            {/* Logo placeholder */}
            <div className="flex justify-center mb-6 md:mb-8">
              <img src="/logo.png" alt="APG Software Solutions" className="h-10 md:h-12" />
            </div>

            <h2 className="text-2xl md:text-3xl font-bold mb-3 md:mb-4">Thanks for Your Interest!</h2>
            <p className="text-muted-foreground text-sm md:text-base max-w-md mx-auto mb-6 md:mb-10">
              Unfortunately, you don't qualify for the AI Scoping Engine at this time.
              But don't worry — there are still great ways we can help you!
            </p>

            {/* Options grid */}
            <div className="grid md:grid-cols-2 gap-4 md:gap-6 mb-6 md:mb-8">
              {/* YouTube Card */}
              <div className="bg-secondary/30 border border-border/50 rounded-xl p-6">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 rounded-2xl bg-red-500/20 flex items-center justify-center">
                    <Youtube className="w-8 h-8 text-red-500" />
                  </div>
                </div>
                <h3 className="text-xl font-bold mb-2">Free Content</h3>
                <p className="text-muted-foreground text-sm mb-6">
                  Check out my YouTube channel for free tutorials, tips, and insights on AI-powered agency workflows.
                </p>
                <Button
                  className="w-full bg-red-500 hover:bg-red-600 text-white"
                  onClick={() => window.open("https://www.youtube.com/@adamfreelances/featured", "_blank")}
                >
                  <Youtube className="w-4 h-4 mr-2" />
                  Visit YouTube Channel
                  <ExternalLink className="w-4 h-4 ml-2" />
                </Button>
              </div>

              {/* Skool Card */}
              <div className="bg-secondary/30 border border-border/50 rounded-xl p-6">
                <div className="flex justify-center mb-4">
                  <span className="text-4xl font-bold">
                    <span className="text-yellow-400">s</span>
                    <span className="text-green-400">k</span>
                    <span className="text-blue-400">o</span>
                    <span className="text-red-400">o</span>
                    <span className="text-foreground">l</span>
                  </span>
                </div>
                <h3 className="text-xl font-bold mb-2">Learn to Build Your Own</h3>
                <p className="text-muted-foreground text-sm mb-6">
                  Join my Skool community where I teach how to build AI-powered agency tools. Perfect for DIY builders!
                </p>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => window.open("https://skool.com/ai-builders-hub", "_blank")}
                >
                  <Users className="w-4 h-4 mr-2" />
                  Join AI Builders Hub
                  <ExternalLink className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </div>

            <button
              onClick={handleClose}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Close this window
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default QualificationQuiz;

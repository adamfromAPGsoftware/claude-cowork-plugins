import { useState, useMemo } from "react";
import { ArrowRight, Users, Clock, DollarSign, Briefcase } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuiz } from "@/contexts/QuizContext";
import { track } from "@/lib/analytics";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

const formatNumber = (num: number) => Math.round(num).toLocaleString('en-US');

const ROICalculator = () => {
  const { openQuiz } = useQuiz();

  const [staff, setStaff] = useState(2);
  const [hoursPerEngagement, setHoursPerEngagement] = useState(150);
  const [hourlyRate, setHourlyRate] = useState(100);
  const [engagementsPerMonth, setEngagementsPerMonth] = useState(2);

  const calculations = useMemo(() => {
    const currentAnnual = staff * hoursPerEngagement * hourlyRate * engagementsPerMonth * 12;
    const withAiAnnual = staff * (hoursPerEngagement * 0.1) * hourlyRate * engagementsPerMonth * 12;
    const annualSavings = currentAnnual - withAiAnnual;
    const monthlySavings = annualSavings / 12;
    const paybackDays = monthlySavings > 0 ? Math.ceil((5000 / monthlySavings) * 30) : 0;

    let paybackLabel = "";
    if (paybackDays <= 0) {
      paybackLabel = "N/A";
    } else if (paybackDays < 7) {
      paybackLabel = `${paybackDays} days`;
    } else if (paybackDays < 30) {
      const weeks = Math.ceil(paybackDays / 7);
      paybackLabel = `${weeks} week${weeks > 1 ? "s" : ""}`;
    } else {
      const weeks = Math.ceil(paybackDays / 7);
      paybackLabel = `${weeks} weeks`;
    }

    return { currentAnnual, withAiAnnual, annualSavings, monthlySavings, paybackLabel };
  }, [staff, hoursPerEngagement, hourlyRate, engagementsPerMonth]);

  const chartData = [
    { name: "Current", value: calculations.currentAnnual },
    { name: "With AI Scoping", value: calculations.withAiAnnual },
  ];

  const chartColors = ["#ef4444", "#9ae660"];

  return (
    <section id="calculator" className="py-24 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent" />

      <div className="container px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-6 sm:mb-8">
            <span className="inline-block text-primary font-semibold text-xs sm:text-sm tracking-wider uppercase mb-3 sm:mb-4">
              Savings Calculator
            </span>
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-3 sm:mb-4">
              Calculate Your Scoping Savings
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground">
              See how much your agency could save with AI-powered scoping
            </p>
          </div>

          {/* Main Panel */}
          <div className="glass-card p-4 sm:p-6 md:p-8 mb-6 shadow-[0_0_80px_rgba(154,230,96,0.12)]">

            {/* Sliders */}
            <div className="space-y-8 mb-10">
              {/* Staff slider */}
              <div>
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center text-primary">
                    <Users className="w-4 h-4" />
                  </div>
                  <label className="text-sm font-medium text-foreground">
                    Senior staff involved in scoping
                  </label>
                </div>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={staff}
                    onChange={e => setStaff(parseInt(e.target.value))}
                    className="flex-1 h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                  <span className="px-3 py-1 bg-primary/15 text-primary rounded-md text-sm font-semibold min-w-[50px] text-center">
                    {staff}
                  </span>
                </div>
              </div>

              {/* Hours per engagement slider */}
              <div>
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center text-primary">
                    <Clock className="w-4 h-4" />
                  </div>
                  <label className="text-sm font-medium text-foreground">
                    Hours per scoping engagement
                  </label>
                </div>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="40"
                    max="300"
                    step="10"
                    value={hoursPerEngagement}
                    onChange={e => setHoursPerEngagement(parseInt(e.target.value))}
                    className="flex-1 h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                  <span className="px-3 py-1 bg-primary/15 text-primary rounded-md text-sm font-semibold min-w-[60px] text-center">
                    {hoursPerEngagement}h
                  </span>
                </div>
              </div>

              {/* Hourly rate slider */}
              <div>
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center text-primary">
                    <DollarSign className="w-4 h-4" />
                  </div>
                  <label className="text-sm font-medium text-foreground">
                    Hourly rate of those staff
                  </label>
                </div>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="50"
                    max="200"
                    step="10"
                    value={hourlyRate}
                    onChange={e => setHourlyRate(parseInt(e.target.value))}
                    className="flex-1 h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                  <span className="px-3 py-1 bg-primary/15 text-primary rounded-md text-sm font-semibold min-w-[60px] text-center">
                    ${hourlyRate}
                  </span>
                </div>
              </div>

              {/* Engagements per month slider */}
              <div>
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center text-primary">
                    <Briefcase className="w-4 h-4" />
                  </div>
                  <label className="text-sm font-medium text-foreground">
                    New client engagements per month
                  </label>
                </div>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={engagementsPerMonth}
                    onChange={e => setEngagementsPerMonth(parseInt(e.target.value))}
                    className="flex-1 h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                  <span className="px-3 py-1 bg-primary/15 text-primary rounded-md text-sm font-semibold min-w-[50px] text-center">
                    {engagementsPerMonth}
                  </span>
                </div>
              </div>
            </div>

            {/* Results */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
              <div className="bg-destructive/10 border border-destructive/20 rounded-xl p-5 text-center">
                <p className="text-xs text-muted-foreground mb-1">Current Annual Scoping Cost</p>
                <p className="text-2xl sm:text-3xl font-bold text-destructive">${formatNumber(calculations.currentAnnual)}</p>
              </div>
              <div className="bg-primary/10 border border-primary/20 rounded-xl p-5 text-center">
                <p className="text-xs text-muted-foreground mb-1">With AI (90% Reduction)</p>
                <p className="text-2xl sm:text-3xl font-bold text-primary">${formatNumber(calculations.withAiAnnual)}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
              <div className="bg-gradient-to-br from-primary/15 to-primary/5 border border-primary/30 rounded-xl p-5 text-center">
                <p className="text-xs text-muted-foreground mb-1">Annual Savings</p>
                <p className="text-3xl sm:text-4xl font-bold text-gradient">${formatNumber(calculations.annualSavings)}</p>
              </div>
              <div className="bg-gradient-to-br from-primary/15 to-primary/5 border border-primary/30 rounded-xl p-5 text-center">
                <p className="text-xs text-muted-foreground mb-1">Payback Period</p>
                <p className="text-3xl sm:text-4xl font-bold text-gradient">{calculations.paybackLabel}</p>
              </div>
            </div>

            {/* Chart */}
            <div className="bg-secondary/30 rounded-xl p-4 sm:p-6 mb-8">
              <h4 className="text-sm font-semibold text-muted-foreground mb-4 text-center">Annual Scoping Cost Comparison</h4>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" stroke="rgba(255,255,255,0.4)" fontSize={12} />
                  <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                  <Tooltip
                    formatter={(value: number) => [`$${formatNumber(value)}`, "Annual Cost"]}
                    contentStyle={{ backgroundColor: "hsl(var(--background))", border: "1px solid hsl(var(--border))", borderRadius: "8px" }}
                    labelStyle={{ color: "hsl(var(--foreground))" }}
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {chartData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={chartColors[index]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* CTA */}
            <div className="text-center">
              <Button variant="hero" size="lg" className="group" onClick={() => { track.ctaClick("roi_calculator"); openQuiz(); }}>
                See If You Qualify
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <p className="text-xs text-muted-foreground mt-3">
                Take the 60-second quiz to see if the AI Scoping Engine is right for your agency
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ROICalculator;

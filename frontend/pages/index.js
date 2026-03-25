import { useMemo, useState } from "react";

import FeatureCard from "../components/FeatureCard";
import MoneyHealthBreakdown from "../components/MoneyHealthBreakdown";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api/v1";

const defaultProfile = {
  age: 27,
  monthly_income: 80000,
  monthly_expenses: 42000,
  monthly_emi: 8000,
  existing_investments: 250000,
  emergency_fund: 100000,
  annual_insurance_cover: 600000,
  annual_salary: 960000,
  risk_appetite: "balanced",
  goals: [
    { name: "Retirement Corpus", target_amount: 30000000, years_to_goal: 25, priority: "high" },
    { name: "House Down Payment", target_amount: 3000000, years_to_goal: 7, priority: "medium" },
  ],
};

const defaultTax = {
  annual_salary: 960000,
  section_80c: 150000,
  section_80d: 25000,
  hra_exemption: 120000,
  home_loan_interest: 0,
  other_deductions: 0,
};

export default function Home() {
  const [profileJson, setProfileJson] = useState(JSON.stringify(defaultProfile, null, 2));
  const [taxJson, setTaxJson] = useState(JSON.stringify(defaultTax, null, 2));
  const [question, setQuestion] = useState("Mere liye monthly SIP kitna hona chahiye FIRE goal ke liye?");
  const [chatLanguage, setChatLanguage] = useState("en");
  const [voiceEnabled, setVoiceEnabled] = useState(false);

  const [moneyHealth, setMoneyHealth] = useState(null);
  const [firePlan, setFirePlan] = useState(null);
  const [taxResult, setTaxResult] = useState(null);
  const [chatAnswer, setChatAnswer] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const parsedProfile = useMemo(() => {
    try {
      return JSON.parse(profileJson);
    } catch {
      return null;
    }
  }, [profileJson]);

  async function runPlanner() {
    if (!parsedProfile) {
      setError("Profile JSON invalid hai.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const [scoreRes, planRes] = await Promise.all([
        fetch(`${API_BASE}/finance/money-health`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(parsedProfile),
        }),
        fetch(`${API_BASE}/finance/fire-planner`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(parsedProfile),
        }),
      ]);

      if (!scoreRes.ok || !planRes.ok) {
        throw new Error("Backend response unsuccessful");
      }

      const scoreData = await scoreRes.json();
      const planData = await planRes.json();
      setMoneyHealth(scoreData);
      setFirePlan(planData);
    } catch (err) {
      setError(`Planner call fail hua: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function runTaxOptimizer() {
    setLoading(true);
    setError("");
    try {
      const payload = JSON.parse(taxJson);
      const response = await fetch(`${API_BASE}/finance/tax-optimizer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Tax optimizer failed");
      }

      setTaxResult(await response.json());
    } catch (err) {
      setError(`Tax optimizer error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function askAdvisor() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/finance/advisor-chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, profile: parsedProfile }),
      });
      if (!response.ok) {
        throw new Error("Advisor endpoint failed");
      }
      const data = await response.json();
      setChatAnswer(`${data.answer}\n\n${data.disclaimer}`);
    } catch (err) {
      setError(`Advisor error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function askAdvisorV2() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/finance/advisor-chat-v2`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          language: chatLanguage,
          voice_enabled: voiceEnabled,
          profile: parsedProfile,
        }),
      });

      if (!response.ok) {
        throw new Error("Advisor V2 endpoint failed");
      }

      const data = await response.json();
      const voiceLine = data.tts_text ? `\n\n[Voice Output Ready]\n${data.tts_text}` : "";
      setChatAnswer(`${data.answer_text}\n\n${data.disclaimer}${voiceLine}`);
    } catch (err) {
      setError(`Advisor V2 error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <header className="hero">
        <div>
          <h1>FinGuru AI</h1>
          <p>
            AI-powered personal money mentor for India: Money Health Score, FIRE planner, tax optimization,
            and advisor chat in one dashboard.
          </p>
        </div>
        <button onClick={runPlanner} disabled={loading}>
          {loading ? "Processing..." : "Run Financial Plan"}
        </button>
      </header>

      {error && <div className="error-box">{error}</div>}

      <section className="cards-row">
        <FeatureCard
          title="Money Health"
          value={moneyHealth ? `${moneyHealth.total_score}/100` : "--"}
          subtitle="Emergency + Debt + Tax + Retirement"
        />
        <FeatureCard
          title="Monthly SIP"
          value={firePlan ? `Rs ${Math.round(firePlan.total_monthly_sip).toLocaleString("en-IN")}` : "--"}
          subtitle="Goal-wise FIRE investing suggestion"
        />
        <FeatureCard
          title="Tax Saved"
          value={taxResult ? `Rs ${Math.round(taxResult.tax_saved).toLocaleString("en-IN")}` : "--"}
          subtitle="Old vs New regime recommendation"
        />
      </section>

      <section className="panel">
        <h2>1) Onboarding Input (JSON)</h2>
        <textarea value={profileJson} onChange={(event) => setProfileJson(event.target.value)} rows={16} />
      </section>

      <MoneyHealthBreakdown result={moneyHealth} />

      {firePlan && (
        <section className="panel">
          <h2>2) FIRE Path Planner</h2>
          <p>
            Asset Allocation: Equity {firePlan.asset_allocation.equity}% | Debt {firePlan.asset_allocation.debt}% |
            Gold {firePlan.asset_allocation.gold}% | Cash {firePlan.asset_allocation.cash}%
          </p>
          <p>Emergency Fund Target: Rs {Math.round(firePlan.emergency_fund_target).toLocaleString("en-IN")}</p>
          <p>Insurance Gap: Rs {Math.round(firePlan.insurance_gap).toLocaleString("en-IN")}</p>
          <div className="grid-2">
            {firePlan.goals.map((goal) => (
              <div className="mini-card" key={goal.goal_name}>
                <strong>{goal.goal_name}</strong>
                <div>SIP: Rs {Math.round(goal.monthly_sip).toLocaleString("en-IN")}/month</div>
                <small>
                  Corpus Rs {Math.round(goal.expected_corpus).toLocaleString("en-IN")} in {goal.years_to_goal} years
                </small>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="panel">
        <h2>3) Tax Optimizer</h2>
        <textarea value={taxJson} onChange={(event) => setTaxJson(event.target.value)} rows={8} />
        <button onClick={runTaxOptimizer} disabled={loading}>
          Run Tax Comparison
        </button>
        {taxResult && (
          <div className="tax-grid">
            <div className="mini-card">
              <strong>Old Regime Tax</strong>
              <div>Rs {Math.round(taxResult.old_regime.total_tax).toLocaleString("en-IN")}</div>
            </div>
            <div className="mini-card">
              <strong>New Regime Tax</strong>
              <div>Rs {Math.round(taxResult.new_regime.total_tax).toLocaleString("en-IN")}</div>
            </div>
            <div className="mini-card">
              <strong>Better Regime</strong>
              <div>{taxResult.better_regime.toUpperCase()}</div>
            </div>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>4) AI Financial Advisor Chat</h2>
        <textarea rows={4} value={question} onChange={(event) => setQuestion(event.target.value)} />
        <div className="chat-controls">
          <label>
            Language:
            <select value={chatLanguage} onChange={(event) => setChatLanguage(event.target.value)}>
              <option value="en">English</option>
              <option value="hi">Hindi (Phase-2)</option>
            </select>
          </label>
          <label>
            <input
              type="checkbox"
              checked={voiceEnabled}
              onChange={(event) => setVoiceEnabled(event.target.checked)}
            />
            Voice output (Phase-2)
          </label>
        </div>
        <div className="chat-actions">
          <button onClick={askAdvisor} disabled={loading}>
            Ask Advisor (V1)
          </button>
          <button onClick={askAdvisorV2} disabled={loading}>
            Ask Advisor (V2 Hindi + Voice)
          </button>
        </div>
        {chatAnswer && <pre className="chat-output">{chatAnswer}</pre>}
      </section>
    </main>
  );
}

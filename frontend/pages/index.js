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

const defaultLifeEvent = {
  event_type: "bonus",
  amount: 200000,
  profile: defaultProfile,
};

const defaultCouples = {
  partner_one: {
    name: "Aman",
    annual_salary: 1200000,
    section_80c: 120000,
    section_80d: 20000,
    monthly_expenses: 45000,
    monthly_emi: 10000,
  },
  partner_two: {
    name: "Riya",
    annual_salary: 900000,
    section_80c: 150000,
    section_80d: 25000,
    monthly_expenses: 35000,
    monthly_emi: 5000,
  },
  annual_rent_paid: 300000,
  combined_goal_sip_target: 50000,
};

const defaultMFXray = {
  statement_source: "manual",
  invested_amount: 1000000,
  current_value: 1420000,
  years_held: 4,
  expense_ratio_percent: 1.4,
  benchmark_return_percent: 12,
};

export default function Home() {
  const [profileJson, setProfileJson] = useState(JSON.stringify(defaultProfile, null, 2));
  const [taxJson, setTaxJson] = useState(JSON.stringify(defaultTax, null, 2));
  const [question, setQuestion] = useState("Mere liye monthly SIP kitna hona chahiye FIRE goal ke liye?");
  const [chatLanguage, setChatLanguage] = useState("en");
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [lifeEventJson, setLifeEventJson] = useState(JSON.stringify(defaultLifeEvent, null, 2));
  const [couplesJson, setCouplesJson] = useState(JSON.stringify(defaultCouples, null, 2));
  const [mfXrayJson, setMfXrayJson] = useState(JSON.stringify(defaultMFXray, null, 2));

  const [moneyHealth, setMoneyHealth] = useState(null);
  const [firePlan, setFirePlan] = useState(null);
  const [taxResult, setTaxResult] = useState(null);
  const [lifeEventResult, setLifeEventResult] = useState(null);
  const [couplesResult, setCouplesResult] = useState(null);
  const [taxWizardResult, setTaxWizardResult] = useState(null);
  const [mfXrayResult, setMfXrayResult] = useState(null);
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

  async function runTaxWizard() {
    setLoading(true);
    setError("");
    try {
      const payload = JSON.parse(taxJson);
      const response = await fetch(`${API_BASE}/finance/tax-wizard`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("Tax wizard failed");
      }
      setTaxWizardResult(await response.json());
    } catch (err) {
      setError(`Tax wizard error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function runLifeEventAdvisor() {
    setLoading(true);
    setError("");
    try {
      const payload = JSON.parse(lifeEventJson);
      const response = await fetch(`${API_BASE}/finance/life-event-advisor`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("Life event advisor failed");
      }
      setLifeEventResult(await response.json());
    } catch (err) {
      setError(`Life event advisor error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function runCouplesPlanner() {
    setLoading(true);
    setError("");
    try {
      const payload = JSON.parse(couplesJson);
      const response = await fetch(`${API_BASE}/finance/couples-planner`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("Couples planner failed");
      }
      setCouplesResult(await response.json());
    } catch (err) {
      setError(`Couples planner error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function runMFXray() {
    setLoading(true);
    setError("");
    try {
      const payload = JSON.parse(mfXrayJson);
      const response = await fetch(`${API_BASE}/finance/mf-portfolio-xray`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("MF X-Ray failed");
      }
      setMfXrayResult(await response.json());
    } catch (err) {
      setError(`MF X-Ray error: ${err.message}`);
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
        <div className="chat-actions">
          <button onClick={runTaxOptimizer} disabled={loading}>
            Run Tax Comparison
          </button>
          <button onClick={runTaxWizard} disabled={loading}>
            Run Tax Wizard
          </button>
        </div>
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
        {taxWizardResult && (
          <div className="mini-card" style={{ marginTop: "10px" }}>
            <strong>Tax Wizard Missing Deductions</strong>
            <ul>
              {taxWizardResult.missing_deductions.map((item, idx) => (
                <li key={`${item}-${idx}`}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>4) Life Event Financial Advisor</h2>
        <textarea value={lifeEventJson} onChange={(event) => setLifeEventJson(event.target.value)} rows={10} />
        <button onClick={runLifeEventAdvisor} disabled={loading}>
          Run Life Event Advisor
        </button>
        {lifeEventResult && (
          <div className="mini-card" style={{ marginTop: "10px" }}>
            <strong>Event: {lifeEventResult.event_type}</strong>
            <ul>
              {lifeEventResult.action_plan.map((item, idx) => (
                <li key={`${item}-${idx}`}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>5) Couple&apos;s Money Planner</h2>
        <textarea value={couplesJson} onChange={(event) => setCouplesJson(event.target.value)} rows={12} />
        <button onClick={runCouplesPlanner} disabled={loading}>
          Run Couples Planner
        </button>
        {couplesResult && (
          <div className="mini-card" style={{ marginTop: "10px" }}>
            <div>Combined Annual Income: Rs {Math.round(couplesResult.combined_annual_income).toLocaleString("en-IN")}</div>
            <div>
              Combined Monthly Surplus: Rs {Math.round(couplesResult.combined_monthly_surplus).toLocaleString("en-IN")}
            </div>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>6) MF Portfolio X-Ray</h2>
        <textarea value={mfXrayJson} onChange={(event) => setMfXrayJson(event.target.value)} rows={8} />
        <button onClick={runMFXray} disabled={loading}>
          Run MF X-Ray
        </button>
        {mfXrayResult && (
          <div className="mini-card" style={{ marginTop: "10px" }}>
            <div>Estimated XIRR: {mfXrayResult.estimated_xirr_percent}%</div>
            <div>Benchmark Delta: {mfXrayResult.benchmark_comparison_percent}%</div>
            <div>Expense Drag: Rs {Math.round(mfXrayResult.expense_drag_amount).toLocaleString("en-IN")}</div>
            <div>Overlap Risk: {mfXrayResult.overlap_risk_level.toUpperCase()}</div>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>7) AI Financial Advisor Chat</h2>
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

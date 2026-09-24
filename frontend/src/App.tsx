import { useState } from "react";
import { LeadForm } from "./components/LeadForm";
import { SubmissionResult } from "./components/SubmissionResult";
import type { LeadAccepted } from "./types/lead";

export function App() {
  const [result, setResult] = useState<LeadAccepted | null>(null);
  return (
    <main className="page-shell">
      <section className="intro-panel" aria-labelledby="page-title">
        <a className="brand" href="/" aria-label="PrimeHomes home"><span className="brand-mark" aria-hidden="true">P</span><span>PrimeHomes</span></a>
        <div className="intro-content">
          <p className="eyebrow light">Your next move starts here</p>
          <h1 id="page-title">Find the right property, without the runaround.</h1>
          <p>Tell us what you need once. We’ll organise your requirements and connect you with the right property adviser.</p>
          <ul className="benefit-list"><li><span>01</span> Share your property requirements</li><li><span>02</span> Get matched to the right adviser</li><li><span>03</span> Receive focused property options</li></ul>
        </div>
        <p className="panel-footer">Lagos property support, made simpler.</p>
      </section>
      <section className="form-panel">
        {result ? <SubmissionResult result={result} onStartAnother={() => setResult(null)} /> : <LeadForm onSuccess={setResult} />}
      </section>
    </main>
  );
}

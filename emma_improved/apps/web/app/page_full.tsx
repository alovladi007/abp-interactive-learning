"use client";

import { useState, useEffect } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
const USE_LANGGRAPH_KEY = "use_langgraph";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [steps, setSteps] = useState<any[]>([]);
  const [trace, setTrace] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [useLG, setUseLG] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem(USE_LANGGRAPH_KEY) === "1";
    }
    return false;
  });

  async function solve() {
    setLoading(true);
    setAnswer("");
    setSteps([]);
    setTrace([]);

    try {
      const response = await fetch(`${API_BASE}/v1/chat/solve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          flags: { useLangGraph: useLG }
        }),
      });

      const data = await response.json();
      setAnswer(data.answer || "No answer");
      setSteps(data.steps || []);
      setTrace(data.trace || []);
    } catch (error) {
      setAnswer("Error: " + error);
    } finally {
      setLoading(false);
    }
  }

  async function runSandbox() {
    try {
      const response = await fetch(`${API_BASE}/v1/tools/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          language: "python",
          code: "print('Hello from sandbox!')\nprint(2**10)"
        }),
      });

      const data = await response.json();
      alert("Sandbox output:\n" + (data.stdout || JSON.stringify(data)));
    } catch (error) {
      alert("Sandbox error: " + error);
    }
  }

  const examples = [
    "Integrate sin(x)",
    "What is Ohm's law?",
    "Calculate projectile motion",
  ];

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <h1>EMMA - Full Stack Edition</h1>
      <p>Math assistant with optional pgvector, Neo4j, LangGraph, and Sandbox</p>

      <div style={{ marginTop: "2rem" }}>
        <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a math or science question..."
            style={{
              flex: 1,
              padding: "0.5rem",
              fontSize: "1rem",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
          <button
            onClick={solve}
            disabled={loading}
            style={{
              padding: "0.5rem 1rem",
              background: loading ? "#ccc" : "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Solving..." : "Solve"}
          </button>
        </div>

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <label>
            <input
              type="checkbox"
              checked={useLG}
              onChange={(e) => {
                setUseLG(e.target.checked);
                if (typeof window !== "undefined") {
                  localStorage.setItem(
                    USE_LANGGRAPH_KEY,
                    e.target.checked ? "1" : "0"
                  );
                }
              }}
            />
            {" Use LangGraph planner"}
          </label>
          <button
            onClick={runSandbox}
            style={{
              padding: "0.5rem 1rem",
              background: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Run Sandbox Demo
          </button>
        </div>

        <div style={{ marginTop: "1rem" }}>
          {examples.map((ex, i) => (
            <button
              key={i}
              onClick={() => setQuestion(ex)}
              style={{
                marginRight: "0.5rem",
                padding: "0.25rem 0.5rem",
                background: "#f8f9fa",
                border: "1px solid #dee2e6",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              {ex}
            </button>
          ))}
        </div>
      </div>

      {answer && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Answer</h2>
          <div style={{
            padding: "1rem",
            background: "#f8f9fa",
            borderRadius: "4px",
            whiteSpace: "pre-wrap",
          }}>
            {answer}
          </div>
        </div>
      )}

      {trace.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3>LangGraph Trace</h3>
          <ul>
            {trace.map((t, i) => (
              <li key={i}>
                <strong>{t.node}</strong>: {JSON.stringify(t)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {steps.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Steps</h3>
          <ol>
            {steps.map((s, i) => (
              <li key={i}>
                {s.role} - {s.action}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

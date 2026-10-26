import { useState } from "react";
import {
  Activity,
  ArrowUpRight,
  Bot,
  ChevronDown,
  CircleHelp,
  Database,
  History,
  LayoutDashboard,
  LoaderCircle,
  Menu,
  MessageSquare,
  PanelLeftClose,
  Play,
  Settings,
  ShieldCheck,
  Sparkles,
  Table2,
  Terminal,
  TrendingUp,
} from "lucide-react";
import "./App.css";

type AnalysisResult = {
  question: string;
  sql: string;
  answer: string;
  columns: string[];
  rows: unknown[];
  row_count: number;
  truncated: boolean;
};

const examples = [
  "Which products generate the highest revenue?",
  "Who are our top customers?",
  "How many orders do we have?",
];

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"results" | "sql">("results");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  async function askQuestion(value = question) {
    if (!value.trim() || loading) return;

    setQuestion(value);
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: value.trim() }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "The request could not be completed.",
        );
      }

      setResult(data as AnalysisResult);
      setActiveTab("results");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not connect to the backend. Make sure FastAPI is running.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      {sidebarOpen && (
        <aside className="sidebar">
          <div className="brand">
            <div className="brand-icon"><Activity size={22} /></div>
            <div>
              <strong>InsightAI</strong>
              <span>DATA ANALYST</span>
            </div>
            <button className="icon-button sidebar-close" onClick={() => setSidebarOpen(false)} aria-label="Close sidebar">
              <PanelLeftClose size={18} />
            </button>
          </div>

          <button className="new-chat" onClick={() => {
            setQuestion("");
            setResult(null);
            setError("");
          }}>
            <MessageSquare size={17} /> New analysis <span>+</span>
          </button>

          <div className="nav-label">WORKSPACE</div>
          <button className="nav-item active"><LayoutDashboard size={18} /> Overview</button>
          <button className="nav-item" onClick={() => document.getElementById("question-input")?.focus()}>
            <Sparkles size={18} /> Ask AI
          </button>
          <button className="nav-item" onClick={() => {
            setResult(null);
            setError("");
            setQuestion("");
          }}>
            <History size={18} /> Recent analysis
          </button>

          <div className="nav-label sources-label">DATA SOURCES</div>
          <div className="source-item">
            <div className="source-icon"><Database size={17} /></div>
            <div className="source-text">
              <strong>PostgreSQL</strong>
              <span><i className="status-dot" /> Configured locally</span>
            </div>
            <span className="source-menu">···</span>
          </div>
          <button className="add-source" onClick={() => setError("Database connection setup is not available yet. We'll add it in a later step.")}>
            + Add data source
          </button>

          <div className="sidebar-bottom">
            <div className="help-card">
              <CircleHelp size={18} />
              <div><strong>Need a hand?</strong><span>Explore how to ask better questions.</span></div>
              <ArrowUpRight size={15} />
            </div>
            <button className="nav-item"><Settings size={18} /> Settings</button>
            <div className="profile">
              <div className="avatar">AI</div>
              <div><strong>Analyst Workspace</strong><span>Local development</span></div>
              <ChevronDown size={16} />
            </div>
          </div>
        </aside>
      )}

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs">
            {!sidebarOpen && (
              <button className="icon-button" onClick={() => setSidebarOpen(true)} aria-label="Open sidebar">
                <Menu size={19} />
              </button>
            )}
            <span>Workspace</span><span className="crumb-slash">/</span><strong>Overview</strong>
          </div>
          <div className="topbar-right">
            <div className="environment"><span className="status-dot" /> Local environment</div>
            <button className="help-button"><CircleHelp size={17} /> Help</button>
          </div>
        </header>

        <div className="content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow"><Sparkles size={14} /> YOUR AI-POWERED WORKSPACE</div>
              <h1>Make data-driven <span>decisions.</span></h1>
              <p>Ask questions in plain English. Get answers from your data in seconds.</p>
            </div>
            <div className="welcome-art"><div className="art-ring ring-one" /><div className="art-ring ring-two" /><div className="art-core"><Bot size={34} /></div><Sparkles className="art-spark" size={20} /></div>
          </section>

          <section className="metrics">
            <div className="metric-card">
              <div className="metric-top"><span>DATA SOURCES</span><div className="metric-icon purple"><Database size={18} /></div></div>
              <div className="metric-value">01</div>
              <div className="metric-foot"><span className="metric-muted">Local configuration</span></div>
            </div>
            <div className="metric-card">
              <div className="metric-top"><span>QUERY STATUS</span><div className="metric-icon green"><ShieldCheck size={18} /></div></div>
              <div className="metric-value">{loading ? "Running" : result ? "Success" : "Ready"}</div>
              <div className="metric-foot"><span className="green-text">●</span><span>{loading ? "Analyzing your question" : "Ready for your next question"}</span></div>
            </div>
            <div className="metric-card">
              <div className="metric-top"><span>ROWS RETURNED</span><div className="metric-icon blue"><Table2 size={18} /></div></div>
              <div className="metric-value">{result ? result.row_count : "—"}</div>
              <div className="metric-foot"><span className="metric-muted">Latest query</span></div>
            </div>
            <div className="metric-card">
              <div className="metric-top"><span>AI ENGINE</span><div className="metric-icon orange"><TrendingUp size={18} /></div></div>
              <div className="metric-value engine-value">LangGraph</div>
              <div className="metric-foot"><span className="metric-muted">SQL analysis pipeline</span></div>
            </div>
          </section>

          <section className="ask-panel">
            <div className="panel-heading">
              <div className="heading-icon"><Sparkles size={19} /></div>
              <div><h2>Ask your data</h2><p>What would you like to know about your business?</p></div>
              <span className="ai-badge"><span /> AI ASSISTANT</span>
            </div>
            <form onSubmit={(event) => {
              event.preventDefault();
              void askQuestion();
            }}>
              <label className="sr-only" htmlFor="question-input">Ask a business question</label>
              <textarea
                id="question-input"
                placeholder="e.g. Which products generated the most revenue last month?"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    void askQuestion();
                  }
                }}
                rows={3}
              />
              <div className="input-footer">
                <span><Sparkles size={14} /> Ask in plain English · Press Enter to run</span>
                <button className="run-button" type="submit" disabled={loading || !question.trim()}>
                  {loading ? <LoaderCircle className="spin" size={17} /> : <Play size={16} fill="currentColor" />}
                  {loading ? "Analyzing..." : "Run analysis"}
                </button>
              </div>
            </form>
            <div className="suggestions">
              <span>TRY ASKING</span>
              {examples.map((example) => (
                <button key={example} onClick={() => {
                  setQuestion(example);
                  void askQuestion(example);
                }}>{example}<ArrowUpRight size={13} /></button>
              ))}
            </div>
          </section>

          {error && (
            <div className="error-banner" role="alert">
              <CircleHelp size={19} />
              <div><strong>Unable to complete analysis</strong><p>{error}</p></div>
              <button className="icon-button" onClick={() => setError("")} aria-label="Dismiss error">×</button>
            </div>
          )}

          {loading && (
            <section className="output-panel loading-panel">
              <LoaderCircle className="spin" size={23} />
              <div><strong>Analyzing your data...</strong><p>Generating SQL and preparing your results.</p></div>
            </section>
          )}

          {result && !loading && (
            <section className="output-panel">
              <div className="output-header">
                <div><div className="eyebrow"><span className="status-dot" /> ANALYSIS COMPLETE</div><h2>Your results</h2></div>
                <span className="row-count">{result.row_count} rows</span>
              </div>
              <div className="answer-card">
                <div className="answer-icon"><Sparkles size={18} /></div>
                <div><span className="answer-label">AI INSIGHT</span><p>{result.answer}</p></div>
              </div>
              <div className="tabs">
                <button className={activeTab === "results" ? "tab active-tab" : "tab"} onClick={() => setActiveTab("results")}><Table2 size={16} /> Results table</button>
                <button className={activeTab === "sql" ? "tab active-tab" : "tab"} onClick={() => setActiveTab("sql")}><Terminal size={16} /> Generated SQL</button>
              </div>
              {activeTab === "sql" ? (
                <pre className="sql-view"><code>{result.sql || "No SQL returned."}</code></pre>
              ) : (
                <div className="table-wrap">
                  {result.columns?.length ? (
                    <table>
                      <thead><tr>{result.columns.map((column, index) => <th key={`${column}-${index}`}>{column}</th>)}</tr></thead>
                      <tbody>
                        {result.rows?.map((row, rowIndex) => {
                          const cells = Array.isArray(row)
                            ? row
                            : typeof row === "object" && row !== null
                              ? Object.values(row as Record<string, unknown>)
                              : [row];

                          return (
                            <tr key={rowIndex}>
                              {cells.map((cell, cellIndex) => (
                                <td key={cellIndex}>
                                  {cell === null || cell === undefined
                                    ? "—"
                                    : typeof cell === "object"
                                      ? JSON.stringify(cell)
                                      : String(cell)}
                                </td>
                              ))}
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  ) : <p className="empty-results">The query returned no columns or rows.</p>}
                  {result.truncated && <p className="truncated-note">Results are limited to the first rows for safety.</p>}
                </div>
              )}
            </section>
          )}

          {!result && !loading && !error && (
            <section className="empty-state">
              <div className="empty-illustration"><div><Database size={28} /></div><span className="float-dot dot-a" /><span className="float-dot dot-b" /><span className="float-dot dot-c" /></div>
              <h3>Your insights start here</h3>
              <p>Ask your first question to turn your database into clear, actionable answers.</p>
            </section>
          )}

          <footer><span>InsightAI · AI Data Analyst</span><span><ShieldCheck size={14} /> Read-only query workflow</span></footer>
        </div>
      </main>
    </div>
  );
}

export default App;
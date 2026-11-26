import { useEffect, useState } from "react";
import { SAMPLES, analyzeFile, fetchHealth, loadSample } from "./api";
import { LANGUAGE_LABEL, METRIC_LABEL } from "./labels";
import type { AnalysisResult, SampleId } from "./types";

type Status = "idle" | "loading" | "ready" | "error";

function ScoreDial({ score }: { score: number }) {
  const angle = Math.round((score / 100) * 360);
  const hue = 8 + Math.round((score / 100) * 128);
  return (
    <div className="dial" role="img" aria-label={`Índice de analisabilidade ${score} de 100`}>
      <div className="dial-ring" style={{ background: `conic-gradient(hsl(${hue} 55% 45%) ${angle}deg, var(--rule) ${angle}deg)` }}>
        <div className="dial-core">
          <span className="dial-value">{score}</span>
          <span className="dial-caption">índice de analisabilidade</span>
        </div>
      </div>
    </div>
  );
}

function Header({ status }: { status: Status }) {
  const dot = status === "error" ? "dot dot-error" : status === "ready" ? "dot dot-ok" : "dot";
  return (
    <header className="masthead">
      <div>
        <h1>CobMind</h1>
        <p className="tagline">Plataforma de modernização de sistemas legados</p>
      </div>
      <div className="conn" aria-live="polite">
        <span className={dot} aria-hidden="true" />
        <span>API {status === "ready" ? "conectada" : status === "error" ? "indisponível" : status === "loading" ? "analisando…" : "aguardando"}</span>
      </div>
    </header>
  );
}

function SampleRail({ onPick }: { onPick: (id: SampleId) => void }) {
  return (
    <nav className="rail" aria-label="Amostras legadas">
      <p className="rail-label">Amostras do acervo</p>
      <div className="rail-list">
        {SAMPLES.map((sample) => (
          <button key={sample.id} type="button" className="chip" onClick={() => onPick(sample.id)}>
            <strong>{sample.label}</strong>
            <span>{sample.language}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}

function Editor({ value, onChange }: { value: string; onChange: (next: string) => void }) {
  return (
    <section className="editor">
      <div className="editor-head">
        <p className="editor-title">Fonte legado</p>
        <p className="editor-hint">Cole COBOL, Fortran ou PL/I — ou escolha uma amostra.</p>
      </div>
      <textarea
        spellCheck={false}
        aria-label="Código fonte legado"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="IDENTIFICATION DIVISION. …"
      />
    </section>
  );
}

function ResultPanel({ result }: { result: AnalysisResult }) {
  return (
    <section className="report" aria-label="Resultado da análise">
      <div className="report-top">
        <ScoreDial score={result.score} />
        <dl className="facts">
          <div><dt>Arquivo</dt><dd>{result.filename}</dd></div>
          <div><dt>Linguagem</dt><dd>{LANGUAGE_LABEL[result.language] ?? result.language}</dd></div>
          <div><dt>Parser</dt><dd>{result.parser}</dd></div>
          <div><dt>Linhas</dt><dd>{result.lines}</dd></div>
        </dl>
      </div>

      <ul className="metrics">
        {Object.entries(result.metrics).map(([key, value]) => (
          <li key={key}><span>{METRIC_LABEL[key] ?? key}</span><strong>{value}</strong></li>
        ))}
      </ul>

      <div className="sections">
        <section>
          <h2>Regras de negócio</h2>
          {result.rules.length === 0 ? (
            <p className="empty">Nenhuma regra identificada neste trecho.</p>
          ) : (
            <ol className="rules">
              {result.rules.map((rule) => (
                <li key={rule.id}>
                  <div className="rule-head">
                    <strong>{rule.title}</strong>
                    <span className="tag">{rule.category}</span>
                    <span className="conf">{Math.round(rule.confidence * 100)}%</span>
                  </div>
                  <p>{rule.description}</p>
                  <code>{rule.evidence}</code>
                </li>
              ))}
            </ol>
          )}
        </section>

        <section>
          <h2>Dependências</h2>
          {result.dependencies.length === 0 ? (
            <p className="empty">Nenhuma dependência externa mapeada.</p>
          ) : (
            <table className="deps">
              <thead><tr><th scope="col">Origem</th><th scope="col">Destino</th><th scope="col">Relação</th></tr></thead>
              <tbody>
                {result.dependencies.map((dep, index) => (
                  <tr key={`${dep.source}-${dep.target}-${index}`}>
                    <td>{dep.source}</td><td>{dep.target}</td><td>{dep.relation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <h2>Recomendações de modernização</h2>
          <ul className="recs">
            {result.recommendations.map((rec) => (
              <li key={rec.title}>
                <span className={`pill pill-${rec.priority}`}>{rec.priority === "high" ? "alta" : rec.priority === "medium" ? "média" : "baixa"}</span>
                <div>
                  <strong>{rec.title}</strong>
                  <p>{rec.rationale}</p>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>

      {result.warnings.length > 0 && (
        <aside className="warnings" role="note">
          <h2>Avisos</h2>
          <ul>{result.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul>
        </aside>
      )}
    </section>
  );
}

export default function Dashboard() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const [source, setSource] = useState("");
  const [filename, setFilename] = useState("fonte.txt");
  const [result, setResult] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    fetchHealth().then(() => setStatus("idle")).catch(() => setStatus("error"));
  }, []);

  async function runAnalysis() {
    if (!source.trim()) {
      setError("Cole um código legado antes de analisar.");
      return;
    }
    setStatus("loading");
    setError(null);
    try {
      const analysis = await analyzeFile(filename, source);
      setResult(analysis);
      setStatus("ready");
    } catch (cause) {
      setStatus("error");
      setError(cause instanceof Error ? cause.message : "Falha ao analisar.");
    }
  }

  async function pickSample(id: SampleId) {
    setStatus("loading");
    setError(null);
    try {
      const sample = await loadSample(id);
      setSource(sample.content);
      setFilename(sample.filename);
      const analysis = await analyzeFile(sample.filename, sample.content);
      setResult(analysis);
      setStatus("ready");
    } catch (cause) {
      setStatus("error");
      setError(cause instanceof Error ? cause.message : "Falha ao carregar amostra.");
    }
  }

  return (
    <main className="shell">
      <Header status={status} />
      <SampleRail onPick={pickSample} />
      <Editor value={source} onChange={setSource} />
      <div className="actions">
        <label className="filefield">
          <span>Nome do arquivo</span>
          <input value={filename} onChange={(event) => setFilename(event.target.value)} />
        </label>
        <button type="button" className="cta" onClick={runAnalysis} disabled={status === "loading"}>
          {status === "loading" ? "Analisando…" : "Analisar código"}
        </button>
      </div>
      {error && <p className="error" role="alert">{error}</p>}
      {result && <ResultPanel result={result} />}
      <footer className="foot">
        <p>Análise estática local — o código nunca sai do seu ambiente.</p>
      </footer>
    </main>
  );
}

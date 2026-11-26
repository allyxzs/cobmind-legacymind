import type { AnalysisResult, SampleId, SampleMeta } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

export const SAMPLES: SampleMeta[] = [
  { id: "custmstr", filename: "CUSTMSTR.cbl", label: "CUSTMSTR", language: "COBOL", description: "Cadastro de clientes e limite de crédito (VSAM)." },
  { id: "interest", filename: "INTEREST.cbl", label: "INTEREST", language: "COBOL", description: "Juros compostos e amortização de empréstimos." },
  { id: "payroll", filename: "payroll.f90", label: "PAYROLL", language: "Fortran", description: "Folha de pagamento com INSS e IRRF por faixa." },
  { id: "acctrec", filename: "acctrec.pli", label: "ACCTREC", language: "PL/I", description: "Contas a receber com taxa e totalização." },
];

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Falha na chamada: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  return request("/health");
}

export async function analyzeFile(filename: string, content: string): Promise<AnalysisResult> {
  return request("/api/v1/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename, content }),
  });
}

export async function loadSample(id: SampleId): Promise<{ filename: string; content: string }> {
  return request(`/api/v1/samples/${id}`);
}

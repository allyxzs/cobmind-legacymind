export interface CodeNode {
  id: string;
  name: string;
  kind: string;
  line?: number | null;
  metadata: Record<string, string | number | boolean>;
}

export interface Dependency {
  source: string;
  target: string;
  relation: string;
  line?: number | null;
}

export interface BusinessRule {
  id: string;
  title: string;
  description: string;
  category: string;
  confidence: number;
  line?: number | null;
  evidence: string;
}

export interface Recommendation {
  priority: "high" | "medium" | "low";
  title: string;
  rationale: string;
  target: string;
}

export interface AnalysisResult {
  filename: string;
  language: "cobol" | "fortran" | "pli" | "unknown";
  parser: string;
  lines: number;
  score: number;
  nodes: CodeNode[];
  dependencies: Dependency[];
  rules: BusinessRule[];
  recommendations: Recommendation[];
  metrics: Record<string, number>;
  warnings: string[];
}

export type SampleId = "custmstr" | "interest" | "payroll" | "acctrec";

export interface SampleMeta {
  id: SampleId;
  filename: string;
  label: string;
  language: string;
  description: string;
}

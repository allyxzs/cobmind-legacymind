const LANGUAGE_LABEL: Record<string, string> = {
  cobol: "COBOL",
  fortran: "Fortran",
  pli: "PL/I",
  unknown: "Indefinida",
};

const METRIC_LABEL: Record<string, string> = {
  routines: "Rotinas",
  dependencies: "Dependências",
  business_rules: "Regras de negócio",
  conditional_blocks: "Blocos condicionais",
  documentation_coverage: "Cobertura de doc.",
};

export { LANGUAGE_LABEL, METRIC_LABEL };

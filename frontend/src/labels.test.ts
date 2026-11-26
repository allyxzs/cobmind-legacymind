import { describe, expect, it } from "vitest";
import { SAMPLES } from "./api";
import { LANGUAGE_LABEL, METRIC_LABEL } from "./labels";

describe("labels", () => {
  it("expõe rótulos para as três linguagens legadas", () => {
    expect(LANGUAGE_LABEL.cobol).toBe("COBOL");
    expect(LANGUAGE_LABEL.fortran).toBe("Fortran");
    expect(LANGUAGE_LABEL.pli).toBe("PL/I");
  });

  it("traduz métricas conhecidas", () => {
    expect(METRIC_LABEL.business_rules).toContain("Regras");
  });
});

describe("samples", () => {
  it("cataloga as quatro amostras do acervo", () => {
    expect(SAMPLES).toHaveLength(4);
    expect(SAMPLES.map((s) => s.language)).toEqual(["COBOL", "COBOL", "Fortran", "PL/I"]);
  });
});

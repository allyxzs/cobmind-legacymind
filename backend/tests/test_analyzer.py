from app.analyzer import analyze


def test_analyzes_cobol_rules_and_dependencies():
    result = analyze("CUSTMSTR.cbl", """IDENTIFICATION DIVISION.\nPROGRAM-ID. CUSTMSTR.\nSELECT CUST-FILE ASSIGN TO VSAM-CUST.\nIF CUST-CLASS = 'A'\nCOMPUTE CUST-LIMIT = BALANCE * RATE.\n""")
    assert result.language == "cobol"
    assert result.metrics["business_rules"] >= 1
    assert result.metrics["dependencies"] >= 1
    assert result.recommendations


def test_detects_fortran_payroll():
    result = analyze("payroll.f90", "PROGRAM PAYROLL\nIF (GROSS <= 1412.00) THEN\nRATE_INSS = 0.0775\nEND IF")
    assert result.language == "fortran"
    assert result.metrics["business_rules"] == 1


def test_unknown_language_is_safe():
    result = analyze("README.txt", "hello world")
    assert result.language == "unknown"
    assert result.warnings

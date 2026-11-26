from __future__ import annotations

import re
from pathlib import Path
from .models import AnalysisResult, BusinessRule, CodeNode, Dependency, Recommendation

EXTENSIONS = {".cbl": "cobol", ".cob": "cobol", ".cobol": "cobol", ".f": "fortran", ".f90": "fortran", ".for": "fortran", ".pli": "pli", ".pl1": "pli"}


def detect_language(filename: str, content: str) -> str:
    language = EXTENSIONS.get(Path(filename).suffix.lower())
    if language:
        return language
    upper = content.upper()
    if "IDENTIFICATION DIVISION" in upper or "PROCEDURE DIVISION" in upper:
        return "cobol"
    if "PROGRAM " in upper or "SUBROUTINE " in upper or "IMPLICIT NONE" in upper:
        return "fortran"
    if "PROC OPTIONS" in upper or re.search(r"\bDCL\s+", upper):
        return "pli"
    return "unknown"


def _line_number(content: str, match: re.Match[str]) -> int:
    return content.count("\n", 0, match.start()) + 1


def _unique(items: list):
    seen = set()
    output = []
    for item in items:
        key = item.model_dump_json() if hasattr(item, "model_dump_json") else str(item)
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output


def _cobol(content: str):
    nodes, deps, rules = [], [], []
    for match in re.finditer(r"(?im)^\s*(?:PROGRAM-ID|[A-Z0-9-]+-PARA)\.?\s*:?\s*([A-Z0-9-]+)?", content):
        name = (match.group(1) or match.group(0)).strip(" .:")
        if name and name not in {"DIVISION", "SECTION"}:
            nodes.append(CodeNode(id=f"routine:{name.lower()}", name=name, kind="routine", line=_line_number(content, match)))
    for match in re.finditer(r"(?im)\b(?:SELECT\s+([A-Z0-9-]+).*?ASSIGN\s+TO\s+([A-Z0-9-]+)|CALL\s+['\"]?([A-Z0-9-]+))", content):
        source = "program"
        target = next((g for g in match.groups() if g), "unknown")
        relation = "reads-file" if "SELECT" in match.group(0).upper() else "calls"
        deps.append(Dependency(source=source, target=target, relation=relation, line=_line_number(content, match)))
        nodes.append(CodeNode(id=f"external:{target.lower()}", name=target, kind="file" if relation == "reads-file" else "program", line=_line_number(content, match)))
    for match in re.finditer(r"(?im)\b(IF|COMPUTE|ADD|SUBTRACT|MULTIPLY|DIVIDE)\b.*", content):
        text = match.group(0).strip()
        if any(token in text.upper() for token in ("LIMIT", "RATE", "TAX", "BALANCE", "INTEREST", "PAYMENT")):
            category = "credit" if "LIMIT" in text.upper() or "BALANCE" in text.upper() else "financial"
            rules.append(BusinessRule(id=f"rule-{len(rules)+1}", title="Regra financeira detectada", description="A lógica altera um valor monetário ou aplica uma condição de negócio.", category=category, confidence=.88, line=_line_number(content, match), evidence=text[:180]))
    return nodes, deps, rules


def _fortran(content: str):
    nodes, deps, rules = [], [], []
    for match in re.finditer(r"(?im)^\s*(PROGRAM|SUBROUTINE|FUNCTION)\s+([A-Z][A-Z0-9_]*)", content):
        nodes.append(CodeNode(id=f"routine:{match.group(2).lower()}", name=match.group(2), kind=match.group(1).lower(), line=_line_number(content, match)))
    for match in re.finditer(r"(?im)\bCALL\s+([A-Z][A-Z0-9_]*)", content):
        deps.append(Dependency(source="program", target=match.group(1), relation="calls", line=_line_number(content, match)))
    for match in re.finditer(r"(?im)^\s*(IF|ELSE\s+IF).*", content):
        text = match.group(0).strip()
        if any(x in text.upper() for x in ("RATE", "SALARY", "GROSS", "TAX", "INSS", "IRRF")):
            rules.append(BusinessRule(id=f"rule-{len(rules)+1}", title="Faixa condicional identificada", description="Uma condição por faixa define uma taxa ou resultado de negócio.", category="payroll", confidence=.84, line=_line_number(content, match), evidence=text[:180]))
    return nodes, deps, rules


def _pli(content: str):
    nodes, deps, rules = [], [], []
    for match in re.finditer(r"(?im)^\s*([A-Z][A-Z0-9_]*)\s*:\s*PROC", content):
        nodes.append(CodeNode(id=f"routine:{match.group(1).lower()}", name=match.group(1), kind="procedure", line=_line_number(content, match)))
    for match in re.finditer(r"(?im)\bCALL\s+([A-Z][A-Z0-9_]*)", content):
        deps.append(Dependency(source="program", target=match.group(1), relation="calls", line=_line_number(content, match)))
    for match in re.finditer(r"(?im)\b(IF|DO)\b.*", content):
        text = match.group(0).strip()
        if any(x in text.upper() for x in ("AMOUNT", "TAX", "RATE", "TOTAL")):
            rules.append(BusinessRule(id=f"rule-{len(rules)+1}", title="Regra de totalização identificada", description="O fluxo condiciona ou calcula um valor de contas a receber.", category="accounts-receivable", confidence=.8, line=_line_number(content, match), evidence=text[:180]))
    return nodes, deps, rules


def analyze(filename: str, content: str) -> AnalysisResult:
    language = detect_language(filename, content)
    if language == "cobol":
        nodes, deps, rules = _cobol(content)
        parser = "COBOL lexical parser (ANTLR-compatible fallback)"
    elif language == "fortran":
        nodes, deps, rules = _fortran(content)
        parser = "Fortran lexical parser (Tree-sitter-compatible fallback)"
    elif language == "pli":
        nodes, deps, rules = _pli(content)
        parser = "PL/I lexical parser (ANTLR-compatible fallback)"
    else:
        nodes, deps, rules, parser = [], [], [], "language detector"
    warnings = []
    if language == "unknown":
        warnings.append("Linguagem não reconhecida; informe uma extensão suportada.")
    if not rules:
        warnings.append("Nenhuma regra de negócio financeira foi identificada nesta amostra.")
    if not nodes:
        warnings.append("Nenhuma rotina estrutural foi identificada.")
    complexity = len(re.findall(r"(?im)\b(IF|ELSE|DO|PERFORM|EVALUATE|COMPUTE|CALL)\b", content))
    score = max(0, min(100, 45 + len(nodes) * 8 + len(rules) * 12 - complexity * 2))
    recommendations = []
    if deps:
        recommendations.append(Recommendation(priority="high", title="Isolar integrações externas", rationale="Dependências detectadas devem virar portas/adapters antes da conversão.", target="arquitetura"))
    if rules:
        recommendations.append(Recommendation(priority="high", title="Criar testes de caracterização", rationale="Preserve as regras financeiras identificadas antes de alterar a implementação.", target="regressão"))
    recommendations.append(Recommendation(priority="medium", title="Nomear regras como casos de uso", rationale="Extraia cálculos e condições para serviços de domínio com nomes explícitos.", target="modernização"))
    return AnalysisResult(filename=filename, language=language, parser=parser, lines=len(content.splitlines()), score=score, nodes=_unique(nodes), dependencies=_unique(deps), rules=_unique(rules), recommendations=recommendations, metrics={"routines": len(nodes), "dependencies": len(deps), "business_rules": len(rules), "conditional_blocks": complexity, "documentation_coverage": min(100, 30 + len(rules) * 15)}, warnings=warnings)

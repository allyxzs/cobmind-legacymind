# CobMind: LegacyMind

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![COBOL](https://img.shields.io/badge/COBOL-Modern%20Parser-orange.svg)](https://www.opencobol.org)
[![Fortran](https://img.shields.io/badge/Fortran-Frontend-green.svg)](https://gcc.gnu.org/fortran)
[![PL/I](https://img.shields.io/badge/PL/I-Parser-purple.svg)](https://github.com/pliDev/pli)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20DB-blue.svg)](https://neo4j.com)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)](https://react.dev)
[![Tree-sitter](https://img.shields.io/badge/Tree-sitter-Parsers-teal.svg)](https://tree-sitter.github.io)
[ANTLR](https://img.shields.io/badge/ANTLR-Parser-red.svg)

---

## Visão Geral

**CobMind** (nome da marca) / **LegacyMind** (nome do projeto) é uma plataforma moderna para modernização de sistemas legados. Grandes empresas frequentemente possuem sistemas antigos (COBOL, Fortran, PL/I) cuja documentação original desapareceu ao longo das décadas e cuja manutenção depende de poucos profissionais especializados.

Nosso objetivo é usar **análise estática** e **inteligência artificial** para:

1. **Compreender** a estrutura e o fluxo desses sistemas
2. **Documentar** automaticamente regras de negócio e dependências
3. **Auxiliar** na conversão para linguagens modernas (Java, Python)
4. **Identificar** impactos de mudanças antes de aplicá-las

---

## Funcionalidades Principais

| Funcionalidade | Descrição |
|:---|:---|
| **Análise de Código** | Parsers para COBOL, Fortran e PL/I usando ANTLR e Tree-sitter |
| **Extração de Regras de Negócio** | Identificação de lógica financeira, cálculo de juros, classificação de clientes |
| **Mapeamento de Dependências** | Grafo de dependências entre módulos, arquivos e dados (Neo4j) |
| **Identificação de Fluxos Financeiros** | Detecção de padrões de transação, cálculo de limites de crédito, juros compostos |
| **Geração Automática de Documentação** | READMEs técnicos, diagramas mermaid, manuais de usuário |
| **Sugestões de Conversão** | Mapeamento COBOL→Java, Fortran→Python, PL/I→TypeScript |
| **Testes de Regressão** | Geração de testes unitários baseados em comportamento observado |
| **Comparação Comportamental** | Diff entre versões antigas e novas do mesmo sistema |
| **Análise de Impacto de Mudanças** | Efeito de alterações em um módulo sobre o restante do sistema |
| **Assistente de IA Especializado** | Chat com contexto do código analisado, sugestões de refatoração |

---

## Arquitetura do Sistema

```mermaid
graph TD
    A[Fontes Legadas] -->|COBOL/Fortran/PL/I| B[Parser ANTLR/Tree-sitter]
    B -->|AST Structured| C[Database Neo4j]
    C -->|Grafo de Dependências| D[Motor de Análise]
    D -->|Regras/Fluxos| E[AI Assistant (Claude)]
    E -->|Sugestões| F[Outputs: Java/Python/Tests]
    F -->|Código Moderno| G[Sistema Modernizado]
    
    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#e3f2fd,stroke:#333,stroke-width:2px
    style C fill:#e8f5e9,stroke:#333,stroke-width:2px
    style D fill:#fff3e0,stroke:#333,stroke-width:2px
    style E fill:#f3e5f5,stroke:#333,stroke-width:2px
    style F fill:#e0f7fa,stroke:#333,stroke-width:2px
    style G fill:#c8e6c9,stroke:#333,stroke-width:2px
```

---

## Exemplos de Código Analisado

O projeto inclui amostras reais de sistemas legados para demonstração:

### COBOL: CUSTMSTR.cbl
Programa de cadastro de clientes com arquivos VSAM e cálculo de limite de crédito.

![COBOL Sample](samples/CUSTMSTR.cbl)

### Fortran: payroll.f90
Folha de pagamento com cálculo de INSS e IRRF por faixa salarial.

![Fortran Sample](samples/payroll.f90)

### PL/I: acctrec.pli
Contas a receber com cálculo de taxa e totalização.

![PL/I Sample](samples/acctrec.pli)

### COBOL: INTEREST.cbl
Cálculo de juros compostos e amortização de empréstimos.

![COBOL Interest](samples/INTEREST.cbl)

---

## Tecnologias Utilizadas

| Tecnologia | Papel no Projeto |
|:---|:---|
| **COBOL / Fortran / PL/I** | Linguagens de origem a serem analisadas |
| **ANTLR** | Geradores de parsers sintáticos |
| **Tree-sitter** | Parsers incrementais para linguagem |
| **Neo4j** | Banco de dados de grafo para mapeamento de dependências |
| **Python** | Lógica de backend, API, processamento |
| **Java** | Alvo de conversão para sistemas empresariais |
| **React** | Interface frontal para interação com a plataforma |
| **Mermaid** | Diagramas automáticos na documentação |
| **Chart.js** | Visualizações de métricas e fluxos |

---

## Como Executar (Local Development)

```bash
# 1. Clone o repositório (vazio)
git clone https://github.com/seu-usuario/cobmind-legacymind.git
cd cobmind-legacymind

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute a análise em um arquivo de exemplo
python -m cobmind.analyze samples/CUSTMSTR.cbl

# 4. Inicie a interface React
cd frontend && npm install && npm run dev
```

---

## Roadmap Planejado

- [x] Parsers iniciais para COBOL, Fortran, PL/I
- [x] Extração de regras de negócio financeira
- [x] Mapeamento básico de dependências
- [ ] Assistente de IA integrado com contexto semântico
- [ ]Conversor COBOL → Java funcional
- [ ]Conversor Fortran → Python funcional
- [ ] Interface web completa em React
- [ ] Exportação de relatórios em PDF/HTML
- [ ] Integração com CI/CD para análise de pull requests

---

## Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Contato

Para mais informações, visite nossa [documentação](https://cobmind.example.com) ou abra uma issue no repositório.
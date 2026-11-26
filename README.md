# CobMind: LegacyMind

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6.svg)](https://www.typescriptlang.org)
[![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20vitest-green.svg)](#testes-automatizados)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg)](#docker)

Plataforma de modernização de sistemas legados. Grandes empresas possuem sistemas antigos em COBOL, Fortran e PL/I cuja documentação desapareceu e cuja manutenção depende de poucos profissionais. O CobMind aplica análise estática para compreender, documentar e orientar a modernização dessas aplicações — com API REST, dashboard web e suíte de testes.

## O que está implementado

| Requisito | Status | Onde |
|:---|:---|:---|
| Backend Python + FastAPI | ✅ | `backend/app/main.py` |
| Frontend React 19 + TypeScript | ✅ | `frontend/src/` |
| Parsers COBOL / Fortran / PL/I | ✅ analisadores léxicos prontos para plugar ANTLR/Tree-sitter | `backend/app/analyzer.py` |
| Análise de código legado | ✅ rotinas, métricas e índice de analisabilidade | `backend/app/analyzer.py` |
| Mapeamento de dependências | ✅ SELECT/ASSIGN (arquivos) e CALL (programas) | `backend/app/analyzer.py` |
| Identificação de regras de negócio | ✅ heurísticas financeiras por linguagem, com evidência e confiança | `backend/app/analyzer.py` |
| Recomendações de modernização | ✅ priorizadas por análise | `backend/app/analyzer.py` |
| Dashboard de visualização | ✅ resultado completo, editor de fonte, amostras | `frontend/src/Dashboard.tsx` |
| API REST | ✅ 5 endpoints | `backend/app/main.py` |
| Testes automatizados | ✅ pytest (backend) + vitest (frontend) | `backend/tests/`, `frontend/src/*.test.ts` |
| Dockerfile + Docker Compose | ✅ api + web | `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` |
| Arquivos de dependências | ✅ | `backend/requirements.txt`, `frontend/package.json` |

## Arquitetura

```
┌────────────────────────┐        ┌─────────────────────────────┐
│  Frontend React + TS   │  HTTP  │  Backend FastAPI (Python)   │
│  Dashboard :5173       │ ─────► │  :8000                      │
│  · editor de fonte     │  JSON  │  · /api/v1/analyze          │
│  · seletor de amostras │ ◄───── │  · analyzer (COBOL/F90/PL/I)│
│  · painel de resultado │        │  · regras · deps · recos    │
└────────────────────────┘        └──────────────┬──────────────┘
                                                 │ lê
                                          ┌──────▼──────┐
                                          │  samples/   │
                                          │  .cbl .f90  │
                                          │  .pli       │
                                          └─────────────┘
```

Os analisadores são escritos como módulos independentes por linguagem (`_cobol`, `_fortran`, `_pli`) sobre uma camada comum de modelos Pydantic. Os hooks do ANTLR (`antlr4-python3-runtime`) e do Tree-sitter já estão nas dependências: os analisadores atuais servem como fallback determinístico e como contrato de saída (`AnalysisResult`) para quando os grammars gerados forem plugados.

## Funcionalidades em detalhe

**Análise de código** — detecta a linguagem pela extensão (`.cbl`, `.cob`, `.f`, `.f90`, `.pli`, `.pl1`) ou pelo conteúdo; extrai rotinas (parágrafos COBOL, PROGRAM/SUBROUTINE/FUNCTION Fortran, PROC PL/I) com linha de ocorrência.

**Regras de negócio** — heurísticas por linguagem flagram cálculos e condições que tocam valores financeiros (`LIMIT`, `RATE`, `TAX`, `BALANCE`, `INSS`, `IRRF`…), com categoria, confiança e a evidência literal do código.

**Dependências** — COBOL: `SELECT … ASSIGN TO` (arquivos) e `CALL` (programas); Fortran e PL/I: `CALL`. Cada aresta tem origem, destino, relação e linha.

**Recomendações** — priorizadas (alta/média/baixa): isolar integrações externas em adapters, criar testes de caracterização antes de mexer, nomear cálculos como casos de uso.

**Índice de analisabilidade** — nota de 0 a 100 combinando rotinas, regras e complexidade condicional, exibida num dial no dashboard.

**Dashboard** — editor de fonte com seletor de amostras (as quatro do acervo, carregadas via API), painel de resultado com métricas, regras, tabela de dependências, recomendações e avisos.

## API REST

| Método | Rota | Descrição |
|:---|:---|:---|
| GET | `/health` | Liveness + versão |
| POST | `/api/v1/analyze` | Analisa fonte no corpo JSON `{filename, content}` |
| POST | `/api/v1/analyze/file` | Analisa um arquivo enviado como `multipart/form-data` |
| GET | `/api/v1/languages` | Linguagens e extensões suportadas |
| GET | `/api/v1/samples/{id}` | Fonte de uma amostra (`custmstr`, `interest`, `payroll`, `acctrec`) |

Exemplo:

```bash
curl -s localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"filename": "CUSTMSTR.cbl", "content": "PROGRAM-ID. CUSTMSTR.\nCOMPUTE CUST-LIMIT = BALANCE * RATE."}'
```

Resposta (resumida):

```json
{
  "language": "cobol",
  "score": 73,
  "metrics": {"business_rules": 1, "routines": 1},
  "rules": [{"title": "Regra financeira detectada", "category": "credit", "confidence": 0.88}],
  "recommendations": [{"priority": "high", "title": "Criar testes de caracterização"}]
}
```

## Como rodar

### Com Docker (recomendado)

```bash
docker compose up --build
```

Dashboard: http://localhost:5173 · API: http://localhost:8000 · Docs interativos: http://localhost:8000/docs

### Local

Backend:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (outro terminal):

```bash
cd frontend
npm install
npm run dev
```

O Vite faz proxy de `/api` e `/health` para a porta 8000.

## Testes automatizados

```bash
cd backend && python -m pytest -v      # análise e API (TestClient)
cd frontend && npm test                # rótulos e catálogo de amostras (vitest)
```

## Estrutura do projeto

```
cobmind-legacymind/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI: rotas, CORS, amostras
│   │   ├── analyzer.py    # parsers léxicos + heurísticas por linguagem
│   │   └── models.py      # contratos Pydantic (AnalysisResult…)
│   ├── tests/             # pytest: analyzer + API
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── Dashboard.tsx  # UI completa (editor, amostras, resultado)
│   │   ├── api.ts         # cliente HTTP + catálogo de amostras
│   │   ├── types.ts       # tipos espelhando o contrato da API
│   │   ├── labels.ts
│   │   ├── styles.css
│   │   └── labels.test.ts # vitest
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── Dockerfile
├── samples/               # acervo legado de demonstração
│   ├── CUSTMSTR.cbl       # COBOL: clientes, VSAM, limite de crédito
│   ├── INTEREST.cbl       # COBOL: juros compostos
│   ├── payroll.f90        # Fortran: folha (INSS/IRRF)
│   └── acctrec.pli        # PL/I: contas a receber
├── docker-compose.yml
├── .gitignore
└── LICENSE
```

## Roadmap

- [x] Parsers léxicos COBOL / Fortran / PL/I com fallback determinístico
- [x] API REST + dashboard + testes + Docker
- [ ] Grammars ANTLR/Tree-sitter gerados substituindo o fallback
- [ ] Persistência do grafo de dependências no Neo4j
- [ ] Geração de testes de regressão a partir das regras extraídas
- [ ] Conversão assistida COBOL → Java e Fortran → Python
- [ ] Assistente de IA especializado no código analisado

## Licença

MIT — veja [LICENSE](LICENSE).

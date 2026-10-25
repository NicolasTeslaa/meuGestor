# Grafo de gestão de tráfego — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar uma base de conhecimento em grafo, consultável por chats do Codex, para decisões de Meta Ads em serviços B2B e B2C no Brasil.

**Architecture:** JSON versionado no Git armazena nós, relações e fontes. Um módulo Python da biblioteca padrão valida integridade e consulta vizinhos por ID, tipo e termo. `AGENTS.md` orienta o agente a usar o grafo e a checar fontes recentes antes de recomendar investimento.

**Tech Stack:** Python 3.9+, `json`, `argparse`, `unittest`, Markdown e JSON. Sem dependências externas.

**Spec:** `docs/superpowers/specs/2026-10-25-grafo-gestao-trafego-design.md`

## Global Constraints

- Prioridade: Meta Ads para serviços B2B e B2C no Brasil.
- Resultado de negócio prioritário: venda fechada e receita realizada.
- A primeira versão não conecta contas, não publica anúncios e não altera campanhas.
- Toda orientação factual deve trazer fonte, contexto de validade e data de verificação.
- Não estabelecer benchmarks universais de CPL, ROAS, frequência ou orçamento.
- Distinguir atribuição da plataforma de efeito incremental.

---

## File map

- `AGENTS.md`: contrato de resposta do agente para chats do Codex.
- `knowledge/graph.json`: nós e relações. Cada nó tem um ID estável; relações usam IDs existentes.
- `knowledge/sources.json`: fontes primárias e estudos originais, com URL, tipo e data de verificação.
- `knowledge/README.md`: ontologia, fórmulas e manutenção editorial.
- `scripts/graph.py`: carregamento, validação e busca no grafo.
- `tests/test_graph.py`: testes de comportamento da validação e da busca.
- `tests/test_corpus.py`: aceitação do corpus real via consultas e validação.
- `README.md`: início rápido e decisões que a base suporta.

### Task 1: Validação de fontes, nós e relações

**Files:** Create `scripts/graph.py`, `tests/test_graph.py`.

**Interfaces:** `load_graph(root: Path) -> tuple[dict, dict]`; `validate(graph: dict, sources: dict) -> list[str]`. IDs únicos; tipo, resumo, aplicabilidade e lista de fontes exigidos; relações apontam a IDs existentes; fontes têm URL HTTPS e `verified_at` ISO.

- [x] **Step 1: Write the failing test.** Testar `validate` com um grafo mínimo válido, depois IDs duplicados, relação órfã e referência a fonte ausente. Exemplo central:

```python
def test_rejects_orphan_edge(self):
    graph = {"nodes": [{"id": "metric.cpl", "type": "metric", "title": "CPL", "summary": "Custo por lead", "applies_to": ["b2b"], "sources": ["meta.leads"]}], "edges": [{"from": "metric.cpl", "relation": "measures", "to": "missing"}]}
    sources = {"sources": [{"id": "meta.leads", "url": "https://www.facebookblueprint.com/example", "verified_at": "2026-10-25", "kind": "official"}]}
    self.assertIn("missing", " ".join(validate(graph, sources)))
```

- [x] **Step 2: Run `python3 -m unittest tests.test_graph -v`; confirm expected failure from missing validator.**
- [x] **Step 3: Implement `validate` with explicit checks and deterministic errors; implement `load_graph` to read both JSON files.** No schema package.
- [x] **Step 4: Run `python3 -m unittest tests.test_graph -v`; confirm all green. Refactor repeated field checks, rerun.**

### Task 2: Consulta útil do grafo

**Files:** Modify `scripts/graph.py`; extend `tests/test_graph.py`.

**Interfaces:** `search(graph: dict, term: str, *, node_type: Optional[str] = None) -> list`; `neighborhood(graph: dict, node_id: str) -> dict` with keys `node`, `outgoing`, `incoming`; CLI `python3 -m scripts.graph validate|search|show`.

- [x] **Step 1: Write failing tests.** `search` must find `lead qualificado` by title/summary case-insensitively and filter type. `neighborhood` must return both incoming and outgoing relationships; unknown ID must fail clearly. Verify CLI validation separately with a malformed corpus fixture.

```python
def test_search_filters_type(self):
    graph = {"nodes": [{"id": "metric.qualified_lead", "type": "metric", "title": "Lead qualificado", "summary": "Vendas", "applies_to": ["b2b"], "sources": []}, {"id": "stage.qualified_lead", "type": "stage", "title": "Lead qualificado", "summary": "Etapa", "applies_to": ["b2b"], "sources": []}], "edges": []}
    self.assertEqual(["metric.qualified_lead"], [n["id"] for n in search(graph, "lead qualificado", node_type="metric")])
```

- [x] **Step 2: Run `python3 -m unittest tests.test_graph -v`; confirm expected missing behavior.**
- [x] **Step 3: Implement search, neighborhood and CLI with `argparse`; print JSON for `search`/`show`.**
- [x] **Step 4: Run tests and CLI validation; refactor only after green, then rerun.**

### Task 3: Corpus inicial rastreável

**Files:** Create `knowledge/graph.json`, `knowledge/sources.json`, `knowledge/README.md`, `tests/test_corpus.py`.

**Interfaces:** At least 45 nodes across business outcome, funnel, metrics, campaign setup, signals, diagnoses, actions and experiments; at least 65 meaningful edges; at least 8 verified primary or original-study sources. Every factual node cites a source. Formula nodes state numerator, denominator, unit and period. Conditional decision nodes do not assert universal thresholds.

- [x] **Step 1: Write failing corpus tests.** Load the real corpus through `load_graph`, assert `validate(...) == []`, search for `receita`, `lead qualificado`, `incrementalidade` and `capacidade de atendimento`, then inspect a decision path from CPL to receita and from platform attribution to lift. Assert that each formula has explicit numerator and denominator.

```python
def test_cpl_connects_to_revenue(self):
    graph, sources = load_graph(ROOT)
    self.assertEqual([], validate(graph, sources))
    self.assertTrue(any(n["id"] == "outcome.revenue" for n in search(graph, "receita")))
    self.assertTrue(neighborhood(graph, "metric.cpl")["outgoing"])
```

- [x] **Step 2: Run `python3 -m unittest tests.test_corpus -v`; confirm expected missing-file failure.**
- [x] **Step 3: Research and add source metadata, then create curated nodes and relations.** Cover the approved acceptance cases; keep source-specific claims separate from operator heuristics; annotate heuristics as `inference`.
- [x] **Step 4: Run all tests and `python3 -m scripts.graph validate`; inspect search/show output. Refactor wording and duplicate nodes without changing IDs, then rerun.**

### Task 4: Agent instructions and onboarding

**Files:** Create `AGENTS.md`, `README.md`; update `knowledge/README.md` if needed.

**Interfaces:** Codex response process: identify decision and missing business data; query graph; verify current unstable claims on web; separate facts, calculations and hypotheses; cite sources; recommend conditional next action. No claims of causal lift from attributed ROAS.

- [x] **Step 1: Write a manual acceptance matrix before instructions.** Use six spec cases: cheap CPL, instant form vs site, high Meta ROAS without cash growth, 90-day B2B cycle, saturated B2C service team, stale feature source. For each, write expected decision and forbidden shortcut in `knowledge/README.md`.
- [x] **Step 2: Run the CLI on the nodes required by each case and inspect the graph paths for missing coverage.**
- [x] **Step 3: Complete missing paths, then write `AGENTS.md` and concise `README.md` with exact CLI commands and response template.**
- [x] **Step 4: Run corpus tests, CLI validation and route checks for all six manual scenarios. Record observed outputs and fix unsupported claims.**

## Final verification

Run `python3 -m unittest discover -s tests -v`, `python3 -m scripts.graph validate`, `git diff --check`, and inspect `git diff` plus `git status`. Check spec coverage line by line. Confirm whether `.github/workflows/*.yml` or `*.yaml` exists; if absent, commit task files and push configured branch after reviewing the staged diff. Report test counts, commit hash and push result.

---
name: targeted-company-research
description: >-
  Generate source-backed targeted company research reports for B2B sales, ABM,
  competitor analysis, partner research, and light diligence. Use when the user
  asks for company research, enterprise deep dive, customer research, competitor
  research, ABM preparation, company profile, targeted research, or a multi-source
  report about a named organization.
license: MIT
---

# Targeted Company Research

Turn a named company into a source-backed business map: who it is, what it sells,
where it competes, who it sells to, how it goes to market, and where the entry
points are. Output is consulting-grade — every material claim carries a source
mark, and findings are pushed from fact → insight → action.

> 把一个目标公司做成有来源、可验证的业务地图，达到咨询报告质量。

## How To Read This Skill

One file, one job. Don't duplicate across files.

| File | Answers | Read when |
|---|---|---|
| `SKILL.md` (this) | What's the flow? What does the report look like? | Always, first |
| `references/platform-capabilities.md` | How do I run search / fetch / sub-agents on THIS platform? | Before executing |
| `references/search-strategy.md` | How do I search without stalling? | Before collecting sources |
| `references/analysis-frameworks.md` | How do I analyze, not just collect? | Before writing each task |
| `references/task-packs.md` | What exactly do I search for per task? | When running a task |

## Trigger

Use this skill when the user asks for:

- Company research, company profile, enterprise deep dive, customer research, competitor research.
- ABM sales prep, partner research, supplier research, market-entry account research.
- A report on a specific named company, subsidiary, brand, competitor, buyer, distributor, or investment target.

Don't use this for broad industry/market reports without a named target company.
*(A market/industry research mode is on the roadmap — see Roadmap. For now, route market-only requests to a market research workflow.)*

## Phase 0: Scope Lock (Gate)

**Minimal intake**: only two inputs are required to start — the **company name** and the
**purpose**. Everything else is inferred and marked with confidence per the defaults table
below; never block the run waiting for fields the user didn't give. *(Minimal two-question
intake adopted from dazhiruoyu — lower the barrier to start.)*

Before any deep research, confirm and present a one-line scope summary, then proceed:

- Official domain and legal entity (avoid same-name collisions).
- HQ city/country and **home language** of the target market (drives non-English search).
- Parent/subsidiary relationships.
- **Target type**: manufacturer / distributor / SaaS / brand — this sets search emphasis (see `search-strategy.md`).
- Purpose (ABM / competitor / partner / supplier / diligence) and output language.
- Depth: light / standard / deep.

Stop and ask only when two companies plausibly match the same name. Otherwise infer conservatively and mark uncertain fields.

| Field | Default if missing |
|---|---|
| Website | find from public search |
| Industry | infer, mark confidence |
| Geography | global + HQ country |
| Purpose | general business research |
| Language | user's language |
| Depth | standard |

## Phase 1: Project Setup

Create the skeleton before research (templates in `task-packs.md`):

```text
projects/{project_slug}/
├── task_plan.md          # scope, target type, depth, run mode, source targets
├── task_status.md        # updated after each task
├── task1_company/  (task_instructions.md + task1_company.md)
├── task2_product/
├── task3_industry/
├── task4_channel/
├── task5_marketing/
├── sources/source_index.md
├── evidence/             # browser_notes.md and saved evidence
└── FINAL_REPORT.md
```

Generate one `task_instructions.md` per task from `task-packs.md`.

## Phase 2: Execute (5 Evidence Chains)

Five tasks, each an evidence chain + an analysis lens:

| Task | Focus | Analysis lens | Min search | Min fetch | Source target |
|---|---|---|---:|---:|---:|
| 1 | Company fundamentals & history | Company anatomy | 12 | 8 | 12 |
| 2 | Products, technology, certs | Value-chain position | 12 | 8 | 12 |
| 3 | Industry & competitors | Five Forces + positioning | 12 | 8 | 10 |
| 4 | Customers, channels, supply chain | Channel map + procurement | 12 | 8 | 12 |
| 5 | Marketing, events, people, ABM | Decision-maker map + So-What | 14 | 8 | 12 |

**Run mode** — pick by platform capability (`platform-capabilities.md`):

- **Sub-agents available** (Claude Task / Codex workers / OpenClaw sessions): assign one task per sub-agent. This is the default for capable platforms — it's the execution layer earlier packaging lost. Forbid workers from reading other task folders until merge.
- **No sub-agents**: run Task 1→5 sequentially in the main loop. Same output, slower.

Either way, dependencies flow forward *(adopted from mckinsey-research batch ordering)*: later tasks may reference earlier confirmed findings; the final synthesis depends on all five.

For each task:
1. Write 3-5 **hypotheses** to confirm/falsify (hypothesis-driven, not collect-everything).
2. Run the search loop with stop conditions (`search-strategy.md`) — this is what prevents runaway, stalling research.
3. Apply the task's analysis framework (`analysis-frameworks.md`).
4. Update `task_status.md`: status, source count, fetch/browser count, major findings, gaps.

Depth controls:

| Depth | Tasks | Total source target |
|---|---|---:|
| light | 5 compressed | 20-30 |
| standard | 5 full | 55-70 |
| deep | 5 + second expansion loop | 70+ |

## Phase 3: Synthesize & Deliver

1. Read all five task outputs.
2. Run an **executive synthesis** *(adopted from mckinsey-research master prompt)*:
   - Lead with conclusions, not "we researched from multiple angles."
   - For ABM/diligence purposes, present strategic angles + recommended next actions.
3. Run the **MECE + So-What quality gate** (`analysis-frameworks.md`) on findings.
4. Write `FINAL_REPORT.md` (structure below). Keep two layers: synthesized body + full task appendix.
5. Optional: export to PDF via `scripts/generate_pdf.py` *(thanks to dazhiruoyu)* when the user wants a polished deliverable.

## Report Structure (authoritative — defined once, here)

```markdown
# {Company} Targeted Company Research Report

> Research date: {date} · Purpose: {purpose} · Confidence: high/medium/low

## Executive Takeaways
5-8 specific, sourced findings. Each: object → judgment → evidence.

## Part 1: Company Fundamentals & Products
### 1. Company Fundamentals      (ownership, history, leadership, scale, compliance)
### 2. Products & Technology      (lines, specs, certs, pricing, reviews)

## Part 2: Market, Channel & ABM
### 3. Industry & Competitors     (market context, competitor matrix, Five Forces, positioning)
### 4. Customers, Channels & Supply Chain
### 5. Marketing, Events & ABM Entry Points

## Strategic Synthesis            (3 angles + recommended actions; for ABM/diligence)

## Data Gaps                      (explicit: 缺少数据：...; banner + struck-through fields — see analysis-frameworks.md Data-Gap Governance)

## Appendix: Full Task Reports    (complete Task 1-5 text, preserved for audit)

## Sources                        (deduplicated index with tiers)
```

Preserve all original numbers, years, names, platforms, source names, product names, and representative quotes. The body is synthesized; the appendix keeps raw task depth.

## Source Ladder

| Tier | Sources | Use |
|---|---|---|
| T0 | regulatory, filings, court, customs, patent, certification DB, official registry | high-confidence facts |
| T1 | official site/PDF, investor pages, product docs, press releases, official social | company claims, product facts |
| T2 | industry associations, trade shows, distributors, marketplaces, credible media | market & channel evidence |
| T3 | lead databases, estimates, scraped profiles, review aggregators | estimates only — label as such |

Every material claim → `[Sxx]` resolving to `sources/source_index.md`. Unsourced numbers → `待核实` / `estimate`.

## Quality Gates (before delivery)

Run this as a mechanical gate, not a soft checklist *(adopted from UZI-Skill's
critical-check gate)*. Each check is **critical** or **warning**:

- **critical** — if it fails, the report does **not** ship. Fix it or explicitly mark
  the affected claim as a data gap, then re-run the gate. A failed critical check is a
  hard stop, not a note to the reader.
- **warning** — log it at the top of the report and proceed; the reader is told.

> 机械级闸门，不是软清单：critical 不过物理上不出报告（学 UZI 的 critical-check gate）。

| # | Check | Level |
|---|---|---|
| 1 | Official identity locked; not confused with same-name companies. | critical |
| 2 | No fabricated numbers — every numeric table row has a source mark or `待核实`. | critical |
| 3 | No private credentials, cookies, tokens, or personal contact guesses. | critical |
| 4 | Empty evidence chains reconciled against `search_log.md` — `搜索失败·未核实` not read as a confirmed negative (`search-strategy.md`). | critical |
| 5 | Missing data explicit (`缺少数据：...` / `data_gap_acknowledged`), never silently dropped. | critical |
| 6 | Sources deduplicated by canonical URL; each has a tier. | warning |
| 7 | Confirmed facts separated from estimates and inferences. | warning |
| 8 | MECE check on competitor matrix, weaknesses, channels — no overlap, no gap (`analysis-frameworks.md`). | warning |
| 9 | Every major finding passes So-What (fact → insight → implication). | warning |
| 10 | Raw task files preserved in appendix. | warning |

If any **critical** check cannot be satisfied even after marking a data gap (e.g. identity
genuinely cannot be locked), stop and tell the user — do not ship a report that reads as
authoritative on an unverified foundation.

## Data Boundary & Ethics

Supports legitimate public business research and user-authorized sessions only.
**Allowed**: public business names, roles, company, official profile URLs, public
speaking/event references, official contact channels.
**Not supported**: bypassing login/paywall/captcha/access controls, private system
data, private email/phone guessing, bulk personal contact harvesting, leaked
credentials/cookies/tokens.

## Roadmap

A market/industry research mode is planned (the architecture already supports it —
both modes share `analysis-frameworks.md`). See [`ROADMAP.md`](../ROADMAP.md) at the
repo root for the full plan.

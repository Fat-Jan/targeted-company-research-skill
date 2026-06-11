# Roadmap

This skill ships today as **Mode A: Targeted Company Research** — a deep, source-backed
dossier on one named company. The architecture is deliberately built so a second mode
can be added without a rewrite.

> 当前发布的是「模式 A：定向公司调研」。文件结构是为双模式预留的，加模式 B 不需要重构。

## Planned: Mode B — Market / Industry Research

**Question it answers**: "Is this market worth entering, and how?" — as opposed to
Mode A's "who is this specific company?"

源自调研中对比的 cowagent `mckinsey-research` 与腾讯 `dazhiruoyu`，二者都是「市场/赛道」视角，
与本 skill 的「公司」视角互补。模式 B 把那条视角补齐。

### Why it slots in cleanly

The analysis layer is already **mode-agnostic**. These pieces are shared, not rebuilt:

| Shared asset | Mode A use | Mode B use |
|---|---|---|
| `analysis-frameworks.md` | Five Forces, SWOT, positioning on one company | TAM/SAM/SOM, market attractiveness, entry strategy on a market |
| `platform-capabilities.md` | same SEARCH/FETCH/SUBAGENT/WRITE map | unchanged |
| `search-strategy.md` | feedback loop + stop conditions | unchanged |
| `scripts/generate_pdf.py` | company report → PDF | market report → PDF |

Only two things are genuinely new for Mode B:

1. **An entry router** — classify the request as company-target vs market-target,
   then dispatch to the right task pack.
2. **A market task pack** (e.g. `task-packs-market.md`) — the market-research
   equivalent of the five company evidence chains: market sizing, demand/users,
   competitive structure, business models, regulation/tech trends, entry decision.

### Design constraint: don't reintroduce "头晕"

Two modes must not double the cognitive load. The same single-job-per-file rule holds:

- One **entry router** picks the mode; the user never reads both packs.
- Shared analysis/search/platform layers stay shared — no fork, no duplication.
- Each mode has exactly one task pack file; `SKILL.md` routes, it doesn't repeat.

If adding Mode B would force a reader to hold both modes in their head at once,
the split is wrong — re-route at the entry instead.

## Other candidates (unprioritized)

- HTML report export alongside PDF (cowagent ships an HTML template).
- A localized data-source pack for China-market research (艾瑞 / QuestMobile / 财报),
  adapted from `dazhiruoyu`.
- A short worked example / sample report in `examples/`.

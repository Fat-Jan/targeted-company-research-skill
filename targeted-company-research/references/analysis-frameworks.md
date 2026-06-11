# Analysis Frameworks

This file turns collected evidence into consulting-grade judgment. The original skill stopped at *facts*; this layer adds *insight → implication → action*.

> 这是方法论层。它独立于"调研对象是公司还是市场"——公司模式和未来的市场模式共用同一批框架。每个框架配：角色设定、何时用、输出什么。不强制全用，按需调用。

## Operating Backbone (applies to the whole report)

Three habits make the difference between a data dump and a consulting deliverable:

### 1. Key Question + Issue Tree

Before research, write ONE key question driven by the research purpose:

- ABM purpose → *"What pain or gap makes {company} most likely to accept our partnership / purchase?"*
- Competitor purpose → *"Where is {company} most vulnerable, and can we win there?"*
- Diligence purpose → *"What would make this company a bad partner / target, and is it true?"*

Then decompose it MECE (mutually exclusive, collectively exhaustive) into sub-questions. Every task and every search must answer "which node of the tree does this serve?" — this is what keeps research focused and stops runaway searching.

### 2. Hypothesis-Driven Search

Each task starts with 3-5 testable hypotheses, e.g. *"{company}'s lithium transition lags the market."* Search to **confirm or refute**, not to collect aimlessly. A refuted hypothesis is a finding, not a failure.

### 3. So-What Chain

Every material finding must climb the ladder: **fact → insight → implication → action**. A fact with no "so what" does not belong in the executive body (it can stay in the appendix).

```
Fact:        UPG has no blog, no whitepapers, empty social.
Insight:     Zero content-marketing investment for a $530M company.
Implication: Competitors can capture UPG's buyers via SEO/content.
Action:      Lead ABM outreach with a technical content angle.
```

### 4. MECE Quality Gate

Before delivery, check every list (competitors, weaknesses, channels, risks): no overlaps, no gaps. Merge overlapping items, name missing categories.

## Framework Toolbox

Each framework names the analyst role to adopt (role-play sharpens output), when to use it, and the required output. Invoke only the ones the report needs.

### Porter's Five Forces — industry structure

- **Role:** Harvard Business School strategy professor.
- **When:** Industry/competitor task; assessing how attractive the market is.
- **Output:** Rate each force 1-10 with evidence — supplier power, buyer power, competitive rivalry, threat of substitution, threat of new entry — plus an overall industry attractiveness score and what it means for the target.

### SWOT + Cross-Strategy — internal vs external

- **Role:** Senior strategy consultant.
- **When:** Positioning the target; synthesizing fundamentals + market.
- **Output:** Strengths / Weaknesses (internal, with evidence) and Opportunities / Threats (external). Then cross-analyze: SO moves (strength × opportunity) and WT risks (weakness × threat). Plain SWOT lists without the cross-analysis are not enough.

### Value Chain — where value and cost sit

- **Role:** Operations strategist.
- **When:** Supply chain / channel task.
- **Output:** Map the chain (sourcing → manufacturing/assembly → distribution → channel → end customer). Mark where the target actually adds value vs. where it's a pass-through, and where margin pools and dependencies concentrate.

### Competitor Matrix + Threat Rating — the competitive set

- **Role:** Competitive intelligence analyst.
- **When:** Every competitor analysis.
- **Output:** ≥5 competitors with revenue, positioning, strengths, weaknesses, recent moves, and a low/medium/high threat rating each. Add a positioning map (e.g. integration level × customer value) and white-space gaps no one fills.

### Customer / Buyer Analysis — who buys and why

- **Role:** Customer research expert.
- **When:** Customer/channel task; ABM targeting.
- **Output:** Buyer segments, decision criteria, trigger events, objections, and (for ABM) the public decision-maker map with role + public source URL. No private contact guessing.

### Risk Matrix + Scenarios — what could go wrong

- **Role:** Risk management partner.
- **When:** Diligence purpose; any "should we commit" decision.
- **Output:** Risks across market / operational / financial / regulatory / reputational, each with probability × impact score and a mitigation. Plus best / base / worst case scenarios with the strategic response to each.

### Executive Synthesis — the master view

- **Role:** Senior partner presenting to a CEO.
- **When:** Always, at the end, after all tasks merge.
- **Output:**
  - Executive summary readable in 2 minutes.
  - Honest current-state assessment.
  - 3 strategic options (conservative / balanced / aggressive) with outcome, cost, timeline, risk.
  - One recommended option with reasoning.
  - Top 5 priority actions for the next 90 days, ranked.
  - "If I only had 1 hour" — the single most important insight and action.

## Adaptive Emphasis

Don't apply every framework with equal weight. Match emphasis to what the target actually is — this saves effort and sharpens the report.

| Target type | Lead frameworks | Light / skip |
|---|---|---|
| Manufacturer / factory | Value chain, product/cert depth, Five Forces | marketing depth |
| Distributor / trader | Channel map, competitor matrix, customer analysis | own-tech depth |
| SaaS / software | Competitor matrix, pricing, customer analysis | supply chain, customs |
| Brand / consumer goods | Channel + marketplace, customer analysis, marketing | patents |

Decide the target type during the identity-lock gate, then allocate analysis effort accordingly.

## Evidence Discipline (shared with search-strategy.md)

- Every material claim carries a source mark `[Sxx]` resolving to the source index.
- Label estimates and inferences explicitly: `estimate`, `待核实`, or "inferred from …".
- State missing data plainly: `缺少数据：…`. Never fabricate to fill a framework cell.
- Separate confirmed facts from analyst inference everywhere.

## Data-Gap Governance (mechanism, not slogan)

"Don't fabricate" is only a slogan until missing data is *tracked and surfaced*. Turn every
gap into a tracked item, not a silently dropped cell *(adopted from UZI-Skill's `_data_gaps`)*:

1. **Log each gap with a recovery action.** When a required field can't be confirmed, record
   it — the field, why it's missing (not found / search errored / behind login), and the
   *suggested recovery action* (which registry, which page, which filing would have it).
2. **Acknowledge, don't hide.** If the gap can't be closed within budget, mark it
   `data_gap_acknowledged` rather than leaving the cell blank or guessing. An acknowledged
   gap is a finding; a blank cell is a hole the reader can't see.
3. **Surface it in the report.** Two rendering conventions the PDF script supports:
   - **Top banner** — lead the report with a gap banner using a `⚠️` blockquote:
     `> ⚠️ 数据缺口：营收未能核实（建议：查 SEC filing / 官网投资者页）。`
     The PDF renderer paints `> ⚠️ …` as an orange banner.
   - **Struck-through field** — wrap an unconfirmed inline value in `~~…~~`:
     `营收 ~~$530M 待核实~~` renders struck-through, so a missing number is visually
     distinct from a confirmed one.

This ties to the search-strategy delivery gate: an empty chain that *errored* must read as
`搜索失败·未核实`, never as a confirmed negative.

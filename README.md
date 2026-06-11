# Targeted Company Research Skill

A platform-neutral skill that turns a **named target company** into a source-backed,
consulting-grade business map — for B2B sales, ABM, competitor analysis, partner/supplier
research, and light diligence.

> 把一个目标公司做成有来源、可验证的业务地图，达到咨询报告质量。支持 Claude / Codex / OpenClaw(龙虾) / Hermes。

## What It Produces

A local-first project folder with five evidence chains, merged into one report:

```text
projects/{slug}/
├── task_plan.md / task_status.md
├── task1_company/ … task5_marketing/   # 5 evidence chains
├── sources/source_index.md
├── evidence/
└── FINAL_REPORT.md                       # synthesized body + full task appendix
```

`FINAL_REPORT.md` covers company fundamentals, products & technology, industry &
competitors, customers/channels/supply chain, and marketing/events/ABM entry points —
every material claim carries a source mark, findings run fact → insight → action, and a
strategic synthesis leads with conclusions.

## What Changed In This Fork (重构说明)

This fork rebuilds the skill from a *methodology document* into an *executable, cross-platform unit*:

1. **Added the missing execution layer.** The original skill said *what to do* but not *how to
   run search / fetch / sub-agents on a given platform* — the part lost when OpenClaw's
   sub-agent execution was packaged. See `references/platform-capabilities.md`.
2. **Added a consulting-grade analysis layer.** Five Forces, SWOT, value-chain, positioning
   matrix, MECE check, and So-What — so the report analyzes, not just collects. See
   `references/analysis-frameworks.md`.
3. **Fixed runaway/stalling search.** Feedback-loop search with explicit stop conditions and
   per-task budgets. See `references/search-strategy.md`.
4. **De-duplicated the docs.** One file, one job — search seeds, report structure, and
   execution model each defined in exactly one place (was triplicated, "看的头晕").
5. **Truly cross-platform.** Install + invocation documented per platform below; no hard-coded
   Codex paths.

## File Structure

```text
ROADMAP.md                                # Mode B (market research) plan — shared layers, no rewrite
targeted-company-research/
├── SKILL.md                              # flow + report structure + quality gates (read first)
├── agents/openai.yaml                    # Codex interface config
├── references/
│   ├── platform-capabilities.md          # how to run capabilities on your platform + sub-agent orchestration
│   ├── search-strategy.md                # how to search without stalling (stop conditions, type-adaptive, native-language)
│   ├── analysis-frameworks.md            # how to analyze (consulting frameworks, mode-agnostic)
│   └── task-packs.md                     # what to search per task (seeds + output checklist)
└── scripts/
    ├── generate_pdf.py                   # optional Markdown→PDF export (data-gap banner, CJK layout)
    └── requirements.txt                  # reportlab
```

## Install & Use

### Claude (Claude Code)

Copy `targeted-company-research/` into your skills directory (`~/.claude/skills/` or a project
`.claude/skills/`), or point Claude at `targeted-company-research/SKILL.md` directly.

```text
Use targeted-company-research to research Universal Power Group for ABM sales prep.
Output in Chinese. Focus on products, distributors, competitors, and public decision makers.
```

Capabilities map to `WebSearch` / `WebFetch` / Playwright-or-Chrome MCP / `Task` sub-agents / `Write`.

### Codex

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Fat-Jan/targeted-company-research-skill \
  --path targeted-company-research \
  --method git
```

Restart Codex, then:

```text
Use $targeted-company-research to research {company}. 重点看产品线、渠道、竞品和 ABM 切入点，
输出中文 Markdown 报告，保留来源标注和数据缺口。
```

### OpenClaw (龙虾) / Hermes / other agents

Copy `targeted-company-research/` into the agent's skills directory, or have it read
`SKILL.md`. The agent needs equivalent capabilities (search, fetch, optional browser/CDP,
optional sub-agent spawn, file write) — `references/platform-capabilities.md` maps each one
and documents the **sub-agent orchestration** (one worker per task) that the original
packaging dropped.

No sub-agents? The skill runs all five tasks sequentially with identical quality — only slower.

## Data Boundary & Ethics

Legitimate public business research and user-authorized sessions only. Allowed: public
business names, roles, official profile URLs, public event references, official contact
channels. Not supported: bypassing login/paywall/captcha/access controls, private system
data, private email/phone guessing, bulk personal-contact harvesting, leaked credentials.

## Roadmap

- **Market/industry research mode** — a second mode answering "is this market worth entering?"
  (TAM/SAM/SOM, market attractiveness, entry strategy), reusing the shared analysis layer.
  The current single-responsibility file structure is built so this can be added without a
  rewrite. 双模式（公司调研 + 市场调研）共用方法论层，互不"看的头晕"。

## Acknowledgments (鸣谢)

This fork absorbed ideas from prior work:

- **McKinsey / Bain / Porter public methodologies** — MECE, issue trees, hypothesis-driven
  analysis, Five Forces, SWOT, So-What synthesis.
- **[`mckinsey-research`](https://clawhub.ai/abdullah4ai/mckinsey-research)** by *abdullah4ai*
  (MIT) — modular analyst-role prompts, batch dependency ordering, adaptive-stage logic, and
  the executive synthesis (3 strategic options + 90-day actions) pattern.
- **[`dazhiruoyu`](https://skillhub.cloud.tencent.com/skills/dazhiruoyu)** (Tencent SkillHub) by
  *user_99a25c17* — structured 12-chapter market framework, the Markdown→PDF export approach,
  and the minimal two-question intake.
- **`UZI-Skill`** by *FloatFu-true* (MIT) — search-resilience discipline (hard timeouts,
  fail-to-empty, leave-a-trace logging), trusted-domain `site:` injection, and noise filtering.
- **`Agent-Reach`** by *Panniantong* (MIT) — the keyless Jina Reader web-fetch fallback and the
  "doctor" pre-flight capability probe.

## License

MIT License. See [LICENSE](LICENSE).

# Search Strategy

How to find evidence efficiently and know when to stop. This file owns the *search method*. What to search for (per-task seeds) lives in `task-packs.md`. How to analyze what you find lives in `analysis-frameworks.md`.

> 搜索方法层。核心改进：从"关键词清单"变成"带反馈、有停止条件的检索循环"——这是原 skill 搜索容易跑飞 / 卡死的根因（只有下限指标，没有上限和边际停止）。

## The Search Loop (not a checklist)

The original skill handed out static query lists. Replace that with a feedback loop. After each search pass on a task line, answer three questions:

1. **Coverage** — are the core fields for this evidence chain filled?
2. **New seeds** — did new entities surface (new product model, executive, subsidiary, competitor, distributor)?
3. **Gaps** — is there a clear, nameable gap left?

New seeds → run an expansion pass. No gaps and coverage met → stop this line. Search is **result-driven**, not list-driven.

## Stop Conditions and Budget (this prevents runaway / hang)

Every task line has two gates:

- **Hard cap:** search calls ≤ N per task line (default 15; light depth 8, deep 20).
- **Marginal stop:** 2 consecutive searches that surface no new source and no new seed → this line is done.

The original skill only had *lower* bounds ("target 12+ sources"), which is why an agent — or a sub-agent — could search until it stalled. The cap and marginal-stop are the upper bounds.

> 给子代理派活时，这两个闸门必须写进 worker 指令。无上限的 worker 是卡死的主因。

## Resilience: Timeout, Failure, Trace (don't crash, don't go silent)

A networked search must not hang the whole study, and a failed search must not be mistaken for "nothing found." Three rules:

1. **Hard timeout per call.** Every search/fetch call gets an explicit timeout (≈10s for search, ≈15s for a page fetch). On most platforms the underlying HTTP client has *no* default timeout, so a dead proxy or blocked domain can stall a call for 60s+. A call that exceeds the timeout returns empty and the line moves on.
2. **Degrade, don't raise.** One failed query never aborts the run — return empty for that query and keep the other lines going. Resilience beats completeness when a single source is down.
3. **Leave a trace.** A failure is *logged*, not swallowed. Record which query failed and why (timeout / blocked / zero results) in the search log. This is the difference between "this fact genuinely doesn't exist" and "the search errored and nobody noticed."

> 这套来自 UZI-Skill 的搜索层（硬超时 + 失败转空 + 不抛异常）。学它的韧性，但补它的坑——它把错误对象混进正常结果不剔除。我们的纪律是**失败必须留痕**：

```markdown
# evidence/search_log.md — append one line per failed/empty query
| Query | Task | Result | Reason |
|---|---|---|---|
| "ACME Corp 海关 出口" | Task 4 | failed | timeout >10s（代理/网络） |
| site:acme.de Impressum | Task 1 | empty | 0 results — 需换 seed 重试 |
```

**Delivery gate (ties back to Source Ladder):** before finalizing, reconcile every empty evidence chain against this log. A chain marked empty for a *real* reason (target genuinely has no patents) → state that. A chain empty because the search *errored* → retry or explicitly flag `搜索失败·未核实`. Never let a silent error read as a confirmed negative.

## Search vs Fetch Discipline (iron rule)

**Search only discovers and locates URLs. It never deep-reads. Only stable pages that made it into the candidate pool get fetched for facts.**

Two phases, never blurred:

1. **Breadth scan** — search across all task lines, build a candidate pool in `sources/source_index.md`. Cheap, fast, no deep reading.
2. **Deep fetch** — extract facts only from pooled, stable pages (official pages, PDFs, registries, articles).

Blending the two (fetching every search hit) is what blows up context and time.

## Target-Type-Adaptive Emphasis

Don't search every dimension equally. Decide target type at the identity-lock gate, then weight effort:

| Target type | Search emphasis | Can go light |
|---|---|---|
| Manufacturer / factory | product models, certifications, patents, customs import/export | marketing content |
| Distributor / trader | channels, carried brands, marketplaces, customers | own R&D / tech |
| SaaS / software | pricing page, integrations, customer logos, funding | supply chain, customs |
| Brand / consumer goods | marketplace reviews, retail presence, ad/marketing | patents |

This mirrors the analysis emphasis table in `analysis-frameworks.md` — same target type drives both what you search and how you analyze.

## Language and Geography Strategy (overseas blind spot)

Search in the target's **home language and country domains first**, not only English:

- German company → German queries + `site:.de` + local registry (Handelsregister).
- Chinese company → Chinese queries + 天眼查/企查查-type registries.
- Japanese company → Japanese queries + local sources.

The original skill searched English-only, which misses local registration, local media, and local trade shows for non-US targets. Lock the home language + HQ-country domains at the identity gate and fold them into queries.

## Query Operator Cheat Sheet

| Operator | Use |
|---|---|
| `"exact phrase"` | legal names, product models, exact titles |
| `site:domain` | confine to official site or a specific registry/marketplace |
| `filetype:pdf` | catalogs, datasheets, annual reports, certificates |
| `A OR B` | alias groups: legal name OR brand OR abbreviation |
| `-term` | exclude a same-name collision |
| date terms | `2024 2025 2026` for recent news, filings, events |
| registry/assoc names | add the actual registry or association name as a keyword |

## Keyword Matrix (build before searching, update after each pass)

| Dimension | Query seeds |
|---|---|
| Entity | legal name, brand, ticker, domain, old names, abbreviations, local-language names |
| Organization | parent, subsidiaries, acquired brands, divisions, leadership, founders |
| Product | category, model/SKU names, datasheet terms, certification terms |
| Market | industry, buyer industry, use case, geography, channel, application |
| Evidence | revenue, employees, funding, acquisition, lawsuit, patent, certification, catalog |
| Channel | distributor, reseller, Amazon, Walmart, Alibaba, dealer, partner, service center |
| ABM | CEO, president, VP sales/marketing, procurement, trade show, webinar, case study |
| Source type | `filetype:pdf`, `site:`, registry, association, trade show, patent, SEC |

Run at least one expansion pass after the first 8-12 useful sources. Newly discovered names become new query seeds.

## Search Phases (end to end)

1. **Identity lock** — official domain, legal entity, HQ, parent/subsidiaries, main product category, same-name collision risk, **target type**, **home language**. Stop and ask the user if two companies plausibly match the name. *(This is the Diamond Gate — confirm scope before deep work.)*
2. **Project setup** — create the skeleton (see SKILL.md), write hypotheses per task.
3. **Breadth scan** — 20-40 candidate sources across all task lines into the source index.
4. **Deep fetch** — extract facts from pooled stable pages and PDFs.
5. **Browser/CDP fetch** — only when static fetch fails on JS-heavy or interactive public pages (see `platform-capabilities.md` for how; log to `evidence/browser_notes.md`).
6. **Expansion loop** — re-search using discovered models, subsidiaries, executives, distributors, competitors. Often finds better evidence than the original name searches.
7. **Sequential merge** — read task outputs, synthesize, preserve full task text in the appendix, dedupe the source index by canonical URL.

## Source Ladder

| Tier | Examples | Use |
|---|---|---|
| T0 | SEC, Companies House, court, customs, patent offices, certification databases, official registry | high-confidence facts |
| T1 | official site, official PDFs, investor pages, press releases, official social | company claims, product facts |
| T2 | industry associations, trade shows, distributors, marketplaces, credible media | market & channel evidence |
| T3 | lead databases, estimates, scraped profiles, review aggregators | estimates only — label tier + confidence |

Every material claim needs a source mark `[Sxx]`. Unsourced numbers → `待核实` or `estimate`.

Record candidates as:

```markdown
| ID | Tier | Task | Source | URL | Date checked | Notes |
|---|---|---|---|---|---|---|
| S01 | T1 | Task 1 | Company About page | https://... | YYYY-MM-DD | history, leadership |
```

## Trusted-Domain Injection (make the Source Ladder executable)

The ladder above is *advice* until you bake it into the query. Instead of searching open web and hoping a T0/T1 source floats up, **constrain the query to authority domains with `site:` OR-groups**:

```
(site:sec.gov OR site:companieshouse.gov.uk OR site:<registry>) "ACME Corp" filing
(site:<official-domain> OR site:<official-domain>/investors) revenue 2025
```

Keep per-evidence-chain domain shortlists and inject them automatically:

| Evidence chain | Inject these domains first |
|---|---|
| Legal / registry | SEC, Companies House, local registry (Handelsregister, 国家企业信用), court, patent office |
| Official claims | the company's own domain + `/investors` + `/press` + official PDFs |
| Market / channel | industry association sites, trade-show sites, marketplace domains, credible trade media |
| News / events | reputable financial/trade press domains for the target's home country |

> 这是 UZI-Skill `search_trusted()` 的核心：按维度预存权威域，搜索时自动拼 `(site:a OR site:b) query`，把结果锁在权威源里，过滤掉词典/UGC 噪声。它对口我们的 Source Ladder——只是把"优先官方源"从文档建议升级成可执行的查询模板。

Practical limits: cap the OR-group at ~5-6 domains (query length), and keep one *un-constrained* fallback pass — if the `site:`-locked query returns empty, retry open-web before marking the chain empty (a too-narrow `site:` filter is a common false negative).

## Noise Filter (drop garbage before it pools)

Before a search hit enters the candidate pool, drop the predictable garbage so it never costs a fetch:

- **Same-name collisions** — a different company sharing the name. Resolve at the identity gate, then `-term` the wrong industry out of queries.
- **Dictionary / encyclopedia noise** — generic word definitions instead of the entity (acute for short or common names). A hit whose text is mostly definitional, not about the company, is garbage.
- **Scraper / lead-aggregator clones** — auto-generated profile pages that restate the same thin data. Keep one as a T3 estimate at most; drop the rest.
- **SEO / ad farms** — listicles and ad pages that name-drop the company without primary facts.

> UZI-Skill 用一个关键词命中计数器（文本里命中 ≥2 个噪声特征词就丢）做这件事。我们不需要硬编码词表——规则是：**一条结果若不能明确指向目标实体本身，就不进池**。判断放在入池前，省下后续 fetch 成本。


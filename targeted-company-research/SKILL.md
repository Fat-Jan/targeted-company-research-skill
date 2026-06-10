---
name: targeted-company-research
description: >-
  Generate source-backed targeted company research reports for B2B sales, ABM,
  competitor analysis, partner research, and light diligence. Use when the user
  asks for company research, enterprise deep dive, customer research, competitor
  research, ABM preparation, company profile, targeted research, or a multi-source
  report about a named organization.
metadata:
  short-description: Source-backed company deep-dive reports
---

# Targeted Company Research

## Trigger

Use this skill when the user asks for:

- Company research, company profile, enterprise deep dive, customer research, competitor research.
- ABM sales preparation, partner research, supplier research, market-entry account research.
- A report on a specific named company, subsidiary, brand, competitor, buyer, distributor, or investment target.

Do not use this skill for broad industry reports without a named target company. Use a market or industry research workflow instead.

## Research Outcome

Create a source-backed Markdown report that explains the target company from five angles:

1. Company fundamentals, history, ownership, leadership, financial scale, compliance.
2. Product lines, technology, certifications, pricing signals, reviews.
3. Industry structure, market size, competitors, strategic position.
4. Customers, channels, distributors, supply chain, procurement signals.
5. Marketing, events, public decision makers, ABM entry points.

Default output is local-first:

```text
projects/{project_slug}/
├── task_plan.md
├── task1_company/task1_company.md
├── task2_product/task2_product.md
├── task3_industry/task3_industry.md
├── task4_channel/task4_channel.md
├── task5_marketing/task5_marketing.md
├── sources/source_index.md
├── evidence/
└── FINAL_REPORT.md
```

Optional outputs: HTML/PDF export, slide summary, or CRM/ABM brief only when the user asks.

## Required Inputs

If missing, infer conservatively from public sources and mark uncertain fields:

| Field | Meaning | Default |
|---|---|---|
| Target company | Legal name, brand name, or common name | Required |
| Website | Official site | Find from public search |
| Industry | Main business category | Infer and mark confidence |
| Geography | HQ and priority market | Global + HQ country |
| Research purpose | ABM, competitor, partner, supplier, diligence | General business research |
| Language | Output language | User language |
| Depth | light, standard, deep | standard |

## Source Ladder

Collect evidence in this order:

1. T0 regulatory, filings, court, customs, certification, official registry, patent and standards databases.
2. T1 company-owned pages, official news, investor pages, product docs, catalog PDFs, public social accounts.
3. T2 credible third-party databases, industry associations, trade shows, distributors, marketplaces, media.
4. T3 estimates and lead databases such as LinkedIn, ZoomInfo-like pages, import/export mirrors, review sites.

Every material claim needs a source mark such as `[S12]`. Unsourced numbers must be marked `待核实` or `estimate`.

## Search And Fetch Strategy

Use both breadth and depth:

- `web_search` discovers source candidates, aliases, subsidiaries, competitors, people, channels, documents, and regional results.
- `web_fetch` extracts stable pages, PDFs, product docs, articles, registry pages, and official pages found by search.
- CDP/browser access handles JavaScript-rendered pages, logged-in user-owned sessions, marketplace pages, LinkedIn-like public profile surfaces, and pages where static fetch fails.

Read `references/research-playbook.md` before running deep or standard research. It defines keyword expansion, Boolean query patterns, CDP/browser rules, evidence logging, and quality gates.

Read `references/task-instructions-template.md` when creating worker instructions or when the user asks for a full multi-part report.

## Keyword Expansion

Before collecting sources, build a keyword matrix:

- Entity aliases: legal name, brand name, abbreviations, former names, subsidiaries, acquired brands, local-language names.
- Domain terms: product categories, use cases, certifications, materials, standards, buyer industries.
- Evidence terms: revenue, employees, funding, acquisition, lawsuit, certification, patent, datasheet, catalog, distributor, reseller, trade show, case study.
- Geography terms: HQ city, manufacturing sites, target markets, language variants.
- Source operators: `site:`, `filetype:pdf`, exact quotes, OR groups, date terms, registry names, association names.

Run at least one expansion pass after the first 8-12 useful sources. Newly discovered product names, executives, subsidiaries, customers, and competitors become new query seeds.

## Browser And CDP Rules

Use the user's real browser or a CDP-connected browser only for public pages or user-authorized sessions.

Good CDP/browser targets:

- Official sites that render content in JavaScript.
- Product catalogs, store pages, review pages, and search pages that fail under static fetch.
- Public LinkedIn/company/team pages when the user has an authorized browser session.
- Trade show exhibitor directories, distributor locators, certification search pages, patent search pages.

Rules:

- Do not bypass paywalls, access controls, captchas, or private systems.
- Do not collect private personal contact data. Public business names, roles, official profile URLs, official contact forms, and published company emails are acceptable.
- Preserve evidence: page URL, access date, page title, key extracted text, and whether the source came from `web_search`, `web_fetch`, or browser/CDP.
- If browser extraction is visual, save a short note in `evidence/browser_notes.md` with the URL and observed facts.

Physical browser/CDP access pattern:

1. Open the target URL in the available browser tool or a user-authorized Chrome/CDP session.
2. Wait for the page to finish rendering or for the relevant result list/card/table to appear.
3. Extract title, URL, visible text, table rows, public profile fields, and product cards; prefer DOM text over screenshots.
4. Use screenshots only for evidence that cannot be reliably extracted as text.
5. Save the extracted facts to `evidence/browser_notes.md` and cite the URL in `sources/source_index.md`.
6. Return to `web_search` with newly discovered names, product models, certificates, distributors, or people.

## Execution Model

For standard/deep reports, split work into five tasks:

| Task | Focus | Minimum search | Minimum fetch/browser | Target sources |
|---|---:|---:|---:|---:|
| Task 1 | Company fundamentals and history | 12 | 8 | 12 |
| Task 2 | Products, technology, certifications | 12 | 8 | 12 |
| Task 3 | Industry and competitors | 12 | 8 | 10 |
| Task 4 | Customers, channels, supply chain | 12 | 8 | 12 |
| Task 5 | Marketing, events, public people, ABM | 14 | 8 | 12 |

Parallel workers are optional. If the environment supports subagents or OpenClaw sessions, assign one task per worker and forbid workers from reading other task output until final merge. If parallel workers are unavailable, run the tasks sequentially.

The skill is platform-neutral:

- Codex: use available web search/fetch/browser tools and local files.
- OpenClaw or other agents: use equivalent search, fetch, CDP, browser, and file-writing capabilities.
- No fixed model, Feishu, Slack, Google Drive, or private upload service is required.

## Report Structure

`FINAL_REPORT.md` should contain:

```markdown
# {Company} Targeted Company Research Report

> Research date: {date}
> Purpose: {purpose}
> Confidence: high / medium / low

## Executive Takeaways
5-8 specific findings with source marks.

## 1. Company Fundamentals
Ownership, history, leadership, footprint, scale, compliance.

## 2. Products And Technology
Product lines, technical specs, certifications, pricing and reviews.

## 3. Industry And Competitors
Market context, competitor matrix, positioning, strategic risks.

## 4. Customers, Channels And Supply Chain
Customer evidence, distributor/channel map, sourcing/procurement signals.

## 5. Marketing, Events And ABM Entry Points
Messaging, public campaigns, events, public decision makers, recommended angles.

## Data Gaps
Missing or low-confidence items.

## Sources
Deduplicated source index.
```

Keep all original numbers, years, names, platforms, source names, product names, and representative quotes that support the conclusion.

## Quality Gates

Before final delivery:

- Confirm the official website and legal/company identity are not confused with similarly named companies.
- Deduplicate sources and mark source tiers.
- Check every table row that contains a number has a source mark or `待核实`.
- Separate confirmed facts from estimates and inferences.
- Record missing data explicitly as `缺少数据：...`.
- Remove unsupported outreach claims and private contact guesses.
- Keep raw task files; do not only deliver a polished summary.

## Public Data And Ethics

This skill supports legitimate business research. It does not support credential misuse, private data extraction, evading access controls, or personal contact harvesting.

For people research, collect only public business identity information relevant to the company report: name, role, company, official profile URL, public speaking/event references, and official business contact channels.

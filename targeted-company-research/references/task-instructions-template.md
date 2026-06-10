# Task Instructions Template

Replace variables before assigning work:

| Variable | Meaning |
|---|---|
| `{COMPANY}` | Target company full name |
| `{SHORT}` | Short name or brand |
| `{WEBSITE}` | Official website |
| `{INDUSTRY}` | Industry |
| `{GEOGRAPHY}` | HQ or priority market |
| `{PROJECT}` | Project slug |
| `{LANGUAGE}` | Output language |
| `{PURPOSE}` | ABM, competitor, partner, supplier, diligence, or general |

## Shared Worker Rules

- Work only on the assigned task.
- Use `web_search` for breadth and `web_fetch` for source extraction.
- Use browser/CDP when fetch fails on public JavaScript-heavy pages.
- Save evidence notes for browser/CDP pages in `projects/{PROJECT}/evidence/browser_notes.md`.
- Add source marks `[Sxx]` to material claims.
- Mark estimates and missing facts explicitly.
- Do not read other task folders until final merge.
- Do not collect private personal contact information or guess private emails.

## Task 1: Company Fundamentals And History

```markdown
# Task 1: {COMPANY} Company Fundamentals And History

## Objective

Collect verified facts on identity, ownership, history, leadership, footprint, scale, compliance, and key milestones for {COMPANY}.

## Known Inputs

- Company: {COMPANY}
- Short name: {SHORT}
- Website: {WEBSITE}
- Industry: {INDUSTRY}
- Geography: {GEOGRAPHY}
- Purpose: {PURPOSE}
- Output language: {LANGUAGE}

## Search Seeds

- "{COMPANY}" revenue employees
- "{COMPANY}" legal entity headquarters
- "{COMPANY}" acquisition funding ownership
- "{COMPANY}" CEO leadership team founder CFO
- "{COMPANY}" lawsuit litigation recall regulatory
- "{COMPANY}" annual report SEC filing registry
- site:{WEBSITE_DOMAIN} about leadership history
- "{COMPANY}" sustainability ESG compliance

## Fetch Targets

- Official about/history/contact pages.
- Registry, filing, court, certification, patent or regulatory pages.
- Official PDFs and press releases.
- Credible company databases only for estimates.

## Output

Write to `projects/{PROJECT}/task1_company/task1_company.md`.

Include:

- Identity lock and similar-name risks.
- Company timeline.
- Ownership and subsidiaries.
- Leadership table.
- Locations and footprint.
- Revenue/employee/scale estimates with confidence.
- Compliance, litigation, ESG.
- Data gaps.
- Sources.
```

## Task 2: Products, Technology And Certifications

```markdown
# Task 2: {COMPANY} Products, Technology And Certifications

## Objective

Map {COMPANY}'s product lines, technical specifications, certification signals, pricing and review evidence.

## Search Seeds

- "{COMPANY}" products catalog filetype:pdf
- "{COMPANY}" datasheet specifications
- "{SHORT}" product model certification
- site:{WEBSITE_DOMAIN} products catalog support downloads
- "{COMPANY}" UL ISO CE RoHS REACH certification
- "{COMPANY}" patent technology R&D
- site:amazon.com "{SHORT}" OR "{COMPANY}"
- site:walmart.com "{SHORT}" OR "{COMPANY}"

## Fetch Targets

- Product pages and catalog PDFs.
- Datasheets and certification documents.
- Marketplace pages and distributor product pages.
- Patent or standards pages.

## Output

Write to `projects/{PROJECT}/task2_product/task2_product.md`.

Include:

- Product taxonomy.
- Model/specification table.
- Certification matrix.
- Pricing/review signals.
- Technology differentiation.
- Product evidence gaps.
- Sources.
```

## Task 3: Industry And Competitors

```markdown
# Task 3: {SHORT} Industry And Competitor Analysis

## Objective

Explain the industry context, market structure, key competitors, and strategic position of {SHORT}.

## Search Seeds

- "{INDUSTRY}" market size CAGR forecast
- "{INDUSTRY}" competitive landscape market share
- "{COMPANY}" competitors
- "{INDUSTRY}" trends 2024 2025 2026 regulation
- "{INDUSTRY}" supply chain value chain
- "{Competitor}" revenue products market share

## Fetch Targets

- Market reports with accessible summaries.
- Industry association pages.
- Competitor official pages and filings.
- Distributor/category pages that reveal competitive sets.

## Output

Write to `projects/{PROJECT}/task3_industry/task3_industry.md`.

Include:

- Market size and growth with source tiers.
- Value chain and profit pool view.
- Competitor matrix with at least five competitors for standard/deep reports.
- Positioning map in text/table form.
- Opportunities, threats, and implications for {SHORT}.
- Sources.
```

## Task 4: Customers, Channels And Supply Chain

```markdown
# Task 4: {SHORT} Customers, Channels And Supply Chain

## Objective

Map public evidence of customers, channel structure, distributors, marketplaces, sourcing, logistics and procurement signals.

## Search Seeds

- "{COMPANY}" customers clients case study
- "{COMPANY}" distributor reseller dealer partner
- "{COMPANY}" import export supplier customs
- "{COMPANY}" OEM ODM partnership
- "{COMPANY}" warehouse distribution center
- "{COMPANY}" procurement sourcing supply chain
- site:amazon.com "{SHORT}" OR "{COMPANY}"
- site:walmart.com "{SHORT}" OR "{COMPANY}"

## Fetch Targets

- Case studies and customer pages.
- Distributor and reseller pages.
- Marketplace pages.
- Import/export or customs mirrors.
- Job pages mentioning procurement, logistics, sourcing or sales channels.

## Output

Write to `projects/{PROJECT}/task4_channel/task4_channel.md`.

Include:

- Confirmed customer evidence.
- Channel map by type and region.
- Marketplace SKU, price and rating evidence when public.
- Supply chain and sourcing signals.
- Procurement implications for ABM or partnership.
- Sources.
```

## Task 5: Marketing, Events, Public People And ABM

```markdown
# Task 5: {SHORT} Marketing, Events, Public People And ABM Entry Points

## Objective

Analyze public marketing behavior, events, messaging, content assets, public business decision makers and practical ABM entry angles.

## Search Seeds

- "{COMPANY}" trade show exhibitor booth
- "{COMPANY}" webinar case study white paper
- "{COMPANY}" press release news 2024 2025 2026
- "{COMPANY}" CEO president VP sales VP marketing
- "{COMPANY}" association member
- "{COMPANY}" LinkedIn leadership
- site:{WEBSITE_DOMAIN} news blog resources

## Fetch Targets

- Official news/blog/resources pages.
- Trade show and association pages.
- Public company profile pages.
- Public event speaker pages.
- Official social pages and video channels.

## Output

Write to `projects/{PROJECT}/task5_marketing/task5_marketing.md`.

Include:

- Messaging and positioning.
- Content and PR cadence.
- Events and associations.
- Public business decision makers with name, role, company, source URL.
- Official contact channels, not private guesses.
- ABM entry angles tied to source evidence.
- Sources.
```

## Merge Template

```markdown
# {COMPANY} Targeted Company Research Report

> Research date: {DATE}
> Purpose: {PURPOSE}
> Source count: {SOURCE_COUNT}

## Executive Takeaways

1. ...

## 1. Company Fundamentals

## 2. Products And Technology

## 3. Industry And Competitors

## 4. Customers, Channels And Supply Chain

## 5. Marketing, Events And ABM Entry Points

## Data Gaps

- 缺少数据：...

## Sources

| ID | Tier | Source | URL | Notes |
|---|---|---|---|---|
```

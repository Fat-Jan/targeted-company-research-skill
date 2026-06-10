# Research Playbook

## Research Thesis

Targeted company research turns a named company into an evidence-backed business map: who the company is, what it sells, where it competes, who it sells to, how it reaches the market, and which public signals matter for ABM, partnership, competition, or diligence.

## Keyword Expansion Matrix

Build this matrix before source collection. Update it after each discovery pass.

| Dimension | Query seeds |
|---|---|
| Entity | legal name, brand name, ticker, domain, old names, abbreviations, local-language names |
| Organization | parent, subsidiaries, acquired brands, divisions, leadership names, founder names |
| Product | category names, model names, SKU names, datasheet terms, certification terms |
| Market | industry, buyer industry, use case, geography, channel, application |
| Evidence | revenue, employees, funding, acquisition, lawsuit, patent, certification, catalog |
| Channel | distributor, reseller, Amazon, Walmart, Alibaba, dealer, partner, service center |
| ABM | CEO, president, VP sales, VP marketing, procurement, trade show, webinar, case study |
| Source type | filetype:pdf, site:official-domain, registry, association, trade show, patent, SEC |

Use exact names first, then alias groups:

```text
"{Company Legal Name}" revenue employees
"{Brand}" OR "{Abbreviation}" products catalog filetype:pdf
site:{official_domain} (about OR leadership OR news OR products OR catalog)
"{Company}" (distributor OR reseller OR partner OR dealer)
"{Company}" (patent OR certification OR UL OR ISO OR CE)
"{Company}" (trade show OR exhibitor OR booth OR webinar)
"{Company}" (acquisition OR funding OR lawsuit OR litigation)
"{Company}" "{Product Category}" competitors
"{Executive Name}" "{Company}"
```

## Search Phases

### Phase 1: Identity Lock

Confirm the target company identity before deep research:

- Official domain and legal entity.
- HQ city/country.
- Parent/subsidiary relationships.
- Main product category.
- Similar-name collision risks.

Stop and clarify with the user when two companies plausibly match the same target name.

### Phase 2: Breadth Search

Collect 20-40 candidate sources across all five task areas. Use search results to discover:

- Alternative names and subsidiaries.
- Product models and certifications.
- Competitors and distributors.
- Executive names and public event references.
- Market reports and association pages.

Save candidate source metadata in `sources/source_index.md`:

```markdown
| ID | Tier | Task | Source | URL | Date checked | Notes |
|---|---|---|---|---|---|---|
| S01 | T1 | Task 1 | Company website | https://... | YYYY-MM-DD | About page |
```

### Phase 3: Deep Fetch

Use `web_fetch` or equivalent extraction for stable pages:

- Official about/product/news pages.
- PDF catalogs, datasheets, annual reports, certificates.
- Regulatory pages and public registries.
- Association pages and trade show directories.
- Credible third-party profiles and market data pages.

For each source, extract only facts relevant to the report. Avoid long pasted excerpts. Preserve exact numbers, dates, titles, product names, standards, and source names.

### Phase 4: Browser/CDP Fetch

Use a CDP-connected browser when static extraction fails or when a page is JavaScript-heavy.

Good targets:

- Product listing pages with client-side rendering.
- Marketplace product pages and review summaries.
- Trade show exhibitor search pages.
- LinkedIn-like company surfaces in a user-authorized session.
- Certification lookup tools that require interactive search.

Evidence note format:

```markdown
## Browser Evidence

### B01
- URL:
- Page title:
- Access date:
- Tool: browser/CDP
- Extracted facts:
- Screenshot path, if saved:
- Confidence:
```

Browser rules:

- Use only public pages or user-authorized sessions.
- Do not bypass login, paywall, captcha, robots restrictions, or rate limits.
- Do not scrape private personal data.
- Prefer official company contact channels over individual emails.

Implementation pattern:

1. Open the public target URL in the available browser tool, Chrome connector, or OpenClaw/CDP browser session.
2. Wait for the required content to render: company cards, product grids, certification search results, marketplace reviews, event exhibitor rows, or public profile fields.
3. Extract visible DOM text first: page title, canonical URL, section headings, table rows, product names, prices, ratings, dates, event names, person names and roles.
4. Use screenshot evidence only when DOM extraction is not reliable.
5. Record a short browser note with URL, title, access date, extracted facts, confidence, and screenshot path when used.
6. Feed newly discovered entities back into the keyword matrix.

Avoid foreground focus stealing when the environment provides a background browser or in-app browser. If only the user's visible Chrome is available, keep navigation minimal and preserve the current tab context where possible.

### Phase 5: Expansion Loop

Run a second keyword pass using discovered names:

- Product model names.
- Subsidiaries and acquired brands.
- Executives and event speakers.
- Distributors and customer names.
- Competitors and standards.
- Industry-specific databases.

The second pass often finds better evidence than the original company-name searches.

## Source Tiers

| Tier | Source examples | Use |
|---|---|---|
| T0 | SEC, Companies House, court records, customs, patent offices, certification databases | High-confidence facts |
| T1 | Official website, official PDFs, investor pages, official social pages, press releases | Company claims and product facts |
| T2 | Industry associations, trade shows, distributors, marketplaces, credible media | Market and channel evidence |
| T3 | Lead databases, estimates, scraped company profiles, review aggregators | Estimates only |

Label private-company revenue, employee count, traffic, and market share estimates with tier and confidence.

## Task-Specific Search Packs

### Task 1: Company Fundamentals

Search for:

- `{Company} revenue employees`
- `{Company} legal entity headquarters`
- `{Company} acquisition funding ownership`
- `{Company} leadership team CEO CFO founder`
- `{Company} lawsuit litigation recall regulatory`
- `site:{domain} about history leadership`
- `{Company} annual report SEC filing Companies House registry`

Output facts:

- Legal identity, HQ, history, ownership, leadership.
- Revenue/employee range with confidence.
- Locations, facilities, warehouses.
- Regulatory, litigation, certification, ESG facts.

### Task 2: Products And Technology

Search for:

- `{Company} products catalog filetype:pdf`
- `{Company} datasheet specifications`
- `{Company} product model certification`
- `{Product Category} "{Company}" review rating`
- `site:{domain} products catalog support downloads`
- `{Company} patent technology R&D`

Output facts:

- Product line map.
- Model/specification table.
- Certifications and standards.
- Pricing/review signals.
- Technical differentiation and gaps.

### Task 3: Industry And Competitors

Search for:

- `{Industry} market size CAGR forecast`
- `{Industry} competitive landscape market share`
- `{Company} competitors`
- `{Competitor} revenue product market share`
- `{Industry} trends 2024 2025 2026 regulation`
- `{Industry} supply chain value chain`

Output facts:

- Market structure and growth.
- Competitor matrix, at least five competitors for standard/deep research.
- Positioning, opportunities, threats.
- Clear distinction between market facts and strategic inference.

### Task 4: Customers, Channels, Supply Chain

Search for:

- `{Company} customers clients case study`
- `{Company} distributor reseller dealer partner`
- `{Company} import export supplier customs`
- `site:amazon.com "{Company}" "{Brand}"`
- `site:walmart.com "{Company}" "{Brand}"`
- `{Company} warehouse distribution center`
- `{Company} procurement sourcing supply chain`

Output facts:

- Confirmed customers and evidence.
- Channel map by region/type.
- Marketplace presence, SKU/price/rating signals.
- Sourcing and procurement signals.

### Task 5: Marketing, Events, Public People, ABM

Search for:

- `{Company} trade show exhibitor booth`
- `{Company} webinar case study white paper`
- `{Company} LinkedIn leadership`
- `{Company} CEO president VP sales VP marketing`
- `{Company} press release news 2024 2025 2026`
- `{Company} association member`
- `site:{domain} news blog resources`

Output facts:

- Messaging and positioning.
- Recent campaigns and content assets.
- Trade shows/events.
- Public business decision makers: name, role, company, public profile/event URL.
- ABM entry angles with evidence, not private contact guesses.

## Final Report Rules

Lead with conclusions:

- Specific object.
- Clear judgment.
- Data or source evidence.

Bad: `We researched the company from multiple angles.`

Good: `{Company} is a privately held battery distributor with stronger channel evidence than technology differentiation; confirmed evidence includes {N} distributor pages, {N} product catalog pages, and {N} certification records.`

Every table needs source marks. Every source mark must resolve to the source index.

Missing evidence must be explicit:

```text
缺少数据：未找到公开可验证的 2025 年营收；第三方估算仅能支持区间判断。
```

## Quality Checklist

- Official company identity locked.
- All five task files exist for standard/deep reports.
- Source index has no duplicate URLs unless the page supports different facts.
- Source tier assigned for every source.
- No private credentials, cookies, tokens, or personal contact guesses in output.
- Browser/CDP observations are logged when used.
- Inferences are labeled as inferences.
- Final report preserves raw numbers, years, platform names, people names, product names, source names, and representative short quotes.

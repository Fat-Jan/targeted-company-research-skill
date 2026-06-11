# Platform Capabilities Map

This skill describes *what to do*. This file describes *how to actually do it on your platform* — which concrete tool maps to each abstract capability. Read this before executing research.

> 这份文件解决"执行层"问题：把抽象能力（搜索 / 抓取 / 浏览器 / 子代理 / 写文件）映射到你所在平台的真实工具名。原始 skill 缺这一层，导致"知道做什么、不知道怎么调起能力"。

## Abstract Capabilities

The research workflow needs five capabilities:

| Capability | Purpose |
|---|---|
| `SEARCH` | Discover source candidates, aliases, competitors, people, documents. Breadth. |
| `FETCH` | Extract facts from a known stable URL or PDF. Depth. |
| `BROWSER` | Render JavaScript-heavy pages, marketplace pages, public profile surfaces, certification/exhibitor lookup tools, and user-authorized sessions where static fetch fails. |
| `SUBAGENT` | Run one research task (or one analysis module) in an isolated worker, in parallel, then return a structured result. |
| `WRITE` | Persist task files, evidence notes, the source index, and the final report locally. |

## Platform Tool Map

| Capability | Claude (Claude Code / API) | Codex | OpenClaw (龙虾) | Hermes / other |
|---|---|---|---|---|
| `SEARCH` | `WebSearch` | native `web_search` | `web_search` tool, or a spawned worker that searches | any web search tool |
| `FETCH` | `WebFetch` | native `web_fetch` | `web_fetch` / page-read tool, or a worker that reads the page | any URL fetch / reader |
| `BROWSER` | Playwright/Chrome MCP server (`browser_navigate`, `browser_snapshot`, `browser_evaluate`); no native browser otherwise | built-in browser tool | CDP-connected browser session | any CDP / headless browser |
| `SUBAGENT` | `Task` tool (spawn one sub-agent per research task) | parallel workers | `sessions_spawn` / sub-agent spawn | any worker/job spawn API |
| `WRITE` | `Write` / `Edit` | native file write | file write tool | any file write |

> 龙虾的关键执行路径：搜索和读网页是由**子代理**完成的。打包成 skill 时这条编排逻辑容易丢失。下面的"Subagent Orchestration"明确写出来，让任何平台都能复现。

## Capability Probe

Before research, decide which capabilities are available. Do not assume.

1. `SEARCH` — almost always available. Required. If absent, ask the user to paste search results.
2. `FETCH` — usually available. If absent, fall back to `BROWSER`, then to the keyless Jina Reader (below), then to asking the user to paste page text.
3. `BROWSER` — optional but high-value. If absent, skip JS-only sources and mark them as data gaps; never fabricate.
4. `SUBAGENT` — optional accelerator. If absent, run tasks sequentially (see Execution Model in SKILL.md). Sequential is a fully supported path, not a degraded one.
5. `WRITE` — required for the local-first output. If absent, stream the report inline and tell the user nothing was persisted.

When a capability is missing, state it once at the start, pick the documented fallback, and continue. Do not stop the whole run for one missing optional capability.

## Auto-Downgrade Depth (don't over-promise on a thin environment)

Depth (`light` / `standard` / `deep`, defined in SKILL.md) is not only the user's choice —
the probe can **downgrade it automatically** when the environment can't sustain the asked
depth *(adopted from UZI-Skill's auto-degrade)*. Decide right after the probe, before research:

| Probe result | Action |
|---|---|
| `SUBAGENT` absent **and** depth was `deep` | drop to `standard` (a deep run serially is slow and stall-prone) |
| `FETCH` and `BROWSER` both absent | drop to `light` — without reliable page reading, evidence depth can't be met |
| `SEARCH` returns errors/empty on first probe queries (network blocked) | drop to `light`, lean on user-pasted sources |
| first install / no MCP browser configured | default to `light` until the user opts into deeper |

State the downgrade once: *"Running at `standard` instead of `deep` — no sub-agent
capability on this platform."* Never silently run `deep` quality bars on a `light`
environment, and never claim a depth the evidence can't back.

## SEARCH vs FETCH Discipline

This single rule prevents context bloat and runaway searches:

- **`SEARCH` only discovers and locates URLs. It never deep-reads.** Skim result titles/snippets, add good URLs to the candidate pool, move on.
- **`FETCH` (or `BROWSER`) only runs on URLs already in the candidate pool**, to extract specific facts for the report.

Two phases: breadth-scan to fill a candidate pool first, then batch-extract from it. Do not fetch a page the moment you find it — collect, then mine.

## Subagent Orchestration

When `SUBAGENT` is available, this is the recommended way to run research — it is faster and keeps each task's context clean. This is the execution layer that was missing from the original packaged skill.

**Spawn rule: one worker per task (or per analysis module).** Each worker gets:

1. Its own `task_instructions.md` (from `task-packs.md`) — the only task it works on.
2. The shared identity lock (company legal name, official domain, HQ) so workers don't research the wrong entity.
3. `SEARCH` + `FETCH` (+ `BROWSER` if available) + `WRITE` to its own task folder.
4. A hard instruction: **do not read other task folders** until the final merge.

**Worker contract:**

- Return a structured result: status, source count, fetch/browser count, major findings, data gaps.
- Write findings to `projects/{slug}/taskN_xxx/taskN_xxx.md` and evidence to `evidence/`.
- A worker may not declare the overall job done. Only the orchestrator merges and finalizes.

**Orchestrator contract:**

- Spawn workers per the batch dependency order in SKILL.md (later batches receive earlier batches' findings as context).
- Verify each worker's evidence (files written, source counts) before accepting it.
- Retry a failed worker once, then mark it `blocked` with a note rather than dropping it silently.

**Operational guards (learned from production runs):**

- **Stagger launches** (~5s between workers in a batch) to avoid search rate limits.
- **Validate output length / completeness** per worker; a 2-line return means the worker failed — retry.
- **Cap per-task search budget** (see search-strategy.md stop conditions) so a worker can't loop forever.

> 这些守护规则（错峰启动、输出校验、失败重试一次、单任务搜索预算上限）直接治"子代理慢、容易卡死"。

## Browser/CDP Rules

Use the user's real browser or a CDP-connected browser only for public pages or user-authorized sessions.

- Do not bypass login, paywall, captcha, robots restrictions, or rate limits.
- Do not collect private personal data. Public business names, roles, official profile URLs, official contact forms, and published company emails are acceptable.
- Prefer DOM text extraction over screenshots; use screenshots only when text extraction is unreliable.
- Log every browser-sourced fact in `evidence/browser_notes.md` with URL, page title, access date, extracted facts, and confidence.
- Avoid foreground focus stealing when a background/in-app browser is available. If only the user's visible Chrome is available, keep navigation minimal.

## Keyless Fetch Fallback (Jina Reader)

When `FETCH` is missing or a page blocks the native fetcher, and before falling back to asking the user, try the keyless Jina Reader — it fetches any public URL and returns clean Markdown, no API key:

```bash
curl -s https://r.jina.ai/https://example.com/about
```

- Public pages only — it does not bypass login, paywall, or access controls.
- Treat the output as a T1/T2 source by the *original* URL, not as r.jina.ai; record the real page URL in the source index.
- Subject to the same hard timeout (~15s) and failure-trace rules as any fetch (see `search-strategy.md`).

> 来自 Agent-Reach 的无 key 网页兜底。与 BROWSER 并列，排在「让用户粘贴」之前——大多数静态公开页用它就能读到，省去开浏览器的开销。

## Sequential Fallback (no SUBAGENT)

If `SUBAGENT` is unavailable, run the tasks yourself in the same batch dependency order. Every quality bar stays identical — the only thing you lose is parallelism. Update `task_status.md` after each task so progress is recoverable if interrupted.

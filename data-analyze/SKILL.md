---
name: data-analyze
description: >
  Answer data questions end-to-end, from a quick metric lookup to a full multi-dimensional
  analysis to a formal report. Trigger when the user asks a question that requires querying,
  aggregating, or interpreting data — "how many X last week", "what's driving the drop in Y",
  "prepare a report on Z metrics", or any request naming a table, dataset, warehouse, CSV/Excel
  file, or metric that needs to be looked up rather than reasoned about from code. Covers
  gathering data (via a connected warehouse or user-provided files/pasted results), analysis,
  validation before presenting, and choosing the right output format (number, table, chart,
  narrative report).
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Data analysis workflow (compiled 2026)
---

# SKILL: Data Analysis — Question to Answer

Answer a data question, scaled to how big the question actually is. Not every ask needs a report, and not every report needs to start from a raw table scan — matching effort to the question is the first decision, not an afterthought.

## Step 1 — Classify the question

|Signal|Complexity|Output shape|
|---|---|---|
|Single metric, simple filter, factual lookup ("how many users signed up last week?")|Quick answer|Number + context + query used|
|Multi-dimensional exploration, trend/driver analysis, comparison ("what's driving the drop in conversion?")|Full analysis|Key finding first, then supporting tables/charts|
|Comprehensive investigation for a stakeholder audience ("prepare a quarterly business review")|Formal report|Executive summary → methodology → findings → caveats → recommendations|

Also pin down: which tables/metrics/dimensions/time range are actually needed, and whether the answer wants a number, a table, a chart, a narrative, or some combination — deciding this before querying avoids re-running the same pull twice.

## Step 2 — Gather the data

**A data warehouse or DB is connected:**
1. Explore the schema to find the relevant tables/columns before writing SQL blind.
2. Write the query — use dialect-specific syntax and best practices (window functions, CTEs, partition-aware filters) rather than generic SQL.
3. Execute and retrieve results.
4. If it fails, debug against the actual error (column name, dialect syntax, join cardinality) and retry — don't rewrite from scratch on the first failure.
5. If results look unexpected (row count off, all-null column, magnitude implausible), sanity-check before treating the pull as ground truth.

**Nothing is connected:**
1. Ask the user for data directly — pasted query results, a CSV/Excel upload, or a description of the schema so a query can be drafted for them to run manually.
2. Do not fabricate or estimate numbers to fill the gap; a partial real answer beats a complete guessed one.

## Step 3 — Analyze

- Calculate the aggregations/comparisons the question actually calls for — don't compute metrics that weren't asked for just because they're available.
- Look for patterns, trends, outliers, anomalies — and for "why" questions, break into sub-questions (did volume change? mix change? rate change per segment?) rather than eyeballing one aggregate.
- Compare across the dimensions that matter for this question specifically (time periods, segments, cohorts) — extra cuts add noise, not rigor.

## Step 4 — Validate before presenting

Run these checks before showing anything to the user; if any one raises a flag, investigate and note it as a caveat rather than silently presenting a number you don't trust:

- **Row count sanity** — does the record count make sense for the filter applied?
- **Null check** — are unexpected nulls skewing an aggregate?
- **Magnitude check** — is the number in a plausible range given what's known about the business?
- **Trend continuity** — does a time series have unexplained gaps or a suspicious step change?
- **Aggregation logic** — do subtotals actually sum to the total?

## Step 5 — Present findings

- **Quick answer:** state the number directly with context, include the query (in a code block) for reproducibility.
- **Full analysis:** lead with the key insight, not the setup; support with tables/charts; note methodology and caveats; suggest a natural follow-up question.
- **Formal report:** executive summary → methodology → detailed findings with evidence → caveats/limitations/data-quality notes → recommendations and next steps.

## Step 6 — Visualize where it helps

Reach for a chart only when it communicates the result better than a table or a sentence would. Pick the chart type deliberately (trend → line, comparison → bar, composition → stacked/treemap, distribution → histogram) rather than defaulting to whatever's fastest to generate.

## Tips

- Specific time ranges, segments, and metrics up front save a clarifying round-trip.
- Naming known table names speeds up schema discovery — ask for them if the user has them.
- Complex questions decompose into multiple queries; don't force one mega-query to answer everything at once.
- Never skip Step 4 — a wrong number presented confidently is worse than a slower correct one.

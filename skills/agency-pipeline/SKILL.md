---
name: agency-pipeline
description: Prospect Pipeline Manager — scans all audit files to build a scored, staged pipeline view with revenue projections
---

# Prospect Pipeline Manager

You are the pipeline management engine for the AI Agency Command Center. When the user runs `/agency pipeline`, you scan the current directory for ALL audit and analysis files across every tool suite, build a comprehensive pipeline view with composite scores, classify each prospect by stage, calculate revenue potential, and output a sortable pipeline report.

This gives the agency operator a bird's-eye view of every prospect they've ever analyzed — where they stand, what's been done, and where the money is.

---

## Invocation

```
/agency pipeline
```

No arguments required. Operates on the current working directory.

---

## Execution Flow

### Step 1 — Discover All Audit Files

Use `Bash` to find every audit/analysis file in the current working directory:

```bash
ls -la *.md 2>/dev/null | grep -iE "(AGENCY-ONBOARD|AGENCY-PROPOSAL|MARKETING-AUDIT|PROSPECT-ANALYSIS|REPUTATION-AUDIT|REPUTATION-SCORECARD|GEO-AUDIT|GEO-REPORT|LEGAL-COMPLIANCE|SALES-PROPOSAL|COMPETITIVE-INTEL|BRAND-MENTIONS|AGENCY-PIPELINE|AGENCY-REPORT)" 2>/dev/null
```

Also run a broader scan to catch files with non-standard naming:
```bash
ls -la *.md 2>/dev/null
```

Review all `.md` files for audit-related content by checking the first 10 lines of each file for score indicators, audit headers, or company analysis markers.

### Step 2 — Parse Each File and Extract Prospect Data

For EACH audit file found, read it and extract:

**Prospect Identification:**
- Company name (from the file title or document header)
- URL (if present in the document)
- Industry/business type
- Location

**Scores (if present):**
- Marketing score (0-100)
- Reputation score (0-100)
- GEO/SEO score (0-100)
- Legal score (0-100)
- Sales opportunity score (0-100)
- Composite/agency score (if pre-calculated)

**File metadata:**
- File name
- Which tool suite generated it (Marketing, Reputation, GEO, Legal, Sales, Agency)
- Date (from file content or filesystem)

**Key data points:**
- Number of critical findings
- Top critical finding (single most impactful issue)
- Recommended tier (if a proposal exists)
- Proposed pricing (if a proposal exists)

### Step 3 — Consolidate by Prospect

Group all files by company/prospect name. A single prospect may have multiple files across different tool suites.

For each unique prospect, build a consolidated record:

```
PROSPECT: [Company Name]
URL: [URL if known]
Industry: [Industry]
Location: [Location]
Files: [List of all files for this prospect]
Suites Completed: [Which of the 5 tool suites have been run]
Suites Pending: [Which haven't been run yet]

Scores:
- Marketing: [score or "—"]
- Reputation: [score or "—"]
- GEO/SEO: [score or "—"]
- Legal: [score or "—"]
- Sales: [score or "—"]
- Composite: [calculated or "—"]
```

### Step 4 — Calculate Composite Scores

For prospects with scores from multiple tool suites, calculate the composite:

```
Composite = (Marketing x 0.25) + (Reputation x 0.20) + (GEO x 0.20) + (Legal x 0.15) + (Sales x 0.20)
```

**If not all scores are available, use adjusted weights:**

Only recalculate weights proportionally across available dimensions. For example, if only Marketing (25%), Reputation (20%), and GEO (20%) are available:
- Total available weight: 65%
- Adjusted: Marketing = 25/65 = 38.5%, Reputation = 20/65 = 30.8%, GEO = 20/65 = 30.8%

Apply the adjusted weights and note the score is partial:
```
Composite (Partial — 3/5 dimensions) = [score]
```

### Step 5 — Classify Pipeline Stage

Assign each prospect to a pipeline stage based on what work has been completed:

| Stage | Criteria | Icon |
|-------|----------|------|
| **New Lead** | Only a quick scan or single audit exists. No comprehensive analysis. | [1] |
| **Audited** | Full onboard report exists, OR 3+ individual audit files exist. Comprehensive data available. | [2] |
| **Proposed** | An `AGENCY-PROPOSAL-*.md` file exists for this prospect. Pricing has been presented. | [3] |
| **Active Client** | The user manually marks a prospect as active, OR a proposal file contains acceptance indicators. | [4] |

**Stage detection logic:**

```
IF AGENCY-PROPOSAL-*.md exists for this prospect:
    stage = "Proposed" [3]
ELSE IF AGENCY-ONBOARD-*.md exists OR (3+ audit files from different suites exist):
    stage = "Audited" [2]
ELSE:
    stage = "New Lead" [1]
```

Note: "Active Client" stage requires manual tagging by the user. If any file contains text indicating active engagement (e.g., "ACTIVE CLIENT" or "ENGAGED"), classify accordingly.

### Step 6 — Calculate Revenue Potential

Estimate the revenue potential for each prospect based on available data:

**Method 1: From Proposal Data (if a proposal exists)**
- Use the recommended tier pricing directly
- Essentials: midpoint of the Essentials range
- Growth: midpoint of the Growth range
- Full Agency: midpoint of the Full Agency range

**Method 2: From Scores (if no proposal but scores exist)**
Use the composite score to estimate which tier they'd likely need:

| Composite Score | Likely Tier | Estimated Monthly Revenue |
|----------------|-------------|--------------------------|
| 0-30 | Full Agency | $5,500/month |
| 31-45 | Full Agency or Growth | $4,000/month |
| 46-60 | Growth | $2,500/month |
| 61-75 | Growth or Essentials | $1,500/month |
| 76-100 | Essentials | $800/month |

Lower scores = more problems = higher revenue potential from agency services.

**Method 3: From Industry (if minimal data)**
Use industry average estimates:

| Industry | Estimated Monthly Potential |
|----------|---------------------------|
| Local Service (HVAC, Plumbing, Roofing) | $2,000-$3,500/month |
| Professional Services (Legal, Accounting) | $2,500-$4,000/month |
| Healthcare/Medical | $3,000-$5,000/month |
| SaaS/Software | $3,500-$6,000/month |
| E-commerce | $2,500-$5,000/month |
| Restaurant/Hospitality | $1,500-$2,500/month |
| Real Estate | $2,000-$3,500/month |

### Step 7 — Calculate Opportunity Score

Create an Opportunity Score (0-100) that combines multiple factors to rank prospects by pursuit priority:

```
Opportunity Score = (Need Score x 0.40) + (Fit Score x 0.30) + (Readiness Score x 0.30)
```

**Need Score (based on composite audit score — inverted):**
- Composite 0-30 = Need 90-100 (desperate need)
- Composite 31-50 = Need 70-89 (significant need)
- Composite 51-70 = Need 50-69 (moderate need)
- Composite 71-100 = Need 20-49 (low need)
- Formula: `Need = 100 - Composite` (capped at 100)

**Fit Score (based on sales opportunity score or industry fit):**
- If Sales score exists, use it directly
- Otherwise, assign based on industry (local service businesses = 80, SaaS = 70, etc.)

**Readiness Score (based on pipeline stage and engagement):**
- Proposed = 90 (they've seen pricing, awaiting decision)
- Audited = 60 (full data, ready for proposal)
- New Lead = 30 (needs more analysis)

### Step 8 — Build Pipeline Summary Statistics

Calculate aggregate pipeline metrics:

```
PIPELINE SUMMARY:
- Total Prospects: [count]
- By Stage: [X] New Leads | [X] Audited | [X] Proposed | [X] Active
- Total Pipeline Value: $[sum of all monthly revenue potentials]/month
- Average Composite Score: [average across all scored prospects]
- Highest Opportunity: [prospect name] (Opportunity Score: [X])
- Suites Used: Marketing [X] | Reputation [X] | GEO [X] | Legal [X] | Sales [X]
```

### Step 9 — Generate the Pipeline Report

Write the report to `AGENCY-PIPELINE.md`:

```markdown
# Agency Pipeline Report

**Generated:** [Current Date]
**Working Directory:** [current directory path]

---

## Pipeline Summary

| Metric | Value |
|--------|-------|
| Total Prospects | [X] |
| New Leads | [X] |
| Audited | [X] |
| Proposed | [X] |
| Active Clients | [X] |
| Total Pipeline Value | $[X]/month |
| Average Composite Score | [X]/100 |

---

## Pipeline Overview

*Sorted by Opportunity Score (highest first)*

| # | Company | Stage | Composite | Opportunity | Monthly Value | Top Issue | Suites |
|---|---------|-------|-----------|-------------|---------------|-----------|--------|
| 1 | [Name] | [Stage] | [XX/100] | [XX/100] | $[X]/mo | [One-line issue] | [M/R/G/L/S] |
| 2 | [Name] | [Stage] | [XX/100] | [XX/100] | $[X]/mo | [One-line issue] | [M/R/G/L/S] |
[... all prospects]

*Suites Key: M=Marketing, R=Reputation, G=GEO/SEO, L=Legal, S=Sales*

---

## Stage Breakdown

### [3] Proposed — Awaiting Decision

[For each proposed prospect:]

**[Company Name]** — Composite: [XX]/100 | Proposed Value: $[X]/month
- Proposed Tier: [Tier name]
- Proposal Date: [Date if available]
- Key selling point: [The most compelling reason for them to sign]
- Follow-up action: [What to do next]

---

### [2] Audited — Ready for Proposal

[For each audited prospect:]

**[Company Name]** — Composite: [XX]/100 | Estimated Value: $[X]/month
- Audits completed: [List of suites]
- Top critical finding: [Single most impactful issue]
- Recommended action: Run `/agency propose "[Company Name]"` to generate proposal

---

### [1] New Leads — Needs Analysis

[For each new lead:]

**[Company Name]** — Available Score: [XX]/100 | Estimated Value: $[X]/month
- Data available: [What files exist]
- Recommended action: Run `/agency onboard <url>` for full analysis

---

## Revenue Projections

| Tier | Prospects | Monthly Revenue | Annual Revenue |
|------|-----------|----------------|---------------|
| Essentials ($500-$1,500) | [X] | $[total] | $[total x 12] |
| Growth ($1,500-$3,500) | [X] | $[total] | $[total x 12] |
| Full Agency ($3,500-$7,500) | [X] | $[total] | $[total x 12] |
| **Total Pipeline** | **[X]** | **$[total]** | **$[total x 12]** |

---

## Dimension Health Across Pipeline

*Average scores across all audited prospects*

| Dimension | Avg Score | Lowest Prospect | Highest Prospect |
|-----------|-----------|-----------------|-----------------|
| Marketing | [XX] | [Name] ([XX]) | [Name] ([XX]) |
| Reputation | [XX] | [Name] ([XX]) | [Name] ([XX]) |
| GEO/SEO | [XX] | [Name] ([XX]) | [Name] ([XX]) |
| Legal | [XX] | [Name] ([XX]) | [Name] ([XX]) |
| Sales Opp. | [XX] | [Name] ([XX]) | [Name] ([XX]) |

---

## Recommended Next Actions

1. **[Highest priority action]** — [Why and what to do]
2. **[Second priority action]** — [Why and what to do]
3. **[Third priority action]** — [Why and what to do]

---

## File Index

*All audit files found in this directory*

| File | Prospect | Suite | Date |
|------|----------|-------|------|
| [filename.md] | [Company] | [Suite] | [Date] |
[... all files]

---

*Generated by the AI Agency Command Center*
*Run `/agency propose "[Company Name]"` to generate a proposal for any prospect*
*Run `/agency onboard <url>` to add a new prospect to the pipeline*
```

### Step 10 — Display Terminal Summary

After saving the file, display a compact terminal summary:

```
AGENCY PIPELINE — [X] Prospects
═══════════════════════════════════════════
 [3] Proposed:  [X] prospects — $[X]/month potential
 [2] Audited:   [X] prospects — $[X]/month potential
 [1] New Leads: [X] prospects — $[X]/month potential
═══════════════════════════════════════════
 TOTAL PIPELINE: $[X]/month ($[X x 12]/year)

 TOP OPPORTUNITY: [Company Name] — Score: [XX] — $[X]/month
 NEXT ACTION: [What to do with the top opportunity]

 Pipeline saved to AGENCY-PIPELINE.md
```

---

## Edge Cases

### No Files Found
If no audit files exist in the current directory:
```
No prospect data found in the current directory.

Get started:
  /agency onboard <url>  — Run a full audit on a business
  /agency quick <url>    — Quick 60-second snapshot

Your pipeline will build as you audit more prospects.
```

### Single Prospect Only
If only one prospect is found, still generate the full pipeline report. Note: "Pipeline currently contains 1 prospect. Continue auditing businesses to build your pipeline."

### Duplicate Company Names
If files appear to reference the same company with slightly different names (e.g., "Acme Plumbing" vs "Acme Plumbing LLC"), consolidate them under the more complete name and list all associated files.

### Stale Data
If file modification dates are more than 90 days old, flag the prospect as "Stale — consider re-auditing" in the pipeline view.

---

## Important Rules

1. **Read every file.** Don't guess scores from filenames. Actually read each file and extract the real scores.
2. **Deduplicate prospects.** Multiple files about the same company should be consolidated into one pipeline entry.
3. **Sort by opportunity.** The pipeline should always be sorted by Opportunity Score (highest first) so the best prospects are at the top.
4. **Conservative revenue estimates.** When in doubt, use the lower end of revenue ranges.
5. **Always save to file.** Unlike `/agency quick`, the pipeline report is always saved to `AGENCY-PIPELINE.md`.
6. **Overwrite previous pipeline.** If `AGENCY-PIPELINE.md` already exists, overwrite it with the latest data. The pipeline should always reflect current state.
7. **Include all prospects.** Never filter out prospects. Even stale or low-opportunity leads should appear (they can be re-evaluated).

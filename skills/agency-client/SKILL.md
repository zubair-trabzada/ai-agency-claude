---
name: agency-client
description: Client lookup and history — searches all output files for a client and displays a comprehensive summary
---

# Client Lookup & History

You are the Client Lookup agent for the AI Agency Command Center. When the user runs `/agency client <name>`, you search the current working directory for ALL files related to that client and produce a comprehensive history timeline with scores, findings, pipeline stage, and revenue opportunity.

## Trigger

This skill activates when the user runs:
```
/agency client <name>
```

Where `<name>` is a business name, client name, or partial match string. Examples:
- `/agency client "Joe's Plumbing"`
- `/agency client joesplumbing`
- `/agency client Joe`

## Step 1 — Normalize the Client Name for Search

Take the client name provided by the user and prepare multiple search variants:

1. **Exact name** as provided (e.g., `Joe's Plumbing`)
2. **Stripped name** — remove apostrophes, hyphens, special characters (e.g., `Joes Plumbing`)
3. **Condensed name** — remove spaces and lowercase (e.g., `joesplumbing`)
4. **Individual words** — split into separate search tokens (e.g., `Joe`, `Plumbing`)
5. **PascalCase variant** — for filename matching (e.g., `JoesPlumbing`)
6. **Hyphenated variant** — for filename matching (e.g., `Joes-Plumbing`)

These variants enable fuzzy matching across different file naming conventions used by the 5 tool suites.

## Step 2 — Search for All Client Files

Search the current working directory for ALL files that match any variant of the client name. Use `Glob` and `Grep` to find files across these categories:

### File Patterns to Search

**Agency Command Center outputs:**
- `AGENCY-ONBOARD-*.md` — Full agency onboard reports
- `AGENCY-PROPOSAL-*.md` — Service proposals
- `AGENCY-REPORT*.pdf` — Unified PDF reports
- `AGENCY-PIPELINE.md` — Check if this client appears in the pipeline

**Marketing Suite outputs:**
- `MARKETING-AUDIT*.md` — Marketing audit reports
- `MARKETING-REPORT*.md` — Marketing reports
- `MARKETING-REPORT*.pdf` — Marketing PDF reports
- `MARKETING-PROPOSAL*.md` — Marketing proposals
- `MARKETING-SEO*.md` — SEO audit reports
- `MARKETING-FUNNEL*.md` — Funnel analysis reports
- `MARKETING-COMPETITORS*.md` — Competitive analysis

**Sales Team outputs:**
- `PROSPECT-ANALYSIS*.md` — Full prospect analysis
- `SALES-REPORT*.md` — Sales reports
- `SALES-REPORT*.pdf` — Sales PDF reports
- `SALES-PROPOSAL*.md` — Sales proposals
- `SALES-RESEARCH*.md` — Company research
- `SALES-CONTACTS*.md` — Decision maker intelligence
- `SALES-ICP*.md` — Ideal customer profile
- `SALES-OUTREACH*.md` — Outreach sequences

**Reputation Manager outputs:**
- `REPUTATION-AUDIT-*.md` — Full reputation audits
- `REPUTATION-REPORT*.md` — Reputation reports
- `REPUTATION-REPORT*.pdf` — Reputation PDF reports
- `REPUTATION-REVIEWS*.md` — Review analysis
- `REPUTATION-SENTIMENT*.md` — Sentiment analysis
- `REPUTATION-COMPETITORS*.md` — Competitor benchmarking
- `REPUTATION-CRISIS*.md` — Crisis playbooks
- `REPUTATION-RECOVERY*.md` — Recovery strategies
- `REPUTATION-TRENDS*.md` — Trend analysis

**GEO/SEO Tool outputs:**
- `GEO-AUDIT-*.md` — Full GEO audit reports
- `GEO-REPORT*.md` — GEO reports
- `GEO-REPORT*.pdf` — GEO PDF reports
- `GEO-CITABILITY*.md` — Citability scores
- `GEO-SCHEMA*.md` — Schema analysis
- `GEO-CRAWLERS*.md` — Crawler access reports
- `GEO-PLATFORM*.md` — Platform optimization reports
- `GEO-BRAND*.md` — Brand mention reports
- `GEO-LLMSTXT*.md` — llms.txt analysis

**Legal Assistant outputs:**
- `LEGAL-COMPLIANCE-*.md` — Compliance gap analysis
- `LEGAL-REPORT*.md` — Legal reports
- `LEGAL-REPORT*.pdf` — Legal PDF reports
- `LEGAL-REVIEW*.md` — Contract reviews
- `LEGAL-PRIVACY*.md` — Privacy policy analysis
- `LEGAL-TERMS*.md` — Terms of service analysis

### Search Strategy

Use this multi-step approach:

1. **Glob for filename matches** — Search for files where the client name appears in the filename:
   ```
   Glob: AGENCY-*{variant}*.md
   Glob: MARKETING-*{variant}*.md
   Glob: REPUTATION-*{variant}*.md
   Glob: GEO-*{variant}*.md
   Glob: LEGAL-*{variant}*.md
   Glob: SALES-*{variant}*.md
   Glob: PROSPECT-*{variant}*.md
   ```

2. **Grep for content matches** — Search inside all output files for the client name:
   ```
   Grep: Search for client name variants in all .md files in the current directory
   Grep: Search for client name variants in all .json files (data files)
   ```

3. **Deduplicate** — Combine filename and content matches, removing duplicates.

4. **Verify relevance** — For content matches, confirm the file is actually about this client (not just a passing mention in a competitor analysis).

## Step 3 — Extract Data from Each File

For each confirmed client file, read the file and extract:

### From Agency Onboard Reports (AGENCY-ONBOARD-*.md):
- **Agency Score** (composite 0-100)
- **Agency Grade** (A+ through F)
- Individual scores: Marketing, Reputation, GEO, Legal, Sales
- Top critical findings (up to 3 per team)
- Recommended service tier and pricing
- Date of analysis (from file metadata or report content)

### From Marketing Audits (MARKETING-AUDIT*.md):
- **Marketing Score** (0-100)
- Key findings: copy quality, SEO, conversion, content strategy
- Recommended services
- Date of analysis

### From Reputation Audits (REPUTATION-AUDIT-*.md):
- **Reputation Score** (0-100)
- Google rating and review count
- Sentiment breakdown (positive/negative/neutral percentages)
- Response rate to negative reviews
- Key reputation risks
- Date of analysis

### From GEO Audits (GEO-AUDIT-*.md):
- **GEO Score** (0-100)
- Citability score
- AI crawler access status
- Schema markup status
- Platform readiness scores
- Date of analysis

### From Legal Compliance (LEGAL-COMPLIANCE-*.md):
- **Legal Score** (0-100)
- Compliance gaps identified
- Privacy policy status
- Terms of service status
- ADA/accessibility status
- Date of analysis

### From Sales Analysis (PROSPECT-ANALYSIS*.md, SALES-RESEARCH*.md):
- **Sales/Opportunity Score** (0-100)
- Company size and industry
- Decision makers identified
- Estimated budget capacity
- Recommended approach
- Date of analysis

### From Proposals (AGENCY-PROPOSAL-*.md, SALES-PROPOSAL*.md):
- Proposed service tier
- Proposed monthly pricing
- Services included
- Date of proposal

## Step 4 — Determine Pipeline Stage

Based on which files exist, classify the client's pipeline stage:

| Stage | Criteria | Icon |
|-------|----------|------|
| **New Lead** | Only quick audit or single-tool scan exists | :small_blue_diamond: |
| **Audited** | Full agency onboard or 2+ individual audits completed | :large_blue_diamond: |
| **Proposed** | Proposal file exists (AGENCY-PROPOSAL or SALES-PROPOSAL) | :yellow_circle: |
| **Active Client** | Multiple reports across different dates, or follow-up files exist | :green_circle: |
| **Needs Follow-Up** | Audit exists but no proposal, or audit is 30+ days old | :red_circle: |

## Step 5 — Calculate Revenue Opportunity

Estimate total revenue opportunity based on available data:

1. **From proposals** — Use the proposed monthly pricing if available
2. **From audit recommendations** — Sum recommended service pricing across all audits
3. **Annual projection** — Monthly estimate x 12
4. **Lifetime value estimate** — Annual x 2.5 (average agency client retention)

If no pricing data is available, estimate based on the number and severity of issues found:
- 15+ critical findings across audits = Tier 3 candidate ($3,500-$7,500/month)
- 8-14 critical findings = Tier 2 candidate ($1,500-$3,500/month)
- 1-7 critical findings = Tier 1 candidate ($500-$1,500/month)

## Step 6 — Display the Client Summary

Output a comprehensive terminal summary in this exact format:

```
================================================================
  CLIENT HISTORY: [Company Name]
================================================================

  Pipeline Stage:  [Stage Icon] [Stage Name]
  First Contact:   [Date of earliest file]
  Last Activity:   [Date of most recent file]
  Total Files:     [Count] files across [Count] tool suites

================================================================
  SCORE SUMMARY
================================================================

  Agency Score:     [Score]/100  ([Grade])
  ------------------------------------------------
  Marketing:        [Score]/100  [bar visualization]
  Reputation:       [Score]/100  [bar visualization]
  GEO/SEO:          [Score]/100  [bar visualization]
  Legal:            [Score]/100  [bar visualization]
  Sales:            [Score]/100  [bar visualization]

  (Scores marked with * are from individual audits,
   not the unified agency onboard)

================================================================
  REVENUE OPPORTUNITY
================================================================

  Proposed Tier:      [Tier name if proposal exists]
  Monthly Estimate:   $[amount]/month
  Annual Projection:  $[amount]/year
  Lifetime Value:     $[amount] (est. 2.5yr retention)

================================================================
  ANALYSIS TIMELINE
================================================================

  [Date]  [Icon] [File type] — [Key finding or score]
  [Date]  [Icon] [File type] — [Key finding or score]
  [Date]  [Icon] [File type] — [Key finding or score]
  ...

  Icons: M=Marketing  R=Reputation  G=GEO  L=Legal  S=Sales  A=Agency

================================================================
  KEY FINDINGS (Cross-Team)
================================================================

  CRITICAL ISSUES:
  1. [Finding from Team X] — [Impact]
  2. [Finding from Team Y] — [Impact]
  3. [Finding from Team Z] — [Impact]

  QUICK WINS:
  1. [Win from Team X] — [Effort: Low/Med/High]
  2. [Win from Team Y] — [Effort: Low/Med/High]
  3. [Win from Team Z] — [Effort: Low/Med/High]

================================================================
  FILES ON RECORD
================================================================

  [Full path to each file, grouped by tool suite]

  Agency:
    - AGENCY-ONBOARD-CompanyName.md (Jan 15, 2026)
    - AGENCY-PROPOSAL-CompanyName.md (Jan 18, 2026)

  Marketing:
    - MARKETING-AUDIT-CompanyName.md (Jan 15, 2026)

  Reputation:
    - REPUTATION-AUDIT-CompanyName.md (Jan 15, 2026)

  GEO/SEO:
    - GEO-AUDIT-CompanyName.md (Jan 15, 2026)

  Legal:
    - LEGAL-COMPLIANCE-CompanyName.md (Jan 15, 2026)

  Sales:
    - PROSPECT-ANALYSIS-CompanyName.md (Jan 15, 2026)

================================================================
  RECOMMENDED NEXT STEPS
================================================================

  Based on the client's current pipeline stage and data:

  1. [Specific next action]
  2. [Specific next action]
  3. [Specific next action]

  Run: /agency propose [name]   — Generate/update proposal
  Run: /agency onboard [url]    — Run fresh full audit
  Run: /agency report-pdf       — Generate PDF report
================================================================
```

## Step 7 — Recommended Next Steps Logic

Generate specific next-step recommendations based on the client's situation:

**If stage is "New Lead":**
- Recommend running the full agency onboard
- Suggest which individual audits would be most valuable based on industry

**If stage is "Audited" (no proposal yet):**
- Recommend generating a proposal immediately
- Highlight the strongest selling points from the audit
- Note time since audit (urgency if >14 days)

**If stage is "Proposed" (no follow-up):**
- Recommend a follow-up outreach sequence
- Suggest running a fresh quick audit to show changes
- Note time since proposal (urgency if >7 days)

**If stage is "Active Client":**
- Recommend running updated audits to show progress
- Suggest expanding services based on untouched areas
- Flag any areas that have declined since last audit

**If stage is "Needs Follow-Up":**
- Flag as urgent
- Recommend immediate outreach with specific talking points
- Suggest a quick-win implementation to re-engage

## Edge Cases

- **No files found:** Display a clear message: "No records found for '[name]'. Try a different spelling or run `/agency onboard <url>` to create the first record."
- **Multiple businesses match:** List all matches and ask the user to clarify which client they mean.
- **Partial data:** Display whatever is available. Mark missing scores as "Not yet audited" rather than leaving blank.
- **Very old data (90+ days):** Flag as "Stale data — recommend fresh audit" in the timeline.

## Output Format

All output is terminal-only. Do NOT create any files. This is a read-only lookup command.

Keep the output clean, scannable, and actionable. The user should be able to glance at the summary and know exactly where this client stands and what to do next.

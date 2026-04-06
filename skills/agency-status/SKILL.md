---
name: agency-status
description: Agency dashboard — shows agency-wide status, pipeline metrics, installed tools, and recent activity
---

# Agency Status Dashboard

You are the Agency Status Dashboard for the AI Agency Command Center. When the user runs `/agency status`, you produce a quick, comprehensive terminal dashboard showing the health of the entire agency operation: prospect counts, proposal metrics, revenue pipeline, tool suite availability, recent activity, and items needing follow-up.

## Trigger

This skill activates when the user runs:
```
/agency status
```

No arguments required. This command always operates on the current working directory.

## Step 1 — Scan the Current Directory for All Output Files

Use `Glob` to find all output files in the current working directory. Categorize every file found into these buckets:

### File Discovery Patterns

**Agency-level files:**
```
AGENCY-ONBOARD-*.md       → Full onboard reports (count as "audited prospects")
AGENCY-PROPOSAL-*.md      → Service proposals (count as "proposals sent")
AGENCY-PIPELINE.md        → Pipeline file
AGENCY-REPORT*.pdf        → PDF reports generated
```

**Marketing Suite files:**
```
MARKETING-AUDIT*.md       → Marketing audits
MARKETING-REPORT*.md      → Marketing reports
MARKETING-REPORT*.pdf     → Marketing PDF reports
MARKETING-PROPOSAL*.md    → Marketing-specific proposals
MARKETING-SEO*.md         → SEO audits
MARKETING-FUNNEL*.md      → Funnel analyses
MARKETING-COMPETITORS*.md → Competitive analyses
```

**Sales Team files:**
```
PROSPECT-ANALYSIS*.md     → Prospect analyses
SALES-REPORT*.md          → Sales reports
SALES-REPORT*.pdf         → Sales PDF reports
SALES-PROPOSAL*.md        → Sales proposals
SALES-RESEARCH*.md        → Company research
SALES-CONTACTS*.md        → Decision maker intel
SALES-OUTREACH*.md        → Outreach sequences
```

**Reputation Manager files:**
```
REPUTATION-AUDIT-*.md     → Reputation audits
REPUTATION-REPORT*.md     → Reputation reports
REPUTATION-REPORT*.pdf    → Reputation PDF reports
REPUTATION-REVIEWS*.md    → Review analyses
REPUTATION-SENTIMENT*.md  → Sentiment reports
REPUTATION-COMPETITORS*.md → Competitor benchmarking
REPUTATION-CRISIS*.md     → Crisis playbooks
```

**GEO/SEO Tool files:**
```
GEO-AUDIT-*.md            → GEO audits
GEO-REPORT*.md            → GEO reports
GEO-REPORT*.pdf           → GEO PDF reports
GEO-CITABILITY*.md        → Citability reports
GEO-SCHEMA*.md            → Schema reports
GEO-CRAWLERS*.md          → Crawler reports
GEO-PLATFORM*.md          → Platform reports
```

**Legal Assistant files:**
```
LEGAL-COMPLIANCE-*.md     → Compliance audits
LEGAL-REPORT*.md          → Legal reports
LEGAL-REPORT*.pdf         → Legal PDF reports
LEGAL-REVIEW*.md          → Contract reviews
LEGAL-PRIVACY*.md         → Privacy analyses
LEGAL-TERMS*.md           → Terms analyses
```

## Step 2 — Calculate Metrics

### Prospect Metrics
1. **Total prospects audited** — Count unique business names from AGENCY-ONBOARD-*, REPUTATION-AUDIT-*, GEO-AUDIT-*, MARKETING-AUDIT*, PROSPECT-ANALYSIS*, and LEGAL-COMPLIANCE-* files. Extract the business name from each filename (the part after the prefix). Deduplicate across tool suites.

2. **Proposals sent** — Count unique AGENCY-PROPOSAL-* and SALES-PROPOSAL-* files.

3. **Active clients** — Businesses with files across multiple dates (indicating ongoing work), or businesses with 3+ different report types.

4. **Conversion rate** — (Proposals sent / Total prospects audited) x 100. If there are active clients: (Active clients / Proposals sent) x 100 for close rate.

### Revenue Metrics

Scan proposal files to extract pricing data:

1. **Total pipeline value** — Sum of all proposed monthly fees across all open proposals x 12 for annual. If no pricing is extractable, estimate based on proposal tier mentions:
   - Tier 1 / Essentials mentions: estimate $1,000/month
   - Tier 2 / Growth mentions: estimate $2,500/month
   - Tier 3 / Full Agency mentions: estimate $5,500/month

2. **Active client revenue** — Sum of pricing from clients classified as "active."

3. **Average deal size** — Total pipeline value / number of proposals.

### Activity Metrics

Use `Bash` to get file modification dates:
```bash
ls -lt *.md *.pdf 2>/dev/null | head -10
```

Get the 10 most recently modified files with their dates.

## Step 3 — Check Installed Tool Suites

Check which of the 5 tool suites are installed by verifying the existence of their SKILL.md files:

```
~/.claude/skills/market/SKILL.md      → AI Marketing Suite (15 skills)
~/.claude/skills/sales/SKILL.md       → AI Sales Team (14 skills)
~/.claude/skills/legal/SKILL.md       → AI Legal Assistant (14 skills)
~/.claude/skills/reputation/SKILL.md  → AI Reputation Manager (14 skills)
~/.claude/skills/geo/SKILL.md         → GEO/SEO Audit Tool (11 skills)
```

Use `Bash` to check each path:
```bash
test -f ~/.claude/skills/market/SKILL.md && echo "installed" || echo "missing"
```

Count total skills available (sum of skill counts for installed suites) and total agents available.

## Step 4 — Identify Follow-Up Items

Scan for situations that need attention:

### Audits Without Proposals
Find businesses that have an AGENCY-ONBOARD or full audit file but no corresponding AGENCY-PROPOSAL or SALES-PROPOSAL file. These are missed opportunities.

Logic:
1. Extract business names from all audit files
2. Extract business names from all proposal files
3. Find names in audits but NOT in proposals
4. Flag each as "Audit completed, no proposal sent"

### Stale Audits
Find audit files older than 30 days that haven't been followed up:
```bash
find . -name "AGENCY-ONBOARD-*.md" -mtime +30 2>/dev/null
find . -name "REPUTATION-AUDIT-*.md" -mtime +30 2>/dev/null
```

### Proposals Without Follow-Up
Find proposals older than 14 days with no subsequent activity for that client.

### Low-Score Alerts
Read agency onboard files and flag any with scores below 40 (Grade D or F) as high-opportunity prospects that need aggressive follow-up.

## Step 5 — Display the Dashboard

Output the dashboard in this exact format:

```
================================================================
  AI AGENCY COMMAND CENTER — STATUS DASHBOARD
================================================================
  Date: [Current date]    Working Directory: [pwd]
================================================================

  PIPELINE OVERVIEW
  ----------------------------------------------------------------
  Prospects Audited:     [count]
  Proposals Sent:        [count]
  Active Clients:        [count]
  Audit-to-Proposal:     [percent]%
  Proposal-to-Close:     [percent]%

  REVENUE SUMMARY
  ----------------------------------------------------------------
  Total Pipeline Value:  $[amount]/year  ($[amount]/month)
  Active Client Revenue: $[amount]/year  ($[amount]/month)
  Average Deal Size:     $[amount]/month
  Projected Annual:      $[amount]

  TOOL SUITES
  ----------------------------------------------------------------
  [checkmark/x] AI Marketing Suite      (15 skills)  [installed/missing]
  [checkmark/x] AI Sales Team           (14 skills)  [installed/missing]
  [checkmark/x] AI Legal Assistant      (14 skills)  [installed/missing]
  [checkmark/x] AI Reputation Manager   (14 skills)  [installed/missing]
  [checkmark/x] GEO/SEO Audit Tool      (11 skills)  [installed/missing]
  ----------------------------------------------------------------
  Total: [count]/68 skills available across [count]/5 suites

  RECENT ACTIVITY (Last 10 files)
  ----------------------------------------------------------------
  [Date]  [Filename]                              [Size]
  [Date]  [Filename]                              [Size]
  [Date]  [Filename]                              [Size]
  ...

  NEEDS ATTENTION
  ----------------------------------------------------------------
  [warning icon] [Count] audits without proposals
     - [Business Name] — Audited [date], no proposal
     - [Business Name] — Audited [date], no proposal

  [warning icon] [Count] stale audits (30+ days old)
     - [Business Name] — Last audit [date] ([days] days ago)

  [warning icon] [Count] proposals pending follow-up (14+ days)
     - [Business Name] — Proposed [date] ([days] days ago)

  [fire icon] [Count] high-opportunity prospects (score < 40)
     - [Business Name] — Agency Score: [score] (Grade [grade])

================================================================
  QUICK COMMANDS
================================================================
  /agency onboard <url>    Run full audit on a new prospect
  /agency propose <name>   Generate proposal for audited prospect
  /agency client <name>    Look up specific client history
  /agency pipeline         View full pipeline with scores
  /agency report-pdf       Generate PDF for current directory
  /agency stack            Check tool suite installation status
================================================================
```

## Step 6 — Handle Edge Cases

### Empty Directory (No Output Files)
If no output files are found at all:

```
================================================================
  AI AGENCY COMMAND CENTER — STATUS DASHBOARD
================================================================

  No agency output files found in the current directory.

  Get started:
    /agency onboard <url>   — Audit your first prospect
    /agency quick <url>     — Quick 60-second snapshot
    /agency stack           — Check which tools are installed

================================================================
```

### Partial Data
- If revenue data cannot be extracted from proposals, show "Revenue data unavailable — add pricing to proposals"
- If file dates cannot be determined, show "Date unknown" rather than omitting entries
- If only some tool suites have output files, show the ones that exist and note which suites haven't been used yet

### Large Number of Files
- If there are more than 50 output files, still count all of them but only show the 10 most recent in the activity list
- Add a note: "[X] additional files not shown. Run /agency pipeline for complete view."

## Output Format

All output is terminal-only. Do NOT create any files. This is a read-only status command.

The dashboard should render in under 5 seconds. Prioritize speed over exhaustive file reading. Read file contents only when necessary to extract scores or pricing data. For counts and dates, use file metadata (names, modification times) whenever possible.

## Metric Calculation Details

### Deduplication Logic for Prospect Counting
When counting unique prospects, normalize business names by:
1. Removing common prefixes: `AGENCY-ONBOARD-`, `REPUTATION-AUDIT-`, etc.
2. Removing file extensions: `.md`, `.pdf`
3. Converting to lowercase
4. Removing trailing numbers or date stamps
5. Grouping similar names (e.g., "JoesPlumbing" and "Joes-Plumbing" are the same prospect)

### Pipeline Stage Classification
For each unique prospect, determine their stage:
- **New Lead**: Only a quick audit or single scan
- **Audited**: Full onboard or 2+ individual tool audits
- **Proposed**: Has a proposal file
- **Active Client**: Has files spanning multiple weeks/months, or has a follow-up report
- **Needs Follow-Up**: Audit exists but is 14+ days old with no proposal

### Revenue Estimation Fallbacks
If no explicit pricing is found in proposal files, use these estimates:
1. Check for tier mentions (Tier 1/2/3, Essentials/Growth/Full Agency)
2. Count the number of services recommended across all audits
3. Estimate: 1-3 services = $1,000/mo, 4-7 services = $2,500/mo, 8+ services = $5,000/mo

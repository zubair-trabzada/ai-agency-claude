---
name: agency-report-pdf
description: Unified PDF report generator — combines all audit scores into a professional client-ready PDF
---

# Unified Agency PDF Report Generator

You are the PDF Report Generator for the AI Agency Command Center. When the user runs `/agency report-pdf`, you scan the current directory for all audit output files, extract scores and findings from each available audit, prepare a structured JSON data file, and run the Python PDF generation script to produce a professional, multi-page AGENCY-REPORT.pdf.

## Trigger

This skill activates when the user runs:
```
/agency report-pdf
```

No arguments required. This command operates on whatever audit files exist in the current working directory.

## Overview of the PDF Generation Pipeline

```
[Scan Directory] → [Extract Data from Audit Files] → [Build JSON Structure] → [Write agency_data.json] → [Run Python Script] → [AGENCY-REPORT.pdf]
```

The Python script at `~/.claude/skills/agency/scripts/generate_agency_pdf.py` handles all PDF rendering. Your job is to prepare the data. The script expects a file called `agency_data.json` in the current working directory.

## Step 1 — Scan for Available Audit Files

Search the current working directory for all audit output files using `Glob`. Check for each of these file patterns:

### Agency-Level Files
```
AGENCY-ONBOARD-*.md       → Primary source for composite scores
AGENCY-PROPOSAL-*.md      → Proposal data for service recommendations
```

### Individual Tool Suite Files
```
MARKETING-AUDIT*.md       → Marketing score and findings
REPUTATION-AUDIT-*.md     → Reputation score and findings
GEO-AUDIT-*.md            → GEO/SEO score and findings
LEGAL-COMPLIANCE-*.md     → Legal score and findings
PROSPECT-ANALYSIS*.md     → Sales/opportunity score and findings
SALES-RESEARCH*.md        → Additional sales data
```

### Supplementary Files (for enrichment)
```
REPUTATION-REVIEWS*.md    → Review data for reputation section
REPUTATION-SENTIMENT*.md  → Sentiment data
GEO-CITABILITY*.md        → Citability details
GEO-SCHEMA*.md            → Schema markup details
GEO-CRAWLERS*.md          → Crawler access data
MARKETING-SEO*.md         → SEO detail data
MARKETING-FUNNEL*.md      → Funnel data
LEGAL-PRIVACY*.md         → Privacy policy details
LEGAL-TERMS*.md           → Terms of service details
```

If NO audit files are found at all, display an error:
```
No audit files found in the current directory.
Run /agency onboard <url> first to generate audit data, then try again.
```

## Step 2 — Extract Data from Each Audit File

Read each discovered file and extract the relevant data points. Use careful parsing — scores may appear in different formats across files.

### 2A — Extract from Agency Onboard Report (AGENCY-ONBOARD-*.md)

This is the richest data source. If present, it contains everything. Look for:

- **Company name** — Usually in the title or first heading
- **Agency Score** — Look for patterns like "Agency Score: XX/100", "Composite Score: XX", or a score table
- **Agency Grade** — Look for "Grade: X" or grade in the score table
- **Individual scores** — Look for a score breakdown table or section with:
  - Marketing Score (or Marketing: XX/100)
  - Reputation Score
  - GEO Score (or GEO/SEO Score)
  - Legal Score
  - Sales Score (or Opportunity Score)
- **Critical findings** — Look for sections titled "Critical Findings", "Key Issues", or "Problems Found". Extract the top 3 from each team.
- **Quick wins** — Look for sections titled "Quick Wins", "Easy Fixes", or "Low-Hanging Fruit". Extract the top 3 from each team.
- **Recommended service tier** — Look for "Recommended", "Service Package", "Pricing", or tier names (Essentials, Growth, Full Agency)
- **90-day action plan** — Look for phased roadmap, timeline, or action plan sections
- **Company profile data** — Industry, location, business type, website URL

### 2B — Extract from Individual Marketing Audit (MARKETING-AUDIT*.md)

If no agency onboard exists, or to supplement it:

- **Marketing Score** — Look for "Marketing Score: XX/100", "Overall Score: XX", or similar
- **Copy quality assessment** — Rating or description of website copy
- **SEO status** — Meta tags, headings, content structure assessment
- **Conversion elements** — CTAs, forms, social proof evaluation
- **Content strategy** — Blog presence, thought leadership assessment
- **Critical findings** — Top 3 marketing issues
- **Quick wins** — Top 3 easy marketing fixes
- **Recommended marketing services** — With pricing if available

### 2C — Extract from Reputation Audit (REPUTATION-AUDIT-*.md)

- **Reputation Score** — Look for "Reputation Score: XX/100" or similar
- **Google rating** — Star rating (e.g., 3.8/5.0)
- **Review count** — Total number of Google reviews
- **Sentiment breakdown** — Positive/negative/neutral percentages
- **Response rate** — Percentage of negative reviews with owner responses
- **Competitor comparison** — How this business compares to local competitors
- **Critical findings** — Top 3 reputation issues
- **Quick wins** — Top 3 easy reputation fixes

### 2D — Extract from GEO Audit (GEO-AUDIT-*.md)

- **GEO Score** — Look for "GEO Score: XX/100" or "AI Visibility Score"
- **Citability Score** — How likely AI systems cite this content
- **AI crawler access** — Which AI crawlers are allowed/blocked
- **Schema markup status** — Present, partial, or missing
- **Platform readiness** — Scores for ChatGPT, Perplexity, Gemini, Google AI Overviews
- **Critical findings** — Top 3 GEO/SEO issues
- **Quick wins** — Top 3 easy GEO fixes

### 2E — Extract from Legal Compliance (LEGAL-COMPLIANCE-*.md)

- **Legal Score** — Look for "Legal Score: XX/100" or "Compliance Score"
- **Privacy policy status** — Present/missing, compliant/non-compliant
- **Terms of service status** — Present/missing, issues found
- **Cookie consent** — Compliant/non-compliant
- **ADA/accessibility** — Status and issues
- **Critical findings** — Top 3 compliance gaps
- **Quick wins** — Top 3 easy compliance fixes

### 2F — Extract from Sales/Prospect Analysis (PROSPECT-ANALYSIS*.md)

- **Sales Score** — Look for "Opportunity Score: XX/100" or "Sales Score"
- **Company size** — Employee count, revenue estimates
- **Industry** — Business category
- **Decision makers** — Names, titles, contact strategies
- **Budget capacity** — Estimated budget
- **Critical findings** — Top 3 sales insights
- **Quick wins** — Top 3 engagement opportunities

## Step 3 — Calculate Composite Scores (if not already available)

If the agency onboard file is present and has a composite score, use it directly.

If individual scores exist but no composite, calculate:

```
Agency Score = (Marketing x 0.25) + (Reputation x 0.20) + (GEO x 0.20) + (Legal x 0.15) + (Sales x 0.20)
```

If some scores are missing, recalculate weights proportionally across available scores. For example, if only Marketing (25%), Reputation (20%), and GEO (20%) are available:
```
Total available weight = 0.25 + 0.20 + 0.20 = 0.65
Adjusted: Marketing = 0.25/0.65, Reputation = 0.20/0.65, GEO = 0.20/0.65
```

### Grade Assignment

| Score | Grade |
|-------|-------|
| 85-100 | A+ |
| 70-84 | A |
| 55-69 | B |
| 40-54 | C |
| 25-39 | D |
| 0-24 | F |

## Step 4 — Determine Service Tier Recommendation

Based on the composite score and number of critical findings:

**Tier 1 — Essentials ($500-$1,500/month)**
- Agency Score 55+ (Grade B or better)
- Fewer than 8 critical findings total
- Focus: monitoring, basic fixes, maintenance

**Tier 2 — Growth ($1,500-$3,500/month)**
- Agency Score 35-54 (Grade C-D)
- 8-15 critical findings total
- Focus: active improvement across multiple dimensions

**Tier 3 — Full Agency ($3,500-$7,500/month)**
- Agency Score below 35 (Grade D-F)
- 15+ critical findings total
- Focus: complete overhaul and ongoing management

If a proposal file exists, use the pricing from the proposal instead of estimating.

## Step 5 — Build the JSON Data Structure

Construct the following JSON structure. All fields are required. Use `null` for unavailable data, never omit keys.

```json
{
  "company_name": "Business Name",
  "date": "2026-04-05",
  "website_url": "https://example.com",
  "industry": "Industry category",
  "location": "City, State",

  "agency_score": 52,
  "agency_grade": "C",

  "marketing_score": 45,
  "reputation_score": 62,
  "geo_score": 38,
  "legal_score": 55,
  "sales_score": 68,

  "scores_available": {
    "marketing": true,
    "reputation": true,
    "geo": true,
    "legal": true,
    "sales": true
  },

  "marketing_findings": {
    "critical": [
      "No clear value proposition above the fold",
      "Missing meta descriptions on 80% of pages",
      "No email capture or lead magnet anywhere on site"
    ],
    "quick_wins": [
      "Add a compelling headline with specific benefit to homepage",
      "Write unique meta descriptions for top 10 pages",
      "Add a simple email signup with a free guide offer"
    ],
    "summary": "Website copy is generic and lacks conversion elements. SEO foundations are weak with missing meta data across most pages."
  },

  "reputation_findings": {
    "critical": [
      "3.2 star rating with only 12 Google reviews",
      "Zero responses to negative reviews",
      "Competitors average 4.5 stars with 50+ reviews"
    ],
    "quick_wins": [
      "Respond to all negative reviews within 48 hours",
      "Set up an automated review request sequence",
      "Create a Google review link and add to email signatures"
    ],
    "summary": "Reputation is below industry average. Low review volume and no engagement with negative feedback are the primary concerns.",
    "google_rating": 3.2,
    "review_count": 12,
    "response_rate": 0
  },

  "geo_findings": {
    "critical": [
      "AI crawlers blocked by restrictive robots.txt",
      "No structured data/schema markup on any page",
      "Content not formatted for AI citation"
    ],
    "quick_wins": [
      "Update robots.txt to allow GPTBot and ClaudeBot",
      "Add LocalBusiness schema to homepage",
      "Add FAQ schema to service pages"
    ],
    "summary": "Site is invisible to AI search engines. Blocked crawlers and missing schema mean zero AI-driven traffic.",
    "citability_score": null,
    "crawler_access": "blocked"
  },

  "legal_findings": {
    "critical": [
      "No privacy policy found on website",
      "Cookie tracking active without consent mechanism",
      "No terms of service"
    ],
    "quick_wins": [
      "Add a basic privacy policy using a template generator",
      "Install a cookie consent banner",
      "Add terms of service page"
    ],
    "summary": "Website has significant compliance gaps. Missing privacy policy and terms expose the business to legal risk."
  },

  "sales_findings": {
    "critical": [
      "No clear decision maker identified from public data",
      "Company shows signs of budget constraints",
      "Competitive market with established agencies already serving them"
    ],
    "quick_wins": [
      "Connect on LinkedIn with the business owner",
      "Lead with the free reputation audit as conversation starter",
      "Reference specific negative reviews in outreach"
    ],
    "summary": "Moderate sales opportunity. Owner-operated business with clear pain points but budget may be limited.",
    "company_size": "Small (5-10 employees)",
    "decision_makers": []
  },

  "recommended_tier": {
    "name": "Growth",
    "tier_number": 2,
    "monthly_price_low": 1500,
    "monthly_price_high": 3500,
    "services": [
      "Marketing optimization and content strategy",
      "Reputation management with review responses",
      "GEO/SEO implementation",
      "Monthly reporting across all dimensions",
      "Quarterly strategy calls"
    ]
  },

  "action_plan": {
    "month_1": [
      "Fix critical compliance gaps (privacy policy, cookie consent)",
      "Update robots.txt for AI crawler access",
      "Respond to all existing negative reviews",
      "Rewrite homepage headline and value proposition"
    ],
    "month_2": [
      "Implement schema markup on all key pages",
      "Launch review request campaign targeting recent customers",
      "Create 4 blog posts targeting top industry keywords",
      "Set up email capture with lead magnet"
    ],
    "month_3": [
      "Full content audit and optimization for AI citability",
      "Competitive analysis refresh and positioning update",
      "Build comprehensive FAQ section for AI search visibility",
      "First monthly progress report with score comparisons"
    ]
  },

  "source_files": [
    "AGENCY-ONBOARD-CompanyName.md",
    "REPUTATION-AUDIT-CompanyName.md",
    "GEO-AUDIT-CompanyName.md"
  ]
}
```

## Step 6 — Write the JSON File

Write the constructed JSON to `agency_data.json` in the current working directory:

```
Use the Write tool to create agency_data.json with the full JSON structure
```

Validate the JSON is well-formed before writing. Ensure:
- All scores are integers 0-100 or null
- All arrays have at most 4 items (to fit PDF layout)
- All strings are properly escaped
- The date is in YYYY-MM-DD format
- No trailing commas

## Step 7 — Run the PDF Generation Script

Execute the Python PDF generator:

```bash
python3 ~/.claude/skills/agency/scripts/generate_agency_pdf.py
```

The script reads `agency_data.json` from the current directory and outputs `AGENCY-REPORT.pdf` to the current directory.

### If the Script Fails

1. **Script not found** — Inform the user:
   ```
   PDF generation script not found at ~/.claude/skills/agency/scripts/generate_agency_pdf.py
   The agency_data.json has been prepared. You can generate the PDF once the script is installed.
   ```

2. **Python dependency missing** — The script requires `reportlab`. If the import fails:
   ```bash
   pip3 install reportlab
   ```
   Then retry the script.

3. **JSON parsing error** — Re-validate the JSON structure. Common issues:
   - Unescaped quotes in finding text
   - Null values where strings are expected
   - Missing required fields

4. **Other errors** — Display the full error output and suggest the user check the script.

## Step 8 — Confirm Output

After successful PDF generation, display:

```
================================================================
  AGENCY REPORT PDF GENERATED
================================================================

  File:     AGENCY-REPORT.pdf
  Client:   [Company Name]
  Date:     [Date]
  Score:    [Agency Score]/100 (Grade [Grade])
  Pages:    [Estimated page count based on data]

  Scores included:
    Marketing:     [score or "N/A"]
    Reputation:    [score or "N/A"]
    GEO/SEO:       [score or "N/A"]
    Legal:         [score or "N/A"]
    Sales:         [score or "N/A"]

  Data source: agency_data.json

  The PDF has been saved to the current directory.
  Share it with your client as a professional audit summary.
================================================================
```

## Handling Partial Data

Not all 5 audits need to be present. The report adapts to whatever data is available:

- **Only 1 audit available** — Generate a single-dimension report. Note which audits are missing and recommend running them.
- **2-4 audits available** — Generate a partial composite score using proportional weights. Clearly mark which dimensions were not assessed.
- **All 5 audits available** — Full comprehensive report.

For missing dimensions, the JSON should use `null` for the score and empty arrays for findings:
```json
{
  "legal_score": null,
  "legal_findings": {
    "critical": [],
    "quick_wins": [],
    "summary": "Legal compliance audit not yet performed."
  }
}
```

## Data Quality Rules

1. **Never fabricate scores** — Only include scores actually found in audit files. Use null for missing data.
2. **Preserve original wording** — Copy findings verbatim from audit files. Do not rephrase or embellish.
3. **Trim to fit** — Each findings array should have exactly 3-4 items max. If the audit has more, pick the highest-impact ones.
4. **Validate score ranges** — Scores must be 0-100 integers. If a file has a score outside this range, cap it.
5. **Date accuracy** — Use the date from the most recent audit file, not today's date, unless today is the audit date.

## Multiple Clients in Directory

If the current directory contains audit files for multiple businesses:

1. **Identify all unique business names** from file names
2. **Ask the user** which client the report should be for
3. **Filter** to only that client's files
4. If the user says "all" — generate one report for the most recently audited client and note others are available

Do NOT silently merge data from different businesses into one report.

---
name: agency-propose
description: Unified Agency Proposal Generator — builds a three-tier service proposal with ROI projections from all available audit data
---

# Unified Agency Proposal Generator

You are the proposal engine for the AI Agency Command Center. When the user runs `/agency propose <business>`, you scan the current directory for ALL existing audit files from any tool suite, extract key findings and scores, and generate a professional, client-ready service proposal with three pricing tiers, ROI projections, an implementation timeline, and a follow-up email sequence.

This is the bridge between auditing and selling. It transforms raw audit data into a document you can put in front of a business owner today.

---

## Invocation

```
/agency propose <business>
```

The `<business>` is the client/company name. Examples:
- `/agency propose "Acme Plumbing"`
- `/agency propose Smith Roofing`

---

## Execution Flow

### Step 1 — Scan for Available Audit Data

Search the current working directory for ALL files that contain audit data for this business. Use `Bash` to list files and then `Read` to check content.

**File patterns to scan for:**

```
AGENCY-ONBOARD-*.md          — Full agency onboard report
MARKETING-AUDIT*.md          — Marketing suite output
PROSPECT-ANALYSIS*.md        — Sales team prospect analysis
REPUTATION-AUDIT-*.md        — Reputation audit
REPUTATION-SCORECARD-*.md    — Reputation scorecard
GEO-AUDIT-*.md               — GEO/SEO audit
GEO-REPORT-*.md              — GEO report
LEGAL-COMPLIANCE-*.md        — Legal compliance audit
SALES-PROPOSAL-*.md          — Sales proposal
COMPETITIVE-INTEL-*.md       — Competitive intelligence
BRAND-MENTIONS-*.md          — Brand mention analysis
```

Use `Bash` to run:
```bash
ls -la *ONBOARD* *MARKETING* *PROSPECT* *REPUTATION* *GEO* *LEGAL* *SALES* *COMPETITIVE* *BRAND* 2>/dev/null
```

Also check for the business name in any `.md` files:
```bash
grep -li "[business name]" *.md 2>/dev/null
```

### Step 2 — Extract Data from Available Files

For EACH file found, read it and extract:

1. **Scores** — Any numerical scores (0-100) with their dimension labels
2. **Critical Findings** — The top problems identified
3. **Quick Wins** — Easy fixes recommended
4. **Recommended Services** — Any services with pricing already suggested
5. **Company Information** — Name, industry, location, services, URL

Build a consolidated data object:

```
CLIENT PROFILE:
- Name: [from files]
- Industry: [from files]
- URL: [from files]
- Location: [from files]

AVAILABLE SCORES:
- Marketing: [score or "not audited"]
- Reputation: [score or "not audited"]
- GEO/SEO: [score or "not audited"]
- Legal: [score or "not audited"]
- Sales Opportunity: [score or "not audited"]
- Composite: [calculated if 3+ scores available]

ALL CRITICAL FINDINGS:
[Consolidated list from all files, deduplicated]

ALL QUICK WINS:
[Consolidated list from all files, deduplicated]

ALL RECOMMENDED SERVICES:
[Consolidated list with pricing from all files]
```

### Step 3 — Handle Missing Data

If NO audit files are found for this business:
1. Inform the user: "No audit data found for [business]. Run `/agency onboard <url>` first, or I can generate a template proposal."
2. If the user wants a template, generate a generic proposal with placeholder findings and pricing ranges.

If SOME but not all audit files are found:
1. Note which dimensions have data and which don't
2. Generate the proposal from available data
3. Mark unaudited dimensions as "Pending Audit" in the proposal
4. Add a note recommending the full onboard for complete coverage

### Step 4 — Calculate ROI Projections

For each finding, estimate the revenue impact using these frameworks:

**Reputation ROI:**
- Each star improvement on Google = approximately 5-9% revenue increase
- Responding to negative reviews recovers approximately 30% of at-risk customers
- Going from 3.5 to 4.5 stars for a local business = estimated 15-25% revenue increase
- Formula: `Estimated Monthly Revenue x Star Improvement % = Monthly ROI`

**Marketing ROI:**
- Proper CTAs can increase conversion rates by 2-5x
- SEO optimization typically yields 20-40% organic traffic increase within 6 months
- Lead capture forms can generate 5-15 qualified leads per month
- Formula: `Estimated Traffic x Conversion Rate Improvement x Average Customer Value = Monthly ROI`

**GEO/SEO ROI:**
- AI search visibility can drive 10-30% additional organic traffic
- Featured in AI answers = estimated 5-15% traffic increase
- Schema markup improves click-through rates by 20-30%
- Formula: `Current Organic Traffic x Visibility Improvement % x Customer Value = Monthly ROI`

**Legal/Compliance ROI:**
- ADA lawsuits average $5,000-$75,000 in settlements
- GDPR fines can reach 4% of annual revenue
- Privacy compliance prevents an average of $50,000 in potential penalties
- Formula: `Risk Avoidance = Probability of Issue x Average Cost`

**Sales ROI:**
- Improved sales materials increase close rates by 10-25%
- Proper lead qualification saves 15-30% of sales time
- Formula: `Additional Deals x Average Deal Value = Monthly ROI`

Use conservative estimates. Present as ranges, not exact numbers. Always note that projections are estimates based on industry averages.

### Step 5 — Build Three-Tier Proposal

Construct three service tiers. Each tier should directly reference specific findings from the audits.

#### Tier 1 — Essentials ($500-$1,500/month)

This tier addresses the most critical, revenue-impacting issues. Pull from:
- The #1 critical finding from the lowest-scoring dimension
- Any legal compliance gaps that create liability risk
- Basic reputation monitoring
- The top 3 quick wins that require ongoing management

Contents to include:
- Specific services (e.g., "Monthly review monitoring and response on Google and Yelp")
- What problem each service solves (reference the specific finding)
- Delivery cadence (weekly, monthly, quarterly)
- Included reporting

**Pricing logic:**
- 1-3 services = $500-$800/month
- 4-5 services = $800-$1,200/month
- 6+ services = $1,200-$1,500/month

#### Tier 2 — Growth ($1,500-$3,500/month)

Everything in Essentials, plus proactive optimization. Pull from:
- Critical findings from the 2 lowest-scoring dimensions
- Full marketing optimization recommendations
- Active reputation management (not just monitoring)
- GEO/SEO implementation
- Monthly strategy calls

Contents to include:
- All Essentials services
- Additional services that drive growth
- Content creation specifications (e.g., "2 blog posts/month optimized for AI citability")
- Monthly reporting and strategy call

**Pricing logic:**
- Local service business: $1,500-$2,500/month
- SaaS/E-commerce: $2,000-$3,000/month
- Multi-location business: $2,500-$3,500/month

#### Tier 3 — Full Agency ($3,500-$7,500/month)

The complete agency experience. Pull from ALL findings across ALL dimensions.

Contents to include:
- All Growth services
- Comprehensive marketing overhaul
- Content creation at scale (4+ pieces/month)
- Ongoing legal compliance monitoring
- Sales collateral and outreach support
- Quarterly strategy reviews with leadership
- Dedicated Slack/communication channel
- Priority response times

**Pricing logic:**
- Small local business: $3,500-$4,500/month
- Medium business (10-50 employees): $4,500-$6,000/month
- Larger business (50+ employees): $6,000-$7,500/month

### Step 6 — Build 90-Day Implementation Timeline

Structure the timeline in three phases, pulling specific action items from audit findings:

**Phase 1: Foundation (Days 1-30)**
Focus: Critical fixes, compliance, quick wins
- Week 1: Onboarding kickoff, access setup, baseline metrics
- Week 2-3: Critical compliance fixes (legal gaps, privacy policy)
- Week 3-4: Quick wins implementation (the ones with highest impact-to-effort ratio)
- Deliverable: Month 1 progress report

**Phase 2: Optimization (Days 31-60)**
Focus: Marketing, reputation, SEO/GEO improvements
- Week 5-6: Marketing optimization (CTAs, copy, conversion elements)
- Week 7-8: Reputation management launch (review responses, request campaigns)
- Week 7-8: GEO/SEO implementation (schema, content structure, AI crawler access)
- Deliverable: Month 2 progress report + first strategy call

**Phase 3: Growth (Days 61-90)**
Focus: Scaling, content, competitive positioning
- Week 9-10: Content strategy launch
- Week 11-12: Performance benchmarking and competitive analysis
- Week 12: Quarterly review with full performance data
- Deliverable: Quarter 1 comprehensive report with ROI tracking

### Step 7 — Create Follow-Up Email Sequence

Generate 3 emails for after the proposal is sent:

**Email 1: Proposal Follow-Up (Send 2 days after proposal)**
- Subject line that references a specific finding (e.g., "Re: The [specific issue] we found on your website")
- Brief reminder of the most impactful finding
- Restate the ROI potential
- Soft CTA to schedule a call
- Keep under 150 words

**Email 2: Value Add (Send 5 days after proposal)**
- Subject line offering additional value (e.g., "Quick tip for [Company Name]'s [specific area]")
- Share one actionable tip they can implement immediately (a quick win from the audit)
- Position it as a taste of what the full engagement delivers
- CTA to discuss the proposal
- Keep under 150 words

**Email 3: Final Touch (Send 10 days after proposal)**
- Subject line creating gentle urgency (e.g., "Last thoughts on [Company Name]'s digital strategy")
- Reference competitive pressure or market timing
- Offer a modified engagement option (lower tier or pilot project)
- Clear final CTA
- Keep under 120 words

### Step 8 — Generate the Proposal Document

Write the complete proposal to `AGENCY-PROPOSAL-[ClientName].md`. Replace spaces in the client name with hyphens.

Use this structure:

```markdown
# Agency Proposal: [Company Name]

**Prepared for:** [Company Name]
**Prepared by:** [Leave blank for user to fill]
**Date:** [Current Date]
**Proposal Valid Until:** [Date + 30 days]

---

## The Opportunity

[2-3 paragraphs summarizing what was found in the audits. Lead with the biggest opportunity, quantified if possible. Frame everything in terms of revenue impact, not technical jargon. Make the business owner feel the cost of inaction.]

### What We Analyzed

| Dimension | Status | Score | Key Finding |
|-----------|--------|-------|-------------|
| Marketing | [Audited/Pending] | [XX/100] | [One-line finding] |
| Reputation | [Audited/Pending] | [XX/100] | [One-line finding] |
| GEO/SEO | [Audited/Pending] | [XX/100] | [One-line finding] |
| Legal Compliance | [Audited/Pending] | [XX/100] | [One-line finding] |
| Sales Opportunity | [Audited/Pending] | [XX/100] | [One-line finding] |

**Composite Score:** [XX]/100 — Grade: [X]

---

## What We Found

### Critical Issues Requiring Attention

[List the top 5 critical findings across all audits, each with:]
1. **[Issue Title]**
   - What we found: [Specific evidence]
   - Why it matters: [Revenue/risk impact]
   - How we fix it: [Service that addresses this]

### Quick Wins Available Now

[List the top 5 quick wins, each with:]
1. **[Win Title]**
   - What to do: [Specific action]
   - Expected result: [Projected improvement]
   - Timeline: [How long to implement]

---

## Recommended Service Packages

### Tier 1: Essentials — $[X]-$[Y]/month

*Best for: Getting the critical issues fixed and building a foundation*

**Included Services:**
- [Service 1] — addresses [finding reference]
- [Service 2] — addresses [finding reference]
- [Service 3] — addresses [finding reference]
- Monthly performance report
- Email support

**Expected Results (90 days):**
- [Projected outcome 1]
- [Projected outcome 2]
- [Projected outcome 3]

**Estimated ROI:** $[X]-$[Y]/month in additional revenue or risk avoidance

---

### Tier 2: Growth — $[X]-$[Y]/month *(Recommended)*

*Best for: Actively growing your digital presence and competitive position*

**Everything in Essentials, plus:**
- [Service 4] — drives [growth metric]
- [Service 5] — drives [growth metric]
- [Service 6] — drives [growth metric]
- [Content deliverables with quantities]
- Monthly strategy call (30 minutes)
- Priority support

**Expected Results (90 days):**
- [Projected outcome 1]
- [Projected outcome 2]
- [Projected outcome 3]
- [Projected outcome 4]

**Estimated ROI:** $[X]-$[Y]/month in additional revenue or risk avoidance

---

### Tier 3: Full Agency — $[X]-$[Y]/month

*Best for: Comprehensive digital transformation with dedicated agency partnership*

**Everything in Growth, plus:**
- [Service 7] — delivers [outcome]
- [Service 8] — delivers [outcome]
- [Service 9] — delivers [outcome]
- [Full content calendar with quantities]
- Quarterly strategy review with leadership
- Dedicated communication channel
- Priority response (same-day)

**Expected Results (90 days):**
- [Projected outcome 1]
- [Projected outcome 2]
- [Projected outcome 3]
- [Projected outcome 4]
- [Projected outcome 5]

**Estimated ROI:** $[X]-$[Y]/month in additional revenue or risk avoidance

---

## ROI Projections

| Investment | Monthly Cost | Projected Monthly Return | ROI Multiple |
|------------|-------------|------------------------|-------------|
| Essentials | $[X] | $[Y] | [Z]x |
| Growth | $[X] | $[Y] | [Z]x |
| Full Agency | $[X] | $[Y] | [Z]x |

*Projections based on industry averages and findings specific to [Company Name]. Actual results may vary based on market conditions and implementation.*

### How We Calculated This

[2-3 sentences explaining the ROI methodology in plain English. Reference specific findings that drive the projections. Example: "Based on your current 3.2-star Google rating, moving to 4.0+ stars typically increases local service revenue by 15-25%. For a business of your size, that represents an estimated $X-$Y per month in additional revenue."]

---

## 90-Day Implementation Timeline

### Phase 1: Foundation (Days 1-30)
| Week | Focus | Deliverables |
|------|-------|-------------|
| 1 | Onboarding & Setup | Kickoff call, access setup, baseline metrics |
| 2 | Critical Fixes | [Specific compliance/risk items] |
| 3 | Quick Wins | [Specific quick win implementations] |
| 4 | Foundation Review | Month 1 progress report |

### Phase 2: Optimization (Days 31-60)
| Week | Focus | Deliverables |
|------|-------|-------------|
| 5-6 | [Primary optimization area] | [Specific deliverables] |
| 7-8 | [Secondary optimization area] | [Specific deliverables] |
| 8 | Mid-Point Review | Month 2 report + strategy call |

### Phase 3: Growth (Days 61-90)
| Week | Focus | Deliverables |
|------|-------|-------------|
| 9-10 | [Growth initiative 1] | [Specific deliverables] |
| 11-12 | [Growth initiative 2] | [Specific deliverables] |
| 12 | Quarterly Review | Q1 comprehensive report with ROI |

---

## Why Work With Us

[3 bullet points — leave mostly templated for the user to customize:]
- **Data-Driven Approach:** Every recommendation is backed by comprehensive audits across 5 dimensions, not guesswork
- **[Customizable point about team/experience]**
- **[Customizable point about results/guarantee]**

---

## Next Steps

1. **Choose your tier** — Select the package that fits your goals and budget
2. **Schedule a kickoff call** — We'll walk through the plan and answer questions
3. **We start working** — Implementation begins within 48 hours of agreement

**To get started, reply to this proposal or call [phone placeholder].**

---

## Appendix: Detailed Audit Scores

[If audit data is available, include the full dimension breakdown tables from each audit]

---

*This proposal is valid for 30 days from [Date].*
*Generated by the AI Agency Command Center*
```

### Step 9 — Generate Follow-Up Emails

After the main proposal, append a section to the file:

```markdown
---

## Follow-Up Email Sequence

### Email 1: Proposal Follow-Up (Send Day 2)

**Subject:** Re: The [specific issue] we found on [Company Name]'s website

[Email body — under 150 words, references top finding, restates ROI, soft CTA for call]

---

### Email 2: Value Add (Send Day 5)

**Subject:** Quick tip for [Company Name]'s [specific area]

[Email body — under 150 words, shares one actionable quick win, positions as taste of full engagement]

---

### Email 3: Final Touch (Send Day 10)

**Subject:** Last thoughts on [Company Name]'s digital strategy

[Email body — under 120 words, references competition, offers modified option, clear final CTA]
```

---

## Output

- **File:** `AGENCY-PROPOSAL-[ClientName].md` saved to the current working directory
- **Terminal:** Display a summary confirming which audits were incorporated, the recommended tier, and the estimated total ROI range
- **Follow-up prompt:** "Proposal saved. Run `/agency pipeline` to see your full prospect pipeline."

---

## Important Rules

1. **Client-ready language.** No jargon. No technical terms without explanation. Write as if the reader is a business owner, not a marketer.
2. **Specific over generic.** Every service item should reference a specific finding from the audits. Never say "improve your marketing" — say "rewrite your homepage headline to include your primary service area and key differentiator."
3. **Conservative ROI.** Always use ranges and hedge with "estimated" and "based on industry averages." Never promise exact returns.
4. **Recommend Tier 2.** Mark it as "Recommended" in the proposal. It's the sweet spot for most businesses and has the best chance of closing.
5. **Leave customization hooks.** The "Why Work With Us" section and contact details should have clear placeholders for the user to fill in.
6. **Deduplicate findings.** If the same issue appears in multiple audits (e.g., SEO mentioned in both Marketing and GEO), consolidate into one finding with cross-references.
7. **Price based on business size.** A solo plumber gets the low end of each range. A multi-location company gets the high end.

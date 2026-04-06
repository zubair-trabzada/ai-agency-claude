---
name: agency-quick
description: 60-Second Agency Snapshot — rapid 5-dimension assessment without subagents, outputs a compact scorecard
---

# 60-Second Agency Snapshot

You are the rapid assessment engine for the AI Agency Command Center. When the user runs `/agency quick <url>`, you perform a fast, single-pass evaluation of a business across all 5 agency dimensions — Marketing, Reputation, GEO/SEO, Legal, and Sales — and output a compact scorecard in under 60 seconds.

This is the lightweight alternative to the full onboard. No subagents. No parallel processing. One fetch, one analysis, one scorecard. Use this to quickly qualify a prospect before committing to a full audit.

---

## Invocation

```
/agency quick <url>
```

Examples:
- `/agency quick https://www.acmeplumbing.com`
- `/agency quick smithroofing.com`

If the user provides a domain without protocol, prepend `https://`.

---

## Execution Flow

### Step 1 — Fetch the Homepage

Use `WebFetch` to retrieve the target URL with this prompt:

```
Extract a comprehensive business analysis from this page. I need:

BUSINESS INFO: Company name, industry, location, services offered, phone/email

MARKETING SIGNALS: Quality of headline/hero, clarity of value proposition, presence of CTAs, social proof (testimonials/reviews/logos), lead capture forms, content quality

REPUTATION INDICATORS: Any reviews or ratings displayed on site, testimonials, trust badges, BBB or association memberships, years in business claims

SEO/GEO READINESS: Meta title and description quality, heading structure, schema markup presence, content depth and structure, FAQ sections, whether content has clear quotable statements with data/statistics

LEGAL COMPLIANCE: Privacy policy link present, terms of service link, cookie consent banner, SSL/HTTPS, ADA accessibility indicators (alt tags, ARIA), contact information completeness

SALES OPPORTUNITY: Business size indicators, market position, competitive landscape hints, technology sophistication, growth signals, estimated company maturity
```

### Step 2 — Rapid 5-Dimension Assessment

Using ONLY the data returned from the single WebFetch call, evaluate all 5 dimensions. Do NOT launch subagents. Do NOT make additional web requests. Work with what you have.

Score each dimension 0-100 based on observable evidence from the homepage.

#### Dimension 1: Marketing Quality (Weight: 25%)

Evaluate based on what you can see:
- **Headline/Hero:** Is there a clear, benefit-driven headline? (0-20 points)
- **Value Proposition:** Can you tell what they do and why to choose them within 5 seconds? (0-20 points)
- **CTAs:** Are there clear calls-to-action? (0-20 points)
- **Social Proof:** Testimonials, reviews, logos, case studies present? (0-20 points)
- **Content Quality:** Is the copy professional, specific, and customer-focused? (0-20 points)

Total = sum of the 5 components.

Key Finding: Identify the single biggest marketing gap.
Quick Win: Identify the single easiest marketing improvement.

#### Dimension 2: Reputation Indicators (Weight: 20%)

Evaluate based on visible signals:
- **On-site Reviews:** Are reviews or ratings displayed? (0-25 points)
- **Trust Signals:** Awards, certifications, BBB, association badges? (0-25 points)
- **Testimonials:** Quality and specificity of testimonials? (0-25 points)
- **Credibility Markers:** Years in business, team bios, guarantees? (0-25 points)

Total = sum of the 4 components.

Note: Without searching review platforms, this is a surface-level assessment. Flag this limitation.

Key Finding: Identify the single biggest reputation gap visible from the site.
Quick Win: Identify the single easiest reputation improvement.

#### Dimension 3: SEO/GEO Readiness (Weight: 20%)

Evaluate based on page structure:
- **Meta Tags:** Title tag and meta description present and optimized? (0-20 points)
- **Content Structure:** Proper heading hierarchy (H1, H2, H3)? (0-20 points)
- **AI Citability:** Clear, definitive statements AI could quote? Data, stats, expertise signals? (0-20 points)
- **Schema Indicators:** Any structured data visible? FAQ markup? LocalBusiness? (0-20 points)
- **Content Depth:** Enough substantive content for AI systems to reference? (0-20 points)

Total = sum of the 5 components.

Key Finding: Identify the single biggest SEO/GEO gap.
Quick Win: Identify the single easiest SEO/GEO improvement.

#### Dimension 4: Legal Compliance (Weight: 15%)

Evaluate based on visible compliance elements:
- **Privacy Policy:** Link exists and is accessible? (0-25 points)
- **Terms of Service:** Link exists? (0-25 points)
- **Cookie Consent:** Banner or consent mechanism present? (0-25 points)
- **SSL & Accessibility:** HTTPS active? Basic accessibility indicators? (0-25 points)

Total = sum of the 4 components.

Key Finding: Identify the single biggest compliance gap.
Quick Win: Identify the single easiest compliance fix.

#### Dimension 5: Sales Opportunity Fit (Weight: 20%)

Evaluate the prospect quality for agency services:
- **Market Need:** How much would this business benefit from agency services? (0-25 points)
- **Budget Signals:** Do they appear to have budget? (established, multiple services, professional site vs basic) (0-25 points)
- **Digital Maturity Gap:** How far behind are they? (bigger gap = higher opportunity score) (0-25 points)
- **Accessibility:** Is this likely an owner-operator who makes buying decisions? (0-25 points)

Total = sum of the 4 components.

Key Finding: Identify the single biggest sales insight.
Quick Win: Identify the best engagement hook.

### Step 3 — Calculate Composite Score

```
Agency Snapshot Score = (Marketing x 0.25) + (Reputation x 0.20) + (GEO x 0.20) + (Legal x 0.15) + (Sales x 0.20)
```

Round to the nearest whole number.

Assign a grade:
| Score | Grade |
|-------|-------|
| 85-100 | A+ |
| 70-84 | A |
| 55-69 | B |
| 40-54 | C |
| 25-39 | D |
| 0-24 | F |

### Step 4 — Output the Scorecard

Output DIRECTLY to the terminal. Do NOT save to a file. Keep the entire output under 40 lines.

Use this exact format:

```
============================================================
  AGENCY SNAPSHOT: [Company Name]
  URL: [url]
  Date: [Current Date]
============================================================

  COMPOSITE SCORE: [XX]/100 — Grade: [X]

  DIMENSION BREAKDOWN:
  ┌─────────────────────┬───────┬─────────────────────────────────────┐
  │ Dimension           │ Score │ Key Finding                         │
  ├─────────────────────┼───────┼─────────────────────────────────────┤
  │ Marketing (25%)     │ XX    │ [One-line finding]                  │
  │ Reputation (20%)    │ XX    │ [One-line finding]                  │
  │ GEO/SEO (20%)       │ XX    │ [One-line finding]                  │
  │ Legal (15%)         │ XX    │ [One-line finding]                  │
  │ Sales Opp. (20%)    │ XX    │ [One-line finding]                  │
  └─────────────────────┴───────┴─────────────────────────────────────┘

  QUICK WINS:
  1. [Marketing quick win]
  2. [Reputation quick win]
  3. [GEO/SEO quick win]
  4. [Legal quick win]
  5. [Sales quick win]

  PROSPECT VERDICT: [One sentence — is this worth pursuing?]

  BOTTOM LINE: [One sentence — the single most impactful thing
  this business should do to improve their digital presence]

============================================================
  Run: /agency onboard [url] — for the full multi-team audit
============================================================
```

---

## Scoring Calibration Guide

To keep scores consistent across assessments, use these benchmarks:

**Score 80-100 (A+/A):** Polished, professional site with strong marketing, visible social proof, proper legal compliance, good content structure. Think: a well-funded company with an active marketing team.

**Score 55-79 (B):** Decent site that covers the basics but has notable gaps. Has a CTA but it's weak. Has some reviews but doesn't display them well. Has a privacy policy but it's generic. Most small businesses land here.

**Score 40-54 (C):** Functional but clearly lacking in multiple areas. Template website with minimal customization. No visible social proof. Missing legal pages. Thin content. This is the sweet spot for agency services.

**Score 25-39 (D):** Outdated or poorly built website. Major gaps everywhere. This business is leaving significant money on the table and needs help urgently.

**Score 0-24 (F):** Broken, non-functional, or effectively non-existent web presence. May need to start from scratch.

---

## Industry-Specific Scoring Adjustments

When scoring, apply industry-specific context to each dimension. Different industries have different baseline expectations.

### Local Service Businesses (Plumbing, HVAC, Roofing, Locksmith, etc.)

**Marketing:** These businesses rarely have strong marketing. A clear phone number above the fold and a service list already puts them at 50+. Look for: service area pages, before/after galleries, emergency contact prominence.

**Reputation:** This is their most critical dimension. Weight heavily: Google star rating mentions on site, testimonial quality and specificity, guarantee badges, license/insurance display. A local service company with no visible reviews or testimonials on their website scores below 30.

**GEO/SEO:** Local businesses often lack any GEO optimization. Look for: LocalBusiness schema, service area mentions, structured content that AI could cite for "best [service] in [city]" queries. NAP (Name, Address, Phone) consistency matters here.

**Legal:** Most local service businesses have minimal compliance. A privacy policy alone pushes them to 40+. Look for: licensing disclosures, insurance information, service guarantees with clear terms.

**Sales Opportunity:** Local service businesses in the 3.0-4.0 star range with 20+ reviews are the sweet spot. Owner-operators who answer their own phone = high accessibility. Multiple negative reviews about the same issue = clear pain point to lead with.

### SaaS / Software Companies

**Marketing:** Higher baseline expected. Score against: clear product screenshots or demo, pricing page, feature comparison, free trial CTA, blog/resource center. SaaS without a clear free trial or demo CTA scores below 50.

**Reputation:** Look for: G2/Capterra mentions, case studies, customer logos, NPS or satisfaction claims. SaaS reputation lives on review platforms more than Google reviews.

**GEO/SEO:** Critical for SaaS. Content depth matters enormously. Look for: knowledge base, documentation, blog cadence, pillar pages, FAQ sections. SaaS with thin content scores below 40.

**Legal:** Higher stakes. Privacy policy must mention data processing, Terms must cover SaaS-specific items (SLAs, data ownership, termination). Cookie consent is essential.

**Sales Opportunity:** Evaluate funding stage, team size, current marketing sophistication. Early-stage SaaS with product-market fit but no marketing team = ideal prospect.

### E-Commerce

**Marketing:** Product page quality is everything. Look for: product descriptions, high-quality images, customer reviews on products, upsell/cross-sell, cart abandonment mechanisms, email capture popups.

**Reputation:** Product reviews are the focus. Trust badges (Norton, McAfee, BBB), return policy prominence, shipping information visibility.

**GEO/SEO:** Product schema, review schema, breadcrumbs, category page structure. E-commerce without product schema scores below 30 on this dimension.

**Legal:** Privacy compliance is critical for e-commerce. PCI compliance indicators, clear refund/return policies, shipping terms, cookie consent for tracking pixels.

**Sales Opportunity:** Revenue indicators from product breadth, pricing levels, and marketing sophistication. Smaller e-commerce stores with 50-500 products and no dedicated marketing team are ideal.

### Healthcare / Medical

**Marketing:** Trust and credibility over flashiness. Look for: provider bios with credentials, insurance accepted, patient testimonials (HIPAA-compliant), appointment booking.

**Reputation:** Patient reviews are extremely high-stakes. Google rating is often the first thing potential patients see. Response to negative reviews must be HIPAA-compliant (no patient information).

**GEO/SEO:** Medical content requires strong E-E-A-T signals. Author credentials, medical review dates, structured FAQ content, condition-specific pages.

**Legal:** Highest stakes of any industry. HIPAA indicators, patient privacy notices, telehealth disclosures if applicable, ADA accessibility for healthcare sites.

**Sales Opportunity:** Medical practices with poor online presence but strong clinical reputations are excellent prospects. Multi-provider practices have higher budgets.

### Restaurant / Hospitality

**Marketing:** Menu presentation, online ordering integration, ambiance photos, events/specials promotion. A restaurant with no online menu scores below 30.

**Reputation:** Google and Yelp ratings are everything. Response rate to reviews directly impacts foot traffic. Review volume matters more than perfection.

**GEO/SEO:** Menu schema, Restaurant schema, hours, location. Most restaurants have zero GEO optimization, making this a high-opportunity dimension.

**Legal:** Health department compliance, allergen disclosures, ADA compliance for online ordering, privacy policy for reservation/ordering data.

**Sales Opportunity:** Multi-location restaurant groups are ideal. Single-location restaurants may have limited budgets but high reputation pain.

---

## Comparison Mode

If the user provides multiple URLs separated by "vs" or a comma, run the snapshot on each URL and output a side-by-side comparison:

```
/agency quick acmeplumbing.com vs smithplumbing.com
```

In comparison mode:
1. Fetch both URLs (two WebFetch calls, can run in parallel)
2. Score each business across all 5 dimensions
3. Output a comparison scorecard:

```
============================================================
  AGENCY SNAPSHOT — HEAD-TO-HEAD COMPARISON
  Date: [Current Date]
============================================================

  ┌─────────────────────┬────────────────┬────────────────┐
  │ Dimension           │ [Company A]    │ [Company B]    │
  ├─────────────────────┼────────────────┼────────────────┤
  │ Marketing (25%)     │ XX             │ XX             │
  │ Reputation (20%)    │ XX             │ XX             │
  │ GEO/SEO (20%)       │ XX             │ XX             │
  │ Legal (15%)         │ XX             │ XX             │
  │ Sales Opp. (20%)    │ XX             │ XX             │
  ├─────────────────────┼────────────────┼────────────────┤
  │ COMPOSITE           │ XX — Grade [X] │ XX — Grade [X] │
  └─────────────────────┴────────────────┴────────────────┘

  WINNER: [Company] by [X] points
  BIGGEST GAP: [Dimension where the difference is largest]

============================================================
  Run: /agency onboard <url> — for the full multi-team audit
============================================================
```

Keep comparison output under 30 lines total.

---

## Important Rules

1. **Speed is the priority.** This must complete in under 60 seconds. One WebFetch call. No subagents. No additional searches.
2. **Under 40 lines of output.** Be concise. Every word must earn its place.
3. **Honest scores.** Do not inflate. Most small businesses score 35-65. A score above 75 should be rare.
4. **Surface-level only.** Acknowledge that this is a snapshot, not a deep audit. The reputation score in particular is limited without searching review platforms.
5. **Always end with the CTA** to run the full onboard for deeper analysis.
6. **No file output.** This command prints to terminal only.

---

## Error Handling

- **If WebFetch fails:** Try the URL with/without `www.` prefix. If still failing, inform the user the URL is unreachable and ask them to verify.
- **If the page has very little content:** Score accordingly (low scores are valid data) and note that the limited web presence is itself a major finding.
- **If the URL is a social media page:** Inform the user that quick scan works best with a business website. Attempt the scan with available data but note the limitation.
- **If the URL redirects:** Follow the redirect and note the final URL in the scorecard.

---

## When to Recommend the Full Onboard

Always recommend the full onboard, but adjust the urgency:

- **Score below 40:** "This business has critical gaps. A full onboard will reveal exactly where the money is being left on the table."
- **Score 40-60:** "There are significant opportunities here. A full onboard will quantify the ROI of fixing these issues."
- **Score 60-75:** "Solid foundation with room to grow. A full onboard will identify the highest-impact improvements."
- **Score above 75:** "Strong presence overall. A full onboard will find the edge cases and competitive advantages most businesses miss."

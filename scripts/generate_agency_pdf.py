#!/usr/bin/env python3
"""
AI Agency Command Center — Unified PDF Report Generator
Generates a professional, multi-page agency report combining scores from
all 5 audit teams (Marketing, Reputation, GEO, Legal, Sales).

Requires: reportlab (pip install reportlab)

Usage:
    python3 generate_agency_pdf.py                      # Demo mode with sample data
    python3 generate_agency_pdf.py --demo               # Demo mode (explicit)
    python3 generate_agency_pdf.py agency_data.json      # From JSON file
    python3 generate_agency_pdf.py data.json output.pdf  # Custom output path
"""

import sys
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line, Wedge
    from reportlab.graphics import renderPDF
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ── Color Palette ───────────────────────────────────────────────────────────

COLORS = {
    "navy": HexColor("#1a1a2e"),
    "blue": HexColor("#0066cc"),
    "gold": HexColor("#d4a843"),
    "success": HexColor("#27ae60"),
    "warning": HexColor("#f39c12"),
    "danger": HexColor("#e74c3c"),
    "light_bg": HexColor("#f4f6f9"),
    "text": HexColor("#2c3e50"),
    "text_light": HexColor("#8395a7"),
    "border": HexColor("#dfe6e9"),
    "white": white,
    "black": black,
    "row_alt": HexColor("#f8f9fc"),
}


# ── Utility Functions ───────────────────────────────────────────────────────

def score_color(score):
    """Return color based on score range."""
    if score >= 70:
        return COLORS["success"]
    elif score >= 40:
        return COLORS["warning"]
    else:
        return COLORS["danger"]


def get_grade(score):
    """Return letter grade from numeric score."""
    if score >= 85:
        return "A+"
    elif score >= 70:
        return "A"
    elif score >= 55:
        return "B"
    elif score >= 40:
        return "C"
    elif score >= 25:
        return "D"
    else:
        return "F"


def severity_color(severity):
    """Return color for severity level."""
    mapping = {
        "High": COLORS["danger"],
        "Medium": COLORS["warning"],
        "Low": COLORS["success"],
        "Critical": COLORS["danger"],
    }
    return mapping.get(severity, COLORS["warning"])


# ── Drawing Components ──────────────────────────────────────────────────────

def draw_score_gauge(score, size=120):
    """Create a circular score gauge with colored ring and centered text."""
    d = Drawing(size + 20, size + 30)
    cx = size / 2 + 10
    cy = size / 2 + 15

    # Outer ring
    color = score_color(score)
    d.add(Circle(cx, cy, size / 2,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, size / 2 - 14,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score number
    d.add(String(cx, cy - 4, str(int(score)),
                 fontSize=32, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # "/ 100" label
    d.add(String(cx, cy - 20, "/ 100",
                 fontSize=10, fillColor=COLORS["text_light"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def draw_horizontal_bars(teams, scores, width=460, height=200):
    """Create horizontal bar chart for team scores."""
    d = Drawing(width, height)

    bar_height = 24
    gap = 12
    max_bar_width = width - 200
    start_y = height - 25
    label_x = 5
    bar_x = 140

    for i, (team, score) in enumerate(zip(teams, scores)):
        y = start_y - i * (bar_height + gap)

        # Team label
        d.add(String(label_x, y + 7, team,
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=COLORS["border"],
                   strokeWidth=0.5))

        # Score bar
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None))

        # Score text
        d.add(String(bar_x + max_bar_width + 12, y + 7,
                     f"{int(score)}",
                     fontSize=11, fillColor=color,
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


def draw_mini_gauge(score, size=50):
    """Small gauge for inline use."""
    d = Drawing(size + 10, size + 10)
    cx = size / 2 + 5
    cy = size / 2 + 5
    color = score_color(score)
    d.add(Circle(cx, cy, size / 2, fillColor=color, strokeColor=None))
    d.add(Circle(cx, cy, size / 2 - 8, fillColor=COLORS["white"], strokeColor=None))
    d.add(String(cx, cy - 3, str(int(score)),
                 fontSize=14, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))
    return d


# ── Custom Styles ───────────────────────────────────────────────────────────

def build_styles():
    """Create custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    custom = {
        "title": ParagraphStyle(
            "AgencyTitle", parent=styles["Title"],
            fontSize=32, textColor=COLORS["navy"],
            spaceAfter=8, fontName="Helvetica-Bold"
        ),
        "subtitle": ParagraphStyle(
            "AgencySubtitle", parent=styles["Normal"],
            fontSize=14, textColor=COLORS["text_light"],
            spaceAfter=20, fontName="Helvetica"
        ),
        "heading": ParagraphStyle(
            "AgencyHeading", parent=styles["Heading1"],
            fontSize=20, textColor=COLORS["navy"],
            spaceBefore=20, spaceAfter=12,
            fontName="Helvetica-Bold"
        ),
        "subheading": ParagraphStyle(
            "AgencySubheading", parent=styles["Heading2"],
            fontSize=14, textColor=COLORS["blue"],
            spaceBefore=14, spaceAfter=8,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "AgencyBody", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14
        ),
        "body_bold": ParagraphStyle(
            "AgencyBodyBold", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica-Bold", leading=14
        ),
        "small": ParagraphStyle(
            "AgencySmall", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text_light"],
            spaceAfter=4, fontName="Helvetica", leading=10
        ),
        "grade": ParagraphStyle(
            "AgencyGrade", parent=styles["Title"],
            fontSize=48, textColor=COLORS["gold"],
            spaceAfter=6, fontName="Helvetica-Bold",
            alignment=1
        ),
    }
    return custom


# ── Table Helpers ───────────────────────────────────────────────────────────

def make_header_table_style():
    """Standard table style with navy header."""
    return [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["navy"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["row_alt"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]


# ── Page Builders ───────────────────────────────────────────────────────────

def build_cover_page(data, styles):
    """Page 1 — Cover page with title, company name, date, score gauge, and grade."""
    elements = []
    elements.append(Spacer(1, 1.2 * inch))

    # Title
    elements.append(Paragraph("AI Agency Report", styles["title"]))

    # Company name
    company = data.get("company_name", "Target Company")
    elements.append(Paragraph(company, ParagraphStyle(
        "CompanyName", parent=styles["subtitle"],
        fontSize=18, textColor=COLORS["blue"],
        spaceAfter=6, fontName="Helvetica-Bold"
    )))

    # Date
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    elements.append(Paragraph(f"Report Date: {date_str}", styles["subtitle"]))
    elements.append(Spacer(1, 0.4 * inch))

    # Overall score gauge
    overall = data.get("agency_score", 0)
    gauge = draw_score_gauge(overall, size=130)
    elements.append(gauge)
    elements.append(Spacer(1, 0.2 * inch))

    # Grade
    grade = get_grade(overall)
    elements.append(Paragraph(f"Agency Grade: {grade}", styles["grade"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Executive summary
    summary = data.get("executive_summary",
                       "This report presents a unified analysis across five dimensions: "
                       "Marketing, Reputation, GEO/SEO, Legal Compliance, and Sales Intelligence. "
                       "Each dimension is scored independently and combined into a single Agency Score.")
    elements.append(Paragraph(summary, styles["body"]))

    # URL
    url = data.get("url", "")
    if url:
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Website analyzed: {url}", styles["small"]))

    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(
        "Generated by AI Agency Command Center for Claude Code",
        styles["small"]
    ))

    return elements


def build_score_dashboard(data, styles):
    """Page 2 — Score dashboard with horizontal bar charts and composite score."""
    elements = []
    elements.append(Paragraph("Score Dashboard", styles["heading"]))

    teams = data.get("teams", {})
    team_order = ["Marketing", "Reputation", "GEO/SEO", "Legal", "Sales"]
    team_keys = ["marketing", "reputation", "geo", "legal", "sales"]
    weights = [25, 20, 20, 15, 20]

    team_names = []
    team_scores = []
    for key, name in zip(team_keys, team_order):
        score = teams.get(key, {}).get("score", 0)
        team_names.append(name)
        team_scores.append(score)

    # Bar chart
    chart = draw_horizontal_bars(team_names, team_scores)
    elements.append(chart)
    elements.append(Spacer(1, 0.3 * inch))

    # Composite score calculation display
    overall = data.get("agency_score", 0)
    elements.append(Paragraph(
        f"<b>Composite Agency Score: {int(overall)} / 100</b> "
        f"(Grade: {get_grade(overall)})",
        ParagraphStyle("CompositeScore", parent=styles["body"],
                       fontSize=14, textColor=COLORS["navy"],
                       fontName="Helvetica-Bold", spaceAfter=16)
    ))

    # Score detail table
    table_data = [["Team", "Score", "Weight", "Weighted", "Status"]]
    for key, name, weight in zip(team_keys, team_order, weights):
        score = teams.get(key, {}).get("score", 0)
        weighted = round(score * weight / 100, 1)
        if score >= 70:
            status = "Strong"
        elif score >= 40:
            status = "Needs Work"
        else:
            status = "Critical"
        table_data.append([name, f"{int(score)}", f"{weight}%", f"{weighted}", status])

    # Totals row
    weighted_total = sum(
        teams.get(k, {}).get("score", 0) * w / 100
        for k, w in zip(team_keys, weights)
    )
    table_data.append(["TOTAL", "", "100%", f"{round(weighted_total, 1)}", get_grade(overall)])

    table = Table(table_data, colWidths=[110, 60, 60, 70, 90])
    style_cmds = make_header_table_style()

    # Color-code status column
    for i in range(1, len(table_data)):
        row_data = table_data[i]
        status = row_data[4]
        if status == "Critical":
            style_cmds.append(("TEXTCOLOR", (4, i), (4, i), COLORS["danger"]))
        elif status == "Needs Work":
            style_cmds.append(("TEXTCOLOR", (4, i), (4, i), COLORS["warning"]))
        elif status == "Strong":
            style_cmds.append(("TEXTCOLOR", (4, i), (4, i), COLORS["success"]))
        style_cmds.append(("FONTNAME", (4, i), (4, i), "Helvetica-Bold"))

    # Bold totals row
    last = len(table_data) - 1
    style_cmds.append(("BACKGROUND", (0, last), (-1, last), COLORS["light_bg"]))
    style_cmds.append(("FONTNAME", (0, last), (-1, last), "Helvetica-Bold"))

    table.setStyle(TableStyle(style_cmds))
    elements.append(table)

    return elements


def build_critical_findings(data, styles):
    """Page 3 — Critical findings table across all teams."""
    elements = []
    elements.append(Paragraph("Critical Findings", styles["heading"]))
    elements.append(Paragraph(
        "The most important issues discovered across all five audit dimensions, "
        "ranked by severity and business impact.",
        styles["body"]
    ))
    elements.append(Spacer(1, 0.15 * inch))

    findings = data.get("critical_findings", [])
    if not findings:
        elements.append(Paragraph("No critical findings data available.", styles["body"]))
        return elements

    table_data = [["Team", "Finding", "Severity", "Impact"]]
    for f in findings:
        team = f.get("team", "—")
        finding = Paragraph(f.get("finding", "—"), styles["body"])
        severity = f.get("severity", "Medium")
        impact = Paragraph(f.get("impact", "—"), styles["small"])
        table_data.append([team, finding, severity, impact])

    table = Table(table_data, colWidths=[65, 195, 60, 155])
    style_cmds = make_header_table_style()
    style_cmds.append(("ALIGN", (0, 0), (0, -1), "LEFT"))

    # Color-code severity
    for i, f in enumerate(findings, 1):
        sev = f.get("severity", "Medium")
        color = severity_color(sev)
        style_cmds.append(("TEXTCOLOR", (2, i), (2, i), color))
        style_cmds.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))

    table.setStyle(TableStyle(style_cmds))
    elements.append(table)

    return elements


def build_quick_wins(data, styles):
    """Page 4 — Quick wins table sorted by effort-to-impact ratio."""
    elements = []
    elements.append(Paragraph("Quick Wins", styles["heading"]))
    elements.append(Paragraph(
        "High-impact, low-effort actions that can be implemented immediately. "
        "Sorted by the best effort-to-impact ratio.",
        styles["body"]
    ))
    elements.append(Spacer(1, 0.15 * inch))

    quick_wins = data.get("quick_wins", [])
    if not quick_wins:
        elements.append(Paragraph("No quick wins data available.", styles["body"]))
        return elements

    # Sort: Low effort first, then by High impact
    effort_order = {"Low": 0, "Medium": 1, "High": 2}
    impact_order = {"High": 0, "Medium": 1, "Low": 2}
    quick_wins_sorted = sorted(quick_wins, key=lambda x: (
        effort_order.get(x.get("effort", "Medium"), 1),
        impact_order.get(x.get("expected_impact_level", "Medium"), 1),
    ))

    table_data = [["Team", "Quick Win", "Effort", "Expected Impact"]]
    for qw in quick_wins_sorted:
        team = qw.get("team", "—")
        action = Paragraph(qw.get("action", "—"), styles["body"])
        effort = qw.get("effort", "Medium")
        impact = Paragraph(qw.get("expected_impact", "—"), styles["small"])
        table_data.append([team, action, effort, impact])

    table = Table(table_data, colWidths=[65, 195, 55, 160])
    style_cmds = make_header_table_style()
    style_cmds.append(("ALIGN", (0, 0), (0, -1), "LEFT"))

    # Color-code effort
    for i, qw in enumerate(quick_wins_sorted, 1):
        effort = qw.get("effort", "Medium")
        if effort == "Low":
            style_cmds.append(("TEXTCOLOR", (2, i), (2, i), COLORS["success"]))
        elif effort == "Medium":
            style_cmds.append(("TEXTCOLOR", (2, i), (2, i), COLORS["warning"]))
        else:
            style_cmds.append(("TEXTCOLOR", (2, i), (2, i), COLORS["danger"]))
        style_cmds.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))

    table.setStyle(TableStyle(style_cmds))
    elements.append(table)

    return elements


def build_service_recommendation(data, styles):
    """Page 5 — Three-tier pricing table with ROI projection."""
    elements = []
    elements.append(Paragraph("Service Recommendation", styles["heading"]))
    elements.append(Paragraph(
        "Based on the audit findings, here are three service tiers tailored to "
        "address the identified gaps and maximize return on investment.",
        styles["body"]
    ))
    elements.append(Spacer(1, 0.15 * inch))

    tiers = data.get("service_tiers", {})

    # Essentials tier
    essentials = tiers.get("essentials", {})
    elements.append(Paragraph("Tier 1 — Essentials", styles["subheading"]))
    elements.append(Paragraph(
        f"<b>{essentials.get('price', '$500 - $1,500/month')}</b>",
        ParagraphStyle("TierPrice", parent=styles["body"],
                       fontSize=13, textColor=COLORS["blue"],
                       fontName="Helvetica-Bold", spaceAfter=6)
    ))
    for item in essentials.get("includes", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))
    elements.append(Spacer(1, 0.1 * inch))

    # Growth tier
    growth = tiers.get("growth", {})
    elements.append(Paragraph("Tier 2 — Growth", styles["subheading"]))
    elements.append(Paragraph(
        f"<b>{growth.get('price', '$1,500 - $3,500/month')}</b>",
        ParagraphStyle("TierPrice2", parent=styles["body"],
                       fontSize=13, textColor=COLORS["blue"],
                       fontName="Helvetica-Bold", spaceAfter=6)
    ))
    for item in growth.get("includes", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))
    elements.append(Spacer(1, 0.1 * inch))

    # Full Agency tier
    full = tiers.get("full_agency", {})
    elements.append(Paragraph("Tier 3 — Full Agency", styles["subheading"]))
    elements.append(Paragraph(
        f"<b>{full.get('price', '$3,500 - $7,500/month')}</b>",
        ParagraphStyle("TierPrice3", parent=styles["body"],
                       fontSize=13, textColor=COLORS["blue"],
                       fontName="Helvetica-Bold", spaceAfter=6)
    ))
    for item in full.get("includes", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))
    elements.append(Spacer(1, 0.2 * inch))

    # ROI Projection
    elements.append(Paragraph("ROI Projection", styles["subheading"]))
    roi = data.get("roi_projection", {})
    roi_data = [
        ["Metric", "Current (Est.)", "After 90 Days", "Improvement"],
        [
            "Monthly Leads",
            str(roi.get("current_leads", "15-25")),
            str(roi.get("projected_leads", "40-65")),
            roi.get("leads_improvement", "+160%")
        ],
        [
            "Online Reputation",
            str(roi.get("current_rating", "3.8 stars")),
            str(roi.get("projected_rating", "4.3 stars")),
            roi.get("rating_improvement", "+0.5 stars")
        ],
        [
            "AI Search Visibility",
            str(roi.get("current_visibility", "Low")),
            str(roi.get("projected_visibility", "Moderate")),
            roi.get("visibility_improvement", "2-3x increase")
        ],
        [
            "Compliance Risk",
            str(roi.get("current_risk", "High")),
            str(roi.get("projected_risk", "Low")),
            roi.get("risk_improvement", "Mitigated")
        ],
    ]

    roi_table = Table(roi_data, colWidths=[110, 100, 100, 100])
    roi_style = make_header_table_style()
    roi_style.append(("FONTNAME", (3, 1), (3, -1), "Helvetica-Bold"))
    roi_style.append(("TEXTCOLOR", (3, 1), (3, -1), COLORS["success"]))
    roi_table.setStyle(TableStyle(roi_style))
    elements.append(roi_table)

    return elements


def build_action_plan(data, styles):
    """Page 6 — 90-day action plan in three phases."""
    elements = []
    elements.append(Paragraph("90-Day Action Plan", styles["heading"]))
    elements.append(Paragraph(
        "A phased implementation roadmap to address critical findings, "
        "capture quick wins, and build long-term competitive advantage.",
        styles["body"]
    ))
    elements.append(Spacer(1, 0.15 * inch))

    plan = data.get("action_plan", {})

    # Phase 1
    phase1 = plan.get("phase_1", {})
    elements.append(Paragraph("Phase 1 — Days 1-30: Quick Wins & Critical Fixes", styles["subheading"]))
    elements.append(Paragraph(
        phase1.get("focus", "Address urgent compliance gaps, respond to unanswered reviews, "
                   "fix critical website conversion issues, and configure AI crawler access."),
        styles["body"]
    ))
    for item in phase1.get("actions", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))
    elements.append(Spacer(1, 0.15 * inch))

    # Phase 2
    phase2 = plan.get("phase_2", {})
    elements.append(Paragraph("Phase 2 — Days 31-60: Growth Initiatives", styles["subheading"]))
    elements.append(Paragraph(
        phase2.get("focus", "Launch proactive reputation campaigns, implement GEO-optimized "
                   "content strategy, build marketing funnels, and begin sales outreach optimization."),
        styles["body"]
    ))
    for item in phase2.get("actions", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))
    elements.append(Spacer(1, 0.15 * inch))

    # Phase 3
    phase3 = plan.get("phase_3", {})
    elements.append(Paragraph("Phase 3 — Days 61-90: Optimization & Scaling", styles["subheading"]))
    elements.append(Paragraph(
        phase3.get("focus", "Measure results from Phase 1-2, optimize performing channels, "
                   "scale content production, and establish ongoing monitoring systems."),
        styles["body"]
    ))
    for item in phase3.get("actions", []):
        elements.append(Paragraph(f"  {item}", styles["body"]))

    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph(
        "Generated by AI Agency Command Center for Claude Code",
        styles["small"]
    ))

    return elements


# ── Main Report Generator ──────────────────────────────────────────────────

def generate_report(data, output_path):
    """Build the complete multi-page agency PDF report."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = build_styles()
    elements = []

    # Page 1 — Cover
    elements.extend(build_cover_page(data, styles))
    elements.append(PageBreak())

    # Page 2 — Score Dashboard
    elements.extend(build_score_dashboard(data, styles))
    elements.append(PageBreak())

    # Page 3 — Critical Findings
    elements.extend(build_critical_findings(data, styles))
    elements.append(PageBreak())

    # Page 4 — Quick Wins
    elements.extend(build_quick_wins(data, styles))
    elements.append(PageBreak())

    # Page 5 — Service Recommendation
    elements.extend(build_service_recommendation(data, styles))
    elements.append(PageBreak())

    # Page 6 — 90-Day Action Plan
    elements.extend(build_action_plan(data, styles))

    # Build the PDF
    doc.build(elements)
    return output_path


# ── Demo Data ───────────────────────────────────────────────────────────────

def get_demo_data():
    """Return sample data for demo mode."""
    return {
        "company_name": "Apex Home Services",
        "url": "https://apexhomeservices.com",
        "date": datetime.now().strftime("%B %d, %Y"),
        "agency_score": 47,
        "executive_summary": (
            "Apex Home Services shows significant gaps across multiple dimensions. "
            "Marketing fundamentals are partially in place but conversion optimization is weak. "
            "Reputation management is largely absent with unanswered negative reviews accumulating. "
            "The website is not optimized for AI search engines and has notable legal compliance gaps. "
            "This represents a strong agency opportunity with clear, demonstrable value across all service lines."
        ),
        "teams": {
            "marketing": {"score": 52, "weight": 25},
            "reputation": {"score": 38, "weight": 20},
            "geo": {"score": 29, "weight": 20},
            "legal": {"score": 55, "weight": 15},
            "sales": {"score": 72, "weight": 20},
        },
        "critical_findings": [
            {
                "team": "Marketing",
                "finding": "Homepage headline is generic with no clear value proposition. "
                           "Visitors cannot understand what makes Apex different within 5 seconds.",
                "severity": "High",
                "impact": "Estimated 40-60% of visitors bounce before understanding the service offering."
            },
            {
                "team": "Marketing",
                "finding": "No lead capture mechanism anywhere on the site. No email signup, "
                           "no free estimate form above the fold, no chat widget.",
                "severity": "High",
                "impact": "Website traffic generates zero leads through digital channels."
            },
            {
                "team": "Reputation",
                "finding": "14 negative Google reviews in the last 6 months with zero owner responses. "
                           "Common complaints center on pricing surprises and missed appointments.",
                "severity": "High",
                "impact": "3.2 star rating is below the 4.0 threshold where most consumers filter results."
            },
            {
                "team": "Reputation",
                "finding": "Primary competitor (Elite Home Pros) has 4.6 stars with 240 reviews "
                           "vs. Apex's 3.2 stars with 67 reviews.",
                "severity": "Medium",
                "impact": "Losing an estimated 30-50% of comparison shoppers to the higher-rated competitor."
            },
            {
                "team": "GEO/SEO",
                "finding": "robots.txt blocks GPTBot and PerplexityBot, making the site invisible "
                           "to ChatGPT and Perplexity search results.",
                "severity": "High",
                "impact": "Completely missing from AI-powered search recommendations in their service area."
            },
            {
                "team": "GEO/SEO",
                "finding": "No schema markup of any kind. No LocalBusiness, no Service, "
                           "no AggregateRating, no FAQ structured data.",
                "severity": "Medium",
                "impact": "Missing rich search results and AI citation opportunities."
            },
            {
                "team": "Legal",
                "finding": "Privacy policy was last updated in 2019 and does not mention CCPA. "
                           "Site collects form data from California residents.",
                "severity": "High",
                "impact": "Potential CCPA non-compliance exposure up to $7,500 per intentional violation."
            },
            {
                "team": "Legal",
                "finding": "No cookie consent banner despite running Google Analytics and Facebook Pixel.",
                "severity": "Medium",
                "impact": "GDPR non-compliance for any EU visitors; erodes trust with privacy-conscious users."
            },
            {
                "team": "Sales",
                "finding": "Company is actively hiring 3 field technicians, indicating growth phase "
                           "and budget availability for marketing investment.",
                "severity": "Low",
                "impact": "Strong signal that timing is right for agency outreach."
            },
        ],
        "quick_wins": [
            {
                "team": "Marketing",
                "action": "Rewrite homepage headline to include specific service area and benefit. "
                          "Example: 'Trusted HVAC & Plumbing in [City] — Same-Day Service, Upfront Pricing'",
                "effort": "Low",
                "expected_impact": "Reduce bounce rate by 20-30% with clear value proposition.",
                "expected_impact_level": "High",
            },
            {
                "team": "Marketing",
                "action": "Add a 'Get Free Estimate' form above the fold on the homepage with "
                          "name, phone, and service type fields.",
                "effort": "Low",
                "expected_impact": "Begin capturing leads from existing website traffic immediately.",
                "expected_impact_level": "High",
            },
            {
                "team": "Reputation",
                "action": "Respond to all 14 unanswered negative reviews within 48 hours with "
                          "personalized, empathetic responses offering resolution.",
                "effort": "Low",
                "expected_impact": "Shows future customers the business cares; can recover 30% of unhappy reviewers.",
                "expected_impact_level": "High",
            },
            {
                "team": "Reputation",
                "action": "Launch a post-service review request via text/email to satisfied customers. "
                          "Target 10 new 5-star reviews in the first month.",
                "effort": "Medium",
                "expected_impact": "Move rating from 3.2 toward 3.8 within 60 days.",
                "expected_impact_level": "High",
            },
            {
                "team": "GEO/SEO",
                "action": "Update robots.txt to allow GPTBot, PerplexityBot, Google-Extended, "
                          "and Anthropic crawlers.",
                "effort": "Low",
                "expected_impact": "Immediately become eligible for AI search citations and recommendations.",
                "expected_impact_level": "High",
            },
            {
                "team": "GEO/SEO",
                "action": "Add LocalBusiness schema markup with name, address, phone, hours, "
                          "and service area.",
                "effort": "Low",
                "expected_impact": "Enable rich search results and improve AI entity recognition.",
                "expected_impact_level": "Medium",
            },
            {
                "team": "Legal",
                "action": "Install a cookie consent banner with opt-in mechanism. "
                          "CookieYes or Termly offer free tiers.",
                "effort": "Low",
                "expected_impact": "Achieve basic cookie compliance in under 1 hour.",
                "expected_impact_level": "Medium",
            },
            {
                "team": "Legal",
                "action": "Generate an updated privacy policy using a CCPA-compliant template "
                          "and publish it to the website.",
                "effort": "Medium",
                "expected_impact": "Eliminate primary CCPA exposure risk.",
                "expected_impact_level": "High",
            },
            {
                "team": "Sales",
                "action": "Connect with the owner on LinkedIn referencing their recent hiring "
                          "and offer a free agency audit as a conversation starter.",
                "effort": "Low",
                "expected_impact": "Personalized outreach with growth-timing angle has 3-5x response rate.",
                "expected_impact_level": "Medium",
            },
        ],
        "service_tiers": {
            "essentials": {
                "price": "$500 - $1,500/month",
                "includes": [
                    "Respond to all Google reviews within 24 hours",
                    "Monthly review generation campaign (10-15 new reviews/month)",
                    "Privacy policy and cookie consent compliance fix (one-time)",
                    "robots.txt and schema markup configuration (one-time)",
                    "Monthly performance dashboard",
                ]
            },
            "growth": {
                "price": "$1,500 - $3,500/month",
                "includes": [
                    "Everything in Essentials",
                    "Homepage and landing page copy optimization",
                    "Lead capture form and funnel implementation",
                    "GEO-optimized content creation (4 pages/month)",
                    "Full schema markup implementation across the site",
                    "Active reputation management with sentiment monitoring",
                    "Monthly strategy call with performance review",
                ]
            },
            "full_agency": {
                "price": "$3,500 - $7,500/month",
                "includes": [
                    "Everything in Growth",
                    "Complete website marketing overhaul",
                    "Ongoing legal compliance monitoring and updates",
                    "AI platform monitoring (ChatGPT, Perplexity, Gemini citations)",
                    "Sales outreach sequences and lead nurturing",
                    "Competitor tracking across all dimensions",
                    "Dedicated monthly reports with executive summaries",
                    "Quarterly strategy reviews with roadmap updates",
                ]
            }
        },
        "roi_projection": {
            "current_leads": "15-25",
            "projected_leads": "40-65",
            "leads_improvement": "+160%",
            "current_rating": "3.2 stars",
            "projected_rating": "3.9 stars",
            "rating_improvement": "+0.7 stars",
            "current_visibility": "Low",
            "projected_visibility": "Moderate",
            "visibility_improvement": "3x increase",
            "current_risk": "High",
            "projected_risk": "Low",
            "risk_improvement": "Mitigated",
        },
        "action_plan": {
            "phase_1": {
                "focus": "Address urgent gaps that are actively costing the business customers and "
                         "creating legal exposure. Focus on compliance, reputation recovery, and "
                         "basic conversion fixes.",
                "actions": [
                    "Respond to all 14 unanswered negative Google reviews",
                    "Update robots.txt to allow AI crawlers (GPTBot, PerplexityBot, Google-Extended)",
                    "Install cookie consent banner (CookieYes or Termly)",
                    "Generate and publish updated CCPA-compliant privacy policy",
                    "Rewrite homepage headline with clear value proposition",
                    "Add lead capture form above the fold",
                    "Add LocalBusiness schema markup",
                ]
            },
            "phase_2": {
                "focus": "Build on the foundation from Phase 1 with proactive growth initiatives. "
                         "Launch review generation, create GEO-optimized content, and begin "
                         "marketing funnel development.",
                "actions": [
                    "Launch automated review request campaign targeting recent customers",
                    "Create 4 GEO-optimized service pages with FAQ schema",
                    "Build email capture funnel with service-specific lead magnets",
                    "Implement AggregateRating and Service schema markup",
                    "Create comparison content vs. top 2 competitors",
                    "Set up AI platform citation monitoring dashboard",
                    "Complete ADA accessibility quick fixes (alt text, form labels, heading hierarchy)",
                ]
            },
            "phase_3": {
                "focus": "Measure Phase 1-2 results, double down on what's working, and establish "
                         "ongoing monitoring and optimization systems for long-term growth.",
                "actions": [
                    "Analyze 60-day performance data across all dimensions",
                    "Optimize top-performing content and conversion paths",
                    "Scale review generation to maintain 10+ new reviews per month",
                    "Launch retargeting campaigns for website visitors",
                    "Create monthly client report template with all 5 dimensions",
                    "Establish quarterly business review cadence",
                    "Build content calendar for next 90 days based on performance data",
                ]
            }
        }
    }


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    """Entry point — handles demo mode, JSON file input, and custom output paths."""
    output_path = "AGENCY-REPORT.pdf"

    # Demo mode (no args or --demo flag)
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        data = get_demo_data()
        generate_report(data, output_path)
        print(f"Demo agency report generated: {output_path}")
        return

    # JSON input mode
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    try:
        with open(input_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Could not read {input_file}: {e}")
        sys.exit(1)

    generate_report(data, output_path)
    print(f"Agency report generated: {output_path}")


if __name__ == "__main__":
    main()

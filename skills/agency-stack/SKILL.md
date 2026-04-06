---
name: agency-stack
description: Tool suite status checker — shows which of the 5 AI tool suites are installed and ready
---

# Tool Suite Status Checker

You are the Stack Checker for the AI Agency Command Center. When the user runs `/agency stack`, you check which of the 5 AI tool suites are installed, display their status, show install commands for missing suites, and provide a summary of total capabilities.

## Trigger

This skill activates when the user runs:
```
/agency stack
```

No arguments required.

## Step 1 — Check Each Tool Suite

Check the following 5 paths to determine which suites are installed. Use `Bash` to test file existence:

```bash
test -f ~/.claude/skills/market/SKILL.md && echo "INSTALLED" || echo "MISSING"
test -f ~/.claude/skills/sales/SKILL.md && echo "INSTALLED" || echo "MISSING"
test -f ~/.claude/skills/legal/SKILL.md && echo "INSTALLED" || echo "MISSING"
test -f ~/.claude/skills/reputation/SKILL.md && echo "INSTALLED" || echo "MISSING"
test -f ~/.claude/skills/geo/SKILL.md && echo "INSTALLED" || echo "MISSING"
```

### Suite Details Reference

| Suite | Path | Skills | Agents | Primary Commands |
|-------|------|--------|--------|-----------------|
| AI Marketing Suite | `~/.claude/skills/market/SKILL.md` | 15 | 5 | `/market`, `/market audit`, `/market seo`, `/market funnel`, `/market copy` |
| AI Sales Team | `~/.claude/skills/sales/SKILL.md` | 14 | 4 | `/sales`, `/sales prospect`, `/sales research`, `/sales outreach` |
| AI Legal Assistant | `~/.claude/skills/legal/SKILL.md` | 14 | 3 | `/legal`, `/legal review`, `/legal compliance`, `/legal privacy` |
| AI Reputation Manager | `~/.claude/skills/reputation/SKILL.md` | 14 | 5 | `/reputation`, `/reputation audit`, `/reputation reviews`, `/reputation respond` |
| GEO/SEO Audit Tool | `~/.claude/skills/geo/SKILL.md` | 11 | 5 | `/geo`, `/geo audit`, `/geo citability`, `/geo schema` |

## Step 2 — Count Sub-Skills for Installed Suites

For each installed suite, count the actual number of SKILL.md files in its directory tree:

```bash
find ~/.claude/skills/market -name "SKILL.md" 2>/dev/null | wc -l
find ~/.claude/skills/sales -name "SKILL.md" 2>/dev/null | wc -l
find ~/.claude/skills/legal -name "SKILL.md" 2>/dev/null | wc -l
find ~/.claude/skills/reputation -name "SKILL.md" 2>/dev/null | wc -l
find ~/.claude/skills/geo -name "SKILL.md" 2>/dev/null | wc -l
```

This gives the actual installed skill count rather than the expected count.

## Step 3 — Check for Version Info

For each installed suite, check if there is version information available:

1. Look for a `VERSION` file in the suite root directory
2. Check the first few lines of the main SKILL.md for version mentions
3. Check for a `package.json` or `metadata.json` in the suite directory

If version info is not available, display "latest" as the version.

## Step 4 — Check the Agency Suite Itself

Also verify the Agency Command Center's own installation:

```bash
test -f ~/.claude/skills/agency/SKILL.md && echo "INSTALLED" || echo "MISSING"
```

Count agency sub-skills:
```bash
find ~/.claude/skills/agency -name "SKILL.md" 2>/dev/null | wc -l
```

## Step 5 — Display the Stack Status

Output the dashboard in this format:

```
================================================================
  AI AGENCY COMMAND CENTER — TOOL SUITE STATUS
================================================================

  COMMAND CENTER
  ----------------------------------------------------------------
  [checkmark] Agency Orchestrator     ~/.claude/skills/agency/
              Sub-skills: [count]     Version: [version]

  TOOL SUITES
  ----------------------------------------------------------------
  [checkmark/x]  AI Marketing Suite      [count] skills   [version]
                 Path: ~/.claude/skills/market/
                 Commands: /market, /market audit, /market seo...

  [checkmark/x]  AI Sales Team           [count] skills   [version]
                 Path: ~/.claude/skills/sales/
                 Commands: /sales, /sales prospect, /sales research...

  [checkmark/x]  AI Legal Assistant      [count] skills   [version]
                 Path: ~/.claude/skills/legal/
                 Commands: /legal, /legal review, /legal compliance...

  [checkmark/x]  AI Reputation Manager   [count] skills   [version]
                 Path: ~/.claude/skills/reputation/
                 Commands: /reputation, /reputation audit, /reputation reviews...

  [checkmark/x]  GEO/SEO Audit Tool      [count] skills   [version]
                 Path: ~/.claude/skills/geo/
                 Commands: /geo, /geo audit, /geo citability...

  ----------------------------------------------------------------
  TOTALS
  ----------------------------------------------------------------
  Suites Installed:  [count]/5
  Total Skills:      [count]/68
  Total Agents:      [count]/22
  Agency Ready:      [Yes/No — Yes if all 5 installed]

================================================================
```

## Step 6 — Show Install Commands for Missing Suites

For each missing suite, display the install command. Use these GitHub-based install commands:

```
  MISSING SUITES — Install Commands
  ----------------------------------------------------------------

  AI Marketing Suite:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh | bash

  AI Sales Team:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/ai-sales-claude/main/install.sh | bash

  AI Legal Assistant:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash

  AI Reputation Manager:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/ai-reputation-claude/main/install.sh | bash

  GEO/SEO Audit Tool:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash

  Install all missing suites at once:
    curl -sL https://raw.githubusercontent.com/zubair-trabzada/ai-agency-claude/main/install-all.sh | bash
```

Only show this section if at least one suite is missing. If all suites are installed, show:

```
  All 5 tool suites are installed and ready.
  Run /agency onboard <url> to launch a full multi-team audit.
```

## Step 7 — Capability Summary

If all suites are installed, show what the full stack can do:

```
  FULL STACK CAPABILITIES
  ----------------------------------------------------------------
  With all 5 suites installed, /agency onboard launches:
    - 5 parallel audit agents
    - Covering 68 individual analysis skills
    - Producing unified scoring across all dimensions
    - Client-ready reports with pricing recommendations

  Individual suite commands remain available:
    /market    — Run marketing-only analysis
    /sales     — Run sales-only analysis
    /legal     — Run legal-only analysis
    /reputation — Run reputation-only analysis
    /geo       — Run GEO/SEO-only analysis

  Agency commands:
    /agency onboard <url>   — Full 5-team audit
    /agency quick <url>     — 60-second snapshot
    /agency propose <name>  — Generate proposal
    /agency client <name>   — Client lookup
    /agency status          — Agency dashboard
    /agency report-pdf      — Generate PDF report
================================================================
```

## Edge Cases

- **Agency orchestrator itself is missing**: This should not happen if the user is running this command, but if detected, warn them to reinstall the agency suite.
- **Partial suite installation**: A suite directory might exist but be incomplete (missing sub-skill files). Count actual SKILL.md files rather than assuming the expected count.
- **Permission errors**: If a path exists but cannot be read, note it as "Installed (permission error)" and suggest fixing permissions.

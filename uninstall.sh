#!/bin/bash
# AI Agency Command Center — Uninstaller
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}Uninstalling AI Agency Command Center...${NC}"
echo ""

SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

# Remove skills (orchestrator + sub-skills)
SKILLS=("agency" "agency-onboard" "agency-quick" "agency-propose" "agency-pipeline" "agency-client" "agency-status" "agency-report-pdf" "agency-stack")
for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        rm -rf "$SKILLS_DIR/$skill"
        echo -e "  ${GREEN}✓${NC} Removed skill: $skill"
    fi
done

# Remove agents
AGENTS=("agency-marketing" "agency-reputation" "agency-geo" "agency-legal" "agency-sales")
for agent in "${AGENTS[@]}"; do
    if [ -f "$AGENTS_DIR/$agent.md" ]; then
        rm "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} Removed agent: $agent"
    fi
done

echo ""
echo -e "${GREEN}AI Agency Command Center uninstalled.${NC}"
echo -e "  Note: The 5 tool suites (market, sales, legal, reputation, geo) were NOT removed."
echo -e "  To remove those, run their individual uninstallers."
echo ""

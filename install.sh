#!/bin/bash
# AI Agency Command Center — Claude Code Skills Installer
# Installs agency skills, agents, and scripts into Claude Code

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GOLD='\033[0;33m'
NC='\033[0m'

echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║     AI Agency Command Center — Claude Code Skills    ║${NC}"
echo -e "${GOLD}║     8 Skills · 5 Agents · 5 Teams · PDF Reports     ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect script directory (local vs curl|bash)
if [ -n "$BASH_SOURCE" ] && [ "$BASH_SOURCE" != "bash" ] && [ -f "$BASH_SOURCE" ]; then
    SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
else
    # Running via curl | bash — need to clone
    echo -e "${YELLOW}Running remote install — cloning repository...${NC}"
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/zubair-trabzada/ai-agency-claude.git "$TEMP_DIR/ai-agency-claude" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to clone repository.${NC}"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
    SCRIPT_DIR="$TEMP_DIR/ai-agency-claude"
fi

# Target directories
SKILLS_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.claude/agents"

echo -e "${BLUE}Source:${NC}  $SCRIPT_DIR"
echo -e "${BLUE}Target:${NC} $SKILLS_DIR"
echo ""

# Check if Claude Code is available
if command -v claude &>/dev/null; then
    echo -e "${GREEN}✓ Claude Code detected${NC}"
else
    echo -e "${YELLOW}⚠ Claude Code not found in PATH${NC}"
    if [ -t 0 ]; then
        read -p "  Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then rm -rf "$TEMP_DIR"; fi
            exit 0
        fi
    else
        echo "  Continuing (non-interactive mode)..."
    fi
fi

# Create directories
echo -e "\n${BLUE}Creating directories...${NC}"
mkdir -p "$SKILLS_DIR"
mkdir -p "$AGENTS_DIR"

# ─── Install main orchestrator ───────────────────────────────────────

echo -e "${BLUE}Installing main orchestrator...${NC}"
mkdir -p "$SKILLS_DIR/agency"
cp "$SCRIPT_DIR/agency/SKILL.md" "$SKILLS_DIR/agency/SKILL.md"
echo -e "  ${GREEN}✓${NC} agency/SKILL.md (orchestrator)"

# ─── Install scripts ─────────────────────────────────────────────────

echo -e "\n${BLUE}Installing scripts...${NC}"
SCRIPTS_TARGET="$SKILLS_DIR/agency/scripts"
mkdir -p "$SCRIPTS_TARGET"

SCRIPT_COUNT=0
if [ -d "$SCRIPT_DIR/scripts" ]; then
    for script_file in "$SCRIPT_DIR/scripts"/*; do
        if [ -f "$script_file" ]; then
            cp "$script_file" "$SCRIPTS_TARGET/$(basename "$script_file")"
            chmod +x "$SCRIPTS_TARGET/$(basename "$script_file")"
            echo -e "  ${GREEN}✓${NC} $(basename "$script_file")"
            SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
        fi
    done
fi

if [ $SCRIPT_COUNT -eq 0 ]; then
    echo -e "  ${YELLOW}⚠${NC} No scripts found (skipping)"
fi

# ─── Install sub-skills ──────────────────────────────────────────────

echo -e "\n${BLUE}Installing sub-skills...${NC}"
SKILLS=(
    "agency-onboard"
    "agency-quick"
    "agency-propose"
    "agency-pipeline"
    "agency-client"
    "agency-status"
    "agency-report-pdf"
    "agency-stack"
)

SKILL_COUNT=0
for skill in "${SKILLS[@]}"; do
    if [ -f "$SCRIPT_DIR/skills/$skill/SKILL.md" ]; then
        mkdir -p "$SKILLS_DIR/$skill"
        cp "$SCRIPT_DIR/skills/$skill/SKILL.md" "$SKILLS_DIR/$skill/SKILL.md"
        echo -e "  ${GREEN}✓${NC} $skill"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $skill (not found, skipping)"
    fi
done

# ─── Install agents ──────────────────────────────────────────────────

echo -e "\n${BLUE}Installing agents...${NC}"
AGENTS=(
    "agency-marketing"
    "agency-reputation"
    "agency-geo"
    "agency-legal"
    "agency-sales"
)

AGENT_COUNT=0
for agent in "${AGENTS[@]}"; do
    if [ -f "$SCRIPT_DIR/agents/$agent.md" ]; then
        cp "$SCRIPT_DIR/agents/$agent.md" "$AGENTS_DIR/$agent.md"
        echo -e "  ${GREEN}✓${NC} $agent"
        AGENT_COUNT=$((AGENT_COUNT + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $agent (not found, skipping)"
    fi
done

# ─── Check Python dependencies ───────────────────────────────────────

echo -e "\n${BLUE}Checking Python dependencies...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
    PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)" 2>/dev/null)
    PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)" 2>/dev/null)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        echo -e "  ${GREEN}✓${NC} Python $PYTHON_VERSION detected (3.8+ required)"
    else
        echo -e "  ${YELLOW}⚠${NC} Python $PYTHON_VERSION detected — 3.8+ recommended"
    fi

    # Check for reportlab (needed for PDF reports)
    if python3 -c "import reportlab" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} reportlab installed (PDF reports ready)"
    else
        echo -e "  ${YELLOW}⚠${NC} reportlab not installed (needed for PDF reports)"
        echo -e "    Install with: ${CYAN}pip install reportlab${NC}"
    fi
else
    echo -e "  ${RED}✗${NC} Python 3 not found — PDF reports won't work"
    echo -e "    Install Python: ${CYAN}https://python.org${NC}"
fi

# ─── Cleanup temp directory if used ──────────────────────────────────

if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

# ─── Summary ─────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║             Installation Complete!                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Orchestrator:     ${GREEN}✓${NC} agency"
echo -e "  Skills installed: ${GREEN}$SKILL_COUNT${NC}"
echo -e "  Agents installed: ${GREEN}$AGENT_COUNT${NC}"
echo -e "  Scripts installed:${GREEN} $SCRIPT_COUNT${NC}"

# ─── Tool Suite Status ───────────────────────────────────────────────

echo ""
echo -e "${BLUE}═══ Tool Suite Status ═══${NC}"
echo ""

SUITES_INSTALLED=0
SUITES_MISSING=0

# Check each tool suite
check_suite() {
    local dir_name="$1"
    local display_name="$2"
    local install_cmd="$3"

    if [ -f "$SKILLS_DIR/$dir_name/SKILL.md" ]; then
        echo -e "  ${GREEN}✓${NC} $display_name"
        SUITES_INSTALLED=$((SUITES_INSTALLED + 1))
    else
        echo -e "  ${RED}✗${NC} $display_name ${YELLOW}(not installed)${NC}"
        echo -e "    ${CYAN}$install_cmd${NC}"
        SUITES_MISSING=$((SUITES_MISSING + 1))
    fi
}

check_suite "market" "AI Marketing Suite" \
    "curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-marketing-claude/main/install.sh | bash"

check_suite "sales" "AI Sales Team" \
    "curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-sales-team-claude/main/install.sh | bash"

check_suite "legal" "AI Legal Assistant" \
    "curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash"

check_suite "reputation" "AI Reputation Manager" \
    "Available in AI Workshop community → https://skool.com/aiworkshop"

check_suite "geo" "GEO/SEO Audit Tool" \
    "curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/main/install.sh | bash"

echo ""
echo -e "  Suites ready: ${GREEN}$SUITES_INSTALLED${NC}/5"

if [ $SUITES_MISSING -gt 0 ]; then
    echo -e "  ${YELLOW}Install missing suites above for full agency capabilities.${NC}"
fi

# ─── Commands ─────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}Available Commands:${NC}"
echo "  /agency onboard <url>     Full 5-team parallel audit"
echo "  /agency quick <url>       60-second agency snapshot"
echo "  /agency propose <business> Unified service proposal"
echo "  /agency pipeline          Prospect pipeline view"
echo "  /agency client <name>     Client lookup"
echo "  /agency status            Agency dashboard"
echo "  /agency report-pdf        Unified PDF report"
echo "  /agency stack             Check installed tool suites"
echo ""
echo -e "  ${YELLOW}Start a new Claude Code session to use the skills.${NC}"
echo ""

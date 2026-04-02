# AGENTS.md

This file provides guidance to AI Agents when working with code in this repository.

## Project Overview

This chapter demonstrates agent-based workflows for comprehensive project analysis through specialized agent specifications. Unlike code-based implementations, this chapter uses markdown specifications that define agent roles, responsibilities, and coordination patterns for analyzing software projects.

The project implements a **coordinator-led multi-agent architecture** where Claude Code acts as the master coordinator, orchestrating specialist agents that produce structured reports about project architecture, components, and dependencies.

## Environment Setup

**No Virtual Environment Required**:
- This chapter does not have Python code or `requirements.txt`
- Uses Claude Code's native agent system through markdown specifications
- All agents are defined as `.md` files under `agents/` and `commands/`

**Usage Requirements**:
- Claude Code CLI (claude.ai/code)
- Access to agent specifications via `.claude/agents/` directory
- Optional: MCP servers for dependency validation (Context7, Firecrawl)

## Project Structure

### Directory Layout

```
4-prompts-e-workflow-de-agentes/
├── agents/
│   ├── orchestrator.md              # Coordination and manifest management
│   ├── architectural-analyzer.md     # High-level architecture analysis
│   ├── component-deep-analyzer.md    # Individual component deep-dive
│   └── dependency-auditor.md         # Dependency analysis and validation
└── commands/
    └── run-project-state-full-report.md  # Full workflow orchestration
```

### Agent Specifications

#### 1. orchestrator.md
**Role**: Task Orchestrator and Registry Manager

**Responsibilities**:
- Initializes project structure and creates `MANIFEST.md` as single source of truth
- Registers all specialist outputs with title, absolute path, agent name, and timestamp
- Enforces folder policy and path normalization
- Guarantees component coverage by comparing expected vs actual reports
- Validates and finalizes `MANIFEST.md` ensuring integrity

**Key Constraints**:
- **Never invokes other agents** - only master coordinator (Claude Code) does
- Maintains strict separation of concerns
- Only writes to designated `docs/agents/orchestrator/` directory
- Uses absolute paths rooted at `/` for all references

**Output Location**: `docs/agents/orchestrator/MANIFEST.md`

#### 2. architectural-analyzer.md
**Role**: High-Level Architecture Specialist

**Responsibilities**:
- Analyzes project structure and identifies critical components
- Documents architectural patterns and design decisions
- Produces comprehensive architecture report
- Lists all components for downstream analysis

**Output Pattern**: `docs/agents/architectural-analyzer/<file-name>.md`

**Key Sections**:
- Project overview
- Technology stack
- Critical components list (used by Phase 3)
- Architectural patterns
- Integration points

#### 3. component-deep-analyzer.md
**Role**: Component-Specific Analysis Specialist

**Responsibilities**:
- Performs deep analysis of individual components
- One agent instance per component (parallel execution)
- Examines implementation details, patterns, and concerns
- Produces individual component reports

**Output Pattern**: `docs/agents/component-deep-analyzer/<component-name>-report-YYYY-MM-DD-HH:MM:SS.md`

**Coverage Requirement**: MUST analyze ALL components listed in Architecture Report
- If Architecture Report lists 10 components → 10 parallel tasks
- No component may be skipped
- Coordinator verifies 100% coverage

#### 4. dependency-auditor.md
**Role**: Dependency Analysis and Security Specialist

**Responsibilities**:
- Catalogs all project dependencies
- Validates versions and maintenance status
- Identifies known vulnerabilities (using MCP servers if available)
- Provides evidence-based security assessment

**Output Pattern**: `docs/agents/dependency-auditor/<file-name>.md`

**Validation Tools**:
- Context7 MCP server for dependency lookups
- Firecrawl MCP server for version checking
- **Never fabricates CVEs** - only reports verified issues

### Command Workflow

#### run-project-state-full-report.md
**Purpose**: Complete project analysis workflow with multi-agent coordination

**Execution Flow**:

**Phase 1: Task(orchestrator)**
- Read user flags (`--project-folder`, `--output-folder`, `--ignore-folders`)
- Normalize paths and create required directories
- Initialize empty `MANIFEST.md` structure

**Phase 2: Parallel specialist agents**
- `Task(dependency-auditor)` - Produces dependency report
- `Task(architectural-analyzer)` - Produces architecture report
- Both run in parallel for efficiency
- Orchestrator updates `MANIFEST.md` after each completion

**Phase 3: Component analysis (parallel)**
- Parse Architecture Report to extract component list
- Launch `Task(component-deep-analyzer)` for EACH component in parallel
- Coverage verification: MUST have report for every component
- Orchestrator registers each component report in `MANIFEST.md`

**Phase 4: Task(orchestrator)**
- Aggregates all report references
- Finalizes `MANIFEST.md` with validation
- De-duplicates entries and confirms integrity

**Phase 5: README generation**
- Read `MANIFEST.md` as source of truth
- Build index with report titles and absolute links
- Validate all links before saving
- Save `README-YYYY-MM-DD-HH:MM:SS.md` in orchestrator directory

## Usage Examples

```bash
# Run workflow on current directory
/run-project-state-full-report

# Specify project folder
/run-project-state-full-report --project-folder=my-project

# Custom output location
/run-project-state-full-report --project-folder=my-project --output-folder=analysis-output

# Ignore specific folders (no scanning)
/run-project-state-full-report --ignore-folders=venv,node_modules,.git,dist
```

**Output Structure** (with `--output-folder`):
```
<output-folder>/
├── orchestrator/
│   ├── MANIFEST.md
│   └── README-2025-01-13-14:30:00.md
├── architectural-analyzer/
│   └── architecture-report.md
├── component-deep-analyzer/
│   ├── component-a-report-2025-01-13-14:32:00.md
│   ├── component-b-report-2025-01-13-14:32:01.md
│   └── ...
└── dependency-auditor/
    └── dependencies-report-2025-01-13-14:31:00.md
```

## Architecture & Key Concepts

### Coordinator-Led Multi-Agent Pattern

**Claude Code (YOU) = Master Coordinator**:
- Sequences phases and manages parallelism
- Invokes each agent with separate `Task()` calls
- Orchestrator NEVER spawns sub-agents
- All communication flows through coordinator

**Agent Separation**:
```python
# CORRECT: Coordinator invokes agents
Task(orchestrator)  # Phase 1
Task(architectural-analyzer)  # Phase 2
Task(dependency-auditor)      # Phase 2 (parallel)
Task(orchestrator)  # Update MANIFEST
Task(component-deep-analyzer, component="auth")  # Phase 3
Task(component-deep-analyzer, component="api")   # Phase 3 (parallel)
# ...

# WRONG: Orchestrator spawning agents
# The orchestrator MUST NOT invoke other agents!
```

**MANIFEST.md as Single Source of Truth**:
- Only orchestrator writes to `MANIFEST.md`
- Updated after EACH agent completes
- Contains:
  - Tracked Reports (title, absolute path, agent, timestamp)
  - Workflow notes (task IDs, status)
  - General information (project folder, ignore lists)

### Critical Constraints

1. **Strict Agent Separation**:
   - Each agent invoked with separate `Task()` call
   - Orchestrator NEVER spawns sub-agents
   - Claude Code coordinates sequences and parallelism

2. **Path Policy**:
   - ALL paths are absolute (rooted at `/`)
   - NEVER write outside designated locations
   - NEVER create ad-hoc folders like `reports/` or `output/`
   - Follow exact agent specifications

3. **Component Coverage**:
   - MUST analyze 100% of components from Architecture Report
   - Coordinator verifies coverage before Phase 4
   - Launch additional tasks for missing components

4. **No Code Modifications**:
   - Reports are **descriptive, not prescriptive**
   - NEVER suggest edits, refactors, or migrations
   - NEVER open PRs or modify configuration
   - Only summarize findings

5. **Evidence-Based Security**:
   - NEVER fabricate CVEs
   - Use dependency-auditor evidence only
   - Cite exact package names and versions
   - Avoid vague language ("probably safe", "should be fine")

6. **No Duplication**:
   - Orchestrator validates before registration
   - NEVER duplicate reports with different names/timestamps
   - If changes needed: edit existing report, don't create new one

### MANIFEST.md Template

```markdown
# MANIFEST — <Project Name>
Generated on: YYYY-MM-DD-HH:MM:SS
Orchestrator Path: /docs/agents/orchestrator

## Tracked Reports
- Project Architecture: /docs/agents/architectural-analyzer/architecture-report.md
- Components:
  - Auth Service: /docs/agents/component-deep-analyzer/auth-report-2025-01-13-14:32:00.md
  - API Gateway: /docs/agents/component-deep-analyzer/api-report-2025-01-13-14:32:01.md
- Dependencies: /docs/agents/dependency-auditor/dependencies-report.md

## Workflow
- Task architectural-analyzer: completed at 2025-01-13-14:30:00
- Task dependency-auditor: completed at 2025-01-13-14:30:05
- Task component-deep-analyzer (auth): completed at 2025-01-13-14:32:00
- Task component-deep-analyzer (api): completed at 2025-01-13-14:32:01

## General Information
- Project folder: /Users/user/my-project
- Output folder: /Users/user/my-project/analysis-output
- Ignore folders: venv, node_modules, .git
```

### README Output Template

```markdown
# <Project Name> Project State Full Report

<Short project description>.

This document consolidates key aspects of the project as a comprehensive X-ray, covering architecture, components, and dependencies.

Generated on: YYYY-MM-DD HH:MM:SS

## Overview and Architecture
[Project Architecture](/docs/agents/architectural-analyzer/architecture-report.md)

## Components
- [Auth Service](/docs/agents/component-deep-analyzer/auth-report-2025-01-13-14:32:00.md)
- [API Gateway](/docs/agents/component-deep-analyzer/api-report-2025-01-13-14:32:01.md)

## Dependencies
[Dependencies Report](/docs/agents/dependency-auditor/dependencies-report.md)
```

## Best Practices

### For Agent Specification Authors

1. **Clear Role Definition**:
   - Single responsibility per agent
   - Explicit inputs and outputs
   - Well-defined output location pattern

2. **Coordinator Communication**:
   - Agents communicate ONLY with coordinator
   - Never assume other agents exist
   - Provide structured, predictable outputs

3. **Path Discipline**:
   - Use absolute paths rooted at `/`
   - Follow agent specification exactly
   - Never create unauthorized directories

### For Workflow Designers

1. **Maximize Parallelism**:
   - Phase 2: Run dependency + architecture in parallel
   - Phase 3: Run all component analyzers in parallel
   - Only synchronize when data dependencies exist

2. **Coverage Verification**:
   - Parse Architecture Report for component list
   - Count launched tasks vs listed components
   - Re-launch for any missing reports

3. **MANIFEST Discipline**:
   - Update after EACH agent completes
   - Validate paths exist before registration
   - Check for duplicates by subject and path

## Important Notes

- **No Python Code**: This chapter is specification-driven, not code-driven
- **Claude Code Required**: Agents work through Claude Code's native system
- **No Dependencies**: No `pip install` or virtual environment needed
- **Output Validation**: Always verify absolute paths exist before finalizing
- **Parallel Execution**: Leverage `Task()` parallelism for performance
- **Report Integrity**: Never duplicate reports - edit existing if changes needed

## Negative Instructions

**NEVER**:
- Modify codebase (no PRs, refactors, config changes)
- Run upgrades or migrations (no `npm update`, `go get -u`)
- Invent CVEs without evidence from dependency-auditor
- Use vague language ("probably safe", "seems OK")
- Include emojis or stylized characters
- Provide time estimates
- Create agent folders in repository root
- Create unauthorized files/folders (`reports/`, `output/`, `tmp/`)
- Duplicate reports (edit existing instead)

**ALWAYS**:
- Follow agent specifications exactly
- Use absolute paths rooted at `/`
- Validate 100% component coverage
- Update `MANIFEST.md` after each agent
- Verify paths before finalizing
- Provide evidence-based findings only

## Version Compatibility

- **Claude Code**: Latest version with agent system support
- **Agent Specs**: Markdown format following YAML frontmatter conventions
- **MCP Servers** (optional): Context7, Firecrawl for enhanced validation

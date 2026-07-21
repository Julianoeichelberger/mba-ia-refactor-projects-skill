# Skill: refactor-arch

Automated architectural refactoring skill that analyzes, audits, and refactors any backend project to the MVC (Model-View-Controller) pattern.

This skill is technology-agnostic and works with any backend framework (Python/Flask, Node.js/Express, etc.).

## Invocation

```
/refactor-arch
```

## Execution Flow

Execute the 3 phases sequentially. Each phase must complete before the next begins.

---

## Phase 1: Project Analysis

Scan the entire project to understand its current state. Read ALL source files.

### Steps

1. **Detect the technology stack:**
   - Programming language (Python, JavaScript, TypeScript, etc.)
   - Framework (Flask, Express, Django, FastAPI, etc.)
   - Database (SQLite, PostgreSQL, MySQL, MongoDB, etc.)
   - Dependencies (read requirements.txt, package.json, or equivalent)

2. **Map the current architecture:**
   - List all source files and their line counts
   - Identify the domain (e-commerce, task manager, LMS, etc.)
   - Identify database tables/collections and their schemas
   - Map all routes/endpoints with their HTTP methods
   - Classify the current architectural pattern (monolithic, partial MVC, layered, etc.)

3. **Print the analysis summary** in this exact format:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <detected language>
Framework:     <detected framework and version>
Dependencies:  <key dependencies>
Domain:        <application domain description>
Architecture:  <current architecture description>
Source files:  <N> files analyzed
DB tables:     <comma-separated table names>
================================
```

Refer to `project-analysis.md` for detection heuristics.

---

## Phase 2: Architecture Audit

Cross-reference the codebase against the anti-patterns catalog to generate a comprehensive audit report.

### Steps

1. **Scan for anti-patterns:** Check every source file against the catalog in `anti-patterns-catalog.md`. For each finding:
   - Identify the exact file and line number(s)
   - Classify the severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Describe the problem clearly
   - Explain the impact
   - Provide a specific recommendation

2. **Check for deprecated APIs:** Identify any deprecated functions, methods, or libraries being used. Refer to `anti-patterns-catalog.md` section on deprecated APIs.

3. **Generate the audit report** following the template in `audit-report-template.md`. The report must:
   - Be ordered by severity (CRITICAL first, then HIGH, MEDIUM, LOW)
   - Include at least 5 findings
   - Include at least 1 CRITICAL or HIGH finding
   - Include exact file paths and line numbers for every finding

4. **Print the complete report** to the console.

5. **MANDATORY: Ask for confirmation before proceeding.** Display:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

**DO NOT proceed to Phase 3 without explicit user confirmation.** Wait for the user to respond with "y" or "yes".

---

## Phase 3: Refactoring

Restructure the project to follow the MVC pattern, fixing all identified anti-patterns.

### Steps

1. **Plan the new structure** following the guidelines in `mvc-architecture-guidelines.md`. The target structure must include:
   - `config/` — Configuration module (environment variables, settings)
   - `models/` — Data models and database abstraction
   - `controllers/` — Business logic and request handling
   - `views/` or `routes/` — Route definitions and HTTP interface
   - `middlewares/` — Error handling, validation, logging
   - `app.py` or `app.js` — Composition root / entry point

2. **Execute the refactoring** applying the transformation patterns from `refactoring-playbook.md`:
   - Extract configuration to environment-based config module (Pattern 1)
   - Separate data access into model classes/modules (Pattern 4)
   - Move business logic to controllers (Pattern 8)
   - Define routes in dedicated view/route files
   - Implement **real authentication** where the audit found fake/missing auth — replace fake tokens with signed JWT, verify on every protected route, and protect mutating/data-exposing endpoints (Pattern 11)
   - Centralize error handling in middleware (Pattern 7)
   - **Fix EVERY CRITICAL and HIGH finding from the Phase 2 report** — this is mandatory, not best-effort
   - Fix as many MEDIUM and LOW issues as practical

3. **MANDATORY: Trace findings to changes.** Phase 3 is not complete until every CRITICAL and HIGH finding from the Phase 2 report maps to a concrete code change. Build a traceability table — one row per CRITICAL/HIGH finding — and **do not mark a finding resolved unless you have verified the offending code is actually gone**, not merely relocated. Common trap: a finding whose code was *moved* during restructuring (e.g., `login()` moved from a route file into a controller) carries its vulnerability with it. Grep the refactored tree for the original signature to confirm. For the fake-JWT finding specifically, `grep -r "fake-jwt-token"` must return **zero matches** and a real verification path (decorator/middleware) must exist. If any CRITICAL/HIGH finding cannot be fully resolved, STOP and report it explicitly — never silently ship a partial fix.

4. **Validate the result:**
   - Verify the application starts without errors
   - Verify all original endpoints still respond correctly
   - Confirm no anti-patterns remain in the refactored code
   - Confirm the traceability table from step 3 shows every CRITICAL/HIGH finding as RESOLVED

5. **Print the completion summary:**

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<tree view of new structure>

## Changes Made
- <summary of key changes>

## CRITICAL / HIGH Findings Resolution
| # | Severity | Finding | Fix (file:line) | Status |
|---|----------|---------|-----------------|--------|
| 1 | CRITICAL | <finding> | <where/how fixed> | RESOLVED |
| ... every CRITICAL and HIGH finding from Phase 2 — no omissions ... |

## Validation
  <check> Application boots without errors
  <check> All endpoints respond correctly
  <check> Every CRITICAL/HIGH finding resolved (table above)
  <check> Anti-patterns resolved
================================
```

---

## Reference Files

- `project-analysis.md` — Heuristics for detecting language, framework, database, and architecture mapping
- `anti-patterns-catalog.md` — Catalog of anti-patterns with detection signals and severity classification
- `audit-report-template.md` — Standardized format for the Phase 2 audit report
- `mvc-architecture-guidelines.md` — Target MVC architecture rules, layer responsibilities
- `refactoring-playbook.md` — Concrete transformation patterns with before/after code examples

## Important Rules

- This skill is **technology-agnostic** — it must work with any backend stack
- **Never modify files without user confirmation** (Phase 2 must pause)
- Always provide **exact file paths and line numbers** in findings
- The refactored code must be **functionally equivalent** — no features removed
- Use **parameterized queries** for all database operations (never string concatenation)
- Use **environment variables** for all configuration (never hardcode secrets)
- Use **proper password hashing** (bcrypt, argon2) — never MD5 or plaintext
- Use **real authentication** — never fake/predictable tokens (`'fake-jwt-token-' + id`). When the audit flags fake or missing auth, Phase 3 must issue signed JWTs (PyJWT / flask-jwt-extended / jsonwebtoken), verify them on protected routes, and protect mutating/data-exposing endpoints (Pattern 11)
- **Every CRITICAL and HIGH finding from Phase 2 must be resolved in Phase 3** — restructuring code without fixing its vulnerabilities is not a valid refactor

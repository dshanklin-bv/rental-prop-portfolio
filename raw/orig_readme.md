# Real Estate Cash-Flow & Scenario Modeling — Master README

> A finance-grade, explainable modeling tool that starts simple, stays correct, and grows only when it changes decisions.

---

## 🎯 Product Vision (End Goals)

Build a **unit-aware, after-tax, real/nominal** cash-flow engine with an approachable Streamlit UI that:

* **Models** residential & commercial properties (single-unit → multi-tenant → portfolio).
* **Explains** results (assumptions register, validations, and reproducible Run JSON artifacts).
* **Compares** against opportunity costs (risk-free/TIPS/IG/Equity) in **real** terms.
* **Evolves** via optional AI assistants for **document ingestion** and **explainability**, without forcing integrations.
* **Scales** from a personal tool to a foundation for a multi-tenant SaaS **without** re-architecture.

**Outcome:** A tool that answers “Should I buy/hold/refi/sell?” with **after-tax, real IRR**, clear sensitivities, and auditability—before any advanced features are turned on.

---

## 🧭 Principles

1. **Correctness over flash**: After-tax and real vs nominal are *first-class*.
2. **Progressive disclosure**: Features appear in phases and behind toggles.
3. **Reproducible by design**: Every run writes a minimal **Run JSON**; differences are diff-able.
4. **Manual first**: No brittle integrations; uploads & pasted text only (S3 simulated locally).
5. **Observability ≠ overhead**: Append-only JSONL logs (SQLite optional later).
6. **Add only when it changes decisions**: Monte Carlo, benchmarks, and AI are opt-in.

---

## 🗺️ Phased Roadmap (with Stopping Criteria)

### Phase 0 — Working Tool (ship if it answers the decision)

* **Multi-unit cash-flow** (unit leases → property roll-up)
* **Loans** (P\&I, IO), **exit by cap rate**, **selling costs**
* **Taxes**: straight-line depreciation (27.5y resi / 39y CRE), simple recapture at exit
* **Metrics**: Cap Rate, NOI, DSCR, CoC, **IRR (nominal, after-tax)**
* **Sensitivity**: rent ±x%, exit cap ±y bps, rate +z bps (tornado chart)
* **Exports**: CSV/XLSX of assumptions & cash flows; 1-page PDF summary
* **Run JSON v1 (minimal)**: `meta, assumptions, timelines_nominal, metrics, validations`

**Stop here when:** Matches 2–3 hand-built Excel cases within **±2 bps IRR**.

---

### Phase 1 — Guardrails & Observability

* **Rule-based validations/linting** with plain-English explanations (no AI)
* **Real vs nominal** view; **macro as bounds** (CPI/r\_f for sanity checks)
* **JSONL runtime logs** for parse/run/warn events (SQLite optional later)

**Stop when:** Validations caught at least one user error; logs used once to debug.

---

### Phase 1a — Data Entry Assist (user-driven, optional)

* **Multimodal ingestion** (manual uploads/paste only): leases, bills, rent rolls
* Confidence scores & citations; **apply after review** (no auto-apply)
* **Acceptance criterion:** reduces time-to-first-run by **≥30%** on two real cases

---

### Phase 2 — Usability & Provenance

* **Run Viewer**: browse, diff, and download past runs; “why did IRR move?”
* **Re-parse from Inbox** (simulated S3 folder) and show field-level diffs pre-apply
* **Run JSON v1.x** additive growth only (schema-versioned)

---

### Phase 3 — Risk & Opportunity Cost (feature-flagged)

* **Monte Carlo** (100–500 paths): p5/p95 IRR, **Prob\[DSCR<1.0]**, CVaR on cash flow
* **Benchmarks** (manual expected returns): TIPS/IG/Equity; **after-tax, real excess return**
* Enable **only** if outputs change decisions; otherwise keep off.

---

## 🧱 Architecture Overview

```
/app
  /pages
    01_Model.py           # Core inputs/outputs (Phase 0)
    02_Sensitivity.py     # Tornado + sliders
    03_Ingestion.py       # Upload/paste + review (Phase 1a, optional)
    04_Runs.py            # Run Viewer & diffs (Phase 2)
    05_Settings.py        # Toggles, units, formats
  /engine                 # Extractable, testable core (no Streamlit imports)
    models.py             # Pydantic dataclasses for scenarios, units, leases
    cashflow.py           # Monthlies, roll-ups, exit, metrics
    taxes.py              # Depreciation, recapture (Phase 0), entity hooks
    macros.py             # Real/nominal transforms, CPI/r_f bounds (Phase 1)
    sensitivity.py        # Deterministic bumps
    serializer.py         # Build minimal Run JSON v1
    runlog.py             # Save/load run artifacts + index
  /agents                 # Optional AI helpers (kept behind toggles)
    extract.py            # OCR/LLM-to-JSON ingestion (manual uploads only)
    explain.py            # Future: narrative memos (off by default)
  /persistence
    storage.py            # Inbox (timestamped files), JSONL logs
    db.py                 # SQLite (optional), WAL on
    pylogger_sqlite.py    # Logging handler (optional)
  /data
    inbox/                # Raw uploaded/pasted artifacts (simulated S3)
    runs/                 # Saved Run JSON artifacts (.json/.json.gz)
    ingestions.jsonl      # Metadata for raw artifacts
    runtime.jsonl         # Append-only runtime logs (default)
```

**Extractable engine** enables:

* Unit tests & golden files
* Reuse under a future API/Next.js UI
* Reproducible calculations independent of Streamlit

---

## 📦 Run JSON (v1 Minimal Contract)

* `meta`: run\_id, engine\_semver, created\_at\_utc, scenario\_id (optional)
* `assumptions`: property, units & leases, loan, expenses, exit, taxes (minimal)
* `timelines_nominal`: monthly arrays (income, expenses, NOI, debt service, ATCF)
* `metrics`: Cap Rate Yr1, DSCR min, CoC, IRR nominal (after-tax), equity multiple
* `validations`: list of rule results (level, code, message, affected paths)

**Rules:**

* Only additive changes across versions (no renames)
* Migrations required for expansions (v1 → v1.1, etc.)

---

## 🧪 Acceptance Criteria (Phase 0)

1. **Numerical parity**: IRR and DSCR align with benchmark spreadsheets within **±2 bps** on set scenarios.
2. **Explainability**: A user can answer “what drove the IRR change?” from **Run Viewer** + validations alone.
3. **Portability**: All core tables export to **CSV/XLSX**; 1-page **PDF** summarizes assumptions & metrics.

---

## 🔍 Validations & Guardrails (Non-AI)

* **Structure**: lease dates ordered; non-overlapping; positive rents
* **Finance**: DSCR ≥ floor; exit cap within bounds; selling cost % range
* **Tax**: depreciation basis ≥ 0; recapture not negative; stop if entity mismatch
* **Macro bounds (optional)**: warn if expense growth ≪ CPI, etc.

---

## 🔌 Ingestion (Optional, Manual Only)

* Accept PDFs/images/CSV/text via upload or paste
* Parse → confidence per field → citation snippets (page/coords)
* **Apply after review**; never auto-apply
* Persist raw artifacts to `data/inbox/` and record entries in `ingestions.jsonl`

---

## 📈 Telemetry (Lightweight)

* Default: **runtime.jsonl** (append-only) logs canonical events:

  * `parse.start/done`, `ingest.saved`, `run.start/done`, `warn.validation`
* Optional: switch to **SQLite** with the same event schema for in-app queries
* Purpose: debugging, UX improvement, future AI heuristics—not surveillance

---

## 🔐 Security & Privacy

* No integrations or external APIs required
* Raw artifacts stored locally; PII never embedded in Run JSON
* Redact tenant names in UI exports; reference by unit labels
* Future encryption at rest (when/if moving beyond local dev)

---

## ❌ Non-Goals (for Now)

* Multi-tenant auth/RBAC
* Auto-fetching market/macro data
* AI-driven edits without human approval
* Full accounting/GL or property management workflows

---

## 🚀 Getting Started (Prototype)

1. Install & run Streamlit app.
2. Enter units, expenses, and loan → **Phase 0** outputs.
3. Save a **Run** → inspect **Run JSON** + exports.
4. (Optional) Enable **Macro Bounds** and **Ingestion** toggles.

---

## 🧩 Contribution & Testing

* Unit tests for: amortization, exit value math, depreciation/recapture, real/nominal transforms
* Golden files for sample scenarios (diff against Run JSON)
* Lint rules live with the engine and write to `validations` in Run JSON

---

## 📚 Glossary

* **Real vs nominal**: Purchasing-power adjusted vs face-value cash flows.
* **After-tax IRR**: Internal rate of return including depreciation shields and exit taxes.
* **DSCR**: Debt service coverage ratio (NOI / debt service).
* **Run JSON**: Self-contained artifact of one model run for reproducibility and diffing.

---

## 🌅 Future (Only if Decisions Demand It)

* Monte Carlo risk paths; tail metrics; certainty-equivalent returns
* Benchmarks and efficient frontier vs alternative assets
* Narrative memos and richer AI critique **behind toggles**
* Postgres/S3 migration if/when multi-user becomes real

---

**North Star:** *Answer the investment decision correctly, transparently, and reproducibly. Everything else is a toggle.*

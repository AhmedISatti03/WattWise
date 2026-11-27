# WattWise — Backend Design Review and Next-Task Handoff

**Reviewer:** Muhammad Ahmed Ijaz Satti (Ahmed)  
**Date:** 28 November 2026  
**Version:** 1.0  
**Related work:** [PR #29](https://github.com/AhmedISatti03/WattWise/pull/29), [#14](https://github.com/AhmedISatti03/WattWise/issues/14), [#11](https://github.com/AhmedISatti03/WattWise/issues/11)  
**Status:** Final review response. Core design decisions approved with qualifications and outstanding details below. This is not blanket approval of every detail in a decision-log row.

Umut, thank you for preparing the backend proposal, contract examples and runnable foundation. They give us a concrete basis for reviewing the design together and coordinating the backend, frontend and AI work.

Ahmed reviewed D01–D14 individually. These approvals establish the agreed direction. Details explicitly left open require recommendations and confirmation before the affected behaviour is implemented. The reviewed proposal was at commit `a56fafbe230e45261683c241ca465cc973c0288e`.

## 1. Repository structure and responsibilities

Follow the proposed organization:

| Location | Purpose |
|---|---|
| `backend/` | Application code, migrations, tests and commands |
| `docs/api/` | Shared API contract, schemas and examples |
| `docs/backend/decision-log.md` | Decisions, approval status and remaining questions |
| `docs/backend/scenario-definitions.md` | Expected scenario behaviour |

The backend owns authoritative calculations, coverage, freshness and eligibility decisions. Frontend formatters may handle presentation, including units and display precision.

Frontend branch merging and changes to the shared frontend data layer remain outside BE01 and should be coordinated through Miray’s relevant tasks.

## 2. Decisions approved by Ahmed

| ID | Approved direction | Qualification / remaining detail |
|---|---|---|
| **D01 — Stack** | Python/FastAPI, Pydantic, SQLAlchemy and Alembic. PostgreSQL is the target database for the integrated demonstration. | SQLite remains available for convenient development and foundation checks. |
| **D02 — Sessions** | Server-side browser sessions using HttpOnly, SameSite=Lax cookies, CSRF protection for mutations and separate collector credentials. | Session lifetime, password policy, recovery scope and exact security configuration remain open. |
| **D03 — Ownership** | One household per account initially. Enforce ownership on every request and restrict collectors to assigned devices. Return 404 for foreign resources. | Detailed response envelopes will be reviewed with the contract. |
| **D04 — Time** | UTC timestamps, household-local calendar boundaries, separate observation/receipt times and start-inclusive/end-exclusive periods. | Contract examples must consistently express these rules. |
| **D05 — Readings** | Cumulative imported energy in kWh, instantaneous power in W, unique event IDs and explicit counter epochs. | Collector fields, reset verification and export handling remain open. |
| **D06 — Batches** | Partial batch acceptance, per-event outcomes, safe identical retries, conflicts for changed duplicates and acknowledgement after commit. | Batch limits and exact HTTP/result semantics remain open. |
| **D07 — Delayed data** | Accept valid delayed readings, recalculate affected intervals and prevent double counting. Preserve uncertainty where detailed allocation is unsupported. | Clock-skew limits, reset checks, bucket allocation and invalidation details remain open. |
| **D08 — Tariffs** | Effective-dated tariffs, precise monetary arithmetic, preserved historical bill records and matching charge bases for budgets/forecasts. | Supported charges, rounding, decimal representation and historical recalculation policy remain open. |
| **D09 — Baseline forecast** | Latest seven complete valid days within the current cycle, reliable elapsed-cycle energy and daily household-midnight recomputation. | Partial-day treatment, maturity labels, expiry and budget-warning freshness remain open. |
| **D10 — Status and clock** | Separate device freshness, collector contact and browser-request failures. Use a consistent simulation clock. | Proposed 30-second device and 180-second collector thresholds are provisional. Reporting intervals and replay completion behaviour remain open. |
| **D11 — Bills** | Provisional extraction, editable review, explicit confirmation, manual fallback and duplicate-safe confirmation. Keep bill consumption separate from monitored consumption. | Supplier samples, required fields, upload restrictions, OCR and retention/correction rules remain open. |
| **D12 — Insights** | Evidence-backed alerts, deduplication, recalculation and resolution after relevant changes. Prioritize actual overspend and suppress unsupported forecast warnings. | Dismissal, reappearance, history and equality/rounding rules remain open. |
| **D13 — Assistant** | Read-only authorized functions, shared backend results, supporting periods/references and isolated provider failures. Keep provider secrets server-side. | Exact functions, chat contract, provider, retention, timeouts and streaming remain open. |
| **D14 — Scope** | Record the local demonstration using persisted synthetic readings and coordinated assistant integration. | Physical-hardware verification and real-household accuracy evaluation remain separate. Simulation does not complete #4. |

These are Ahmed’s design decisions. Miray’s frontend contract review remains necessary. Update D14’s scope amendment to reflect this confirmation while preserving the distinction between the demonstration and later hardware/accuracy verification.

## 3. Coordinating the assistant and AI work

Ahmed will take the lead on assistant design, model integration, prompts and AI evaluation, so you don’t need to carry that extra workload alongside the backend.

Your authorized query and calculation services will provide the foundation. We’ll agree the interface together, with Miray involved in the chat presentation requirements. Your suggestions are welcome throughout.

Please identify the available backend capabilities and any constraints the assistant must respect. Ahmed will develop the exact assistant-function requirements through #24–27 and coordinate them with you.

Umut continues to own the explainable baseline forecast. Ahmed’s later ML candidate under #28 will be evaluated against that baseline.

## 4. Next task: finalize outstanding implementation decisions

**Goal:** Turn the remaining questions into concrete, reviewable specifications that let backend and frontend implementation progress consistently.

Use this response as the handoff for the corresponding follow-up issue. Work through the following increments, prioritizing the details required by the next implementation task.

### A. Resolve the details needed for accounts and settings

Prepare recommendations for:

- Session lifetime, expiry, restoration and logout behaviour.
- Cookie configuration for local development and later HTTPS deployment.
- CSRF token issuance, transport and validation.
- Password requirements and password-recovery scope.
- Household/settings fields, validation and revision-conflict behaviour.
- The minimum tariff/settings representation required by #16.

For each shared behaviour, provide a recommended choice, a short reason and an example request or response. Identify the minimum supported tariff profile explicitly and coordinate supplier/sample requirements with Ahmed. Do not silently adopt the illustrative TRY 3/kWh example as a real tariff.

### B. Finalize the ingestion contract before #17

Specify:

- Exact reading fields and units.
- Counter-epoch creation and reset verification.
- Handling of exported energy and unsupported measurements.
- Batch-size limits, per-event outcomes and HTTP statuses.
- Duplicate and conflict behaviour.
- Future timestamp tolerance, late arrivals and recalculation.
- Coverage and bucket-allocation rules, including unavailable results.

Include examples showing a successful batch, mixed valid/invalid readings, an identical retry, a changed duplicate, a reset and a delayed reading.

### C. Prepare simulation decisions before #18

Specify:

- Reporting intervals and the resulting freshness thresholds.
- Scenario clock, replay speed and completed-replay behaviour.
- Seeded repeatability and reset scope.
- How generated readings enter the actual ingestion pipeline.

Continue distinguishing fixture responses from persisted simulated measurements.

### D. Track decisions needed by later features

Record the remaining tariff, forecast, bill, alert and assistant questions against their implementation tasks.

They do not all need to block accounts, ingestion or simulation. Resolve each before implementing the behaviour it governs. Supplier/sample selection remains coordinated with Ahmed under #3. Assistant requirements remain coordinated through Ahmed’s AI tasks.

## 5. Deliverables and review

Update the existing documents rather than creating competing specifications:

- **Decision log:** record the approvals above accurately, retain partial/provisional status where applicable and add concrete recommendations for open details. Cite this response and the follow-up issue as approval evidence.
- **API contract:** update schemas and examples to match confirmed decisions. Clearly identify proposed production routes and implemented routes.
- **Scenario definitions:** express expected results for retries, gaps, resets, delayed readings and simulation states.
- **Scope amendment:** reflect D14’s approved delivery direction without implying hardware or real-world accuracy completion.
- **Task/PR evidence:** identify which decisions unblock which implementation tasks and summarize changes for review.

Bring unresolved choices affecting shared behaviour back to Ahmed for confirmation. Coordinate screen fields and response states with Miray. Routine implementation choices and independent work can continue within the approved direction.

**This task is complete when:**

- Approved decisions and remaining questions are accurately recorded.
- The details required for the next implementation increment are concrete and reviewed, with Ahmed’s confirmations recorded.
- The shared contract, schemas and examples agree with those decisions, with Miray’s relevant interface review recorded.
- Later questions have an owner and an identified implementation checkpoint.
- The next backend increment has clear inputs and acceptance criteria.

If confirmations are pending, report the precise outstanding items and continue independent work. Do not mark unanswered proposals approved.

## 6. Review boundaries

This response approves the design direction described above. API contract acceptance, independent setup verification and PR merge remain separate review steps.

Issues #16–18 remain implementation work ahead. We will review the contract, mock API and runnable foundation individually before deciding their completion status. This response does not independently verify the test results reported in PR #29 or close any issue.

The follow-up task refines the outstanding decisions and records this review; it complements #14/#11 and does not replace the implementation tasks #16–18.

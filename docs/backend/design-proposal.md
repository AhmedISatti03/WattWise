# Backend design proposal

**Status:** Draft for Ahmed and frontend review · **Version:** 0.1 · **Date:** 27 November 2026  
**Issues:** #14, #11 · **Handoff:** backend v1.0, BE01

## 1. Existing work and intended increment

The repository's `main` contains the seven-feature scope, worked measurement examples, insight scenarios, frontend requirements/wireframes, collector plan and both v1.0 handoffs. The frontend foundation remains on its feature branch with PR #13 open against `dev`. Miray's consumption branch supplies JSON fixtures, `dashboardApi.ts` and framework-independent energy helpers. Neither branch contains a persistent ingestion backend. The fixture helper is not an ingestion pipeline; its data must not be reported as stored measurements.

The initial increment provides a reviewable stack proposal, shared contract/examples, decision log, and task/scenario mapping. Independent code scaffolding can provide startup/configuration, database migration machinery, health checks and explicitly labelled mock endpoints while shared behavior awaits confirmation. Do not promote mock responses to integrated backend completion.

## 2. Proposed technical stack

| Concern | Recommendation | Rationale / alternative |
|---|---|---|
| Runtime/API | Python 3.12+ and FastAPI with Pydantic validation | Fits data processing and Ahmed's Python integrations; typed validation/OpenAPI. A TypeScript server is viable but introduces a different analytical integration boundary. |
| Persistence | PostgreSQL 17 target; SQLAlchemy 2 ORM and Alembic migrations | Transactions, constraints, timezone-aware timestamps and a clear schema history. SQLite is a portable scaffold/test profile, not evidence of PostgreSQL compatibility. A `postgres:17-alpine` local verification profile is available; actual results belong in the verification evidence. |
| Local database startup | Existing local PostgreSQL or a separately configured container | Document both choices; the laptop demonstration must not depend on a hosted database. Do not require Docker merely to inspect the initial scaffold. |
| Browser authentication | Revocable opaque server-side session, hashed token in an HttpOnly, SameSite=Lax cookie; CSRF token on mutations | Supports session restoration without browser localStorage tokens and permits immediate revocation. Use Secure cookies with HTTPS; any loopback-only HTTP development exception must be explicit. Exact origins, cookie lifetime and CSRF validation remain subject to D02 confirmation. |
| Device authentication | Separate revocable collector credential, scoped server-side to registered devices/household | User and collector permissions remain distinct. Payload household IDs never establish ownership. |
| OCR | Text-PDF extraction first; propose a locally configured OCR engine for scanned PDF/photo fallback | Supplier and redacted samples remain unselected under #3. Choose exact dependency and retention policy after sample evaluation; do not claim generic OCR completes supplier-specific extraction. |
| Tests | pytest, HTTPX/TestClient, temporary databases; PostgreSQL integration job when selected | Test real request/transaction boundaries, duplicate handling, ownership and restart persistence. Fixtures alone do not prove ingestion. |
| Interface | Versioned HTTP JSON under `/api/v1`; draft contract version in response metadata | Frontend and assistant use application services rather than separate calculation implementations. |

Exact versions and install commands belong in the runnable backend package; pin the tested set. The scaffold records dependencies in `uv.lock` and `requirements.lock`; Python 3.12.14 is the current local runtime. These are setup facts, not claims that every database/application test has passed. Approval status is recorded in the [decision log](decision-log.md), not inferred from this proposal.

## 3. Logical structure and boundaries

```text
browser / future collector / synthetic replay client
                         ↓
              API validation + authorization
                         ↓
 accounts · households · readings · bills · query services
                         ↓
 transactionally stored records and provenance
                         ↓
 aggregation → costs → baseline forecast → insight evidence
                         ↓
 frontend responses / authorized assistant functions
```

Proposed repository areas: `backend/` for application/migrations/tests/commands; `docs/api/` for the single shared interface and examples; `docs/backend/decision-log.md` for decisions; `docs/backend/scenario-definitions.md` for expected scenario behavior. Frontend display formatters may be reused, but calculations and validity decisions become backend responsibilities. Do not merge the frontend branches or rewrite their shared data layer as part of BE01.

## 4. Proposed persisted entities

| Entity | Essential purpose / constraints |
|---|---|
| User and session | Unique normalized email; password hash; session token hash, expiry and revocation. Never return password/token hashes. |
| Household and settings revision | One owned household per user initially; timezone, half-open billing cycle, budget, effective tariff versions, optimistic revision. |
| Device and collector registration | Stable UUID, household ownership, scope `household` or `appliance`, model/channel mapping, source kind; collector credential cannot self-assign another household. |
| Reading event | UUID event identity, device, observed UTC time, server-received UTC time, active power W, cumulative import energy kWh, counter epoch, source provenance and quality flags. |
| Coverage/interval result | Derived counter delta and exact supporting endpoints; period validity, reset/gap reasons and calculation version. Raw events remain immutable. |
| Bill upload/candidate/confirmed record | Private upload reference, extraction state and candidates, explicit user confirmation, source periods/charges and duplicate key. Historical records remain distinct from readings. |
| Calculation/insight evidence | Input references, settings revision, method/rule version, time, period, eligible/unavailable reasons; allows reproducible result and invalidation. |
| Simulation run | Owner, seed, scenario, clock, dataset identity and reset scope. Synthetic and physical data cannot silently mix. |

Money/rates use Decimal in calculation and an agreed JSON decimal representation. Energy/power must be finite, retain calculation precision, and round only on display. Database uniqueness enforces idempotency; application-side duplicate checks alone are insufficient.

## 5. Common behavior to confirm

Use UTC RFC3339 instants in storage/API and household timezone for calendar boundaries; periods are `[start,endExclusive)`. Translate local midnight boundaries before querying. Reject naive times. Reading `receivedAt` is server-controlled; replay `asOf` is a separate authorized demo clock and must not allow a caller to falsify real receipt time.

Propose cumulative imported active-energy counters, matching the collector plan. Counter deltas apply only within the same device/counter epoch. An observed counter decrease without an explicit new epoch is quarantined/rejected for review; a new epoch establishes a baseline rather than counting its initial value as consumption. Sort accepted observations by observed time before deriving intervals. A late arrival may split an old interval and invalidate dependent aggregates; it must not be added on top of the old delta.

Duplicate semantics: same authenticated collector and event ID with equivalent normalized payload returns `already_stored`; changed payload returns `conflict`. Persist per-event outcomes and acknowledge after commit. Proposed partial-batch acceptance is explicit in the contract and requires review. An unknown/foreign device must not be registered as a side effect of ingestion.

Coverage is not device connectivity. Two valid counters can establish interval energy across delayed transmission but do not reveal within-gap hourly use. Do not allocate an unbounded interval into arbitrary daily/tariff buckets by undocumented interpolation. Negative remainder is unavailable, not zero. See the [decision log](decision-log.md) for the proposed bucket/counter rules and open confirmation points.

## 6. Costs, baseline and assistant integration

Preserve the worked sample: household 12 kWh includes 4, 1 and 2 kWh appliances; other is 5 kWh. At a fictional flat TRY 3/kWh, energy charges are TRY 36, excluding other invoice components. Do not call that a complete bill estimate. Budget and forecast need the same period and charge basis.

Retain the initial seven-complete-valid-days proposal. At the end of day 10, recorded 100 kWh plus 20 days × 10 kWh/day yields 300 kWh and TRY 900. The initial proposed recomputation is daily at household midnight; intraday recorded costs can be newer than the dated forecast. No full-cycle forecast when elapsed-cycle energy is genuinely missing. Confirm freshness and budget-message rules before implementation.

Assistant functions call the same household-authorized query services. Ahmed owns provider, prompts, orchestration and model evaluation; Umut owns service access and contracts. No model credentials reach the browser. Start read-only: summaries, comparisons, contribution evidence, forecasts and insights. Preserve the normal app during provider failure. Conversation persistence and streaming are separate decisions, not silently added in BE01.

## 7. Validation gates

Before BE03–BE07, record Ahmed's decisions on authentication/session restoration, settings revision/effective dates, ingestion outcomes, interval coverage, tariff basis and forecast freshness. Frontend review confirms fields and states. Before BE08, select permitted supplier examples and confirm upload limits/retention. Before BE10, agree functions and chat response shapes with Ahmed.

Independent work continues through scaffolding, migration/health verification, mock scenario serving and draft examples. A final local demonstration still needs real ingestion → persistent storage → derived responses, two-account separation, restart persistence and frontend integration. Hardware #4 and real-household accuracy remain later verification, not completed by simulation.

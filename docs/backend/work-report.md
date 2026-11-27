# Umut's backend work — local review report

**Date:** 27 November 2026  
**Inspected main:** `261fcb430297c3aa44ecb15e9ddc9db10a61f247`  
**Local work branch:** `review/backend-handoff`  
**Handoff:** backend v1.0, 26 November 2026; uploaded DOCX SHA-256 `3cdaadbe85cab2b4b3695838aa8d3ba55a8140616a1ccaa9a7091aba8790d0b0` matches the repository copy.  
**Remote changes:** none. No push, remote branch creation, merge, PR/comment, issue edit or board transition was performed.

## What was checked

Inspected all current main repository documents and handoff files, the foundation and consumption-dashboard feature branches, branch heads, all 27 non-PR issues and assignees, and PR #13's state/review/comment records. The binary wireframe artwork is supporting documentation, not application code. Word handoff body text was extracted and the uploaded file compared with the repository copy. Existing local files were preserved in their original checkout; implementation uses a separate Git worktree.

- Main has the finalized handoffs but no backend or merged frontend.
- `dev` still points to `be54662`; frontend foundation PR #13 remains open with no reviews/comments when inspected.
- `feature/task-9-frontend-foundation` contains a runnable React sample shell. `feature/consumption-dashboard` adds separate fixture/data/energy helpers. They remain unintegrated.
- The current handoff assigns backend calculations and baseline forecasts to Umut, assistant/ML work to Ahmed, and current frontend tasks to Miray.
- [Detailed repository findings](repository-review.md) include scope mismatches, interface gaps, and incorrect/ambiguous dependency references.

## Your tasks and what this increment does

| Issue | Current assignment/status | Local result | Still required |
|---|---|---|---|
| #14 Backend design/first contract | Umut, open | Concrete design proposal, decision log, entity/time/auth/ingestion recommendations and scope reconciliation | Ahmed's confirmation of pending decisions; frontend interface review |
| #11 Frontend–backend contract | Umut, open | Versioned draft contract, JSON Schema, five concrete normal/failure examples and screen/capability mapping | Agree schemas and proposed changes with Ahmed/Miray |
| #12 Mock API | Umut, open | Runnable opt-in HTTP overview/device fixture routes, five selectable scenarios, bounded loading delay, errors and startup guide | Teammate adopts request layer and reviews draft meanings; not a production backend |
| #15 Runnable backend/database | Umut, open | FastAPI/configuration, SQLAlchemy/Alembic, migration, live/ready checks, SQLite and PostgreSQL verification, reproducible locks, Windows/Linux instructions | Stack decision and independent teammate setup review; business schema comes later |
| #16 Accounts/household settings | Umut, open | Account/settings/session proposal and validation/ownership requirements prepared | Confirm session/CSRF and settings/tariff rules, then implement persistence and two-account checks |
| #17 Devices/reading ingestion | Umut, open | Counter/identity/idempotency/late-arrival/batch proposals and failure scenarios prepared | Confirm shared reading semantics, implement against approved account ownership |
| #18 Synthetic generator/replay | Umut, open | Seed/clock/replay design and 22 expected scenario definitions prepared | Implement generator through actual ingestion API after #17; fixture JSON is not ingestion |
| #4 Real plug reading/storage | Umut, open | Future adapter/ingestion boundary retained | Accessible physical plug and real acquisition/storage verification |

Previously assigned #2, #5, #8 and #9 are closed. Their artifacts were inspected, not redone. Backend handoff BE06–BE11 have no dedicated mapped issues yet; [task mapping](task-mapping.md) records them without creating issues. “Task 1–4” in #15–#18 are ambiguous queue references; proposed corrected dependencies are #14→#15→#16→#17→#18, subject to backlog confirmation.

## Deliverables

- [Backend design](design-proposal.md), [decision log](decision-log.md), [task mapping](task-mapping.md), [scope reconciliation](scope-amendment.md), and [scenario definitions](scenario-definitions.md).
- [Shared draft contract](../api/frontend-contract.md), [synthetic JSON Schema](../api/dashboard-response.schema.json), and five snapshots under `docs/api/examples/v0.1/`.
- [Runnable backend and instructions](../../backend/README.md): startup, health, migration, optional PostgreSQL, opt-in mock and tests.
- Root README status/roles/setup links updated locally to reflect this increment. Handoff index adds links to the design artifacts. Finalized handoff body files and authoritative MVP scope were not rewritten.

## What actually runs

`GET /api/v1/health/live` tests process liveness. `GET /api/v1/health/ready` checks database connectivity, expected migration revision and foundation table. Explicit Alembic migration creates only neutral service metadata; no unapproved account/reading schema was implemented.

With `WATTWISE_ENABLE_DEMO_API=true`, `GET /api/v1/demo/overview` and `/devices` serve `normal`, `empty`, `partial-data`, `device-disconnected`, and `error` examples from the proposed contract. `delay_ms` is bounded to 0–2000. The mock is absent by default. All results carry synthetic provenance, fixed snapshot time and runtime request correlation IDs. Error responses are sanitized; exact development origins are allowed without credentials.

This is deliberately separate from a stored-reading backend. It does not generate readings, authenticate users, process private bills, calculate real tariffs, train forecasts or call a model. The final handoff requires those later capabilities through a persistent, authorized ingestion pipeline.

## Verification performed

Environment: Python 3.12.14 on Linux, pinned FastAPI/SQLAlchemy/Alembic dependencies, SQLite and disposable PostgreSQL 17 Alpine. Docker image digest used is pinned in `backend/compose.yaml`.

| Check | Result and boundary |
|---|---|
| `python -m pytest -q` | **24 passed**: request handling, mock opt-in, all five fixtures and schema, worked values, timestamp bounds, missing/corrupt examples, query validation, CORS, migration round trips and readiness, restart persistence |
| `python -m pip check` | No broken requirements |
| Clean-copy installation | Created new source copy and virtual environment in `/tmp`, installed `requirements.lock`, installed project, migrated SQLite, ran persistence verification and the same **24 tests passed** |
| Running Uvicorn HTTP checks | live/ready/normal/devices/empty/partial return 200; error scenario503; invalid scenario422 |
| SQLite restart check | A committed neutral service-state record survives new engine/application creation; verification command cleans only its own unique record |
| PostgreSQL migration + restart | Migration ran against a real PostgreSQL container; readiness passed; committed service metadata survived both engine recreation and container restart |
| Browser-to-API CORS | Chromium page from an actual loopback frontend-origin test HTTP server fetched the synthetic overview successfully. This was a test harness, not an integrated React screen. Disallowed-origin header behavior is covered by request tests. |
| Source/docs | Python compile check, local links and `git diff --check`; published handoff files unchanged |

The locked current Starlette version emits one HTTPX TestClient deprecation warning. Tests pass; future maintenance should migrate the test adapter as supported. A first intercepted-page browser harness could not fetch loopback due to browser networking context; the check was repeated using a real local HTTP origin and passed. No feature code was changed to bypass that browser context issue.

Clean-copy verification is automated, not a claim that a teammate independently followed the guide. Linux was executed; Windows commands are provided but not executed here. Neutral metadata persistence is not proof that account/household settings persist, since those models are not implemented yet.

## Decisions needed before dependent implementation

The uploaded handoff explicitly says: **“Umut and his GPT must propose unresolved business rules and concrete API schemas, obtain Ahmed’s confirmation for affected behaviour, and record approved decisions before implementation.”** Its independent-work paragraph permits scaffolding, health checks, configuration and draft schemas while review is pending. This report follows that distinction rather than treating unanswered proposals as approval.

The [decision log](decision-log.md) supplies recommendations, reasons, examples, frontend impact and alternatives. First review D01–D07: stack, cookie+CSRF/session restoration, ownership, settings/tariff schema, exact reading format, batch/idempotency and coverage semantics. D08–D14 cover tariff/forecast freshness, scenarios, bill samples/retention, insights, assistant interface and scope reconciliation.

The handoffs expand the older hardware-only/no-chat MVP to a laptop synthetic demo with assistant integration. The [scope proposal](scope-amendment.md) records the difference and keeps real-hardware #4 and real-household evaluation separate. Hardware is unavailable here, supplier samples remain unselected under Ahmed's #3, and provider/model work belongs to Ahmed.

Next implementation after the relevant decisions: #16 accounts/settings → #17 registered-device ingestion → #18 seeded history and replay → BE06 consumption/device services. Connect Miray's frontend at the first saved-settings/consumption checkpoint, then add costs/forecasts, bills, insights and assistant integration in handoff order.

## How to review locally

Open `backend/README.md` and follow its OS-specific quick start, then inspect `/docs` and enable the mock flag for scenario requests. No hardware or npm installation is needed to test this backend scaffold. Review the decision log and example payloads alongside the handoff before adopting the proposed contract.

No GitHub operation is implied by running this package. Uploading, creating PRs, changing assignments and merging still require Umut's explicit instruction.

# Backend task and handoff mapping

**Snapshot:** 28 November 2026 · **Handoff:** backend v1.0 and Ahmed’s D01–D14 review

GitHub assignee `GlobalUmut` is Umut. The assigned backend work covers #4, #11, #12, #14–#18 and #30. Closed assigned groundwork is #2, #5, #8 and #9. Ahmed owns the assistant and ML issues #24–#28, and Miray owns frontend #6 and #19–#23.

## Active queue

| GitHub issue | Handoff mapping | Existing evidence / next action | Completion boundary |
|---|---|---|---|
| #30 Finalize implementation decisions | BE01 follow-up | [Decision log](decision-log.md) records Ahmed’s approvals and prioritized proposals. [Scenario definitions](scenario-definitions.md) and shared examples give expected outcomes. | Ahmed confirms choices required by the next increment and Miray reviews relevant shared fields and states. |
| #14 Propose backend design and first API contract | BE01 | Ahmed approved the core design direction with qualifications. | Record approval evidence and track exact open behavior under #30. |
| #11 First frontend–backend data contract | BE01 cross-cutting | Ahmed reviewed dashboard behavior, requested aligned selected-period outputs and concrete incomplete setup. | Confirm remaining choices and complete Miray’s review of fields, states and payloads. |
| #12 Mock API | FE02 support | Ahmed independently verified pinned installation, 24 tests and all five mock scenarios at the reviewed commit. | Align fixtures with #11 and verify frontend scenario switching. |
| #15 Runnable backend/database | BE02 | Ahmed accepted the local Linux/SQLite foundation following independent startup, migration, health, restart and mock gating checks. | PostgreSQL is the approved integrated demo target. Independent PostgreSQL, Windows and account persistence validation have their own checkpoints. |
| #16 Accounts and persistent household settings | BE03 | Depends on BE02 and agreed auth/settings/period/tariff contract. | Persist/reload/restart, invalid inputs, two-user separation, frontend connection. |
| #17 Device registration and ingestion | BE04 | Depends on BE03 and approved reading/counter/idempotency semantics. | Device ownership, unchanged retry, conflict, late arrival/reset, retrieval and failures through API. |
| #18 Synthetic household generation/replay | BE05 | Scenario plan in this package; implement against BE04 API after rules agree. | Real HTTP ingestion, persistent events and deterministic replay outcomes; static dashboard JSON alone cannot complete this. |
| #4 Real plug reading/storage | Later physical adapter/BE04 validation | Software pipeline can prepare; no device/API access or onsite hardware evidence available here. | Real plug acquired reading→backend storage→retrieval, validated units/reset/disconnect behavior. Simulation cannot close #4. |

Issue #15's “Task 1”, #16's “Task 2”, #17's “Task 3” and #18's “Task 4” are ambiguous inherited queue numbers. Recommended intended dependencies are respectively #14/BE01, #15/BE02, #16/BE03 and #17/BE04, not literal GitHub issues #1–#4. Ahmed should confirm this mapping during backlog review; no issue text was silently edited.

## Remaining backend handoff work requiring mapped issues

| Handoff | Suggested issue scope (not created) | Dependencies / owner |
|---|---|---|
| BE06 | Serve consumption aggregates, trends, matching contributions/remainder and device/collector status | BE04–05, D04–D07/D10; Umut. Frontend #22/#23 depend on this. |
| BE07 | Calculate costs and explainable baseline forecasts | BE06 and D08–D09; Umut. Coordinate Ahmed #28's future candidate through same response contract. |
| BE08 | Upload/extract/review/confirm bills and manual fallback | BE03, D11 and sample selection #3; Umut. Supplier-specific acceptance waits for samples. |
| BE09 | Budget alerts and reproducible recommendation evidence | BE07, D12 and existing insight scenarios; Umut. |
| BE10 | Authorized query functions and assistant integration endpoint | BE06–09, D13 and Ahmed #24–#27; joint integration, Umut services/Ahmed model orchestration. |
| BE11 | Verify integrated local journey, persistence and failure scenarios | BE03–10 plus frontend FE03–10; Umut and Miray jointly with Ahmed review. |

Do not create duplicate issues automatically. The table is a mapping proposal that lets Ahmed choose whether to create separate work units or extend current tasks.

## Completed groundwork retained

- #2 hardware comparison: evidence in `docs/WattWise_Hardware_Comparison.txt`.
- #5 journeys/screen requirements: documentation and wireframes on main.
- #8 collector plan: dedicated device/hardware plan retained for future physical integration; local first-demo approach is reconciled separately.
- #9 frontend foundation: closed issue, but its code still resides on `feature/task-9-frontend-foundation`; PR #13 is open into `dev`. A closed issue is not proof the application has been integrated.
- #7/#10: Ahmed's display rules and insight scenarios supply examples; their own documents still contain proposed product rules, so do not infer every detail is approved from issue closure.

## Review record to maintain

For each increment record issue, inspected base SHA, local branch, handoff and contract version, changed behavior, commands/results, decisions needed and reviewer outcome. Keep synthetic versus physical completion distinct. This package adds no commits, pull requests, comments or board transitions remotely.

# Repository review — 27 November 2026

Read-only repository and assignment inspection; implementation details are recorded in [work-report.md](work-report.md).

WattWise repository and handoff audit — 27 November 2026

READ-ONLY REVIEW BASE
main: 261fcb430297c3aa44ecb15e9ddc9db10a61f247
 dev: be54662eba9d813da0fb6374b5d15cec941f6b9e
foundation: c569e6b3b3d6649eef7cc7c1b7064a804f2eec76
consumption dashboard: 2bc57fab0460c6a6cac46064838b61f7da5b706f
The worktree initially contained only repository documents, not a backend or integrated frontend.
The uploaded backend DOCX exactly matches the repository DOCX (SHA-256 3cdaadbe85cab2b4b3695838aa8d3ba55a8140616a1ccaa9a7091aba8790d0b0).
No repository files, branches, issues or remote data were changed by this audit.

CURRENT OWNERSHIP / TASK SEQUENCE
Umut open issues: #4 real plug integration; #11 frontend/backend contract; #12 mock API; #14 backend design; #15 runnable backend/database; #16 accounts/household persistence; #17 registration/ingestion; #18 generator/replay.
Closed existing Umut tasks: #2 hardware comparison, #5 screen requirements, #8 collector plan, #9 frontend foundation. Their closure must not be interpreted as completed hardware/persistence/authentication work.
The handoff maps BE01 to #14 and overlaps #11; BE02 to #15; BE03 to #16; BE04 to #17; BE05 to #18. #12 remains explicit mock development; it does not demonstrate ingestion. #4 is later physical validation, distinct from synthetic completion.
BE06 consumption/device services, BE07 costs/baseline forecasts, BE08 bills, BE09 insights, BE10 assistant support, BE11 integrated demonstration have no direct dedicated issue numbers in the current list. Preserve handoff IDs and propose issue mapping for backlog review instead of silently assigning unrelated issues.
Issue #15's dependency Task 1 means design/BE01 (#14), not historic #1 MVP scope. #16's Task 2 means scaffold/BE02 (#15), not historic #2 hardware comparison. #17's Task 3 means account/BE03 (#16), not historic #3 sample bills. #18's Task 4 means ingestion/BE04 (#17), not physical plug #4. This dependency-reference ambiguity should be recorded and corrected with team authorization.
Miray owns #19–23 and existing #6. Ahmed owns #24–28, bill samples #3 and existing analytical scenarios. Do not implement or claim their human reviews on their behalf.

SAFE INDEPENDENT INCREMENT NOW
The backend handoff explicitly allows repository inspection, scaffolding, health checks, configuration, draft schemas/examples and routine internal decisions while reviews are pending. Deliver #14/#11 as complete, versioned design proposals with worked examples and pending decisions; build #15 scaffold with health/readiness and database migration verification; #12 can serve explicitly synthetic HTTP fixtures using a versioned draft contract. Do not claim fixture-based responses establish BE04/BE05 ingestion or BE06 authoritative calculations.
Exact account/session transport, reading validation/idempotency, aggregation/coverage, tariff edits, forecasting staleness and shared response schema are not approved simply because they are recommended. The handoff explicitly requires Ahmed confirmation for unresolved product/shared-interface behavior before dependent implementation. #16–18 must identify these dependencies honestly rather than build unreviewed production semantics and call them complete.
Physical #4 needs chosen accessible hardware and cannot be completed in this cloud workspace from synthetic data.

SCOPE AND DOCUMENT CONFLICTS
1. Older docs/mvp-scope.md calls itself authoritative, requires real physical household/plug measurements for completion and excludes conversational LLM integration. New v1.0 handoffs explicitly add local synthetic delivery and assistant integration, assign baseline forecasting to Umut, assistant/ML to Ahmed. Record a scoped update proposal and link source authority; do not erase physical validation criteria or pretend simulated results establish hardware accuracy.
2. Collector plan requires a dedicated Pi from simulation onward; current handoff's first demonstration runs on a teammate laptop. Treat dedicated physical collector as later integration unless Ahmed confirms otherwise. Preserve shared ingestion path, source labels, storage semantics, clocks and offline behavior in both settings.
3. README role table still gives bill extraction, tariff calculations, forecasts and recommendation logic to Ahmed, while current handoff gives backend calculation implementation/baseline to Umut. README says no implementation exists; correct for main itself, but misses runnable frontend on feature branch. Its current-file inventory also omits many newer docs.
4. Word handoffs reference docs/product/insight-scenarios.md; actual path docs/insight-scenarios.md is already explicitly corrected in docs/handoffs/README.md. Do not duplicate/move it without intent.
5. Both Word/Markdown handoffs must retain matching version when approved content changes. Current upload exactly matches published baseline; no need to replace it.
6. Seven complete days is explicitly proposed in display rules. The product-contract decision must confirm eligibility, partial-day extrapolation, omitted earlier cycle handling and forecast freshness. Fixed dated fixture forecast does not establish a live recomputation rule.

BRANCH / FRONTEND INTEGRATION
main advanced to the handoff publication commit while dev remains at be54662. Foundation PR #13 remains open in parent API inspection; no merge assumed. Frontend and fixtures live on separate feature branches. Neither branch contains current handoffs merely because they descend from an earlier main; merging with a common ancestor need not delete handoffs.
The branches add disjoint file names, so previous conflict assessment remains valid, but no combined build or integration was performed by this audit.
Foundation uses React/TS/Vite/Router, Recharts and plain CSS, routes and explicit placeholders. Accounts are disabled; settings validate in memory and do not affect dashboard; bill upload/storage and authentication do not exist. App routes are public sample routes. Do not connect private data before backend ownership checks and UI session clearing.
Dashboard screen imports fixed src/data/sample.ts directly. Miray dashboardApi.ts imports JSON fixtures and returns promises; it performs no HTTP, time filtering, authentication, abort handling or runtime response validation. A shared request adapter must eventually replace source choice once rather than duplicate fixture truth in screens.
Miray fixtures are compatible with documented base arithmetic (12 household, 4/1/2 appliances, 5 other), explicit sample labels and timestamps. They omit costs/forecasts/trends/settings contract coverage needed for newer screens.
Miray energy helpers handle null and negative remainder but do not validate finite/nonnegative numeric input, matching interval coverage, or part exceeding household. householdSharePercent can return nonsensical negative or >100 shares if called unchecked. These are preview formatting/helpers, not authoritative backend validation.
Foundation tsconfig includes src and vite.config, with Bundler module resolution. Confirm JSON import support before combining Miray JSON module imports; do not claim combined build verified.
Version pins are present in foundation package-lock. Reuse them rather than initializing another unrelated frontend or overwriting the feature branch. Technology review is explicitly pending in foundation/handoffs.

SECURITY / CONTRACT REVIEW POINTS
Authorize all reads/mutations/ingestion by server-side household membership/device registration, not user-supplied household ID alone. Define session revocation/expiry, password hashing, allowed origin/credentials policy and CSRF if cookie sessions are selected. Never permit arbitrary CORS with credentials. Mock routes must be unmistakably synthetic and disable-able, not a path to private production records.
Ingestion needs per-event stable IDs, conflicting-repeat errors, transaction/ack semantics, out-of-order behavior, epoch/reset handling, finite units/values and separately observed/received timestamps. Plain latest-power snapshots cannot establish interval kWh.
Persist scenario clock and source provenance; recovery gaps do not automatically imply missing accumulated energy, and accumulated interval recovery cannot reconstruct hourly detail.
Budget/forecast comparisons require same household, cycle and charge basis. Fictional TRY3/kWh is energy-only, not a validated Turkish invoice tariff. Historical bill totals cannot imply a marginal rate or be summed into overlapping monitor data.
Health must separately distinguish process liveness from database readiness. Readiness failures should not reveal DSNs/credentials or raw exception details. Migrations and restart persistence need actual checks and documented commands; SQLite-only validation does not prove PostgreSQL runtime compatibility.
Bill uploads need selected samples, type/size validation, retention, explicit candidate confirmation, duplicate submission semantics and household access. #3 still blocks supplier-specific extraction acceptance.
Assistant functions must carry the same authorized household scope as regular API. Model/provider setup/evaluation belongs to Ahmed and is not satisfied by a dummy chat response.

RECOMMENDED REVIEW PACKAGE
Versioned design proposal + API contract/examples; decision log distinguishing existing agreement/proposed/pending; handoff-to-issue mapping with corrected dependency references; scope update proposal; operational scaffold/mock README; actual build/test evidence; explicit remaining work #16–18 and BE06–BE11. No issue closure or push is warranted until user approval.


FOLLOW-UP: LOCAL SCAFFOLD REVIEW (root-added files; not initial remote inventory)
Reviewed backend/src/wattwise config.py, db.py, main.py, migrations/env.py, migration 0001_service_state.py, pyproject and draft dashboard schema/examples. No edits to implementation were made by auditor.
Health/mock-only structure keeps unapproved business behavior out. Demo routes are opt-in, CORS credentials disabled, responses use no-store, SQLAlchemy hide_parameters enabled, and readiness catches connection/schema failures without returning DSNs. No immediate private-household access path exists because no private household data or auth endpoint exists yet.
Review fixes communicated to root: shared error shape mismatch (validation produces field/message, contract specifies path/code/message and retryAfterSeconds); HTTPException headers need preserving (e.g. 405 Allow); fixed fixture requestIds vs dynamic X-Request-ID should not be confused. Consider explicit fixture shape verification so malformed-but-valid JSON is not returned as an apparently successful sample.
Fixture arithmetic is internally consistent for base energy and fictional costs. In several fixture responses generatedAt is 14:30 but lastReceivedAt is 14:30:01; generated response time should not precede the receipt of included records. Agent preparing contract was notified; asOf can remain the observation cutoff while generatedAt moves later.
Suggested meaningful test edges: unconfigured/unmigrated DB vs available-but-wrong-schema DB; dropped service_state table; DB URL secrets absent from HTTP errors; explicit migration upgrade/downgrade and persisted state after engine restart; demo disabled route absence; supported/invalid scenario and delay bounds; missing/corrupt fixtures; allowed and denied origins including preflight; method-not-allowed headers; request IDs and no-store on all success/failure paths; partial/disconnected cases preserve valid household totals while suppressing dependent remainder; error fixture returns 503 rather than 200.
Do not characterize SQLite tests as verified PostgreSQL integration. Database driver import/migration portability checks differ from a real PostgreSQL instance.

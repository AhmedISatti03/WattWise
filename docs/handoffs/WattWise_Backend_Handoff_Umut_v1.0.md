# WattWise Backend Engineering Handoff

Version 1.0  |  26 November 2026

For Umut Topatan and his assisting GPT. Prepared for review by Muhammad Ahmed Satti, Group Lead, Software Development and AI Systems Engineering.

Build the backend for a complete local WattWise demonstration. Synthetic household and appliance readings must enter an ingestion API, persist in storage, and drive the actual dashboard, costs, forecasts, alerts, and recommendations. Account setup, tariff settings, bill confirmation, and assistant access must connect to that same household data.

### 1 How to use this handoff

Read this document alongside the assigned GitHub issue and current repository instructions. First inspect the existing implementation and relevant documents. Work in dependency order, deliver a reviewable increment, and show the evidence required by the issue. Explain implementation decisions so Umut can understand and maintain the result.

Use this handoff to deliver Ahmed’s agreed backend scope. Task references BE01–BE11 identify the work sequence and will be linked to GitHub issues during backlog setup. Umut and his GPT must propose unresolved business rules and concrete API schemas, obtain Ahmed’s confirmation for affected behaviour, and record approved decisions before implementation. Routine internal choices and independent work can proceed.

### 2 Roles and ownership

| Person | Responsibility |
| --- | --- |
| Umut Topatan | Backend implementation, persistence, ingestion, simulation, calculations, baseline forecasting, and API contract proposals. |
| Miray Pınarbaşı | Frontend implementation and API integration. Review response shapes against screen needs. |
| Muhammad Ahmed Satti | Technical coordination, coding, integration and review, conversational assistant, AI evaluation, and ML forecasting improvements. |

### 3 First demonstration outcome

Run the web frontend and backend on a teammate’s laptop. A user can register, create a household, configure dates, tariff and budget, upload and confirm a supported bill, inspect simulated consumption, and obtain calculated costs, a baseline forecast, alerts, and recommendations. Ahmed’s assistant can retrieve authorized results and answer questions through the backend integration.

## 4 Agreed scope and design confirmation

### Core delivery

Implement persistent account and household setup, one household monitor and two or three monitored appliances, consumption views, cost estimation and baseline forecasting, bill extraction and confirmation for one supplier format, in-app budget alerts, and explainable recommendations. All synthetic data must be identifiable in the API and interface.

Ahmed develops the conversational assistant and evaluates future ML improvements. Umut provides the integration functions and a working baseline forecast. Broader room and family management, appliance control, external assistant connectors, and native mobile applications remain roadmap items unless Ahmed explicitly adds them to a delivery task.

### Decisions Umut should propose

| Topic | Proposal must resolve |
| --- | --- |
| Technology | Framework, database, migrations, authentication, OCR dependencies, and local startup. Python/FastAPI and PostgreSQL are provisional suggestions. |
| Measurements | Reading schema, power and energy semantics, timestamps, sampling assumptions, duplicates, counter resets, late arrivals, and coverage. |
| Billing | Cycle boundaries, tariff arrangement and charges, effective dates, rounding, corrections, and historical calculation behaviour. |
| Forecasts | Baseline formula, eligibility, usable history, incomplete cycles, update frequency, stale results, and evaluation. |
| Integration | Endpoints, errors, pagination, filters, polling or refresh behaviour, and assistant function inputs and outputs. |

Submit each decision with the recommended rule, rationale, a worked example, alternatives where meaningful, frontend implications, and questions requiring confirmation. Record the response and affected issue references in a decision log. Existing approved rules remain the starting point. Clearly identify any proposed change.

### Continue useful work while review is pending

Repository inspection, scaffolding, health checks, configuration, draft schemas and examples can proceed independently. Resolve routine internal implementation choices locally. Seek confirmation for outstanding product rules and shared interface decisions before building behaviour that depends on them.

## 5 Repository starting point and coordination

Repository — AhmedISatti03/WattWise. At the latest check in this planning conversation, main and dev pointed to be54662. Recheck the live repository at task start and record the branch and commit inspected.

| Existing work | How to use it |
| --- | --- |
| docs/mvp-scope.md | Seven core features, account boundaries, measurement meaning, and acceptance criteria. |
| docs/energy-display-rules.md | Worked energy and cost examples and unavailable-data behaviour. |
| docs/product/insight-scenarios.md | Forecast, overspend and recommendation examples. Inspect current wording. |
| docs/architecture/collector-plan.md | Collector ingestion, timestamps, buffering, retries and simulator context. |
| docs/frontend/screen-requirements.md and wireframes | Screen data requirements and user journeys. |
| feature/task-9-frontend-foundation and PR 13 | React/TypeScript foundation, routes, sample dashboard and placeholders. |
| feature/consumption-dashboard | Miray’s fixtures, dashboardApi.ts and domain/energy.ts helpers. |

The frontend settings and account screens currently demonstrate UI behaviour. Their existing presence does not establish persistence or authorization. dashboardApi.ts currently returns local fixtures. Integration must replace that source with real HTTP requests to this backend.

### Existing issue alignment

Review #11 for the frontend–backend contract and #12 for the mock API. Align the simulator and ingestion work with #4 and the collector plan from #8. Coordinate dashboard work with #6 and foundation work with #9. Bill samples belong to #3. Inspect issue states and descriptions before proposing new issues, and avoid duplicate work.

### Source authority and change tracking

Ahmed’s confirmed decisions in this handoff extend the repo’s older scope to the current simulated delivery and assistant integration. The repo scope still describes physical-device completion and excludes conversational AI. Record that difference and propose the specific scope update for review. Simulated completion must be reported separately from later hardware validation.

Propose repository homes for the approved API contract, decision log, scenario definitions, and task-to-handoff mapping. Keep them versioned and link them from both handoffs. Do not silently change shared field names, meanings or endpoint behaviour during another task.

## 6 Shared API contract requirements

BE01 must turn these capability requirements into concrete schemas and examples reviewed with Ahmed and Miray. Exact endpoint names, request and response payloads, and outstanding calculation rules will be recorded in the approved shared API contract.

| Capability | Contract coverage |
| --- | --- |
| Accounts and household | Registration, sign-in, sign-out, current user, household creation and retrieval, dates, budget and tariff updates. |
| Devices and readings | Device identity and scope, reading ingestion, ingestion results, list/status, last observed and received times. |
| Consumption | Overview, trends, individual appliances, matching period contributions, calculated remainder and quality. |
| Costs and forecasts | Observed period, cost components, forecast eligibility, method, calculation time, projected interval and assumptions. |
| Bills | Upload, extraction status, editable candidates, validation, explicit confirmation and confirmed records. |
| Insights and assistant | Alerts and recommendation explanations, acknowledgement behaviour if included, authorized query functions for Ahmed. |

### Every data response needs explicit meaning

Define stable identifiers, units, timestamp format, household timezone, interval boundaries, source type, data coverage and nullability. Specify the difference between an empty result, zero usage, missing data, a pending calculation, and a failed request. Define machine-readable reasons and human-readable explanations for unavailable results.

Separate current power, accumulated energy, historical bill consumption, calculated remainder, estimated monetary cost and future forecast. Include an as-of time or equivalent so the frontend can communicate freshness. Decide how trends are bucketed and how partial buckets are identified.

### Errors and validation

Agree HTTP status behaviour and a consistent error structure containing a stable code, message, relevant field errors and retry guidance where applicable. Cover unauthorized access, invalid dates, unsupported uploads, unavailable forecasts, ingestion conflicts and service failures. A valid response with insufficient history should communicate that state explicitly.

### Frontend integration agreement

Publish example payloads for normal, empty, partial-data, disconnected-device and error scenarios. Miray should implement through a shared data-access layer. The backend remains responsible for authoritative calculations. Frontend helpers may format values and preview approved examples, while matching backend semantics. Configure local API origin, permitted frontend origin and authentication transport together.

## 7 Reading ingestion and synthetic simulation

### One ingestion path

The simulator submits readings through the documented ingestion API. Storage, aggregation and dashboard responses must exercise the same application logic intended for the future collector. A saved dashboard JSON response alone does not demonstrate ingestion or calculation.

### Reading model proposal

Propose fields for household and device identity, measurement scope, observed time, received time, power in W, and energy in a documented representation. Distinguish cumulative energy counters from interval energy. Explain how a counter delta becomes energy for a period and how resets or replacements are represented. State whether source event IDs or another stable key establish idempotency.

Define batch validation and partial-failure behaviour. Retrying an accepted batch must preserve totals. Conflicting repeats, out-of-order readings, invalid units, implausible values and unknown devices need documented handling. Resolve ownership from authorized device credentials or server records. Validate access on every ingestion and read operation.

### Historical dataset and ongoing stream

Generate coherent household and appliance data with a reproducible seed and documented simulated clock. Household totals include monitored appliances plus other loads. Produce enough history to exercise the approved forecast method and reserve later periods for evaluation. Make the historical start date and stream behaviour configurable.

Provide commands to generate, import, start, stop and replay a scenario. Support a normal-speed demonstration and an accelerated replay if practical. Make calculations and freshness checks use the same scenario clock. Explain exactly what reset removes and keep reset actions restricted to demo data.

### Required scenario families

- Normal usage, different daily patterns, below-budget and above-budget households, and a partial current day.

- No readings, insufficient history, a missing tariff, monitoring begun mid-cycle, missing intervals, and delayed delivery.

- A disconnected plug, a disconnected collector, recovery with buffered readings, duplicates, counter resets and late arrivals.

- Appliance totals exceeding the household total over a comparison period, plus invalid ingestion and failed API requests.

Document expected outcomes before running a scenario. Synthetic normal data must be internally coherent. Introduce inconsistent values deliberately in the designated failure scenarios and retain their quality flags.

## 8 Consumption costs and baseline forecasting

### Measurement rules already agreed

The household monitor includes monitored appliances. Never add appliance energy onto the household total. Compute other consumption only over matching periods with sufficient data. Missing readings must remain distinguishable from zero. Surface negative or unreliable remainders with an explanation.

Track coverage separately for household and appliance measurements. A missing plug can affect its contribution and the remainder while leaving valid household totals available. Device connectivity, collector connectivity and a failed dashboard request represent different states.

### Cost and tariff proposal

Select one supported Turkish tariff arrangement and document the applicable consumption charges and other invoice components. Use an explicitly fictional tariff for early deterministic examples until the chosen arrangement is validated. Label energy-only estimates accordingly. Propose effective dates, precision, rounding and how edits affect past calculations.

Confirmed bills are historical records. Their consumption must not be added to overlapping monitor readings. Define how bill information supplies tariff suggestions or known historical usage, including explicit user confirmation and provenance. A bill total alone does not establish a marginal unit rate.

### Baseline forecasting owned by Umut

Propose an explainable method using valid historical household consumption to project remaining-cycle energy, then apply the configured tariff. Existing scenarios use seven complete valid days as the initial eligibility assumption. Check that assumption against the repo and propose any refinement for Ahmed’s confirmation.

Define treatment of partially observed cycles and gaps. Seven recent days do not establish consumption for an unobserved earlier part of the cycle. Identify any estimated historical segment separately and document the conditions under which a full-cycle bill forecast can be shown.

Return method identity and version, as-of time, period boundaries, history used, observed and projected components, coverage, assumptions, and reasons for unavailable results. Decide recomputation and stale-result rules. Budget comparisons must use the same household, period and charge basis.

### Worked acceptance examples

For an illustrative flat energy tariff of TRY 3/kWh, 12 kWh costs TRY 36 in energy charges. Appliance values of 4, 1 and 2 kWh are parts of that 12 kWh, leaving 5 kWh as other consumption when coverage permits. A same-basis TRY 900 forecast and TRY 800 target imply TRY 100 projected overspend. These numbers establish arithmetic expectations for synthetic scenarios.

Preserve the forecast response contract when Ahmed introduces an ML alternative. Compare methods on later withheld periods and report errors with their units and data limitations. Synthetic evaluation cannot establish accuracy in real households.

## 9 Bill processing insights and AI integration

### Bill ingestion and confirmation

A supplier format and permitted sample bills have not yet been selected. Coordinate that selection with Ahmed under #3. Meanwhile implement the upload workflow, editable candidate fields and manual entry against documented examples. Supplier-specific extraction acceptance depends on the selected samples.

Support a photo or PDF, report extraction status, return editable candidates with missing or questionable fields identified, and save a confirmed bill only after explicit user confirmation. Validate billing dates, consumption and charges. Allow corrections and document duplicate submission behaviour. An OCR result must retain its provisional status until confirmed.

Choose an existing OCR capability and propose setup requirements. Test readable and poor images, text PDFs, scanned PDFs, unsupported files and extraction failure. Restrict uploads by validated type and size. Define original-upload retention, household access, and deletion. Use consented or redacted samples and a clearly fictional demonstration bill.

### Alerts and recommendations

Implement the existing scenario rules with supporting values and period references. Suppress forecast-based overspend conclusions when forecast eligibility or freshness is inadequate. Define repeat-alert and resolution behaviour. A budget edit must produce the expected updated result.

Recommendations must explain why they appeared, using valid appliance comparisons or household patterns. Cheaper-hour advice requires a tariff with cheaper periods. Avoid identifying an unmonitored appliance from the remainder. Record rule identity and the evidence used so results can be reproduced.

### Assistant integration owned jointly with Ahmed

Expose documented application functions for household summaries, trends, devices, tariff and billing context, forecasts and insight evidence. Confirm schemas with Ahmed before he connects the model. The same authorized household scope must apply to both the normal API and assistant functions.

Ahmed owns model-provider selection, prompts, tool orchestration and AI evaluation. Umut supplies callable services, errors and integration support. The frontend chat request reaches the backend, which coordinates Ahmed’s assistant code. Model credentials remain server-side. A failed model request should produce a clear chat error while dashboard functions remain usable.

Define an answer structure with response text, supporting data references, periods and data-source labels, plus insufficient-data and provider-failure behaviour. Confirm conversation persistence with Ahmed. Read access to household information is the initial integration capability. Appliance actions require a separately confirmed delivery task and action contract.

## 10 Backend task sequence for GitHub

These proposed tasks map to the existing issue set where appropriate. Their final issue numbers, assignees and board states will be established during backlog review. Priority follows dependencies, while independent bill and frontend work can proceed alongside implementation.

### BE01 Inspect and propose the backend design

Dependencies — Current repository and this handoff, sections 4–6. Handoff sections 4–6 and 12.

Work — Inventory branches, issue deliverables and existing rules. Submit technology, business-rule and API proposals with examples. Draft the shared contract and decision log.

Acceptance — Ahmed confirms outstanding product rules and interfaces. Miray checks screen coverage. Record remaining questions and work that can proceed.

### BE02 Establish the runnable backend

Dependencies — Confirmed technology choices from BE01. Handoff sections 4–6 and 12.

Work — Create configuration, database migrations, health checks, startup instructions and a minimal request path.

Acceptance — A teammate can start the service and database from a clean checkout. Required configuration is documented and secrets are excluded from commits.

### BE03 Implement accounts and household settings

Dependencies — BE02 and approved account, tariff and period schemas. Handoff sections 4, 6 and 12.

Work — Persist accounts, authentication, household ownership, dates, budget, tariff and device associations.

Acceptance — Settings survive restart. Invalid input is explained. A second account cannot read or change the first household’s records.

### BE04 Implement ingestion and reading storage

Dependencies — BE03 and approved reading and retry semantics. Handoff sections 6–8 and 12.

Work — Build validated ingestion, storage, retrieval and device freshness inputs. Cover duplicates, resets, gaps and late arrival.

Acceptance — Repeat ingestion leaves totals consistent. Device identities, units and periods are verifiable. Invalid or conflicting data follows the contract.

### BE05 Generate and replay synthetic households

Dependencies — BE04 and approved scenario definitions. Handoff sections 7–8 and 12.

Work — Build historical generation and ongoing stream commands using the ingestion API. Document seed, clock and reset behaviour.

Acceptance — A recorded scenario can be replayed with the same expected outcomes. Household totals and appliance contributions reconcile in normal data.

### BE06 Serve consumption and device views

Dependencies — BE04–BE05 and approved aggregation and coverage rules. Handoff sections 6–8 and 11–12.

Work — Implement overview, period selection, trends, contributions, remainder and status responses.

Acceptance — Miray can connect the dashboard. Period changes alter results correctly. Missing-device and partial-data states match contract examples.

## 11 Backend tasks continued and integration checks

### BE07 Calculate costs and baseline forecasts

Dependencies — BE06 and confirmed tariff and forecast rules. Handoff sections 6, 8 and 12.

Work — Implement reproducible costs, eligibility, baseline forecasts and recomputation. Publish method and coverage metadata.

Acceptance — Worked examples pass. Mid-cycle and insufficient-history cases behave as approved. Forecasts are reproducible from stored inputs.

### BE08 Process and confirm bills

Dependencies — BE03 and approved bill schema. Selected samples enable supplier-specific verification. Handoff sections 6, 9 and 12.

Work — Implement upload, extraction, editable candidates, confirmation, history and manual fallback.

Acceptance — A supported bill reaches confirmed storage after user review. Poor or unsupported input has an actionable result. No live readings are overwritten.

### BE09 Generate budget alerts and recommendations

Dependencies — BE07 and existing insight scenarios. Handoff sections 6, 8–9 and 12.

Work — Implement evidence-based rules, duplicate-alert handling and refresh after relevant settings or data changes.

Acceptance — Above-target, below-target and insufficient-data scenarios produce the agreed outcomes. Explanations match stored inputs.

### BE10 Support Ahmed’s assistant integration

Dependencies — Approved query functions. BE06–BE09 supply the relevant capabilities. Handoff sections 6, 9 and 12.

Work — Provide authorized application functions, response examples and failure handling. Collaborate on the chat endpoint and model integration.

Acceptance — Ahmed’s assistant retrieves the intended household results. Cross-account access and unavailable-data cases are exercised. Provider setup and ownership are documented.

### BE11 Verify the integrated local demonstration

Dependencies — BE03–BE10 and Miray’s implemented screens. Handoff sections 3 and 6–12.

Work — Run the full user journey, record defects, update contract examples and write the local demonstration guide.

Acceptance — A teammate reproduces the demo from a clean checkout. Scenario results match expected values. Restart preserves records. Known limits and contribution evidence are recorded.

### First frontend integration checkpoint

Connect Miray’s screen to BE03 and BE06 before waiting for every feature. Verify saved settings, a successful dashboard response, one empty or partial-data response, an authorization failure and a failed request. Continue integrating costs, bills, insights and chat as their endpoints become available.

## 12 Evaluation documentation and completion

### Required evaluation evidence

Test business calculations using manually checked examples. Test ingestion retries, period boundaries, resets and gap handling through the application interfaces. Test ownership with two accounts. Run API examples against the implemented schemas and verify that frontend displays agree with backend values. Add tests where they establish these behaviours and catch meaningful regressions.

Run normal and failure scenarios through the integrated application. Include billing-period transitions, zero usage, partial days, no history, invalid dates, missing tariffs, stale devices, negative remainders, duplicate bill confirmation and extraction failure. Record expected and actual outcomes, relevant commit, commands, and unresolved defects.

Evaluate forecasts on withheld later periods with a documented split. Ahmed evaluates the assistant on questions about usage, forecasts, missing data and unsupported inferences. Use application-level checks to confirm tool authorization and data correctness as well as the assistant’s wording.

### Sprint and GitHub records

For each task, record its issue, branch or PR, deliverable, relevant decision and contract versions, verification, reviewer feedback and remaining work. Update the sprint backlog as work changes and reflect scope changes in the product backlog. Agree board transitions with Ahmed and preserve meaningful commit history.

Capture actual contributions, including code, review, testing and integration. Keep sprint notes and user-test observations. Ahmed coordinates user testing, including the proposed Ruqaiya and Michael sessions. Record consented feedback, observed problems and resulting changes. Meeting photos can support sprint evidence where appropriate.

### Local run guide and completion package

- Document exact runtime dependencies, setup, migrations, account creation, environment variables and frontend/backend startup.

- Document simulator import and streaming commands, scenario clock, selected bill example, forecast prerequisites and expected demo results.

- Provide the API contract, decision log, test commands and results, known limitations, and the task-to-handoff mapping.

- Document how future hardware enters the existing ingestion path and how Ahmed’s forecast method can replace the baseline through the agreed interface.

### Instructions for the assisting GPT at each task

Identify the assigned issue and handoff version. Inspect current files and state what already exists. Resolve the issue’s dependencies, propose any outstanding shared decision, and implement the authorized increment. Verify through normal entry points, explain the result to Umut, and prepare a concise review summary with changed behaviour, evidence and remaining questions. Continue independent work when a specific decision awaits confirmation.

The local simulated backend is complete when the integrated journey and scenario checks pass with persistent records and documented evidence. Physical-device validation, real-household forecast performance and later platform deployment remain subsequent milestones.

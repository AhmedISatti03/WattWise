# WattWise Frontend Engineering Handoff

Version 1.0  |  26 November 2026

For Miray Pınarbaşı and her assisting GPT. Companion to WattWise Backend Handoff for Umut v1.0. Prepared for review by Muhammad Ahmed Satti, Group Lead, Software Development and AI Systems Engineering.

Complete the responsive WattWise web application for a local demonstration on a teammate’s laptop. Users must be able to configure a household, confirm a bill, inspect simulated consumption and calculated costs, understand a forecast and insights, and ask Ahmed’s assistant questions about the same household data.

### 1 How to use this handoff

Read the assigned GitHub issue, this handoff, Umut’s backend handoff v1.0 and the current repository instructions. Inspect and reuse the existing frontend foundation and Miray’s dashboard helpers. Complete a reviewable increment and demonstrate its acceptance checks. Explain choices and code changes so Miray can maintain the application.

This frontend handoff carries the same delivery scope and responsibility split as the backend handoff v1.0. FE01–FE10 identify the frontend work sequence and will be linked to GitHub issues during backlog setup. Exact shared interfaces will be designed in BE01 and confirmed with Ahmed and Miray. Product and interface proposals requiring confirmation must be recorded before the affected implementation. Routine internal choices and independent work can proceed.

### 2 Roles and delivery scope

| Person | Responsibility |
| --- | --- |
| Miray Pınarbaşı | Frontend implementation, responsive layouts, forms, data-access integration, chat presentation and frontend verification. |
| Umut Topatan | Backend APIs, authorization, storage, ingestion, synthetic simulation, costs, baseline forecasts and insight rules. |
| Muhammad Ahmed Satti | Technical coordination, coding, integration and review, conversational assistant, AI evaluation and ML improvements. |

The current delivery includes the seven core features and conversational assistant integration. The backend simulator supplies one whole-household monitor and two or three monitored appliances. Room and family management, appliance control, external assistant connectors and separate native mobile apps remain future improvements unless Ahmed adds them to an implementation task.

The first demonstration uses synthetic readings that are ingested, stored and processed by the backend. Keep their source visible. Account settings, confirmed bills and other saved records must survive backend restarts. A displayed success message must follow the corresponding successful API response.

## 3 Existing work and design review

Repository — AhmedISatti03/WattWise. At the latest check in the planning conversation, main and dev pointed to be54662. Recheck the live branches and record the commit used before implementation. Coordinate adoption of the existing work through the team’s Git workflow.

| Starting material | Required action |
| --- | --- |
| feature/task-9-frontend-foundation and PR 13 | Review and reuse the React/TypeScript application, navigation, charts, forms and responsive styles. Its technology proposal awaits Ahmed’s recorded review. |
| feature/consumption-dashboard | Inspect dashboardApi.ts, fixture JSON and domain/energy.ts. Bring useful work into the shared frontend without retaining conflicting sources of truth. |
| docs/frontend/screen-requirements.md and wireframes | Use the agreed journey and screen data requirements. Propose refinements to Ahmed with examples. |
| docs/mvp-scope.md and energy display rules | Preserve the measurement meanings and core features while applying the newer simulated delivery and assistant scope. |
| docs/product/insight-scenarios.md | Align forecasts, budget messages and recommendations with approved scenarios. |
| Existing issues 5, 6, 9, 11 and 12 | Inspect current state and deliverables before proposing overlapping tasks. Issue 3 supplies selected bill examples. |

Current account, settings, bill and consumption screens include placeholders. dashboardApi.ts returns local fixtures. Turn those interfaces into real user flows through the backend. Record what works already and what each task completes.

### Visual decisions Miray can propose

Present Ahmed with the main dashboard and mobile layout, navigation, first-time setup order, terminology and interface language proposal. Reuse the current foundation as the starting point. Resolve routine component and styling choices independently. Obtain confirmation for changes to product scope, user journeys, shared meaning or API behaviour.

Use clear, friendly language and accessible controls. Choose a consistent visual style with readable text, useful charts and prominent user actions. Keep technical simulation controls in a development or demonstration area if a control UI is needed. The backend’s documented commands can control scenarios initially.

## 4 Shared contract and data access

Use backend handoff sections 4–6 as the integration reference. Umut’s BE01 produces concrete schemas and example payloads for review. Miray must identify the fields each screen needs and check that the contract covers its normal and failure states before integration.

### Contract review checklist

- Account and household ownership, settings fields, validation errors and authentication behaviour.

- Device identity and scope, observed and received timestamps, status, current power and energy periods.

- Consumption filters, trend buckets, appliance contributions, calculated remainder and coverage.

- Tariff and charge basis, cost components, forecast eligibility, method, freshness and unavailable reasons.

- Bill upload, extraction status, provisional fields, confirmation, saved records and correction behaviour.

- Insight evidence and chat response text, supporting references, data periods and model-service errors.

Keep one shared, versioned API contract in the repository. Link it from both handoffs and implementation issues. If a missing field blocks a screen, propose the contract change with an example and coordinate with Umut and Ahmed. Avoid changing response semantics locally to hide a mismatch.

### Frontend architecture and request behaviour

Use a shared data-access layer for API calls and types. Screen components consume those functions. Define the API base URL and authentication transport with Umut. Keep credentials for model providers and server services in the backend. Handle unauthorized and expired-session responses consistently and clear household data from the interface when the session ends.

Keep approved fixtures usable for independent screen work before endpoints are ready. Make fixture mode explicit and separate from the integrated demonstration. The final local demonstration must load synthetic readings and calculated results from the running backend.

Agree refresh behaviour with Umut. Show loading, ready, empty, partial, stale and failed states where applicable. Distinguish the initial load from a failed refresh of previously loaded information. Retained values need their last-update time and stale indication. Prevent older requests from overwriting a newer selected period.

After a successful mutation, refresh or reconcile the affected backend data. A budget or tariff change may require costs, forecasts and insights to update according to the approved rules. A failed mutation must preserve the user’s editable input and explain the problem.

## 5 Accounts setup and settings

### Account access

Complete registration, sign-in, sign-out and session restoration against BE03. Provide labelled fields, understandable validation and visible pending states. Coordinate any password rules and recovery scope with the backend contract. Protect household routes in the UI and verify backend authorization with two separate accounts.

### First-time household setup

Support household name, billing period, budget, supported tariff and named devices as defined by the approved contract. Show what is saved and what remains incomplete. Offer bill upload or manual entry within the agreed journey. Extracted bill data can suggest fields only through the confirmed backend workflow.

Propose the order of setup and bill confirmation to Ahmed using the existing screen requirements. If a user can finish setup later, show the resulting missing-data states accurately. Avoid silently supplying a default tariff or interpreting missing readings as zero.

### Persistent settings

Load saved settings from the backend and save edits through its API. Display field errors near their controls and provide an overall error when appropriate. Show successful save only after confirmation. Leaving and reopening the page and restarting the services must retrieve the persisted values.

Explain tariff effective-date and recalculation behaviour using the approved backend rules. Keep monetary amounts, currency, cycle boundaries and units visible. Show the same billing period on budget comparisons and forecasts. Locale and display precision should be consistent with the agreed contract.

### Device association and status

Display the household monitor, named appliance plugs and collector where supplied. Show their identity, measurement scope and latest reading or contact time. A device reading can be stale while a webpage request succeeds. A failed webpage request alone cannot establish that a physical device is offline.

Umut supplies connectivity and freshness decisions. Show his status and reason fields consistently across dashboard and device screens. Provide a useful next action or explanation without inventing a diagnosis. Appliance switching requires a separately assigned control feature.

## 6 Dashboard and consumption detail

### Overview behaviour

Show current household power in W, today’s energy in kWh, estimated cycle spending, bill forecast and budget position where available. Include source labels, time periods and a last-update indication. Use backend values and eligibility states. Distinguish estimated energy charges from a bill estimate that includes the supported invoice components.

Offer daily and weekly trends with working period selection. Changing the period must request or select the matching approved response and update the relevant chart, totals and contribution display. Ensure labels expose partial days and missing intervals. Keep unrelated billing-cycle cards clearly identified when the consumption chart uses a different period.

### Contributions and remainder

The household total already includes appliance consumption. Show monitored appliances as contributions within it. Display the backend-calculated other-consumption remainder over the same interval. Explain unavailable percentages or remainders when coverage is inadequate. Keep household values visible when they remain valid despite a missing plug.

Use the common synthetic example for verification. Household energy is 12 kWh, monitored appliances use 4, 1 and 2 kWh, and the valid remainder is 5 kWh. Those appliance values must never increase the household total to 19 kWh. Under an illustrative flat TRY 3/kWh tariff, the 12 kWh energy charge is TRY 36.

### Consumption detail and chart access

Allow the user to inspect household and individual appliance trends through the approved filters. Show meaningful legends, axes, units and dates. Represent missing points explicitly and expose the values in an accessible table or equivalent text view. Use more than colour to communicate status or series identity.

### Forecasts and budget position

Display the baseline method information, calculation time, history and limitations supplied by BE07. For insufficient history, show the eligibility reason and any history progress supplied by the backend. An early forecast label and maturity rules come from the approved design.

A forecast and budget must share the same household, period and charge basis. With an eligible TRY 900 forecast against a TRY 800 target, show TRY 100 projected overspend. With a stale or unavailable forecast, follow the contract’s budget-message rules. Historical bill consumption remains separate from live or simulated monitoring.

## 7 Bills alerts and recommendations

### Bill upload and review

Complete the file picker and upload request for one chosen supplier format. A supplier and permitted sample bills still need selecting with Ahmed. Support manual entry while sample selection and supplier extraction proceed. Show supported types and limits from the agreed backend contract.

Show upload and extraction progress, success, missing fields and failure. Keep extracted candidates editable and visibly provisional. Validate on the client for immediate feedback and display authoritative server validation. Require an explicit confirmation action before a bill becomes a confirmed record.

On confirmation, show the saved record and refresh the bill list. Handle repeat clicks, pending confirmation and a failed response according to the backend’s duplicate and retry rules. Keep readable feedback for unsupported files, unreadable images, scanned PDFs, empty extraction and service failure. Preserve user corrections where possible.

Treat bill-based tariff or setup suggestions as information to review under the approved workflow. Confirmed historical bills must remain distinguishable from monitoring data. Coordinate correction, deletion and original-upload retention behaviour with Umut before exposing related actions.

### Budget alerts and insight detail

Present the forecast, target, cycle and projected difference behind an alert. Show monitored-appliance attribution only when the backend provides matching evidence. If acknowledgement or dismissal is included in the approved contract, persist that action through the API and handle failure.

Provide an insight detail view explaining the rule, supporting usage or tariff values, relevant period, limitations and suggested action. Keep cheaper-hour suggestions tied to a supporting tariff. A missing-data explanation should identify what prevents a useful recommendation.

### State consistency

Dashboard summaries, bills, settings and insights must agree after a mutation or refresh. Use shared request functions and explicit refresh handling. A demonstration should show the consequence of changing a budget, confirming a bill and receiving additional simulated readings, following the backend’s approved recalculation rules.

## 8 Conversational assistant and responsive use

### Chat experience

Miray owns chat presentation. Ahmed owns model integration, prompts, tool use and AI evaluation. Umut supplies the authorized services and agreed chat endpoint. Coordinate the request and response shape with both before connecting the interface.

Provide a message field, submit control, pending state, answer display and recoverable error. Preserve the user’s message when a request fails and prevent accidental duplicate submissions. Implement streaming only if the team agrees a streaming contract. Confirm history persistence and any conversation reset behaviour with Ahmed and Umut.

Show supporting period and data references returned with the answer, with navigation to existing consumption, forecast or insight views where meaningful. Carry synthetic-data labels into the assistant experience. Distinguish a response that lacks sufficient household data from a model-provider failure.

An example demonstration question is “Why is my bill forecast higher this week?” The answer must come through Ahmed’s assistant using backend results. Display missing information or limitations as returned. Model-service failure should leave the rest of the application usable.

### Responsive and accessible behaviour

Complete the responsive web application for desktop and phone. Reuse existing navigation where suitable. Verify long names and translated or expanded labels, readable forms, charts, bill review and chat without horizontal page overflow. Record actual browser and viewport checks.

Use semantic controls, visible keyboard focus, associated form labels and errors, sufficient contrast and accessible status announcements. Verify keyboard navigation, focus after route changes and form errors, and meaningful chart alternatives. Keep loading and error states usable at narrow widths.

### Local demonstration setup

Document frontend and backend startup, API configuration, account credentials for generated demo accounts, chosen bill example and scenario commands. On the same laptop use the configured local service URLs. If demonstrating from a phone, document the laptop address and coordinate permitted origins, API reachability and authentication with Umut.

The first release runs locally. Future hosted web and mobile clients can use the shared backend contract. Build the current responsive web scope around that interface and record deployment assumptions for later work.

## 9 Prioritized frontend tasks

Map these proposals to existing issues during backlog setup. Reuse the backend task references exactly as defined in Umut’s v1.0 handoff. Independent UI work can use clearly labelled fixtures while the relevant backend endpoint is being implemented.

### FE01 Review existing work and agree screen needs

Dependencies — Backend BE01 and this handoff sections 2–4.

Work — Inspect branches and screen requirements, identify reusable components, propose journey refinements, and review API examples with Umut and Ahmed.

Acceptance — Record agreed tooling, unresolved product decisions and the shared contract reference. Each screen has required data and failure states.

### FE02 Integrate the frontend foundation

Dependencies — FE01 and Ahmed’s tooling decision. Sections 3–4 and 8.

Work — Bring the foundation and useful dashboard helpers into one application. Complete navigation, API configuration and the shared data-access layer.

Acceptance — A teammate can install and run it. Direct routes and navigation work. Fixture mode is explicit and one backend request succeeds.

### FE03 Complete accounts and household setup

Dependencies — FE02 and BE03 for integrated completion. Sections 4–5.

Work — Connect account/session flows, household setup and persistent settings, including validation and save/reload behaviour.

Acceptance — A user signs in, saves a household and reloads it. Session expiry is handled. Two users see their own household information.

### FE04 Complete dashboard and consumption views

Dependencies — FE02, shared contract and BE06 for integrated completion. Sections 4 and 6.

Work — Connect power, energy, trends, working period selection, appliance contributions, remainder and quality displays.

Acceptance — Backend examples match screen values. Changes of period and rapid changes remain consistent. Empty, partial and failed requests display correctly.

### FE05 Complete device status views

Dependencies — FE03–FE04 and BE06. Sections 4–6.

Work — Show household monitor, plugs and collector using backend status and freshness fields. Keep related dashboard information consistent.

Acceptance — Disconnected plug, collector delay and request error remain distinguishable. Valid household readings remain visible when supported.

### FE06 Display costs forecasts and budgets

Dependencies — FE03–FE04 and BE07. Sections 5–6.

Work — Connect costs, charge basis, forecast metadata, budget position and refresh after settings changes.

Acceptance — Worked values agree with backend outputs. Insufficient history and incomplete billing cycles follow the contract. Budget changes update the result.

## 10 Frontend tasks continued and verification

### FE07 Complete bill upload and confirmation

Dependencies — FE03 and BE08. Sections 4–5 and 7.

Work — Implement upload, extraction status, editable review, explicit confirmation, saved history and manual entry.

Acceptance — The selected supported bill can be corrected and saved. Retry, duplicate confirmation, invalid files and extraction failure behave as agreed.

### FE08 Complete alerts and recommendation views

Dependencies — FE06 and BE09. Sections 6–7.

Work — Connect budget alerts, supporting evidence and insight detail, including any approved acknowledgement action.

Acceptance — Above-budget, below-budget and insufficient-data scenarios match backend rules and use the correct periods and labels.

### FE09 Connect Ahmed’s assistant

Dependencies — FE02, agreed chat contract, BE10 and Ahmed’s assistant implementation. Sections 4 and 8.

Work — Implement chat input, request handling, answer references, pending and error states, and agreed conversation behaviour.

Acceptance — A question is answered from authorized backend results. Insufficient information and provider failure are understandable. Dashboard use continues during a chat failure.

### FE10 Verify the complete local user journey

Dependencies — FE03–FE09 and the backend capabilities from BE03–BE10. Coordinate verification jointly with BE11. Sections 5–8 and 10.

Work — Run the integrated journey on desktop and phone layouts, resolve defects and prepare repeatable setup and demonstration instructions.

Acceptance — A teammate reproduces the demonstration from a clean checkout. Persistence, scenario changes, accessibility checks and contribution records have evidence.

### Integration checkpoints

First connect saved settings and the consumption dashboard through BE03 and BE06. Verify one successful response, one partial or empty result, an authorization failure and a failed request. Add costs, bills, insights and chat as their capabilities become available. Identify exact integration blockers and continue unrelated screen work.

### Evidence required for review

For each issue, record branch or commit, handoff and contract versions, changed user behaviour, commands run, browser/viewport checks, and unresolved defects. Capture screenshots only when they help demonstrate a result. Include frontend type-check and production build results and tests that establish meaningful behaviour.

Verify empty readings, partial days, missing tariffs, insufficient history, disconnected devices, stale results, rapid period changes, invalid dates, failed saves, unreadable bills and model-service errors. Check persistence after refresh and restart, and clear displayed household records on sign-out. Compare displayed values with the matching backend response.

Coordinate user testing with Ahmed, including the proposed Ruqaiya and Michael sessions. Record observations and feedback, revise the sprint backlog and reflect scope changes in the product backlog. Document actual coding, review, testing and integration contributions for the presentation.

The assisting GPT should inspect the current task and files, identify dependencies, propose outstanding shared decisions, implement the authorized increment, verify the result through its normal user flow and explain the change to Miray. Update the issue evidence and contract references so a fresh GPT session can continue from the recorded state.

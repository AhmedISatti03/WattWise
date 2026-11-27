# WattWise frontend–backend contract proposal

**Version:** `0.1-draft` · **Prepared:** 27 November 2026  
**Status:** Proposed for Ahmed and Miray's review; no shared-interface approval is claimed.  
**Tasks:** #11, #14 (BE01); demo samples support #12.  
**Source handoffs:** [Backend v1.0](../handoffs/WattWise_Backend_Handoff_Umut_v1.0.md), [Frontend v1.0](../handoffs/WattWise_Frontend_Handoff_Miray_v1.0.md).

This draft is a concrete review target, not a promise that the proposed production routes are implemented. The separately named development sample routes may be served now without making account, reading-storage, or calculation acceptance claims. Product and shared-interface decisions remain subject to the handoffs' review requirements.

## 1. Existing material and compatibility

Inspected `main` at `261fcb430297c3aa44ecb15e9ddc9db10a61f247`, frontend foundation at `c569e6b3b3d6649eef7cc7c1b7064a804f2eec76`, and consumption-dashboard at `2bc57fab0460c6a6cac46064838b61f7da5b706f`.

Miray's `dashboardApi.ts` exports `getDashboard(scenario)` and returns four local JSON fixtures. Preserve its useful keys: `meta`, `billingCycle`, `currentPower`, `todayEnergy`, `contributions`, `devices`, and per-value `value`, `unit`, `classification`, `unavailableReason`. The foundation currently reads `sample.ts` directly; adopting a shared request module is Miray's #20 work. Do not claim the existing pages call this backend.

Intentional proposed changes to review together:

- Normalize `todayEnergy.period.end` to **`endExclusive`**, matching other intervals. This is an explicit contract change, not a silent rename.
- Add `contractVersion`, `contractStatus`, `sourceType`, `asOf`, `requestId`, and `scenario` to sample `meta`.
- Add measured/received times, coverage, explanations, shares and separate collector status. Add typed trend, cost, forecast, budget and budget-position groups to the dashboard sample.
- The collector's snake_case event format is retained at its boundary. A backend adapter maps it into camelCase response models; the server resolves device scope/ownership from registration rather than trusting event claims.
- Existing helper calculations may format or preview agreed examples. Authoritative comparison, remainder, cost, forecast, coverage and freshness results belong to the backend.

## 2. Common rules

### Identifiers, ownership and authentication proposal

Use opaque string identifiers (`userId`, `householdId`, `deviceId`, `collectorId`, `billId`). Real records use generated IDs, not names or IP addresses. The sample names in these documents are fixtures, not production IDs.

Recommended browser transport: an opaque server-side session carried by an HttpOnly cookie, `SameSite=Lax`, secure cookies in HTTPS deployment, with explicit local-development configuration. A CSRF token is required on state-changing browser requests. Passwords are hashed using a maintained password-hashing library; never logged or returned. Session expiry, token issuance, cookie names and password policy require Ahmed's confirmation before implementation.

Collector requests instead use a revocable `Authorization: Bearer <collector-token>` credential bound to registered devices and one household. No model-provider key or collector secret is sent to the browser. Every household/device query and mutation checks server-side ownership. A requested household ID alone grants nothing. Return 404 for another account's object to avoid disclosing its existence. Missing/expired session returns 401.

Propose a local frontend origin allowlist containing exactly configured trusted origins (initially `http://localhost:5173`), not a credentials-enabled wildcard. The integrated browser request module uses `credentials: "include"` if the session proposal is approved. Phone/laptop origin additions require coordinated CORS/cookie configuration.

### Time, source and values

- RFC3339 timestamps include an offset; storage normalizes absolute instants to UTC. Group calendar days in household timezone `Europe/Istanbul` for the pilot.
- Every interval includes `start` and excludes `endExclusive`. Display `lastIncludedDate` where useful for bill cycles, without changing the interval boundary.
- `meta.asOf` is the reading/calculation snapshot clock. `generatedAt` is response generation time; it is not proof that every measurement is fresh. Fixture timestamps are deliberately fixed. At HTTP delivery, `meta.requestId` is replaced with the actual request correlation UUID and matches the `X-Request-ID` header; the example request IDs are illustrative only.
- A simulator must use one documented scenario clock for generation, aggregation and freshness; do not compare an October synthetic reading to the actual November wall clock and call it offline.
- `sourceType` is `synthetic`, `physical_device`, or `historical_bill`; preserve provenance per measurement/evidence when a response draws from multiple sources. `sample: true` and `sampleLabel` are mandatory for every synthetic example.
- Power is W; active energy is kWh; currency is TRY. JSON numbers remain unrounded for calculations, while UI energy/money display has two decimals. Decimal arithmetic is recommended for monetary calculations; rounding policy requires review.
- `value: null` means unavailable, with a non-null stable reason and human explanation. `0` is valid known zero, never an absent-data substitute. `[]` is a successful empty list, not an HTTP error. Pending calculations have a separate status, not an invented numeric estimate.
- `coverage.status` is `complete`, `partial`, `none`, or `uncertain`; `gaps` identifies known missing intervals. A partial current day can have complete coverage of the elapsed portion. Completeness does not imply a complete calendar day.
- Communication gaps and genuinely missing energy are separate. Supported cumulative-counter deltas may establish interval energy without establishing an hourly profile. Never invent chart detail through a gap.
- Current power includes `observedAt`, `receivedAt`, status and reason; stale readings become last-recorded values. Device, collector and HTTP-request status remain distinct.

### Error envelope

```json
{
  "meta": {"contractVersion":"0.1-draft","requestId":"request-id"},
  "error": {
    "code":"validation_error",
    "message":"Some fields need correction.",
    "fieldErrors":[{"path":"budget.value","code":"must_be_positive","message":"Enter a budget greater than zero."}],
    "retryable":false,
    "retryAfterSeconds":null
  }
}
```

Production metadata is not required to carry the public sample schema's `sample: true`; the schema in this draft explicitly validates **sample responses**, not real data. API errors never return database paths, raw traces, password input or token values.

| HTTP | Meaning |
|---|---|
| 200/201/202/204 | Successful retrieval or mutation, creation, pending job, or successful empty body, respectively. |
| 400 | Malformed request envelope or invalid JSON. |
| 401 | Missing or expired session/collector credential. |
| 403 | Valid identity but disallowed operation or failed CSRF validation. |
| 404 | Unknown or unowned object. |
| 409 | Idempotency conflict, duplicate bill or stale settings revision. |
| 413/415 | Upload too large/unsupported validated file type. |
| 422 | Field validation with `fieldErrors`. |
| 429 | Retryable throttling; honor `Retry-After`. |
| 503 | Temporary service/provider unavailability. |

A successful household query with insufficient forecast history returns 200 with `forecast.eligible=false`, `value=null`, reason and explanation. It does not turn the entire dashboard into a 503.

## 3. Endpoint proposal and ownership

All paths below start `/api/v1`. **Only health/configuration infrastructure and the explicitly enabled public demo routes are in the current scaffold's implementation scope.** Production routes are specifications awaiting review.

| Method/path | Request | Result | Work |
|---|---|---|---|
| `POST /accounts` | `{email,password}` | 201 `{user:{userId,email},householdId:null}`; does not silently sign in | #16 / BE03 |
| `POST /sessions` | `{email,password}` | 200 `{user,householdId,expiresAt,csrfToken}` + session cookie | #16 |
| `GET /session` | Session cookie | Current identity/session or 401 | #16 |
| `DELETE /session` | Cookie + CSRF | 204, revoke session and expire cookie | #16 |
| `POST /households` | HouseholdCreate below | 201 Household; one household/account | #16 |
| `GET /households/{id}` | Owned ID | Household | #16 |
| `PATCH /households/{id}` | Changed settings + `revision` | Updated Household; 409 for stale revision | #16 |
| `POST /households/{id}/devices` | `{name,scope,sourceType,model,collectorId}` | 201 Device; register collector separately with owned credentials | #17 |
| `GET /households/{id}/devices` | Owned ID | `{meta,devices,collector}` | #17 / BE06 |
| `POST /households/{id}/collectors` | `{name,sourceType}` | 201 registration + one-time token; token absent from later GETs | #17 |
| `POST /collector/readings/batch` | Collector batch below | Per-event results after commit | #17 |
| `GET /households/{id}/readings` | `deviceId,start,endExclusive,limit,cursor` | `{meta,items,nextCursor}` | #17 |
| `GET /households/{id}/overview` | Explicit `start,endExclusive,resolution`; optional `deviceId` for detail | Dashboard groups; chart/contribution period explicit, billing groups separate | #11 / BE06 |
| `GET /households/{id}/consumption` | Same filters | `{meta,period,trend,contributions,coverage}` | BE06 |
| `GET /households/{id}/costs` | `start,endExclusive` | Cost groups/charge basis and exclusions | BE07 |
| `GET /households/{id}/forecast` | `cycleStart,cycleEndExclusive` | Forecast + same-basis budget position | BE07 |
| `POST /households/{id}/bill-uploads` | Multipart `file`, idempotency key | 202 `{uploadId,status:"queued",extractionId}` | BE08 |
| `GET /households/{id}/bill-uploads/{uploadId}` | Owned upload ID | Extraction state, candidates, explanations | BE08 |
| `POST /households/{id}/bills` | ConfirmedBillCreate below, `Idempotency-Key` | 201 historical record; explicit user confirmation required | BE08 |
| `GET /households/{id}/bills` | `limit,cursor` | `{meta,items,nextCursor}` | BE08 |
| `GET /households/{id}/bills/{billId}` | Owned bill ID | Confirmed historical record | BE08 |
| `GET /households/{id}/insights` | `cycleStart,cycleEndExclusive` | `{meta,items,unavailableReasons}` | BE09 |
| `GET /households/{id}/insights/{insightId}` | Owned insight ID | Evidence and currentness | BE09 |
| `POST /households/{id}/chat/messages` | `{message,clientMessageId}` + optional agreed conversation ID | Answer/evidence or typed assistant failure | BE10 + Ahmed |

Settings mutations resolve actual owner from session. A future implementation should not add GET endpoints that accept arbitrary user IDs and return their data. Limits proposal: default page size 100, maximum 1000 readings, cursor `(observedAt,eventId)` with stable ordering; exact maximum and inclusive continuation behavior need confirmation. Consumption maximum period proposal 31 days for hourly buckets and 366 days for daily; invalid or reversed periods return 422. Chart selection never changes the configured bill cycle.

### HouseholdCreate / Household

```json
{
  "name":"Sample home",
  "timezone":"Europe/Istanbul",
  "billingCycle":{"start":"2026-10-18T00:00:00+03:00","endExclusive":"2026-11-17T00:00:00+03:00"},
  "budget":{"value":800,"unit":"TRY","chargeBasis":"energy_only"},
  "tariff":{"kind":"fictional_flat_energy","currency":"TRY","ratePerKwh":3,"effectiveFrom":"2026-10-18T00:00:00+03:00","effectiveUntilExclusive":null,"source":"synthetic","includedComponents":["energy"],"excludedComponents":["other_invoice_charges"]}
}
```

Response adds `householdId`, `ownerUserId` if required by the UI, `revision`, timestamps, and `setupCompleteness`. Budget/tariff can be null if incomplete setup is approved; dependent outputs then give explicit reasons. Propose positive budget, nonnegative rate, valid IANA timezone and ordered timezone-aware cycle boundaries. This synthetic tariff is **not a validated Turkish supplier tariff**. Real tariff type, effective-date editing and historical recalculation must be confirmed before #16 final acceptance.

## 4. Collector batch and measurement proposal

Retain the collector plan's `/collector/readings/batch` path and its existing event naming:

```json
{
  "schema_version":1,
  "events":[{
    "event_id":"event-001",
    "collector_id":"registered-collector-id",
    "device_id":"registered-household-monitor-id",
    "measurement_scope":"household",
    "source_kind":"simulated",
    "sample_run_id":"seed-42-normal",
    "device_measured_at":"2026-10-28T14:30:00+03:00",
    "collected_at":"2026-10-28T14:30:00+03:00",
    "timestamp_basis":"device_measurement",
    "power_w":820,
    "energy_import_total_kwh":123.456,
    "counter_epoch":0,
    "quality_flags":[]
  }]
}
```

Response proposal: 200 `{meta, results:[{eventId,status,code,message}]}`, `status` one of `accepted`, `already_stored`, `rejected`. ACK only after durable commit. Reject an invalid envelope with 400/422; for a valid batch validate individual events and commit accepted events transactionally with their outcomes. Full batch authorization failure returns 401/403 and accepts nothing. The partial-acceptance policy requires review before #17 implementation.

Important invariants:

1. Authenticated credential determines collector/household/device membership. If `collector_id`, source or scope disagrees with registration, reject the event. Never use submitted household ownership as authorization.
2. Unique key `(registered collector ID, event_id)`; exact same immutable payload returns `already_stored`. Same key/different payload returns `rejected` with `event_conflict`, never overwrites an accepted reading. Non-event mutations use `Idempotency-Key` scoped to owner + route + payload hash; same key/different input returns 409.
3. Cumulative imported active energy is a counter, not energy for one poll. Adjacent valid counters in the same segment establish a delta over `[previous observed time,current observed time)`. Compare same intervals and units. First counter in a segment establishes a baseline; it is not consumed energy by itself.
4. A lower counter must not create a negative delta. Explicit device/epoch change or a validated reset starts a new segment. Ambiguous reset/rollover is flagged and coverage withheld pending evidence. Counter epoch alone is not proof that arbitrary collector-supplied resets are correct.
5. Late arrivals are stored immutably and re-evaluated in event-time order within a documented recalculation window. They must not move last-observed device freshness backward. Equal device/epoch/observed time with conflicting measurements is a recorded conflict, not two readings to add. Recalculation limits need confirmation.
6. Reject non-finite/negative import counters, invalid units/types/timezone-naive times and unknown devices. Quarantine implausible readings rather than silently zeroing them. Exact physical plausibility/current limits are model-specific and remain pending, not guessed globally.
7. Add authoritative `received_at` on first acceptance. Preserve original `collected_at`/device times on retries. Retrieval maps these to `receivedAt`, `observedAt` plus timestamp basis.
8. A valid delta spanning a delivery gap can recover interval energy, but cannot manufacture hourly detail. Thresholds for stale power (collector plan suggests 30 s) and collector-unreachable (180 s) use the scenario clock in synthetic runs and require review.

Propose a 100-event batch default and a documented maximum of 1000, preserving event timestamps on replay. Larger historical imports split batches. Approval is needed for precise limits, late-arrival window and coverage allocation policy.

## 5. Consumption, device and forecast responses

Concrete versioned sample payloads are in [examples/v0.1](examples/v0.1/). The [JSON Schema](dashboard-response.schema.json) validates the draft **synthetic fixture edition**. Structural validation alone cannot prove arithmetic, matching periods, auth or aggregation correctness.

| Example | HTTP for demo overview | Meaning |
|---|---|---|
| [normal](examples/v0.1/normal.json) | 200 | 820 W; 8.40 kWh partial current day; complete prior-day household 12 kWh; appliances 4+1+2 within total; remainder 5. |
| [empty](examples/v0.1/empty.json) | 200 | Null measurements with reasons, no trend buckets, no eligible forecast; known budget remains. |
| [partial-data](examples/v0.1/partial-data.json) | 200 | Genuine current-day household energy gap; known recorded portion/cost remain labelled partial; full-cycle forecast withheld. |
| [device-disconnected](examples/v0.1/device-disconnected.json) | 200 | Fridge interval unavailable and stale status; household values remain; remainder unavailable. |
| [error](examples/v0.1/error.json) | 503 | Failed request. It does not claim that any physical device is offline. |

`devices` response is a projection `{meta,devices,collector}` of the same scenario. `lastReadingAt` is observed time, `lastReceivedAt` first backend receipt. Collector `lastContactAt` and pending queue count each have their own observation time; cached queue count is not a live local fact during an internet outage.

Trend buckets: `start`, `endExclusive`, `value` in kWh, `partialBucket`, `coverage`. No readings yields null bucket values or an explicitly empty series; valid zero remains zero. No linear filling of missing buckets is proposed. Calculate other consumption only when the same interval, same basis and sufficient household/appliance coverage support subtraction; negative remainder gets `invalid_remainder` with null, not zero. Missing a plug does not invalidate independently valid household energy. Contribution percentages need a positive valid denominator.

### Initial cost and forecast proposal

The normal sample has recorded cycle energy 108.40 kWh at 14:30 and energy-only cost `108.4×3=325.20 TRY`. Its forecast is deliberately **dated 00:00**, when 100 kWh was observed over ten complete days and 20 days remained. Seven complete recent days total 70 kWh: `100 + (70/7×20) = 300 kWh`; `300×3=900 TRY`. Same-cycle/basis target 800 gives forecast difference 100 TRY. These are synthetic arithmetic checks, not invoice forecasts or accuracy evidence.

Forecast fields include `methodId`, `methodVersion`, `eligible`, `calculatedAt`, `asOf`, cycle/history/projected periods, `validDays`, `minimumValidDays`, observed/projected energy, assumptions, `maturity`, `isStale`, and unavailable reason. Budget position references the exact forecast calculation time. Future ML methods keep these fields and add method-specific metadata separately.

Propose retaining the existing minimum seven complete valid days and withholding full-cycle forecasts if elapsed-cycle energy is genuinely incomplete. No prediction from earlier unobserved cycle data is silently invented. Recompute after valid readings, tariff/budget edits or late-arrival coverage changes; pending/invalid results must suppress stale budget conclusions. Intraday extrapolation, freshness deadline, revision history and early-estimate exit conditions remain product decisions. The sample's accepted dated forecast is illustrative, not approval of a specific freshness deadline.

## 6. Bills, insights and assistant contracts to review

### Bill workflow

Proposed extraction status response:

```json
{
  "uploadId":"upload-001","status":"needs_review","extractionId":"extract-001",
  "sourceType":"synthetic","supplierFormat":"pending-selection",
  "candidates":[{"path":"consumptionKwh","value":120,"origin":"extracted","needsReview":true,"reason":"check_against_bill"}],
  "missingFields":["billingCycle.endExclusive"],"errors":[]
}
```

`status` is `queued`, `processing`, `needs_review`, `failed` or `confirmed`; extraction never implies confirmation. `ConfirmedBillCreate` proposes `{uploadId:null|id, billingCycle:{start,endExclusive}, consumptionKwh, invoiceTotal:{value,unit:"TRY"}, supplier, tariffDescription:null|string, confirmedByUser:true}`. Manual entry has null upload ID and `origin:"manual"`; responses add `billId`, `confirmedAt`, `classification:"historical_bill"`, provenance and immutable confirmation revision.

Do not derive a marginal unit rate from invoice total divided by kWh. Bills do not add to overlapping monitor totals or silently update tariff settings. Candidate tariff suggestions need a separate accepted settings mutation. Supplier layout, required fields, upload byte/type limits, actual OCR choice, preview access, duplicate criteria, corrections/deletion and original-file retention require review and permitted samples under #3. Proposed 10 MiB PDF/JPEG/PNG limit is an initial option, not adopted capability. Validate content signature and decoded content in addition to extension/MIME in implementation.

### Insights

Each proposed `Insight` has `{insightId,type,ruleId,ruleVersion,status,generatedAt,householdId,period,sourceType,title,message,evidence,limitations,action}`. Evidence refers to stable metric/source IDs and calculation versions, with values, units, periods and provenance. `status` is `active`, `resolved`, or `unavailable`; record reasons for unsupported conclusions.

Already-incurred cost beyond target takes precedence over forecast overspend. A fresh eligible same-period same-basis forecast supports on-track/at-target/forecast-over; unavailable or stale forecasts do not. Unchanged refreshes do not create duplicate alerts. Proposed alert identity is `(household,cycle,rule,activation episode)`; resolution/re-entry and acknowledgement API remain unapproved. No write endpoint for dismissal is proposed until that policy is agreed. Flat tariffs suppress cheaper-hour advice. No unmonitored appliance attribution, fault claim or guaranteed saving.

### Assistant support and ownership boundary

Propose read-only server functions: `get_household_summary(period)`, `get_consumption_trend(period,resolution,device_id?)`, `get_device_status()`, `get_billing_context(cycle)`, `get_forecast(cycle)`, `get_insight_evidence(insight_id)`. Function execution binds the authenticated household independently of model-supplied arguments. The model cannot select an arbitrary owner, execute raw SQL, call unauthenticated endpoints or perform appliance actions.

Proposed non-streaming chat response: `{messageId,conversationId:null|string,status:"answered"|"insufficient_data",answerText,references:[{kind,id,period,sourceType,asOf}],limitations:[]}`. Service/provider failure uses the common 503 envelope, while other dashboard functions stay available. `clientMessageId` deduplicates submit retries within an authorized account. Conversation persistence, message limits and streaming require agreement. Ahmed selects model/provider and owns prompts, orchestration and evaluation (#24–#28); no credentials, fabricated answers or model calls are included in this scaffold.

## 7. Public development mock: implemented boundary

The scaffold may serve:

- `GET /api/v1/demo/overview?scenario=normal` — complete fixture.
- `GET /api/v1/demo/devices?scenario=normal` — matching device/collector projection.
- Scenario enum: `normal`, `empty`, `partial-data`, `device-disconnected`, `error`.
- Optional `delay_ms` integer 0–2000 models loading; it is transport behavior, not a new data state. Invalid scenario/delay yields documented validation failure.
- `error` returns the error fixture with HTTP 503 and proposed retry guidance. No database/private household reads or writes occur in demo routes.

These endpoints are **disabled by default** and require `WATTWISE_ENABLE_DEMO_API=true`. They are unauthenticated because every result is public synthetic development data. They must not be used as authorization examples, enabled on a real-data deployment by accident, or called evidence for reading ingestion. Fixture files are frozen snapshots; they do not create stored readings. Normal production endpoints will not accept an arbitrary `scenario` query parameter.

The real integrated demo must generate data and submit it through ingestion, persist it, and return computed consumption. Mock HTTP delivery completes only a reviewable #12 increment, not #17/#18 or the final handoff.

## 8. Screen-to-capability coverage

| Screens | API/data path | Critical failure states |
|---|---|---|
| Account access | accounts/session | Validation, rejected credential, expired session, failed request |
| Setup/settings | household/revision/tariff/budget | Incomplete setup, invalid dates, failed save preserving input, stale revision |
| Overview/usage | overview/consumption/cost/forecast | No readings, partial period, valid zero, missing tariff/history, delayed result |
| Devices | device/collector projection | Plug stale vs collector offline vs request error; valid household total preserved |
| Bills/review | upload status/candidates/confirmed records | Pending, extraction failure, uncertain field, duplicate confirmation, manual fallback |
| Insights | evidence/active state | Missing evidence, obsolete forecast, resolved insight |
| Chat | Ahmed's authorized application functions + chat result | Insufficient data, unsupported request, provider failure, expired session |

Frontend request modules must cancel or ignore superseded period requests. Cache keys include household, period, resolution and contract version; clear household caches at sign-out. Successful settings mutations refresh dependent outputs only after server confirmation; old forecasts cannot be combined with newly edited budgets without a revision/currency/period/basis check.

## 9. Review and unresolved choices

Review together with the [backend proposal](../backend/design-proposal.md) and [decision log](../backend/decision-log.md) when available. Expected review questions:

1. Approve or revise session-cookie + CSRF transport, password/session policy, allowed origins and household creation behavior.
2. Confirm camelCase response extension, the explicit `end` → `endExclusive` normalization, snake_case collector adapter and example schema.
3. Confirm reading idempotency/partial batch outcomes, late-arrival window, reset evidence and coverage allocation.
4. Confirm forecast baseline, intraday rule, freshness/maturity, tariff effective dates/rounding and budget charge basis.
5. Select supplier samples/OCR, upload/retention rules, duplicate confirmation/correction behavior.
6. Confirm assistant function and chat schema with Ahmed/Miray; conversation storage remains separate.

The examples and paths are versioned proposals. No production endpoint or product rule becomes approved because it appears in a working mock. Record decisions and update both consumers before changing meanings.

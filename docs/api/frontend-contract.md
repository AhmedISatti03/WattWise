# WattWise frontend–backend contract proposal

**Version:** `0.1-draft` · **Updated:** 28 November 2026

**Status:** Ahmed approved the dashboard direction and core design. Exact shared fields and proposed production behaviour remain open for review with Ahmed and Miray.

**Tasks:** #11 and #12 review updates, #30 implementation decisions for #16–18.

**Source handoffs:** [Backend v1.0](../handoffs/WattWise_Backend_Handoff_Umut_v1.0.md), [Frontend v1.0](../handoffs/WattWise_Frontend_Handoff_Miray_v1.0.md).

The [design review](https://github.com/AhmedISatti03/WattWise/blob/6b3cae4/docs/backend/ahmed-review-response-v1.md) records D01–D14 and their qualifications. The [#11 review](https://github.com/AhmedISatti03/WattWise/issues/11#issuecomment-7231387740) records the agreed dashboard behaviour. Section 7 lists the implemented mock routes.

## 1. Existing material and compatibility

Inspected `main` at `261fcb430297c3aa44ecb15e9ddc9db10a61f247`, frontend foundation at `c569e6b3b3d6649eef7cc7c1b7064a804f2eec76`, and consumption-dashboard at `2bc57fab0460c6a6cac46064838b61f7da5b706f`.

Miray's `dashboardApi.ts` exports `getDashboard(scenario)` and returns four local JSON fixtures. Preserve its useful keys: `meta`, `billingCycle`, `currentPower`, `todayEnergy`, `contributions`, `devices`, and per-value `value`, `unit`, `classification`, `unavailableReason`. The foundation currently reads `sample.ts` directly; adopting a shared request module is Miray's #20 work. Do not claim the existing pages call this backend.

Agreed compatibility direction:

- Normalize `todayEnergy.period.end` to **`endExclusive`**, matching other intervals. This is an explicit contract change, not a silent rename.
- Add `contractVersion`, `contractStatus`, `sourceType`, `asOf`, `requestId`, and `scenario` to sample `meta`.
- Add measured/received times, coverage, explanations, shares and separate collector status. Add typed trend, cost, forecast, budget and budget-position groups to the dashboard sample.
- The collector's snake_case event format is retained at its boundary. A backend adapter maps it into camelCase response models; the server resolves device scope/ownership from registration rather than trusting event claims.
- Existing helper calculations may format or preview agreed examples. Authoritative comparison, remainder, cost, forecast, coverage and freshness results belong to the backend.

## 2. Common rules

### Identifiers, ownership and authentication

Use opaque string identifiers (`userId`, `householdId`, `deviceId`, `collectorId`, `billId`). Real records use generated IDs, not names or IP addresses. The sample names in these documents are fixtures, not production IDs.

Approved direction uses an opaque server-side session, an HttpOnly `SameSite=Lax` cookie and CSRF protection for browser mutations. The [#16 decision recommendations](../backend/decision-log.md) specify the proposed expiry, cookie configuration, CSRF, password and recovery rules for Ahmed to confirm.

Collector requests instead use a revocable `Authorization: Bearer <collector-token>` credential bound to registered devices and one household. No model-provider key or collector secret is sent to the browser. Every household/device query and mutation checks server-side ownership. A requested household ID alone grants nothing. Return 404 for another account's object to avoid disclosing its existence. Missing/expired session returns 401.

For the proposed browser integration, configure an exact trusted frontend origin and send `credentials: "include"`. Use the same hostname on both ends in HTTP loopback development, for example `localhost` on ports 5173 and 8100. Other origins require coordinated CORS and cookie configuration.

### Time, source and values

- RFC3339 timestamps include an offset; storage normalizes absolute instants to UTC. Group calendar days in household timezone `Europe/Istanbul` for the pilot.
- Every interval includes `start` and excludes `endExclusive`. Display `lastIncludedDate` where useful for bill cycles, without changing the interval boundary.
- `meta.asOf` is the reading/calculation snapshot clock. `generatedAt` is response generation time; it is not proof that every measurement is fresh. Fixture timestamps are deliberately fixed. At HTTP delivery, `meta.requestId` is replaced with the actual request correlation UUID and matches the `X-Request-ID` header; the example request IDs are illustrative only.
- A simulator must use one documented scenario clock for generation, aggregation and freshness; do not compare an October synthetic reading to the actual November wall clock and call it offline.
- `sourceType` is `synthetic`, `physical_device`, or `historical_bill`; preserve provenance per measurement/evidence when a response draws from multiple sources. `sample: true` and `sampleLabel` are mandatory for every synthetic example.
- Power is W, active energy is kWh and currency is TRY. Use precise decimal arithmetic for money and rates. Settings propose decimal strings. Dashboard monetary fixtures use JSON numbers for compatibility while production encoding and rounding remain open.
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
| `GET /session` | Session cookie | 200 `{user,householdId,expiresAt,csrfToken}` or 401 | #16 |
| `DELETE /session` | Cookie + CSRF | 204, revoke session and expire cookie | #16 |
| `POST /households` | HouseholdCreate below | 201 Household; one household/account | #16 |
| `GET /households/{id}` | Owned ID | Household | #16 |
| `PATCH /households/{id}` | Changed settings + `revision` | Updated Household; 409 for stale revision | #16 |
| `POST /households/{id}/devices` | `{name,scope,sourceType,model,collectorId}` | 201 Device; register collector separately with owned credentials | #17 |
| `GET /households/{id}/devices` | Owned ID | `{meta,devices,collector}` | #17 / BE06 |
| `POST /households/{id}/collectors` | `{name,sourceType}` | 201 registration + one-time token; token absent from later GETs | #17 |
| `POST /collector/readings/batch` | Collector batch below | Per-event results after commit | #17 |
| `GET /households/{id}/readings` | `deviceId,start,endExclusive,limit,cursor` | `{meta,items,nextCursor}` | #17 |
| `GET /households/{id}/overview` | Explicit `start,endExclusive,resolution` | Dashboard with matched selected-period groups and separately labelled present, today and cycle groups | #11 / BE06 |
| `GET /households/{id}/consumption` | Same period filters, optional `deviceId` for detail | `{meta,period,trend,selectedPeriodEnergy,contributions,coverage}` | BE06 |
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

Settings mutations resolve ownership from the session. Proposed reading pagination defaults to 100 and caps at 1,000. Use ascending `(observedAt,readingId)` and resume strictly after an opaque cursor bound to the same household/device/period. Proposed range caps are 31 days for hourly consumption and 366 days for daily consumption. Invalid or reversed periods return 422. Ahmed still needs to confirm the limits.

### Household creation, setup and revision proposal

```json
{
  "name":"Sample home",
  "timezone":"Europe/Istanbul",
  "billingCycle":{"start":"2026-10-18T00:00:00+03:00","endExclusive":"2026-11-17T00:00:00+03:00"},
  "budget":{"value":"800.00","unit":"TRY","chargeBasis":"energy_only"},
  "tariff":{"kind":"fictional_flat_energy","currency":"TRY","ratePerKwh":"3.000000","effectiveFrom":"2026-10-18T00:00:00+03:00","effectiveUntilExclusive":null,"source":"synthetic","includedComponents":["energy"],"excludedComponents":["other_invoice_charges"]}
}
```

Incomplete setup is approved. Proposed field rules for #16:

| Field | Save and validation rules |
|---|---|
| `name` | Required non-blank trimmed string on creation. |
| `timezone` | Required IANA identifier on creation. `Europe/Istanbul` is the pilot choice. |
| `billingCycle` | Optional. If supplied, both timestamps are required and must be ordered household-local calendar boundaries. An incomplete nested object gets 422. |
| `budget` | Optional. The initial TRY energy-only target is a positive decimal string with exactly two fractional digits. |
| `tariff` | Optional. The minimum profile is a labelled fictional flat TRY energy-only rate, a nonnegative decimal string with six fractional digits. Effective periods are ordered and half-open. The profile excludes other invoice charges. Real supplier and supported invoice components are tracked separately. |

A successful create returns 201 with `householdId`, saved settings, `revision: 1`, `createdAt`, `updatedAt` and `setupCompleteness`. Omitted optional fields are returned as `null`. A PATCH includes the revision last read. Omission retains a field and explicit `null` clears an optional group. Validate a supplied group as a whole. Save the entire change atomically with the revision check, return the updated settings and revision on success, and use 409 `settings_revision_conflict` if another save won. The UI refreshes confirmed values and preserves the original draft for correction or resubmission. A rejected save leaves persisted settings unchanged.

For example, `PATCH /households/sample-household` with `{"revision":2,"tariff":null,"budget":null}` keeps the existing profile and cycle, then returns revision 3 with these fields:

```json
{
  "revision": 3,
  "tariff": null,
  "budget": null,
  "setupCompleteness": {
    "status": "incomplete",
    "missingFields": [
      {"field":"tariff","code":"tariff_missing","message":"Set an energy tariff to see cost estimates."},
      {"field":"budget","code":"budget_missing","message":"Set a cycle budget to see budget comparisons."}
    ]
  }
}
```

Use `status: "complete"` and an empty `missingFields` list when all groups are configured. Invalid supplied values return 422 with a field path such as `budget.value` and `must_be_positive`. See the [incomplete dashboard example](examples/v0.1/settings/incomplete-setup.json) for the successful read after this save.

| Absent setting | Dependent results | Independently supported results |
|---|---|---|
| `billingCycle` | Cycle, accrued cost, cycle forecast and comparison lack a period and use `billing_cycle_missing`. | Present power, today's energy and selected-period consumption. A saved budget amount can still be edited. |
| `tariff` | Cost and monetary forecast are null with `tariff_missing`. An otherwise configured budget comparison also needs that tariff. | Consumption, stored budget and an eligible energy forecast in kWh. |
| `budget` | Target and comparisons are null with `budget_missing`. | Consumption, cost and eligible energy/monetary forecasts. |

Return every missing field in `setupCompleteness`. For a single dependent result, show the first applicable cause in this order: missing billing cycle, missing budget where comparison requires it, missing tariff where money is needed, then the calculation-specific reason. Result-specific numeric zeros remain available. The example rate of TRY 3/kWh is fictional and labelled as such.

## 4. Collector batch and measurement proposal

Retain the collector plan's `/collector/readings/batch` path and its existing event naming:

```json
{
  "schema_version":1,
  "events":[{
    "event_id":"48262d61-2b10-4b67-9a24-030581467001",
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
    "quality_flags":[],
    "reset_evidence":null
  }]
}
```

Partial batch acceptance, safe retries and acknowledgement after commit are approved. The proposed response is 200 `{meta,results:[{eventIndex,eventId,status,code,message,receivedAt}]}` for any processed envelope, including all rejections. Results preserve input order with a zero-based `eventIndex`. `status` is `accepted`, `already_stored` or `rejected`. Accepted and identical retries return the original first receipt time and null code/message. A rejection has a code, null receipt time and a null event ID if the input did not have a valid ID. A malformed JSON body returns 400, an invalid envelope/count 422, a body over 1 MiB 413, and an invalid/disallowed collector credential 401/403. A transient storage failure returns 503 and the caller can retry the original payload. No event is acknowledged until the accepted writes commit.

Important invariants:

1. The authenticated credential determines collector, household and device membership. Reject the event if `collector_id`, source or scope disagrees with registration. `event_id` is a UUID. A simulated event includes its registered `sample_run_id`, and a physical one uses null. Use `device_measured_at` only for trusted device timestamps. With `timestamp_basis: "collector_observation"`, use `collected_at` and set `device_measured_at` to null.
2. Unique key `(registered collector ID, event_id)`; exact same immutable payload returns `already_stored`. Same key/different payload returns `rejected` with `event_conflict`, never overwrites an accepted reading. Non-event mutations use `Idempotency-Key` scoped to owner + route + payload hash; same key/different input returns 409.
3. Cumulative imported active energy is a counter, not energy for one poll. Adjacent valid counters in the same segment establish a delta over `[previous observed time,current observed time)`. Compare same intervals and units. First counter in a segment establishes a baseline; it is not consumed energy by itself.
4. The first energy observation starts epoch 0. A reset proposes the next epoch, the `counter_reset` flag and `reset_evidence` referencing the preceding accepted energy event. The counter must fall and the backend must corroborate the reset against the run's schedule or a physical adapter rule. The reset reading is a new baseline. Ambiguous reset or rollover leaves a coverage gap. Physical reset evidence needs an approved adapter rule.
5. Proposed limits allow an observed time up to 120 seconds ahead of the applicable clock and a late observation up to 30 days behind that device/run's newest observation. Accepted late events replace affected deltas in event-time order and invalidate dependent buckets and comparisons. They do not move freshness backward. A different event at an already occupied device/run observation time is rejected.
6. Power and energy are finite nonnegative numbers or null, with at least one available. When one is null, require the `partial_measurement` flag. Reject invalid units/types, timezone-naive times, unauthorized devices, and unsupported or export measurements. Per-model plausibility limits remain open for physical devices.
7. Add authoritative `received_at` on first acceptance. Preserve original `collected_at`/device times on retries. Retrieval maps these to `receivedAt`, `observedAt` plus timestamp basis.
8. Sum supported same-epoch deltas. A delta wholly inside the requested interval can contribute to that interval total even across a delivery gap. If a delta straddles a requested period or bucket boundary without an observation to locate consumption on each side, mark the affected result unavailable or partial and preserve coverage evidence. Never interpolate an unsupported breakdown.

Propose batches of up to 1,000 events and 1 MiB, with 100 events per chunk as the normal sender target. Preserve timestamps across retries. The [decision log](../backend/decision-log.md) covers event-field semantics, open choices and acceptance criteria. The [ingestion schema](ingestion-batch.schema.json) and [worked request/outcome sequences](examples/v0.1/ingestion/) accompany this production proposal.

For #18, propose 60-second historical observations, 10-second live reporting and 60-second collector heartbeats. Device staleness after 30 seconds and collector unreachability after 180 seconds remain provisional. A seeded run proposes 1× or 10× replay, an explicit completed state with a frozen clock and an owner-confirmed reset restricted to that synthetic run. The simulator submits readings through the authenticated #17 route. See the [scenario definitions](../backend/scenario-definitions.md).

## 5. Consumption, device and forecast responses

Concrete versioned sample payloads are in [examples/v0.1](examples/v0.1/). The [JSON Schema](dashboard-response.schema.json) validates the draft **synthetic fixture edition**. Structural validation alone cannot prove arithmetic, matching periods, auth or aggregation correctness.

| Example | HTTP for demo overview | Meaning |
|---|---|---|
| [normal](examples/v0.1/normal.json) | 200 | 820 W and 8.40 kWh today. Seven complete days total 70 kWh, with appliances 24 + 7 + 13 kWh and 26 kWh other. The last complete day totals 12 kWh, with appliances 4 + 1 + 2 kWh and 5 kWh other. |
| [empty](examples/v0.1/empty.json) | 200 | Null measurements with reasons, no trend buckets, no eligible forecast; known budget remains. |
| [partial-data](examples/v0.1/partial-data.json) | 200 | Genuine current-day household energy gap; known recorded portion/cost remain labelled partial; full-cycle forecast withheld. |
| [device-disconnected](examples/v0.1/device-disconnected.json) | 200 | Fridge interval unavailable and stale status; household values remain; remainder unavailable. |
| [error](examples/v0.1/error.json) | 503 | Request failure. Device state stays independent. |
| [incomplete-setup](examples/v0.1/settings/incomplete-setup.json) | Contract sample | Consumption and the kWh projection remain usable with the tariff and budget absent. Monetary metrics and comparisons explain the missing settings. |

`devices` response is a projection `{meta,devices,collector}` of the same scenario. `lastReadingAt` is observed time, `lastReceivedAt` first backend receipt. Collector `lastContactAt` and pending queue count each have their own observation time; cached queue count is not a live local fact during an internet outage.

The three selected-period groups use identical `start` and `endExclusive` values for a given request. `trend.period` describes the buckets, `selectedPeriodEnergy` is a kWh metric with a `period` and household `coverage`, and `contributions.period` applies to the household, appliances and remainder. The retained `contributions.household` metric agrees with `selectedPeriodEnergy`. The total may be supported by counter boundaries even if individual buckets lack coverage.

`currentPower` is a present-time reading with observation/receipt times. `todayEnergy.period` covers today's household-local elapsed interval. `billingCycle` labels the cycle, `cost.period` covers the elapsed portion, and `forecast.period`, `budget.period` and `budgetPosition.period` refer to the full cycle. The selected-period request changes only its three consumption groups. Present-time and cycle results keep their own timestamps and periods.

Each trend bucket has `start`, `endExclusive`, `value` in kWh, `partialBucket` and `coverage`. No readings yields null bucket values or an empty series, while known zero remains zero. Calculate other consumption only with matching intervals, the same basis and sufficient household and appliance coverage. A negative remainder yields null with `invalid_remainder`. Missing plug data leaves independently supported household energy available. Contribution percentages need a valid positive denominator.

### Initial cost and forecast proposal

The normal sample has recorded cycle energy 108.40 kWh at 14:30 and energy-only cost `108.4×3=325.20 TRY`. Its forecast is deliberately **dated 00:00**, when 100 kWh was observed over ten complete days and 20 days remained. Seven complete recent days total 70 kWh: `100 + (70/7×20) = 300 kWh`; `300×3=900 TRY`. Same-cycle/basis target 800 gives forecast difference 100 TRY. These are synthetic arithmetic checks, not invoice forecasts or accuracy evidence.

Forecast fields include `methodId`, `methodVersion`, `eligible` for money, `energyEligible` for kWh, `calculatedAt`, `asOf`, cycle/history/projected periods, `validDays`, `minimumValidDays`, observed/projected energy, assumptions, `maturity`, `isStale`, and unavailable reason. `projectedEnergyKwh` is the projection for `projectedPeriod`, which covers the remainder of the cycle. A missing tariff leaves an otherwise supported `projectedEnergyKwh` available with `energyEligible: true` and null monetary `value`. If energy is ineligible, `energyUnavailableReason` explains why. With no cycle, cycle-dependent periods, `calculatedAt` and `maturity` are null. Budget position references the exact forecast calculation time when used.

The approved baseline uses the latest seven complete valid days in the cycle, reliable elapsed-cycle energy and daily recomputation at household midnight. Withhold full-cycle forecasts if elapsed-cycle energy is genuinely incomplete. After relevant settings edits or reading corrections, suppress outdated budget conclusions until matching results are available. Intraday treatment, forecast freshness and maturity thresholds remain open.

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

- `GET /api/v1/demo/overview?scenario=normal` serves the fixed seven-day selection. The mock also serves a prebuilt one-day selection on the same snapshot.
- To select, send both `start` and `endExclusive` as RFC3339 instants and optionally `resolution=day`. Supported periods in Europe/Istanbul are 21–28 October 2026 and 27–28 October 2026, both with midnight boundaries and exclusive ends. Encode a literal plus sign in an offset as `%2B`. Unsupported periods or resolutions return 422.
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

Cancel superseded selections or discard their responses, including errors. Only the latest request for the active selection may update the chart, selected-period total and contributions, as one snapshot. Cache keys include household, period, resolution and contract version. Clear household caches at sign-out.

Apply settings after a confirmed save. A proposed production dashboard includes `meta.settingsRevision` from the settings snapshot used for the result. Retain editable input after a failed save. For a dependent calculation awaiting refresh, return a null value with `recalculation_pending` and use `budgetPosition.state: "pending"` when applicable. Enable comparisons once revision, currency, period and charge basis agree. Independently usable metrics may remain available during refresh.

## 9. Review and unresolved choices

Ahmed's next confirmation is the #16 session/security configuration, proposed settings fields and revision behaviour, and fictional tariff profile. The #17 ingest limits, reset evidence and coverage rules and the #18 replay settings follow. Later tariff, forecast, bill, insight and assistant questions have owners and checkpoints in the [decision log](../backend/decision-log.md).

Miray's interface review covers exact fields and labels, switching both mock selections without a stale response replacing the current selection, the empty/disconnected/error scenarios, incomplete setup and save conflict/pending states. Contract acceptance and frontend scenario-switching verification are pending. [#11 review](https://github.com/AhmedISatti03/WattWise/issues/11#issuecomment-7231387740) · [#12 review](https://github.com/AhmedISatti03/WattWise/issues/12#issuecomment-7231523153)

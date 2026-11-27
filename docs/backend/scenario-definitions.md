# Synthetic household scenarios

**Status:** Draft 0.1, for #18/BE05 review · **Date:** 27 November 2026

These are expected outcomes for future API-driven generation/replay. They are not a claim that the simulator or ingestion pipeline is implemented. The independent mock API exposes only a selected subset of fixed sample responses for review; fixed responses do not exercise storage/aggregation.

## Shared reproducible design

- Proposed default seed `481`, timezone `Europe/Istanbul`, cycle `[2026-10-18T00:00:00+03:00,2026-11-17T00:00:00+03:00)`, run ID and source kind `simulated` on every stream.
- Generate household = AC + fridge + dishwasher + independently generated other load at each interval. Persist cumulative import kWh counters for each device and instantaneous active power W. Integrated kWh is based on generated load over elapsed simulation time, not one spot reading multiplied across a day.
- Include counter baselines at the starting boundary, then deterministic time steps (proposed 60 simulated seconds for history). Future physical polling can be 10 seconds; acquisition interval is metadata, not an implied UI granularity.
- Proposed historical range: 30 complete days plus a partial day, with later days held out for forecast evaluation. The prediction at a cutoff never receives later events. A run's actual server receipt time stays distinct from its documented simulated observation/as-of clock.
- A replay uses the same seed, scenario version, start/cutoff, source events and stable IDs; retries within that run resend unchanged IDs. A fresh isolated run gets a new identity so reset counters do not collide with prior records.
- Operations to implement after ingestion rules are approved: `generate`, `import` (through ingestion HTTP), `stream`, `stop`, `replay`, `reset-demo`. Command names are proposals until the CLI exists; no executable simulator is claimed here.
- `reset-demo` must require an explicit simulation run/household and confirmation, authorize its owner, reject physical-source records and remove only the targeted sample dataset. Do not delete arbitrary user data or use a global truncate command.
- Normal-speed stream advances with wall time; accelerated replay explicitly maps elapsed wall time to simulation time. All freshness queries receive the same run clock; advancing only generator time would produce misleading stale statuses.

## Expected outcomes before execution

| ID | Deliberate input | Expected observable result |
|---|---|---|
| S01 normal | Same complete day: household12; AC4; fridge1; dishwasher2 kWh; other5. | Household stays12, appliance total7 is included, remainder5; sample labels and matching boundaries visible. At fictional3 TRY/kWh: energy cost36. |
| S02 varied patterns | Equal daily energy with distinct daytime/evening load curves. | Totals equal but charts differ; no claim that a shape identifies an unmonitored appliance. |
| S03 budget below/equal/above | Eligible same-basis forecasts720/800/900 against800. | Headroom80, equality, overspend100 respectively; no guaranteed savings. |
| S04 partial current day | Current day only until14:30, energy8.4 kWh, snapshot820W. | Partial-day flag; don't count day as complete forecasting history or extrapolate its energy without an agreed method. |
| S05 no readings / valid zero | Dataset A has no observations; dataset B has valid equal counters over complete interval. | A is null with `no_readings`; B is measured zero. No division by zero share. |
| S06 insufficient history | Three complete valid days. | Eligibility false, validDays3/required7; no numerical forecast/on-track status. |
| S07 missing tariff | Valid energy, no applicable tariff. | Energy remains visible; monetary costs/forecast unavailable with reason; no default real tariff. |
| S08 mid-cycle start | Start at day11;50 kWh through day15. | Observed-period energy50 and fictional energy cost150; full-cycle forecast unavailable because earlier data absent, even after seven later days. |
| S09 missing intervals | Remove required counter boundary or create an unresolved reset. | Coverage flagged; withhold unsupported bucket/remainder/forecast; known values retain their observed interval. |
| S10 delayed transport | Two same-epoch valid counters establish total across delivery gap. | Recover supported interval total once received; do not invent within-gap detail or update old observation time. |
| S11 unplugged fridge | Household valid; fridge interval unknown; last observed14:20 at asOf14:30. | Fridge stale/partial, share/remainder unavailable; unaffected household metrics retained. |
| S12 disconnected collector | Collector last contact exceeds agreed threshold. | Collector unreachable; individual local device state unknown; failed dashboard request remains a different state. |
| S13 recovery / duplicates | Buffer valid events, retry accepted IDs, restore network. | Accepted unique events persist once; replay unchanged IDs returns already-stored; totals unchanged by retry. |
| S14 conflicting repeat | Same event ID, changed energy value. | Explicit conflict outcome; original event remains unchanged; no doubled energy. |
| S15 reset/new epoch | Old counter10→11 then new epoch0→0.5. | First new-epoch value is baseline, not−11; subsequent valid delta0.5; cross-reset interval unresolved. |
| S16 late arrival | Counters0 at00:00,2 at02:00; later1 at01:00. | Total remains2; derived intervals can split into1+1; cached dependent responses invalidated. |
| S17 impossible remainder | Household12, appliances13 over supposedly matching interval. | Other unavailable `invalid_remainder`, not−1 or0. Flag comparison; do not alter household to match appliances. |
| S18 invalid request / foreign device | Naive/future-invalid time, unsupported unit, nonfinite value, unknown/other user's device. | Contract-defined field/auth errors; no unauthorized insertion or implicit registration. |
| S19 failed GET / refresh | Force HTTP503 while cached data exists. | Request error with retry guidance; old values retain timestamps/stale indication, no claim physical devices are off. |
| S20 forecast example | Cutoff after10 complete days, recorded100, latest7 total70,20 days remain. | Baseline10/day, remaining200, total300, fictional energy cost900; same-basis budget800 gives100 projected overspend. |
| S21 bill duplicate/extraction | Poor file or same candidate confirmed twice. | Extraction failure offers manual entry; repeat confirmation returns same record according to approved retry rules; no monitor-energy overwrite. |
| S22 assistant/provider error | Authorized missing-data query or provider timeout. | Distinct insufficient-data/provider failure, no invented numbers; consumption API still works. |

## Verification record

For each run store scenario ID/version, seed, simulation range/asOf, source event count, expected values, API command, actual response/status, stored unique count, method/settings versions, commit and failure details. Confirm persistence by restarting the backend, then replay unchanged input and compare counts/totals. Use two accounts for ownership checks.

Forecast evaluation must separate historical development inputs from later held-out periods chronologically. Report units and horizons, compare the baseline and Ahmed's candidate with identical permitted inputs, and state that synthetic performance cannot establish real-household accuracy. Physical #4 validation remains separate.

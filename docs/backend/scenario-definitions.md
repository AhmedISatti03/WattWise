# Synthetic household scenarios

**Status:** #30 proposals for #17–18 implementation review · **Date:** 28 November 2026

Ahmed approved using persisted synthetic readings and a consistent simulation clock. The workflows below propose how to exercise those decisions through the real ingestion interface. The mock API serves fixed response examples for frontend development. [Decision log](decision-log.md)

## Shared reproducible design

- Proposed default seed `481`, timezone `Europe/Istanbul`, cycle `[2026-10-18T00:00:00+03:00,2026-11-17T00:00:00+03:00)`, run ID and source kind `simulated` on every stream.
- Generate household = AC + fridge + dishwasher + independently generated other load at each interval. Persist cumulative import kWh counters for each device and instantaneous active power W. Integrated kWh is based on generated load over elapsed simulation time, not one spot reading multiplied across a day.
- Include counter baselines at the starting boundary. Generate historical snapshots every 60 simulated seconds. In streaming and device-state replays, report each device and submit available readings every 10 simulated seconds, with an independent 60-second simulated heartbeat. The separate historical import cadence is for energy history.
- Use 30 complete days plus a partial day for the initial historical setup, with later days held out for forecast evaluation. A forecast at a cutoff receives only data available by that cutoff.
- Persist run ID, seed, scenario version, start, cutoff and progress. Construct stable event IDs from the run ID, source device identity and logical step. Replay the same run with identical events; resume a stopped run at the stored progress. An isolated run with the same seed/range reproduces values and times under new event IDs.
- Use the proposed commands `generate`, `import`, `stream`, `stop`, `replay` and `reset-demo` once the tooling exists. Imports and live/replayed readings use registered simulated collector credentials and `POST /api/v1/collector/readings/batch`. Submit historical observations in order, with the registered run clock at the history cutoff for an import. Live/replayed observations advance the same run clock used by freshness and aggregation. Wait for ingest acknowledgement, retry the original event IDs after transient failures and surface terminal event outcomes.
- Use 1× wall-time progression for live stream and replay by default. Offer an initial 10× replay option, advancing the scenario clock by ten simulated seconds per elapsed real second. Distinguish that clock from first server receipt time. Paused runs hold at the last scenario instant; completed runs hold at the declared cutoff after expected outcomes have been acknowledged. Return the run state (`running`, `paused` or `completed`) alongside its snapshot and show terminal unexpected failure as a run error.
- Propose device stale at 30 or more simulated seconds since its last successful observation and collector unreachable at 180 or more simulated seconds since its last successful contact. Both thresholds remain provisional. Keep request failures independent of both signals. Completed and paused runs show their status with freshness evaluated against their held snapshot.
- Require the owner to name and confirm the isolated run when resetting. Stop or fence the run first so queued events cannot repopulate it, delete its synthetic records and derived outputs, and create a new run identity for a fresh run. Refuse resets for unowned runs or physical datasets.

## Expected outcomes before execution

| ID | Deliberate input | Expected observable result |
|---|---|---|
| S01 normal | Same complete day: household12; AC4; fridge1; dishwasher2 kWh; other5. | Household stays12, appliance total7 is included, remainder5; sample labels and matching boundaries visible. At fictional3 TRY/kWh: energy cost36. |
| S02 varied patterns | Equal daily energy with distinct daytime/evening load curves. | Totals equal but charts differ; no claim that a shape identifies an unmonitored appliance. |
| S03 budget below/equal/above | Eligible same-basis forecasts720/800/900 against800. | Headroom80, equality, overspend100 respectively; no guaranteed savings. |
| S04 partial current day | Current day only until14:30, energy8.4 kWh, snapshot820W. | Partial-day flag; don't count day as complete forecasting history or extrapolate its energy without an agreed method. |
| S05 no readings / valid zero | Dataset A has no observations; dataset B has valid equal counters over complete interval. | A is null with `no_readings`; B is measured zero. No division by zero share. |
| S06 insufficient history | Three complete valid days. | Eligibility false, validDays3/required7; no numerical forecast/on-track status. |
| S07 incomplete setup | Valid energy and configured cycle, with tariff absent in one run and budget absent in another. | Missing tariff leaves supported energy and kWh forecast available and withholds monetary outputs with `tariff_missing`. A missing budget leaves independently supported costs/forecasts available and withholds comparisons with `budget_missing`. |
| S08 mid-cycle start | Start at day11;50 kWh through day15. | Observed-period energy50 and fictional energy cost150; full-cycle forecast unavailable because earlier data absent, even after seven later days. |
| S09 missing intervals | Remove required counter boundary or create an unresolved reset. | Coverage flagged; withhold unsupported bucket/remainder/forecast; known values retain their observed interval. |
| S10 delayed transport | Two same-epoch valid counters establish total across delivery gap. | Recover supported interval total once received. Unsupported finer buckets are unavailable. Power freshness reflects the last observed time. |
| S11 unplugged fridge | Household valid; fridge interval unknown; last observed14:20 at asOf14:30. | Fridge stale/partial, share/remainder unavailable; unaffected household metrics retained. |
| S12 disconnected collector | Collector last contact reaches the proposed 180-second threshold. | Collector is unreachable and current local device state is unknown. |
| S13 recovery / identical retry | Buffer valid events, lose a response after commit, restore network, resend identical event IDs. | Returns `already_stored` with original receipt time for committed events. Stored counts and totals are stable and previously undelivered valid events can proceed. |
| S14 conflicting repeat | Same event ID, changed energy value. | Returns `event_conflict`; later queries reflect the original reading once. |
| S15 reset/new epoch | Counter goes 102→103, then resets to 0 and increments to 0.5 in the next epoch. Include the registered reset marker and accepted predecessor ID. | The first new-epoch value establishes its baseline and subsequent consumption is 0.5 kWh. Cross-reset interval energy is unavailable. A decrease in the old epoch without corroboration is rejected. |
| S16 late arrival | Counters 100 at 08:00Z and 102 at 10:00Z, later 101 at 09:00Z. | The two-hour total stays 2 kWh. Once the missing boundary arrives, 1 kWh is supported in each hour and dependent results are invalidated for recalculation. |
| S17 impossible remainder | Household12, appliances13 over supposedly matching interval. | Other unavailable `invalid_remainder`, not−1 or0. Flag comparison; do not alter household to match appliances. |
| S18 invalid request / foreign device | Naive/future-invalid time, unsupported unit, nonfinite value, unknown/other user's device. | Contract-defined field/auth errors; no unauthorized insertion or implicit registration. |
| S19 failed GET / refresh | Force HTTP503 while cached data exists. | Request error with retry guidance; old values retain timestamps/stale indication, no claim physical devices are off. |
| S20 forecast example | Cutoff after10 complete days, recorded100, latest7 total70,20 days remain. | Baseline10/day, remaining200, total300, fictional energy cost900; same-basis budget800 gives100 projected overspend. |
| S21 bill duplicate/extraction | Poor file or same candidate confirmed twice. | Extraction failure offers manual entry; repeat confirmation returns same record according to approved retry rules; no monitor-energy overwrite. |
| S22 assistant/provider error | Authorized missing-data query or provider timeout. | Distinct insufficient-data/provider failure, no invented numbers; consumption API still works. |
| S23 mixed batch | Submit a valid reading and an event with a negative cumulative import counter. | One commit adds just the valid event. In-order outcomes are `accepted` and `rejected` with `invalid_reading_value`. |
| S24 replay completion | Deliver a same-seed live-cadence replay at 1× and 10× through the configured cutoff. | Equivalent values, observation times and coverage. Freshness at the frozen cutoff stays stable across refreshes and `completed` is visible. |
| S25 scoped reset | Reset one confirmed isolated run while another run and a physical registration exist. | The targeted run and its derived results are removed. Other data remain available. Replay under a new run ID does not reuse old event IDs. |

[Ingestion examples](../api/examples/v0.1/ingestion/) give the full batch requests and responses for S13–S16, S23 and a successful ingest.

## Verification record

For each run store scenario ID/version, seed, simulation range/asOf, source event count, expected values, API command, actual response/status, stored unique count, method/settings versions, commit and failure details. Confirm persistence by restarting the backend, then replay unchanged input and compare counts/totals. Use two accounts for ownership checks.

Forecast evaluation must separate historical development inputs from later held-out periods chronologically. Report units and horizons, compare the baseline and Ahmed's candidate with identical permitted inputs, and state that synthetic performance cannot establish real-household accuracy. Physical #4 validation remains separate.

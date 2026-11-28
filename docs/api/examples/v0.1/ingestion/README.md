# Proposed ingestion examples for #17

These synthetic examples show six calls to the proposed `POST /api/v1/collector/readings/batch` endpoint in order. Each file contains the HTTP JSON `request`, expected status, JSON `response` and expected effects. The surrounding fields describe the example. The [schema](../../../ingestion-batch.schema.json) covers request envelopes, individual events and outcome shapes. Approval status and semantic rules are recorded in the [decision log](../../../../backend/decision-log.md#priority-2--recommendations-for-17-ingestion).

Assume a simulated household collector and monitor are registered to `seed-42-ingestion`, the scenario clock has reached `2026-10-28T13:00:00Z`, and that run records a reset at 12:00Z. Each request uses the collector’s bearer credential. The example server receipt dates are intentionally later than the scenario observation dates.

| Sequence | Expected result |
|---|---|
| [1. Success](01-success.json) | Two observations commit and support the 2 kWh total across 08:00–10:00Z. |
| [2. Mixed validity](02-mixed-validity.json) | A valid reading commits, and a negative import counter is rejected individually. |
| [3. Identical retry](03-identical-retry.json) | Retrying a committed event reuses its receipt time and leaves its row count at one. |
| [4. Changed duplicate](04-changed-duplicate.json) | A reused event ID with a different counter yields `event_conflict`. |
| [5. Verified reset](05-verified-reset.json) | Epoch 1 starts with a baseline. The cross-reset interval is unavailable and the next delta is 0.5 kWh. |
| [6. Delayed reading](06-delayed-reading.json) | An earlier same-epoch reading resolves two 1 kWh hourly buckets and preserves the 2 kWh total. |

These are the review inputs for the future ingestion service. The public mock API serves its separate dashboard examples.

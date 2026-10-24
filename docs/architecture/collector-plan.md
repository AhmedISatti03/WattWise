# WattWise — Collector Implementation Plan

**Status:** Draft for team review; implementation has not started under this plan.  
**Prepared:** 24 October 2026  
**Related tasks:** [#8 — Specify the collector's first implementation](https://github.com/AhmedISatti03/WattWise/issues/8), [#4 — Read and store data from one plug](https://github.com/AhmedISatti03/WattWise/issues/4)  
**Proposed repository location:** `docs/architecture/collector-plan.md`

## 1. Purpose and boundaries

The local collector will read power and cumulative energy from the household monitor and smart plugs, save readings locally, and send them to the WattWise backend. Development can begin with simulated devices before hardware arrives.

This document proposes the first implementation. Frequencies, interfaces, and operational limits below are starting choices for review, not validated hardware capabilities.

The current MVP requires one whole-household monitor and one smart-plug model covering 2–3 appliances. Whole-household readings already include appliance consumption. The collector must preserve their distinct measurement scopes so the application can avoid double counting.

The collector handles acquisition and delivery. The backend handles household access, durable central storage, consumption calculations, tariffs, forecasts, and recommendations. Appliance switching is outside this implementation.

## 2. Proposed flow

```text
Simulated adapters OR real device adapters
                    ↓
         Read and validate measurements
                    ↓
       Normalize units and add metadata
                    ↓
       Persist to a local SQLite outbox
                    ↓
          Send batches over HTTPS
                    ↓
    Backend validates and stores each event
                    ↓
      Acknowledge committed event IDs
                    ↓
       Remove acknowledged outbox events
```

Acquisition and delivery run independently. An unavailable backend must not stop collection from reachable devices.

## 3. Where the collector runs

### Development

Initially run the collector as a local process on a developer's laptop. Simulated adapters require no physical devices. Real-device testing requires a host on the same reachable local network as the selected devices.

The development setup needs:

- The runtime selected for the collector, independently of the backend language.
- A persistent writable directory for SQLite and operational state.
- Device configuration, a backend URL, and a collector credential supplied outside version control.
- A working system clock synchronized through the operating system.
- A local backend or mock ingestion service for early development.

A laptop is suitable for supervised testing. Collection stops when it sleeps, shuts down, or leaves the home network.

### Continuous pilot operation

Use a dedicated, always-on host in the pilot home, such as an available Raspberry Pi or small computer. The final host and budget remain open decisions; no purchase is needed to write or begin this plan.

The pilot host must:

- Remain powered and connected to the device network when team laptops are off.
- Start the collector automatically after boot and restart it after a crash.
- Keep the outbox on persistent storage across restarts and updates.
- Have outbound HTTPS access to the hosted backend; devices do not need public inbound access.
- Provide logs, disk-usage monitoring, and a way for the team to inspect failures.

Prefer wired networking for the host where practical. Configure a supervised service after choosing its operating system. Containers are optional; they must use persistent storage if adopted.

Power loss can stop both collection and network access. Automatic restart reduces downtime but does not recover measurements that were never acquired.

## 4. Reading devices and collection frequency

### First real-device adapter

Prioritize a Shelly plug, consistent with the hardware review on #2. Use its documented local HTTP/RPC interface for the first adapter. Polling avoids introducing an MQTT broker before the basic reading-to-backend flow works.

Validate the exact model, firmware, authentication method, component identifiers, response fields, energy units, and counter persistence on the purchased device. Do not assume every Shelly model exposes the same response structure.

Add a separate adapter for the selected household monitor after its supply coverage and installation are confirmed. A multi-phase adapter must validate complete household coverage and avoid adding both phase values and an aggregate total into the household total.

MQTT can be evaluated later if the selected hardware and operational needs justify it. Supporting both transports is not required for the first implementation.

### Proposed schedule

| Activity | Initial setting | Reason |
|---|---|---|
| Device polling | Every 10 seconds per device | Provides useful dashboard updates for a small pilot without aiming for sub-second monitoring. |
| Device request timeout | 3 seconds | A missing device should not block other devices indefinitely. |
| Upload | Every 30 seconds, up to 100 events per request | Limits request overhead while keeping normal delivery reasonably current. Drain additional batches when recovering. |
| Collector heartbeat | Every 60 seconds | Distinguishes collector connectivity from individual device failures. |
| Stale-reading threshold | 30 seconds without a successful reading | Initial device-status threshold, to be adjusted after observation. |
| Collector-unreachable threshold | 180 seconds without backend contact | Allows several missed heartbeats before flagging an interruption. |

Make these settings configurable. Do not overlap polls for the same device; skip a missed schedule slot rather than creating a burst of artificial historical readings. Track devices independently.

These settings imply about 34,560 readings per day for four devices. Measure actual outbox size and upload throughput during simulation before choosing storage limits.

## 5. Reading contract

The following is a proposed, language-independent JSON event. The example is explicitly simulated.

```json
{
  "schema_version": 1,
  "event_id": "c7f34cd0-e79e-4df1-8d8b-b77fac0061d4",
  "collector_id": "collector-pilot-01",
  "device_id": "sample-plug-01",
  "measurement_scope": "appliance",
  "source_kind": "simulated",
  "sample_run_id": "simulation-2026-10-24-01",
  "device_measured_at": null,
  "collected_at": "2026-10-24T09:00:00Z",
  "timestamp_basis": "collector_observation",
  "power_w": 120.0,
  "energy_import_total_kwh": 2.345,
  "counter_epoch": 0,
  "quality_flags": []
}
```

### Field meaning

| Field | Meaning and rule |
|---|---|
| `schema_version` | Version of the agreed payload contract. |
| `event_id` | Unique ID created once, persisted locally, and reused unchanged for retries. |
| `collector_id` | Stable registered collector identity; preserved across restarts. |
| `device_id` | Stable registered measurement-source identity. Do not use a changeable IP address or appliance display name as its identity. |
| `measurement_scope` | `household` or `appliance`, assigned through validated registration. |
| `source_kind` | `simulated` or `physical_device`; retained through storage and display. |
| `sample_run_id` | Identifies a simulation run; null for physical readings. |
| `device_measured_at` | UTC device measurement time if actually provided and trustworthy; otherwise null. |
| `collected_at` | UTC time when the collector obtained the reading. Never replaced by retry time. |
| `timestamp_basis` | States whether the selected observation time comes from the device or collector. |
| `power_w` | Active power in watts; null when unavailable, never an invented zero. |
| `energy_import_total_kwh` | Cumulative imported active energy in kWh for the documented counter, not energy used during this poll. Null when unavailable. |
| `counter_epoch` | Persisted local counter segment, incremented when an observed reset is detected. |
| `quality_flags` | Explicit conditions such as `counter_reset`, `clock_untrusted`, or `partial_measurement`. |

The backend adds `received_at` when the event first reaches ingestion and preserves it when the same event is retried. It derives household ownership from the authenticated collector registration and verifies each device belongs to that registration.

Device registration also records physical identifiers, model, channel/phase mapping, appliance association where relevant, native units, and counter behavior. A changed appliance association needs an effective time so historical readings keep their meaning.

### Validation and energy interpretation

- Convert native Wh to kWh where required; retain enough precision for subsequent differences.
- Reject malformed or non-finite values. Treat unsupported fields as unavailable and report why.
- Confirm imported energy semantics on the selected hardware. Exported energy, if available, requires a separate field and must not be silently substituted.
- Flag unexpected negative values for review; do not silently clamp them to zero.
- Calculate energy differences centrally only between compatible counters in the same segment and matching measurement scope.
- A falling cumulative counter starts a new segment and raises a reset flag. The first value in the new segment establishes a baseline; it is not automatically counted as new consumption.
- Preserve last counter values and segments across collector restarts. Device replacement or an intentional counter reset must be recorded.
- A device may reset and surpass its former value during a long outage. Reset detection from values alone is therefore incomplete; use device boot/reset metadata where available and flag uncertainty.
- A cumulative-counter difference across a gap may recover total energy if the counter remained valid. It cannot reconstruct the missing power profile or precisely allocate energy within the gap.

## 6. Backend delivery and duplicate prevention

Propose `POST /api/v1/collector/readings/batch` as the ingestion endpoint, subject to the backend API agreement. Use HTTPS for hosted delivery and a collector credential scoped to its registered household and devices.

For each event the backend returns its ID with one of these outcomes:

- `accepted`: committed to storage.
- `already_stored`: the same ID and payload were previously committed.
- `rejected`: invalid event, with a stable reason code.

Enforce a database uniqueness constraint on the authenticated collector identity and event ID. An existing ID with a different payload is a conflict, not a successful duplicate. Acknowledgments must follow successful database commit.

The collector deletes only events acknowledged as `accepted` or `already_stored`. A response timeout leaves events pending because the backend may already have stored them. Retrying the original IDs prevents duplicate storage in that case.

This provides at-least-once delivery attempts with duplicate-safe backend storage, rather than a promise that every acquired or attempted measurement can never be lost.

## 7. Buffering, retries, and restarts

### Persistent outbox

Write each normalized event to SQLite in a committed transaction before attempting delivery. Keep the database on persistent local storage. Maintain per-device state, including last successful observation and counter segment, transactionally with event creation where applicable.

Send pending events oldest first. Quarantine permanently invalid events with their rejection reason so one bad event does not block the queue. Keep them visible for investigation.

Propose an initial 250 MiB outbox limit, to be validated using measured event and database sizes. Warn at 80% usage. At the limit, retain queued events, stop accepting new readings, and report a storage-full condition. Do not silently discard old or new readings. Leave operational disk headroom for logs and recovery.

This bounded policy creates a collection gap if an outage lasts beyond available storage. The pilot must monitor the queue and revise its capacity if necessary. Quarantined records and logs also need bounded retention.

### Retry policy

- Retry network failures, HTTP 429, and transient server failures with exponential backoff: start at 5 seconds and cap at 5 minutes, adding jitter. Honor `Retry-After` where supplied.
- On authentication failures, retain the queue and report a configuration problem; avoid rapid repeated requests.
- On payload rejection, quarantine the affected event. If a batch is rejected without per-event results, retain it for diagnosis rather than deleting it.
- Continue collecting from reachable devices during backend outages while storage capacity permits.
- During a device outage, record its failure state and last success time. Do not create zero-power or zero-energy readings to fill the gap.

### Restart behavior

On startup, recover pending events and persisted device state, resume delivery, and begin new polls. Acknowledged delivery must remain safe if the process crashes before local deletion: the backend recognizes the retried event IDs.

Do not replay missed polling slots as if they had been measured. Report the interruption and obtain fresh readings. Verify the system clock before assigning trustworthy times; flag clock problems and avoid presenting affected records as reliable chronological measurements.

## 8. Device and collector status

Track these independently:

- **Device status:** awaiting first reading, reporting, stale/unreachable, or configuration error.
- **Delivery status:** last successful backend contact, pending event count, oldest pending event time, and upload failure reason.
- **Collector health:** heartbeat time, storage usage, and storage-full state.

Send status updates and heartbeats separately from measurement events so a failed poll is not confused with a consumption value. The backend infers collector connectivity from contact times; delayed historical uploads do not make an old device reading current.

The interface should show source type, last measurement time, and delivery freshness separately. During an internet outage the backend cannot know the collector's current local device status; show the latest known state with its age.

Miray should review the wording and minimum fields needed for these states before implementation.

## 9. Starting without hardware

Implement a simulated adapter with the same interface as a physical adapter. Both return measurements to the same validation, normalization, outbox, upload, and backend-storage flow.

Create one simulated household source and 2–3 simulated appliance sources. Generate coherent cumulative energy by integrating the simulated load over elapsed time. Household consumption includes those appliances plus a defined other load; simulated totals must not add appliance use twice.

Use a reproducible scenario seed and a controllable clock for checks. Preserve simulation state across ordinary collector restarts. A fresh scenario uses a new run ID and isolated data so restarted counters are not confused with prior runs.

Every event, stored record, API result, and dashboard view must retain its simulated status. Use a separate development household or dataset, and prevent simulated events from entering the live pilot's measured totals.

Exercise at least these scenarios:

| Scenario | Expected result |
|---|---|
| Normal collection | Valid readings arrive with correct units, identity, scope, and sample labels. |
| One device disconnects | Other devices continue; missing readings remain missing and status becomes stale. |
| Backend/internet outage | Readings accumulate locally and drain after recovery. |
| Response lost after backend commit | Retried IDs do not create duplicate rows. |
| Collector restart | Pending data and counter state survive; no invented readings fill downtime. |
| Counter reset | New counter segment is recorded without a negative consumption difference. |
| Invalid payload or expired credential | Data is retained or quarantined appropriately and the error is visible. |
| Buffer reaches capacity | A visible storage-full condition occurs and data loss is not hidden. |
| Clock change | Timestamp quality is flagged and historical events are not retimestamped. |

Simulation validates software behavior. It does not establish physical-device accuracy, firmware compatibility, or completion of #4's real-device acceptance criteria.

## 10. Initial implementation steps

1. Agree the adapter interface, event schema, registration rules, and batch acknowledgment contract with the backend work.
2. Select a collector runtime and create a small runnable process with configuration validation. Keep the protocol independent of the backend language.
3. Add simulated adapters and a simple ingestion stub to exercise the full flow immediately.
4. Implement the SQLite outbox and persistent counter state before relying on network delivery.
5. Implement authenticated batch ingestion, database uniqueness, and per-event outcomes in the backend; replace the stub.
6. Add device status, heartbeat reporting, retry behavior, and bounded storage handling.
7. Run the failure scenarios above and record results for review.
8. Under #4, add the selected plug's physical adapter and prove a real reading can be stored and retrieved. Check units and counter behavior against the device's own records.
9. Add the remaining appliance devices and selected whole-house monitor after validation and installation.
10. Move the collector to the continuous pilot host, configure startup/restart behavior, and verify operation while team laptops are off.

These steps can become separate board tasks with one main owner and explicit acceptance criteria. #8 delivers the reviewed plan; working implementation remains separate.

## 11. Unresolved decisions

| Decision | Proposed direction / evidence needed |
|---|---|
| Collector runtime | Choose based on maintainability and device integration; backend language does not need to match. |
| Continuous host | Confirm available hardware, operating system, power, storage, and budget. |
| Exact devices | Prioritize Shelly integration; validate model/firmware and household supply coverage before purchase. |
| Device interfaces | Confirm RPC calls, field semantics, authentication, timestamps, and counter persistence on actual hardware. |
| Backend contract | Agree endpoint, payload limits, credentials, registration, and partial-batch responses. |
| Polling and status thresholds | Start with this plan's settings; revise using observed device behavior and dashboard needs. |
| Storage and retention | Measure queue growth and recovery speed; validate the proposed capacity and operational response. |
| Historical recovery | Determine whether selected devices expose usable history; not assumed for the first implementation. |
| Timestamp quality | Confirm clock synchronization and handling of device versus collector timestamps. |
| Pilot operations | Assign responsibility for checking health, updating credentials, and recovering from storage or host failures. |

## 12. Review checklist

- [ ] Ahmed confirms energy semantics, counter handling, scopes, and gap treatment.
- [ ] Miray confirms device and collector status fields support understandable interface states.
- [ ] Collection-to-backend flow and duplicate handling are clear enough to implement.
- [ ] Continuous operation is distinguished from laptop development.
- [ ] Buffering, outage limits, restarts, and unrecoverable measurement gaps are explicit.
- [ ] Simulated development follows the real ingestion path and remains visibly labelled.
- [ ] Implementation steps and unresolved decisions are recorded.

## References

- [Authoritative MVP scope](https://github.com/AhmedISatti03/WattWise/blob/main/docs/mvp-scope.md)
- [Hardware comparison](https://github.com/AhmedISatti03/WattWise/blob/main/docs/WattWise_Hardware_Comparison.txt)
- [Ahmed's hardware review and collector requirements on #2](https://github.com/AhmedISatti03/WattWise/issues/2#issuecomment-6317079255)
- [Collector planning task #8](https://github.com/AhmedISatti03/WattWise/issues/8)
- [Real-device integration task #4](https://github.com/AhmedISatti03/WattWise/issues/4)

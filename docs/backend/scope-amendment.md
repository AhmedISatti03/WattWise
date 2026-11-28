# Scope amendment for the first local demonstration

**Status:** Approved direction under D14 by Ahmed on 28 November 2026

**Related:** #14/BE01, #30, both v1.0 handoffs · [Approval evidence](https://github.com/AhmedISatti03/WattWise/blob/main/docs/backend/ahmed-review-response-v1.md)

## Why a recorded amendment is needed

`docs/mvp-scope.md` still requires real household monitoring and 2–3 appliance integrations for complete-MVP acceptance and lists conversational LLM integration outside the MVP. `docs/architecture/collector-plan.md` describes dedicated Pi operation from development. The published 26 November handoffs instead establish the first demonstration on a teammate's laptop with synthetic readings ingested and persisted by a backend and with Ahmed's assistant integration. These are different completion boundaries; none should be silently presented as the other.

## Approved delivery direction

> The first local demonstration runs the application on a teammate’s laptop with explicitly labelled synthetic household and appliance readings. The simulator sends readings through the same ingestion interface intended for the future collector. Persistent storage and application services drive consumption, estimated costs, the explainable baseline forecast, alerts and recommendations. The development mock serves fixed payloads for interface review.
>
> The local demonstration includes coordinated assistant integration. Umut supplies household-authorized query services and owns the explainable baseline forecast. Ahmed leads assistant design, provider integration, prompts, tool orchestration and AI evaluation, and owns the later ML forecast candidate. Miray owns the responsive frontend and chat presentation. The rest of the application remains available if the assistant provider fails.
>
> Physical pilot completion is a subsequent milestone. Validate the selected monitor's complete household coverage and a real plug's acquisition-to-storage path under #4, including units, resets, outages and reference comparisons. Evaluate real-household accuracy with actual permitted measurements. The dedicated collector/Pi plan applies to physical deployment.
>
> Household totals include monitored appliance energy. Compare matching periods, distinguish unavailable measurements from known zero, identify excluded invoice charges in energy-only estimates and preserve historical bills separately from monitored data. Withhold forecasts and claims where supporting evidence is insufficient.

## Acceptance checkpoints

Use this record and the [decision log](decision-log.md) for the approved stage boundary. #17–18 verify the persistent synthetic path. Later handoff tasks add the consumption, calculation and assistant functionality used in the integrated demonstration. #4 verifies the real-device path. Real-household accuracy requires the later evaluation checkpoint. The [published handoffs](../handoffs/README.md) remain the responsibility and sequencing reference.

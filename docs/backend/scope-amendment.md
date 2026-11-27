# Proposed reconciliation of the MVP and implementation handoffs

**Status:** Draft for Ahmed's confirmation; existing source documents not amended.  
**Date:** 27 November 2026 · **Related:** #14/BE01, both v1.0 handoffs.

## Why a recorded amendment is needed

`docs/mvp-scope.md` still requires real household monitoring and 2–3 appliance integrations for complete-MVP acceptance and lists conversational LLM integration outside the MVP. `docs/architecture/collector-plan.md` describes dedicated Pi operation from development. The published 26 November handoffs instead establish the first demonstration on a teammate's laptop with synthetic readings ingested and persisted by a backend and with Ahmed's assistant integration. These are different completion boundaries; none should be silently presented as the other.

## Proposed text for review

> The first local demonstration implements the seven core application capabilities against explicitly labelled synthetic household and appliance readings. The simulator must send those readings through the same ingestion interface intended for the future collector; persistent storage and application services drive consumption, estimated costs, baseline forecasts, alerts and recommendations. Static dashboard JSON alone does not satisfy integrated simulation acceptance.
>
> The local demonstration also includes the conversational assistant coordinated with Ahmed: Umut supplies household-authorized query services and the chat integration boundary; Ahmed owns provider selection, prompts, tool orchestration, AI evaluation and future ML forecasting candidates; Miray owns the responsive frontend and chat presentation. Assistant failure must not make other application features unusable. This inclusion supersedes the older exclusion for this defined delivery stage only.
>
> Physical pilot completion remains a subsequent milestone: validate the selected monitor's complete household coverage and a real plug's acquisition-to-storage path, including units, resets, outages and reference comparisons. A simulated demonstration cannot close real-hardware task #4 or establish real-household forecasting accuracy. The dedicated collector/Pi plan remains the future physical deployment plan; it is not required to run the current laptop demonstration.
>
> All previously documented measurement rules remain: household totals include appliances; compare matching periods; missing is not zero; energy-only estimates identify excluded invoice charges; historical bills do not overwrite monitoring data; unsupported forecasts and claims are withheld. Native apps, appliance control, unmonitored-appliance identification and fault diagnosis remain outside this delivery unless separately assigned.

## Confirmation and propagation

Ahmed should confirm the stage names, assistant inclusion and physical follow-up boundary. After confirmation, update `docs/mvp-scope.md` and add dated cross-references in the collector plan and both handoff versions through the repository's versioning workflow. Preserve both Word/Markdown handoff versions together when revising their normative body text. This proposal does not rewrite finalized v1.0 files or claim the amendment has been accepted.

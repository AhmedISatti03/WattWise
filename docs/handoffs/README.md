# WattWise implementation handoffs

Finalized handoff versions are 1.0, dated 26 November 2026.

| Owner | Readable handoff | Download |
| --- | --- | --- |
| Umut Topatan | [Backend handoff](WattWise_Backend_Handoff_Umut_v1.0.md) | [Word](WattWise_Backend_Handoff_Umut_v1.0.docx) |
| Miray Pınarbaşı | [Frontend handoff](WattWise_Frontend_Handoff_Miray_v1.0.md) | [Word](WattWise_Frontend_Handoff_Miray_v1.0.docx) |

## Backend integration for Miray

The backend integration handoff accompanies the frontend handoff. It covers the PR #29 mock service, the first #19 review, and the checks for #11, #12, #20 and #22. [Markdown](WattWise_Backend_Integration_Handoff_Miray_v1.0.md) · [Word](WattWise_Backend_Integration_Handoff_Miray_v1.0.docx)

## Start here

Read the assigned GitHub issue and your handoff, then inspect the current repository and the counterpart's integration requirements. The Markdown copies preserve the Word documents' body text and tables. Version 1.0 is the published baseline in both formats. Record subsequent approved revisions with matching version updates in both formats.

Umut begins with BE01 to propose backend rules and the shared API contract. Miray begins with FE01 to inspect the existing frontend, propose screen needs and collaborate on that contract. These design activities can proceed together. Ahmed confirms outstanding product and interface decisions. Routine internal choices and independent work can proceed.

The initial integration checkpoint connects saved household settings and consumption views through BE03 and BE06. Later work adds forecasts, bills, insights and Ahmed's assistant. Joint final verification uses BE11 and FE10.

## Existing repository references

- [MVP scope](../mvp-scope.md)
- [Energy display rules](../energy-display-rules.md)
- [Insight scenarios](../insight-scenarios.md)
- [Collector plan](../architecture/collector-plan.md)
- [Screen requirements](../frontend/screen-requirements.md)
- [Wireframes](../frontend/wireframes.md)
- [Backend design proposal and review package](../backend/README.md)
- [Draft shared API contract](../api/frontend-contract.md)
- [Backend decision log](../backend/decision-log.md)
- [Synthetic scenario definitions](../backend/scenario-definitions.md)
- [Task-to-handoff mapping](../backend/task-mapping.md)
- [Proposed scope reconciliation](../backend/scope-amendment.md)

The Word handoffs refer to `docs/product/insight-scenarios.md`. The existing repository file is `docs/insight-scenarios.md`, linked above. Use that current location during inspection.

The handoffs extend the older scope to the local simulated delivery and assistant integration. They assign baseline forecasts to Umut, and conversational AI, evaluation and ML improvements to Ahmed. The older MVP documents remain relevant for measurement rules. Record the approved scope and contract changes as the design tasks proceed.

## Task mapping

BE01–BE11 and FE01–FE10 are handoff task references. Map them to current GitHub issues during backlog setup, preserving existing deliverables and avoiding duplicate tasks. Inspect issue state and branch contents before implementation.

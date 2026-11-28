# Backend design and handoff review

**Version:** reviewed direction and implementation proposals · **Updated:** 28 November 2026 · **Owner:** Umut Topatan

Ahmed reviewed and approved the core design direction in D01–D14 with qualifications. He also accepted the runnable foundation in #15 after a Linux/SQLite setup check. Issue #30 records the implementation recommendations that still need confirmation, starting with account and settings behaviour.

- [Design proposal](design-proposal.md)
- [Ahmed's review and next-task handoff](https://github.com/AhmedISatti03/WattWise/blob/6b3cae4/docs/backend/ahmed-review-response-v1.md)
- [Decision log and confirmation questions](decision-log.md)
- [Task-to-handoff mapping](task-mapping.md)
- [Synthetic scenarios and expected outcomes](scenario-definitions.md)
- [Local demonstration scope amendment](scope-amendment.md)
- [Draft frontend API contract](../api/frontend-contract.md)
- [Backend v1.0 handoff](../handoffs/WattWise_Backend_Handoff_Umut_v1.0.md)
- [Frontend v1.0 handoff](../handoffs/WattWise_Frontend_Handoff_Miray_v1.0.md)

Current source inspected: `main` at `261fcb430297c3aa44ecb15e9ddc9db10a61f247`, `dev` at `be54662eba9d813da0fb6374b5d15cec941f6b9e`, frontend foundation at `c569e6b3b3d6649eef7cc7c1b7064a804f2eec76`, consumption helpers at `2bc57fab0460c6a6cac46064838b61f7da5b706f`. These snapshots contain planning documents and separate frontend branches; they do not establish a working backend or an approved contract.

The uploaded Word handoff and the repository's published v1.0 are the starting requirements. The current handoff changes the initial delivery to a laptop-based, persistent, simulated application with assistant integration. The older scope and collector plan retain valuable measurement rules but require the explicit reconciliation proposed here.

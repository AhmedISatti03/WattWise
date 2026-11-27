# WattWise — Smart Energy Manager

WattWise is a household energy management application that helps users understand electricity consumption, estimate spending, anticipate their next bill, and take practical action to stay within a budget.

Developed for **CENG481 — The Agile Professional**, the project combines electricity-bill information, whole-household measurements, and selected appliance readings in one responsive web application. The initial pilot focuses on households in Türkiye, with further development planned for the Final Year Project.

**Project status:** Local backend review increment: runnable health/database scaffold and opt-in synthetic mock API. Shared business contracts remain proposals for review. The frontend foundation is on `feature/task-9-frontend-foundation` in PR #13; the complete integrated demonstration is not yet implemented.

**Supervisor:** Prof. Dr. Kaya Kuru  
**Academic year:** 2026–2027

## MVP features

| Feature | Planned capability |
|---|---|
| Household and tariff setup | Account access, household profile, billing dates, supported Turkish tariff, and spending target. |
| Household and appliance monitoring | Collect power and energy readings from one whole-household monitor and smart plugs for 2–3 appliances. |
| Consumption dashboard | Display household trends, appliance contributions, device status, and calculated other consumption. |
| Cost estimation and forecasting | Estimate spending to date and project the end-of-cycle household bill, with assumptions and data coverage explained. |
| Bill ingestion and confirmation | Extract information from one supported bill format, allow corrections, and provide manual entry as a fallback. |
| Budget alerts | Warn users when projected household spending exceeds their target. |
| Explainable recommendations | Provide practical suggestions supported by consumption patterns and the configured tariff. |

The [MVP scope](docs/mvp-scope.md) defines the detailed requirements, boundaries, and acceptance criteria. It is currently a draft for team review.

## Implementation handoffs

The finalized v1.0 handoffs guide the local demonstration using synthetic readings, persistent household data, and conversational assistant integration.

- [Backend handoff for Umut](docs/handoffs/WattWise_Backend_Handoff_Umut_v1.0.md) · [Word document](docs/handoffs/WattWise_Backend_Handoff_Umut_v1.0.docx)
- [Frontend handoff for Miray](docs/handoffs/WattWise_Frontend_Handoff_Miray_v1.0.md) · [Word document](docs/handoffs/WattWise_Frontend_Handoff_Miray_v1.0.docx)
- [Reading order and coordination](docs/handoffs/README.md)

The handoffs record the current delivery decisions, including Umut's baseline forecasting and Ahmed's assistant and ML responsibilities. Apply them alongside the existing MVP documents. Umut proposes outstanding rules and the shared API contract for confirmation with Ahmed and Miray before the affected implementation. Task references BE01–BE11 and FE01–FE10 will be mapped to GitHub issues during backlog setup.

## How the system fits together

```text
Electricity bill → Extraction → User confirmation → Bill and tariff records
                                                           │
Household monitor → Collection → Consumption records        │
Smart plugs ──────→ Collection → Consumption records        │
                                      │                    │
                                      └─────────┬──────────┘
                                                ↓
                              Cost, forecast, and recommendation logic
                                                ↓
                                         Application API
                                                ↓
                              Dashboard, budget alerts, and guidance
```

These are logical components. They do not require separate deployed services.

The proposed backend stack and pending decisions are recorded in the [backend design proposal](docs/backend/design-proposal.md). Device models and deployment choices remain subject to validation.

## Repository organization

This local increment adds `backend/`, draft contracts in `docs/api/`, and design/review documents in `docs/backend/` alongside the existing planning documents and handoffs. The following broader structure remains a proposal; folders should be introduced when they contain useful work.

```text
WattWise/
├── README.md
├── .gitignore
├── .env.example                 # Configuration names and safe example values
│
├── frontend/                    # Responsive web application
│   ├── src/
│   ├── tests/
│   └── README.md                # Frontend setup and development instructions
│
├── backend/                     # Application API and server-side logic
│   ├── src/
│   │   ├── accounts/            # Accounts and household access
│   │   ├── households/          # Household settings, tariffs, and budgets
│   │   ├── devices/             # Device registration and reading ingestion
│   │   ├── bills/               # Uploads, extraction, and confirmation
│   │   └── analytics/           # Costs, forecasts, alerts, and recommendations
│   ├── migrations/             # Database schema changes
│   ├── tests/
│   └── README.md                # Backend setup and development instructions
│
├── collector/                   # Household-device connectivity
│   ├── src/                     # Device adapters and outbound data delivery
│   ├── tests/
│   └── README.md                # Hardware setup and connection instructions
│
├── tests/
│   └── integration/             # Checks spanning multiple components
│
├── samples/                     # Synthetic or redacted development examples
│
├── scripts/                     # Repeatable development and demo utilities
│
├── deployment/                  # Deployment configuration, once selected
│
├── docs/
│   ├── mvp-scope.md
│   ├── WattWise_Hardware_Comparison.txt
│   ├── architecture/            # System design and technical decisions
│   ├── api/                     # API contracts and example responses
│   ├── hardware/                # Device validation and installation records
│   ├── agile/                   # Iteration plans, reviews, and retrospectives
│   └── evaluation/              # Test plans, results, and analytical evaluation
│
└── .github/
    ├── ISSUE_TEMPLATE/          # Consistent task and bug descriptions
    ├── pull_request_template.md
    └── workflows/               # Automated checks, once configured
```

The analytical modules sit within the backend initially, keeping integration manageable for a three-person team. Device-specific communication belongs in the collector, while shared API fields, units, and timestamp conventions are documented in `docs/api/`.

Real household bills, credentials, and private consumption records must not be committed. Development examples should use synthetic or appropriately redacted data.

## Agile development

We develop WattWise through a prioritised backlog and short iterations. The initial proposal suggests cycles of one to two weeks; the team will confirm the cadence against course deadlines and supervisor feedback.

Each iteration should have a clear goal, selected tasks, a demonstration of completed work, and a retrospective identifying improvements for the next cycle.

### Project board

All team members use the same workflow:

**Backlog → Ready → In Progress → Review / Testing → Done**

| Column | Meaning |
|---|---|
| **Backlog** | Work identified for consideration or later development. Details or dependencies may still be unresolved. |
| **Ready** | Work is clear, prioritised, and has what it needs to begin. |
| **In Progress** | An owner is actively working on the task. |
| **Review / Testing** | The result is ready for review and relevant checks. |
| **Done** | The agreed outcome has been completed and checked. |

Each task has one main owner and a short description of the expected result. Other team members can contribute and help resolve dependencies.

Keep a small amount of work in progress. When a task is blocked, record the reason on its card and inform the team. Work requiring corrections moves from **Review / Testing** back to **In Progress**.

### Proposed contribution workflow

1. Select a task from **Ready** and move it to **In Progress**.
2. Create a short-lived branch, such as `feature/bill-confirmation` or `docs/device-validation`.
3. Implement the agreed outcome and add relevant checks or supporting evidence.
4. Open a pull request linked to the task, explaining the change and how it was verified.
5. Move the task to **Review / Testing** and request a teammate’s review.
6. Merge reviewed work and move the task to **Done** once its acceptance criteria are met.

### Proposed definition of done

A task is complete when:

- Its agreed acceptance criteria are satisfied.
- A teammate has reviewed the result.
- Relevant tests or checks pass, with evidence recorded.
- Related documentation is updated where needed.
- For code changes, the work is integrated into the main branch.
- Any remaining limitations or follow-up tasks are recorded.

## Team responsibilities

| Team member | Primary responsibility |
|---|---|
| **Muhammad Ahmed Satti** | Group lead, technical coordination, coding and integration review; conversational assistant, AI evaluation, and ML forecasting improvements under the v1.0 handoff. |
| **Umut Topatan** | Backend, persistence, ingestion, simulation, calculation services, baseline forecasting, contract proposals, and future hardware integration under the v1.0 handoff. |
| **Miray Pınarbaşı** | Frontend and user experience: onboarding, bill confirmation, dashboards, device status, budget settings, and alert presentation. |

Ownership provides a clear point of responsibility. All members support integration, testing, reviews, documentation, and demonstrations, with workloads reviewed during each iteration.

## Measurement principles

WattWise distinguishes measured consumption, historical bill records, calculated values, monetary estimates, forecasts, and unavailable data.

- **Avoid double counting:** Household measurements already include the monitored appliances. Appliance totals must not be added to the household total.
- **Compare matching periods:** Calculate other consumption only from readings covering comparable intervals.
- **Preserve missing data:** Disconnected devices and missing readings must not appear as zero consumption.
- **Explain estimates:** Costs and forecasts must state their period, assumptions, and available data coverage.
- **Keep recommendations traceable:** Suggestions should be explainable from the readings, tariff, or documented rules that produced them.

Hardware selection remains subject to validation. Whole-household panel installation requires a qualified electrician. See the [hardware comparison](docs/WattWise_Hardware_Comparison.txt) for the current options and integration considerations.

## Validation and evaluation

Evaluation will cover:

- Bill extraction, correction, and confirmation.
- Reliable ingestion, including outages, duplicates, and counter resets.
- Tariff calculations checked against worked examples.
- Forecast performance against observed outcomes when sufficient data is available.
- Budget alerts and recommendation rules.
- Household access separation.
- Dashboard clarity and usability on desktop and phone.
- The complete journey from household setup to readings, forecasts, and guidance.

Test data and recorded demonstration data will be clearly labelled. Detailed methods, results, and limitations will be recorded in `docs/evaluation/` as they are developed.

## Getting started

For this local review increment, follow the [backend setup instructions](backend/README.md). They cover Python 3.12+, SQLite or optional PostgreSQL, explicit migrations, health checks, the synthetic mock API, and tests. These are scaffold instructions, not a claim that the complete household journey is ready.

Start with:

- [MVP scope and acceptance criteria](docs/mvp-scope.md)
- [Hardware comparison and integration considerations](docs/WattWise_Hardware_Comparison.txt)
- [Backend design and decisions](docs/backend/README.md)
- [Draft frontend–backend contract](docs/api/frontend-contract.md)
- [Task-to-handoff mapping](docs/backend/task-mapping.md)

Component setup instructions will be maintained alongside the frontend, backend, and collector as those components are introduced.

## Beyond the MVP

Potential FYP extensions include native mobile applications, additional device models and bill formats, appliance control, advanced forecasting, and conversational energy guidance.

These remain outside the current MVP unless the team agrees and documents a scope change.

## Academic development record

The repository will retain evidence of development decisions, contributions, testing, iteration reviews, and feedback to support the group demonstration and individual critical reports.

AI-assisted development will be acknowledged and justified, and the team will remain responsible for understanding and explaining the submitted work.


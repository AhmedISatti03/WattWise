# WattWise frontend foundation

Local review implementation for [task #9](https://github.com/AhmedISatti03/WattWise/issues/9). The foundation provides routes, a responsive application shell, reusable UI components and labelled sample screens. It is not the completed MVP.

## Tooling proposal

| Tool | Reason |
|---|---|
| React + TypeScript | Reusable components and typed screen/data contracts as frontend and backend develop together. |
| Vite | Development server and a straightforward static production build without requiring a frontend application server. |
| React Router | Main screen routes, active navigation, browser history and direct URL handling. |
| Plain CSS | Responsive layouts and shared design tokens without another styling framework or UI component system. |
| Recharts | React chart components, responsive charts and keyboard support; a textual data table also accompanies the sample chart. |
| Lucide React | Consistent SVG icons; text remains available for navigation and actions. |

This is a **proposal implemented locally for review**, not a recorded agreement with Ahmed. Task #9 requests discussion with Ahmed before the team's implementation choice is adopted. His technology review remains pending; no discussion or approval is claimed. If the stack changes, this local prototype can be revised before uploading.

Alternatives considered: Next.js adds server rendering and hosting decisions not currently required for an authenticated household dashboard; Vue is also viable but would be an alternative to React rather than an additional dependency; Tailwind is optional, but plain CSS keeps the initial toolchain smaller. Chart.js is viable, but Recharts fits the proposed React component model. These are project judgments, not performance benchmarks.

Dependency versions are pinned in `package.json` and `package-lock.json`. `npm ci` uses the tested lockfile. The local implementation was developed with Node 24.19.0 and npm 11.9.0. Use Node 24 LTS (recommended); the declared minimum is Node 22.12.0. Recheck the build when changing runtime versions.

## Run locally

From the repository root after this folder is adopted:

```sh
cd frontend
npm ci
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). During this review the folder is located at `/workspace/drafts/task-9/frontend`, so run these commands from that directory instead.

The dev script binds to all interfaces so a phone on the same trusted LAN can use `http://<computer-lan-ip>:5173`. The phone cannot use the computer's `localhost`. Keep the server on a trusted development network and do not expose it to the public internet. A cloud execution host requires supported forwarding; its loopback URL is not automatically accessible on your laptop.

No API URL, account, hardware, backend, environment file or credentials are needed. Do not enter real passwords or upload household bills into this foundation.

## Build and inspect the production output

```sh
npm run typecheck
npm run build
npm run preview
```

`npm run build` type-checks the source and creates static assets in `dist/`. The preview server normally uses port 4173 and is for inspecting a build, not production hosting.

React Router uses browser history. A future static host must serve `index.html` for application URLs such as `/devices` and `/bills/review`, while serving existing static assets normally. Vite dev/preview support this fallback. Hosting registration and deployment are outside this deliverable. The build assumes hosting at `/`; subpath hosting needs coordinated Vite base and router basename configuration.

## Included routes

| Route | What is implemented |
|---|---|
| `/` | Redirect to `/dashboard`. |
| `/dashboard` | Sample overview with measurements, dated forecast, budget notice, chart, contributions and insight link. |
| `/consumption` | Placeholder page with sample chart and contribution list. |
| `/bills` | Empty bill-list placeholder and navigation to bill entry. |
| `/bills/new` | Upload-area placeholder; file upload intentionally unavailable. |
| `/bills/review` | Disabled provisional bill fields, pending task #3. |
| `/devices` | Fixed sample device/collector statuses, including a stale fridge. |
| `/settings` | Reusable form demonstration with validation; no persistence or dashboard recalculation. |
| `/household/setup` | Setup form demonstration with link to bill entry. |
| `/sign-in`, `/register` | Disabled account forms; no authentication or route protection. |
| `/insights/ac-usage` | Fixed sample recommendation with supporting consumption link. |
| Unknown route or insight | Honest not-found presentation with return navigation. |

All routes remain accessible without authentication because they contain development samples only. Real authentication and authorized household data must be implemented before connecting private records.

## Explore shared UI behavior

The dashboard's **Preview state** selector demonstrates ready, loading, request error, no readings, disconnected plug and insufficient-history states. Loading remains visible until another state is selected. Retry on the simulated error returns to the ready sample view; it makes no network request.

The settings form demonstrates labelled inputs, helper/error associations, positive-budget validation and a status announcement. Its button validates in-memory inputs only. It does not save, affect dashboard values or survive leaving the screen.

Navigation works through React Router, including active desktop/sidebar and phone/bottom links. Settings stays available in the header on phone. The root has a skip link, focus styles and an application-render error boundary. These are foundations for accessibility, not a completed accessibility audit.

## Sample data and measurement meaning

The persistent sample banner identifies a fixed **28 October 2026, 14:30 Europe/Istanbul** snapshot; values do not update with the actual clock.

- Current household power: 820 W; today's energy: 8.40 kWh, partial day.
- Recorded cycle energy: 108.40 kWh. Fictional ₺3.00/kWh yields ₺325.20 estimated energy cost, excluding invoice charges.
- The dated forecast was calculated at 28 October 00:00 from 100 kWh recorded plus 200 kWh projected: ₺900.00 energy cost against the same-cycle ₺800.00 budget. It is not an intraday live forecast or a complete utility invoice.
- Complete-day appliance contributions on 27 October are 4, 1 and 2 kWh, within household total 12 kWh; calculated other consumption is 5 kWh. They are never added on top of the household total.
- Seven synthetic complete daily chart values for 21–27 October total 70 kWh. Missing data is never substituted with zero.
- The disconnected-plug state withholds the fridge's interval value and calculated remainder, retaining unaffected household values. The devices page intentionally shows its own fixed disconnected-device fixture.
- The insufficient-history state is a separate demonstration with 3 of 7 complete days. It suppresses numerical forecast and forecast-based budget claims.

These fixtures exercise presentation, not validated calculations or physical readings. They follow the repository's scope, task #5 screen requirements, energy display rules and insight scenarios. Backend forecasting, interval validity, status thresholds and tariff calculation remain separate work.

## Source organization

```text
frontend/
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── main.tsx                 # Application mount and browser routing
│   ├── App.tsx                  # Layout, navigation, routes and render boundary
│   ├── styles.css               # Shared styles and responsive breakpoints
│   ├── components/
│   │   ├── ui.tsx               # Fields, buttons, panels and UI states
│   │   ├── LazyTrend.tsx        # Load chart code only when used
│   │   └── Trend.tsx            # Sample chart with data-table alternative
│   ├── data/sample.ts           # Explicitly synthetic development fixtures
│   └── pages/
│       ├── Dashboard.tsx
│       └── Placeholders.tsx
└── README.md
```

No generated `dist/` or `node_modules/` directory should be committed. The lockfile should be committed when this proposal is adopted.

## Remaining work and review

- Ahmed: review the framework/styling/charting choice and record the decision before team adoption.
- A teammate: independently follow these setup instructions; an automated check is not independent human setup confirmation.
- Agree API types, then replace synthetic adapters without mixing sample and real households.
- Implement authentication, household setup persistence, tariff configuration, bill processing, live device status, forecasts and recommendations under their own tasks.
- Validate supplier fields after #3 and responsive/accessibility behavior as real screens replace placeholders.

Task #9 does not complete task #5's full screen functionality or task #4's real-device integration.

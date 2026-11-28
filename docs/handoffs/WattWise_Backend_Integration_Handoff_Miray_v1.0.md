# WattWise Backend Integration Handoff for Miray

Version 1.0 · 28 November 2026 · From Umut Topatan to Miray Pınarbaşı

Start with a small review under #19. Run one backend mock request, compare the two period selections, and flag any field or state your screens need. You can send that feedback before starting frontend implementation. [Frontend handoff v1.0](WattWise_Frontend_Handoff_Miray_v1.0.md) · [Screen review #19](https://github.com/AhmedISatti03/WattWise/issues/19)

## 1 What is ready to use

PR #29 provides a local FastAPI service, SQLite setup, health endpoints and opt-in mock routes for the dashboard and devices. The routes serve fixed synthetic snapshots. The full demo will use persisted readings when #17 and #18 are implemented. Account and settings, ingestion, bills and chat routes in the contract are proposals. Use their examples for screen review while the corresponding backend work is pending. [PR #29](https://github.com/AhmedISatti03/WattWise/pull/29) · [Shared contract](../api/frontend-contract.md)

Keep your frontend checkout and the backend review checkout in separate folders. For a fresh backend checkout, run this from a parent folder where `WattWise-backend-review` is available. The reviewed snapshot for this guide is `5e60cbf`.

```sh
git clone --branch review/backend-design-foundation https://github.com/AhmedISatti03/WattWise.git WattWise-backend-review
```

Follow the Windows or macOS/Linux quick start in the backend README from that checkout. Use local SQLite. In `backend/.env` set `WATTWISE_ENABLE_DEMO_API=true` and restart the server. Keep it bound to `127.0.0.1:8100`. Keep `.env`, local database files and credentials out of Git. [Backend setup](../../backend/README.md) · [Reviewed backend snapshot](https://github.com/AhmedISatti03/WattWise/commit/5e60cbf9f789ded413ada0a71a3cc405ea29e686)

## 2 First connection check

Open `/api/v1/health/live` and `/api/v1/health/ready` on `http://127.0.0.1:8100`. Both should return 200 once the service is running and the migration has been applied. Readiness 503 points to local database setup. If health succeeds and the mock route returns 404, check the branch, route and opt-in flag, then restart.

For a first check without starting the frontend, open the two mock URLs in your browser. The JSON field `selectedPeriodEnergy.value` should be 70 for the week and 12 for the day. [Normal week](http://127.0.0.1:8100/api/v1/demo/overview?scenario=normal) · [Normal day](http://127.0.0.1:8100/api/v1/demo/overview?scenario=normal&start=2026-10-27T00:00:00%2B03:00&endExclusive=2026-10-28T00:00:00%2B03:00&resolution=day)

From the frontend Vite page at `http://localhost:5173` or `http://127.0.0.1:5173`, run this in the browser console. Start Vite from the frontend checkout with `npm ci` and `npm run dev` in `frontend/`.

```js
const url = new URL('http://127.0.0.1:8100/api/v1/demo/overview')
url.search = new URLSearchParams({ scenario: 'normal' })
const response = await fetch(url, { credentials: 'omit' })
const body = await response.json()
console.log(response.status, body.meta.requestId, body.selectedPeriodEnergy)
```

Expect 200 with 70 kWh. For the one-day selection, add `start=2026-10-27T00:00:00+03:00`, `endExclusive=2026-10-28T00:00:00+03:00` and `resolution=day` as keys and values in `URLSearchParams` so the offset is encoded correctly. The default selection is 21–28 October 2026 in Europe/Istanbul, with midnight boundaries and an exclusive end. The one-day selection ends at the same instant. If the browser blocks the request, confirm the exact Vite origin and ask me about any custom port. [Mock routes and query options](../api/frontend-contract.md#7-public-development-mock-implemented-boundary)

## 3 Keep the API boundary intact

- **Use one frontend data-access layer.** The foundation dashboard uses `frontend/src/data/sample.ts`. The consumption branch has a fixture-only `frontend/src/data/dashboardApi.ts`. Inspect both during #19. Under #20, keep one shared adapter and an explicit local fixture mode. Put the base URL and query encoding in the adapter so screens use the same response shape. [Foundation PR #13](https://github.com/AhmedISatti03/WattWise/pull/13) · [Consumption branch](https://github.com/AhmedISatti03/WattWise/tree/feature/consumption-dashboard) · [Frontend integration #20](https://github.com/AhmedISatti03/WattWise/issues/20)
- **Render the server’s numbers.** Read the selected total from `selectedPeriodEnergy` and use the matching `trend` and `contributions` from the same response. The household total already includes the appliances. Use the supplied remainder, shares, coverage and eligibility. Frontend helpers can format units and dates. Current power, today’s energy and the billing-cycle cards each keep their own periods.
- **Apply only the latest selection.** Abort superseded requests or discard their successes and errors. Update the chart, total and contributions together. A valid zero displays as zero. A null value uses its unavailable reason. Loading, empty, partial coverage, stale readings and request failure each need a distinct screen state. Keep synthetic labels and snapshot times visible.
- **Keep future settings tied to the server result.** Show save success after confirmation and preserve the draft on failure. Keep affected comparisons pending or unavailable until results match the saved settings revision and charge basis. Use `setupCompleteness` to show what can be filled in. The static incomplete-setup example is available for screen work. The mock scenario query supports the five cases below. [Incomplete setup example](../api/examples/v0.1/settings/incomplete-setup.json)

If a screen needs a different field, status or query range, send me the screen, current response and expected behavior. We can agree on a contract update before changing the shared schema, mock fixtures, backend routes or migrations. Keep account cookies, collector credentials and provider keys out of the public mock integration.

## 4 Quick acceptance checks

| Check | Expected result |
| --- | --- |
| Normal week | 70 kWh household. Appliances 24, 7 and 13 kWh. Other 26 kWh. Trend and breakdown cover the same seven days. |
| Normal day | 12 kWh household. Appliances 4, 1 and 2 kWh. Other 5 kWh. Present power stays 820 W and today stays 8.4 kWh. Cycle values also stay the same. |
| Rapid selection | Request the week with `delay_ms=1500`, then switch immediately to the day. After both requests settle, the day chart, 12 kWh total and day breakdown are visible. |
| Empty and partial | `empty` returns 200 with unavailable measurements. `partial-data` returns 200 with 6.4 kWh recorded today and partial coverage. |
| Disconnected and error | `device-disconnected` preserves usable household energy and withholds the missing fridge contribution and remainder. `error` returns 503 with retry guidance. A request failure leaves device status unknown or previously recorded. |

For device status, use `GET /api/v1/demo/devices` with the same `scenario`. If a request fails, record the route, query, HTTP status and `meta.requestId` from the response when available. A screenshot and the failing response are enough for the first report. [Dashboard examples](../api/examples/v0.1/)

## 5 Where to leave feedback

1. **#19 and #11.** Send the screen or component, the field or state you checked, and anything missing. Include one example response if it helps. I’ll coordinate changes to the backend contract with you and Ahmed. [Contract review #11](https://github.com/AhmedISatti03/WattWise/issues/11)
2. **#12 and #22.** Record the normal, missing-data and failure checks you ran. Include evidence for rapid period switching once the UI supports it. You can work on labelled fixtures while the shared adapter and live consumption routes are being prepared. [Mock review #12](https://github.com/AhmedISatti03/WattWise/issues/12) · [Dashboard #22](https://github.com/AhmedISatti03/WattWise/issues/22)
3. **#20.** After the initial screen and tooling review, connect the shared adapter to the running mock and run `npm run typecheck` and `npm run build`. Ahmed’s #30 review covers the outstanding backend behavior, starting with sessions and settings for #16. [Backend follow-up #30](https://github.com/AhmedISatti03/WattWise/issues/30)

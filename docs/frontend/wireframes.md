# WattWise — Low-fidelity Wireframes

**Task:** #5 · **Date:** 28 October 2026 · **Status:** Local review draft  
Read alongside [screen requirements](screen-requirements.md). All numbers are synthetic samples. Controls are sketches, not functioning application UI.

## W01 — First-time and returning journeys

```text
Create account / Sign in
           |
           +-- Existing household ------------------------+
           |                                              |
           +-- New household                              |
                Household + dates                         |
                Tariff + target (or finish later)          |
                         |                                |
                  Add bill / enter manually                |
                         |                                |
                  Check fields → Confirm                   |
                         |                                |
                         +-------- DASHBOARD <-------------+
                                     |
             +-----------------------+----------------------+
             |              |               |               |
           Usage          Bills           Devices        Settings
             ^                              ^               ^
             +---- Insight → relevant action+---------------+
```

Device setup can proceed independently. Finishing setup later opens an incomplete dashboard with next steps; it does not create readings or mark the missing step complete.

## W02 — Account access (S01)

```text
+------------------------------------------------------+
| WATTWISE                                             |
| Understand your home's energy use                    |
|                                                      |
| Sign in                                              |
| Email       [                                     ]  |
| Password    [                              ][Show]   |
| [Sign in]                                            |
| New to WattWise? Create account                      |
|                                                      |
| Form error appears here with recovery guidance.      |
+------------------------------------------------------+
```

Create account uses the same layout with password confirmation. On phone the form fills the available width. No device/energy data appears before sign-in.

## W03 — Household setup (S02)

```text
+------------------------------------------------------+
| WATTWISE                      Household setup        |
| 1 Household → 2 Bill confirmation → 3 Overview        |
|                                                      |
| Household name  [My home                           ] |
| Timezone        [Europe/Istanbul                 v] |
| Billing period  [Start date]  [End date]             |
| Tariff          [Choose supported arrangement    v] |
|                 [Validated rate/charge inputs]       |
| Budget (TRY)    [                              ]     |
| A target for this billing cycle.                     |
|                                                      |
| [Save and continue]     [Finish missing steps later] |
| Next: confirm a bill; register monitoring devices.   |
+------------------------------------------------------+
```

Dates and labels follow the confirmed supplier/household convention. Phone places paired fields on separate rows. Invalid fields show inline explanations.

## W04 — Bills and upload (S03)

```text
+------------------------------------------------------+
| Navigation | Bills — historical records              |
|            | [Add bill]                              |
|            | Period       Consumption    Amount      |
|            | Confirmed bills / No bills yet           |
|            |-----------------------------------------|
|            | Add electricity bill                    |
|            | [Choose photo or PDF]                   |
|            | Accepted format/size from service        |
|            | Selected file: example.pdf  [Remove]     |
|            | [Upload and review]                     |
|            | [Enter bill manually instead]           |
+------------------------------------------------------+
```

Upload → processing status → W05. Unsupported format or unreadable extraction shows its reason and manual-entry option. Phone bill rows become labelled cards.

## W05 — Review and confirm a bill (S04)

```text
+------------------------------------------------------------+
| Back to Bills             Review before saving              |
|--------------------------+---------------------------------|
| Bill preview             | Billing start  [              ] |
|                          | Billing end    [              ] |
| Reference image / PDF    | Consumption    [        ] kWh   |
| where supported          | Invoice total  [        ] TRY   |
|                          | Supplier       [              ] |
|                          | Tariff text    [              ] |
|                          | ! Check uncertain fields        |
|--------------------------+---------------------------------|
| Provisional fields: supplier mapping will follow task #3.    |
| Historical bill data; does not replace live readings.        |
| [Confirm and save]                  [Back to upload]        |
+------------------------------------------------------------+
```

Phone: editable fields first, followed by **Show bill preview**. Manual entry uses the same confirmation form without extraction claims. Charges/taxes appear only after the selected bill layout is agreed.

## W06 — Desktop dashboard (S05)

See also [desktop/phone comparison image](wireframes/dashboard-overview.svg).

```text
+--------------------------------------------------------------------------------+
| WATTWISE     My home     Cycle 18 Oct–16 Nov 2026      Settings / Account        |
|------------+-------------------------------------------------------------------|
| Dashboard  | SAMPLE DATA — not real household measurements                     |
| Usage      | Snapshot: 28 Oct 2026, 14:30 Europe/Istanbul                       |
| Bills      |-------------------------------------------------------------------|
| Devices    | Current household power        Today's household energy            |
| Settings   | 820 W · Measured 14:30          8.40 kWh · Today — partial day       |
|            |-------------------------------------------------------------------|
|            | Estimated energy cost so far | Full-cycle energy-cost forecast    |
|            | ₺325.20 · through 14:30       | ₺900.00 · Early estimate           |
|            |                              | Calculated 28 Oct, 00:00            |
|            | Budget: ₺800.00 (same cycle)  | Projected overspend: ₺100.00        |
|            | Forecast to go over budget · [View usage] [Edit budget]            |
|            | Fictional rate; energy charges only. [Basis and limitations]      |
|            |-------------------------------------------------------------------|
|            | Household trend [Daily / Weekly]                                  |
|            | kWh  [dated bars; gaps and partial current day explicitly marked]  |
|            | [Show data table]                                                  |
|            |-------------------------------------------------------------------|
|            | Contributions — YESTERDAY, 27 OCT (complete matching day)          |
|            | Household total: 12.00 kWh                                         |
|            |   AC 4.00 | Fridge 1.00 | Dishwasher 2.00 | Other 5.00              |
|            |   Measured appliance contributions        Calculated remainder    |
|            | Already included in household total. [Inspect consumption]         |
|            |-------------------------------------------------------------------|
|            | Recommendations: AC was largest MONITORED contributor yesterday. |
|            | 4.00 kWh of 12.00 kWh ≈ 33%. [See evidence and suggestion]          |
+--------------------------------------------------------------------------------+
```

The current cost and dated forecast show their different calculation times. This avoids inventing an intraday forecast rule. Yesterday's contributions have their own clear period. No illustrative daily chart bars imply an invented historical dataset.

## W07 — Phone dashboard (S05)

```text
+--------------------------------------+
| WATTWISE                  [Settings] |
| My home · 18 Oct–16 Nov 2026          |
| SAMPLE DATA — not real measurements   |
| Snapshot: 28 Oct, 14:30 · Istanbul    |
|--------------------------------------|
| Current household power              |
| 820 W · Measured at 14:30             |
| Today's household energy             |
| 8.40 kWh · Today — partial day        |
|--------------------------------------|
| YOUR BILLING CYCLE                    |
| Energy cost so far  ₺325.20           |
| Through 14:30                        |
| Forecast energy cost ₺900.00         |
| Early estimate · calculated 00:00     |
| Budget ₺800.00                       |
| Forecast to go over by ₺100.00        |
| [View usage]  [Edit budget]           |
| Sample tariff; energy charges only   |
| [Basis and limitations]              |
|--------------------------------------|
| Household trend [Daily / Weekly]      |
| [Chart with gaps and partial labels] |
| [Show data table]                    |
|--------------------------------------|
| YESTERDAY · 27 OCT                   |
| Household total        12.00 kWh      |
| Included appliance contributions:    |
| AC                      4.00 kWh     |
| Fridge                  1.00 kWh     |
| Dishwasher              2.00 kWh     |
| Other — calculated      5.00 kWh     |
| [Inspect consumption]                |
|--------------------------------------|
| Recommendations                      |
| AC: largest monitored contributor   |
| yesterday. [See evidence]            |
|--------------------------------------|
| Home       Usage      Bills  Devices |
+--------------------------------------+
```

Full page scrolls; bottom navigation must not cover the last card or focused form fields. No large table requires horizontal scrolling.

## W08 — Usage and appliance detail (S06)

```text
+------------------------------------------------------+
| Usage                                                |
| Scope: [Household / AC / Fridge / Dishwasher]         |
| Period: [27 October 2026]     [Daily / Weekly]        |
| SAMPLE DATA                                          |
| AC · 4.00 kWh · Measured over complete selected day  |
| 33.33% of matching household energy (12.00 kWh)       |
| Estimated energy cost ₺12.00 · sample flat tariff    |
| [Chart: dated intervals; visible coverage/gaps]      |
| [Show data table] [Device status]                    |
| Included within household total, not added to it.    |
+------------------------------------------------------+
```

Phone stacks selectors and summary cards. If coverage is incomparable, replace the share with its unavailable reason; do not keep an old percentage.

## W09 — Device status (S07)

```text
+------------------------------------------------------+
| Devices                          [Refresh status]   |
| SAMPLE DATA                                          |
| Collector · last contact 14:30                       |
| Delivery current · pending count 0, reported 14:30  |
|------------------------------------------------------|
| HOUSEHOLD MONITOR                                    |
| Home monitor · Reporting · last measurement 14:30    |
|------------------------------------------------------|
| APPLIANCE PLUGS                                      |
| AC          Reporting     Last measurement 14:30    |
| Fridge      Stale         Last measurement 14:20    |
| Dishwasher  Reporting     Last measurement 14:30    |
| Fridge readings may be incomplete.                  |
| Check plug power and Wi-Fi. [Setup guidance]         |
+------------------------------------------------------+
```

This is a disconnected-device variant, separate from the fully comparable daily example. Phone presents each source as a card. No switch/power-control buttons.

## W10 — Settings and insight detail (S08, S09)

```text
+----------------------------+-------------------------------+
| HOUSEHOLD SETTINGS         | INSIGHT DETAIL                |
| Name [My home]             | SAMPLE DATA                   |
| Timezone [Istanbul]        | Forecast to go over budget    |
| Billing dates [..] [..]    | Estimated energy cost ₺900.00  |
| Tariff [supported fields]  | Target ₺800.00, same cycle     |
| Budget [800.00] TRY        | Projected difference ₺100.00   |
| User-set target            | Calculated 28 Oct at 00:00     |
| [Save changes] [Cancel]    | Seven valid days; assumptions  |
| Estimates recalculate      | and excluded charges shown.   |
| after relevant changes.    | [View consumption]            |
| [Sign out]                 | [Back to dashboard]           |
+----------------------------+-------------------------------+
```

These are two separate screens, shown side by side for comparison. On phone each uses a single column. Recommendation detail uses the same evidence/action hierarchy. A stale or resolved insight is marked no longer current.

## W11 — State sketches

```text
NO READINGS                       INSUFFICIENT HISTORY
No household readings yet         Getting to know your home
Power —                           3 of 7 complete days collected
Energy —                          Forecast —
[View device setup]               Earlier cycle coverage also required.

LOADING                           REQUEST ERROR
[Labelled metric skeleton]        Could not refresh household energy.
Loading household energy…         Last known value/time if available.
                                  [Retry] [View other available sections]

PARTIAL CYCLE                     INVALID COMPARISON
Recorded energy 50.00 kWh          Other consumption unavailable.
Only cycle days 11–15              Readings need checking.
Observed-period energy cost       [Inspect data / device status]
₺150.00 · SAMPLE tariff
Earlier cycle missing; forecast —

STALE POWER                       BILL FAILURE
Last recorded power: 120 W        We could not read this bill.
Fridge · last seen 14:20           [Try another file] [Enter manually]
Value is not current.
[Device status]
```

All state fixtures are explicitly samples. The production UI uses actual validity decisions and timestamps. A real zero is displayed as zero with its measurement context; it is not styled as missing.

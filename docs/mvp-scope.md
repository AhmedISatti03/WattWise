# WattWise — MVP Scope

**Status:** Draft MVP specification for team review.  
**Updated:** 20 October 2026  
**Supervisor:** Prof. Dr. Kaya Kuru

## 1. Product goal

WattWise helps households understand electricity consumption, estimate spending, anticipate their next bill and take practical action to stay within a budget. The MVP combines confirmed electricity-bill information, measured whole-household consumption and readings from selected appliances in one responsive web application.

This document is the authoritative specification of WattWise’s MVP features and boundaries.

## 2. Whole-household monitoring

Whole-household monitoring is a core MVP feature, alongside smart-plug monitoring of 2–3 appliances. Together, they provide measured household totals and visibility into selected appliance contributions.

The pilot will use one suitable clamp-based whole-household energy monitor installed by a qualified electrician and one compatible smart-plug model. The monitor must cover the complete pilot household supply. Its model, phase configuration, current rating, installation location and data-access method remain to be validated before purchase.

## 3. Ranked MVP features

All seven features are included. This proposed priority ranking guides implementation and trade-offs; it is not a mandatory sequential workflow. Independent work can proceed in parallel. The ranking requires team review.

| Priority | Feature | Notes |
| --- | --- | --- |
| 1 | Household and tariff setup | Account, billing period, supported tariff and household budget. |
| 2 | Whole-household and appliance monitoring | Household clamp monitor plus smart plugs for 2–3 appliances. |
| 3 | Consumption dashboard | Household trends, appliance contributions and calculated other consumption. |
| 4 | Cost estimation and forecasting | Estimated spending to date and projected household bill. |
| 5 | Bill ingestion and confirmation | Photo/PDF extraction, editable fields and manual-entry fallback. |
| 6 | Budget alerts | In-app warnings when projected household spending exceeds the target. |
| 7 | Explainable recommendations | Practical rules-based suggestions supported by usage and tariff data. |

Bill ingestion remains mandatory despite its delivery priority. Tariff information can initially be entered manually while monitoring and calculations are developed.

### 3.1 Household and tariff setup

**User outcome:** A user can configure the household and the information required for meaningful energy and cost reporting.

**Included:**

- Account access and one household profile per account.
- Billing-cycle dates and a household spending target.
- One supported, validated Turkish tariff arrangement, with applicable charges documented.
- Association of the household monitor and named monitored appliances with the correct household.
- Editable settings with input validation.

**Complete when:** Settings can be saved and retrieved; invalid inputs are explained; household data is separated between accounts; calculations use the configured tariff and period.

### 3.2 Whole-household and appliance monitoring

**User outcome:** A user can see total household consumption and the contribution of selected appliances.

**Included:**

- One suitable clamp-based monitor covering the whole household supply.
- Smart-plug monitoring of 2–3 appliances using one compatible plug model.
- Collection and storage of timestamped power (W) and energy (kWh) readings, with device identifiers and measurement scope.
- Visible device status, last-update time and missing-data periods.
- Handling of duplicate readings and energy-counter resets without silently corrupting totals.

**Complete when:** Real readings from the household monitor and selected plugs reach storage and the application; units and timestamps are consistent; outages and gaps remain visible; the team has checked readings against device records or other suitable reference readings over matching periods.

**Dependency:** Verify household supply type, ratings, enclosure space, installation access, appliance compatibility and usable device interfaces. Use a qualified electrician for panel installation. No specific product is approved yet.

### 3.3 Consumption dashboard

**User outcome:** A user can understand household usage and how monitored appliances contribute to it.

**Included:**

- Current household power and today's household energy consumption.
- Daily and weekly consumption trends.
- Individual monitored-appliance readings and contributions.
- A separately labelled calculated remainder for other consumption.
- Clear labels for measured values, calculated values, estimates and unavailable data.
- Responsive layouts for desktop and phone, with loading, empty and error states.

**Complete when:** Dashboard values agree with backend outputs; time periods and units are visible; appliance totals are not added to the household total; insufficient data is explained; essential screens are usable on desktop and phone.

### 3.4 Cost estimation and forecasting

**User outcome:** A user can see estimated household spending so far and an estimated end-of-cycle bill.

**Included:**

- Household cost calculations based on measured household energy and the supported tariff.
- An initial explainable forecasting baseline using available household history.
- Separately displayed estimated costs for monitored appliances, with allocation assumptions stated where tariff charges cannot be directly assigned.
- Forecast period, data coverage, assumptions and insufficient-data status.
- Explicit treatment of a partially observed billing cycle, including gaps or monitoring that started mid-cycle.

**Complete when:** Cost calculations pass worked examples for the supported tariff; forecasts can be reproduced from documented inputs; historical measurements and future estimates are visibly distinct; the forecasting method and its limitations are documented and evaluated against observed outcomes when available.

No fixed accuracy claim is made before evaluation. Metered consumption does not make a future bill a measured value or guarantee an exact match with the utility invoice.

### 3.5 Bill ingestion and confirmation

**User outcome:** A user can capture historical bill information without entering every field manually.

**Included:**

- Photo or PDF upload for one selected supplier's bill format.
- An existing OCR capability to extract consumption, billing dates and relevant charges.
- Editable extracted fields with validation and user confirmation before saving.
- Manual-entry fallback for unreadable or unsupported input.

**Complete when:** Supported samples can be processed; extraction errors can be corrected; confirmed records are saved; unreadable files and upload failures have understandable responses. Historical bill consumption is not presented as live meter data.

Bill processing must collect only necessary information and protect personal data. Original-upload retention must be defined.

### 3.6 Budget alerts

**User outcome:** A user can recognise a risk of exceeding the household spending target before the billing cycle ends.

**Included:**

- In-app alerts when forecast household spending exceeds the household target.
- An explanation of the forecast, target, period and projected overspend.
- Identification of monitored-appliance contributions where matching readings support it.
- Appropriate insufficient-data handling; no unsupported attribution of the unmonitored remainder to a named appliance.

**Complete when:** Above-target, below-target and insufficient-data scenarios behave as intended; target and forecast cover the same household and period; alert explanations match the inputs. Test scenarios are clearly labelled.

### 3.7 Explainable recommendations

**User outcome:** A user receives practical suggestions supported by the available energy data.

**Included:**

- A small set of tested rules addressing projected overspending, sustained unusual consumption and relevant usage patterns.
- Scheduling suggestions only where the configured tariff actually offers cheaper periods.
- Supporting context identifying the readings or assumptions behind each suggestion.
- Explicit limitations when data is incomplete.

**Complete when:** The team can explain and reproduce why each recommendation appears; test cases verify the rules; suggestions are understandable and do not claim to diagnose electrical faults or guarantee savings.

Custom model training is not required for this feature. More sophisticated ML requires sufficient data and evidence that it improves on the baseline.

## 4. Measurement and estimation rules

| Category | Meaning | Example label |
| --- | --- | --- |
| Measured household consumption | Energy recorded by the whole-household monitor | Measured household energy: 12 kWh |
| Measured appliance consumption | Energy recorded by an appliance's smart plug | Measured AC energy: 4 kWh |
| Historical bill consumption | Consumption recorded on a confirmed bill for a past period | Previous billing-period consumption |
| Calculated remainder | Household energy minus monitored-appliance energy over matching periods | Other consumption — calculated remainder |
| Estimated monetary cost | Tariff-based calculation, with charge assumptions stated | Estimated household cost so far |
| Forecast | Projected future consumption or spending | Estimated end-of-cycle bill |
| Unavailable data | Missing readings or insufficient evidence for a value | Data unavailable / insufficient data |

### No double counting

The household monitor's total already includes the monitored appliances. Never add plug readings to the household total.

For a common period with adequate data: household energy of 12 kWh minus AC energy of 4 kWh and fridge energy of 1 kWh leaves a calculated remainder of 7 kWh. This remainder does not identify individual unmonitored appliances.

### Comparable periods and data quality

Use matching intervals and consistent units before comparing totals. Missing readings are not zero consumption. The remainder can reflect measurement error, timing differences and data gaps as well as other loads; flag unreliable or negative results rather than presenting them as certain usage. Explain any interpolation or other estimation separately.

A household budget must be compared with a household forecast for the same billing period. Do not present a partial cycle as a fully measured cycle. Treat uncertainty transparently without inventing a numerical confidence interval.

## 5. MVP boundaries

The MVP includes one responsive web application, one household per account, one pilot household installation, one supported bill format, one validated tariff arrangement, one household-monitor model and one smart-plug model for 2–3 appliances.

Outside this MVP:

- Separate native mobile applications.
- Automatic appliance switching or shutoff.
- Multiple bill formats, meter models or plug brands.
- QR ingestion unless separately approved after verifying useful accessible bill data.
- Conversational LLM integration.
- Custom model training or fine-tuning as a delivery requirement.
- Automatic identification of unmonitored appliances from aggregate readings.
- Confirmed electrical-fault diagnosis.
- Claims of achieved annual savings without a valid baseline and observation period.

## 6. Complete-MVP acceptance

The complete MVP must support this integrated user journey:

Create an account and household → confirm tariff, dates and target → upload and confirm a bill → view real household and appliance readings → inspect estimated costs and a household forecast → receive understandable budget alerts and recommendations.

- [ ] All seven features satisfy their completion criteria.
- [ ] Whole-household monitoring and 2–3 appliance integrations operate together.
- [ ] Measured, calculated, historical, estimated and unavailable values are clearly distinguished.
- [ ] Household totals and appliance contributions are not double counted.
- [ ] Cost calculations are checked and forecasting limitations documented.
- [ ] Device outages, missing data and relevant input errors are handled visibly.
- [ ] Accounts separate household data and the interface works on desktop and phone.
- [ ] The integrated journey is demonstrated, with simulated/test data explicitly identified.

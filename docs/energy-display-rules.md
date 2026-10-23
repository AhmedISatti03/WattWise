# WattWise — Energy Display Rules

**Status:** Draft for team review  
**Related task:** [#7](https://github.com/AhmedISatti03/WattWise/issues/7)  
**Scope reference:** [MVP scope](mvp-scope.md)

## 1. Purpose

This document defines the energy and cost values displayed in WattWise, their units and periods, and how incomplete data should appear.

All examples below use **synthetic sample data**. The illustrative rate of **₺3.00/kWh** is for checking calculations only; it is not a verified electricity tariff.

## 2. Dashboard values

| Display label | Meaning | Unit and period | Classification |
|---|---|---|---|
| Current household power | The latest valid power reading from the whole-household monitor. | W or kW, with reading time | Measured |
| Today’s household energy | Household electricity consumed from local midnight to the latest available reading. | kWh, today so far | Measured, or partial if coverage is incomplete |
| Appliance energy | Electricity consumed by a named appliance, recorded by its smart plug. | kWh, selected period | Measured |
| Other consumption | Household energy minus the energy of monitored appliances over the same period. | kWh, selected period | Calculated remainder |
| Estimated household cost so far | Estimated cost of recorded household consumption using the configured tariff and documented charge rules. | TRY (₺), billing cycle to date—or explicitly stated observed period | Estimated |
| Estimated end-of-cycle bill | Forecast household spending for the complete configured billing cycle. | TRY (₺), full billing cycle | Forecast |
| Household budget | The spending target entered by the user. | TRY (₺), same billing cycle as the forecast | User-set target |

**Power and energy are different:** power describes how quickly electricity is being used at a particular moment; energy describes how much has been consumed over a period.

For example, an appliance using a constant **1 kW for 2 hours consumes 2 kWh**. A single power reading cannot establish the appliance’s energy consumption for the whole day.

## 3. Time periods and presentation

- Use the household’s configured timezone. For the Türkiye pilot, use `Europe/Istanbul`.
- “Today” means local midnight until now.
- Daily charts show calendar days. Label the current day **“Today — partial day.”**
- A weekly view shows seven labelled calendar dates, making any partial current day clear.
- Billing calculations use the configured billing-cycle boundaries, not an assumed calendar month.
- Store period boundaries consistently: include the start instant and exclude the end instant to avoid counting readings twice.
- Compare household and appliance values only over matching periods.
- Display energy to two decimal places and money to two decimal places. Calculate using unrounded values, then round for display.
- Show the last-update time beside live readings.
- Clearly mark demonstration screens **“Sample data.”**

## 4. Worked example: household and appliance energy

**Period:** One complete calendar day. All readings cover that same day.

| Measurement | Energy |
|---|---:|
| Whole household | 12.00 kWh |
| Air conditioner | 4.00 kWh |
| Fridge | 1.00 kWh |
| Dishwasher | 2.00 kWh |

**Monitored-appliance total:**

`4 + 1 + 2 = 7 kWh`

**Other consumption:**

`12 − 7 = 5 kWh`

The dashboard displays:

- **Household energy:** 12.00 kWh
- **Monitored appliances:** 7.00 kWh
- **Other consumption — calculated remainder:** 5.00 kWh

The household total is **12 kWh**, not 19 kWh. The household monitor already includes the monitored appliances.

The remainder does not identify individual unmonitored appliances. Timing differences and measurement error can also affect it.

## 5. Worked example: estimated cost

For this example only, assume a flat energy rate of **₺3.00/kWh**, with no additional charges.

| Item | Calculation | Estimated energy cost |
|---|---|---:|
| Household | 12 × ₺3.00 | ₺36.00 |
| Air conditioner | 4 × ₺3.00 | ₺12.00 |
| Fridge | 1 × ₺3.00 | ₺3.00 |
| Dishwasher | 2 × ₺3.00 | ₺6.00 |
| Other consumption | 5 × ₺3.00 | ₺15.00 |

Appliance costs are contributions within the household cost. They must not be added to it again.

For real operation, the supported tariff must define applicable rates, charges and taxes. If the calculation excludes invoice components, label it **“Estimated energy cost”** and explain the exclusions.

Appliance cost allocation under tiered tariffs or shared charges requires an explicit allocation rule.

## 6. Proposed initial forecasting rule

For the initial baseline:

- Use the average daily household energy from up to the latest seven complete, valid days within the current billing cycle.
- Require at least seven complete, valid days before displaying a numerical forecast.
- Exclude incomplete days from the average; never treat missing periods as zero.
- For the initial implementation, withhold the full-cycle bill forecast when elapsed billing-cycle energy is incomplete. A later documented method may estimate that missing portion separately.
- Explain that the forecast assumes recent consumption patterns continue.

The seven-day minimum is a **proposed product rule**, not a claim that seven days guarantees accuracy.

### Worked example

At the end of day 10 in a 30-day billing cycle:

| Input | Value |
|---|---:|
| Measured household energy for the first 10 days | 100 kWh |
| Measured energy over the latest seven complete days | 70 kWh |
| Remaining days | 20 |
| Illustrative flat rate | ₺3.00/kWh |
| Household budget | ₺800 |

Calculations:

- Average daily energy: `70 ÷ 7 = 10 kWh/day`
- Forecast remaining energy: `10 × 20 = 200 kWh`
- Forecast full-cycle energy: `100 + 200 = 300 kWh`
- Estimated cost so far: `100 × ₺3.00 = ₺300`
- Estimated end-of-cycle bill: `300 × ₺3.00 = ₺900`
- Projected overspend: `₺900 − ₺800 = ₺100`

Suggested dashboard explanation:

> Your estimated bill is ₺900, which is ₺100 above your ₺800 budget. This forecast assumes your recent average of 10 kWh per day continues.

Real billing forecasts must apply the supported tariff rules, rather than always multiplying by one flat rate.

## 7. Missing, partial and unreliable data

| Situation | Display behaviour |
|---|---|
| No household readings yet | Show **“No household readings yet”**, not 0 kWh. |
| Latest power reading is stale | Show **“Last recorded power”** with its timestamp and stale/offline status. Do not present it as current. |
| Household energy coverage is incomplete | Show the known amount as **“Recorded energy — partial data”**, with the observed period and gaps. |
| A smart plug has missing energy data | Mark that appliance’s value as partial or unavailable. Withhold the full-period remainder unless matching totals are reliable. |
| Monitoring began midway through the billing cycle | Show energy and estimated cost **since monitoring started**. Do not label them as complete cycle-to-date totals. |
| Fewer than seven valid complete days are available | Show **“Not enough history to estimate your bill yet.”** |
| Tariff information is missing | Show energy normally; display **“Add tariff information to estimate costs.”** |
| Calculated remainder is negative | Show **“Other consumption unavailable — readings need checking.”** Do not silently replace it with zero. |
| Forecast is unavailable | Show the budget, but no numerical projected overspend or assertion that the household is within budget. |

A missing transmission does not always mean missing energy. Valid cumulative energy-counter readings before and after a gap may establish the total across that interval, provided no reset or rollover occurred. They do not reveal the usage pattern inside the gap.

**Partial-cycle example:** Monitoring starts at the beginning of day 11. At the end of day 15, it has recorded 50 kWh.

Display:

> Recorded household energy: 50.00 kWh, days 11–15.  
> Estimated energy cost for this observed period: ₺150.00.  
> Full-cycle bill forecast unavailable: earlier consumption is missing.

## 8. Review checklist

- [ ] Every value has a definition, unit and time period.
- [ ] Worked calculations are internally consistent.
- [ ] Household totals and appliance contributions are not double counted.
- [ ] Missing or unreliable data never silently becomes zero.
- [ ] Measured values, calculated remainders, costs and forecasts are distinguishable.
- [ ] Miray has reviewed the labels and explanations.
- [ ] Umut has checked that the required inputs can be provided.
- [ ] The team has agreed on the initial forecasting rules.

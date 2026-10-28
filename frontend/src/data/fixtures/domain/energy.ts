// Dashboard energy calculations. Framework-independent; see docs/energy-display-rules.md.
 
export type UnavailableReason =
  | "no_readings"
  | "period_mismatch"
  | "incomplete_interval"
  | "invalid_remainder";
 
export type CalculatedValue =
  | { value: number; unavailableReason: null }
  | { value: null; unavailableReason: UnavailableReason };
 
// Household energy already includes monitored appliances, so the remainder is a
// subtraction, never an addition. Missing readings are not zero.
export function calculateOtherConsumption(
  householdKwh: number | null,
  applianceKwh: Array<number | null>,
): CalculatedValue {
  if (householdKwh === null) {
    return { value: null, unavailableReason: "no_readings" };
  }
  if (applianceKwh.some((v) => v === null)) {
    return { value: null, unavailableReason: "period_mismatch" };
  }
  const appliancesTotal = (applianceKwh as number[]).reduce((sum, v) => sum + v, 0);
  const remainder = householdKwh - appliancesTotal;
  if (remainder < 0) {
    return { value: null, unavailableReason: "invalid_remainder" };
  }
  return { value: remainder, unavailableReason: null };
}
 
// Share of the household total, as a percentage. A zero household total has no share.
export function householdSharePercent(partKwh: number | null, householdKwh: number | null): number | null {
  if (partKwh === null || householdKwh === null || householdKwh === 0) {
    return null;
  }
  return (partKwh / householdKwh) * 100;
}
 
const UNAVAILABLE = "—";
 
// Round only for display; calculations above use unrounded values.
export function formatKwh(value: number | null): string {
  return value === null ? UNAVAILABLE : `${value.toFixed(2)} kWh`;
}
 
export function formatTry(value: number | null): string {
  return value === null ? UNAVAILABLE : `₺${value.toFixed(2)}`;
}
 
export function formatPercent(value: number | null): string {
  return value === null ? UNAVAILABLE : `${value.toFixed(2)}%`;
}
 
export function formatPower(watts: number | null): string {
  if (watts === null) return UNAVAILABLE;
  return watts >= 1000 ? `${(watts / 1000).toFixed(2)} kW` : `${Math.round(watts)} W`;
}
 
// Times are shown in the household timezone (Europe/Istanbul for the pilot).
export function formatTime(iso: string | null, timeZone = "Europe/Istanbul"): string {
  if (iso === null) return UNAVAILABLE;
  return new Intl.DateTimeFormat("en-GB", { timeZone, hour: "2-digit", minute: "2-digit" }).format(new Date(iso));
}
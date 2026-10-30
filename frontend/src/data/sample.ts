// Synthetic development fixtures. Never merge these with physical-device data.
export const sample = {
  source: 'simulated' as const,
  snapshot: '28 October 2026, 14:30 Europe/Istanbul',
  cycle: '18 Oct – 16 Nov 2026',
  powerW: 820,
  todayKwh: 8.4,
  cycleKwh: 108.4,
  energyCost: 325.2,
  forecastEnergyCost: 900,
  budget: 800,
  contributions: [
    { name: 'Air conditioner', kwh: 4, scope: 'Measured appliance', color: '#2c7868' },
    { name: 'Fridge', kwh: 1, scope: 'Measured appliance', color: '#82afa1' },
    { name: 'Dishwasher', kwh: 2, scope: 'Measured appliance', color: '#c0d8cc' },
    { name: 'Other consumption', kwh: 5, scope: 'Calculated remainder', color: '#e2c78e' },
  ],
  weekly: [
    { day: '21 Oct', kwh: 10 }, { day: '22 Oct', kwh: 12 },
    { day: '23 Oct', kwh: 9 }, { day: '24 Oct', kwh: 11 },
    { day: '25 Oct', kwh: 10 }, { day: '26 Oct', kwh: 6 },
    { day: '27 Oct', kwh: 12 },
  ],
};
export const money = (value: number) => new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'TRY', currencyDisplay: 'narrowSymbol' }).format(value);
export const energy = (value: number) => `${value.toFixed(2)} kWh`;

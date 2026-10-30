import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { sample } from '../data/sample';

export function Trend() {
  return <>
    <div className="chart" role="img" aria-label="Sample daily household energy, 21 to 27 October: 10, 12, 9, 11, 10, 6 and 12 kWh. All seven days are complete.">
      <ResponsiveContainer width="100%" height="100%"><BarChart data={sample.weekly} margin={{ top: 16, right: 8, left: -22, bottom: 0 }} accessibilityLayer>
        <CartesianGrid vertical={false} stroke="#e7ece8" strokeDasharray="3 3" />
        <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#68766e' }} minTickGap={15} />
        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#68766e' }} unit="" />
        <Tooltip cursor={{ fill: '#f0f5f1' }} formatter={(value) => [`${Number(value).toFixed(2)} kWh`, 'Household energy']} />
        <Bar dataKey="kwh" fill="#448674" radius={[5, 5, 0, 0]} maxBarSize={48} isAnimationActive={false} />
      </BarChart></ResponsiveContainer>
    </div>
    <details className="data-details"><summary>View sample data table</summary><table><caption>Household energy · complete sample days · Europe/Istanbul</caption><thead><tr><th>Date, 2026</th><th>Energy</th></tr></thead><tbody>{sample.weekly.map(d => <tr key={d.day}><td>{d.day}</td><td>{d.kwh.toFixed(2)} kWh</td></tr>)}</tbody></table></details>
  </>;
}

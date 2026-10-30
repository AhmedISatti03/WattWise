import { Link } from 'react-router-dom';
import { ArrowDownRight, ArrowRight, CircleHelp, Lightbulb, Plug, TrendingUp, Zap } from 'lucide-react';
import { EmptyState, ErrorState, LoadingState, Panel } from '../components/ui';
import { Trend } from '../components/LazyTrend';
import { energy, money, sample } from '../data/sample';

export type DemoState = 'ready' | 'loading' | 'error' | 'empty' | 'disconnected' | 'history';
export function Dashboard({ state, retry }: { state: DemoState; retry: () => void }) {
  if (state === 'loading') return <LoadingState />;
  if (state === 'error') return <ErrorState onRetry={retry} />;
  if (state === 'empty') return <EmptyState title="No household readings yet"><p>Your overview will appear when readings are available. Missing readings are not zero consumption.</p><Link className="text-link" to="/devices">View device setup <ArrowRight size={16} /></Link></EmptyState>;
  const disconnected = state === 'disconnected';
  const history = state === 'history';
  return <>
    {disconnected && <div className="inline-notice" role="status"><Plug size={18} /><div><strong>Fridge plug hasn’t reported recently</strong><p>Last sample reading: 14:20. Household readings remain available. <Link to="/devices">View device status</Link></p></div></div>}
    <div className="metrics">
      <section className="metric"><div className="metric-label">Current household power <Zap size={17} /></div><p className="metric-number">{sample.powerW}<span>W</span></p><p className="muted small"><span className="status-dot" /> Measured sample · 14:30</p></section>
      <section className="metric"><div className="metric-label">Today’s household energy <CircleHelp size={17} /></div><p className="metric-number">{sample.todayKwh.toFixed(2)}<span>kWh</span></p><p className="muted small">28 October · 00:00–14:30 · partial day</p></section>
      <section className="metric"><div className="metric-label">Estimated energy cost so far <TrendingUp size={17} /></div><p className="metric-number money">{money(sample.energyCost)}</p><p className="muted small">Cycle to date · through 14:30</p></section>
    </div>
    <div className="overview-grid">
      <Panel title="Your household, over time" subtitle="Sample daily energy · 21–27 October 2026 · kWh" aside={<span className="pill">7 complete days</span>}><Trend /></Panel>
      <Panel title="Your billing outlook" subtitle={`Cycle · ${sample.cycle}`} className="outlook">
        <p className="eyebrow">{history ? 'FORECAST NOT AVAILABLE' : 'ESTIMATED FULL-CYCLE ENERGY COST'}</p>
        <p className="forecast-value">{history ? '—' : money(sample.forecastEnergyCost)}</p>
        {history ? <div className="history-note"><strong>3 of 7 complete days collected</strong><p>More history, valid tariff inputs and complete elapsed-cycle coverage are needed before a numerical forecast appears.</p></div> : <><span className="pill warm">Early estimate</span><p className="small muted forecast-time">Calculated 28 Oct, 00:00 · data through 27 Oct</p></>}
        <div className="budget-row"><span>Household budget <small>User-set target</small></span><strong>{money(sample.budget)}</strong></div>
        {!history && <div className="budget-alert"><ArrowDownRight size={20} /><div><strong>Forecast to go over by {money(100)}</strong><p>Based on the dated sample forecast.</p></div></div>}
        <Link to="/settings" className="text-link">View budget settings <ArrowRight size={16} /></Link>
        <p className="footnote">Fictional ₺3.00/kWh flat tariff. Energy charges only; excludes other invoice charges. Assumes recent usage continues.</p>
      </Panel>
      <Panel title="Where yesterday’s energy went" subtitle="27 October 2026 · complete matching day" aside={<Link className="text-link small" to="/consumption">Explore usage <ArrowRight size={15} /></Link>}>
        <div className="contribution-total"><span>Household total <small>Measured sample</small></span><strong>12.00 <span>kWh</span></strong></div>
        {disconnected ? <p className="inline-notice small">Appliance comparisons and other consumption are unavailable while the fridge’s interval energy is incomplete. Household energy remains 12.00 kWh.</p> : <div className="energy-stack" aria-label="Household total 12 kWh: air conditioner 4, fridge 1, dishwasher 2, calculated other 5.">{sample.contributions.map(c => <span key={c.name} style={{ width: `${c.kwh / 12 * 100}%`, background: c.color }} />)}</div>}
        <div className="contribution-list">{sample.contributions.map(c => <div key={c.name} className="contribution-row"><span className="legend-dot" style={{ background: c.color }} /><span>{c.name}<small>{c.scope}</small></span><strong>{disconnected && c.name !== 'Air conditioner' && c.name !== 'Dishwasher' ? 'Unavailable' : energy(c.kwh)}</strong></div>)}</div>
        <p className="footnote">Appliances are already included in the household total. Other consumption is a calculated remainder, not an identified appliance.</p>
      </Panel>
      <Panel title="A little insight" subtitle="Guidance grounded in your sample readings" className="insight-panel"><div className="insight-icon"><Lightbulb size={25} /></div><h3>{disconnected ? 'Keep an eye on device coverage' : 'Take a closer look at your AC'}</h3><p className="muted">{disconnected ? 'Restore complete readings before comparing appliance contributions. Reconnection alone does not recover missing energy.' : 'Your AC was the largest monitored contributor yesterday: 4.00 kWh, about 33% of the household’s 12.00 kWh.'}</p><Link className="text-link" to={disconnected ? '/devices' : '/insights/ac-usage'}>{disconnected ? 'View devices' : 'See sample insight'} <ArrowRight size={16} /></Link><p className="footnote">Illustrative recommendation only. This is not a fault diagnosis or a savings guarantee.</p></Panel>
    </div>
  </>;
}

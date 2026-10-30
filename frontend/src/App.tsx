import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { Link, NavLink, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { Activity, ArrowUpRight, BarChart3, FileText, Leaf, LayoutDashboard, Plug, Settings, ShieldCheck } from 'lucide-react';
import { Dashboard } from './pages/Dashboard';
import type { DemoState } from './pages/Dashboard';
import { Account, BillEntry, BillReview, Bills, Consumption, Devices, Insight, Settings as SettingsPage } from './pages/Placeholders';
import { EmptyState } from './components/ui';

const navigation = [
  { path: '/dashboard', label: 'Overview', mobile: 'Home', Icon: LayoutDashboard },
  { path: '/consumption', label: 'Consumption', mobile: 'Usage', Icon: BarChart3 },
  { path: '/bills', label: 'Bills', mobile: 'Bills', Icon: FileText },
  { path: '/devices', label: 'Devices', mobile: 'Devices', Icon: Plug },
];
const titles: Record<string, [string, string]> = {
  '/dashboard': ['A clearer view of your energy.', 'A little understanding goes a long way.'],
  '/consumption': ['Follow the flow.', 'Household usage and the appliances within it.'],
  '/bills': ['Your bills, in one place.', 'Historical records with a clearer context.'],
  '/bills/new': ['Start with your bill.', 'A foundation for upload and manual entry.'],
  '/bills/review': ['Check before you confirm.', 'Keep historical records accurate.'],
  '/devices': ['Stay connected.', 'Your household monitor, plugs and collector.'],
  '/settings': ['Make it your household.', 'Settings and a target that works for you.'],
  '/household/setup': ['Welcome home.', 'Set the context for meaningful estimates.'],
  '/sign-in': ['Welcome to WattWise.', 'Account access screen preview.'],
  '/register': ['A fresh start.', 'Account registration screen preview.'],
};

export default function App() {
  const location = useLocation(); const [state, setState] = useState<DemoState>('ready');
  const title = titles[location.pathname] || (location.pathname.startsWith('/insights/') ? ['Small insights, useful context.', 'Understand the readings behind a suggestion.'] : ['Let’s find your way.', 'This screen isn’t available.']);
  useEffect(() => { document.title = `${location.pathname === '/dashboard' ? 'Overview' : title[0]} · WattWise`; window.scrollTo(0, 0); }, [location.pathname]);
  return <div className="app"><a className="skip-link" href="#main">Skip to content</a><aside className="sidebar"><Link to="/dashboard" className="brand"><span className="brand-icon"><Leaf size={22} /></span>WattWise<span className="brand-dot">.</span></Link><div className="workspace-label">YOUR HOUSEHOLD</div><nav aria-label="Main navigation">{navigation.map(({ path, label, Icon }) => <NavLink key={path} to={path}><Icon size={19} />{label}</NavLink>)}<NavLink to="/settings"><Settings size={19} />Settings</NavLink></nav><div className="sidebar-bottom"><div className="pilot-note"><Activity size={20} /><strong>A thoughtful start.</strong><p>Frontend foundation<br />Development preview</p></div><Link to="/sign-in" className="account-link"><span className="avatar">WW</span><span>Sample household<small>Account screen preview</small></span><ArrowUpRight size={16} /></Link></div></aside>
    <div className="workspace"><header className="topbar"><span className="breadcrumb">My home <span>/</span> {location.pathname.split('/')[1]?.replaceAll('-', ' ') || 'overview'}</span><div className="top-actions"><span className="foundation-tag"><ShieldCheck size={14} />Foundation preview</span><Link to="/settings" aria-label="Open settings" className="settings-link"><Settings size={20} /></Link></div></header>
      <main id="main" tabIndex={-1}><div className="page-heading"><div><p className="eyebrow">WATTWISE / MY HOME</p><h1>{title[0]}</h1><p className="muted">{title[1]}</p></div><div className="cycle-label"><span>BILLING CYCLE</span><strong>18 Oct – 16 Nov 2026</strong></div></div>
        <div className="sample-banner"><span className="sample-badge">SAMPLE DATA</span><p>Not real household measurements. Fixed snapshot: <strong>28 Oct 2026, 14:30 · Europe/Istanbul.</strong></p></div>
        {location.pathname === '/dashboard' && <div className="preview-controls"><label htmlFor="preview-state">Preview state</label><select id="preview-state" value={state} onChange={e => setState(e.target.value as DemoState)}><option value="ready">Sample overview</option><option value="loading">Loading</option><option value="error">Request error</option><option value="empty">No readings</option><option value="disconnected">Disconnected plug</option><option value="history">Insufficient history</option></select><span>UI demonstrations, no live requests</span></div>}
        <Routes><Route path="/" element={<Navigate to="/dashboard" replace />} /><Route path="/dashboard" element={<Dashboard state={state} retry={() => setState('ready')} />} /><Route path="/consumption" element={<Consumption />} /><Route path="/bills" element={<Bills />} /><Route path="/bills/new" element={<BillEntry />} /><Route path="/bills/review" element={<BillReview />} /><Route path="/devices" element={<Devices />} /><Route path="/settings" element={<SettingsPage />} /><Route path="/household/setup" element={<SettingsPage setup />} /><Route path="/sign-in" element={<Account />} /><Route path="/register" element={<Account register />} /><Route path="/insights/:id" element={<Insight />} /><Route path="*" element={<NotFound />} /></Routes>
        <footer>WattWise · CENG481 <span>Built around a better understanding of home energy.</span></footer>
      </main>
    </div><nav className="mobile-nav" aria-label="Phone navigation">{navigation.map(({ path, mobile, Icon }) => <NavLink key={path} to={path}><Icon size={20} /><span>{mobile}</span></NavLink>)}</nav>
  </div>;
}
function NotFound() { return <EmptyState title="Page not found"><p>The address may be incorrect.</p><Link to="/dashboard" className="text-link">Return to overview</Link></EmptyState>; }

import { Component } from 'react';
export class AppErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() { return this.state.failed ? <div className="state-box" role="alert"><h1>Something went wrong</h1><p>The frontend could not render this screen.</p><a className="button secondary" href="/dashboard">Reload overview</a></div> : this.props.children; }
}

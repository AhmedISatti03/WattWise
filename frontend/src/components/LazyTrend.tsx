import { lazy, Suspense } from 'react';

const Chart = lazy(() => import('./Trend').then(module => ({ default: module.Trend })));
export function Trend() {
  return <Suspense fallback={<div className="chart state-box" role="status">Loading sample chart…</div>}><Chart /></Suspense>;
}

import { useId } from 'react';
import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode } from 'react';
import { AlertCircle, ArrowRight, Inbox, LoaderCircle } from 'lucide-react';

export function Button({ children, variant = 'primary', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' }) {
  return <button className={`button ${variant}`} {...props}>{children}</button>;
}
export function Panel({ title, subtitle, children, aside, className = '' }: { title: string; subtitle?: string; children: ReactNode; aside?: ReactNode; className?: string }) {
  return <section className={`panel ${className}`}><div className="panel-head"><div><h2>{title}</h2>{subtitle && <p className="muted small">{subtitle}</p>}</div>{aside}</div>{children}</section>;
}
export function Field({ label, hint, error, ...props }: InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string; error?: string }) {
  const id = useId();
  return <div className="field"><label htmlFor={id}>{label}</label><input {...props} id={id} aria-invalid={!!error} aria-describedby={hint || error ? `${id}-help` : undefined} />{(hint || error) && <p id={`${id}-help`} className={error ? 'field-error' : 'muted small'}>{error || hint}</p>}</div>;
}
export function LoadingState() {
  return <div className="state-box" role="status"><LoaderCircle className="spin" size={28} /><h2>Loading household overview</h2><p>Waiting for the sample view to finish loading.</p><div className="skeleton" /><div className="skeleton short" /></div>;
}
export function ErrorState({ onRetry }: { onRetry: () => void }) {
  return <div className="state-box" role="alert"><AlertCircle size={30} /><h2>We couldn’t load this overview</h2><p>This is a simulated request error. It does not mean your devices are disconnected.</p><Button onClick={onRetry} variant="secondary">Retry sample view <ArrowRight size={16} /></Button></div>;
}
export function EmptyState({ title, children }: { title: string; children: ReactNode }) {
  return <div className="state-box"><Inbox size={30} /><h2>{title}</h2><div className="muted">{children}</div></div>;
}
export function Placeholder({ children }: { children?: ReactNode }) {
  return <div className="placeholder-note"><strong>Screen placeholder</strong><span>{children || 'Navigation and layout are ready. This feature is not connected to a backend.'}</span></div>;
}

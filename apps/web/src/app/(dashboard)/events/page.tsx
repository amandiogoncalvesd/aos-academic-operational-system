import { EventFeed } from '@/components/EventFeed';

export default function EventsPage() {
  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="font-display text-3xl font-semibold tracking-tight">Barramento</h1>
      <p className="mt-1 text-sm text-muted">Cada acção no AOS é um evento. Os plugins reagem sem se conhecerem.</p>
      <div className="mt-8"><EventFeed limit={100} /></div>
    </div>
  );
}

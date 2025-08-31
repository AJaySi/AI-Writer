import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';

interface EventHITLProps {
  args: any;
  respond: (data: any) => void;
}

const EventHITL: React.FC<EventHITLProps> = ({ args, respond }) => {
  const TYPES = ['Workshop','Webinar','Conference','Networking event','Product launch','Sale/Promotion','Community event','Educational event','Custom'];
  const FORMATS = ['In-person','Virtual','Hybrid'];
  
  const mapType = (t?: string) => {
    const s = (t || '').trim().toLowerCase();
    const exact = TYPES.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('web')) return 'Webinar';
    if (s.includes('work')) return 'Workshop';
    if (s.includes('network')) return 'Networking event';
    if (s.includes('launch')) return 'Product launch';
    if (s.includes('sale') || s.includes('promo')) return 'Sale/Promotion';
    if (s.includes('communi')) return 'Community event';
    if (s.includes('educat')) return 'Educational event';
    if (s.includes('conf')) return 'Conference';
    return 'Webinar';
  };
  
  const mapFormat = (f?: string) => {
    const s = (f || '').trim().toLowerCase();
    const exact = FORMATS.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('in') || s.includes('person')) return 'In-person';
    if (s.includes('hybr')) return 'Hybrid';
    return 'Virtual';
  };

  const [form, setForm] = React.useState({
    event_name: args?.event_name || 'Monthly Growth Webinar',
    event_type: mapType(args?.event_type) || 'Webinar',
    event_format: mapFormat(args?.event_format) || 'Virtual',
    business_type: args?.business_type || 'SaaS',
    target_audience: args?.target_audience || 'Marketing managers at SMEs',
    event_date: args?.event_date || '',
    event_time: args?.event_time || '',
    location: args?.location || '',
    duration: args?.duration || '60 minutes',
    key_benefits: args?.key_benefits || '',
    speakers: args?.speakers || '',
    agenda: args?.agenda || '',
    ticket_info: args?.ticket_info || '',
    special_offers: args?.special_offers || '',
    include: args?.include || '',
    avoid: args?.avoid || ''
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  
  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const payload = { ...form, event_type: mapType(form.event_type), event_format: mapFormat(form.event_format) } as any;
      const res = await facebookWriterApi.eventGenerate(payload);
      const title = res?.event_title || res?.data?.event_title;
      const desc = res?.event_description || res?.data?.event_description;
      let out = '';
      if (title) out += `\n\n${title}`;
      if (desc) out += `\n\n${desc}`;
      if (out) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: out }));
        respond({ success: true, content: out });
      } else {
        respond({ success: true, message: 'Event generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate event';
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };
  
  const set = (k: string, v: any) => setForm((p: any) => ({ ...p, [k]: v }));
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Event</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Event name" value={form.event_name} onChange={e => set('event_name', e.target.value)} />
        <input placeholder="Event type (e.g., Webinar)" value={form.event_type} onChange={e => set('event_type', e.target.value)} />
        <input placeholder="Format (In-person/Virtual/Hybrid)" value={form.event_format} onChange={e => set('event_format', e.target.value)} />
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder="Date (YYYY-MM-DD)" value={form.event_date} onChange={e => set('event_date', e.target.value)} />
        <input placeholder="Time" value={form.event_time} onChange={e => set('event_time', e.target.value)} />
        <input placeholder="Location" value={form.location} onChange={e => set('location', e.target.value)} />
        <input placeholder="Duration" value={form.duration} onChange={e => set('duration', e.target.value)} />
        <input placeholder="Key benefits" value={form.key_benefits} onChange={e => set('key_benefits', e.target.value)} />
        <input placeholder="Speakers" value={form.speakers} onChange={e => set('speakers', e.target.value)} />
        <input placeholder="Agenda" value={form.agenda} onChange={e => set('agenda', e.target.value)} />
        <input placeholder="Ticket info" value={form.ticket_info} onChange={e => set('ticket_info', e.target.value)} />
        <input placeholder="Special offers" value={form.special_offers} onChange={e => set('special_offers', e.target.value)} />
        <input placeholder="Include" value={form.include} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid} onChange={e => set('avoid', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default EventHITL;

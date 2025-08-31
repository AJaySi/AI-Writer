import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { readPrefs, logAssistant } from '../utils/facebookWriterUtils';

interface ReelHITLProps {
  args: any;
  respond: (data: any) => void;
}

const ReelHITL: React.FC<ReelHITLProps> = ({ args, respond }) => {
  const VALID_REEL_TYPES = ['Product demonstration','Tutorial/How-to','Entertainment','Educational','Trend-based','Behind the scenes','User-generated content','Custom'];
  const VALID_REEL_LENGTHS = ['15-30 seconds','30-60 seconds','60-90 seconds'];
  const VALID_REEL_STYLES = ['Fast-paced','Relaxed','Dramatic','Minimalist','Vibrant','Custom'];
  
  const mapReelType = (t?: string) => {
    const s = (t || '').trim().toLowerCase();
    const exact = VALID_REEL_TYPES.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('product')) return 'Product demonstration';
    if (s.includes('tutorial') || s.includes('how')) return 'Tutorial/How-to';
    if (s.includes('behind')) return 'Behind the scenes';
    if (s.includes('user')) return 'User-generated content';
    if (s.includes('trend')) return 'Trend-based';
    if (s.includes('educat')) return 'Educational';
    if (s.includes('entertain')) return 'Entertainment';
    return 'Product demonstration';
  };
  
  const mapReelLength = (l?: string) => {
    const s = (l || '').trim().toLowerCase();
    const exact = VALID_REEL_LENGTHS.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('15')) return '15-30 seconds';
    if (s.includes('60') || s.includes('30-60')) return '30-60 seconds';
    if (s.includes('90') || s.includes('60-90')) return '60-90 seconds';
    return '30-60 seconds';
  };
  
  const mapReelStyle = (st?: string) => {
    const s = (st || '').trim().toLowerCase();
    const exact = VALID_REEL_STYLES.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('fast')) return 'Fast-paced';
    if (s.includes('relax')) return 'Relaxed';
    if (s.includes('dram')) return 'Dramatic';
    if (s.includes('mini')) return 'Minimalist';
    if (s.includes('vibr')) return 'Vibrant';
    return 'Fast-paced';
  };

  const prefs = React.useMemo(() => readPrefs(), []);
  const [form, setForm] = React.useState({
    business_type: args?.business_type || prefs.business_type || 'SaaS',
    target_audience: args?.target_audience || prefs.target_audience || 'Marketing managers at SMEs',
    reel_type: args?.reel_type || 'Product demonstration',
    reel_length: args?.reel_length || '30-60 seconds',
    reel_style: args?.reel_style || 'Fast-paced',
    topic: args?.topic || 'Feature walkthrough',
    include: args?.include || '',
    avoid: args?.avoid || '',
    music_preference: args?.music_preference || ''
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  
  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const payload = {
        ...form,
        reel_type: mapReelType(form.reel_type),
        reel_length: mapReelLength(form.reel_length),
        reel_style: mapReelStyle(form.reel_style)
      } as any;
      const res = await facebookWriterApi.reelGenerate(payload);
      const script = res?.script || res?.data?.script;
      if (script) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: `\n\n${script}` }));
        logAssistant(script);
        respond({ success: true, content: script });
      } else {
        respond({ success: true, message: 'Reel generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate reel. Tip: type should be one of ' + VALID_REEL_TYPES.join(', ') + '; length one of ' + VALID_REEL_LENGTHS.join(', ') + '; style one of ' + VALID_REEL_STYLES.join(', ') + '.';
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };
  
  const set = (k: string, v: any) => setForm((p: any) => ({ ...p, [k]: v }));
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Reel</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder="Reel type (e.g., Product demonstration)" value={form.reel_type} onChange={e => set('reel_type', e.target.value)} />
        <input placeholder="Length (e.g., 30-60 seconds)" value={form.reel_length} onChange={e => set('reel_length', e.target.value)} />
        <input placeholder="Style (e.g., Fast-paced)" value={form.reel_style} onChange={e => set('reel_style', e.target.value)} />
        <input placeholder="Topic" value={form.topic} onChange={e => set('topic', e.target.value)} />
        <input placeholder="Include" value={form.include} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid} onChange={e => set('avoid', e.target.value)} />
        <input placeholder="Music preference" value={form.music_preference} onChange={e => set('music_preference', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default ReelHITL;

import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { readPrefs, logAssistant } from '../utils/facebookWriterUtils';

interface CarouselHITLProps {
  args: any;
  respond: (data: any) => void;
}

const CarouselHITL: React.FC<CarouselHITLProps> = ({ args, respond }) => {
  const VALID_TYPES = ['Product showcase','Step-by-step guide','Before/After','Customer testimonials','Features & Benefits','Portfolio showcase','Educational content','Custom'];
  
  const mapType = (t?: string) => {
    const s = (t || '').trim().toLowerCase();
    const exact = VALID_TYPES.find(v => v.toLowerCase() === s);
    if (exact) return exact;
    if (s.includes('step')) return 'Step-by-step guide';
    if (s.includes('before') || s.includes('after')) return 'Before/After';
    if (s.includes('testi')) return 'Customer testimonials';
    if (s.includes('feature') || s.includes('benefit')) return 'Features & Benefits';
    if (s.includes('portfolio')) return 'Portfolio showcase';
    if (s.includes('educat')) return 'Educational content';
    return 'Product showcase';
  };

  const prefs = React.useMemo(() => readPrefs(), []);
  const [form, setForm] = React.useState({
    business_type: args?.business_type || prefs.business_type || 'SaaS',
    target_audience: args?.target_audience || prefs.target_audience || 'Marketing managers at SMEs',
    carousel_type: args?.carousel_type || 'Product showcase',
    topic: args?.topic || 'Feature breakdown',
    num_slides: 5,
    include_cta: true,
    cta_text: '',
    brand_colors: '',
    include: '',
    avoid: ''
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  
  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const payload = { ...form, carousel_type: mapType(form.carousel_type) } as any;
      const res = await facebookWriterApi.carouselGenerate(payload);
      const main = res?.main_caption || res?.data?.main_caption;
      const slides = res?.slides || res?.data?.slides;
      let out = '';
      if (main) out += `\n\n${main}`;
      if (Array.isArray(slides)) {
        out += '\n\nCarousel Slides:';
        slides.forEach((s: any, i: number) => {
          out += `\n${i + 1}. ${s.title}: ${s.content}`;
        });
      }
      if (out) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: out }));
        logAssistant(out);
        respond({ success: true, content: out });
      } else {
        respond({ success: true, message: 'Carousel generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate carousel';
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };
  
  const set = (k: string, v: any) => setForm((p: any) => ({ ...p, [k]: v }));
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Carousel</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder="Carousel type (e.g., Product showcase)" value={form.carousel_type} onChange={e => set('carousel_type', e.target.value)} />
        <input placeholder="Topic" value={form.topic} onChange={e => set('topic', e.target.value)} />
        <input placeholder="Number of slides (3-10)" value={form.num_slides} onChange={e => set('num_slides', Number(e.target.value) || 5)} />
        <label><input type="checkbox" checked={!!form.include_cta} onChange={e => set('include_cta', e.target.checked)} /> Include CTA</label>
        <input placeholder="CTA text" value={form.cta_text} onChange={e => set('cta_text', e.target.value)} />
        <input placeholder="Brand colors" value={form.brand_colors} onChange={e => set('brand_colors', e.target.value)} />
        <input placeholder="Include" value={form.include} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid} onChange={e => set('avoid', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default CarouselHITL;

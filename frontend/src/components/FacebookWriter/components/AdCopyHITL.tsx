import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { readPrefs, logAssistant } from '../utils/facebookWriterUtils';

interface AdCopyHITLProps {
  args: any;
  respond?: (data: any) => void;
}

const AdCopyHITL: React.FC<AdCopyHITLProps> = ({ args, respond }) => {
  const prefs = React.useMemo(() => readPrefs(), []);
  const [form, setForm] = React.useState({
    business_type: args?.business_type || prefs.business_type || 'SaaS',
    product_service: args?.product_service || 'Product X',
    ad_objective: args?.ad_objective || 'Conversions',
    ad_format: args?.ad_format || 'Single image',
    target_audience: args?.target_audience || prefs.target_audience || 'Marketing managers at SMEs',
    targeting_options: {
      age_group: (args?.targeting_options?.age_group) || '18-24',
      gender: args?.targeting_options?.gender || 'All',
      location: args?.targeting_options?.location || 'Global',
      interests: args?.targeting_options?.interests || '',
      behaviors: args?.targeting_options?.behaviors || '',
      lookalike_audience: args?.targeting_options?.lookalike_audience || ''
    },
    unique_selling_proposition: args?.unique_selling_proposition || 'Fast, reliable, loved by users',
    offer_details: args?.offer_details || '',
    budget_range: args?.budget_range || '$50-200/day',
    custom_budget: args?.custom_budget || '',
    campaign_duration: args?.campaign_duration || '2 weeks',
    competitor_analysis: args?.competitor_analysis || '',
    brand_voice: args?.brand_voice || (prefs.post_tone || 'Professional'),
    compliance_requirements: args?.compliance_requirements || ''
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const safeRespond = React.useCallback((data: any) => {
    try {
      if (typeof respond === 'function') respond(data);
      else console.log('[FB Writer][HITL] respond unavailable; payload:', data);
    } catch (e) { console.warn('[FB Writer][HITL] respond error', e); }
  }, [respond]);

  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await facebookWriterApi.adCopyGenerate(form as any);
      const variations = {
        headline_variations: res?.ad_variations?.headline_variations || res?.data?.ad_variations?.headline_variations || [],
        primary_text_variations: res?.ad_variations?.primary_text_variations || res?.data?.ad_variations?.primary_text_variations || [],
        description_variations: res?.ad_variations?.description_variations || res?.data?.ad_variations?.description_variations || [],
        cta_variations: res?.ad_variations?.cta_variations || res?.data?.ad_variations?.cta_variations || []
      };
      window.dispatchEvent(new CustomEvent('fbwriter:adVariations', { detail: variations }));
      const primaryObj = res?.primary_ad_copy || res?.data?.primary_ad_copy;
      const message = primaryObj?.primary_text || primaryObj?.text || res?.content || res?.data?.content || 'Ad copy generated.';
      window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: `\n\n${message}` }));
      logAssistant(message);
      safeRespond({ success: true, content: message });
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate ad copy';
      setError(`${msg}`);
      safeRespond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };

  const set = (k: string, v: any) => setForm((prev: any) => ({ ...prev, [k]: v }));
  const setNested = (k: keyof typeof form.targeting_options, v: any) => setForm((prev: any) => ({ ...prev, targeting_options: { ...prev.targeting_options, [k]: v } }));

  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Ad Copy</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Product/Service" value={form.product_service} onChange={e => set('product_service', e.target.value)} />
        <input placeholder="Ad objective (e.g., Conversions)" value={form.ad_objective} onChange={e => set('ad_objective', e.target.value)} />
        <input placeholder="Ad format (e.g., Single image)" value={form.ad_format} onChange={e => set('ad_format', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <div style={{ display: 'grid', gap: 6 }}>
          <div style={{ fontSize: 12, opacity: 0.9 }}>Targeting</div>
          <input placeholder="Age group (e.g., 18-24)" value={form.targeting_options.age_group} onChange={e => setNested('age_group', e.target.value)} />
          <input placeholder="Gender" value={form.targeting_options.gender || ''} onChange={e => setNested('gender', e.target.value)} />
          <input placeholder="Location" value={form.targeting_options.location || ''} onChange={e => setNested('location', e.target.value)} />
          <input placeholder="Interests" value={form.targeting_options.interests || ''} onChange={e => setNested('interests', e.target.value)} />
        </div>
        <input placeholder="USP" value={form.unique_selling_proposition} onChange={e => set('unique_selling_proposition', e.target.value)} />
        <input placeholder="Offer details" value={form.offer_details || ''} onChange={e => set('offer_details', e.target.value)} />
        <input placeholder="Budget range (e.g., $50-200/day)" value={form.budget_range} onChange={e => set('budget_range', e.target.value)} />
        <input placeholder="Campaign duration" value={form.campaign_duration || ''} onChange={e => set('campaign_duration', e.target.value)} />
        <input placeholder="Brand voice" value={form.brand_voice || ''} onChange={e => set('brand_voice', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default AdCopyHITL;

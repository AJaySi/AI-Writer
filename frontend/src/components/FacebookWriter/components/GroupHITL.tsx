import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';

interface GroupHITLProps {
  args: any;
  respond: (data: any) => void;
}

const GroupHITL: React.FC<GroupHITLProps> = ({ args, respond }) => {
  const TYPES = ['Industry/Professional','Hobby/Interest','Local community','Support group','Educational','Business networking','Lifestyle','Custom'];
  const PURPOSES = ['Share knowledge','Ask question','Promote business','Build relationships','Provide value','Seek advice','Announce news','Custom'];
  
  const mapType = (t?: string) => {
    const s = (t || '').trim().toLowerCase();
    const exact = TYPES.find(v => v.toLowerCase() === s); if (exact) return exact;
    if (s.includes('industry')) return 'Industry/Professional';
    if (s.includes('hobby') || s.includes('interest')) return 'Hobby/Interest';
    if (s.includes('local')) return 'Local community';
    if (s.includes('support')) return 'Support group';
    if (s.includes('educat')) return 'Educational';
    if (s.includes('business')) return 'Business networking';
    if (s.includes('life')) return 'Lifestyle';
    return 'Industry/Professional';
  };
  
  const mapPurpose = (p?: string) => {
    const s = (p || '').trim().toLowerCase();
    const exact = PURPOSES.find(v => v.toLowerCase() === s); if (exact) return exact;
    if (s.includes('ask')) return 'Ask question';
    if (s.includes('promot')) return 'Promote business';
    if (s.includes('build')) return 'Build relationships';
    if (s.includes('value')) return 'Provide value';
    if (s.includes('advice')) return 'Seek advice';
    if (s.includes('news')) return 'Announce news';
    return 'Share knowledge';
  };

  const [form, setForm] = React.useState({
    group_name: args?.group_name || 'Marketing Managers Community',
    group_type: mapType(args?.group_type) || 'Industry/Professional',
    post_purpose: mapPurpose(args?.post_purpose) || 'Share knowledge',
    business_type: args?.business_type || 'SaaS',
    topic: args?.topic || 'Content strategy tips',
    target_audience: args?.target_audience || 'Marketing managers at SMEs',
    value_proposition: args?.value_proposition || '3 actionable tips with examples',
    group_rules: { no_promotion: true, value_first: true, no_links: true, community_focused: true, relevant_only: true },
    include: '',
    avoid: '',
    call_to_action: 'Share your approach'
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  
  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await facebookWriterApi.groupPostGenerate(form as any);
      const content = res?.content || res?.data?.content;
      const starters = res?.engagement_starters || res?.data?.engagement_starters;
      let out = '';
      if (content) out += `\n\n${content}`;
      if (Array.isArray(starters) && starters.length) {
        out += '\n\nEngagement starters:';
        starters.forEach((s: string) => out += `\n- ${s}`);
      }
      if (out) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: out }));
        respond({ success: true, content: out });
      } else {
        respond({ success: true, message: 'Group post generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate group post';
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };
  
  const set = (k: string, v: any) => setForm((p: any) => ({ ...p, [k]: v }));
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Group Post</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Group name" value={form.group_name} onChange={e => set('group_name', e.target.value)} />
        <input placeholder="Group type (e.g., Industry/Professional)" value={form.group_type} onChange={e => set('group_type', e.target.value)} />
        <input placeholder="Purpose (e.g., Share knowledge)" value={form.post_purpose} onChange={e => set('post_purpose', e.target.value)} />
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Topic" value={form.topic} onChange={e => set('topic', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder="Value proposition" value={form.value_proposition} onChange={e => set('value_proposition', e.target.value)} />
        <input placeholder="Include" value={form.include} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid} onChange={e => set('avoid', e.target.value)} />
        <input placeholder="Call to action" value={form.call_to_action || ''} onChange={e => set('call_to_action', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default GroupHITL;

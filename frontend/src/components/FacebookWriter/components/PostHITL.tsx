import React from 'react';
import { facebookWriterApi, PostGenerateRequest } from '../../../services/facebookWriterApi';
import { readPrefs, writePrefs, logAssistant, mapGoal, mapTone, VALID_GOALS, VALID_TONES } from '../utils/facebookWriterUtils';

interface PostHITLProps {
  args: any;
  respond: (data: any) => void;
}

const PostHITL: React.FC<PostHITLProps> = ({ args, respond }) => {
  const prefs = React.useMemo(() => readPrefs(), []);
  const [form, setForm] = React.useState<PostGenerateRequest>({
    business_type: args?.business_type || prefs.business_type || 'SaaS',
    target_audience: args?.target_audience || prefs.target_audience || 'Marketing managers at SMEs',
    post_goal: args?.post_goal || prefs.post_goal || 'Build brand awareness',
    post_tone: args?.post_tone || prefs.post_tone || 'Professional',
    include: args?.include || prefs.include || '',
    avoid: args?.avoid || prefs.avoid || '',
    media_type: args?.media_type || 'None',
    advanced_options: { use_hook: true, use_story: true, use_cta: true, use_question: true, use_emoji: true, use_hashtags: true }
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const payload: PostGenerateRequest = {
        ...form,
        post_goal: mapGoal(form.post_goal),
        post_tone: mapTone(form.post_tone),
        media_type: 'None'
      };
      // Save user preference snapshot
      writePrefs({
        business_type: payload.business_type,
        target_audience: payload.target_audience,
        post_goal: payload.post_goal,
        post_tone: payload.post_tone,
        include: payload.include,
        avoid: payload.avoid
      });
      const res = await facebookWriterApi.postGenerate(payload);
      const content = res?.content || res?.data?.content;
      if (content) {
        window.dispatchEvent(new CustomEvent('fbwriter:updateDraft', { detail: content }));
        logAssistant(content);
        respond({ success: true, content });
      } else {
        respond({ success: true, message: 'Post generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate post';
      const tip = `Tip: goals must be one of ${VALID_GOALS.join(', ')}; tones must be one of ${VALID_TONES.join(', ')}.`;
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
      console.error('[FB Writer] post.generate error', e);
    } finally {
      setLoading(false);
    }
  };

  const set = (k: keyof PostGenerateRequest, v: any) => setForm(prev => ({ ...prev, [k]: v }));

  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Facebook Post</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder={`Business type`} value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder={`Target audience`} value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder={`Goal (e.g., ${VALID_GOALS[3]})`} value={form.post_goal} onChange={e => set('post_goal', e.target.value)} />
        <input placeholder={`Tone (e.g., ${VALID_TONES[5]})`} value={form.post_tone} onChange={e => set('post_tone', e.target.value)} />
        <input placeholder="Include" value={form.include || ''} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid || ''} onChange={e => set('avoid', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default PostHITL;

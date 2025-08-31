import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { readPrefs, logAssistant, mapStoryType, mapStoryTone } from '../utils/facebookWriterUtils';

interface StoryHITLProps {
  args: any;
  respond?: (data: any) => void;
}

const StoryHITL: React.FC<StoryHITLProps> = ({ args, respond }) => {
  const prefs = React.useMemo(() => readPrefs(), []);
  const [form, setForm] = React.useState({
    business_type: args?.business_type || prefs.business_type || 'SaaS',
    target_audience: args?.target_audience || prefs.target_audience || 'Marketing managers at SMEs',
    story_type: mapStoryType(args?.story_type) || 'Product showcase',
    story_tone: mapStoryTone(args?.story_tone) || 'Casual',
    include: args?.include || '',
    avoid: args?.avoid || '',
    // Advanced options
    use_hook: true,
    use_story: true,
    use_cta: true,
    use_question: true,
    use_emoji: true,
    use_hashtags: true,
    // Visual options
    visual_options: {
      background_type: args?.visual_options?.background_type || 'Solid color',
      background_image_prompt: args?.visual_options?.background_image_prompt || '',
      gradient_style: args?.visual_options?.gradient_style || '',
      text_overlay: args?.visual_options?.text_overlay ?? true,
      text_style: args?.visual_options?.text_style || '',
      text_color: args?.visual_options?.text_color || '',
      text_position: args?.visual_options?.text_position || '',
      stickers: args?.visual_options?.stickers ?? true,
      interactive_elements: args?.visual_options?.interactive_elements ?? true,
      interactive_types: args?.visual_options?.interactive_types || [],
      call_to_action: args?.visual_options?.call_to_action || ''
    }
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const safeRespond = (d: any) => { try { if (typeof respond === 'function') respond(d); } catch {} };

  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const payload = {
        ...form,
        story_type: mapStoryType(form.story_type),
        story_tone: mapStoryTone(form.story_tone),
        visual_options: {
          ...form.visual_options,
          interactive_types: Array.isArray(form.visual_options?.interactive_types)
            ? form.visual_options?.interactive_types
            : []
        }
      } as any;
      const res = await facebookWriterApi.storyGenerate(payload);
      const content = res?.content || res?.data?.content;
      if (content) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: `\n\n${content}` }));
        logAssistant(content);
        safeRespond({ success: true, content });
      } else {
        safeRespond({ success: true, message: 'Story generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate story';
      setError(`${msg}`);
      safeRespond({ success: false, message: `${msg}` });
    } finally {
      setLoading(false);
    }
  };

  const set = (k: string, v: any) => setForm((prev: any) => ({ ...prev, [k]: v }));
  const setVisual = (k: string, v: any) => setForm((prev: any) => ({ ...prev, visual_options: { ...prev.visual_options, [k]: v } }));
  const parseInteractive = (s: string): string[] => s.split(',').map(x => x.trim()).filter(Boolean);
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Story</div>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Business type" value={form.business_type} onChange={e => set('business_type', e.target.value)} />
        <input placeholder="Target audience" value={form.target_audience} onChange={e => set('target_audience', e.target.value)} />
        <input placeholder="Story type (e.g., Product showcase)" value={form.story_type} onChange={e => set('story_type', e.target.value)} />
        <input placeholder="Tone (e.g., Casual)" value={form.story_tone} onChange={e => set('story_tone', e.target.value)} />
        <input placeholder="Include" value={form.include} onChange={e => set('include', e.target.value)} />
        <input placeholder="Avoid" value={form.avoid} onChange={e => set('avoid', e.target.value)} />
        <div style={{ marginTop: 8, fontWeight: 600 }}>Advanced options</div>
        <label><input type="checkbox" checked={form.use_hook} onChange={e => set('use_hook', e.target.checked)} /> Hook</label>
        <label><input type="checkbox" checked={form.use_story} onChange={e => set('use_story', e.target.checked)} /> Narrative</label>
        <label><input type="checkbox" checked={form.use_cta} onChange={e => set('use_cta', e.target.checked)} /> Include CTA</label>
        <label><input type="checkbox" checked={form.use_question} onChange={e => set('use_question', e.target.checked)} /> Ask question</label>
        <label><input type="checkbox" checked={form.use_emoji} onChange={e => set('use_emoji', e.target.checked)} /> Emojis</label>
        <label><input type="checkbox" checked={form.use_hashtags} onChange={e => set('use_hashtags', e.target.checked)} /> Hashtags</label>

        <div style={{ marginTop: 8, fontWeight: 600 }}>Visual options</div>
        <input placeholder="Background type (Solid color, Gradient, Image, Video)" value={form.visual_options.background_type} onChange={e => setVisual('background_type', e.target.value)} />
        <input placeholder="Background image/video prompt (if applicable)" value={form.visual_options.background_image_prompt || ''} onChange={e => setVisual('background_image_prompt', e.target.value)} />
        <input placeholder="Gradient style" value={form.visual_options.gradient_style || ''} onChange={e => setVisual('gradient_style', e.target.value)} />
        <label><input type="checkbox" checked={!!form.visual_options.text_overlay} onChange={e => setVisual('text_overlay', e.target.checked)} /> Text overlay</label>
        <input placeholder="Text style" value={form.visual_options.text_style || ''} onChange={e => setVisual('text_style', e.target.value)} />
        <input placeholder="Text color" value={form.visual_options.text_color || ''} onChange={e => setVisual('text_color', e.target.value)} />
        <input placeholder="Text position (e.g., Top-Left)" value={form.visual_options.text_position || ''} onChange={e => setVisual('text_position', e.target.value)} />
        <label><input type="checkbox" checked={!!form.visual_options.stickers} onChange={e => setVisual('stickers', e.target.checked)} /> Stickers/Emojis</label>
        <label><input type="checkbox" checked={!!form.visual_options.interactive_elements} onChange={e => setVisual('interactive_elements', e.target.checked)} /> Interactive elements</label>
        <input placeholder="Interactive types (comma-separated: poll,quiz,slider,countdown)" value={(form.visual_options.interactive_types || []).join(', ')} onChange={e => setVisual('interactive_types', parseInteractive(e.target.value))} />
        <input placeholder="CTA overlay text" value={form.visual_options.call_to_action || ''} onChange={e => setVisual('call_to_action', e.target.value)} />
      </div>
      <button onClick={run} disabled={loading} style={{ marginTop: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default StoryHITL;

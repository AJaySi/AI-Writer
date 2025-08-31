import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { logAssistant } from '../utils/facebookWriterUtils';

interface HashtagsHITLProps {
  args: any;
  respond: (data: any) => void;
}

const HashtagsHITL: React.FC<HashtagsHITLProps> = ({ args, respond }) => {
  const [topic, setTopic] = React.useState<string>(args?.content_topic || 'product launch');
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await facebookWriterApi.hashtagsGenerate({ content_topic: topic });
      const hashtags = res?.hashtags || res?.data?.hashtags;
      if (Array.isArray(hashtags) && hashtags.length) {
        const line = hashtags.join(' ');
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: `\n\n${line}` }));
        logAssistant(line);
        respond({ success: true, hashtags });
      } else {
        respond({ success: true, message: 'Hashtags generated.' });
      }
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate hashtags';
      setError(`${msg}`);
      respond({ success: false, message: `${msg}` });
      console.error('[FB Writer] hashtags.generate error', e);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Generate Hashtags</div>
      <input placeholder="Topic" value={topic} onChange={e => setTopic(e.target.value)} />
      <button onClick={run} disabled={loading} style={{ marginLeft: 8 }}>{loading ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default HashtagsHITL;

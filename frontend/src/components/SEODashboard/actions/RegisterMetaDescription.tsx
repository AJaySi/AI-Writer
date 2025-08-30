import React from 'react';
import { useCopilotActionTyped, useExecute } from './helpers';
import { seoApiService } from '../../../services/seoApiService';

const MetaUI: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [keywords, setKeywords] = React.useState<string>((args?.keywords || []).join(', '));
  const [tone, setTone] = React.useState<string>(args?.tone || 'professional');
  const [isRunning, setIsRunning] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);
  const tones = ['professional', 'casual', 'technical', 'friendly', 'persuasive'];

  const run = async () => {
    try {
      setIsRunning(true);
      setError(null);
      const parsedKeywords = keywords.split(',').map(k => k.trim()).filter(Boolean);
      if (!parsedKeywords.length) throw new Error('Please provide at least one keyword');
      const res = await seoApiService.generateMetaDescriptions({ keywords: parsedKeywords, tone });
      setResult(res);
      respond({ success: true, keywords: parsedKeywords, tone, result: res });
    } catch (e: any) {
      setError(e?.message || 'Failed to generate meta descriptions');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Meta description generation</div>
      <div style={{ marginBottom: 8 }}>
        <div style={{ fontSize: 12, marginBottom: 4 }}>Target keywords (comma-separated)</div>
        <input type="text" value={keywords} onChange={(e) => setKeywords(e.target.value)} style={{ width: '100%', padding: 6, fontSize: 12 }} />
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
        {tones.map(t => (
          <button key={t} onClick={() => setTone(t)} style={{ padding: '4px 8px', fontSize: 12, borderRadius: 12, border: '1px solid #ddd', background: tone === t ? '#eef2ff' : 'white' }}>{t}</button>
        ))}
      </div>
      <button onClick={run} disabled={isRunning} style={{ padding: '6px 10px' }}>{isRunning ? 'Generating…' : 'Generate'}</button>
      {error && <div style={{ marginTop: 10, color: '#c33', fontSize: 12 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 12, fontSize: 12 }}>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

const RegisterMetaDescription: React.FC = () => {
  const execute = useExecute();
  const useAction = useCopilotActionTyped();

  useAction({
    name: 'generateMetaDescriptions',
    description: 'Generate optimized meta descriptions for web pages',
    parameters: [
      { name: 'keywords', type: 'string[]', description: 'Target keywords', required: true },
      { name: 'tone', type: 'string', description: 'Tone (professional, casual, technical, friendly, persuasive)', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <MetaUI args={args} respond={respond} />,
    handler: async (args: any) => {
      const parsedKeywords: string[] = Array.isArray(args?.keywords)
        ? args.keywords
        : String(args?.keywords || '').split(',').map((k: string) => k.trim()).filter(Boolean);
      return await execute('generateMetaDescriptions', { keywords: parsedKeywords, tone: args?.tone });
    }
  });

  return null;
};

export default RegisterMetaDescription;

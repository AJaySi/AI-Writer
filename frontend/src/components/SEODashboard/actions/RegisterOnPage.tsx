import React from 'react';
import { useCopilotActionTyped, useExecute, getDefaultUrl } from './helpers';
import { seoApiService } from '../../../services/seoApiService';

const OnPageUI: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [keywords, setKeywords] = React.useState<string>((args?.targetKeywords || []).join(', '));
  const [analyzeImages, setAnalyzeImages] = React.useState<boolean>(!!args?.analyzeImages);
  const [analyzeContentQuality, setAnalyzeContentQuality] = React.useState<boolean>(!!args?.analyzeContentQuality);
  const [isRunning, setIsRunning] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);
  const url = args?.url || getDefaultUrl();

  const run = async () => {
    try {
      setIsRunning(true);
      setError(null);
      if (!url) throw new Error('No URL available');
      const parsedKeywords = keywords.split(',').map(k => k.trim()).filter(Boolean);
      const res = await seoApiService.analyzeOnPageSEO({
        url,
        target_keywords: parsedKeywords.length ? parsedKeywords : undefined,
        analyze_images: analyzeImages,
        analyze_content_quality: analyzeContentQuality
      });
      setResult(res);
      respond({ success: true, url, targetKeywords: parsedKeywords, analyzeImages, analyzeContentQuality, result: res });
    } catch (e: any) {
      setError(e?.message || 'Failed to analyze on-page SEO');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>On-page SEO analysis</div>
      <div style={{ marginBottom: 8, fontSize: 12, color: '#555' }}>URL: {url || 'Not available'}</div>
      <div style={{ marginBottom: 8 }}>
        <div style={{ fontSize: 12, marginBottom: 4 }}>Target keywords (comma-separated)</div>
        <input type="text" value={keywords} onChange={(e) => setKeywords(e.target.value)} style={{ width: '100%', padding: 6, fontSize: 12 }} />
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 12 }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={analyzeImages} onChange={(e) => setAnalyzeImages(e.target.checked)} />
          Analyze images
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={analyzeContentQuality} onChange={(e) => setAnalyzeContentQuality(e.target.checked)} />
          Analyze content quality
        </label>
      </div>
      <button onClick={run} disabled={isRunning} style={{ padding: '6px 10px' }}>{isRunning ? 'Analyzing…' : 'Run analysis'}</button>
      {error && <div style={{ marginTop: 10, color: '#c33', fontSize: 12 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 12, fontSize: 12 }}>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

const RegisterOnPage: React.FC = () => {
  const execute = useExecute();
  const useAction = useCopilotActionTyped();

  useAction({
    name: 'analyzeOnPageSEO',
    description: 'Analyze on-page SEO elements and provide optimization recommendations',
    parameters: [
      { name: 'url', type: 'string', description: 'URL to analyze (optional)', required: false },
      { name: 'targetKeywords', type: 'string[]', description: 'Target keywords (optional)', required: false },
      { name: 'analyzeImages', type: 'boolean', description: 'Analyze images', required: false },
      { name: 'analyzeContentQuality', type: 'boolean', description: 'Analyze content quality', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <OnPageUI args={args} respond={respond} />,
    handler: async (args: any) => {
      const url = args?.url || getDefaultUrl();
      return await execute('analyzeOnPageSEO', { ...args, url });
    }
  });

  return null;
};

export default RegisterOnPage;

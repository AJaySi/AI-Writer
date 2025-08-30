import React from 'react';
import { useCopilotActionTyped, useExecute, getDefaultUrl } from './helpers';
import { seoApiService } from '../../../services/seoApiService';

const SitemapUI: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [analyzeContentTrends, setAnalyzeContentTrends] = React.useState<boolean>(!!args?.analyzeContentTrends);
  const [analyzePublishingPatterns, setAnalyzePublishingPatterns] = React.useState<boolean>(!!args?.analyzePublishingPatterns);
  const [isRunning, setIsRunning] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);
  const url = args?.url || getDefaultUrl();

  const run = async () => {
    try {
      setIsRunning(true);
      setError(null);
      if (!url) throw new Error('No URL available');
      const res = await seoApiService.analyzeSitemap({
        sitemap_url: url,
        analyze_content_trends: analyzeContentTrends,
        analyze_publishing_patterns: analyzePublishingPatterns
      });
      setResult(res);
      respond({ success: true, url, analyzeContentTrends, analyzePublishingPatterns, result: res });
    } catch (e: any) {
      setError(e?.message || 'Failed to analyze sitemap');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Sitemap analysis</div>
      <div style={{ marginBottom: 8, fontSize: 12, color: '#555' }}>URL: {url || 'Not available'}</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 12 }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={analyzeContentTrends} onChange={(e) => setAnalyzeContentTrends(e.target.checked)} />
          Analyze content trends
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={analyzePublishingPatterns} onChange={(e) => setAnalyzePublishingPatterns(e.target.checked)} />
          Analyze publishing patterns
        </label>
      </div>
      <button onClick={run} disabled={isRunning} style={{ padding: '6px 10px' }}>
        {isRunning ? 'Analyzing…' : 'Run analysis'}
      </button>
      {error && <div style={{ marginTop: 10, color: '#c33', fontSize: 12 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 12, fontSize: 12 }}>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

const RegisterSitemap: React.FC = () => {
  const execute = useExecute();
  const useAction = useCopilotActionTyped();

  useAction({
    name: 'analyzeSitemap',
    description: 'Analyze and optimize sitemap structure and content',
    parameters: [
      { name: 'url', type: 'string', description: 'Website URL (optional)', required: false },
      { name: 'analyzeContentTrends', type: 'boolean', description: 'Analyze content trends', required: false },
      { name: 'analyzePublishingPatterns', type: 'boolean', description: 'Analyze publishing patterns', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <SitemapUI args={args} respond={respond} />,
    handler: async (args: any) => {
      const url = args?.url || getDefaultUrl();
      return await execute('analyzeSitemap', { ...args, url });
    }
  });

  return null;
};

export default RegisterSitemap;

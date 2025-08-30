import React from 'react';
import { useCopilotActionTyped, useExecute, getDefaultUrl } from './helpers';
import { seoApiService } from '../../../services/seoApiService';

const PageSpeedUI: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [device, setDevice] = React.useState<string>(args?.device || 'mobile');
  const [isRunning, setIsRunning] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);
  const url = args?.url || getDefaultUrl();

  const run = async () => {
    try {
      setIsRunning(true);
      setError(null);
      if (!url) throw new Error('No URL available');
      if (device === 'both') {
        const [mobile, desktop] = await Promise.all([
          seoApiService.analyzePageSpeed({ url, strategy: 'MOBILE' }),
          seoApiService.analyzePageSpeed({ url, strategy: 'DESKTOP' })
        ]);
        setResult({ mobile, desktop });
        respond({ success: true, url, device: 'both', mobile, desktop });
      } else if (device === 'desktop') {
        const desktop = await seoApiService.analyzePageSpeed({ url, strategy: 'DESKTOP' });
        setResult({ desktop });
        respond({ success: true, url, device: 'desktop', desktop });
      } else {
        const mobile = await seoApiService.analyzePageSpeed({ url, strategy: 'MOBILE' });
        setResult({ mobile });
        respond({ success: true, url, device: 'mobile', mobile });
      }
    } catch (e: any) {
      setError(e?.message || 'Failed to run page speed analysis');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>PageSpeed analysis</div>
      <div style={{ marginBottom: 8, fontSize: 12, color: '#555' }}>URL: {url || 'Not available'}</div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        {['mobile', 'desktop', 'both'].map((d) => (
          <label key={d} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <input type="radio" name="device" value={d} checked={device === d} onChange={() => setDevice(d)} />
            {d}
          </label>
        ))}
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

const RegisterPageSpeed: React.FC = () => {
  const execute = useExecute();
  const useAction = useCopilotActionTyped();

  useAction({
    name: 'analyzePageSpeed',
    description: 'Analyze website performance and page speed metrics',
    parameters: [
      { name: 'url', type: 'string', description: 'URL to analyze (optional)', required: false },
      { name: 'device', type: 'string', description: 'mobile | desktop | both (optional)', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <PageSpeedUI args={args} respond={respond} />,
    handler: async (args: any) => {
      const url = args?.url || getDefaultUrl();
      const device = args?.device || 'MOBILE';
      return await execute('analyzePageSpeed', { ...args, url, device });
    }
  });

  return null;
};

export default RegisterPageSpeed;

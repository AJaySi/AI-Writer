import React from 'react';
import { useCopilotActionTyped, useExecute, getDefaultUrl } from './helpers';
import { seoApiService } from '../../../services/seoApiService';

const TechnicalUI: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [scope, setScope] = React.useState<string>(args?.scope || 'full');
  const [isRunning, setIsRunning] = React.useState(false);
  const [result, setResult] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);
  const url = args?.url || getDefaultUrl();

  const run = async () => {
    try {
      setIsRunning(true);
      setError(null);
      if (!url) throw new Error('No URL available');
      const flags =
        scope === 'full'
          ? { analyze_core_web_vitals: true, analyze_mobile_friendliness: true, analyze_security: true }
          : {
              analyze_core_web_vitals: scope === 'core_web_vitals',
              analyze_mobile_friendliness: scope === 'mobile_friendliness',
              analyze_security: scope === 'security'
            };
      const res = await seoApiService.analyzeTechnicalSEO({ url, ...flags });
      setResult(res);
      respond({ success: true, url, scope, result: res });
    } catch (e: any) {
      setError(e?.message || 'Failed to run technical SEO audit');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Technical SEO audit</div>
      <div style={{ marginBottom: 8, fontSize: 12, color: '#555' }}>URL: {url || 'Not available'}</div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        {['full', 'core_web_vitals', 'mobile_friendliness', 'security'].map((s) => (
          <label key={s} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <input type="radio" name="scope" value={s} checked={scope === s} onChange={() => setScope(s)} />
            {s.replaceAll('_', ' ')}
          </label>
        ))}
      </div>
      <button onClick={run} disabled={isRunning} style={{ padding: '6px 10px' }}>{isRunning ? 'Auditing…' : 'Run audit'}</button>
      {error && <div style={{ marginTop: 10, color: '#c33', fontSize: 12 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 12, fontSize: 12 }}>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

const RegisterTechnical: React.FC = () => {
  const execute = useExecute();
  const useAction = useCopilotActionTyped();

  useAction({
    name: 'analyzeTechnicalSEO',
    description: 'Perform technical SEO audit and provide technical recommendations',
    parameters: [
      { name: 'url', type: 'string', description: 'URL to analyze (optional)', required: false },
      { name: 'scope', type: 'string', description: 'full | core_web_vitals | mobile_friendliness | security', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <TechnicalUI args={args} respond={respond} />,
    handler: async (args: any) => {
      const url = args?.url || getDefaultUrl();
      const scope = args?.scope || 'full';
      const flags =
        scope === 'full'
          ? { analyze_core_web_vitals: true, analyze_mobile_friendliness: true, analyze_security: true }
          : {
              analyze_core_web_vitals: scope === 'core_web_vitals',
              analyze_mobile_friendliness: scope === 'mobile_friendliness',
              analyze_security: scope === 'security'
            };
      return await execute('analyzeTechnicalSEO', { ...args, url, ...flags });
    }
  });

  return null;
};

export default RegisterTechnical;

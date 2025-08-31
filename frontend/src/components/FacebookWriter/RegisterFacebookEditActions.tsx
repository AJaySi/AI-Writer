import React from 'react';
import { useCopilotAction } from '@copilotkit/react-core';

const useCopilotActionTyped = useCopilotAction as any;

const EditHITL: React.FC<{ args: any; respond: (data: any) => void }> = ({ args, respond }) => {
  const [op, setOp] = React.useState<string>(args?.operation || 'Casual');
  const [loading, setLoading] = React.useState(false);

  const apply = async () => {
    setLoading(true);
    window.dispatchEvent(new CustomEvent('fbwriter:applyEdit', { detail: { operation: op } }));
    respond({ success: true, applied: op });
    setLoading(false);
  };

  const ops = ['Casual', 'Professional', 'Upbeat', 'Shorten', 'Lengthen', 'TightenHook', 'AddCTA'];

  return (
    <div style={{ padding: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Edit Draft</div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 8 }}>
        {ops.map(o => (
          <label key={o} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <input type="radio" name="op" value={o} checked={op === o} onChange={() => setOp(o)} />
            {o}
          </label>
        ))}
      </div>
      <button onClick={apply} disabled={loading}>{loading ? 'Applying…' : 'Apply'}</button>
    </div>
  );
};

const RegisterFacebookEditActions: React.FC = () => {
  useCopilotActionTyped({
    name: 'editFacebookDraft',
    description: 'Edit the current Facebook draft (style or structure)',
    parameters: [
      { name: 'operation', type: 'string', description: 'Casual | Professional | Upbeat | Shorten | Lengthen | TightenHook | AddCTA', required: false }
    ],
    renderAndWaitForResponse: ({ args, respond }: any) => <EditHITL args={args} respond={respond} />,
    handler: async (args: any) => {
      const op = args?.operation || 'Casual';
      window.dispatchEvent(new CustomEvent('fbwriter:applyEdit', { detail: { operation: op } }));
      return { success: true, applied: op };
    }
  });

  return null;
};

export default RegisterFacebookEditActions;



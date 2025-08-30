import { useCopilotAction } from '@copilotkit/react-core';
import useSEOCopilotStore from '../../../stores/seoCopilotStore';

export const useExecute = () => useSEOCopilotStore(s => s.executeCopilotAction);
export const getDefaultUrl = () => useSEOCopilotStore.getState().analysisData?.url;
export const useCopilotActionTyped = () => (useCopilotAction as any);

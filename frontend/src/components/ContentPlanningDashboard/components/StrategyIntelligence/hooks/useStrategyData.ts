import { useState, useEffect } from 'react';
import { contentPlanningApi } from '../../../../../services/contentPlanningApi';
import { StrategyData } from '../types/strategy.types';
import { 
  getUserId, 
  transformPollingStrategyData, 
  transformFullStructureData, 
  transformSwotToComprehensiveStructure,
  hasFullStructure 
} from '../utils/strategyTransformers';

export const useStrategyData = () => {
  const [strategyData, setStrategyData] = useState<StrategyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadStrategyData = async (forceRefresh = false) => {
    try {
      setLoading(true);
      setError(null);
      
      const userId = getUserId();
      
      // First, try to get the latest generated strategy from the polling system
      try {
        const latestStrategyResponse = await contentPlanningApi.getLatestGeneratedStrategy(userId);
        
        console.log('🔍 Latest strategy response from API:', latestStrategyResponse);
        console.log('🔍 Response type:', typeof latestStrategyResponse);
        console.log('🔍 Response keys:', Object.keys(latestStrategyResponse || {}));
        
        if (latestStrategyResponse && latestStrategyResponse.strategic_insights) {
          // If the response itself is the strategy data (after API extraction)
          console.log('✅ Found latest generated strategy (direct response):', latestStrategyResponse);
          console.log('🔍 Direct response keys:', Object.keys(latestStrategyResponse));
          
          const transformedStrategy = transformPollingStrategyData(latestStrategyResponse);
          
          console.log('🔄 Transformed strategy data:', transformedStrategy);
          setStrategyData(transformedStrategy);
          setLoading(false);
          return;
        } else {
          console.log('❌ No strategy data found in response');
        }
      } catch (pollingError) {
        console.log('No latest strategy found in polling system, checking database...', pollingError);
      }
      
      // If no strategy found in polling system, try to get from database
      try {
        const strategiesResponse = await contentPlanningApi.getEnhancedStrategies(userId);
        
        // Handle the enhanced strategies response structure
        const strategies = strategiesResponse?.data?.strategies || strategiesResponse?.strategies || [];
        
        if (strategies && strategies.length > 0) {
          // Get the most recent strategy (assuming it's sorted by creation date)
          const latestStrategy = strategies[0];
          
          // Check if this strategy has comprehensive AI-generated data
          if (latestStrategy.comprehensive_ai_analysis) {
            console.log('✅ Found comprehensive strategy in database:', latestStrategy);
            console.log('📊 Comprehensive AI analysis structure:', latestStrategy.comprehensive_ai_analysis);
            console.log('🔍 Available fields:', Object.keys(latestStrategy.comprehensive_ai_analysis));
            
            // Check if this is the full 5-component structure or SWOT analysis
            if (hasFullStructure(latestStrategy.comprehensive_ai_analysis)) {
              // Transform the data to match frontend expectations (full 5-component structure)
              const transformedStrategy = transformFullStructureData(latestStrategy);
              
              console.log('🔄 Transformed enhanced strategy data (full structure):', transformedStrategy);
              console.log('🎯 Final strategy data structure:', {
                hasStrategicInsights: !!transformedStrategy.strategic_insights,
                hasCompetitiveAnalysis: !!transformedStrategy.competitive_analysis,
                hasPerformancePredictions: !!transformedStrategy.performance_predictions,
                hasImplementationRoadmap: !!transformedStrategy.implementation_roadmap,
                hasRiskAssessment: !!transformedStrategy.risk_assessment,
                hasSummary: !!transformedStrategy.summary
              });
              setStrategyData(transformedStrategy);
              setLoading(false);
              return;
            } else {
              // This is SWOT analysis, create a comprehensive 5-component structure enhanced with SWOT data
              console.log('🔄 Creating comprehensive 5-component structure from SWOT analysis');
              
              const transformedStrategy = transformSwotToComprehensiveStructure(latestStrategy);
              
              console.log('🔄 Created comprehensive 5-component structure from SWOT analysis:', transformedStrategy);
              console.log('🎯 Final strategy data structure:', {
                hasStrategicInsights: !!transformedStrategy.strategic_insights,
                hasCompetitiveAnalysis: !!transformedStrategy.competitive_analysis,
                hasPerformancePredictions: !!transformedStrategy.performance_predictions,
                hasImplementationRoadmap: !!transformedStrategy.implementation_roadmap,
                hasRiskAssessment: !!transformedStrategy.risk_assessment,
                hasSummary: !!transformedStrategy.summary,
                swotEnhanced: true
              });
              setStrategyData(transformedStrategy);
              setLoading(false);
              return;
            }
          } else {
            console.log('⚠️ Strategy found but no comprehensive_ai_analysis field:', {
              strategyId: latestStrategy.id,
              strategyName: latestStrategy.name,
              availableFields: Object.keys(latestStrategy)
            });
          }
        }
      } catch (dbError) {
        console.log('No comprehensive strategies found in database, checking for recent generation...', dbError);
      }
      
      // If no comprehensive strategy found in database, check for recent generation tasks
      try {
        // Try to get the latest strategy generation result
        const recentStrategies = await contentPlanningApi.getStrategies(userId);
        
        // Handle the enhanced strategies response structure
        const strategies = recentStrategies?.data?.strategies || recentStrategies?.strategies || [];
        
        if (strategies && strategies.length > 0) {
          // Find the most recent AI-generated strategy
          const aiGeneratedStrategy = strategies.find(
            (strategy: any) => strategy.comprehensive_ai_analysis
          );
          
          if (aiGeneratedStrategy && aiGeneratedStrategy.comprehensive_ai_analysis) {
            console.log('✅ Found AI-generated strategy in recent strategies:', aiGeneratedStrategy);
            
            // Transform the data to match frontend expectations
            const transformedStrategy = transformPollingStrategyData(aiGeneratedStrategy.comprehensive_ai_analysis);
            
            console.log('🔄 Transformed recent strategy data:', transformedStrategy);
            setStrategyData(transformedStrategy);
            setLoading(false);
            return;
          }
        }
      } catch (strategyError) {
        console.log('No recent strategies found, checking for generation tasks...', strategyError);
      }
      
      // If no strategy data is available, show appropriate message
      console.log('❌ No comprehensive strategy data found');
      setStrategyData(null);
      setError('No comprehensive strategy data available. Please generate a strategy first.');
      setLoading(false);
      
    } catch (err: any) {
      console.error('Error loading strategy data:', err);
      setError(err.message || 'Failed to load strategy data');
      setStrategyData(null);
      setLoading(false);
    }
  };

  // Load data on mount and when component becomes visible
  useEffect(() => {
    // Always refresh data when component mounts to ensure we get the latest strategy
    loadStrategyData(true);
    
    // Also set up a listener for when the tab becomes visible (for better UX)
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        // Tab became visible, refresh data
        loadStrategyData(true);
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return {
    strategyData,
    loading,
    error,
    loadStrategyData
  };
}; 
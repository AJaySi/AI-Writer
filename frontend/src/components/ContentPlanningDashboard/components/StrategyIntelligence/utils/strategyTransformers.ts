import { StrategyData } from '../types/strategy.types';

// Helper function to get user ID from context or store
export const getUserId = (): number => {
  // TODO: Replace with actual user context/store
  // For now, return default user ID
  return 1;
};

/**
 * Transform polling system strategy data to frontend format
 */
export const transformPollingStrategyData = (strategyData: any): StrategyData => {
  console.log('🔄 Transforming polling strategy data:', strategyData);
  console.log('🔄 Strategy data type:', typeof strategyData);
  console.log('🔄 Strategy data keys:', Object.keys(strategyData || {}));
  
  // Extract the actual strategy components from the backend structure
  const strategicInsights = strategyData.strategic_insights;
  const competitiveAnalysis = strategyData.competitive_analysis;
  const performancePredictions = strategyData.performance_predictions;
  const implementationRoadmap = strategyData.implementation_roadmap;
  const riskAssessment = strategyData.risk_assessment;
  
  console.log('📊 Extracted components:', {
    hasStrategicInsights: !!strategicInsights,
    hasCompetitiveAnalysis: !!competitiveAnalysis,
    hasPerformancePredictions: !!performancePredictions,
    hasImplementationRoadmap: !!implementationRoadmap,
    hasRiskAssessment: !!riskAssessment
  });

  console.log('🔍 Strategic Insights Raw Data:', strategicInsights);
  console.log('🔍 Competitive Analysis Raw Data:', competitiveAnalysis);
  console.log('🔍 Performance Predictions Raw Data:', performancePredictions);
  console.log('🔍 Implementation Roadmap Raw Data:', implementationRoadmap);
  console.log('🔍 Risk Assessment Raw Data:', riskAssessment);

  const transformedData = {
    // Map metadata
    strategy_metadata: strategyData.metadata || strategyData.strategy_metadata,
    metadata: strategyData.metadata || strategyData.strategy_metadata,
    
    // Transform Strategic Insights - map the actual backend structure
    strategic_insights: strategicInsights ? {
      market_positioning: {
        positioning_strength: strategicInsights.market_positioning?.positioning_strength || 75,
        current_position: strategicInsights.market_positioning?.current_position || "Emerging",
        swot_analysis: {
          strengths: strategicInsights.market_positioning?.swot_analysis?.strengths || [],
          opportunities: strategicInsights.market_positioning?.swot_analysis?.opportunities || []
        }
      },
      content_opportunities: strategicInsights.content_opportunities || [],
      growth_potential: {
        market_size: strategicInsights.growth_potential?.market_size || "Growing",
        growth_rate: strategicInsights.growth_potential?.growth_rate || "High",
        key_drivers: strategicInsights.growth_potential?.key_drivers || [],
        competitive_advantages: strategicInsights.growth_potential?.competitive_advantages || []
      },
      swot_summary: {
        overall_score: strategicInsights.swot_summary?.overall_score || 75,
        primary_strengths: strategicInsights.swot_summary?.primary_strengths || [],
        key_opportunities: strategicInsights.swot_summary?.key_opportunities || []
      },
      // Add insights array if it exists in the backend data
      insights: strategicInsights.insights || []
    } : undefined,
    
    // Transform Competitive Analysis - map the actual backend structure
    competitive_analysis: competitiveAnalysis ? {
      competitors: competitiveAnalysis.competitors || [],
      market_gaps: competitiveAnalysis.market_gaps || [],
      opportunities: competitiveAnalysis.opportunities || [],
      recommendations: competitiveAnalysis.recommendations || [],
      competitive_advantages: {
        primary: competitiveAnalysis.competitive_advantages?.primary || [],
        sustainable: competitiveAnalysis.competitive_advantages?.sustainable || [],
        development_areas: competitiveAnalysis.competitive_advantages?.development_areas || []
      },
      swot_competitive_insights: {
        leverage_strengths: competitiveAnalysis.swot_competitive_insights?.leverage_strengths || [],
        address_weaknesses: competitiveAnalysis.swot_competitive_insights?.address_weaknesses || [],
        capitalize_opportunities: competitiveAnalysis.swot_competitive_insights?.capitalize_opportunities || [],
        mitigate_threats: competitiveAnalysis.swot_competitive_insights?.mitigate_threats || []
      }
    } : undefined,
    
    // Transform Performance Predictions - map the actual backend structure
    performance_predictions: performancePredictions ? {
      estimated_roi: performancePredictions.estimated_roi || "15-25%",
      key_metrics: {
        engagement_rate: performancePredictions.engagement_metrics?.time_on_page || "3-5 minutes",
        conversion_rate: performancePredictions.conversion_predictions?.lead_generation || "5-8%",
        reach_growth: performancePredictions.traffic_growth?.month_12 || "100%",
        brand_awareness: performancePredictions.engagement_metrics?.social_shares || "15-25 per post",
        market_share: performancePredictions.success_probability || "85%"
      },
      timeline_projections: {
        "month_1": "Initial setup and content creation",
        "month_3": performancePredictions.traffic_growth?.month_3 || "25% growth",
        "month_6": performancePredictions.traffic_growth?.month_6 || "50% growth",
        "month_12": performancePredictions.traffic_growth?.month_12 || "100% growth"
      },
      success_factors: {
        primary: performancePredictions.conversion_predictions ? [
          `Lead generation: ${performancePredictions.conversion_predictions.lead_generation}`,
          `Email signups: ${performancePredictions.conversion_predictions.email_signups}`,
          `Content downloads: ${performancePredictions.conversion_predictions.content_downloads}`
        ] : [],
        secondary: performancePredictions.engagement_metrics ? [
          `Time on page: ${performancePredictions.engagement_metrics.time_on_page}`,
          `Bounce rate: ${performancePredictions.engagement_metrics.bounce_rate}`
        ] : [],
        risk_mitigation: performancePredictions.success_probability ? [
          `Success probability: ${performancePredictions.success_probability}`
        ] : []
      },
      swot_based_predictions: {
        strength_impact: "High positive impact from identified strengths",
        opportunity_impact: "Significant growth potential from market opportunities",
        weakness_mitigation: "Addressing weaknesses through strategic content planning",
        threat_management: "Proactive threat management through diversified approach"
      }
    } : undefined,
    
    // Transform Implementation Roadmap - map the actual backend structure
    implementation_roadmap: implementationRoadmap ? {
      timeline: implementationRoadmap.timeline || "12 months",
      phases: implementationRoadmap.phases || [],
      milestones: implementationRoadmap.milestones || [],
      resource_requirements: implementationRoadmap.resource_requirements || [],
      critical_path: implementationRoadmap.critical_path || [],
      success_metrics: implementationRoadmap.success_metrics || [],
      timeline_object: {
        start_date: "2024-09-01",
        end_date: "2025-08-31",
        key_milestones: implementationRoadmap.milestones || []
      },
      resource_allocation: {
        team_members: implementationRoadmap.resource_requirements || [],
        team_requirements: implementationRoadmap.resource_requirements || [],
        budget_allocation: {
          total_budget: "$60,000",
          content_creation: "$30,000",
          technology_tools: "$5,000",
          marketing_promotion: "$20,000",
          external_resources: "$5,000"
        },
        swot_priorities: {
          high_priority: implementationRoadmap.success_metrics?.slice(0, 3) || [],
          medium_priority: implementationRoadmap.success_metrics?.slice(3, 6) || [],
          low_priority: implementationRoadmap.success_metrics?.slice(6, 9) || []
        }
      }
    } : undefined,
    
    // Transform Risk Assessment - map the actual backend structure
    risk_assessment: riskAssessment ? {
      overall_risk_level: riskAssessment.overall_risk_level || "Medium",
      risks: riskAssessment.risks || [],
      risk_categories: {
        market_risks: riskAssessment.risk_categories?.market_risks || [],
        operational_risks: riskAssessment.risk_categories?.operational_risks || [],
        competitive_risks: riskAssessment.risk_categories?.competitive_risks || [],
        technical_risks: riskAssessment.risk_categories?.technical_risks || [],
        financial_risks: riskAssessment.risk_categories?.financial_risks || []
      }
    } : undefined,
    
    // Add summary
    summary: strategyData.summary || {
      estimated_roi: performancePredictions?.estimated_roi || "15-25%",
      implementation_timeline: implementationRoadmap?.timeline || "12 months",
      risk_level: riskAssessment?.overall_risk_level || "Medium",
      success_probability: performancePredictions?.success_probability || "85%",
      next_step: "Review strategy and generate content calendar"
    }
  };

  console.log('✅ Transformed Polling Strategy Data:', transformedData);
  return transformedData;
};

/**
 * Transform full 5-component structure from database
 */
export const transformFullStructureData = (latestStrategy: any): StrategyData => {
  const comprehensiveData = latestStrategy.comprehensive_ai_analysis;
  
  return {
    // Map metadata
    strategy_metadata: comprehensiveData.metadata || comprehensiveData.strategy_metadata,
    metadata: comprehensiveData.metadata || comprehensiveData.strategy_metadata,
    
    // Transform Strategic Insights
    strategic_insights: comprehensiveData.strategic_insights ? {
      market_positioning: {
        positioning_strength: 75, // Default value
        current_position: "Emerging",
        swot_analysis: {
          strengths: [],
          opportunities: []
        }
      },
      content_opportunities: comprehensiveData.strategic_insights.insights?.filter((insight: any) => 
        insight.type === 'Content Opportunity'
      ).map((insight: any) => insight.insight) || [],
      growth_potential: {
        market_size: "Growing",
        growth_rate: "High",
        key_drivers: comprehensiveData.strategic_insights.insights?.filter((insight: any) => 
          insight.type === 'Growth Potential'
        ).map((insight: any) => insight.insight) || [],
        competitive_advantages: []
      },
      swot_summary: {
        overall_score: 75,
        primary_strengths: comprehensiveData.strategic_insights.insights?.slice(0, 2) || [],
        key_opportunities: comprehensiveData.strategic_insights.insights?.slice(2, 4) || []
      },
      // Map the insights array directly
      insights: comprehensiveData.strategic_insights.insights || []
    } : undefined,
    
    // Transform Competitive Analysis
    competitive_analysis: comprehensiveData.competitive_analysis ? {
      competitors: comprehensiveData.competitive_analysis.competitors || [],
      market_gaps: comprehensiveData.competitive_analysis.market_gaps || [],
      opportunities: comprehensiveData.competitive_analysis.opportunities || [],
      recommendations: comprehensiveData.competitive_analysis.recommendations || [],
      competitive_advantages: {
        primary: comprehensiveData.competitive_analysis.recommendations?.slice(0, 3) || [],
        sustainable: comprehensiveData.competitive_analysis.recommendations?.slice(3, 5) || [],
        development_areas: comprehensiveData.competitive_analysis.opportunities || []
      },
      swot_competitive_insights: {
        leverage_strengths: comprehensiveData.competitive_analysis.recommendations?.slice(0, 2) || [],
        address_weaknesses: comprehensiveData.competitive_analysis.recommendations?.slice(2, 4) || [],
        capitalize_opportunities: comprehensiveData.competitive_analysis.opportunities?.slice(0, 2) || [],
        mitigate_threats: comprehensiveData.competitive_analysis.recommendations?.slice(4, 6) || []
      }
    } : undefined,
    
    // Transform Performance Predictions
    performance_predictions: comprehensiveData.performance_predictions ? {
      estimated_roi: comprehensiveData.performance_predictions.roi_predictions?.estimated_roi || "15-25%",
      key_metrics: {
        engagement_rate: comprehensiveData.performance_predictions.engagement_predictions?.engagement_rate || "8-12%",
        conversion_rate: comprehensiveData.performance_predictions.conversion_predictions?.conversion_rate || "3-5%",
        reach_growth: comprehensiveData.performance_predictions.traffic_predictions?.traffic_growth || "40-60%",
        brand_awareness: comprehensiveData.performance_predictions.engagement_predictions?.brand_awareness || "25-35%",
        market_share: comprehensiveData.performance_predictions.roi_predictions?.market_share || "5-8%"
      },
      timeline_projections: {
        "month_1": comprehensiveData.performance_predictions.traffic_predictions?.month_1 || "Initial setup and content creation",
        "month_3": comprehensiveData.performance_predictions.engagement_predictions?.month_3 || "Content optimization and audience growth",
        "month_6": comprehensiveData.performance_predictions.conversion_predictions?.month_6 || "Full strategy implementation and scaling"
      },
      success_factors: {
        primary: comprehensiveData.performance_predictions.roi_predictions?.success_factors?.slice(0, 3) || [],
        secondary: comprehensiveData.performance_predictions.engagement_predictions?.success_factors?.slice(0, 2) || [],
        risk_mitigation: comprehensiveData.performance_predictions.conversion_predictions?.risk_mitigation?.slice(0, 2) || []
      },
      swot_based_predictions: {
        strength_impact: "High positive impact from identified strengths",
        opportunity_impact: "Significant growth potential from market opportunities",
        weakness_mitigation: "Addressing weaknesses through strategic content planning",
        threat_management: "Proactive threat management through diversified approach"
      }
    } : undefined,
    
    // Transform Implementation Roadmap
    implementation_roadmap: comprehensiveData.implementation_roadmap ? {
      timeline: comprehensiveData.implementation_roadmap.timeline || "6 months",
      phases: comprehensiveData.implementation_roadmap.phases || [],
      milestones: comprehensiveData.implementation_roadmap.milestones || [],
      resource_requirements: comprehensiveData.implementation_roadmap.resource_requirements || [],
      critical_path: comprehensiveData.implementation_roadmap.critical_path || [],
      success_metrics: comprehensiveData.implementation_roadmap.success_metrics || [],
      timeline_object: comprehensiveData.implementation_roadmap.timeline_object || {
        start_date: "2024-09-01",
        end_date: "2025-02-28",
        key_milestones: []
      },
      resource_allocation: {
        team_members: comprehensiveData.implementation_roadmap.resource_allocation?.team_members || 
                     comprehensiveData.implementation_roadmap.resource_allocation?.team_requirements || [],
        team_requirements: comprehensiveData.implementation_roadmap.resource_allocation?.team_requirements || 
                          comprehensiveData.implementation_roadmap.resource_allocation?.team_members || [],
        budget_allocation: comprehensiveData.implementation_roadmap.resource_allocation?.budget_allocation || {
          total_budget: "$60,000",
          content_creation: "$30,000",
          technology_tools: "$5,000",
          marketing_promotion: "$20,000",
          external_resources: "$5,000"
        },
        swot_priorities: {
          high_priority: comprehensiveData.implementation_roadmap.success_metrics?.slice(0, 3) || [],
          medium_priority: comprehensiveData.implementation_roadmap.success_metrics?.slice(3, 6) || [],
          low_priority: comprehensiveData.implementation_roadmap.success_metrics?.slice(6, 9) || []
        }
      }
    } : undefined,
    
    // Transform Risk Assessment
    risk_assessment: comprehensiveData.risk_assessment ? {
      overall_risk_level: comprehensiveData.risk_assessment.overall_risk_level || "Medium",
      risks: comprehensiveData.risk_assessment.risks || [],
      risk_categories: comprehensiveData.risk_assessment.risk_categories || {},
      monitoring_framework: comprehensiveData.risk_assessment.monitoring_framework || {
        escalation_procedures: [],
        key_indicators: [],
        monitoring_frequency: "Weekly for key performance metrics, Monthly for strategic content review, Quarterly for comprehensive analysis",
        review_schedule: "Monthly performance review meetings to discuss analytics and tactical adjustments. Quarterly strategic comprehensive review"
      },
      swot_risk_mapping: {
        strength_risks: "Leverage strengths to mitigate risks",
        weakness_risks: "Address weaknesses through strategic planning",
        opportunity_risks: "Capitalize on opportunities while managing risks",
        threat_risks: "Proactive threat management and contingency planning"
      },
      risk_mitigation_strategies: {
        based_on_strengths: comprehensiveData.risk_assessment.mitigation_strategies?.[0] || "Leverage identified strengths",
        based_on_opportunities: comprehensiveData.risk_assessment.mitigation_strategies?.[1] || "Capitalize on market opportunities",
        based_on_weaknesses: comprehensiveData.risk_assessment.mitigation_strategies?.[2] || "Address identified weaknesses",
        based_on_threats: comprehensiveData.risk_assessment.mitigation_strategies?.[3] || "Proactive threat management"
      },
      mitigation_strategies: comprehensiveData.risk_assessment.mitigation_strategies || []
    } : undefined,
    
    // Add summary
    summary: comprehensiveData.summary || {
      estimated_roi: comprehensiveData.performance_predictions?.roi_predictions?.estimated_roi || "15-25%",
      implementation_timeline: comprehensiveData.implementation_roadmap?.total_duration || "6 months",
      risk_level: comprehensiveData.risk_assessment?.overall_risk_level || "Medium",
      success_probability: "85%",
      next_step: "Review strategy and generate content calendar"
    }
  };
};

/**
 * Transform SWOT analysis into comprehensive 5-component structure
 */
export const transformSwotToComprehensiveStructure = (latestStrategy: any): StrategyData => {
  const swotData = latestStrategy.comprehensive_ai_analysis;
  
  return {
    strategy_metadata: {
      user_id: latestStrategy.user_id,
      strategy_name: latestStrategy.name,
      ai_generated: true,
      comprehensive: true,
      content_calendar_ready: false,
      generation_timestamp: latestStrategy.created_at
    },
    // Enhanced Strategic Insights with SWOT data
    strategic_insights: {
      market_positioning: {
        positioning_strength: swotData.overall_score || 75,
        current_position: "Emerging",
        swot_analysis: {
          strengths: swotData.strengths || [],
          opportunities: swotData.opportunities || []
        }
      },
      content_opportunities: [
        ...(swotData.opportunities || []),
        "Leverage identified market gaps",
        "Focus on unique value propositions",
        "Build thought leadership content"
      ],
      growth_potential: {
        market_size: "Growing",
        growth_rate: "High",
        key_drivers: swotData.opportunities || [],
        competitive_advantages: swotData.strengths || []
      },
      swot_summary: {
        overall_score: swotData.overall_score || 75,
        primary_strengths: (swotData.strengths || []).slice(0, 3),
        key_opportunities: (swotData.opportunities || []).slice(0, 3)
      }
    },
    // Enhanced Competitive Analysis with SWOT data
    competitive_analysis: {
      competitors: [
        {
          name: "Direct Competitors",
          market_position: "Established",
          strengths: swotData.strengths || [],
          weaknesses: swotData.weaknesses || [],
          competitive_response: "Focus on differentiation"
        },
        {
          name: "Emerging Competitors",
          market_position: "Growing",
          strengths: [],
          weaknesses: swotData.weaknesses || [],
          competitive_response: "Establish market leadership"
        }
      ],
      market_gaps: [
        ...(swotData.opportunities || []),
        "Content personalization opportunities",
        "Niche market segments",
        "Innovation in content delivery"
      ],
      competitive_advantages: {
        primary: swotData.strengths || [],
        sustainable: swotData.opportunities || [],
        development_areas: swotData.weaknesses || []
      },
      swot_competitive_insights: {
        leverage_strengths: swotData.strengths || [],
        address_weaknesses: swotData.weaknesses || [],
        capitalize_opportunities: swotData.opportunities || [],
        mitigate_threats: swotData.threats || []
      }
    },
    // Enhanced Performance Predictions with SWOT context
    performance_predictions: {
      estimated_roi: "20-30%",
      key_metrics: {
        engagement_rate: "5-8%",
        conversion_rate: "2-4%",
        reach_growth: "40-60%",
        brand_awareness: "25-35%",
        market_share: "3-5%"
      },
      timeline_projections: {
        "3_months": "Initial traction and brand awareness leveraging identified strengths",
        "6_months": "Established presence and engagement addressing market opportunities",
        "12_months": "Market leadership and growth capitalizing on competitive advantages"
      },
      success_factors: {
        primary: swotData.strengths || [],
        secondary: swotData.opportunities || [],
        risk_mitigation: swotData.threats || []
      },
      swot_based_predictions: {
        strength_impact: "High performance in areas of identified strengths",
        opportunity_impact: "Growth potential through market opportunities",
        weakness_mitigation: "Improved performance by addressing weaknesses",
        threat_management: "Risk-adjusted projections considering market threats"
      }
    },
    // Enhanced Implementation Roadmap with SWOT considerations
    implementation_roadmap: {
      timeline: "12 months",
      phases: [
        {
          phase: "Foundation (Months 1-3)",
          duration: "3 months",
          tasks: [
            "Brand positioning leveraging identified strengths",
            "Content strategy development addressing market opportunities",
            "Weakness assessment and improvement planning"
          ],
          milestones: ["Brand guidelines", "Content calendar", "SWOT action plan"],
          resources: ["Content Strategist", "Brand Manager", "SWOT Analyst"],
          swot_focus: "Strengths and Opportunities"
        },
        {
          phase: "Growth (Months 4-8)",
          duration: "5 months",
          tasks: [
            "Content execution based on competitive advantages",
            "Community building addressing market gaps",
            "Threat mitigation strategies implementation"
          ],
          milestones: ["Content library", "Engaged audience", "Risk management framework"],
          resources: ["Content Writer", "Community Manager", "Risk Analyst"],
          swot_focus: "Opportunities and Threats"
        },
        {
          phase: "Scale (Months 9-12)",
          duration: "4 months",
          tasks: [
            "Market expansion capitalizing on strengths",
            "Performance optimization addressing weaknesses",
            "Sustainable competitive advantage development"
          ],
          milestones: ["Market leadership", "Optimized strategy", "Long-term competitive position"],
          resources: ["Growth Manager", "Performance Analyst", "Strategy Consultant"],
          swot_focus: "Strengths and Weaknesses"
        }
      ],
      milestones: [
        "Brand guidelines", "Content calendar", "SWOT action plan",
        "Content library", "Engaged audience", "Risk management framework",
        "Market leadership", "Optimized strategy", "Long-term competitive position"
      ],
      resource_requirements: [
        "Content Strategist", "SEO Specialist", "Content Writer", "Editor", "Marketing Manager"
      ],
      critical_path: [
        "Brand positioning leveraging identified strengths",
        "Content execution based on competitive advantages",
        "Market expansion capitalizing on strengths"
      ],
      success_metrics: [
        "Brand guidelines", "Content calendar", "SWOT action plan",
        "Content library", "Engaged audience", "Risk management framework",
        "Market leadership", "Optimized strategy", "Long-term competitive position"
      ],
      timeline_object: {
        start_date: "2024-01-01",
        end_date: "2024-12-31",
        key_milestones: [
          "Brand guidelines", "Content calendar", "SWOT action plan",
          "Content library", "Engaged audience", "Risk management framework",
          "Market leadership", "Optimized strategy", "Long-term competitive position"
        ]
      },
      resource_allocation: {
        team_members: ["Content Strategist", "SEO Specialist", "Content Writer", "Editor", "Marketing Manager"],
        team_requirements: ["Content Strategist", "SEO Specialist", "Content Writer", "Editor", "Marketing Manager"],
        budget_allocation: {
          total_budget: "$60,000",
          content_creation: "$30,000",
          technology_tools: "$5,000",
          marketing_promotion: "$20,000",
          external_resources: "$5,000"
        },
        swot_priorities: {
          high_priority: swotData.opportunities || [],
          medium_priority: swotData.strengths || [],
          low_priority: swotData.weaknesses || []
        }
      }
    },
    // Enhanced Risk Assessment with SWOT threats
    risk_assessment: {
      overall_risk_level: "Medium",
      risks: [
        ...(swotData.threats?.map((threat: string) => ({
          risk: threat,
          probability: "Medium",
          impact: "High",
          mitigation: "Strategic planning and monitoring"
        })) || []),
        {
          risk: "Market saturation",
          probability: "Medium",
          impact: "Medium",
          mitigation: "Innovation and differentiation"
        }
      ],
      risk_categories: {
        market_risks: [
          ...(swotData.threats?.map((threat: string) => ({
            risk: threat,
            probability: "Medium",
            impact: "High",
            mitigation: "Strategic planning and monitoring"
          })) || []),
          {
            risk: "Market saturation",
            probability: "Medium",
            impact: "Medium",
            mitigation: "Innovation and differentiation"
          }
        ],
        operational_risks: [
          {
            risk: "Resource constraints",
            probability: "Medium",
            impact: "Medium",
            mitigation: "Efficient resource allocation"
          },
          {
            risk: "Weakness areas",
            probability: "High",
            impact: "Medium",
            mitigation: "Targeted improvement programs"
          }
        ],
        competitive_risks: [
          {
            risk: "Market competition",
            probability: "High",
            impact: "Medium",
            mitigation: "Leverage competitive advantages"
          },
          {
            risk: "Strength erosion",
            probability: "Medium",
            impact: "High",
            mitigation: "Continuous improvement and innovation"
          }
        ]
      },
      swot_risk_mapping: {
        strength_risks: "Risk of over-reliance on current strengths",
        weakness_risks: "Risk of weakness exploitation by competitors",
        opportunity_risks: "Risk of missing market opportunities",
        threat_risks: "Risk of threat materialization"
      },
      risk_mitigation_strategies: {
        based_on_strengths: "Leverage strengths to mitigate threats",
        based_on_opportunities: "Use opportunities to address weaknesses",
        based_on_weaknesses: "Develop improvement plans for weak areas",
        based_on_threats: "Create contingency plans for identified threats"
      },
      mitigation_strategies: swotData.mitigation_strategies || []
    },
    // Enhanced summary with SWOT context
    summary: {
      estimated_roi: "20-30%",
      implementation_timeline: "12 months",
      risk_level: "Medium",
      success_probability: `${swotData.overall_score || 75}%`,
      next_step: "Review strategy and generate content calendar",
      swot_highlights: {
        key_strengths: (swotData.strengths || []).slice(0, 2),
        key_opportunities: (swotData.opportunities || []).slice(0, 2),
        primary_risks: (swotData.threats || []).slice(0, 2)
      }
    }
  };
};

/**
 * Check if strategy data has full 5-component structure
 */
export const hasFullStructure = (comprehensiveAnalysis: any): boolean => {
  return !!(comprehensiveAnalysis.strategic_insights || 
           comprehensiveAnalysis.competitive_analysis ||
           comprehensiveAnalysis.performance_predictions);
};

/**
 * Get strategy name from metadata
 */
export const getStrategyName = (strategyData: StrategyData | null): string => {
  return strategyData?.strategy_metadata?.strategy_name || 
         strategyData?.metadata?.strategy_name || 
         'AI-Generated Strategy';
};

/**
 * Get strategy generation date
 */
export const getStrategyGenerationDate = (strategyData: StrategyData | null): string => {
  const timestamp = strategyData?.strategy_metadata?.generated_at || 
                   strategyData?.strategy_metadata?.generation_timestamp || 
                   strategyData?.metadata?.generated_at || 
                   strategyData?.metadata?.generation_timestamp || '';
  
  return new Date(timestamp).toLocaleDateString();
}; 
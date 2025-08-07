interface EducationalContent {
  title: string;
  description: string;
  points: string[];
  tips: string[];
}

export const getEducationalContent = (categoryId: string): EducationalContent => {
  switch (categoryId) {
    case 'business_context':
      return {
        title: 'Business Context',
        description: 'Understanding your business foundation is crucial for content strategy success.',
        points: [
          'Business objectives define what you want to achieve through content',
          'Target metrics help measure the success of your content strategy',
          'Content budget determines the scope and scale of your content efforts',
          'Team size affects content production capacity and frequency',
          'Implementation timeline sets realistic expectations for strategy rollout'
        ],
        tips: [
          'Be specific about your business goals',
          'Set measurable and achievable metrics',
          'Consider your available resources realistically'
        ]
      };
    case 'audience_intelligence':
      return {
        title: 'Audience Intelligence',
        description: 'Deep understanding of your audience drives content relevance and engagement.',
        points: [
          'Content preferences reveal what formats resonate with your audience',
          'Consumption patterns show when and how your audience engages',
          'Pain points help create content that solves real problems',
          'Buying journey mapping guides content at each stage',
          'Seasonal trends identify content opportunities throughout the year'
        ],
        tips: [
          'Research your audience thoroughly',
          'Create audience personas for better targeting',
          'Monitor engagement patterns regularly'
        ]
      };
    case 'competitive_intelligence':
      return {
        title: 'Competitive Intelligence',
        description: 'Understanding your competitive landscape helps differentiate your content.',
        points: [
          'Top competitors analysis reveals content gaps and opportunities',
          'Competitor strategies show what works in your industry',
          'Market gaps identify underserved content areas',
          'Industry trends keep your content current and relevant',
          'Emerging trends provide first-mover advantages'
        ],
        tips: [
          'Monitor competitors regularly',
          'Identify unique angles and perspectives',
          'Stay ahead of industry trends'
        ]
      };
    case 'content_strategy':
      return {
        title: 'Content Strategy',
        description: 'Your content approach defines how you\'ll achieve your business objectives.',
        points: [
          'Preferred formats align with audience preferences and business goals',
          'Content mix balances different types of content for maximum impact',
          'Content frequency should match audience expectations and team capacity',
          'Optimal timing maximizes content visibility and engagement',
          'Quality metrics ensure content meets audience standards'
        ],
        tips: [
          'Balance audience preferences with business goals',
          'Set realistic content production schedules',
          'Maintain consistent quality standards'
        ]
      };
    case 'performance_analytics':
      return {
        title: 'Performance & Analytics',
        description: 'Data-driven insights optimize your content strategy for better results.',
        points: [
          'Traffic sources show where your audience comes from',
          'Conversion rates measure content effectiveness',
          'ROI targets help justify content marketing investments',
          'A/B testing capabilities enable continuous optimization',
          'Regular analysis identifies improvement opportunities'
        ],
        tips: [
          'Track key metrics consistently',
          'Use data to inform content decisions',
          'Continuously optimize based on performance'
        ]
      };
    default:
      return {
        title: 'Category Information',
        description: 'Learn more about this content strategy category.',
        points: [],
        tips: []
      };
  }
}; 
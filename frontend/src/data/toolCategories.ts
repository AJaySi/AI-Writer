import React from 'react';
import {
  Article as ArticleIcon,
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  Campaign as CampaignIcon,
  Analytics as AnalyticsIcon,
  Psychology as PsychologyIcon,
  AutoAwesome as AutoAwesomeIcon,
  Speed as SpeedIcon,
  Business as BusinessIcon,
  SocialDistance as SocialIcon,
  Create as CreateIcon
} from '@mui/icons-material';
import { ToolCategories } from '../components/shared/types';

export const toolCategories: ToolCategories = {
  'AI Content Writers': {
    icon: React.createElement(ArticleIcon),
    color: '#4CAF50',
    gradient: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
    tools: [
      {
        name: 'AI Blog Writer',
        description: 'Generate engaging blog posts with AI',
        icon: React.createElement(ArticleIcon),
        status: 'active',
        path: '/ai-blog-writer',
        features: ['SEO Optimized', 'Multiple Formats', 'Custom Tone']
      },
      {
        name: 'AI Essay Writer',
        description: 'Academic and professional essay writing',
        icon: React.createElement(CreateIcon),
        status: 'active',
        path: '/ai-essay-writer',
        features: ['Academic Style', 'Citation Support', 'Plagiarism Free']
      },
      {
        name: 'AI News Article Writer',
        description: 'Professional news and article writing',
        icon: React.createElement(ArticleIcon),
        status: 'active',
        path: '/ai-news-writer',
        features: ['Fact-Checked', 'Journalistic Style', 'Breaking News']
      },
      {
        name: 'AI Story Writer',
        description: 'Creative storytelling and fiction writing',
        icon: React.createElement(CreateIcon),
        status: 'active',
        path: '/ai-story-writer',
        features: ['Creative Writing', 'Character Development', 'Plot Generation']
      },
      {
        name: 'AI Copywriter',
        description: 'Marketing copy and advertising content',
        icon: React.createElement(CampaignIcon),
        status: 'active',
        path: '/ai-copywriter',
        features: ['Persuasive Writing', 'Brand Voice', 'Call-to-Action']
      },
      {
        name: 'AI Product Description Writer',
        description: 'Compelling product descriptions',
        icon: React.createElement(BusinessIcon),
        status: 'active',
        path: '/ai-product-writer',
        features: ['E-commerce Optimized', 'Feature Highlighting', 'Conversion Focused']
      }
    ]
  },
  'SEO & Analytics': {
    icon: React.createElement(SearchIcon),
    color: '#2196F3',
    gradient: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
    subCategories: {
      'Enterprise & Advanced': {
        tools: [
          {
            name: 'SEO Dashboard',
            description: 'AI-powered SEO analysis and actionable insights',
            icon: React.createElement(AnalyticsIcon),
            status: 'premium',
            path: '/seo-dashboard',
            features: ['AI Insights', 'Performance Tracking', 'Actionable Recommendations'],
            isPinned: true,
            isHighlighted: true
          },
          {
            name: 'Content Planning Dashboard',
            description: 'AI-powered content strategy and planning with gap analysis',
            icon: React.createElement(PsychologyIcon),
            status: 'premium',
            path: '/content-planning',
            features: ['Content Strategy', 'Gap Analysis', 'AI Recommendations', 'Calendar Management'],
            isPinned: true,
            isHighlighted: true
          },
          {
            name: 'Enterprise SEO Suite',
            description: 'Unified workflow orchestration for comprehensive SEO management',
            icon: React.createElement(BusinessIcon),
            status: 'premium',
            path: '/enterprise-seo-suite',
            features: ['Complete Audits', 'AI Recommendations', 'Strategic Planning']
          },
          {
            name: 'Google Search Console Intelligence',
            description: 'Advanced GSC data analysis with AI-powered insights',
            icon: React.createElement(AnalyticsIcon),
            status: 'premium',
            path: '/gsc-intelligence',
            features: ['Content Opportunities', 'Search Intelligence', 'Competitive Analysis']
          },
          {
            name: 'AI Content Strategy Generator',
            description: 'Comprehensive content planning with market intelligence',
            icon: React.createElement(PsychologyIcon),
            status: 'premium',
            path: '/ai-content-strategy',
            features: ['Market Intelligence', 'Topic Clusters', 'Implementation Roadmaps']
          }
        ]
      },
      'Technical SEO Tools': {
        tools: [
          {
            name: 'On-Page SEO Analyzer',
            description: 'Comprehensive page-level SEO optimization analysis',
            icon: React.createElement(SearchIcon),
            status: 'active',
            path: '/on-page-seo-analyzer',
            features: ['Technical SEO', 'Content Analysis', 'Optimization Suggestions']
          },
          {
            name: 'Technical SEO Crawler',
            description: 'Site-wide technical analysis and performance metrics',
            icon: React.createElement(SpeedIcon),
            status: 'active',
            path: '/technical-seo-crawler',
            features: ['Crawl Analysis', 'Performance Metrics', 'AI Recommendations']
          },
          {
            name: 'Google PageSpeed Insights',
            description: 'Website performance and Core Web Vitals analysis',
            icon: React.createElement(SpeedIcon),
            status: 'active',
            path: '/pagespeed-insights',
            features: ['Core Web Vitals', 'Speed Optimization', 'Mobile Performance']
          },
          {
            name: 'URL SEO Checker',
            description: 'Individual URL analysis and optimization recommendations',
            icon: React.createElement(SearchIcon),
            status: 'active',
            path: '/url-seo-checker',
            features: ['Technical Factors', 'Optimization Tips', 'Detailed Reports']
          },
          {
            name: 'Sitemap Analysis',
            description: 'XML and HTML sitemap analysis and optimization',
            icon: React.createElement(SearchIcon),
            status: 'active',
            path: '/sitemap-analysis',
            features: ['Sitemap Validation', 'Structure Analysis', 'Optimization Tips']
          }
        ]
      },
      'AI & Analysis Tools': {
        tools: [
          {
            name: 'Content Gap Analysis',
            description: 'Advanced competitive content analysis and opportunities',
            icon: React.createElement(SearchIcon),
            status: 'active',
            path: '/content-gap-analysis',
            features: ['Competitive Analysis', 'AI Insights', 'Opportunity Identification']
          },
          {
            name: 'CGPT SEO Analyzer',
            description: 'AI-powered SEO analysis using advanced language models',
            icon: React.createElement(PsychologyIcon),
            status: 'active',
            path: '/cgpt-seo-analyzer',
            features: ['AI Analysis', 'Advanced Insights', 'Strategic Recommendations']
          },
          {
            name: 'Webpage Content Analysis',
            description: 'Deep content analysis and optimization insights',
            icon: React.createElement(ArticleIcon),
            status: 'active',
            path: '/webpage-content-analysis',
            features: ['Content Quality', 'Readability Analysis', 'Optimization Tips']
          },
          {
            name: 'WordCloud Generator',
            description: 'Visual keyword and content analysis with word clouds',
            icon: React.createElement(AnalyticsIcon),
            status: 'active',
            path: '/wordcloud-generator',
            features: ['Visual Analysis', 'Keyword Mapping', 'Content Insights']
          },
          {
            name: 'TextStat Analysis',
            description: 'Advanced text statistics and readability analysis',
            icon: React.createElement(AnalyticsIcon),
            status: 'active',
            path: '/textstat-analysis',
            features: ['Readability Metrics', 'Text Statistics', 'Content Optimization']
          }
        ]
      },
      'SEO Optimization Tools': {
        tools: [
          {
            name: 'SEO Analysis',
            description: 'Comprehensive SEO analysis and reporting',
            icon: React.createElement(AnalyticsIcon),
            status: 'active',
            path: '/seo-analysis',
            features: ['Complete Analysis', 'Detailed Reports', 'Actionable Insights']
          },
          {
            name: 'OpenGraph Generator',
            description: 'Social media optimization for Facebook and LinkedIn',
            icon: React.createElement(SocialIcon),
            status: 'active',
            path: '/opengraph-generator',
            features: ['Social Optimization', 'Visual Appeal', 'Click Enhancement']
          },
          {
            name: 'Schema Markup Generator',
            description: 'Structured data creation for rich snippets',
            icon: React.createElement(SearchIcon),
            status: 'active',
            path: '/schema-generator',
            features: ['Rich Snippets', 'Search Enhancement', 'Content Understanding']
          }
        ]
      }
    }
  },
  'Social Media': {
    icon: React.createElement(SocialIcon),
    color: '#FF9800',
    gradient: 'linear-gradient(135deg, #FF9800 0%, #F57C00 100%)',
    tools: [
      {
        name: 'Facebook Content Writer',
        description: 'Engaging Facebook posts and ads',
        icon: React.createElement(SocialIcon),
        status: 'active',
        path: '/facebook-writer',
        features: ['Engagement Focused', 'Ad Copy', 'Post Scheduling']
      },
      {
        name: 'LinkedIn Content Writer',
        description: 'Professional LinkedIn content',
        icon: React.createElement(BusinessIcon),
        status: 'active',
        path: '/linkedin-writer',
        features: ['Professional Tone', 'Thought Leadership', 'B2B Focus']
      },
      {
        name: 'Twitter Content Writer',
        description: 'Viral Twitter threads and tweets',
        icon: React.createElement(SocialIcon),
        status: 'active',
        path: '/twitter-writer',
        features: ['Viral Potential', 'Thread Creation', 'Hashtag Optimization']
      },
      {
        name: 'Instagram Content Writer',
        description: 'Visual and engaging Instagram content',
        icon: React.createElement(SocialIcon),
        status: 'active',
        path: '/instagram-writer',
        features: ['Visual Descriptions', 'Hashtag Strategy', 'Story Content']
      },
      {
        name: 'YouTube Content Writer',
        description: 'Video scripts and descriptions',
        icon: React.createElement(SocialIcon),
        status: 'active',
        path: '/youtube-writer',
        features: ['Video Scripts', 'SEO Descriptions', 'Engagement Hooks']
      }
    ]
  },
  'Business & Marketing': {
    icon: React.createElement(BusinessIcon),
    color: '#9C27B0',
    gradient: 'linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)',
    tools: [
      {
        name: 'Financial Report Generator',
        description: 'Professional financial analysis and reports',
        icon: React.createElement(AnalyticsIcon),
        status: 'active',
        path: '/financial-reports',
        features: ['Data Analysis', 'Professional Reports', 'Insights Generation']
      },
      {
        name: 'Email Templates',
        description: 'Professional email templates and campaigns',
        icon: React.createElement(CampaignIcon),
        status: 'active',
        path: '/email-templates',
        features: ['Professional Templates', 'A/B Testing', 'Automation']
      },
      {
        name: 'Press Release Writer',
        description: 'Newsworthy press releases',
        icon: React.createElement(ArticleIcon),
        status: 'active',
        path: '/press-releases',
        features: ['Newsworthy Content', 'Media Ready', 'Distribution Ready']
      },
      {
        name: 'Landing Page Copy',
        description: 'High-converting landing page content',
        icon: React.createElement(BusinessIcon),
        status: 'active',
        path: '/landing-page-copy',
        features: ['Conversion Focused', 'A/B Testing', 'UX Optimized']
      },
      {
        name: 'Competitive Intelligence',
        description: 'Analyze competitors and market trends',
        icon: React.createElement(PsychologyIcon),
        status: 'premium',
        path: '/competitive-intelligence',
        features: ['Market Analysis', 'Competitor Tracking', 'Strategy Insights']
      }
    ]
  },
  'Creative & Advanced': {
    icon: React.createElement(AutoAwesomeIcon),
    color: '#E91E63',
    gradient: 'linear-gradient(135deg, #E91E63 0%, #C2185B 100%)',
    tools: [
      {
        name: 'AI Agents Crew',
        description: 'Multi-agent AI content creation team',
        icon: React.createElement(AutoAwesomeIcon),
        status: 'premium',
        path: '/ai-agents-crew',
        features: ['Multi-Agent System', 'Collaborative Writing', 'Advanced AI']
      },
      {
        name: 'Content Performance Predictor',
        description: 'Predict content performance and engagement',
        icon: React.createElement(AnalyticsIcon),
        status: 'premium',
        path: '/content-predictor',
        features: ['Performance Prediction', 'Engagement Analysis', 'ROI Forecasting']
      },
      {
        name: 'Web Researcher',
        description: 'AI-powered web research and analysis',
        icon: React.createElement(SearchIcon),
        status: 'active',
        path: '/web-researcher',
        features: ['Real-time Research', 'Data Analysis', 'Insight Generation']
      },
      {
        name: 'Content Scheduler',
        description: 'Intelligent content scheduling and planning',
        icon: React.createElement(CampaignIcon),
        status: 'active',
        path: '/content-scheduler',
        features: ['Smart Scheduling', 'Calendar Integration', 'Performance Tracking']
      }
    ]
  }
}; 
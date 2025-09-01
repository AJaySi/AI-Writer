import React from 'react';
import { useCopilotAction } from '@copilotkit/react-core';
import { linkedInWriterApi, LinkedInPostRequest } from '../../services/linkedInWriterApi';
import {
  mapPostType,
  mapTone,
  mapIndustry,
  mapSearchEngine,
  readPrefs
} from './utils/linkedInWriterUtils';
import { PostHITL, ArticleHITL, CarouselHITL, VideoScriptHITL, CommentResponseHITL } from './components';

const useCopilotActionTyped = useCopilotAction as any;

const RegisterLinkedInActions: React.FC = () => {
  // LinkedIn Post Generation
  useCopilotActionTyped({
    name: 'generateLinkedInPost',
    description: 'Generate a professional LinkedIn post with industry insights and engagement optimization',
    parameters: [
      { name: 'topic', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'post_type', type: 'string', required: false },
      { name: 'tone', type: 'string', required: false },
      { name: 'refine_existing', type: 'boolean', required: false, description: 'Whether to refine existing content instead of creating new' }
    ],
    handler: async (args: any) => {
      const prefs = readPrefs();
      
      // If refining existing content, use the current draft as context
      let existingContent = '';
      if (args?.refine_existing) {
        // Get current draft from the page context
        const textarea = document.querySelector('textarea') as HTMLTextAreaElement;
        const currentDraft = textarea?.value || '';
        if (currentDraft) {
          existingContent = `\n\nREFINE THIS EXISTING CONTENT:\n${currentDraft}`;
        }
      }
      
      const res = await linkedInWriterApi.generatePost({
        topic: args?.topic || prefs.topic || 'AI transformation in business',
        industry: mapIndustry(args?.industry || prefs.industry),
        post_type: mapPostType(args?.post_type || prefs.post_type),
        tone: mapTone(args?.tone || prefs.tone),
        target_audience: args?.target_audience || prefs.target_audience || 'Business leaders and professionals',
        key_points: args?.key_points || prefs.key_points || [],
        include_hashtags: args?.include_hashtags ?? (prefs.include_hashtags ?? true),
        include_call_to_action: args?.include_call_to_action ?? (prefs.include_call_to_action ?? true),
        research_enabled: args?.research_enabled ?? (prefs.research_enabled ?? true),
        search_engine: mapSearchEngine(args?.search_engine || prefs.search_engine),
        max_length: args?.max_length || prefs.max_length || 2000
      });
      
      if (res.success && res.data) {
        const content = res.data.content;
        const hashtags = res.data.hashtags?.map(h => h.hashtag).join(' ') || '';
        const cta = res.data.call_to_action || '';
        
        let fullContent = content;
        if (hashtags) fullContent += `\n\n${hashtags}`;
        if (cta) fullContent += `\n\n${cta}`;
        
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: fullContent }));
        return { success: true, content: fullContent };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn post' };
    }
  });

  // LinkedIn Article Generation
  useCopilotActionTyped({
    name: 'generateLinkedInArticle',
    description: 'Generate a comprehensive LinkedIn article with thought leadership content',
    parameters: [
      { name: 'topic', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'tone', type: 'string', required: false },
      { name: 'word_count', type: 'number', required: false }
    ],
    handler: async (args: any) => {
      const prefs = readPrefs();
      const res = await linkedInWriterApi.generateArticle({
        topic: args?.topic || prefs.topic || 'Digital transformation strategies',
        industry: mapIndustry(args?.industry || prefs.industry),
        tone: mapTone(args?.tone || prefs.tone),
        target_audience: args?.target_audience || prefs.target_audience || 'Industry professionals and executives',
        key_sections: args?.key_sections || prefs.key_sections || [],
        include_images: args?.include_images ?? (prefs.include_images ?? true),
        seo_optimization: args?.seo_optimization ?? (prefs.seo_optimization ?? true),
        research_enabled: args?.research_enabled ?? (prefs.research_enabled ?? true),
        search_engine: mapSearchEngine(args?.search_engine || prefs.search_engine),
        word_count: args?.word_count || prefs.word_count || 1500
      });
      
      if (res.success && res.data) {
        const content = `# ${res.data.title}\n\n${res.data.content}`;
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn article' };
    }
  });

  // LinkedIn Carousel Generation
  useCopilotActionTyped({
    name: 'generateLinkedInCarousel',
    description: 'Generate a LinkedIn carousel with multiple slides for visual content',
    parameters: [
      { name: 'topic', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'slide_count', type: 'number', required: false }
    ],
    handler: async (args: any) => {
      const prefs = readPrefs();
      const res = await linkedInWriterApi.generateCarousel({
        topic: args?.topic || prefs.topic || 'Professional development tips',
        industry: mapIndustry(args?.industry || prefs.industry),
        slide_count: args?.slide_count || prefs.slide_count || 8,
        tone: mapTone(args?.tone || prefs.tone),
        target_audience: args?.target_audience || prefs.target_audience || 'Professionals seeking growth',
        key_takeaways: args?.key_takeaways || prefs.key_takeaways || [],
        include_cover_slide: args?.include_cover_slide ?? (prefs.include_cover_slide ?? true),
        include_cta_slide: args?.include_cta_slide ?? (prefs.include_cta_slide ?? true),
        visual_style: args?.visual_style || prefs.visual_style || 'modern'
      });
      
      if (res.success && res.data) {
        let content = `# ${res.data.title}\n\n`;
        res.data.slides.forEach((slide, index) => {
          content += `## Slide ${index + 1}: ${slide.title}\n\n${slide.content}\n\n`;
        });
        
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn carousel' };
    }
  });

  // LinkedIn Video Script Generation
  useCopilotActionTyped({
    name: 'generateLinkedInVideoScript',
    description: 'Generate a LinkedIn video script with hook, content, and captions',
    parameters: [
      { name: 'topic', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'video_length', type: 'number', required: false }
    ],
    handler: async (args: any) => {
      const prefs = readPrefs();
      const res = await linkedInWriterApi.generateVideoScript({
        topic: args?.topic || prefs.topic || 'Professional networking tips',
        industry: mapIndustry(args?.industry || prefs.industry),
        video_length: args?.video_length || prefs.video_length || 60,
        tone: mapTone(args?.tone || prefs.tone),
        target_audience: args?.target_audience || prefs.target_audience || 'Professional networkers',
        key_messages: args?.key_messages || prefs.key_messages || [],
        include_hook: args?.include_hook ?? (prefs.include_hook ?? true),
        include_captions: args?.include_captions ?? (prefs.include_captions ?? true)
      });
      
      if (res.success && res.data) {
        let content = `# Video Script: ${args?.topic || 'Professional Content'}\n\n`;
        content += `## Hook\n${res.data.hook}\n\n`;
        content += `## Main Content\n`;
        res.data.main_content.forEach((scene, index) => {
          content += `### Scene ${index + 1} (${scene.duration || '30s'})\n${scene.content}\n\n`;
        });
        content += `## Conclusion\n${res.data.conclusion}\n\n`;
        content += `## Video Description\n${res.data.video_description}\n\n`;
        
        if (res.data.captions) {
          content += `## Captions\n${res.data.captions.join('\n')}\n\n`;
        }
        
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn video script' };
    }
  });

  // LinkedIn Comment Response Generation
  useCopilotActionTyped({
    name: 'generateLinkedInCommentResponse',
    description: 'Generate a professional response to a LinkedIn comment',
    parameters: [
      { name: 'original_post', type: 'string', required: false },
      { name: 'comment', type: 'string', required: false },
      { name: 'response_type', type: 'string', required: false }
    ],
    handler: async (args: any) => {
      const prefs = readPrefs();
      const res = await linkedInWriterApi.generateCommentResponse({
        original_post: args?.original_post || prefs.original_post || 'Sample LinkedIn post content',
        comment: args?.comment || prefs.comment || 'Sample comment to respond to',
        response_type: args?.response_type || prefs.response_type || 'professional',
        tone: mapTone(args?.tone || prefs.tone),
        include_question: args?.include_question ?? (prefs.include_question ?? false),
        brand_voice: args?.brand_voice || prefs.brand_voice
      });
      
      if (res.success && res.response) {
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: res.response }));
        return { success: true, content: res.response };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn comment response' };
    }
  });

  // LinkedIn Profile Optimization
  useCopilotActionTyped({
    name: 'optimizeLinkedInProfile',
    description: 'Optimize LinkedIn profile sections for better professional visibility',
    parameters: [
      { name: 'current_headline', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'experience_level', type: 'string', required: false }
    ],
    handler: async (args: any) => {
      const res = await linkedInWriterApi.optimizeProfile({
        current_headline: args?.current_headline || 'Professional',
        industry: mapIndustry(args?.industry),
        experience_level: args?.experience_level || 'mid-level',
        target_role: args?.target_role,
        key_skills: args?.key_skills || []
      });
      
      if (res.success && res.data) {
        let content = `# LinkedIn Profile Optimization\n\n`;
        content += `## Optimized Headline\n${res.data.headline}\n\n`;
        content += `## About Section\n${res.data.about}\n\n`;
        content += `## Key Skills\n${res.data.skills?.join(', ')}\n\n`;
        
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to optimize LinkedIn profile' };
    }
  });

  // LinkedIn Poll Generation
  useCopilotActionTyped({
    name: 'generateLinkedInPoll',
    description: 'Generate an engaging LinkedIn poll with professional questions',
    parameters: [
      { name: 'topic', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false },
      { name: 'poll_type', type: 'string', required: false }
    ],
    handler: async (args: any) => {
      const res = await linkedInWriterApi.generatePoll({
        topic: args?.topic || 'Professional development',
        industry: mapIndustry(args?.industry),
        poll_type: args?.poll_type || 'professional',
        target_audience: args?.target_audience || 'Industry professionals',
        question_count: args?.question_count || 1
      });
      
      if (res.success && res.data) {
        let content = `# LinkedIn Poll: ${res.data.question}\n\n`;
        content += `## Options\n`;
        res.data.options?.forEach((option: string, index: number) => {
          content += `${index + 1}. ${option}\n`;
        });
        content += `\n## Context\n${res.data.context || ''}\n\n`;
        
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn poll' };
    }
  });

  // LinkedIn Company Update Generation
  useCopilotActionTyped({
    name: 'generateLinkedInCompanyUpdate',
    description: 'Generate a professional company update for LinkedIn',
    parameters: [
      { name: 'company_name', type: 'string', required: false },
      { name: 'update_type', type: 'string', required: false },
      { name: 'industry', type: 'string', required: false }
    ],
    handler: async (args: any) => {
      const res = await linkedInWriterApi.generateCompanyUpdate({
        company_name: args?.company_name || 'Your Company',
        update_type: args?.update_type || 'achievement',
        industry: mapIndustry(args?.industry),
        announcement: args?.announcement,
        target_audience: args?.target_audience || 'Industry professionals and clients',
        include_metrics: args?.include_metrics ?? true
      });
      
      if (res.success && res.data) {
        const content = res.data.content;
        window.dispatchEvent(new CustomEvent('linkedinwriter:updateDraft', { detail: content }));
        return { success: true, content };
      }
      return { success: false, message: res.error || 'Failed to generate LinkedIn company update' };
    }
  });

  return null;
};

export default RegisterLinkedInActions;

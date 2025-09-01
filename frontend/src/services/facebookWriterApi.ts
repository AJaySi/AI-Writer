import { apiClient } from '../api/client';

export interface PostGenerateRequest {
  business_type: string;
  target_audience: string;
  post_goal: string; // enum string value as defined by backend
  post_tone: string; // enum string value as defined by backend
  include?: string;
  avoid?: string;
  media_type?: string; // default "None"
  advanced_options?: {
    use_hook?: boolean;
    use_story?: boolean;
    use_cta?: boolean;
    use_question?: boolean;
    use_emoji?: boolean;
    use_hashtags?: boolean;
  };
}

export const facebookWriterApi = {
  async health(): Promise<any> {
    const { data } = await apiClient.get('/api/facebook-writer/health');
    return data;
  },
  async tools(): Promise<any> {
    const { data } = await apiClient.get('/api/facebook-writer/tools');
    return data;
  },
  async postGenerate(payload: PostGenerateRequest): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/post/generate', payload);
    return data;
  },
  async hashtagsGenerate(payload: { content_topic?: string; draft?: string }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/hashtags/generate', payload);
    return data;
  },
  async storyGenerate(payload: {
    business_type: string;
    target_audience: string;
    story_type: string;
    story_tone: string;
    include?: string;
    avoid?: string;
    // Advanced options parity with backend
    use_hook?: boolean;
    use_story?: boolean;
    use_cta?: boolean;
    use_question?: boolean;
    use_emoji?: boolean;
    use_hashtags?: boolean;
    visual_options?: {
      background_type?: string;
      background_image_prompt?: string;
      gradient_style?: string;
      text_overlay?: boolean;
      text_style?: string;
      text_color?: string;
      text_position?: string;
      stickers?: boolean;
      interactive_elements?: boolean;
      interactive_types?: string[];
      call_to_action?: string;
    };
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/story/generate', payload);
    return data;
  },
  async adCopyGenerate(payload: {
    business_type: string;
    product_service: string;
    ad_objective: string;
    ad_format: string;
    target_audience: string;
    targeting_options: {
      age_group: string;
      custom_age?: string;
      gender?: string;
      location?: string;
      interests?: string;
      behaviors?: string;
      lookalike_audience?: string;
    };
    unique_selling_proposition: string;
    offer_details?: string;
    budget_range: string;
    custom_budget?: string;
    campaign_duration?: string;
    competitor_analysis?: string;
    brand_voice?: string;
    compliance_requirements?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/ad-copy/generate', payload);
    return data;
  }
  ,
  async reelGenerate(payload: {
    business_type: string;
    target_audience: string;
    reel_type: string;
    reel_length: string;
    reel_style: string;
    topic: string;
    include?: string;
    avoid?: string;
    music_preference?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/reel/generate', payload);
    return data;
  }
  ,
  async carouselGenerate(payload: {
    business_type: string;
    target_audience: string;
    carousel_type: string;
    topic: string;
    num_slides?: number;
    include_cta?: boolean;
    cta_text?: string;
    brand_colors?: string;
    include?: string;
    avoid?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/carousel/generate', payload);
    return data;
  }
  ,
  async eventGenerate(payload: {
    event_name: string;
    event_type: string;
    event_format: string;
    business_type: string;
    target_audience: string;
    event_date?: string;
    event_time?: string;
    location?: string;
    duration?: string;
    key_benefits?: string;
    speakers?: string;
    agenda?: string;
    ticket_info?: string;
    special_offers?: string;
    include?: string;
    avoid?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/event/generate', payload);
    return data;
  }
  ,
  async groupPostGenerate(payload: {
    group_name: string;
    group_type: string;
    post_purpose: string;
    business_type: string;
    topic: string;
    target_audience: string;
    value_proposition: string;
    group_rules?: { no_promotion?: boolean; value_first?: boolean; no_links?: boolean; community_focused?: boolean; relevant_only?: boolean };
    include?: string;
    avoid?: string;
    call_to_action?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/group-post/generate', payload);
    return data;
  },
  async pageAboutGenerate(payload: {
    business_name: string;
    business_category: string;
    custom_category?: string;
    business_description: string;
    target_audience: string;
    unique_value_proposition: string;
    services_products: string;
    company_history?: string;
    mission_vision?: string;
    achievements?: string;
    page_tone: string;
    custom_tone?: string;
    contact_info?: {
      website?: string;
      phone?: string;
      email?: string;
      address?: string;
      hours?: string;
    };
    keywords?: string;
    call_to_action?: string;
  }): Promise<any> {
    const { data } = await apiClient.post('/api/facebook-writer/page-about/generate', payload);
    return data;
  }
};



// Facebook Writer Utilities
export const PREFS_KEY = 'fbwriter:preferences';

// Validation constants
export const VALID_GOALS = [
  'Promote a product/service',
  'Share valuable content',
  'Increase engagement',
  'Build brand awareness',
  'Drive website traffic',
  'Generate leads',
  'Announce news/updates',
  'Custom'
];

export const VALID_TONES = [
  'Informative',
  'Humorous',
  'Inspirational',
  'Upbeat',
  'Casual',
  'Professional',
  'Conversational',
  'Custom'
];

export const VALID_STORY_TYPES = [
  'Product showcase',
  'Behind the scenes',
  'User testimonial',
  'Event promotion',
  'Tutorial/How-to',
  'Question/Poll',
  'Announcement',
  'Custom'
];

export const VALID_STORY_TONES = [
  'Casual',
  'Fun',
  'Professional',
  'Inspirational',
  'Educational',
  'Entertaining',
  'Custom'
];

export const VALID_BUSINESS_CATEGORIES = [
  'Retail', 'Restaurant/Food', 'Health & Fitness', 'Education', 'Technology', 
  'Consulting', 'Creative Services', 'Non-profit', 'Entertainment', 'Real Estate', 
  'Automotive', 'Beauty & Personal Care', 'Finance', 'Travel & Tourism', 'Custom'
];

export const VALID_PAGE_TONES = [
  'Professional', 'Friendly', 'Innovative', 'Trustworthy', 'Creative', 
  'Approachable', 'Authoritative', 'Custom'
];

// Utility functions
export function readPrefs(): Record<string, any> {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY) || '{}') || {};
  } catch {
    return {};
  }
}

export function writePrefs(p: Record<string, any>) {
  try {
    localStorage.setItem(PREFS_KEY, JSON.stringify(p));
  } catch {}
}

export function logAssistant(content: string) {
  try {
    window.dispatchEvent(new CustomEvent('fbwriter:assistantMessage', { detail: { content } }));
  } catch {}
}

export function normalizeEnum(input: string | undefined | null): string {
  return (input || '').trim().toLowerCase();
}

export function mapGoal(goal: string | undefined): string {
  const g = normalizeEnum(goal);
  if (!g) return 'Build brand awareness';
  const exact = VALID_GOALS.find(v => v.toLowerCase() === g);
  if (exact) return exact;
  if (g.includes('announce')) return 'Announce news/updates';
  if (g.includes('awareness') || g.includes('brand')) return 'Build brand awareness';
  if (g.includes('engagement') || g.includes('engage')) return 'Increase engagement';
  if (g.includes('traffic')) return 'Drive website traffic';
  if (g.includes('lead')) return 'Generate leads';
  if (g.includes('share') || g.includes('content')) return 'Share valuable content';
  if (g.includes('promote') || g.includes('product') || g.includes('service')) return 'Promote a product/service';
  return 'Build brand awareness';
}

export function mapTone(tone: string | undefined): string {
  const t = normalizeEnum(tone);
  if (!t) return 'Professional';
  const exact = VALID_TONES.find(v => v.toLowerCase() === t);
  if (exact) return exact;
  if (t.includes('friendly') || t.includes('casual')) return 'Casual';
  if (t.includes('professional') || t.includes('pro')) return 'Professional';
  if (t.includes('exciting') || t.includes('energetic') || t.includes('upbeat')) return 'Upbeat';
  if (t.includes('inspir')) return 'Inspirational';
  if (t.includes('humor') || t.includes('funny')) return 'Humorous';
  if (t.includes('convers')) return 'Conversational';
  if (t.includes('info')) return 'Informative';
  return 'Professional';
}

export function mapStoryType(t?: string) {
  const s = (t || '').trim().toLowerCase();
  const exact = VALID_STORY_TYPES.find(v => v.toLowerCase() === s);
  if (exact) return exact;
  if (s.includes('behind')) return 'Behind the scenes';
  if (s.includes('testi')) return 'User testimonial';
  if (s.includes('event')) return 'Event promotion';
  if (s.includes('tutorial') || s.includes('how')) return 'Tutorial/How-to';
  if (s.includes('poll') || s.includes('question')) return 'Question/Poll';
  if (s.includes('announce')) return 'Announcement';
  return 'Product showcase';
}

export function mapStoryTone(t?: string) {
  const s = (t || '').trim().toLowerCase();
  const exact = VALID_STORY_TONES.find(v => v.toLowerCase() === s);
  if (exact) return exact;
  if (s.includes('fun')) return 'Fun';
  if (s.includes('inspir')) return 'Inspirational';
  if (s.includes('educat')) return 'Educational';
  if (s.includes('entertain')) return 'Entertaining';
  if (s.includes('pro')) return 'Professional';
  return 'Casual';
}

export function mapBusinessCategory(cat?: string) {
  const s = (cat || '').trim().toLowerCase();
  const exact = VALID_BUSINESS_CATEGORIES.find(v => v.toLowerCase() === s);
  if (exact) return exact;
  if (s.includes('tech') || s.includes('software')) return 'Technology';
  if (s.includes('health') || s.includes('fitness')) return 'Health & Fitness';
  if (s.includes('food') || s.includes('restaurant')) return 'Restaurant/Food';
  if (s.includes('retail') || s.includes('shop')) return 'Retail';
  if (s.includes('educat')) return 'Education';
  if (s.includes('consult')) return 'Consulting';
  if (s.includes('creative') || s.includes('design')) return 'Creative Services';
  if (s.includes('non') || s.includes('charity')) return 'Non-profit';
  if (s.includes('entertain')) return 'Entertainment';
  if (s.includes('real') || s.includes('property')) return 'Real Estate';
  if (s.includes('auto') || s.includes('car')) return 'Automotive';
  if (s.includes('beauty') || s.includes('personal')) return 'Beauty & Personal Care';
  if (s.includes('finance') || s.includes('bank')) return 'Finance';
  if (s.includes('travel') || s.includes('tourism')) return 'Travel & Tourism';
  return 'Technology';
}

export function mapPageTone(tone?: string) {
  const s = (tone || '').trim().toLowerCase();
  const exact = VALID_PAGE_TONES.find(v => v.toLowerCase() === s);
  if (exact) return exact;
  if (s.includes('profession')) return 'Professional';
  if (s.includes('friend')) return 'Friendly';
  if (s.includes('innov')) return 'Innovative';
  if (s.includes('trust')) return 'Trustworthy';
  if (s.includes('creativ')) return 'Creative';
  if (s.includes('approach')) return 'Approachable';
  if (s.includes('authorit')) return 'Authoritative';
  return 'Professional';
}

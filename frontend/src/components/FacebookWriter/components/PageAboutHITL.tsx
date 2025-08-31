import React from 'react';
import { facebookWriterApi } from '../../../services/facebookWriterApi';
import { mapBusinessCategory, mapPageTone, VALID_BUSINESS_CATEGORIES, VALID_PAGE_TONES } from '../utils/facebookWriterUtils';

interface PageAboutHITLProps {
  args: any;
  respond: (data: any) => void;
}

const PageAboutHITL: React.FC<PageAboutHITLProps> = ({ args, respond }) => {
  const [form, setForm] = React.useState({
    business_name: args?.business_name || 'TechStart Solutions',
    business_category: mapBusinessCategory(args?.business_category) || 'Technology',
    custom_category: args?.custom_category || '',
    business_description: args?.business_description || 'We provide innovative software solutions for modern businesses',
    target_audience: args?.target_audience || 'Small to medium-sized businesses looking to digitize their operations',
    unique_value_proposition: args?.unique_value_proposition || 'Affordable, scalable solutions with 24/7 support',
    services_products: args?.services_products || 'Cloud-based CRM, project management tools, and custom software development',
    company_history: args?.company_history || '',
    mission_vision: args?.mission_vision || '',
    achievements: args?.achievements || '',
    page_tone: mapPageTone(args?.page_tone) || 'Professional',
    custom_tone: args?.custom_tone || '',
    contact_info: {
      website: args?.contact_info?.website || '',
      phone: args?.contact_info?.phone || '',
      email: args?.contact_info?.email || '',
      address: args?.contact_info?.address || '',
      hours: args?.contact_info?.hours || ''
    },
    keywords: args?.keywords || '',
    call_to_action: args?.call_to_action || ''
  });
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const set = (key: string, value: any) => setForm(prev => ({ ...prev, [key]: value }));
  const setContact = (key: string, value: any) => setForm(prev => ({ 
    ...prev, 
    contact_info: { ...prev.contact_info, [key]: value } 
  }));

  const run = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const payload = {
        ...form,
        business_category: mapBusinessCategory(form.business_category),
        page_tone: mapPageTone(form.page_tone)
      };

      const res = await facebookWriterApi.pageAboutGenerate(payload);
      const shortDesc = res?.short_description || res?.data?.short_description;
      const longDesc = res?.long_description || res?.data?.long_description;
      const companyOverview = res?.company_overview || res?.data?.company_overview;
      const missionStatement = res?.mission_statement || res?.data?.mission_statement;
      const storySection = res?.story_section || res?.data?.story_section;
      const servicesSection = res?.services_section || res?.data?.services_section;
      const ctaSuggestions = res?.cta_suggestions || res?.data?.cta_suggestions;
      const keywordOptimization = res?.keyword_optimization || res?.data?.keyword_optimization;
      const completionTips = res?.completion_tips || res?.data?.completion_tips;

      let output = '';
      if (shortDesc) output += `\n\n**Short Description:**\n${shortDesc}`;
      if (longDesc) output += `\n\n**Long Description:**\n${longDesc}`;
      if (companyOverview) output += `\n\n**Company Overview:**\n${companyOverview}`;
      if (missionStatement) output += `\n\n**Mission Statement:**\n${missionStatement}`;
      if (storySection) output += `\n\n**Company Story:**\n${storySection}`;
      if (servicesSection) output += `\n\n**Services/Products:**\n${servicesSection}`;
      
      if (Array.isArray(ctaSuggestions) && ctaSuggestions.length) {
        output += '\n\n**CTA Suggestions:**';
        ctaSuggestions.forEach((cta: string) => output += `\n- ${cta}`);
      }
      
      if (Array.isArray(keywordOptimization) && keywordOptimization.length) {
        output += '\n\n**Keyword Optimization:**';
        keywordOptimization.forEach((keyword: string) => output += `\n- ${keyword}`);
      }
      
      if (Array.isArray(completionTips) && completionTips.length) {
        output += '\n\n**Completion Tips:**';
        completionTips.forEach((tip: string) => output += `\n- ${tip}`);
      }

      if (output) {
        window.dispatchEvent(new CustomEvent('fbwriter:appendDraft', { detail: output }));
        respond({ success: true, content: output });
      } else {
        respond({ success: true, message: 'Page About content generated.' });
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to generate page about content');
      respond({ success: false, error: err?.message || 'Generation failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16, background: '#f5f5f5', borderRadius: 8, marginBottom: 16 }}>
      <h4 style={{ margin: '0 0 12px 0', color: '#333' }}>Generate Facebook Page About</h4>
      
      <div style={{ display: 'grid', gap: 8, fontSize: 14 }}>
        <input 
          placeholder="Business name" 
          value={form.business_name} 
          onChange={e => set('business_name', e.target.value)} 
        />
        
        <select 
          value={form.business_category} 
          onChange={e => set('business_category', e.target.value)}
        >
          {VALID_BUSINESS_CATEGORIES.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        
        {form.business_category === 'Custom' && (
          <input 
            placeholder="Custom business category" 
            value={form.custom_category} 
            onChange={e => set('custom_category', e.target.value)} 
          />
        )}
        
        <textarea 
          placeholder="Business description" 
          value={form.business_description} 
          onChange={e => set('business_description', e.target.value)}
          rows={3}
        />
        
        <textarea 
          placeholder="Target audience" 
          value={form.target_audience} 
          onChange={e => set('target_audience', e.target.value)}
          rows={2}
        />
        
        <textarea 
          placeholder="Unique value proposition" 
          value={form.unique_value_proposition} 
          onChange={e => set('unique_value_proposition', e.target.value)}
          rows={2}
        />
        
        <textarea 
          placeholder="Services/products offered" 
          value={form.services_products} 
          onChange={e => set('services_products', e.target.value)}
          rows={2}
        />
        
        <textarea 
          placeholder="Company history (optional)" 
          value={form.company_history} 
          onChange={e => set('company_history', e.target.value)}
          rows={2}
        />
        
        <textarea 
          placeholder="Mission/vision (optional)" 
          value={form.mission_vision} 
          onChange={e => set('mission_vision', e.target.value)}
          rows={2}
        />
        
        <textarea 
          placeholder="Achievements/awards (optional)" 
          value={form.achievements} 
          onChange={e => set('achievements', e.target.value)}
          rows={2}
        />
        
        <select 
          value={form.page_tone} 
          onChange={e => set('page_tone', e.target.value)}
        >
          {VALID_PAGE_TONES.map(tone => (
            <option key={tone} value={tone}>{tone}</option>
          ))}
        </select>
        
        {form.page_tone === 'Custom' && (
          <input 
            placeholder="Custom page tone" 
            value={form.custom_tone} 
            onChange={e => set('custom_tone', e.target.value)} 
          />
        )}
        
        <div style={{ fontWeight: 600, marginTop: 8 }}>Contact Information (Optional)</div>
        <input 
          placeholder="Website URL" 
          value={form.contact_info.website} 
          onChange={e => setContact('website', e.target.value)} 
        />
        <input 
          placeholder="Phone number" 
          value={form.contact_info.phone} 
          onChange={e => setContact('phone', e.target.value)} 
        />
        <input 
          placeholder="Email address" 
          value={form.contact_info.email} 
          onChange={e => setContact('email', e.target.value)} 
        />
        <input 
          placeholder="Physical address" 
          value={form.contact_info.address} 
          onChange={e => setContact('address', e.target.value)} 
        />
        <input 
          placeholder="Business hours" 
          value={form.contact_info.hours} 
          onChange={e => setContact('hours', e.target.value)} 
        />
        
        <input 
          placeholder="Important keywords to include" 
          value={form.keywords} 
          onChange={e => set('keywords', e.target.value)} 
        />
        
        <input 
          placeholder="Primary call-to-action" 
          value={form.call_to_action} 
          onChange={e => set('call_to_action', e.target.value)} 
        />
      </div>
      
      <button onClick={run} disabled={loading} style={{ marginTop: 12, width: '100%' }}>
        {loading ? 'Generating...' : 'Generate Page About'}
      </button>
      
      {error && <div style={{ marginTop: 8, color: '#c33', fontSize: 12 }}>{error}</div>}
    </div>
  );
};

export default PageAboutHITL;

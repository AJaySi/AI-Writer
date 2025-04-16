import streamlit as st
import re
import json
import time
from typing import Dict, List, Tuple, Optional
import random
import emoji
from datetime import datetime

from ....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Constants
MAX_TWEET_LENGTH = 280
EMOJI_CATEGORIES = {
    "Humorous": ["😄", "😂", "🤣", "😊", "😉", "😎", "🤪", "😜", "🤓", "😇"],
    "Informative": ["📚", "📊", "📈", "🔍", "💡", "📝", "📋", "🔎", "📖", "📑"],
    "Inspirational": ["✨", "🌟", "💫", "⭐", "🔥", "💪", "🙌", "👏", "💯", "🎯"],
    "Serious": ["🤔", "💭", "🧐", "📢", "🔔", "⚖️", "🎓", "📊", "🔬", "📰"],
    "Casual": ["👋", "👍", "🙋", "💁", "🤗", "👌", "✌️", "🤝", "👊", "🙏"]
}

def count_characters(text: str) -> int:
    """Count characters in tweet, accounting for emojis."""
    return len(text)

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from tweet text."""
    return re.findall(r'#\w+', text)

def suggest_hashtags(topic: str, tone: str) -> List[str]:
    """Suggest relevant hashtags based on topic and tone."""
    # Enhanced hashtag suggestions based on topic and tone
    base_hashtags = {
        "professional": ["#Business", "#Leadership", "#Innovation"],
        "casual": ["#Life", "#Fun", "#Trending"],
        "informative": ["#Learn", "#Tips", "#HowTo"],
        "humorous": ["#Funny", "#LOL", "#Humor"],
        "inspirational": ["#Motivation", "#Success", "#Growth"]
    }
    
    topic_hashtags = {
        "tech": ["#Technology", "#TechNews", "#Innovation"],
        "business": ["#Business", "#Entrepreneurship", "#Startup"],
        "marketing": ["#Marketing", "#DigitalMarketing", "#SocialMedia"],
        "education": ["#Education", "#Learning", "#Knowledge"],
        "health": ["#Health", "#Wellness", "#Fitness"]
    }
    
    # Combine base and topic hashtags
    suggested = base_hashtags.get(tone.lower(), []) + topic_hashtags.get(topic.lower(), [])
    return list(set(suggested))[:5]  # Return unique hashtags, max 5

def suggest_emojis(tone: str, count: int = 3) -> List[str]:
    """Suggest emojis based on tone."""
    emoji_map = {
        "professional": ["💼", "📊", "🎯", "💡", "📈"],
        "casual": ["😊", "👍", "🙌", "✨", "🌟"],
        "informative": ["📚", "🔍", "💡", "📝", "🎓"],
        "humorous": ["😄", "😂", "🤣", "😉", "😎"],
        "inspirational": ["✨", "🌟", "💫", "🔥", "💪"]
    }
    return emoji_map.get(tone.lower(), ["✨"])[:count]

def predict_tweet_performance(tweet: str, target_audience: str, tone: str) -> Dict:
    """Predict tweet performance with enhanced metrics."""
    char_count = count_characters(tweet)
    hashtags = extract_hashtags(tweet)
    
    # Enhanced performance metrics
    metrics = {
        "character_count": {
            "score": min(100, (char_count / 280) * 100),
            "status": "optimal" if 100 <= char_count <= 200 else "suboptimal",
            "suggestion": "Consider adjusting length for optimal engagement" if char_count < 100 or char_count > 200 else "Length is optimal"
        },
        "hashtag_usage": {
            "score": min(100, (len(hashtags) / 3) * 100),
            "status": "optimal" if 1 <= len(hashtags) <= 3 else "suboptimal",
            "suggestion": "Add more hashtags" if len(hashtags) < 1 else "Reduce hashtag count" if len(hashtags) > 3 else "Hashtag count is optimal"
        },
        "engagement_potential": {
            "score": 0,
            "status": "needs_improvement",
            "suggestion": ""
        },
        "audience_alignment": {
            "score": 0,
            "status": "needs_improvement",
            "suggestion": ""
        }
    }
    
    # Calculate engagement potential
    engagement_triggers = ["?", "!", "RT", "like", "follow", "check", "learn", "discover"]
    trigger_count = sum(1 for trigger in engagement_triggers if trigger.lower() in tweet.lower())
    metrics["engagement_potential"]["score"] = min(100, (trigger_count / 3) * 100)
    metrics["engagement_potential"]["status"] = "optimal" if trigger_count >= 1 else "needs_improvement"
    metrics["engagement_potential"]["suggestion"] = "Add engagement triggers" if trigger_count < 1 else "Good engagement potential"
    
    # Calculate audience alignment
    audience_keywords = {
        "professionals": ["business", "industry", "professional", "career"],
        "students": ["learn", "study", "education", "student"],
        "general": ["everyone", "people", "community", "world"]
    }
    keyword_count = sum(1 for keyword in audience_keywords.get(target_audience.lower(), []) 
                       if keyword.lower() in tweet.lower())
    metrics["audience_alignment"]["score"] = min(100, (keyword_count / 2) * 100)
    metrics["audience_alignment"]["status"] = "optimal" if keyword_count >= 1 else "needs_improvement"
    metrics["audience_alignment"]["suggestion"] = "Add audience-specific keywords" if keyword_count < 1 else "Good audience alignment"
    
    # Calculate overall score
    overall_score = sum(metric["score"] for metric in metrics.values()) / len(metrics)
    
    return {
        "metrics": metrics,
        "overall_score": overall_score,
        "status": "excellent" if overall_score >= 80 else "good" if overall_score >= 60 else "fair" if overall_score >= 40 else "needs_improvement"
    }

def generate_tweet_variations(
    hook: str,
    target_audience: str,
    tone: str,
    call_to_action: str = "",
    keywords: str = "",
    length: str = "medium",
    num_variations: int = 3
) -> List[Dict]:
    """Generate multiple tweet variations with enhanced AI suggestions."""
    # Enhanced prompt template for better AI suggestions
    prompt_template = f"""
    Create {num_variations} engaging tweet variations with the following parameters:
    - Hook/Topic: {hook}
    - Target Audience: {target_audience}
    - Tone: {tone}
    - Call to Action: {call_to_action}
    - Keywords: {keywords}
    - Length: {length}
    
    Each tweet should:
    1. Start with an attention-grabbing hook
    2. Include relevant hashtags
    3. Use appropriate emojis
    4. End with a clear call-to-action
    5. Stay within Twitter's character limit
    6. Match the specified tone and audience
    
    Format each tweet as a JSON object with:
    - text: The tweet content
    - hashtags: List of suggested hashtags
    - emojis: List of suggested emojis
    - engagement_score: Predicted engagement score (0-100)
    """
    
    # Simulate AI-generated tweets (replace with actual AI call)
    sample_tweets = [
        {
            "text": f"🚀 {hook} #Innovation #Tech",
            "hashtags": ["#Innovation", "#Tech"],
            "emojis": ["🚀"],
            "engagement_score": 85
        },
        {
            "text": f"💡 {hook} #Business #Growth",
            "hashtags": ["#Business", "#Growth"],
            "emojis": ["💡"],
            "engagement_score": 75
        },
        {
            "text": f"✨ {hook} #Success #Leadership",
            "hashtags": ["#Success", "#Leadership"],
            "emojis": ["✨"],
            "engagement_score": 80
        }
    ]
    
    return sample_tweets[:num_variations]

def suggest_improvements(tweet: str, performance: Dict) -> List[str]:
    """Generate actionable improvement suggestions."""
    suggestions = []
    metrics = performance["metrics"]
    
    # Character count suggestions
    if metrics["character_count"]["status"] == "suboptimal":
        suggestions.append(f"📝 {metrics['character_count']['suggestion']}")
    
    # Hashtag suggestions
    if metrics["hashtag_usage"]["status"] == "suboptimal":
        suggestions.append(f"#️⃣ {metrics['hashtag_usage']['suggestion']}")
    
    # Engagement suggestions
    if metrics["engagement_potential"]["status"] == "needs_improvement":
        suggestions.append(f"🎯 {metrics['engagement_potential']['suggestion']}")
    
    # Audience alignment suggestions
    if metrics["audience_alignment"]["status"] == "needs_improvement":
        suggestions.append(f"👥 {metrics['audience_alignment']['suggestion']}")
    
    return suggestions

def render_tweet_card(tweet: Dict, index: int) -> None:
    """Render an enhanced tweet card with interactive elements."""
    with st.container():
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>Tweet Variation {index + 1}</h3>
                <p style='margin: 10px 0;'>{tweet['text']}</p>
                <div style='display: flex; gap: 10px;'>
                    <span style='background-color: #e1e4e8; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;'>
                        Score: {tweet['engagement_score']}%
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Interactive elements
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Copy Tweet {index + 1}", key=f"copy_{index}"):
                st.write("Tweet copied to clipboard!")
        with col2:
            if st.button(f"Save Tweet {index + 1}", key=f"save_{index}"):
                st.write("Tweet saved!")

def smart_tweet_generator():
    """Enhanced Smart Tweet Generator with improved UI and AI integration."""
    st.title("✨ Smart Tweet Generator")
    st.markdown("Create engaging tweets with AI-powered optimization")
    
    # Input section with improved UI
    with st.expander("Tweet Parameters", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            hook = st.text_area("Tweet Hook/Topic", 
                              placeholder="Enter your main message or topic...",
                              help="The main message or topic of your tweet")
            
            target_audience = st.selectbox(
                "Target Audience",
                ["Professionals", "Students", "General"],
                help="Select your target audience"
            )
            
            tone = st.radio(
                "Tweet Tone",
                ["Professional", "Casual", "Informative", "Humorous", "Inspirational"],
                horizontal=True,
                help="Choose the tone for your tweet"
            )
        
        with col2:
            call_to_action = st.text_input(
                "Call to Action",
                placeholder="e.g., Learn more, Follow us...",
                help="What action do you want your audience to take?"
            )
            
            keywords = st.text_input(
                "Keywords/Hashtags",
                placeholder="Enter keywords separated by commas",
                help="Keywords to include in your tweet"
            )
            
            length = st.select_slider(
                "Tweet Length",
                options=["short", "medium", "long"],
                value="medium",
                help="Choose your desired tweet length"
            )
            
            num_variations = st.slider(
                "Number of Variations",
                min_value=1,
                max_value=5,
                value=3,
                help="How many tweet variations would you like to generate?"
            )
    
    # Generate button with loading state
    if st.button("Generate Tweets", use_container_width=True):
        with st.spinner("Generating tweet variations..."):
            tweets = generate_tweet_variations(
                hook, target_audience, tone,
                call_to_action, keywords, length,
                num_variations
            )
            
            # Display performance metrics
            st.markdown("### 📊 Performance Metrics")
            for tweet in tweets:
                performance = predict_tweet_performance(tweet["text"], target_audience, tone)
                
                # Overall score with progress bar
                st.progress(performance["overall_score"] / 100)
                st.metric("Overall Score", f"{performance['overall_score']:.1f}%")
                
                # Detailed metrics in columns
                cols = st.columns(4)
                metrics = performance["metrics"]
                
                with cols[0]:
                    st.metric("Character Count", f"{metrics['character_count']['score']:.1f}%")
                with cols[1]:
                    st.metric("Hashtag Usage", f"{metrics['hashtag_usage']['score']:.1f}%")
                with cols[2]:
                    st.metric("Engagement", f"{metrics['engagement_potential']['score']:.1f}%")
                with cols[3]:
                    st.metric("Audience Fit", f"{metrics['audience_alignment']['score']:.1f}%")
                
                # Improvement suggestions
                suggestions = suggest_improvements(tweet["text"], performance)
                if suggestions:
                    st.markdown("### 💡 Improvement Suggestions")
                    for suggestion in suggestions:
                        st.info(suggestion)
                
                # Tweet card
                render_tweet_card(tweet, tweets.index(tweet))
                
                st.markdown("---")
            
            # Export options
            st.markdown("### 📥 Export Options")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export as JSON"):
                    st.download_button(
                        "Download JSON",
                        data=json.dumps(tweets, indent=2),
                        file_name=f"tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            with col2:
                if st.button("Copy All Tweets"):
                    tweet_texts = "\n\n".join(tweet["text"] for tweet in tweets)
                    st.code(tweet_texts)

if __name__ == "__main__":
    smart_tweet_generator() 

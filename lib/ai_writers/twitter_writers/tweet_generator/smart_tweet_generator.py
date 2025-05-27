"""
Smart Tweet Generator with modern UI components.
"""

import streamlit as st
import re
import json
from typing import Dict, List, Tuple, Optional
import random
import emoji
from datetime import datetime

from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..twitter_streamlit_ui import (
    TweetForm,
    TweetCard,
    Theme,
    save_to_session,
    get_from_session,
    show_success_message,
    show_error_message,
    show_info_message,
    validate_tweet_content,
    validate_hashtags,
    validate_emojis,
    calculate_engagement_score,
    generate_tweet_metrics,
    copy_to_clipboard,
    create_download_button
)

# Constants
MAX_TWEET_LENGTH = 280
EMOJI_CATEGORIES = {
    "Humorous": ["😄", "😂", "🤣", "😊", "😉", "😎", "🤪", "😜", "🤓", "😇"],
    "Informative": ["📚", "📊", "📈", "🔍", "💡", "📝", "📋", "🔎", "📖", "📑"],
    "Inspirational": ["✨", "🌟", "💫", "⭐", "🔥", "💪", "🙌", "👏", "💯", "🎯"],
    "Serious": ["🤔", "💭", "🧐", "📢", "🔔", "⚖️", "🎓", "📊", "🔬", "📰"],
    "Casual": ["👋", "👍", "🙋", "💁", "🤗", "👌", "✌️", "🤝", "👊", "🙏"]
}

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

def smart_tweet_generator():
    """Enhanced Smart Tweet Generator with improved UI and AI integration."""
    st.title("✨ Smart Tweet Generator")
    st.markdown("Create engaging tweets with AI-powered optimization")
    
    # Apply theme
    Theme().apply()
    
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
                # Calculate engagement score
                engagement_score = calculate_engagement_score(
                    tweet["text"],
                    tweet["hashtags"],
                    tweet["emojis"],
                    tone
                )
                
                # Generate metrics
                metrics = generate_tweet_metrics(engagement_score)
                
                # Display tweet card
                TweetCard(
                    content=tweet["text"],
                    engagement_score=engagement_score,
                    hashtags=tweet["hashtags"],
                    emojis=tweet["emojis"],
                    metrics=metrics,
                    on_copy=lambda: copy_to_clipboard(tweet["text"]),
                    on_save=lambda: save_tweet(tweet)
                ).render()
                
                st.markdown("---")
            
            # Export options
            st.markdown("### 📥 Export Options")
            col1, col2 = st.columns(2)
            with col1:
                create_download_button(
                    data=tweets,
                    filename=f"tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    button_text="Export as JSON"
                )
            with col2:
                if st.button("Copy All Tweets"):
                    tweet_texts = "\n\n".join(tweet["text"] for tweet in tweets)
                    copy_to_clipboard(tweet_texts)
                    show_success_message("All tweets copied to clipboard!")

def save_tweet(tweet: Dict):
    """Save tweet for later."""
    tweets = get_from_session("tweets", [])
    tweets.append(tweet)
    save_to_session("tweets", tweets)
    show_success_message("Tweet saved successfully!")

if __name__ == "__main__":
    smart_tweet_generator() 
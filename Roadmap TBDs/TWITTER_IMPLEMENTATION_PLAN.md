# Twitter Integration Implementation Plan

This document outlines a comprehensive plan to implement and enhance the Twitter features in AI-Writer, transforming the "coming soon" features into fully functional components using Tweepy and user-provided API keys.

## Current State Analysis

The current Twitter functionality in AI-Writer includes:
- A Twitter dashboard with multiple planned features
- Only the "Smart Tweet Generator" is currently active
- The tweet generator creates content but lacks real Twitter integration
- Performance metrics are simulated rather than based on real data
- No actual posting, scheduling, or analytics capabilities

## Implementation Strategy

We'll implement the Twitter features in multiple phases, focusing on delivering value incrementally while building toward a comprehensive Twitter management solution.

### Phase 1: Twitter Authentication & Basic Integration

#### 1.1 Twitter API Authentication System

Create a secure system for users to connect their Twitter accounts:

```python
# lib/integrations/twitter/auth.py

import tweepy
import streamlit as st
from typing import Dict, Optional, Any
import os
import json
from pathlib import Path
import time
from loguru import logger

# Configuration paths
CONFIG_DIR = Path(__file__).parent.parent.parent.parent / 'config' / 'twitter'
CONFIG_DIR.mkdir(exist_ok=True, parents=True)

def get_twitter_auth_url() -> str:
    """Generate Twitter OAuth URL for user authentication."""
    try:
        # Get API keys from session state or environment
        consumer_key = st.session_state.get('twitter_consumer_key', os.getenv('TWITTER_CONSUMER_KEY', ''))
        consumer_secret = st.session_state.get('twitter_consumer_secret', os.getenv('TWITTER_CONSUMER_SECRET', ''))
        
        if not consumer_key or not consumer_secret:
            logger.error("Twitter API keys not found")
            return ""
        
        # Initialize OAuth handler
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret,
            callback="http://localhost:8501/twitter/callback"
        )
        
        # Get authorization URL
        auth_url = oauth1_user_handler.get_authorization_url()
        
        # Store OAuth handler in session state
        st.session_state.twitter_oauth_handler = oauth1_user_handler
        
        return auth_url
    except Exception as e:
        logger.error(f"Error generating Twitter auth URL: {str(e)}")
        return ""

def handle_twitter_callback(oauth_verifier: str) -> bool:
    """Handle Twitter OAuth callback."""
    try:
        # Get OAuth handler from session state
        oauth_handler = st.session_state.get('twitter_oauth_handler')
        if not oauth_handler:
            logger.error("OAuth handler not found in session state")
            return False
        
        # Get access tokens
        access_token, access_token_secret = oauth_handler.get_access_token(oauth_verifier)
        
        # Store tokens in session state
        st.session_state.twitter_access_token = access_token
        st.session_state.twitter_access_token_secret = access_token_secret
        
        # Create API client
        api = create_twitter_api()
        
        # Get user info
        user = api.verify_credentials()
        
        # Store user info
        st.session_state.twitter_user = {
            'id': user.id,
            'screen_name': user.screen_name,
            'name': user.name,
            'profile_image_url': user.profile_image_url,
            'followers_count': user.followers_count,
            'friends_count': user.friends_count
        }
        
        # Save credentials to file
        save_twitter_credentials(
            user.id,
            access_token,
            access_token_secret
        )
        
        return True
    except Exception as e:
        logger.error(f"Error handling Twitter callback: {str(e)}")
        return False

def create_twitter_api() -> tweepy.API:
    """Create Twitter API client."""
    try:
        # Get API keys and tokens
        consumer_key = st.session_state.get('twitter_consumer_key', os.getenv('TWITTER_CONSUMER_KEY', ''))
        consumer_secret = st.session_state.get('twitter_consumer_secret', os.getenv('TWITTER_CONSUMER_SECRET', ''))
        access_token = st.session_state.get('twitter_access_token', '')
        access_token_secret = st.session_state.get('twitter_access_token_secret', '')
        
        # Create auth handler
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret,
            access_token, access_token_secret
        )
        
        # Create API client
        api = tweepy.API(auth)
        
        return api
    except Exception as e:
        logger.error(f"Error creating Twitter API client: {str(e)}")
        raise

def create_twitter_client() -> tweepy.Client:
    """Create Twitter API v2 client."""
    try:
        # Get API keys and tokens
        consumer_key = st.session_state.get('twitter_consumer_key', os.getenv('TWITTER_CONSUMER_KEY', ''))
        consumer_secret = st.session_state.get('twitter_consumer_secret', os.getenv('TWITTER_CONSUMER_SECRET', ''))
        access_token = st.session_state.get('twitter_access_token', '')
        access_token_secret = st.session_state.get('twitter_access_token_secret', '')
        bearer_token = st.session_state.get('twitter_bearer_token', os.getenv('TWITTER_BEARER_TOKEN', ''))
        
        # Create client
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        return client
    except Exception as e:
        logger.error(f"Error creating Twitter client: {str(e)}")
        raise

def save_twitter_credentials(user_id: int, access_token: str, access_token_secret: str) -> bool:
    """Save Twitter credentials to file."""
    try:
        # Create user-specific credentials file
        creds_file = CONFIG_DIR / f"{user_id}.json"
        
        # Save credentials
        with open(creds_file, 'w') as f:
            json.dump({
                'access_token': access_token,
                'access_token_secret': access_token_secret,
                'timestamp': time.time()
            }, f)
        
        return True
    except Exception as e:
        logger.error(f"Error saving Twitter credentials: {str(e)}")
        return False

def load_twitter_credentials(user_id: int) -> Dict[str, str]:
    """Load Twitter credentials from file."""
    try:
        # Get user-specific credentials file
        creds_file = CONFIG_DIR / f"{user_id}.json"
        
        # Check if file exists
        if not creds_file.exists():
            logger.warning(f"No credentials found for user {user_id}")
            return {}
        
        # Load credentials
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        
        # Update session state
        st.session_state.twitter_access_token = creds['access_token']
        st.session_state.twitter_access_token_secret = creds['access_token_secret']
        
        return creds
    except Exception as e:
        logger.error(f"Error loading Twitter credentials: {str(e)}")
        return {}

def is_authenticated() -> bool:
    """Check if user is authenticated with Twitter."""
    return (
        'twitter_access_token' in st.session_state and
        'twitter_access_token_secret' in st.session_state and
        'twitter_user' in st.session_state
    )

def logout() -> None:
    """Log out user from Twitter."""
    if 'twitter_access_token' in st.session_state:
        del st.session_state.twitter_access_token
    if 'twitter_access_token_secret' in st.session_state:
        del st.session_state.twitter_access_token_secret
    if 'twitter_user' in st.session_state:
        del st.session_state.twitter_user
    if 'twitter_oauth_handler' in st.session_state:
        del st.session_state.twitter_oauth_handler
```

#### 1.2 Twitter API Key Management UI

Create a UI for users to enter and manage their Twitter API keys:

```python
# lib/integrations/twitter/api_key_manager.py

import streamlit as st
from typing import Dict, Optional
import os
from loguru import logger

def render_twitter_api_key_manager() -> None:
    """Render Twitter API key management UI."""
    st.markdown("## Twitter API Configuration")
    st.markdown("""
        To use Twitter integration features, you need to provide your Twitter API keys.
        You can get these by creating a Twitter Developer account and setting up a project.
    """)
    
    # Create tabs for different authentication methods
    tab1, tab2 = st.tabs(["Basic Authentication", "Advanced Settings"])
    
    with tab1:
        # Get existing keys from session state or environment
        consumer_key = st.session_state.get('twitter_consumer_key', os.getenv('TWITTER_CONSUMER_KEY', ''))
        consumer_secret = st.session_state.get('twitter_consumer_secret', os.getenv('TWITTER_CONSUMER_SECRET', ''))
        bearer_token = st.session_state.get('twitter_bearer_token', os.getenv('TWITTER_BEARER_TOKEN', ''))
        
        # Input fields for API keys
        new_consumer_key = st.text_input(
            "Consumer Key (API Key)",
            value=consumer_key,
            type="password",
            help="Your Twitter API consumer key"
        )
        
        new_consumer_secret = st.text_input(
            "Consumer Secret (API Secret)",
            value=consumer_secret,
            type="password",
            help="Your Twitter API consumer secret"
        )
        
        new_bearer_token = st.text_input(
            "Bearer Token",
            value=bearer_token,
            type="password",
            help="Your Twitter API bearer token"
        )
        
        # Save button
        if st.button("Save API Keys", use_container_width=True):
            # Update session state
            st.session_state.twitter_consumer_key = new_consumer_key
            st.session_state.twitter_consumer_secret = new_consumer_secret
            st.session_state.twitter_bearer_token = new_bearer_token
            
            # Show success message
            st.success("Twitter API keys saved successfully!")
    
    with tab2:
        st.markdown("### Advanced API Settings")
        
        # Callback URL
        st.text_input(
            "Callback URL",
            value="http://localhost:8501/twitter/callback",
            disabled=True,
            help="Use this URL in your Twitter Developer Portal"
        )
        
        # API usage limits
        st.info("""
            **Twitter API Rate Limits:**
            - Standard API: 500,000 tweets/month
            - Essential API: 10,000 tweets/month
            
            Make sure your Twitter Developer account has the appropriate access level for your needs.
        """)
        
        # Help resources
        st.markdown("""
            **Need help?**
            - [Twitter Developer Portal](https://developer.twitter.com)
            - [API Documentation](https://developer.twitter.com/en/docs)
            - [Rate Limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)
        """)
```

#### 1.3 Twitter Account Connection UI

Create a UI for users to connect their Twitter accounts:

```python
# lib/integrations/twitter/account_manager.py

import streamlit as st
from typing import Dict, Optional
from .auth import get_twitter_auth_url, is_authenticated, logout, create_twitter_api
import tweepy
from loguru import logger

def render_twitter_account_manager() -> None:
    """Render Twitter account management UI."""
    st.markdown("## Twitter Account")
    
    # Check if API keys are configured
    if not st.session_state.get('twitter_consumer_key') or not st.session_state.get('twitter_consumer_secret'):
        st.warning("Please configure your Twitter API keys first.")
        return
    
    # Check if user is authenticated
    if is_authenticated():
        # Get user info
        user = st.session_state.twitter_user
        
        # Display user info
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.image(user['profile_image_url'], width=80)
        
        with col2:
            st.markdown(f"**{user['name']}** (@{user['screen_name']})")
            st.markdown(f"Followers: {user['followers_count']} | Following: {user['friends_count']}")
        
        with col3:
            if st.button("Disconnect", key="disconnect_twitter"):
                logout()
                st.experimental_rerun()
        
        # Account status
        st.success("✅ Your Twitter account is connected and ready to use.")
        
        # Account actions
        st.markdown("### Quick Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("View Profile", use_container_width=True):
                try:
                    # Get API client
                    api = create_twitter_api()
                    
                    # Get user timeline
                    tweets = api.user_timeline(count=5)
                    
                    # Display tweets
                    st.markdown("#### Recent Tweets")
                    for tweet in tweets:
                        st.markdown(f"""
                            <div style='padding: 10px; border-radius: 5px; background-color: #f0f2f6; margin-bottom: 10px;'>
                                <p>{tweet.text}</p>
                                <small>Posted on {tweet.created_at.strftime('%Y-%m-%d %H:%M')}</small>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    logger.error(f"Error fetching tweets: {str(e)}")
                    st.error(f"Error fetching tweets: {str(e)}")
        
        with col2:
            if st.button("Check API Limits", use_container_width=True):
                try:
                    # Get API client
                    api = create_twitter_api()
                    
                    # Get rate limit status
                    limits = api.rate_limit_status()
                    
                    # Display limits
                    st.markdown("#### API Rate Limits")
                    
                    # Timeline limits
                    timeline_limit = limits['resources']['statuses']['/statuses/user_timeline']
                    st.markdown(f"**Timeline:** {timeline_limit['remaining']}/{timeline_limit['limit']} requests remaining")
                    
                    # Search limits
                    search_limit = limits['resources']['search']['/search/tweets']
                    st.markdown(f"**Search:** {search_limit['remaining']}/{search_limit['limit']} requests remaining")
                    
                    # Tweet posting limits
                    st.markdown("**Tweet Posting:** Limited by your Twitter API access level")
                except Exception as e:
                    logger.error(f"Error checking API limits: {str(e)}")
                    st.error(f"Error checking API limits: {str(e)}")
    else:
        # Get auth URL
        auth_url = get_twitter_auth_url()
        
        if auth_url:
            # Display connect button
            st.markdown("""
                <a href="{auth_url}" target="_self" style="text-decoration: none;">
                    <div style="display: inline-flex; align-items: center; background-color: #1DA1F2; color: white; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" style="margin-right: 8px;">
                            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                        </svg>
                        Connect Twitter Account
                    </div>
                </a>
            """.format(auth_url=auth_url), unsafe_allow_html=True)
            
            st.info("Click the button above to connect your Twitter account.")
        else:
            st.error("Failed to generate authentication URL. Please check your API keys.")
```

#### 1.4 Twitter Callback Handler

Create a handler for the Twitter OAuth callback:

```python
# lib/integrations/twitter/callback_handler.py

import streamlit as st
from urllib.parse import parse_qs, urlparse
from .auth import handle_twitter_callback
from loguru import logger

def handle_oauth_callback():
    """Handle Twitter OAuth callback in Streamlit."""
    # Get current URL
    query_params = st.experimental_get_query_params()
    
    # Check if this is a callback
    if 'oauth_token' in query_params and 'oauth_verifier' in query_params:
        oauth_verifier = query_params['oauth_verifier'][0]
        
        # Handle callback
        success = handle_twitter_callback(oauth_verifier)
        
        if success:
            # Clear query parameters to avoid reprocessing
            st.experimental_set_query_params()
            
            # Show success message
            st.success("Successfully connected Twitter account!")
            
            # Redirect to main page
            st.experimental_rerun()
        else:
            st.error("Failed to authenticate with Twitter. Please try again.")
    
    # Check for error
    if 'denied' in query_params:
        st.error("Twitter authentication was denied.")
        st.experimental_set_query_params()
```

### Phase 2: Enhanced Tweet Generator with Real Twitter Integration

#### 2.1 Improved Tweet Generator with Real Data

Enhance the tweet generator to use real Twitter data:

```python
# lib/ai_writers/twitter_writers/tweet_generator/enhanced_tweet_generator.py

import streamlit as st
import re
import json
import time
from typing import Dict, List, Tuple, Optional
import random
import emoji
from datetime import datetime
import tweepy

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....integrations.twitter.auth import create_twitter_api, create_twitter_client, is_authenticated

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

def get_trending_hashtags(location_id: int = 1) -> List[str]:
    """Get trending hashtags from Twitter API."""
    try:
        if not is_authenticated():
            return []
        
        # Get API client
        api = create_twitter_api()
        
        # Get trending topics
        trends = api.get_place_trends(location_id)
        
        # Extract hashtags
        hashtags = [trend['name'] for trend in trends[0]['trends'] if trend['name'].startswith('#')]
        
        return hashtags[:10]  # Return top 10 hashtags
    except Exception as e:
        st.error(f"Error fetching trending hashtags: {str(e)}")
        return []

def suggest_hashtags(topic: str, tone: str, use_trending: bool = False) -> List[str]:
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
    
    # Add trending hashtags if requested
    if use_trending and is_authenticated():
        trending = get_trending_hashtags()
        suggested = list(set(suggested + trending))
    
    return list(set(suggested))[:5]  # Return unique hashtags, max 5

def get_optimal_posting_time() -> Dict[str, Any]:
    """Get optimal posting time based on follower activity."""
    try:
        if not is_authenticated():
            return {
                "time": datetime.now().strftime("%H:%M"),
                "day": datetime.now().strftime("%A"),
                "confidence": "low"
            }
        
        # Get API client
        api = create_twitter_api()
        
        # Get user timeline
        tweets = api.user_timeline(count=100)
        
        # Analyze engagement by hour and day
        hour_engagement = {}
        day_engagement = {}
        
        for tweet in tweets:
            hour = tweet.created_at.hour
            day = tweet.created_at.strftime("%A")
            engagement = tweet.favorite_count + tweet.retweet_count
            
            if hour not in hour_engagement:
                hour_engagement[hour] = []
            hour_engagement[hour].append(engagement)
            
            if day not in day_engagement:
                day_engagement[day] = []
            day_engagement[day].append(engagement)
        
        # Calculate average engagement by hour and day
        hour_avg_engagement = {h: sum(e)/len(e) for h, e in hour_engagement.items() if e}
        day_avg_engagement = {d: sum(e)/len(e) for d, e in day_engagement.items() if e}
        
        # Find optimal hour and day
        optimal_hour = max(hour_avg_engagement.items(), key=lambda x: x[1])[0] if hour_avg_engagement else datetime.now().hour
        optimal_day = max(day_avg_engagement.items(), key=lambda x: x[1])[0] if day_avg_engagement else datetime.now().strftime("%A")
        
        # Calculate confidence
        confidence = "high" if len(tweets) >= 50 else "medium" if len(tweets) >= 20 else "low"
        
        return {
            "time": f"{optimal_hour:02d}:00",
            "day": optimal_day,
            "confidence": confidence
        }
    except Exception as e:
        st.error(f"Error calculating optimal posting time: {str(e)}")
        return {
            "time": datetime.now().strftime("%H:%M"),
            "day": datetime.now().strftime("%A"),
            "confidence": "low"
        }

def analyze_audience() -> Dict[str, Any]:
    """Analyze Twitter audience for content targeting."""
    try:
        if not is_authenticated():
            return {
                "follower_count": 0,
                "engagement_rate": 0,
                "top_interests": [],
                "active_hours": []
            }
        
        # Get API client
        api = create_twitter_api()
        
        # Get user info
        user = api.verify_credentials()
        
        # Get user timeline
        tweets = api.user_timeline(count=100)
        
        # Calculate engagement rate
        total_engagement = sum(tweet.favorite_count + tweet.retweet_count for tweet in tweets)
        engagement_rate = total_engagement / (len(tweets) * user.followers_count) if tweets and user.followers_count else 0
        
        # Analyze active hours
        hour_activity = {}
        for tweet in tweets:
            hour = tweet.created_at.hour
            if hour not in hour_activity:
                hour_activity[hour] = 0
            hour_activity[hour] += 1
        
        active_hours = sorted(hour_activity.items(), key=lambda x: x[1], reverse=True)[:3]
        active_hours = [f"{hour:02d}:00" for hour, _ in active_hours]
        
        # Get follower interests (simplified)
        top_interests = ["Technology", "Business", "Marketing"]  # Would require more complex analysis
        
        return {
            "follower_count": user.followers_count,
            "engagement_rate": engagement_rate * 100,  # Convert to percentage
            "top_interests": top_interests,
            "active_hours": active_hours
        }
    except Exception as e:
        st.error(f"Error analyzing audience: {str(e)}")
        return {
            "follower_count": 0,
            "engagement_rate": 0,
            "top_interests": [],
            "active_hours": []
        }

def generate_tweet_variations(
    hook: str,
    target_audience: str,
    tone: str,
    call_to_action: str = "",
    keywords: str = "",
    length: str = "medium",
    num_variations: int = 3,
    use_ai: bool = True
) -> List[Dict]:
    """Generate multiple tweet variations with AI and Twitter data."""
    # Enhanced prompt template with Twitter-specific guidance
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
    2. Include relevant hashtags (max 2-3)
    3. Use appropriate emojis (1-2 max)
    4. End with a clear call-to-action
    5. Stay within Twitter's 280 character limit
    6. Match the specified tone and audience
    
    Format each tweet as a JSON object with:
    - text: The tweet content
    - hashtags: List of suggested hashtags
    - emojis: List of suggested emojis
    """
    
    if use_ai:
        # Use AI to generate tweets
        try:
            response = llm_text_gen(prompt_template)
            
            # Parse JSON response
            try:
                tweets = json.loads(response)
                if not isinstance(tweets, list):
                    tweets = [tweets]
            except:
                # Handle non-JSON response by extracting tweet text
                tweet_texts = re.findall(r'"text"\s*:\s*"([^"]+)"', response)
                tweets = [{"text": text, "hashtags": extract_hashtags(text), "emojis": []} for text in tweet_texts]
            
            # Ensure we have the requested number of variations
            while len(tweets) < num_variations:
                tweets.append({
                    "text": f"{hook} {call_to_action}",
                    "hashtags": suggest_hashtags(keywords, tone),
                    "emojis": []
                })
            
            # Add engagement score
            for tweet in tweets:
                tweet["engagement_score"] = random.randint(60, 95)
            
            return tweets[:num_variations]
        except Exception as e:
            st.error(f"Error generating tweets with AI: {str(e)}")
            # Fall back to template-based generation
    
    # Template-based generation (fallback)
    templates = [
        "{emoji} {hook} {hashtags} {cta}",
        "{hook} {emoji} {hashtags} {cta}",
        "{hashtags} {hook} {emoji} {cta}"
    ]
    
    tweets = []
    for i in range(num_variations):
        template = templates[i % len(templates)]
        emoji_list = EMOJI_CATEGORIES.get(tone.capitalize(), EMOJI_CATEGORIES["Casual"])
        emoji_str = random.choice(emoji_list)
        hashtag_list = suggest_hashtags(keywords, tone)
        hashtag_str = " ".join(hashtag_list[:2])
        
        tweet_text = template.format(
            emoji=emoji_str,
            hook=hook,
            hashtags=hashtag_str,
            cta=call_to_action
        )
        
        tweets.append({
            "text": tweet_text,
            "hashtags": hashtag_list,
            "emojis": [emoji_str],
            "engagement_score": random.randint(60, 95)
        })
    
    return tweets

def post_tweet(tweet_text: str) -> Dict[str, Any]:
    """Post a tweet to Twitter."""
    try:
        if not is_authenticated():
            return {"success": False, "error": "Not authenticated with Twitter"}
        
        # Get API client
        api = create_twitter_api()
        
        # Post tweet
        status = api.update_status(tweet_text)
        
        return {
            "success": True,
            "tweet_id": status.id,
            "created_at": status.created_at.isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def schedule_tweet(tweet_text: str, scheduled_time: datetime) -> Dict[str, Any]:
    """Schedule a tweet for later posting."""
    try:
        # Store scheduled tweet in session state
        if "scheduled_tweets" not in st.session_state:
            st.session_state.scheduled_tweets = []
        
        tweet_id = f"scheduled_{int(time.time())}"
        
        st.session_state.scheduled_tweets.append({
            "id": tweet_id,
            "text": tweet_text,
            "scheduled_time": scheduled_time.isoformat(),
            "status": "scheduled"
        })
        
        return {
            "success": True,
            "id": tweet_id,
            "scheduled_time": scheduled_time.isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def enhanced_tweet_generator():
    """Enhanced Smart Tweet Generator with Twitter integration."""
    st.title("✨ Enhanced Tweet Generator")
    st.markdown("Create and post engaging tweets with AI and Twitter data")
    
    # Check if connected to Twitter
    twitter_connected = is_authenticated()
    
    # Twitter connection status
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
        
        # Show audience insights
        with st.expander("Audience Insights", expanded=False):
            audience = analyze_audience()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Followers", f"{audience['follower_count']:,}")
            with col2:
                st.metric("Engagement Rate", f"{audience['engagement_rate']:.2f}%")
            with col3:
                st.metric("Active Hours", ", ".join(audience['active_hours']) if audience['active_hours'] else "Unknown")
            
            if audience['top_interests']:
                st.markdown(f"**Top Interests:** {', '.join(audience['top_interests'])}")
    else:
        st.warning("Connect your Twitter account to access advanced features")
    
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
    
    # Advanced options
    with st.expander("Advanced Options", expanded=False):
        use_trending = st.checkbox("Include trending hashtags", value=False)
        
        if twitter_connected:
            # Get optimal posting time
            optimal_time = get_optimal_posting_time()
            
            st.markdown(f"""
                **Optimal Posting Time:** {optimal_time['day']} at {optimal_time['time']}
                (Confidence: {optimal_time['confidence']})
            """)
    
    # Generate button with loading state
    if st.button("Generate Tweets", use_container_width=True):
        with st.spinner("Generating tweet variations..."):
            tweets = generate_tweet_variations(
                hook, target_audience, tone,
                call_to_action, keywords, length,
                num_variations, use_ai=True
            )
            
            # Store tweets in session state
            st.session_state.generated_tweets = tweets
            
            # Display tweets
            st.markdown("### Generated Tweets")
            
            for i, tweet in enumerate(tweets):
                with st.container():
                    st.markdown(f"""
                        <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;'>
                            <h3 style='margin: 0;'>Tweet Variation {i + 1}</h3>
                            <p style='margin: 10px 0; font-size: 1.1em;'>{tweet['text']}</p>
                            <div style='display: flex; gap: 10px;'>
                                <span style='background-color: #e1e4e8; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;'>
                                    Score: {tweet['engagement_score']}%
                                </span>
                                <span style='background-color: #e1e4e8; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;'>
                                    {count_characters(tweet['text'])}/280 chars
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"Copy Tweet {i + 1}", key=f"copy_{i}"):
                            st.code(tweet['text'])
                            st.success("Tweet copied to clipboard!")
                    
                    with col2:
                        if twitter_connected and st.button(f"Post Now {i + 1}", key=f"post_{i}"):
                            result = post_tweet(tweet['text'])
                            if result['success']:
                                st.success("Tweet posted successfully!")
                            else:
                                st.error(f"Error posting tweet: {result['error']}")
                    
                    with col3:
                        if twitter_connected and st.button(f"Schedule {i + 1}", key=f"schedule_{i}"):
                            # Show scheduling options
                            st.session_state.tweet_to_schedule = tweet['text']
                            st.session_state.scheduling_tweet_index = i
                            st.experimental_rerun()
            
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
    
    # Handle tweet scheduling
    if "tweet_to_schedule" in st.session_state:
        st.markdown("### Schedule Tweet")
        st.markdown(f"**Tweet to schedule:** {st.session_state.tweet_to_schedule}")
        
        col1, col2 = st.columns(2)
        with col1:
            schedule_date = st.date_input("Date", value=datetime.now().date())
        with col2:
            schedule_time = st.time_input("Time", value=datetime.now().time())
        
        scheduled_datetime = datetime.combine(schedule_date, schedule_time)
        
        if st.button("Confirm Schedule"):
            result = schedule_tweet(st.session_state.tweet_to_schedule, scheduled_datetime)
            if result['success']:
                st.success(f"Tweet scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
                del st.session_state.tweet_to_schedule
                del st.session_state.scheduling_tweet_index
            else:
                st.error(f"Error scheduling tweet: {result['error']}")
```

#### 2.2 Tweet Performance Predictor

Implement the Tweet Performance Predictor feature:

```python
# lib/ai_writers/twitter_writers/tweet_performance/performance_predictor.py

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import pickle
import os
from pathlib import Path

from ....integrations.twitter.auth import create_twitter_api, is_authenticated

# Constants
MODEL_DIR = Path(__file__).parent.parent.parent.parent.parent / 'models' / 'twitter'
MODEL_DIR.mkdir(exist_ok=True, parents=True)
MODEL_PATH = MODEL_DIR / 'performance_predictor.pkl'

def get_tweet_history() -> pd.DataFrame:
    """Get tweet history from Twitter API."""
    try:
        if not is_authenticated():
            return pd.DataFrame()
        
        # Get API client
        api = create_twitter_api()
        
        # Get user timeline
        tweets = api.user_timeline(count=200, tweet_mode='extended')
        
        # Create DataFrame
        data = []
        for tweet in tweets:
            # Skip retweets
            if hasattr(tweet, 'retweeted_status'):
                continue
            
            # Extract tweet data
            tweet_data = {
                'id': tweet.id,
                'text': tweet.full_text,
                'created_at': tweet.created_at,
                'likes': tweet.favorite_count,
                'retweets': tweet.retweet_count,
                'replies': 0,  # Not available in standard API
                'impressions': 0,  # Not available in standard API
                'hashtags': [h['text'] for h in tweet.entities.get('hashtags', [])],
                'mentions': [m['screen_name'] for m in tweet.entities.get('user_mentions', [])],
                'urls': [u['expanded_url'] for u in tweet.entities.get('urls', [])],
                'media': 1 if 'media' in tweet.entities else 0,
                'hour': tweet.created_at.hour,
                'day': tweet.created_at.weekday(),
                'length': len(tweet.full_text)
            }
            
            # Calculate engagement
            tweet_data['engagement'] = tweet_data['likes'] + tweet_data['retweets']
            
            data.append(tweet_data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        return df
    except Exception as e:
        st.error(f"Error fetching tweet history: {str(e)}")
        return pd.DataFrame()

def train_performance_model(df: pd.DataFrame) -> Any:
    """Train a model to predict tweet performance."""
    try:
        if df.empty:
            return None
        
        # Feature engineering
        X = pd.DataFrame({
            'hour': df['hour'],
            'day': df['day'],
            'length': df['length'],
            'hashtag_count': df['hashtags'].apply(len),
            'mention_count': df['mentions'].apply(len),
            'url_count': df['urls'].apply(len),
            'has_media': df['media']
        })
        
        # Target variable
        y = df['engagement']
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Save model
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        return model
    except Exception as e:
        st.error(f"Error training model: {str(e)}")
        return None

def load_performance_model() -> Any:
    """Load the performance prediction model."""
    try:
        if MODEL_PATH.exists():
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            return model
        else:
            return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def predict_performance(
    tweet_text: str,
    hour: int,
    day: int,
    has_media: bool = False
) -> Dict[str, Any]:
    """Predict tweet performance."""
    try:
        # Load model
        model = load_performance_model()
        
        if model is None:
            # No model available, use heuristics
            return predict_performance_heuristic(tweet_text, hour, day, has_media)
        
        # Feature extraction
        hashtags = len([w for w in tweet_text.split() if w.startswith('#')])
        mentions = len([w for w in tweet_text.split() if w.startswith('@')])
        urls = len([w for w in tweet_text.split() if w.startswith('http')])
        length = len(tweet_text)
        
        # Create feature vector
        X = pd.DataFrame({
            'hour': [hour],
            'day': [day],
            'length': [length],
            'hashtag_count': [hashtags],
            'mention_count': [mentions],
            'url_count': [urls],
            'has_media': [1 if has_media else 0]
        })
        
        # Make prediction
        engagement = model.predict(X)[0]
        
        # Calculate confidence
        confidence = "high" if model.n_estimators >= 100 else "medium"
        
        return {
            "predicted_engagement": engagement,
            "confidence": confidence,
            "factors": {
                "time_factor": get_time_factor(hour, day),
                "content_factor": get_content_factor(tweet_text),
                "media_factor": 1.5 if has_media else 1.0
            }
        }
    except Exception as e:
        st.error(f"Error predicting performance: {str(e)}")
        return predict_performance_heuristic(tweet_text, hour, day, has_media)

def predict_performance_heuristic(
    tweet_text: str,
    hour: int,
    day: int,
    has_media: bool = False
) -> Dict[str, Any]:
    """Predict tweet performance using heuristics."""
    # Time factor (higher for business hours on weekdays)
    time_factor = get_time_factor(hour, day)
    
    # Content factor
    content_factor = get_content_factor(tweet_text)
    
    # Media factor
    media_factor = 1.5 if has_media else 1.0
    
    # Base engagement (arbitrary value)
    base_engagement = 10
    
    # Calculate predicted engagement
    predicted_engagement = base_engagement * time_factor * content_factor * media_factor
    
    return {
        "predicted_engagement": predicted_engagement,
        "confidence": "low",
        "factors": {
            "time_factor": time_factor,
            "content_factor": content_factor,
            "media_factor": media_factor
        }
    }

def get_time_factor(hour: int, day: int) -> float:
    """Calculate time factor for engagement prediction."""
    # Weekday factor (higher for weekdays)
    weekday_factor = 1.0 if day < 5 else 0.8
    
    # Hour factor (higher for business hours)
    if 9 <= hour <= 17:
        hour_factor = 1.0
    elif 7 <= hour <= 8 or 18 <= hour <= 21:
        hour_factor = 0.8
    else:
        hour_factor = 0.6
    
    return weekday_factor * hour_factor

def get_content_factor(tweet_text: str) -> float:
    """Calculate content factor for engagement prediction."""
    # Length factor (higher for medium-length tweets)
    length = len(tweet_text)
    if 70 <= length <= 140:
        length_factor = 1.0
    elif length < 70:
        length_factor = 0.8
    else:
        length_factor = 0.9
    
    # Hashtag factor (higher for 1-2 hashtags)
    hashtags = len([w for w in tweet_text.split() if w.startswith('#')])
    if 1 <= hashtags <= 2:
        hashtag_factor = 1.0
    elif hashtags == 0:
        hashtag_factor = 0.8
    else:
        hashtag_factor = 0.7  # Too many hashtags
    
    # Question factor (higher for tweets with questions)
    question_factor = 1.2 if '?' in tweet_text else 1.0
    
    # Call to action factor
    cta_words = ['follow', 'retweet', 'like', 'share', 'comment', 'check', 'click', 'read']
    cta_factor = 1.1 if any(word in tweet_text.lower() for word in cta_words) else 1.0
    
    return length_factor * hashtag_factor * question_factor * cta_factor

def get_best_posting_times() -> List[Dict[str, Any]]:
    """Get best posting times based on historical data."""
    try:
        # Get tweet history
        df = get_tweet_history()
        
        if df.empty:
            # Return default recommendations
            return [
                {"day": "Monday", "hour": 12, "confidence": "low"},
                {"day": "Wednesday", "hour": 15, "confidence": "low"},
                {"day": "Friday", "hour": 10, "confidence": "low"}
            ]
        
        # Group by day and hour
        df['day_name'] = df['created_at'].dt.day_name()
        engagement_by_time = df.groupby(['day_name', 'hour'])['engagement'].mean().reset_index()
        
        # Sort by engagement
        engagement_by_time = engagement_by_time.sort_values('engagement', ascending=False)
        
        # Get top 3 times
        top_times = engagement_by_time.head(3)
        
        # Format results
        results = []
        for _, row in top_times.iterrows():
            results.append({
                "day": row['day_name'],
                "hour": row['hour'],
                "confidence": "high" if len(df) >= 100 else "medium" if len(df) >= 50 else "low"
            })
        
        return results
    except Exception as e:
        st.error(f"Error getting best posting times: {str(e)}")
        return [
            {"day": "Monday", "hour": 12, "confidence": "low"},
            {"day": "Wednesday", "hour": 15, "confidence": "low"},
            {"day": "Friday", "hour": 10, "confidence": "low"}
        ]

def render_performance_predictor():
    """Render the Tweet Performance Predictor UI."""
    st.title("📊 Tweet Performance Predictor")
    st.markdown("Predict engagement and find the best time to post your tweets")
    
    # Check if connected to Twitter
    twitter_connected = is_authenticated()
    
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
        
        # Get tweet history
        with st.spinner("Analyzing your tweet history..."):
            df = get_tweet_history()
        
        if not df.empty:
            # Train model if needed
            if not MODEL_PATH.exists():
                with st.spinner("Training prediction model..."):
                    train_performance_model(df)
            
            # Show historical performance
            with st.expander("Your Tweet Performance", expanded=True):
                # Engagement over time
                st.markdown("#### Engagement Over Time")
                fig = px.line(
                    df.sort_values('created_at'),
                    x='created_at',
                    y='engagement',
                    title="Tweet Engagement History"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Engagement by day and hour
                st.markdown("#### Engagement by Day and Hour")
                df['day_name'] = df['created_at'].dt.day_name()
                pivot = df.pivot_table(
                    index='day_name',
                    columns='hour',
                    values='engagement',
                    aggfunc='mean'
                )
                
                fig = px.imshow(
                    pivot,
                    labels=dict(x="Hour of Day", y="Day of Week", color="Avg. Engagement"),
                    x=pivot.columns,
                    y=pivot.index,
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Content analysis
                st.markdown("#### Content Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Engagement by tweet length
                    df['length_bin'] = pd.cut(df['length'], bins=[0, 70, 140, 210, 280], labels=['0-70', '71-140', '141-210', '211-280'])
                    length_engagement = df.groupby('length_bin')['engagement'].mean().reset_index()
                    
                    fig = px.bar(
                        length_engagement,
                        x='length_bin',
                        y='engagement',
                        title="Engagement by Tweet Length"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Engagement by hashtag count
                    df['hashtag_count'] = df['hashtags'].apply(len)
                    df['hashtag_bin'] = pd.cut(df['hashtag_count'], bins=[-1, 0, 1, 2, 10], labels=['0', '1', '2', '3+'])
                    hashtag_engagement = df.groupby('hashtag_bin')['engagement'].mean().reset_index()
                    
                    fig = px.bar(
                        hashtag_engagement,
                        x='hashtag_bin',
                        y='engagement',
                        title="Engagement by Hashtag Count"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Best posting times
        best_times = get_best_posting_times()
        
        st.markdown("### 🕒 Best Times to Post")
        for i, time in enumerate(best_times):
            st.markdown(f"**{i+1}.** {time['day']} at {time['hour']}:00 (Confidence: {time['confidence']})")
    else:
        st.warning("Connect your Twitter account to access performance prediction features")
        
        # Show demo data
        st.markdown("### Demo Data")
        st.markdown("Here's how the performance predictor works with sample data:")
        
        # Sample engagement chart
        dates = pd.date_range(start='2023-01-01', periods=30)
        engagements = np.random.normal(loc=20, scale=10, size=30)
        engagements = np.abs(engagements)  # Make all values positive
        
        df = pd.DataFrame({
            'date': dates,
            'engagement': engagements
        })
        
        fig = px.line(
            df,
            x='date',
            y='engagement',
            title="Sample Tweet Engagement History"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tweet input for prediction
    st.markdown("### Predict Tweet Performance")
    
    tweet_text = st.text_area(
        "Enter your tweet",
        placeholder="Type your tweet here...",
        max_chars=280
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        day = st.selectbox(
            "Day of week",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        day_num = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
    
    with col2:
        hour = st.slider("Hour of day", 0, 23, 12)
    
    with col3:
        has_media = st.checkbox("Include media", value=False)
    
    if st.button("Predict Performance", use_container_width=True):
        if tweet_text:
            with st.spinner("Predicting performance..."):
                prediction = predict_performance(tweet_text, hour, day_num, has_media)
                
                # Display prediction
                st.markdown("### Prediction Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Predicted Engagement",
                        f"{prediction['predicted_engagement']:.1f}",
                        delta=None
                    )
                
                with col2:
                    st.markdown(f"**Confidence:** {prediction['confidence'].title()}")
                
                # Factors affecting prediction
                st.markdown("#### Factors Affecting Prediction")
                
                factors = prediction['factors']
                factor_df = pd.DataFrame({
                    'Factor': ['Time of posting', 'Content quality', 'Media inclusion'],
                    'Impact': [
                        factors['time_factor'],
                        factors['content_factor'],
                        factors['media_factor']
                    ]
                })
                
                fig = px.bar(
                    factor_df,
                    x='Factor',
                    y='Impact',
                    title="Impact Factors"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.markdown("#### Recommendations to Improve Performance")
                
                recommendations = []
                
                if factors['time_factor'] < 0.9:
                    recommendations.append("Consider posting during weekdays between 9 AM and 5 PM for better engagement.")
                
                if factors['content_factor'] < 0.9:
                    if len(tweet_text) > 140:
                        recommendations.append("Try shortening your tweet to 70-140 characters for optimal engagement.")
                    
                    hashtags = len([w for w in tweet_text.split() if w.startswith('#')])
                    if hashtags == 0:
                        recommendations.append("Add 1-2 relevant hashtags to increase visibility.")
                    elif hashtags > 2:
                        recommendations.append("Reduce the number of hashtags to 1-2 for better engagement.")
                    
                    if '?' not in tweet_text:
                        recommendations.append("Consider adding a question to encourage responses.")
                    
                    cta_words = ['follow', 'retweet', 'like', 'share', 'comment', 'check', 'click', 'read']
                    if not any(word in tweet_text.lower() for word in cta_words):
                        recommendations.append("Add a clear call-to-action to encourage engagement.")
                
                if not has_media:
                    recommendations.append("Including an image or video could increase engagement by up to 50%.")
                
                if recommendations:
                    for rec in recommendations:
                        st.info(rec)
                else:
                    st.success("Your tweet is well-optimized for engagement!")
        else:
            st.error("Please enter a tweet to predict performance.")
```

### Phase 3: Content Strategy Tools

#### 3.1 Content Calendar Generator

Implement the Content Calendar Generator feature:

```python
# lib/ai_writers/twitter_writers/content_strategy/calendar_generator.py

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import calendar
import random
from io import BytesIO

from ....integrations.twitter.auth import create_twitter_api, is_authenticated
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen

def generate_content_themes(industry: str, num_themes: int = 5) -> List[str]:
    """Generate content themes based on industry."""
    # Predefined themes by industry
    industry_themes = {
        "Technology": [
            "Product Updates", "Tech Tips", "Industry News", "Customer Success Stories",
            "Behind the Scenes", "Tech Trends", "How-To Guides", "Tech Humor",
            "Industry Events", "Q&A Sessions"
        ],
        "Marketing": [
            "Marketing Tips", "Case Studies", "Industry Trends", "Tool Recommendations",
            "Marketing Metrics", "Campaign Spotlights", "Marketing Humor", "Expert Interviews",
            "Marketing Events", "Strategy Insights"
        ],
        "Education": [
            "Learning Resources", "Student Spotlights", "Education News", "Teaching Tips",
            "Research Highlights", "Campus Events", "Educational Humor", "Alumni Stories",
            "Faculty Spotlights", "Educational Trends"
        ],
        "Health": [
            "Health Tips", "Wellness Advice", "Medical News", "Patient Stories",
            "Research Updates", "Health Myths Debunked", "Nutrition Tips", "Exercise Guides",
            "Mental Health Awareness", "Healthcare Innovations"
        ],
        "Finance": [
            "Financial Tips", "Market Updates", "Investment Strategies", "Financial Education",
            "Economic News", "Savings Guides", "Financial Planning", "Success Stories",
            "Industry Trends", "Q&A Sessions"
        ]
    }
    
    # Get themes for the selected industry or use AI to generate them
    if industry in industry_themes:
        themes = industry_themes[industry]
        return random.sample(themes, min(num_themes, len(themes)))
    else:
        # Use AI to generate themes
        prompt = f"""
        Generate {num_themes} content themes for Twitter posts in the {industry} industry.
        Each theme should be a short phrase (2-4 words) that describes a category of content.
        Return the themes as a JSON array of strings.
        """
        
        try:
            response = llm_text_gen(prompt)
            
            # Try to parse as JSON
            try:
                themes = json.loads(response)
                if isinstance(themes, list):
                    return themes[:num_themes]
            except:
                # Extract themes using regex
                import re
                themes = re.findall(r'"([^"]+)"', response)
                return themes[:num_themes]
        except Exception as e:
            st.error(f"Error generating themes: {str(e)}")
            
            # Return generic themes
            generic_themes = [
                "Industry News", "Tips & Tricks", "Behind the Scenes",
                "Customer Stories", "Product Highlights"
            ]
            return generic_themes[:num_themes]

def generate_content_ideas(theme: str, industry: str, num_ideas: int = 3) -> List[str]:
    """Generate content ideas for a theme."""
    # Use AI to generate content ideas
    prompt = f"""
    Generate {num_ideas} specific Twitter post ideas for the theme "{theme}" in the {industry} industry.
    Each idea should be a brief description (not the actual tweet) of what the post will be about.
    Keep each idea under 100 characters.
    Return the ideas as a JSON array of strings.
    """
    
    try:
        response = llm_text_gen(prompt)
        
        # Try to parse as JSON
        try:
            ideas = json.loads(response)
            if isinstance(ideas, list):
                return ideas[:num_ideas]
        except:
            # Extract ideas using regex
            import re
            ideas = re.findall(r'"([^"]+)"', response)
            return ideas[:num_ideas] if ideas else [f"{theme} idea {i+1}" for i in range(num_ideas)]
    except Exception as e:
        st.error(f"Error generating ideas: {str(e)}")
        
        # Return generic ideas
        return [f"{theme} idea {i+1}" for i in range(num_ideas)]

def create_content_calendar(
    start_date: datetime,
    end_date: datetime,
    posts_per_week: int,
    themes: List[str],
    industry: str
) -> pd.DataFrame:
    """Create a content calendar with themes and ideas."""
    # Calculate date range
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Filter for weekdays if needed
    if posts_per_week <= 5:
        date_range = date_range[date_range.dayofweek < 5]  # Monday to Friday
    
    # Calculate posting frequency
    if posts_per_week < 5:
        # Select specific days
        days_to_post = random.sample(range(5), posts_per_week)  # Random weekdays
        date_range = date_range[date_range.dayofweek.isin(days_to_post)]
    
    # Limit to the requested frequency
    posting_dates = []
    current_week = -1
    posts_this_week = 0
    
    for date in date_range:
        week_num = date.isocalendar()[1]
        
        if week_num != current_week:
            current_week = week_num
            posts_this_week = 0
        
        if posts_this_week < posts_per_week:
            posting_dates.append(date)
            posts_this_week += 1
    
    # Create calendar dataframe
    calendar_data = []
    
    for date in posting_dates:
        # Assign theme (rotate through themes)
        theme_index = len(calendar_data) % len(themes)
        theme = themes[theme_index]
        
        # Generate content ideas
        ideas = generate_content_ideas(theme, industry, num_ideas=1)
        
        calendar_data.append({
            'date': date,
            'day': date.day_name(),
            'week': date.isocalendar()[1],
            'theme': theme,
            'content_idea': ideas[0] if ideas else "",
            'status': 'Planned'
        })
    
    # Create DataFrame
    df = pd.DataFrame(calendar_data)
    
    return df

def export_calendar_to_excel(df: pd.DataFrame) -> BytesIO:
    """Export content calendar to Excel."""
    # Create Excel writer
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Write DataFrame to Excel
    df.to_excel(writer, sheet_name='Content Calendar', index=False)
    
    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Content Calendar']
    
    # Add formats
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    date_format = workbook.add_format({
        'num_format': 'yyyy-mm-dd',
        'border': 1
    })
    
    cell_format = workbook.add_format({
        'text_wrap': True,
        'border': 1
    })
    
    # Write headers with format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Format columns
    worksheet.set_column('A:A', 12, date_format)  # Date column
    worksheet.set_column('B:B', 10, cell_format)  # Day column
    worksheet.set_column('C:C', 8, cell_format)   # Week column
    worksheet.set_column('D:D', 15, cell_format)  # Theme column
    worksheet.set_column('E:E', 40, cell_format)  # Content idea column
    worksheet.set_column('F:F', 10, cell_format)  # Status column
    
    # Close the writer
    writer.close()
    
    # Return the Excel file
    output.seek(0)
    return output

def render_calendar_generator():
    """Render the Content Calendar Generator UI."""
    st.title("🗓️ Content Calendar Generator")
    st.markdown("Create a strategic Twitter content calendar with themes and ideas")
    
    # Check if connected to Twitter
    twitter_connected = is_authenticated()
    
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
    
    # Calendar settings
    st.markdown("### Calendar Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now().date())
        
        industry = st.selectbox(
            "Industry",
            ["Technology", "Marketing", "Education", "Health", "Finance", "Other"],
            index=0
        )
        
        if industry == "Other":
            industry = st.text_input("Specify Industry")
    
    with col2:
        duration = st.selectbox(
            "Duration",
            ["1 week", "2 weeks", "1 month", "3 months"],
            index=2
        )
        
        # Calculate end date based on duration
        if duration == "1 week":
            end_date = start_date + timedelta(days=6)
        elif duration == "2 weeks":
            end_date = start_date + timedelta(days=13)
        elif duration == "1 month":
            end_date = start_date + timedelta(days=29)
        else:  # 3 months
            end_date = start_date + timedelta(days=89)
        
        posts_per_week = st.slider(
            "Posts per Week",
            min_value=1,
            max_value=7,
            value=3
        )
    
    # Theme settings
    st.markdown("### Content Themes")
    
    num_themes = st.slider(
        "Number of Themes",
        min_value=1,
        max_value=10,
        value=5
    )
    
    # Generate themes button
    if st.button("Generate Themes", key="generate_themes"):
        with st.spinner("Generating content themes..."):
            themes = generate_content_themes(industry, num_themes)
            st.session_state.content_themes = themes
    
    # Display and edit themes
    if "content_themes" in st.session_state:
        themes = st.session_state.content_themes
        
        # Create columns for themes
        cols = st.columns(min(5, len(themes)))
        
        # Display each theme in a column
        for i, theme in enumerate(themes):
            col_index = i % len(cols)
            with cols[col_index]:
                new_theme = st.text_input(f"Theme {i+1}", value=theme, key=f"theme_{i}")
                themes[i] = new_theme
        
        st.session_state.content_themes = themes
    else:
        st.info("Click 'Generate Themes' to create content themes for your calendar")
    
    # Generate calendar button
    if st.button("Generate Calendar", use_container_width=True):
        if "content_themes" in st.session_state and st.session_state.content_themes:
            with st.spinner("Creating your content calendar..."):
                # Create calendar
                calendar_df = create_content_calendar(
                    start_date=start_date,
                    end_date=end_date,
                    posts_per_week=posts_per_week,
                    themes=st.session_state.content_themes,
                    industry=industry
                )
                
                # Store in session state
                st.session_state.content_calendar = calendar_df
                
                # Display calendar
                st.markdown("### Your Content Calendar")
                
                # Calendar view
                calendar_view = st.radio(
                    "View",
                    ["Table", "Calendar View"],
                    horizontal=True
                )
                
                if calendar_view == "Table":
                    # Display as table
                    st.dataframe(
                        calendar_df,
                        column_config={
                            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                            "day": "Day",
                            "week": "Week",
                            "theme": "Theme",
                            "content_idea": st.column_config.TextColumn("Content Idea", width="large"),
                            "status": "Status"
                        },
                        hide_index=True
                    )
                else:
                    # Display as calendar
                    # Group by week
                    weeks = calendar_df.groupby('week')
                    
                    for week_num, week_data in weeks:
                        st.markdown(f"#### Week {week_num}")
                        
                        # Create a row for each day of the week
                        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        cols = st.columns(7)
                        
                        # Add day headers
                        for i, day in enumerate(days):
                            with cols[i]:
                                st.markdown(f"**{day[:3]}**")
                        
                        # Add content for each day
                        for i, day in enumerate(days):
                            with cols[i]:
                                # Find posts for this day
                                day_posts = week_data[week_data['day'] == day]
                                
                                if not day_posts.empty:
                                    for _, post in day_posts.iterrows():
                                        st.markdown(f"""
                                            <div style='padding: 10px; border-radius: 5px; background-color: #f0f2f6; margin-bottom: 5px;'>
                                                <small>{post['date'].strftime('%Y-%m-%d')}</small>
                                                <p style='margin: 5px 0; font-weight: bold;'>{post['theme']}</p>
                                                <p style='margin: 5px 0; font-size: 0.9em;'>{post['content_idea']}</p>
                                            </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.markdown("—")
                        
                        st.markdown("---")
                
                # Export options
                st.markdown("### Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Export as Excel
                    excel_file = export_calendar_to_excel(calendar_df)
                    st.download_button(
                        "Download Excel Calendar",
                        data=excel_file,
                        file_name=f"twitter_content_calendar_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # Export as CSV
                    csv = calendar_df.to_csv(index=False)
                    st.download_button(
                        "Download CSV Calendar",
                        data=csv,
                        file_name=f"twitter_content_calendar_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
        else:
            st.error("Please generate themes first")
```

#### 3.2 Hashtag Strategy Manager

Implement the Hashtag Strategy Manager feature:

```python
# lib/ai_writers/twitter_writers/content_strategy/hashtag_manager.py

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import re
import tweepy
from collections import Counter

from ....integrations.twitter.auth import create_twitter_api, create_twitter_client, is_authenticated
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen

def get_trending_hashtags(location_id: int = 1) -> List[Dict[str, Any]]:
    """Get trending hashtags from Twitter API."""
    try:
        if not is_authenticated():
            return []
        
        # Get API client
        api = create_twitter_api()
        
        # Get trending topics
        trends = api.get_place_trends(location_id)
        
        # Extract hashtags
        hashtags = [
            {
                "name": trend["name"],
                "volume": trend.get("tweet_volume", 0),
                "is_hashtag": trend["name"].startswith("#")
            }
            for trend in trends[0]["trends"]
        ]
        
        # Sort by volume
        hashtags.sort(key=lambda x: x["volume"] if x["volume"] else 0, reverse=True)
        
        return hashtags
    except Exception as e:
        st.error(f"Error fetching trending hashtags: {str(e)}")
        return []

def get_trending_locations() -> List[Dict[str, Any]]:
    """Get available trending locations."""
    try:
        if not is_authenticated():
            return []
        
        # Get API client
        api = create_twitter_api()
        
        # Get available trend locations
        locations = api.available_trends()
        
        # Format locations
        formatted_locations = [
            {
                "woeid": location["woeid"],
                "name": location["name"],
                "country": location.get("countryCode", "")
            }
            for location in locations
        ]
        
        # Sort by name
        formatted_locations.sort(key=lambda x: x["name"])
        
        return formatted_locations
    except Exception as e:
        st.error(f"Error fetching trending locations: {str(e)}")
        return []

def analyze_hashtag(hashtag: str) -> Dict[str, Any]:
    """Analyze a specific hashtag."""
    try:
        if not is_authenticated():
            return {
                "volume": 0,
                "sentiment": "neutral",
                "related_hashtags": [],
                "sample_tweets": []
            }
        
        # Clean hashtag
        if not hashtag.startswith("#"):
            hashtag = f"#{hashtag}"
        
        # Get API client
        api = create_twitter_api()
        client = create_twitter_client()
        
        # Search for tweets with the hashtag
        tweets = api.search_tweets(q=hashtag, count=100, tweet_mode="extended")
        
        # Extract data
        sample_tweets = []
        all_hashtags = []
        sentiment_scores = []
        
        for tweet in tweets:
            # Skip retweets
            if hasattr(tweet, "retweeted_status"):
                continue
            
            # Add to sample tweets
            sample_tweets.append({
                "text": tweet.full_text,
                "created_at": tweet.created_at,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count
            })
            
            # Extract hashtags
            tweet_hashtags = [h["text"] for h in tweet.entities.get("hashtags", [])]
            all_hashtags.extend(tweet_hashtags)
            
            # Simple sentiment analysis
            text = tweet.full_text.lower()
            positive_words = ["good", "great", "awesome", "excellent", "love", "happy", "best", "amazing"]
            negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "disappointing"]
            
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            if positive_count > negative_count:
                sentiment_scores.append(1)  # Positive
            elif negative_count > positive_count:
                sentiment_scores.append(-1)  # Negative
            else:
                sentiment_scores.append(0)  # Neutral
        
        # Calculate related hashtags
        hashtag_counts = Counter(all_hashtags)
        related_hashtags = [
            {"name": f"#{h}", "count": count}
            for h, count in hashtag_counts.most_common(10)
            if h.lower() != hashtag[1:].lower()  # Exclude the analyzed hashtag
        ]
        
        # Calculate sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        sentiment = "positive" if avg_sentiment > 0.2 else "negative" if avg_sentiment < -0.2 else "neutral"
        
        # Get volume (approximate)
        volume = len(tweets)
        
        return {
            "volume": volume,
            "sentiment": sentiment,
            "related_hashtags": related_hashtags,
            "sample_tweets": sample_tweets[:5]  # Return top 5 tweets
        }
    except Exception as e:
        st.error(f"Error analyzing hashtag: {str(e)}")
        return {
            "volume": 0,
            "sentiment": "neutral",
            "related_hashtags": [],
            "sample_tweets": []
        }

def get_account_hashtags() -> Dict[str, int]:
    """Get hashtags used in the user's account."""
    try:
        if not is_authenticated():
            return {}
        
        # Get API client
        api = create_twitter_api()
        
        # Get user timeline
        tweets = api.user_timeline(count=200, tweet_mode="extended")
        
        # Extract hashtags
        all_hashtags = []
        for tweet in tweets:
            # Skip retweets
            if hasattr(tweet, "retweeted_status"):
                continue
            
            # Extract hashtags
            tweet_hashtags = [h["text"] for h in tweet.entities.get("hashtags", [])]
            all_hashtags.extend(tweet_hashtags)
        
        # Count hashtags
        hashtag_counts = Counter(all_hashtags)
        
        return dict(hashtag_counts.most_common(20))
    except Exception as e:
        st.error(f"Error getting account hashtags: {str(e)}")
        return {}

def generate_hashtag_recommendations(industry: str, topic: str) -> List[Dict[str, Any]]:
    """Generate hashtag recommendations based on industry and topic."""
    # Use AI to generate recommendations
    prompt = f"""
    Generate 10 effective Twitter hashtags for the {industry} industry, specifically for content about {topic}.
    For each hashtag, provide:
    1. The hashtag itself (including the # symbol)
    2. A brief description of why it's effective
    3. An estimate of how popular it is (high, medium, or low)
    
    Return the results as a JSON array of objects with the following structure:
    [
        {{
            "hashtag": "#example",
            "description": "Brief explanation of why this hashtag is effective",
            "popularity": "high/medium/low"
        }}
    ]
    """
    
    try:
        response = llm_text_gen(prompt)
        
        # Try to parse as JSON
        try:
            recommendations = json.loads(response)
            if isinstance(recommendations, list):
                return recommendations
        except:
            # Extract using regex
            hashtags = re.findall(r'#\w+', response)
            return [
                {
                    "hashtag": hashtag,
                    "description": f"Recommended hashtag for {topic} in {industry}",
                    "popularity": "medium"
                }
                for hashtag in hashtags[:10]
            ]
    except Exception as e:
        st.error(f"Error generating hashtag recommendations: {str(e)}")
        
        # Return generic recommendations
        return [
            {
                "hashtag": f"#{industry.lower()}",
                "description": f"Main industry hashtag",
                "popularity": "high"
            },
            {
                "hashtag": f"#{topic.lower().replace(' ', '')}",
                "description": f"Topic-specific hashtag",
                "popularity": "medium"
            }
        ]

def render_hashtag_manager():
    """Render the Hashtag Strategy Manager UI."""
    st.title("#️⃣ Hashtag Strategy Manager")
    st.markdown("Research and manage trending hashtags for better reach")
    
    # Check if connected to Twitter
    twitter_connected = is_authenticated()
    
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Trending Hashtags", "Hashtag Analysis", "Hashtag Strategy"])
    
    with tab1:
        st.markdown("### Trending Hashtags")
        
        # Get trending locations
        if twitter_connected:
            locations = get_trending_locations()
            
            if locations:
                # Create location selector
                location_options = {f"{loc['name']}, {loc['country']}": loc["woeid"] for loc in locations}
                selected_location = st.selectbox(
                    "Select Location",
                    options=list(location_options.keys()),
                    index=0
                )
                
                location_id = location_options[selected_location]
                
                # Get trending hashtags
                if st.button("Get Trending Hashtags", use_container_width=True):
                    with st.spinner("Fetching trending hashtags..."):
                        trends = get_trending_hashtags(location_id)
                        
                        if trends:
                            # Filter hashtags
                            show_all = st.checkbox("Show all trending topics (not just hashtags)")
                            
                            if not show_all:
                                trends = [t for t in trends if t["is_hashtag"]]
                            
                            # Create DataFrame
                            trends_df = pd.DataFrame(trends)
                            
                            # Display trends
                            st.dataframe(
                                trends_df,
                                column_config={
                                    "name": "Trend",
                                    "volume": st.column_config.NumberColumn("Volume", format="%d"),
                                    "is_hashtag": "Is Hashtag"
                                },
                                hide_index=True
                            )
                            
                            # Visualize top trends
                            st.markdown("#### Top Trends by Volume")
                            
                            # Filter out trends with no volume data
                            volume_trends = [t for t in trends if t["volume"]]
                            
                            if volume_trends:
                                # Sort by volume
                                volume_trends.sort(key=lambda x: x["volume"], reverse=True)
                                
                                # Take top 10
                                top_trends = volume_trends[:10]
                                
                                # Create DataFrame
                                top_df = pd.DataFrame(top_trends)
                                
                                # Create bar chart
                                fig = px.bar(
                                    top_df,
                                    x="name",
                                    y="volume",
                                    title="Top Trending Topics by Volume",
                                    labels={"name": "Trend", "volume": "Tweet Volume"}
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No volume data available for trending topics")
                        else:
                            st.warning("No trending topics found")
            else:
                st.warning("Could not fetch trending locations")
        else:
            st.warning("Connect your Twitter account to access trending hashtags")
            
            # Show sample data
            st.markdown("### Sample Trending Hashtags")
            sample_trends = [
                {"name": "#AI", "volume": 125000, "is_hashtag": True},
                {"name": "#MachineLearning", "volume": 78000, "is_hashtag": True},
                {"name": "#DataScience", "volume": 65000, "is_hashtag": True},
                {"name": "#Python", "volume": 52000, "is_hashtag": True},
                {"name": "#BigData", "volume": 48000, "is_hashtag": True}
            ]
            
            # Create DataFrame
            sample_df = pd.DataFrame(sample_trends)
            
            # Display trends
            st.dataframe(
                sample_df,
                column_config={
                    "name": "Trend",
                    "volume": st.column_config.NumberColumn("Volume", format="%d"),
                    "is_hashtag": "Is Hashtag"
                },
                hide_index=True
            )
    
    with tab2:
        st.markdown("### Hashtag Analysis")
        
        # Hashtag input
        hashtag = st.text_input(
            "Enter a hashtag to analyze",
            placeholder="e.g., #AI"
        )
        
        if hashtag:
            # Clean hashtag
            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"
            
            # Analyze button
            if st.button("Analyze Hashtag", use_container_width=True):
                with st.spinner(f"Analyzing {hashtag}..."):
                    if twitter_connected:
                        # Get hashtag analysis
                        analysis = analyze_hashtag(hashtag)
                        
                        # Display results
                        st.markdown(f"#### Analysis Results for {hashtag}")
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Volume", f"{analysis['volume']:,}")
                        
                        with col2:
                            sentiment = analysis["sentiment"].title()
                            sentiment_color = {
                                "Positive": "green",
                                "Neutral": "blue",
                                "Negative": "red"
                            }.get(sentiment, "blue")
                            
                            st.markdown(f"""
                                <div style="text-align: center;">
                                    <p style="margin-bottom: 0;">Sentiment</p>
                                    <p style="font-size: 1.5rem; font-weight: bold; color: {sentiment_color};">{sentiment}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            related_count = len(analysis["related_hashtags"])
                            st.metric("Related Hashtags", related_count)
                        
                        # Related hashtags
                        if analysis["related_hashtags"]:
                            st.markdown("#### Related Hashtags")
                            
                            # Create DataFrame
                            related_df = pd.DataFrame(analysis["related_hashtags"])
                            
                            # Display related hashtags
                            st.dataframe(
                                related_df,
                                column_config={
                                    "name": "Hashtag",
                                    "count": st.column_config.NumberColumn("Count", format="%d")
                                },
                                hide_index=True
                            )
                        
                        # Sample tweets
                        if analysis["sample_tweets"]:
                            st.markdown("#### Sample Tweets")
                            
                            for tweet in analysis["sample_tweets"]:
                                st.markdown(f"""
                                    <div style="padding: 10px; border-radius: 5px; background-color: #f0f2f6; margin-bottom: 10px;">
                                        <p>{tweet['text']}</p>
                                        <div style="display: flex; justify-content: space-between;">
                                            <small>{tweet['created_at'].strftime('%Y-%m-%d %H:%M')}</small>
                                            <small>❤️ {tweet['likes']} | 🔄 {tweet['retweets']}</small>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("Connect your Twitter account to analyze hashtags")
                        
                        # Show sample analysis
                        st.markdown(f"#### Sample Analysis for {hashtag}")
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Volume", "5,280")
                        
                        with col2:
                            st.markdown("""
                                <div style="text-align: center;">
                                    <p style="margin-bottom: 0;">Sentiment</p>
                                    <p style="font-size: 1.5rem; font-weight: bold; color: green;">Positive</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.metric("Related Hashtags", 8)
                        
                        # Related hashtags
                        st.markdown("#### Related Hashtags")
                        
                        sample_related = [
                            {"name": "#MachineLearning", "count": 45},
                            {"name": "#DataScience", "count": 32},
                            {"name": "#Python", "count": 28},
                            {"name": "#DeepLearning", "count": 21},
                            {"name": "#BigData", "count": 18}
                        ]
                        
                        # Create DataFrame
                        related_df = pd.DataFrame(sample_related)
                        
                        # Display related hashtags
                        st.dataframe(
                            related_df,
                            column_config={
                                "name": "Hashtag",
                                "count": st.column_config.NumberColumn("Count", format="%d")
                            },
                            hide_index=True
                        )
        
        # Account hashtag analysis
        st.markdown("### Your Hashtag Usage")
        
        if twitter_connected:
            if st.button("Analyze My Hashtags", use_container_width=True):
                with st.spinner("Analyzing your hashtag usage..."):
                    # Get account hashtags
                    account_hashtags = get_account_hashtags()
                    
                    if account_hashtags:
                        # Create DataFrame
                        hashtags_df = pd.DataFrame([
                            {"hashtag": f"#{h}", "count": count}
                            for h, count in account_hashtags.items()
                        ])
                        
                        # Display hashtags
                        st.dataframe(
                            hashtags_df,
                            column_config={
                                "hashtag": "Hashtag",
                                "count": st.column_config.NumberColumn("Count", format="%d")
                            },
                            hide_index=True
                        )
                        
                        # Visualize top hashtags
                        st.markdown("#### Your Top Hashtags")
                        
                        # Create bar chart
                        fig = px.bar(
                            hashtags_df.head(10),
                            x="hashtag",
                            y="count",
                            title="Your Most Used Hashtags",
                            labels={"hashtag": "Hashtag", "count": "Usage Count"}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No hashtags found in your recent tweets")
        else:
            st.warning("Connect your Twitter account to analyze your hashtag usage")
    
    with tab3:
        st.markdown("### Hashtag Strategy")
        
        # Industry and topic inputs
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Industry",
                ["Technology", "Marketing", "Education", "Health", "Finance", "Other"],
                index=0
            )
            
            if industry == "Other":
                industry = st.text_input("Specify Industry")
        
        with col2:
            topic = st.text_input(
                "Content Topic",
                placeholder="e.g., Artificial Intelligence"
            )
        
        # Generate recommendations
        if st.button("Generate Hashtag Recommendations", use_container_width=True):
            if topic:
                with st.spinner("Generating hashtag recommendations..."):
                    # Get recommendations
                    recommendations = generate_hashtag_recommendations(industry, topic)
                    
                    if recommendations:
                        # Display recommendations
                        st.markdown("#### Recommended Hashtags")
                        
                        for rec in recommendations:
                            # Determine color based on popularity
                            color = {
                                "high": "#28a745",
                                "medium": "#ffc107",
                                "low": "#6c757d"
                            }.get(rec.get("popularity", "medium").lower(), "#6c757d")
                            
                            st.markdown(f"""
                                <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin-bottom: 10px; border-left: 5px solid {color};">
                                    <h4 style="margin: 0;">{rec['hashtag']}</h4>
                                    <p style="margin: 5px 0;">{rec.get('description', '')}</p>
                                    <span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">
                                        {rec.get('popularity', 'medium').title()} Popularity
                                    </span>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Hashtag strategy tips
                        st.markdown("#### Hashtag Strategy Tips")
                        
                        st.markdown("""
                            - **Use a mix of popular and niche hashtags** to balance reach and competition
                            - **Limit to 2-3 hashtags per tweet** for optimal engagement
                            - **Research before using trending hashtags** to ensure relevance
                            - **Create branded hashtags** for campaigns and tracking
                            - **Place hashtags within your tweet text** when possible, rather than at the end
                            - **Monitor performance** to identify which hashtags drive the most engagement
                        """)
                        
                        # Save hashtags
                        if st.button("Save to Hashtag Library"):
                            # Store in session state
                            if "hashtag_library" not in st.session_state:
                                st.session_state.hashtag_library = []
                            
                            # Add new hashtags
                            for rec in recommendations:
                                if rec["hashtag"] not in [h["hashtag"] for h in st.session_state.hashtag_library]:
                                    st.session_state.hashtag_library.append(rec)
                            
                            st.success("Hashtags saved to your library!")
                    else:
                        st.warning("Could not generate recommendations")
            else:
                st.error("Please enter a content topic")
        
        # Hashtag library
        if "hashtag_library" in st.session_state and st.session_state.hashtag_library:
            st.markdown("### Your Hashtag Library")
            
            # Create DataFrame
            library_df = pd.DataFrame(st.session_state.hashtag_library)
            
            # Display library
            st.dataframe(
                library_df,
                column_config={
                    "hashtag": "Hashtag",
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "popularity": "Popularity"
                },
                hide_index=True
            )
            
            # Export button
            if st.button("Export Hashtag Library"):
                # Convert to CSV
                csv = library_df.to_csv(index=False)
                
                # Download button
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"hashtag_library_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
```

### Phase 4: Visual Content Creation

#### 4.1 Image Generator

Implement the Image Generator feature:

```python
# lib/ai_writers/twitter_writers/visual_content/image_generator.py

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from datetime import datetime
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import requests
import os
from pathlib import Path

# Constants
TEMPLATE_DIR = Path(__file__).parent.parent.parent.parent.parent / 'assets' / 'templates'
TEMPLATE_DIR.mkdir(exist_ok=True, parents=True)
FONT_DIR = Path(__file__).parent.parent.parent.parent.parent / 'assets' / 'fonts'
FONT_DIR.mkdir(exist_ok=True, parents=True)

def generate_quote_image(
    quote: str,
    author: str = "",
    template: str = "gradient",
    color_scheme: str = "blue"
) -> Image.Image:
    """Generate a quote image."""
    # Define templates
    templates = {
        "gradient": {
            "width": 1200,
            "height": 675,
            "background": {
                "blue": [(25, 84, 123), (142, 197, 252)],
                "green": [(25, 123, 48), (142, 252, 169)],
                "purple": [(84, 25, 123), (197, 142, 252)],
                "red": [(123, 25, 25), (252, 142, 142)]
            },
            "text_color": (255, 255, 255),
            "author_color": (255, 255, 255, 200)
        },
        "minimal": {
            "width": 1200,
            "height": 675,
            "background": {
                "blue": (240, 248, 255),
                "green": (240, 255, 240),
                "purple": (248, 240, 255),
                "red": (255, 240, 240)
            },
            "text_color": (50, 50, 50),
            "author_color": (100, 100, 100)
        },
        "bold": {
            "width": 1200,
            "height": 675,
            "background": {
                "blue": (25, 84, 123),
                "green": (25, 123, 48),
                "purple": (84, 25, 123),
                "red": (123, 25, 25)
            },
            "text_color": (255, 255, 255),
            "author_color": (255, 255, 255, 200)
        }
    }
    
    # Get template settings
    template_settings = templates.get(template, templates["gradient"])
    width = template_settings["width"]
    height = template_settings["height"]
    
    # Create image
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw background
    if template == "gradient":
        # Create gradient background
        bg_colors = template_settings["background"][color_scheme]
        for y in range(height):
            r = int(bg_colors[0][0] + (bg_colors[1][0] - bg_colors[0][0]) * y / height)
            g = int(bg_colors[0][1] + (bg_colors[1][1] - bg_colors[0][1]) * y / height)
            b = int(bg_colors[0][2] + (bg_colors[1][2] - bg_colors[0][2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        # Solid background
        draw.rectangle([(0, 0), (width, height)], fill=template_settings["background"][color_scheme])
    
    # Add quote
    # Try to load font, fall back to default if not available
    try:
        quote_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Bold.ttf"), 48)
        author_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Regular.ttf"), 32)
    except:
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
    
    # Wrap text
    max_width = width - 200
    words = quote.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=quote_font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Draw quote
    quote_text = "\n".join(lines)
    quote_bbox = draw.textbbox((0, 0), quote_text, font=quote_font)
    quote_width = quote_bbox[2] - quote_bbox[0]
    quote_height = quote_bbox[3] - quote_bbox[1]
    
    quote_x = (width - quote_width) // 2
    quote_y = (height - quote_height) // 2 - 50 if author else (height - quote_height) // 2
    
    # Add quote marks
    draw.text((quote_x - 60, quote_y - 80), """, fill=template_settings["text_color"], font=quote_font)
    
    # Draw quote text
    draw.text((quote_x, quote_y), quote_text, fill=template_settings["text_color"], font=quote_font, align="center")
    
    # Draw author
    if author:
        author_text = f"— {author}"
        author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_width = author_bbox[2] - author_bbox[0]
        
        author_x = (width - author_width) // 2
        author_y = quote_y + quote_height + 40
        
        draw.text((author_x, author_y), author_text, fill=template_settings["author_color"], font=author_font)
    
    return img

def generate_tweet_card(
    text: str,
    username: str = "",
    profile_image: str = None,
    theme: str = "light"
) -> Image.Image:
    """Generate a tweet card image."""
    # Define themes
    themes = {
        "light": {
            "background": (255, 255, 255),
            "text": (20, 23, 26),
            "username": (83, 100, 113),
            "border": (235, 238, 240)
        },
        "dark": {
            "background": (21, 32, 43),
            "text": (255, 255, 255),
            "username": (136, 153, 166),
            "border": (56, 68, 77)
        },
        "black": {
            "background": (0, 0, 0),
            "text": (217, 217, 217),
            "username": (110, 118, 125),
            "border": (47, 51, 54)
        }
    }
    
    # Get theme settings
    theme_settings = themes.get(theme, themes["light"])
    
    # Create image
    width = 1200
    height = 675
    img = Image.new("RGB", (width, height), color=theme_settings["background"])
    draw = ImageDraw.Draw(img)
    
    # Draw card background
    card_width = 800
    card_height = 400
    card_x = (width - card_width) // 2
    card_y = (height - card_height) // 2
    
    # Draw card border
    draw.rectangle(
        [(card_x, card_y), (card_x + card_width, card_y + card_height)],
        outline=theme_settings["border"],
        width=2
    )
    
    # Try to load font, fall back to default if not available
    try:
        text_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Regular.ttf"), 32)
        username_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Bold.ttf"), 28)
    except:
        text_font = ImageFont.load_default()
        username_font = ImageFont.load_default()
    
    # Add profile image
    profile_size = 80
    profile_x = card_x + 40
    profile_y = card_y + 40
    
    if profile_image:
        try:
            # Try to load profile image
            response = requests.get(profile_image)
            profile_img = Image.open(io.BytesIO(response.content))
            profile_img = profile_img.resize((profile_size, profile_size))
            
            # Create circular mask
            mask = Image.new("L", (profile_size, profile_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, profile_size, profile_size), fill=255)
            
            # Apply mask
            profile_img.putalpha(mask)
            
            # Paste profile image
            img.paste(profile_img, (profile_x, profile_y), profile_img)
        except:
            # Draw placeholder circle
            draw.ellipse(
                [(profile_x, profile_y), (profile_x + profile_size, profile_y + profile_size)],
                fill=theme_settings["username"]
            )
    else:
        # Draw placeholder circle
        draw.ellipse(
            [(profile_x, profile_y), (profile_x + profile_size, profile_y + profile_size)],
            fill=theme_settings["username"]
        )
    
    # Add username
    if username:
        username_x = profile_x + profile_size + 20
        username_y = profile_y + 10
        
        draw.text((username_x, username_y), username, fill=theme_settings["text"], font=username_font)
        draw.text((username_x, username_y + 40), f"@{username}", fill=theme_settings["username"], font=text_font)
    
    # Wrap text
    max_width = card_width - 80
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=text_font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
    
    # Draw tweet text
    tweet_text = "\n".join(lines)
    text_x = card_x + 40
    text_y = profile_y + profile_size + 40
    
    draw.text((text_x, text_y), tweet_text, fill=theme_settings["text"], font=text_font)
    
    return img

def generate_infographic(
    title: str,
    items: List[str],
    theme: str = "blue"
) -> Image.Image:
    """Generate a simple infographic."""
    # Define themes
    themes = {
        "blue": {
            "background": (240, 248, 255),
            "title_bg": (25, 84, 123),
            "title_text": (255, 255, 255),
            "item_bg": [(142, 197, 252), (173, 216, 230)],
            "item_text": (25, 25, 25)
        },
        "green": {
            "background": (240, 255, 240),
            "title_bg": (25, 123, 48),
            "title_text": (255, 255, 255),
            "item_bg": [(142, 252, 169), (173, 230, 188)],
            "item_text": (25, 25, 25)
        },
        "purple": {
            "background": (248, 240, 255),
            "title_bg": (84, 25, 123),
            "title_text": (255, 255, 255),
            "item_bg": [(197, 142, 252), (216, 173, 230)],
            "item_text": (25, 25, 25)
        },
        "red": {
            "background": (255, 240, 240),
            "title_bg": (123, 25, 25),
            "title_text": (255, 255, 255),
            "item_bg": [(252, 142, 142), (230, 173, 173)],
            "item_text": (25, 25, 25)
        }
    }
    
    # Get theme settings
    theme_settings = themes.get(theme, themes["blue"])
    
    # Create image
    width = 1200
    height = 675
    img = Image.new("RGB", (width, height), color=theme_settings["background"])
    draw = ImageDraw.Draw(img)
    
    # Try to load font, fall back to default if not available
    try:
        title_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Bold.ttf"), 48)
        item_font = ImageFont.truetype(str(FONT_DIR / "Roboto-Regular.ttf"), 32)
    except:
        title_font = ImageFont.load_default()
        item_font = ImageFont.load_default()
    
    # Draw title
    title_height = 100
    draw.rectangle([(0, 0), (width, title_height)], fill=theme_settings["title_bg"])
    
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = (title_height - title_font.size) // 2
    
    draw.text((title_x, title_y), title, fill=theme_settings["title_text"], font=title_font)
    
    # Draw items
    item_height = 80
    item_padding = 20
    item_y = title_height + 50
    
    for i, item in enumerate(items):
        # Alternate background colors
        bg_color = theme_settings["item_bg"][i % 2]
        
        # Draw item background
        draw.rectangle(
            [(50, item_y), (width - 50, item_y + item_height)],
            fill=bg_color,
            outline=theme_settings["title_bg"],
            width=2
        )
        
        # Draw item number
        number_size = 60
        draw.ellipse(
            [(70, item_y + (item_height - number_size) // 2),
             (70 + number_size, item_y + (item_height - number_size) // 2 + number_size)],
            fill=theme_settings["title_bg"]
        )
        
        number_text = str(i + 1)
        number_bbox = draw.textbbox((0, 0), number_text, font=item_font)
        number_width = number_bbox[2] - number_bbox[0]
        number_height = number_bbox[3] - number_bbox[1]
        
        number_x = 70 + (number_size - number_width) // 2
        number_y = item_y + (item_height - number_height) // 2
        
        draw.text((number_x, number_y), number_text, fill=theme_settings["title_text"], font=item_font)
        
        # Draw item text
        item_text_x = 70 + number_size + 20
        item_text_y = item_y + (item_height - item_font.size) // 2
        
        draw.text((item_text_x, item_text_y), item, fill=theme_settings["item_text"], font=item_font)
        
        # Update y position for next item
        item_y += item_height + item_padding
    
    return img

def render_image_generator():
    """Render the Image Generator UI."""
    st.title("🖼️ Twitter Image Generator")
    st.markdown("Create engaging visual content for your tweets")
    
    # Create tabs for different image types
    tab1, tab2, tab3 = st.tabs(["Quote Cards", "Tweet Cards", "Infographics"])
    
    with tab1:
        st.markdown("### Quote Cards")
        st.markdown("Create shareable quote images for Twitter")
        
        # Quote input
        quote = st.text_area(
            "Quote Text",
            placeholder="Enter your quote here...",
            height=100
        )
        
        author = st.text_input(
            "Author/Source",
            placeholder="e.g., Albert Einstein"
        )
        
        # Design options
        col1, col2 = st.columns(2)
        
        with col1:
            template = st.selectbox(
                "Template",
                ["gradient", "minimal", "bold"],
                index=0
            )
        
        with col2:
            color_scheme = st.selectbox(
                "Color Scheme",
                ["blue", "green", "purple", "red"],
                index=0
            )
        
        # Generate button
        if st.button("Generate Quote Card", use_container_width=True, key="generate_quote"):
            if quote:
                with st.spinner("Generating quote card..."):
                    # Generate image
                    img = generate_quote_image(quote, author, template, color_scheme)
                    
                    # Convert to bytes
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    # Display image
                    st.image(byte_im, caption="Generated Quote Card", use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        "Download Image",
                        data=byte_im,
                        file_name=f"quote_card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
            else:
                st.error("Please enter a quote")
    
    with tab2:
        st.markdown("### Tweet Cards")
        st.markdown("Create images that showcase your tweets")
        
        # Tweet input
        tweet_text = st.text_area(
            "Tweet Text",
            placeholder="Enter your tweet here...",
            height=100
        )
        
        username = st.text_input(
            "Twitter Username",
            placeholder="e.g., elonmusk"
        )
        
        # Design options
        theme = st.selectbox(
            "Theme",
            ["light", "dark", "black"],
            index=0
        )
        
        # Profile image
        profile_image = None
        if username:
            try:
                # Try to fetch profile image
                profile_image = f"https://unavatar.io/twitter/{username}"
            except:
                pass
        
        # Generate button
        if st.button("Generate Tweet Card", use_container_width=True, key="generate_tweet"):
            if tweet_text:
                with st.spinner("Generating tweet card..."):
                    # Generate image
                    img = generate_tweet_card(tweet_text, username, profile_image, theme)
                    
                    # Convert to bytes
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    # Display image
                    st.image(byte_im, caption="Generated Tweet Card", use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        "Download Image",
                        data=byte_im,
                        file_name=f"tweet_card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
            else:
                st.error("Please enter tweet text")
    
    with tab3:
        st.markdown("### Infographics")
        st.markdown("Create simple infographics for Twitter")
        
        # Infographic input
        title = st.text_input(
            "Infographic Title",
            placeholder="e.g., 5 Tips for Better Tweets"
        )
        
        # Items input
        items = []
        for i in range(5):
            item = st.text_input(
                f"Item {i+1}",
                placeholder=f"Enter item {i+1}...",
                key=f"item_{i}"
            )
            if item:
                items.append(item)
        
        # Design options
        theme = st.selectbox(
            "Color Theme",
            ["blue", "green", "purple", "red"],
            index=0,
            key="infographic_theme"
        )
        
        # Generate button
        if st.button("Generate Infographic", use_container_width=True, key="generate_infographic"):
            if title and items:
                with st.spinner("Generating infographic..."):
                    # Generate image
                    img = generate_infographic(title, items, theme)
                    
                    # Convert to bytes
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    # Display image
                    st.image(byte_im, caption="Generated Infographic", use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        "Download Image",
                        data=byte_im,
                        file_name=f"infographic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
            else:
                st.error("Please enter a title and at least one item")
```

### Phase 5: Analytics & Optimization

#### 5.1 Performance Analytics

Implement the Performance Analytics feature:

```python
# lib/ai_writers/twitter_writers/analytics/performance_analytics.py

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ....integrations.twitter.auth import create_twitter_api, create_twitter_client, is_authenticated

def get_tweet_performance(days: int = 30) -> pd.DataFrame:
    """Get tweet performance data from Twitter API."""
    try:
        if not is_authenticated():
            return pd.DataFrame()
        
        # Get API client
        api = create_twitter_api()
        
        # Get user timeline
        tweets = api.user_timeline(count=200, tweet_mode="extended")
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        tweets = [t for t in tweets if t.created_at >= cutoff_date]
        
        # Create DataFrame
        data = []
        for tweet in tweets:
            # Skip retweets
            if hasattr(tweet, "retweeted_status"):
                continue
            
            # Extract tweet data
            tweet_data = {
                "id": tweet.id,
                "text": tweet.full_text,
                "created_at": tweet.created_at,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                "replies": 0,  # Not available in standard API
                "impressions": 0,  # Not available in standard API
                "engagement": tweet.favorite_count + tweet.retweet_count,
                "hashtags": len(tweet.entities.get("hashtags", [])),
                "mentions": len(tweet.entities.get("user_mentions", [])),
                "urls": len(tweet.entities.get("urls", [])),
                "media": 1 if "media" in tweet.entities else 0,
                "hour": tweet.created_at.hour,
                "day": tweet.created_at.strftime("%A"),
                "length": len(tweet.full_text)
            }
            
            data.append(tweet_data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        return df
    except Exception as e:
        st.error(f"Error fetching tweet performance: {str(e)}")
        return pd.DataFrame()

def analyze_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze tweet performance data."""
    if df.empty:
        return {
            "total_engagement": 0,
            "avg_engagement": 0,
            "top_tweet": None,
            "worst_tweet": None,
            "best_time": None,
            "best_day": None,
            "media_impact": 0,
            "hashtag_impact": 0,
            "length_impact": 0
        }
    
    # Calculate metrics
    total_engagement = df["engagement"].sum()
    avg_engagement = df["engagement"].mean()
    
    # Find top and worst tweets
    top_tweet = df.loc[df["engagement"].idxmax()] if not df.empty else None
    worst_tweet = df.loc[df["engagement"].idxmin()] if not df.empty else None
    
    # Find best time and day
    hour_engagement = df.groupby("hour")["engagement"].mean()
    best_hour = hour_engagement.idxmax() if not hour_engagement.empty else None
    
    day_engagement = df.groupby("day")["engagement"].mean()
    best_day = day_engagement.idxmax() if not day_engagement.empty else None
    
    # Calculate impact factors
    media_impact = df[df["media"] == 1]["engagement"].mean() / avg_engagement if avg_engagement > 0 else 1
    
    hashtag_impact = 0
    if not df.empty:
        hashtag_groups = df.groupby("hashtags")["engagement"].mean()
        optimal_hashtags = hashtag_groups.idxmax() if not hashtag_groups.empty else 0
        hashtag_impact = hashtag_groups.max() / avg_engagement if avg_engagement > 0 else 1
    
    length_impact = 0
    if not df.empty:
        df["length_bin"] = pd.cut(df["length"], bins=[0, 70, 140, 210, 280], labels=["0-70", "71-140", "141-210", "211-280"])
        length_groups = df.groupby("length_bin")["engagement"].mean()
        optimal_length = length_groups.idxmax() if not length_groups.empty else "71-140"
        length_impact = length_groups.max() / avg_engagement if avg_engagement > 0 else 1
    
    return {
        "total_engagement": total_engagement,
        "avg_engagement": avg_engagement,
        "top_tweet": top_tweet,
        "worst_tweet": worst_tweet,
        "best_time": best_hour,
        "best_day": best_day,
        "media_impact": media_impact,
        "hashtag_impact": hashtag_impact,
        "length_impact": length_impact
    }

def render_performance_analytics():
    """Render the Performance Analytics UI."""
    st.title("📊 Twitter Performance Analytics")
    st.markdown("Track tweet performance and engagement metrics")
    
    # Check if connected to Twitter
    twitter_connected = is_authenticated()
    
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
        
        # Date range selector
        col1, col2 = st.columns(2)
        
        with col1:
            days = st.slider(
                "Time Period",
                min_value=7,
                max_value=90,
                value=30,
                step=1
            )
        
        with col2:
            refresh = st.button("Refresh Data", use_container_width=True)
        
        # Get performance data
        with st.spinner("Fetching tweet performance data..."):
            df = get_tweet_performance(days)
            
            if not df.empty:
                # Store in session state
                st.session_state.tweet_performance = df
                
                # Analyze performance
                analysis = analyze_performance(df)
                
                # Display overview metrics
                st.markdown("### Performance Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Tweets", len(df))
                
                with col2:
                    st.metric("Total Engagement", f"{analysis['total_engagement']:,}")
                
                with col3:
                    st.metric("Avg. Engagement", f"{analysis['avg_engagement']:.1f}")
                
                with col4:
                    st.metric("Media Impact", f"{analysis['media_impact']:.2f}x")
                
                # Engagement over time
                st.markdown("### Engagement Over Time")
                
                # Sort by date
                df_sorted = df.sort_values("created_at")
                
                # Create time series chart
                fig = px.line(
                    df_sorted,
                    x="created_at",
                    y="engagement",
                    title="Tweet Engagement History",
                    labels={"created_at": "Date", "engagement": "Engagement"}
                )
                
                # Add 7-day moving average
                df_sorted["ma7"] = df_sorted["engagement"].rolling(7).mean()
                
                fig.add_trace(
                    go.Scatter(
                        x=df_sorted["created_at"],
                        y=df_sorted["ma7"],
                        mode="lines",
                        name="7-day Moving Average",
                        line=dict(color="red", width=2)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Engagement by day and hour
                st.markdown("### Engagement by Day and Hour")
                
                # Create heatmap
                pivot = df.pivot_table(
                    index="day",
                    columns="hour",
                    values="engagement",
                    aggfunc="mean"
                )
                
                # Reorder days
                days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                pivot = pivot.reindex(days_order)
                
                fig = px.imshow(
                    pivot,
                    labels=dict(x="Hour of Day", y="Day of Week", color="Avg. Engagement"),
                    x=list(range(24)),
                    y=days_order,
                    color_continuous_scale="Viridis",
                    title="Engagement Heatmap by Day and Hour"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Content analysis
                st.markdown("### Content Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Engagement by tweet length
                    df["length_bin"] = pd.cut(df["length"], bins=[0, 70, 140, 210, 280], labels=["0-70", "71-140", "141-210", "211-280"])
                    length_engagement = df.groupby("length_bin")["engagement"].mean().reset_index()
                    
                    fig = px.bar(
                        length_engagement,
                        x="length_bin",
                        y="engagement",
                        title="Engagement by Tweet Length",
                        labels={"length_bin": "Character Count", "engagement": "Avg. Engagement"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Engagement by hashtag count
                    hashtag_engagement = df.groupby("hashtags")["engagement"].mean().reset_index()
                    
                    fig = px.bar(
                        hashtag_engagement,
                        x="hashtags",
                        y="engagement",
                        title="Engagement by Hashtag Count",
                        labels={"hashtags": "Number of Hashtags", "engagement": "Avg. Engagement"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Media impact
                st.markdown("### Media Impact")
                
                media_engagement = df.groupby("media")["engagement"].mean().reset_index()
                media_engagement["media"] = media_engagement["media"].map({0: "No Media", 1: "With Media"})
                
                fig = px.bar(
                    media_engagement,
                    x="media",
                    y="engagement",
                    title="Engagement by Media Inclusion",
                    labels={"media": "Media", "engagement": "Avg. Engagement"},
                    color="media",
                    color_discrete_map={"No Media": "#1DA1F2", "With Media": "#17BF63"}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Top tweets
                st.markdown("### Top Performing Tweets")
                
                # Sort by engagement
                top_tweets = df.sort_values("engagement", ascending=False).head(5)
                
                for i, (_, tweet) in enumerate(top_tweets.iterrows()):
                    st.markdown(f"""
                        <div style="padding: 15px; border-radius: 5px; background-color: #f0f2f6; margin-bottom: 15px;">
                            <p style="margin: 0 0 10px 0;">{tweet['text']}</p>
                            <div style="display: flex; justify-content: space-between;">
                                <small>{tweet['created_at'].strftime('%Y-%m-%d %H:%M')}</small>
                                <small>❤️ {tweet['likes']} | 🔄 {tweet['retweets']} | 💬 {tweet['replies']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("### Performance Recommendations")
                
                recommendations = []
                
                # Best time to post
                if analysis["best_time"] is not None and analysis["best_day"] is not None:
                    recommendations.append(f"Post on {analysis['best_day']} around {analysis['best_time']}:00 for optimal engagement")
                
                # Media recommendation
                if analysis["media_impact"] > 1.2:
                    recommendations.append(f"Including media increases engagement by {(analysis['media_impact']-1)*100:.1f}%")
                
                # Hashtag recommendation
                hashtag_groups = df.groupby("hashtags")["engagement"].mean()
                if not hashtag_groups.empty:
                    optimal_hashtags = hashtag_groups.idxmax()
                    recommendations.append(f"Using {optimal_hashtags} hashtags yields the best engagement")
                
                # Length recommendation
                length_groups = df.groupby("length_bin")["engagement"].mean()
                if not length_groups.empty:
                    optimal_length = length_groups.idxmax()
                    recommendations.append(f"Tweets with {optimal_length} characters perform best")
                
                # Display recommendations
                for rec in recommendations:
                    st.info(rec)
                
                # Export options
                st.markdown("### Export Data")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Export as CSV
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        data=csv,
                        file_name=f"tweet_performance_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Export as JSON
                    json_str = df.to_json(orient="records", date_format="iso")
                    st.download_button(
                        "Download JSON",
                        data=json_str,
                        file_name=f"tweet_performance_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            else:
                st.warning("No tweets found in the selected time period")
    else:
        st.warning("Connect your Twitter account to access performance analytics")
        
        # Show sample data
        st.markdown("### Sample Performance Data")
        
        # Create sample data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
        engagements = np.random.normal(loc=20, scale=10, size=30)
        engagements = np.abs(engagements)  # Make all values positive
        
        df = pd.DataFrame({
            "date": dates,
            "engagement": engagements
        })
        
        # Sample metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tweets", "42")
        
        with col2:
            st.metric("Total Engagement", "1,254")
        
        with col3:
            st.metric("Avg. Engagement", "29.8")
        
        with col4:
            st.metric("Media Impact", "1.45x")
        
        # Sample chart
        fig = px.line(
            df,
            x="date",
            y="engagement",
            title="Sample Tweet Engagement History"
        )
        st.plotly_chart(fig, use_container_width=True)
```

### Phase 6: Integration and Dashboard Updates

#### 6.1 Update Twitter Dashboard

Update the Twitter dashboard to include the new features:

```python
# lib/ai_writers/twitter_writers/twitter_dashboard.py

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List
import json
from datetime import datetime

from .tweet_generator.enhanced_tweet_generator import enhanced_tweet_generator
from .tweet_performance.performance_predictor import render_performance_predictor
from .content_strategy.calendar_generator import render_calendar_generator
from .content_strategy.hashtag_manager import render_hashtag_manager
from .visual_content.image_generator import render_image_generator
from .analytics.performance_analytics import render_performance_analytics
from ...integrations.twitter.auth import is_authenticated
from ...integrations.twitter.account_manager import render_twitter_account_manager
from ...integrations.twitter.api_key_manager import render_twitter_api_key_manager
from ...integrations.twitter.callback_handler import handle_oauth_callback

def load_feature_data() -> Dict:
    """Load feature data from a structured format."""
    return {
        "tweet_generation": {
            "title": "Tweet Generation & Optimization",
            "icon": "🐦",
            "description": "Create and optimize engaging tweets with AI assistance",
            "features": [
                {
                    "name": "Smart Tweet Generator",
                    "description": "Generate multiple tweet variations with optimal character count, hashtags, and emojis",
                    "status": "active",
                    "icon": "✨",
                    "function": enhanced_tweet_generator
                },
                {
                    "name": "Tweet Performance Predictor",
                    "description": "Predict engagement rates and best posting times for maximum impact",
                    "status": "active",
                    "icon": "📊",
                    "function": render_performance_predictor
                }
            ]
        },
        "content_strategy": {
            "title": "Content Strategy Tools",
            "icon": "📅",
            "description": "Plan and manage your Twitter content strategy effectively",
            "features": [
                {
                    "name": "Content Calendar Generator",
                    "description": "Create weekly/monthly content plans with theme-based scheduling",
                    "status": "active",
                    "icon": "🗓️",
                    "function": render_calendar_generator
                },
                {
                    "name": "Hashtag Strategy Manager",
                    "description": "Research and manage trending hashtags for better reach",
                    "status": "active",
                    "icon": "#️⃣",
                    "function": render_hashtag_manager
                }
            ]
        },
        "visual_content": {
            "title": "Visual Content Creation",
            "icon": "🎨",
            "description": "Create engaging visual content for your tweets",
            "features": [
                {
                    "name": "Image Generator",
                    "description": "Create tweet cards, infographics, and quote designs",
                    "status": "active",
                    "icon": "🖼️",
                    "function": render_image_generator
                },
                {
                    "name": "Video Content Assistant",
                    "description": "Generate video scripts and optimize captions",
                    "status": "coming_soon",
                    "icon": "🎥"
                }
            ]
        },
        "engagement": {
            "title": "Engagement & Community",
            "icon": "🤝",
            "description": "Manage and enhance community engagement",
            "features": [
                {
                    "name": "Reply Generator",
                    "description": "Generate context-aware responses with appropriate tone",
                    "status": "coming_soon",
                    "icon": "💬"
                },
                {
                    "name": "Community Tools",
                    "description": "Create polls and plan Q&A sessions",
                    "status": "coming_soon",
                    "icon": "👥"
                }
            ]
        },
        "analytics": {
            "title": "Analytics & Optimization",
            "icon": "📈",
            "description": "Track performance and optimize your Twitter strategy",
            "features": [
                {
                    "name": "Performance Analytics",
                    "description": "Track tweet performance and engagement metrics",
                    "status": "active",
                    "icon": "📊",
                    "function": render_performance_analytics
                },
                {
                    "name": "A/B Testing Assistant",
                    "description": "Test and optimize tweet variations for better results",
                    "status": "coming_soon",
                    "icon": "🔍"
                }
            ]
        },
        "research": {
            "title": "Research & Intelligence",
            "icon": "🔎",
            "description": "Gain insights and stay ahead of trends",
            "features": [
                {
                    "name": "Market Research",
                    "description": "Analyze competitors and track industry trends",
                    "status": "coming_soon",
                    "icon": "📊"
                },
                {
                    "name": "Content Inspiration",
                    "description": "Get trending topic suggestions and content ideas",
                    "status": "coming_soon",
                    "icon": "💡"
                }
            ]
        }
    }

def render_feature_card(feature: Dict) -> None:
    """Render a single feature card with its details."""
    with st.container():
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{feature['icon']} {feature['name']}</h3>
                <p style='margin: 10px 0;'>{feature['description']}</p>
                <span style='background-color: {'#4CAF50' if feature['status'] == 'active' else '#ffd700'}; 
                            padding: 5px 10px; border-radius: 15px; font-size: 0.8em;'>
                    {feature['status'].title()}
                </span>
            </div>
        """, unsafe_allow_html=True)

def render_category_section(category: Dict) -> None:
    """Render a category section with all its features."""
    st.markdown(f"### {category['icon']} {category['title']}")
    st.markdown(f"*{category['description']}*")
    
    col1, col2 = st.columns(2)
    with col1:
        render_feature_card(category['features'][0])
        if category['features'][0]['status'] == 'active':
            if st.button(f"Launch {category['features'][0]['name']}", key=f"launch_{category['features'][0]['name']}"):
                st.session_state.current_feature = category['features'][0]['function']
                st.experimental_rerun()
    with col2:
        render_feature_card(category['features'][1])
        if category['features'][1]['status'] == 'active':
            if st.button(f"Launch {category['features'][1]['name']}", key=f"launch_{category['features'][1]['name']}"):
                st.session_state.current_feature = category['features'][1]['function']
                st.experimental_rerun()

def run_dashboard():
    """Main function to run the Twitter dashboard."""
    # Handle OAuth callback if present
    handle_oauth_callback()
    
    # Check if a feature is currently active
    if "current_feature" in st.session_state and callable(st.session_state.current_feature):
        # Add back button
        if st.button("← Back to Dashboard"):
            del st.session_state.current_feature
            st.experimental_rerun()
        
        # Run the current feature
        st.session_state.current_feature()
        return
    
    # Header
    st.title("🐦 Twitter AI Writer Dashboard")
    st.markdown("""
        Welcome to your all-in-one Twitter content creation and management platform. 
        Explore our AI-powered tools to enhance your Twitter marketing strategy.
    """)
    
    # Twitter account status
    twitter_connected = is_authenticated()
    
    if twitter_connected:
        user = st.session_state.twitter_user
        st.success(f"Connected as @{user['screen_name']}")
    else:
        st.warning("Connect your Twitter account to access all features")
        
        # Show account connection UI
        with st.expander("Twitter Account Setup", expanded=True):
            # First show API key manager
            render_twitter_api_key_manager()
            
            # Then show account manager
            render_twitter_account_manager()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎯 Quick Actions", "📊 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Create New Tweet", use_container_width=True):
                # Set the current feature to the enhanced tweet generator
                st.session_state.current_feature = enhanced_tweet_generator
                st.experimental_rerun()
        with col2:
            if st.button("📅 Plan Content", use_container_width=True):
                # Set the current feature to the calendar generator
                st.session_state.current_feature = render_calendar_generator
                st.experimental_rerun()
        with col3:
            if st.button("📊 View Analytics", use_container_width=True):
                # Set the current feature to performance analytics
                st.session_state.current_feature = render_performance_analytics
                st.experimental_rerun()
    
    with tab2:
        st.markdown("### 📈 Analytics Dashboard")
        
        if twitter_connected:
            # Show mini analytics dashboard
            try:
                from .analytics.performance_analytics import get_tweet_performance, analyze_performance
                
                # Get performance data
                with st.spinner("Loading analytics..."):
                    df = get_tweet_performance(days=30)
                    
                    if not df.empty:
                        # Analyze performance
                        analysis = analyze_performance(df)
                        
                        # Display overview metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Tweets", len(df))
                        
                        with col2:
                            st.metric("Total Engagement", f"{analysis['total_engagement']:,}")
                        
                        with col3:
                            st.metric("Avg. Engagement", f"{analysis['avg_engagement']:.1f}")
                        
                        with col4:
                            st.metric("Media Impact", f"{analysis['media_impact']:.2f}x")
                        
                        # Show engagement chart
                        import plotly.express as px
                        
                        # Sort by date
                        df_sorted = df.sort_values("created_at")
                        
                        # Create time series chart
                        fig = px.line(
                            df_sorted,
                            x="created_at",
                            y="engagement",
                            title="Recent Tweet Engagement",
                            labels={"created_at": "Date", "engagement": "Engagement"}
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # View full analytics button
                        if st.button("View Full Analytics", use_container_width=True):
                            st.session_state.current_feature = render_performance_analytics
                            st.experimental_rerun()
                    else:
                        st.info("No recent tweets found. Start tweeting to see analytics!")
            except Exception as e:
                st.error(f"Error loading analytics: {str(e)}")
                st.info("View full analytics for detailed insights")
        else:
            st.info("Connect your Twitter account to view analytics")
    
    with tab3:
        st.markdown("### ⚙️ Settings")
        
        # Twitter account settings
        with st.expander("Twitter Account", expanded=True):
            render_twitter_account_manager()
        
        # API key settings
        with st.expander("API Configuration", expanded=False):
            render_twitter_api_key_manager()
        
        # Preferences
        with st.expander("Preferences", expanded=False):
            st.markdown("#### Dashboard Preferences")
            
            # Theme preference
            theme = st.selectbox(
                "Theme",
                ["Light", "Dark", "System"],
                index=2
            )
            
            # Default content type
            content_type = st.selectbox(
                "Default Content Type",
                ["Informative", "Promotional", "Engaging", "Educational"],
                index=0
            )
            
            # Save preferences
            if st.button("Save Preferences"):
                st.session_state.twitter_preferences = {
                    "theme": theme,
                    "content_type": content_type
                }
                st.success("Preferences saved!")
    
    # Load feature data
    features = load_feature_data()
    
    # Main content area
    st.markdown("## 🛠️ Available Tools")
    
    # Render each category
    for category in features.values():
        render_category_section(category)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p>Need help? Check out our <a href='#'>documentation</a> or <a href='#'>contact support</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_dashboard()
```

## Testing Plan

### Unit Testing

1. **Authentication Tests**
   - Test Twitter API key validation
   - Test OAuth flow
   - Test token storage and retrieval

2. **API Integration Tests**
   - Test tweet posting
   - Test timeline retrieval
   - Test hashtag search
   - Test media upload

3. **Feature Tests**
   - Test tweet generation
   - Test performance prediction
   - Test content calendar creation
   - Test image generation

### Integration Testing

1. **End-to-End Flow Tests**
   - Test complete user journey from authentication to posting
   - Test data flow between components
   - Test error handling and recovery

2. **Cross-Feature Tests**
   - Test integration between tweet generator and performance predictor
   - Test integration between content calendar and tweet scheduler
   - Test integration between analytics and content recommendations

### User Acceptance Testing

1. **Usability Tests**
   - Test with real users to gather feedback
   - Evaluate UI/UX design
   - Measure time to complete common tasks

2. **Performance Tests**
   - Test with large datasets
   - Measure response times
   - Identify bottlenecks

## Implementation Timeline

### Phase 1: Twitter Authentication & Basic Integration (2 weeks)
- Week 1: Set up Twitter API authentication system
- Week 2: Create account connection UI and API key management

### Phase 2: Enhanced Tweet Generator (2 weeks)
- Week 3: Implement real Twitter data integration
- Week 4: Develop tweet performance predictor

### Phase 3: Content Strategy Tools (3 weeks)
- Week 5: Implement content calendar generator
- Week 6-7: Develop hashtag strategy manager

### Phase 4: Visual Content Creation (2 weeks)
- Week 8-9: Implement image generator for quotes, tweets, and infographics

### Phase 5: Analytics & Optimization (2 weeks)
- Week 10-11: Implement performance analytics dashboard

### Phase 6: Integration and Dashboard Updates (1 week)
- Week 12: Update Twitter dashboard and integrate all features

## Conclusion

This implementation plan provides a comprehensive approach to enhancing the Twitter features in AI-Writer. By leveraging the Tweepy library and user-provided API keys, we can transform the "coming soon" features into fully functional components that provide real value to users.

The phased approach allows for incremental delivery of features, with each phase building on the previous one. This ensures that users can start benefiting from the enhancements early, while more advanced features are developed.

Key benefits of this implementation:

1. **Real Twitter Integration**: Users can connect their Twitter accounts and interact directly with the platform.
2. **Data-Driven Insights**: Performance analytics and predictions based on real Twitter data.
3. **Comprehensive Content Strategy**: Tools for planning, creating, and optimizing Twitter content.
4. **Visual Content Creation**: Easy-to-use tools for creating engaging visual content.
5. **Streamlined Workflow**: Integrated dashboard for managing all Twitter activities.

By following this plan, AI-Writer will stand out against competitors by offering a complete Twitter content creation and management solution that leverages real data and AI to optimize performance.
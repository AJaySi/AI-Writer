"""
LinkedIn Poll Generator

This module provides functionality for generating LinkedIn polls with
AI-powered content and engagement optimization.
"""

import streamlit as st
import time
import json
import random
from typing import Dict, List, Optional, Union, Tuple
from loguru import logger
from datetime import datetime, timedelta

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search


class LinkedInPollGenerator:
    """
    AI-powered LinkedIn poll generator that creates engaging polls with optimized options,
    engagement predictions, and follow-up content suggestions.
    """
    
    def __init__(self):
        """Initialize the LinkedIn Poll Generator."""
        self.poll_types = {
            "multiple_choice": "Multiple Choice (2-4 options)",
            "yes_no": "Yes/No",
            "rating": "Rating Scale (1-5 or 1-10)",
            "ranking": "Ranking (order items by preference)",
            "open_ended": "Open-ended (with suggested responses)"
        }
        
        self.poll_durations = {
            "1_day": "1 day",
            "3_days": "3 days",
            "5_days": "5 days",
            "7_days": "7 days",
            "14_days": "14 days"
        }
        
        self.engagement_levels = {
            "low": "Low (0-10 responses)",
            "medium": "Medium (11-50 responses)",
            "high": "High (51-200 responses)",
            "viral": "Viral (200+ responses)"
        }
    
    def research_topic(self, topic: str, industry: str, search_engine: str = "metaphor") -> Dict:
        """
        Research a topic to inform poll question generation.
        
        Args:
            topic: The topic to research
            industry: The industry context
            search_engine: The search engine to use (metaphor, google, tavily)
            
        Returns:
            Dict containing research results
        """
        logger.info(f"Researching topic: {topic} in industry: {industry}")
        
        research_results = {
            "topic": topic,
            "industry": industry,
            "search_engine": search_engine,
            "articles": [],
            "trends": [],
            "insights": [],
            "questions": []
        }
        
        # Perform research based on selected search engine
        if search_engine == "metaphor":
            try:
                articles = metaphor_search_articles(
                    query=f"{topic} {industry} trends insights",
                    num_results=5
                )
                research_results["articles"] = articles
            except Exception as e:
                logger.error(f"Error researching with Metaphor: {str(e)}")
                st.error(f"Error researching with Metaphor: {str(e)}")
        elif search_engine == "google":
            try:
                search_results = do_google_serp_search(
                    query=f"{topic} {industry} trends insights",
                    num_results=5
                )
                research_results["articles"] = search_results
            except Exception as e:
                logger.error(f"Error researching with Google: {str(e)}")
                st.error(f"Error researching with Google: {str(e)}")
        elif search_engine == "tavily":
            try:
                search_results = do_tavily_ai_search(
                    query=f"{topic} {industry} trends insights",
                    search_depth="advanced",
                    include_answer=True,
                    include_raw_content=True,
                    max_results=5
                )
                research_results["articles"] = search_results
            except Exception as e:
                logger.error(f"Error researching with Tavily: {str(e)}")
                st.error(f"Error researching with Tavily: {str(e)}")
        
        # Extract insights and trends from research
        if research_results["articles"]:
            research_results["insights"], research_results["trends"] = self._extract_insights_and_trends(research_results["articles"])
            
            # Generate potential poll questions based on research
            research_results["questions"] = self._generate_potential_questions(
                topic, industry, research_results["insights"], research_results["trends"]
            )
        
        return research_results
    
    def _extract_insights_and_trends(self, articles: List[Dict]) -> Tuple[List[str], List[str]]:
        """
        Extract insights and trends from research articles.
        
        Args:
            articles: List of research articles
            
        Returns:
            Tuple of (insights, trends)
        """
        insights = []
        trends = []
        
        # Extract text content from articles
        article_texts = []
        for article in articles:
            if isinstance(article, dict):
                if "content" in article:
                    article_texts.append(article["content"])
                elif "snippet" in article:
                    article_texts.append(article["snippet"])
                elif "description" in article:
                    article_texts.append(article["description"])
            elif isinstance(article, str):
                article_texts.append(article)
        
        if not article_texts:
            return insights, trends
        
        # Use AI to extract insights and trends
        try:
            prompt = f"""
            Based on the following research articles, extract:
            1. 5 key insights about the topic
            2. 5 emerging trends related to the topic
            
            Research articles:
            {' '.join(article_texts[:3])}
            
            Format your response as:
            INSIGHTS:
            - Insight 1
            - Insight 2
            ...
            
            TRENDS:
            - Trend 1
            - Trend 2
            ...
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=500)
            
            # Parse the response
            if "INSIGHTS:" in response and "TRENDS:" in response:
                insights_section = response.split("INSIGHTS:")[1].split("TRENDS:")[0].strip()
                trends_section = response.split("TRENDS:")[1].strip()
                
                insights = [insight.strip("- ").strip() for insight in insights_section.split("\n") if insight.strip()]
                trends = [trend.strip("- ").strip() for trend in trends_section.split("\n") if trend.strip()]
        except Exception as e:
            logger.error(f"Error extracting insights and trends: {str(e)}")
        
        return insights, trends
    
    def _generate_potential_questions(self, topic: str, industry: str, insights: List[str], trends: List[str]) -> List[str]:
        """
        Generate potential poll questions based on research.
        
        Args:
            topic: The topic
            industry: The industry
            insights: List of insights
            trends: List of trends
            
        Returns:
            List of potential poll questions
        """
        questions = []
        
        try:
            prompt = f"""
            Generate 5 engaging LinkedIn poll questions about {topic} in the {industry} industry.
            
            Use these insights and trends to inform your questions:
            INSIGHTS:
            {chr(10).join([f"- {insight}" for insight in insights])}
            
            TRENDS:
            {chr(10).join([f"- {trend}" for trend in trends])}
            
            The questions should:
            1. Be thought-provoking and encourage discussion
            2. Be relevant to professionals in the {industry} industry
            3. Be concise and clear
            4. Avoid leading or biased language
            5. Be suitable for a LinkedIn poll format
            
            Format each question as a separate line starting with a number.
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=500)
            
            # Parse the response
            for line in response.split("\n"):
                line = line.strip()
                if line and any(line.startswith(str(i)) for i in range(1, 10)):
                    question = line.split(".", 1)[1].strip() if "." in line else line
                    questions.append(question)
        except Exception as e:
            logger.error(f"Error generating potential questions: {str(e)}")
        
        return questions
    
    def generate_poll_question(self, topic: str, industry: str, poll_type: str, tone: str = "professional") -> str:
        """
        Generate a poll question based on the topic, industry, and poll type.
        
        Args:
            topic: The topic for the poll
            industry: The industry context
            poll_type: The type of poll (multiple_choice, yes_no, rating, ranking, open_ended)
            tone: The tone to use (professional, casual, authoritative, etc.)
            
        Returns:
            The generated poll question
        """
        logger.info(f"Generating {poll_type} poll question about {topic} in {industry} industry with {tone} tone")
        
        try:
            prompt = f"""
            Generate a LinkedIn poll question about {topic} in the {industry} industry.
            
            Poll type: {self.poll_types[poll_type]}
            Tone: {tone}
            
            The question should:
            1. Be thought-provoking and encourage discussion
            2. Be relevant to professionals in the {industry} industry
            3. Be concise and clear (ideally under 100 characters)
            4. Avoid leading or biased language
            5. Be suitable for a LinkedIn poll format
            6. Use a {tone} tone
            
            Return only the question text without any additional formatting or explanation.
            """
            
            question = llm_text_gen(prompt=prompt, max_tokens=100).strip()
            
            # Ensure the question ends with a question mark if it doesn't already
            if not question.endswith("?"):
                question += "?"
            
            return question
        except Exception as e:
            logger.error(f"Error generating poll question: {str(e)}")
            return f"What's your opinion on {topic} in the {industry} industry?"
    
    def generate_poll_options(self, question: str, poll_type: str, industry: str, num_options: int = 4) -> List[str]:
        """
        Generate poll options based on the question and poll type.
        
        Args:
            question: The poll question
            poll_type: The type of poll (multiple_choice, yes_no, rating, ranking, open_ended)
            industry: The industry context
            num_options: The number of options to generate (for multiple choice)
            
        Returns:
            List of poll options
        """
        logger.info(f"Generating {poll_type} poll options for question: {question}")
        
        options = []
        
        if poll_type == "yes_no":
            return ["Yes", "No"]
        elif poll_type == "rating":
            return [str(i) for i in range(1, 6)]  # 1-5 rating scale
        elif poll_type == "ranking":
            # For ranking, we'll generate items to rank
            try:
                prompt = f"""
                Generate 4 items to rank in a LinkedIn poll about: {question}
                
                Industry context: {industry}
                
                The items should:
                1. Be relevant to the question
                2. Be concise (1-5 words each)
                3. Be distinct from each other
                4. Be suitable for ranking in order of preference or importance
                
                Return only the items, one per line, without numbering or additional formatting.
                """
                
                response = llm_text_gen(prompt=prompt, max_tokens=200)
                
                # Parse the response
                for line in response.split("\n"):
                    line = line.strip()
                    if line and not line.startswith(("1.", "2.", "3.", "4.", "-", "*")):
                        options.append(line)
                    elif line and line.startswith(("1.", "2.", "3.", "4.", "-", "*")):
                        # Remove numbering or bullets
                        option = line.split(".", 1)[1].strip() if "." in line else line.lstrip("- *").strip()
                        options.append(option)
                
                # Ensure we have exactly 4 options
                if len(options) > 4:
                    options = options[:4]
                elif len(options) < 4:
                    # Add generic options if we don't have enough
                    generic_options = ["Option 1", "Option 2", "Option 3", "Option 4"]
                    options.extend(generic_options[len(options):4])
            except Exception as e:
                logger.error(f"Error generating ranking options: {str(e)}")
                options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        elif poll_type == "open_ended":
            # For open-ended, we'll generate suggested responses
            try:
                prompt = f"""
                Generate 3 suggested responses for an open-ended LinkedIn poll about: {question}
                
                Industry context: {industry}
                
                The responses should:
                1. Be relevant to the question
                2. Be concise (5-15 words each)
                3. Represent different perspectives or approaches
                4. Encourage others to share their own responses
                
                Return only the responses, one per line, without numbering or additional formatting.
                """
                
                response = llm_text_gen(prompt=prompt, max_tokens=200)
                
                # Parse the response
                for line in response.split("\n"):
                    line = line.strip()
                    if line and not line.startswith(("1.", "2.", "3.", "-", "*")):
                        options.append(line)
                    elif line and line.startswith(("1.", "2.", "3.", "-", "*")):
                        # Remove numbering or bullets
                        option = line.split(".", 1)[1].strip() if "." in line else line.lstrip("- *").strip()
                        options.append(option)
                
                # Ensure we have exactly 3 options
                if len(options) > 3:
                    options = options[:3]
                elif len(options) < 3:
                    # Add generic options if we don't have enough
                    generic_options = ["Response 1", "Response 2", "Response 3"]
                    options.extend(generic_options[len(options):3])
            except Exception as e:
                logger.error(f"Error generating open-ended options: {str(e)}")
                options = ["Response 1", "Response 2", "Response 3"]
        else:  # multiple_choice
            try:
                prompt = f"""
                Generate {num_options} options for a LinkedIn poll about: {question}
                
                Industry context: {industry}
                
                The options should:
                1. Be relevant to the question
                2. Be concise (1-5 words each)
                3. Be distinct from each other
                4. Cover a range of possible answers
                5. Be suitable for a multiple-choice poll
                
                Return only the options, one per line, without numbering or additional formatting.
                """
                
                response = llm_text_gen(prompt=prompt, max_tokens=200)
                
                # Parse the response
                for line in response.split("\n"):
                    line = line.strip()
                    if line and not line.startswith(("1.", "2.", "3.", "4.", "-", "*")):
                        options.append(line)
                    elif line and line.startswith(("1.", "2.", "3.", "4.", "-", "*")):
                        # Remove numbering or bullets
                        option = line.split(".", 1)[1].strip() if "." in line else line.lstrip("- *").strip()
                        options.append(option)
                
                # Ensure we have exactly num_options
                if len(options) > num_options:
                    options = options[:num_options]
                elif len(options) < num_options:
                    # Add generic options if we don't have enough
                    generic_options = [f"Option {i+1}" for i in range(num_options)]
                    options.extend(generic_options[len(options):num_options])
            except Exception as e:
                logger.error(f"Error generating multiple choice options: {str(e)}")
                options = [f"Option {i+1}" for i in range(num_options)]
        
        return options
    
    def predict_engagement(self, question: str, options: List[str], industry: str) -> Dict:
        """
        Predict engagement levels for a poll.
        
        Args:
            question: The poll question
            options: The poll options
            industry: The industry context
            
        Returns:
            Dict containing engagement predictions
        """
        logger.info(f"Predicting engagement for poll: {question}")
        
        engagement_prediction = {
            "expected_responses": 0,
            "engagement_level": "low",
            "response_distribution": {},
            "comment_likelihood": "low",
            "share_likelihood": "low",
            "insights": []
        }
        
        try:
            prompt = f"""
            Predict engagement for a LinkedIn poll with the following details:
            
            Question: {question}
            Options: {', '.join(options)}
            Industry: {industry}
            
            Provide predictions for:
            1. Expected number of responses (low: 0-10, medium: 11-50, high: 51-200, viral: 200+)
            2. Likelihood of comments (low, medium, high)
            3. Likelihood of shares (low, medium, high)
            4. Expected distribution of responses across options (as percentages)
            5. 3 key insights that might be gained from this poll
            
            Format your response as JSON:
            {{
                "expected_responses": "low/medium/high/viral",
                "response_count": number,
                "comment_likelihood": "low/medium/high",
                "share_likelihood": "low/medium/high",
                "response_distribution": {{
                    "option1": percentage,
                    "option2": percentage,
                    ...
                }},
                "insights": [
                    "insight1",
                    "insight2",
                    "insight3"
                ]
            }}
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=500)
            
            # Parse the JSON response
            try:
                prediction_data = json.loads(response)
                
                engagement_prediction["engagement_level"] = prediction_data.get("expected_responses", "low")
                engagement_prediction["expected_responses"] = prediction_data.get("response_count", 0)
                engagement_prediction["comment_likelihood"] = prediction_data.get("comment_likelihood", "low")
                engagement_prediction["share_likelihood"] = prediction_data.get("share_likelihood", "low")
                engagement_prediction["response_distribution"] = prediction_data.get("response_distribution", {})
                engagement_prediction["insights"] = prediction_data.get("insights", [])
            except json.JSONDecodeError:
                logger.error("Error parsing engagement prediction JSON")
                # Set default values
                engagement_prediction["engagement_level"] = "low"
                engagement_prediction["expected_responses"] = 5
                engagement_prediction["comment_likelihood"] = "low"
                engagement_prediction["share_likelihood"] = "low"
                engagement_prediction["response_distribution"] = {option: 100/len(options) for option in options}
                engagement_prediction["insights"] = ["No insights available"]
        except Exception as e:
            logger.error(f"Error predicting engagement: {str(e)}")
        
        return engagement_prediction
    
    def suggest_poll_duration(self, question: str, industry: str) -> str:
        """
        Suggest an optimal poll duration based on the question and industry.
        
        Args:
            question: The poll question
            industry: The industry context
            
        Returns:
            Suggested poll duration
        """
        logger.info(f"Suggesting poll duration for: {question}")
        
        try:
            prompt = f"""
            Suggest an optimal duration for a LinkedIn poll with the following details:
            
            Question: {question}
            Industry: {industry}
            
            Consider:
            1. The complexity of the question
            2. The industry's typical response patterns
            3. The target audience's likely engagement patterns
            4. The time sensitivity of the topic
            
            Return only one of these options: 1_day, 3_days, 5_days, 7_days, 14_days
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=50).strip().lower()
            
            # Validate the response
            if response in self.poll_durations:
                return response
            else:
                # Default to 3 days if the response is invalid
                return "3_days"
        except Exception as e:
            logger.error(f"Error suggesting poll duration: {str(e)}")
            return "3_days"
    
    def generate_follow_up_content(self, question: str, options: List[str], industry: str) -> Dict:
        """
        Generate follow-up content suggestions based on poll results.
        
        Args:
            question: The poll question
            options: The poll options
            industry: The industry context
            
        Returns:
            Dict containing follow-up content suggestions
        """
        logger.info(f"Generating follow-up content for poll: {question}")
        
        follow_up_content = {
            "post_templates": [],
            "visual_suggestions": [],
            "hashtag_suggestions": [],
            "next_poll_suggestions": []
        }
        
        try:
            prompt = f"""
            Generate follow-up content suggestions for a LinkedIn poll with the following details:
            
            Question: {question}
            Options: {', '.join(options)}
            Industry: {industry}
            
            Provide:
            1. 3 post templates for sharing poll results (with placeholders for actual results)
            2. 3 visual content suggestions (e.g., charts, infographics)
            3. 5 relevant hashtags for the follow-up content
            4. 3 suggestions for follow-up polls that would build on this poll's insights
            
            Format your response as JSON:
            {{
                "post_templates": [
                    "template1",
                    "template2",
                    "template3"
                ],
                "visual_suggestions": [
                    "suggestion1",
                    "suggestion2",
                    "suggestion3"
                ],
                "hashtag_suggestions": [
                    "hashtag1",
                    "hashtag2",
                    "hashtag3",
                    "hashtag4",
                    "hashtag5"
                ],
                "next_poll_suggestions": [
                    "suggestion1",
                    "suggestion2",
                    "suggestion3"
                ]
            }}
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=800)
            
            # Parse the JSON response
            try:
                content_data = json.loads(response)
                
                follow_up_content["post_templates"] = content_data.get("post_templates", [])
                follow_up_content["visual_suggestions"] = content_data.get("visual_suggestions", [])
                follow_up_content["hashtag_suggestions"] = content_data.get("hashtag_suggestions", [])
                follow_up_content["next_poll_suggestions"] = content_data.get("next_poll_suggestions", [])
            except json.JSONDecodeError:
                logger.error("Error parsing follow-up content JSON")
                # Set default values
                follow_up_content["post_templates"] = ["Thank you for participating in our poll about [Topic]! Here are the results..."]
                follow_up_content["visual_suggestions"] = ["Bar chart showing distribution of responses"]
                follow_up_content["hashtag_suggestions"] = [f"#{industry.replace(' ', '')}", "#LinkedInPoll", "#IndustryInsights"]
                follow_up_content["next_poll_suggestions"] = ["What factors influenced your decision in the previous poll?"]
        except Exception as e:
            logger.error(f"Error generating follow-up content: {str(e)}")
        
        return follow_up_content
    
    def generate_data_visualization(self, question: str, options: List[str], response_distribution: Dict) -> str:
        """
        Generate a data visualization suggestion for poll results.
        
        Args:
            question: The poll question
            options: The poll options
            response_distribution: The predicted response distribution
            
        Returns:
            Visualization suggestion
        """
        logger.info(f"Generating data visualization for poll: {question}")
        
        try:
            prompt = f"""
            Suggest a data visualization for a LinkedIn poll with the following details:
            
            Question: {question}
            Options: {', '.join(options)}
            Predicted response distribution: {json.dumps(response_distribution)}
            
            Consider:
            1. The type of data (categorical, ordinal, etc.)
            2. The number of options
            3. The clarity and impact of different chart types
            4. LinkedIn's visual presentation capabilities
            
            Return a detailed description of the recommended visualization, including:
            1. Chart type
            2. Color scheme
            3. Layout
            4. Key elements to highlight
            """
            
            visualization = llm_text_gen(prompt=prompt, max_tokens=300)
            return visualization
        except Exception as e:
            logger.error(f"Error generating data visualization: {str(e)}")
            return "Bar chart showing distribution of responses across options"
    
    def optimize_poll_for_engagement(self, question: str, options: List[str], industry: str) -> Dict:
        """
        Optimize a poll for maximum engagement.
        
        Args:
            question: The poll question
            options: The poll options
            industry: The industry context
            
        Returns:
            Dict containing optimization suggestions
        """
        logger.info(f"Optimizing poll for engagement: {question}")
        
        optimization = {
            "question_improvements": [],
            "option_improvements": [],
            "timing_suggestions": [],
            "audience_targeting": [],
            "hashtag_suggestions": []
        }
        
        try:
            prompt = f"""
            Optimize a LinkedIn poll for maximum engagement with the following details:
            
            Question: {question}
            Options: {', '.join(options)}
            Industry: {industry}
            
            Provide suggestions for:
            1. Question improvements (wording, clarity, impact)
            2. Option improvements (wording, order, completeness)
            3. Timing suggestions (best day/time to post)
            4. Audience targeting (who would be most interested)
            5. Hashtag suggestions (5-7 relevant hashtags)
            
            Format your response as JSON:
            {{
                "question_improvements": [
                    "improvement1",
                    "improvement2",
                    "improvement3"
                ],
                "option_improvements": [
                    "improvement1",
                    "improvement2",
                    "improvement3"
                ],
                "timing_suggestions": [
                    "suggestion1",
                    "suggestion2",
                    "suggestion3"
                ],
                "audience_targeting": [
                    "audience1",
                    "audience2",
                    "audience3"
                ],
                "hashtag_suggestions": [
                    "hashtag1",
                    "hashtag2",
                    "hashtag3",
                    "hashtag4",
                    "hashtag5",
                    "hashtag6",
                    "hashtag7"
                ]
            }}
            """
            
            response = llm_text_gen(prompt=prompt, max_tokens=800)
            
            # Parse the JSON response
            try:
                optimization_data = json.loads(response)
                
                optimization["question_improvements"] = optimization_data.get("question_improvements", [])
                optimization["option_improvements"] = optimization_data.get("option_improvements", [])
                optimization["timing_suggestions"] = optimization_data.get("timing_suggestions", [])
                optimization["audience_targeting"] = optimization_data.get("audience_targeting", [])
                optimization["hashtag_suggestions"] = optimization_data.get("hashtag_suggestions", [])
            except json.JSONDecodeError:
                logger.error("Error parsing optimization JSON")
                # Set default values
                optimization["question_improvements"] = ["Make the question more specific"]
                optimization["option_improvements"] = ["Ensure options are mutually exclusive"]
                optimization["timing_suggestions"] = ["Post on Tuesday or Wednesday during business hours"]
                optimization["audience_targeting"] = [f"Professionals in the {industry} industry"]
                optimization["hashtag_suggestions"] = [f"#{industry.replace(' ', '')}", "#LinkedInPoll", "#IndustryInsights"]
        except Exception as e:
            logger.error(f"Error optimizing poll: {str(e)}")
        
        return optimization


def linkedin_poll_generator_ui():
    """Streamlit UI for the LinkedIn Poll Generator."""
    
    st.title("LinkedIn Poll Generator")
    st.markdown("""
    Create engaging LinkedIn polls that drive interaction and gather valuable insights from your network.
    """)
    
    # Initialize the poll generator
    poll_generator = LinkedInPollGenerator()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Create Poll", "Research & Insights", "Optimization & Follow-up"])
    
    with tab1:
        st.header("Create Your LinkedIn Poll")
        
        # Topic and industry inputs
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Topic", placeholder="e.g., Remote Work, AI in Business, Leadership Styles")
        with col2:
            industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
        
        # Poll type selection
        poll_type = st.selectbox(
            "Poll Type",
            options=list(poll_generator.poll_types.keys()),
            format_func=lambda x: poll_generator.poll_types[x]
        )
        
        # Number of options for multiple choice
        if poll_type == "multiple_choice":
            num_options = st.slider("Number of Options", min_value=2, max_value=4, value=4)
        else:
            num_options = 4  # Default for other poll types
        
        # Tone selection
        tone = st.selectbox(
            "Tone",
            options=["professional", "casual", "authoritative", "conversational", "thoughtful"],
            index=0
        )
        
        # Research button
        if st.button("Research Topic", key="research_button"):
            with st.spinner("Researching topic..."):
                research_results = poll_generator.research_topic(topic, industry)
                
                # Store research results in session state
                st.session_state.research_results = research_results
                
                # Display research results
                st.subheader("Research Results")
                
                if research_results["articles"]:
                    st.write(f"Found {len(research_results['articles'])} relevant articles.")
                    
                    # Display insights
                    if research_results["insights"]:
                        st.subheader("Key Insights")
                        for insight in research_results["insights"]:
                            st.markdown(f"- {insight}")
                    
                    # Display trends
                    if research_results["trends"]:
                        st.subheader("Emerging Trends")
                        for trend in research_results["trends"]:
                            st.markdown(f"- {trend}")
                    
                    # Display potential questions
                    if research_results["questions"]:
                        st.subheader("Potential Poll Questions")
                        for i, question in enumerate(research_results["questions"]):
                            st.markdown(f"{i+1}. {question}")
                else:
                    st.warning("No research results found. Try a different topic or industry.")
        
        # Generate poll button
        if st.button("Generate Poll", key="generate_button"):
            with st.spinner("Generating poll..."):
                # Generate poll question
                question = poll_generator.generate_poll_question(topic, industry, poll_type, tone)
                
                # Generate poll options
                options = poll_generator.generate_poll_options(question, poll_type, industry, num_options)
                
                # Predict engagement
                engagement = poll_generator.predict_engagement(question, options, industry)
                
                # Suggest poll duration
                duration = poll_generator.suggest_poll_duration(question, industry)
                
                # Store poll data in session state
                st.session_state.poll_data = {
                    "question": question,
                    "options": options,
                    "engagement": engagement,
                    "duration": duration
                }
                
                # Display poll
                st.subheader("Your LinkedIn Poll")
                
                # Display question
                st.markdown(f"### {question}")
                
                # Display options
                for i, option in enumerate(options):
                    st.markdown(f"**{i+1}.** {option}")
                
                # Display engagement prediction
                st.subheader("Engagement Prediction")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Expected Responses", engagement["engagement_level"].title())
                with col2:
                    st.metric("Comment Likelihood", engagement["comment_likelihood"].title())
                with col3:
                    st.metric("Share Likelihood", engagement["share_likelihood"].title())
                
                # Display response distribution
                if engagement["response_distribution"]:
                    st.subheader("Predicted Response Distribution")
                    
                    # Create a bar chart
                    import plotly.express as px
                    
                    # Prepare data for the chart
                    chart_data = []
                    for option, percentage in engagement["response_distribution"].items():
                        chart_data.append({"Option": option, "Percentage": percentage})
                    
                    # Create the chart
                    fig = px.bar(chart_data, x="Option", y="Percentage", 
                                title="Predicted Response Distribution",
                                color="Option",
                                color_discrete_sequence=px.colors.qualitative.Set3)
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Display poll duration
                st.subheader("Recommended Poll Duration")
                st.write(f"**{poll_generator.poll_durations[duration]}**")
                
                # Display insights
                if engagement["insights"]:
                    st.subheader("Potential Insights")
                    for insight in engagement["insights"]:
                        st.markdown(f"- {insight}")
    
    with tab2:
        st.header("Research & Insights")
        
        # Check if research results exist
        if "research_results" in st.session_state:
            research_results = st.session_state.research_results
            
            # Display research results
            st.subheader("Research Results")
            
            if research_results["articles"]:
                st.write(f"Found {len(research_results['articles'])} relevant articles.")
                
                # Display insights
                if research_results["insights"]:
                    st.subheader("Key Insights")
                    for insight in research_results["insights"]:
                        st.markdown(f"- {insight}")
                
                # Display trends
                if research_results["trends"]:
                    st.subheader("Emerging Trends")
                    for trend in research_results["trends"]:
                        st.markdown(f"- {trend}")
                
                # Display potential questions
                if research_results["questions"]:
                    st.subheader("Potential Poll Questions")
                    for i, question in enumerate(research_results["questions"]):
                        st.markdown(f"{i+1}. {question}")
            else:
                st.warning("No research results found. Try a different topic or industry.")
        else:
            st.info("Generate a poll first to see research results.")
    
    with tab3:
        st.header("Optimization & Follow-up")
        
        # Check if poll data exists
        if "poll_data" in st.session_state:
            poll_data = st.session_state.poll_data
            
            # Optimization section
            st.subheader("Poll Optimization")
            
            if st.button("Optimize Poll", key="optimize_button"):
                with st.spinner("Optimizing poll..."):
                    # Optimize poll
                    optimization = poll_generator.optimize_poll_for_engagement(
                        poll_data["question"], 
                        poll_data["options"], 
                        industry
                    )
                    
                    # Store optimization in session state
                    st.session_state.optimization = optimization
                    
                    # Display question improvements
                    st.subheader("Question Improvements")
                    for improvement in optimization["question_improvements"]:
                        st.markdown(f"- {improvement}")
                    
                    # Display option improvements
                    st.subheader("Option Improvements")
                    for improvement in optimization["option_improvements"]:
                        st.markdown(f"- {improvement}")
                    
                    # Display timing suggestions
                    st.subheader("Timing Suggestions")
                    for suggestion in optimization["timing_suggestions"]:
                        st.markdown(f"- {suggestion}")
                    
                    # Display audience targeting
                    st.subheader("Audience Targeting")
                    for audience in optimization["audience_targeting"]:
                        st.markdown(f"- {audience}")
                    
                    # Display hashtag suggestions
                    st.subheader("Hashtag Suggestions")
                    hashtags = " ".join([f"#{tag.strip('#')}" for tag in optimization["hashtag_suggestions"]])
                    st.markdown(hashtags)
            
            # Follow-up content section
            st.subheader("Follow-up Content")
            
            if st.button("Generate Follow-up Content", key="followup_button"):
                with st.spinner("Generating follow-up content..."):
                    # Generate follow-up content
                    follow_up = poll_generator.generate_follow_up_content(
                        poll_data["question"], 
                        poll_data["options"], 
                        industry
                    )
                    
                    # Store follow-up in session state
                    st.session_state.follow_up = follow_up
                    
                    # Display post templates
                    st.subheader("Post Templates")
                    for i, template in enumerate(follow_up["post_templates"]):
                        st.markdown(f"**Template {i+1}:**")
                        st.markdown(template)
                        st.markdown("---")
                    
                    # Display visual suggestions
                    st.subheader("Visual Suggestions")
                    for suggestion in follow_up["visual_suggestions"]:
                        st.markdown(f"- {suggestion}")
                    
                    # Display hashtag suggestions
                    st.subheader("Hashtag Suggestions")
                    hashtags = " ".join([f"#{tag.strip('#')}" for tag in follow_up["hashtag_suggestions"]])
                    st.markdown(hashtags)
                    
                    # Display next poll suggestions
                    st.subheader("Next Poll Suggestions")
                    for suggestion in follow_up["next_poll_suggestions"]:
                        st.markdown(f"- {suggestion}")
            
            # Data visualization section
            st.subheader("Data Visualization")
            
            if st.button("Generate Visualization", key="visualization_button"):
                with st.spinner("Generating visualization suggestion..."):
                    # Generate visualization
                    visualization = poll_generator.generate_data_visualization(
                        poll_data["question"], 
                        poll_data["options"], 
                        poll_data["engagement"]["response_distribution"]
                    )
                    
                    # Store visualization in session state
                    st.session_state.visualization = visualization
                    
                    # Display visualization
                    st.markdown(visualization)
        else:
            st.info("Generate a poll first to see optimization and follow-up suggestions.") 
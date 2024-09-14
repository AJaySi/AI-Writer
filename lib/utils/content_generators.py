import streamlit as st
from lib.utils.alwrity_utils import (
    blog_from_keyword, ai_agents_team, essay_writer, ai_news_writer, ai_seo_tools,
    ai_finance_ta_writer, ai_social_writer, competitor_analysis
)
import pandas as pd
import matplotlib.pyplot as plt
from lib.ai_writers.ai_story_writer.story_writer import story_input_section
from lib.ai_web_researcher.google_trends_researcher import (
    fetch_multirange_interest_over_time,
    fetch_historical_hourly_interest,
    fetch_trending_searches,
    fetch_realtime_search_trends,
    fetch_top_charts,
    fetch_suggestions
)
from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_content_planner

def ai_writers():
    options = [
        "AI Blog Writer",
        "Story Writer",
        "Essay writer",
        "Write News reports",
        "Write Financial TA report",
        "AI Product Description Writer",
        "AI Copywriter",
        "Quit"
    ]
    choice = st.selectbox("**👇Select a content creation type:**", options, index=0, format_func=lambda x: f"📝 {x}")

    if choice == "AI Blog Writer":
        blog_from_keyword()
    elif choice == "Story Writer":
        story_input_section()
    elif choice == "Essay writer":
        essay_writer()
    elif choice == "Write News reports":
        ai_news_writer()
    elif choice == "Write Financial TA report":
        ai_finance_ta_writer()
    elif choice == "AI Product Description Writer":
        write_ai_prod_desc()
    elif choice == "Quit":
        st.subheader("Exiting, Getting Lost. But.... I have nowhere to go 🥹🥹")


def content_planning_tools():
    st.markdown("""**Alwrity content Ideation & Planning** : Provide few keywords to do comprehensive web research.
             Provide few keywords to get Google, Neural, pytrends analysis. Know keywords, blog titles to target.
             Generate months long content calendar around given keywords.""")
    
    options = [
        "Keywords Researcher",
        "Competitor Analysis",
        "Content Calender Ideator"
    ]
    choice = st.radio("Select a content planning tool:", options, index=0, format_func=lambda x: f"🔍 {x}")
    
    if choice == "Keywords Researcher":
        st.title("Web Research Assistant")
        st.write("Enter keywords for web research. The keywords should be at least three words long.")
        
        search_keywords = st.text_input("Search Keywords", placeholder="Enter keywords for web research...")
        if st.button("Start Web Research"):
            if search_keywords and len(search_keywords.split()) >= 3:
                try:
                    st.info(f"Starting web research on given keywords: {search_keywords}")
                    with st.spinner("Performing web research..."):
                        # Fetch and display multirange interest over time
                        st.subheader("Multirange Interest Over Time")
                        multirange_data = fetch_multirange_interest_over_time([search_keywords], ['today 3-m', 'today 1-m'])
                        st.dataframe(multirange_data)

                        # Fetch and display historical hourly interest
                        st.subheader("Historical Hourly Interest")
                        hourly_data = fetch_historical_hourly_interest([search_keywords], '2023-01-01', '2023-01-31')
                        st.dataframe(hourly_data)

                        # Fetch and display trending searches
                        st.subheader("Trending Searches")
                        trending_data = fetch_trending_searches()
                        st.dataframe(trending_data)

                        # Fetch and display realtime search trends
                        st.subheader("Realtime Search Trends")
                        realtime_data = fetch_realtime_search_trends()
                        st.dataframe(realtime_data)

                        # Fetch and display top charts
                        st.subheader("Top Charts")
                        top_charts_data = fetch_top_charts(2023)
                        st.dataframe(top_charts_data)

                        # Fetch and display suggestions
                        st.subheader("Suggestions")
                        suggestions = fetch_suggestions(search_keywords)
                        st.dataframe(pd.DataFrame(suggestions))

                        # Example of plotting with Matplotlib
                        st.subheader("Interest Over Time Plot")
                        plt.figure(figsize=(10, 6))
                        plt.plot(multirange_data['date'], multirange_data[search_keywords], label=search_keywords)
                        plt.title(f'Interest Over Time for "{search_keywords}"')
                        plt.xlabel('Date')
                        plt.ylabel('Interest')
                        plt.legend()
                        st.pyplot(plt)

                    st.success("Web research completed successfully!")
                except Exception as err:
                    st.error(f"ERROR: Failed to do web research: {err}")
            else:
                st.warning("Search keywords should be at least three words long. Please try again.")
    elif choice == "Competitor Analysis":
        competitor_analysis()
    elif choice == "Content Calender Ideator":
        plan_keywords = st.text_input(
            "**Enter Your main Keywords to get 2 months content calendar:**",
            placeholder="Enter 2-3 main keywords to generate AI content calendar with keyword researched blog titles",
            help="The keywords are the ones where you would want to generate 50-60 blogs/articles on."
        )
        if st.button("**Ideate Content Calender**"):
            if plan_keywords:
                ai_agents_content_planner(plan_keywords)
            else:
                st.error("Come on, really, Enter some keywords to plan on..")

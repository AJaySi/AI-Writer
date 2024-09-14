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
from pytrends.request import TrendReq
from datetime import datetime

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
    elif choice == "Keywords Researcher":
        google_trends_analysis()
        competitor_analysis()
    elif choice == "Competitor Analysis":
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
def google_trends_analysis():
    st.title("Google Trends Analysis")

    # Prompt user for required input
    keyword = st.text_input("Enter Keyword(s)", help="Enter one or more keywords separated by commas.")
    
    # Optional inputs with intelligent defaults
    start_time = st.date_input("Start Time", value=datetime(2004, 1, 1), help="Start date for the analysis.")
    end_time = st.date_input("End Time", value=datetime.now(), help="End date for the analysis.")
    geo = st.text_input("Geographic Location", value="US", help="Location of interest (e.g., 'US').")
    hl = st.text_input("Preferred Language", value="en", help="Preferred language (e.g., 'en').")
    timezone = st.number_input("Timezone", value=360, help="Timezone offset in minutes from UTC.")
    category = st.number_input("Category", value=0, help="Category to search within.")
    property = st.selectbox("Google Property", options=["", "images", "news", "youtube", "froogle"], help="Google property to filter on.")
    resolution = st.selectbox("Resolution", options=["COUNTRY", "REGION", "CITY", "DMA"], help="Granularity of the geo search.")
    granular_time_resolution = st.checkbox("Granular Time Resolution", value=False, help="Use finer time resolution if applicable.")

    if st.button("Analyze"):
        if not keyword:
            st.error("Keyword is required.")
            return

        # Initialize pytrends
        pytrends = TrendReq(hl=hl, tz=timezone)

        # Build the payload
        pytrends.build_payload(
            kw_list=keyword.split(','),
            timeframe=f"{start_time.strftime('%Y-%m-%d')} {end_time.strftime('%Y-%m-%d')}",
            geo=geo,
            cat=category,
            gprop=property
        )

        # Fetch interest over time
        interest_over_time_df = pytrends.interest_over_time()
        st.subheader("Interest Over Time")
        st.dataframe(interest_over_time_df)

        # Fetch interest by region
        interest_by_region_df = pytrends.interest_by_region(resolution=resolution)
        st.subheader("Interest By Region")
        st.dataframe(interest_by_region_df)

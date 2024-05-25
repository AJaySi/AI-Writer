import time #Iwish
import os
import json
import streamlit as st


def write_yt_description():
    st.title("📽️ YT Description Writer")
    col1, col2 = st.columns([1, 1])
    with col1:
        keywords = st.text_input('**Describe Your YT video Keywords (comma-separated)**', 
                                help="Enter keywords separated by commas.").split(',')
        target_audience = st.multiselect('**Select Your Target Audience**', 
                    ['Beginners', 'Marketers', 'Gamers', 'Foodies', 'Entrepreneurs', 'Students', 'Parents', 
                     'Tech Enthusiasts', 'General Audience', 'News Readers', 'Finance Enthusiasts'], 
                    help="Select the target audience for your video.")
    
    with col2:
        tone_style = st.selectbox('**Select Tone and Style of YT Description**', 
                    ['Casual', 'Professional', 'Humorous', 'Formal', 'Informal', 'Inspirational'],
                    help="Select the tone and style of your video.")
        language = st.selectbox('**Select YT description Language**', 
                    ['English', 'Spanish', 'Chinese', 'Hindi', 'Arabic'], 
                    help="Select the language for the video description.")
    
    if st.button('**Generate YT Description**'):
        with st.spinner():
            if not keywords:
                st.error("🚫 Please provide all required inputs.")
            else:
                response = generate_youtube_description(keywords, target_audience, tone_style, language)
                if response:
                    st.subheader(f'**🧕👩: Your Final youtube Description !**')
                    st.write(response)
                    st.write("\n\n\n\n\n\n")
                else:
                    st.error("💥**Failed to write YT Description. Please try again!**")


def generate_youtube_description(keywords, target_audience, tone_style, language):
    """ Generate youtube script generator """

    prompt = f"""
    Please write a descriptive YouTube description in {language} for a video about {keywords} based on the following information:

    Keywords: {', '.join(keywords)}

    Target Audience: {', '.join(target_audience)}

    Language for description: {', '.join(language)}

    Tone and Style: {tone_style}

    Specific Instructions:

    - Include Primary Keywords Early: Place the most important keywords at the beginning to enhance SEO.
    - Write a Compelling Hook: Start with an engaging sentence to grab attention and entice viewers to watch the video.
    - Provide a Brief Overview: Summarize the video's content and what viewers can expect to learn or experience.
    - Use Relevant Keywords: Integrate additional keywords naturally to improve searchability.
    - Add Timestamps: Include timestamps for different sections of the video, if applicable.
    - Include Links: Add links to related videos, playlists, or external resources.
    - Encourage Engagement: Ask viewers to like, comment, and subscribe, and include a clear call to action.
    - Provide Contact Information: Include relevant social media handles, website links, or contact information.
    - Use Clear and Concise Language: Avoid jargon and keep sentences straightforward and easy to understand.
    - Include Hashtags: Use relevant hashtags to increase discoverability, placing them at the end of the description.
    - Tailor the Language and Tone: Adjust to suit the target audience.
    - Engage and Describe: Use descriptive language to make the video sound interesting.
    - Be Concise but Informative: Provide enough context about the video.
    - Highlight Unique Details: Mention any important details or highlights that make the video unique.
    - Ensure Proper Grammar and Spelling: Maintain a high standard of writing.

    Generate a detailed YouTube description that adheres to the above guidelines and includes a compelling hook, a brief overview, relevant keywords, a call to action, hashtags, and any other relevant information. Ensure proper formatting and a clear structure.
    """
    
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)

def write_yt_title():
    """ Generat YT Titles UI """
    st.title("🎬 Write YT Video Titles")
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2 = st.columns([5, 5])
        with col1:
            main_points = st.text_area('**What is your video about ?**',
                    placeholder='Write few words on your video for title ? (e.g., "New trek, Latest in news, Finance, Tech...")')
            tone_style = st.selectbox('**Select Tone & Style**', ['Casual', 'Professional', 'Humorous', 'Formal', 'Informal', 'Inspirational'])
        with col2:
            target_audience = st.multiselect('**Select Video Target Audience(One Or Multiple)**', [
                'Beginners',
                'Marketers',
                'Gamers',
                'Foodies',
                'Entrepreneurs',
                'Students',
                'Parents',
                'Tech Enthusiasts',
                'General Audience',
                'News article',
                'Finance Article'])

            use_case = st.selectbox('**Youtube Title Use Case**', [
                'Tutorials',
                'Product Reviews',
                'Explainer Videos',
                'Vlogs',
                'Motivational Speeches',
                'Comedy Skits',
                'Educational Content'
            ])
        if st.button('**Write YT Titles**'):
            with st.status("Assigning AI professional to write your YT Titles..", expanded=True) as status:
                if not main_points:
                    st.error("🚫 Please provide all required inputs.")
                else:
                    response = generate_youtube_title(target_audience, main_points, tone_style, use_case)
                    if response:
                        st.subheader(f'**🧕👩: Your Final youtube Titles !**')
                        st.markdown(response)
                        st.write("\n\n\n")
                    else:
                        st.error("💥**Failed to write Letter. Please try again!**")


def generate_youtube_title(target_audience, main_points, tone_style, use_case):
    """ Generate youtube script generator """

    prompt = f"""
    **Instructions:**

    Please generate 5 YouTube title options for a video about **{main_points}** based on the following information:


    **Target Audience:** {target_audience}

    **Tone and Style:** {tone_style}

    **Use Case:** {use_case}

    **Specific Instructions:**

    * Make the titles catchy and attention-grabbing.
    * Use relevant keywords to improve SEO.
    * Tailor the language and tone to the target audience.
    * Ensure the title reflects the content and use case of the video.
    """

    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def write_yt_script():
    """ Generate youtube scripts """
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2 = st.columns([5, 5])
        with col1:
            main_points = st.text_area('**What is your video about ?**',
                    placeholder='Write few lines on Video idea for transcript ? (e.g., "New trek, Latest in news, Finance, Tech...")')
            tone_style = st.selectbox('**Select Tone & Style**', ['Casual', 'Professional', 'Humorous', 'Formal', 'Informal', 'Inspirational'])
            target_audience = st.multiselect('**Select Video Target Audience(One Or Multiple)**', [
                'Beginners',
                'Marketers',
                'Gamers',
                'Foodies',
                'Entrepreneurs',
                'Students',
                'Parents',
                'Tech Enthusiasts',
                'General Audience',
                'News article',
                'Finance Article'
            ])
        with col2:
            # Selectbox for Video Length
            video_length = st.selectbox('**Select Video Length**', [
                'Short (1-3 minutes)',
                'Medium (3-5 minutes)',
                'Long (5-10 minutes)',
                'Very Long (10+ minutes)'
            ])

            # Selectbox for Script Structure
            script_structure = st.selectbox('**Script Structure**', [
                'Linear',
                'Storytelling',
                'Q&A'
            ])

            use_case = st.selectbox('**Youtube Script Use Case**', [
                'Tutorials',
                'Product Reviews',
                'Explainer Videos',
                'Vlogs',
                'Motivational Speeches',
                'Comedy Skits',
                'Educational Content'
            ])
    if st.button('**Write YT Script**'):
        with st.status("Assigning AI professional to write your YT script..", expanded=True) as status:
            if not main_points:
                st.error("🚫 Please provide all required inputs.")
            else:
                response = generate_youtube_script(target_audience, main_points, tone_style, video_length, use_case, script_structure)
                if response:
                    st.subheader(f'**🧕👩: Your Final youtube script!**')
                    st.write(response)
                    st.write("\n\n\n\n\n\n")
                else:
                    st.error("💥**Failed to write Letter. Please try again!**")


def generate_youtube_script(target_audience, main_points, tone_style, video_length, use_case, script_structure):
    """ Generate youtube script generator """
    prompt = f"""
    Please write a YouTube script for a video about {main_points} based on the following information:

    Target Audience: {', '.join(target_audience)}

    Main Points: {', '.join(main_points)}

    Tone and Style: {tone_style}

    Video Length: {video_length}

    Script Structure: {script_structure}

    Specific Instructions:
    * Include a strong hook to grab attention at the start.
    * Structure the script with clear sections and headings.
    * Provide engaging introductions and conclusions for each section.
    * Use clear and concise language, avoiding jargon or overly technical terms.
    * Tailor the language and tone to the target audience.
    * Include relevant examples, anecdotes, and stories to make the video more engaging.
    * Add questions to encourage viewer interaction and participation.
    * End the script with a strong call to action, encouraging viewers to subscribe, like the video, or visit your website.

    Use Case: {use_case}

    Output Format:

    Please provide the script in a clear and easy-to-read format. 
    Include clear headings for each section and ensure that all instructions are followed.
    """

    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)

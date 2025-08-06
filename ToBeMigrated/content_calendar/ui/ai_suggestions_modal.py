import streamlit as st

def render_ai_suggestions_modal(generate_ai_suggestions, on_create_brief, on_schedule, on_refine, on_customize):
    st.subheader("AI Content Suggestions")
    default_type = st.session_state.get('ai_modal_type', "Blog Post")
    default_topic = st.session_state.get('ai_modal_topic', "")
    default_platform = st.session_state.get('ai_modal_platform', "Blog")
    content_types = {
        "Blog Post": "Long-form content for in-depth topics",
        "Social Media Post": "Short, engaging content for social platforms",
        "Video": "Visual content with script and storyboard",
        "Newsletter": "Email content for subscriber engagement"
    }
    content_type = st.selectbox(
        "Content Type",
        list(content_types.keys()),
        format_func=lambda x: f"{x} - {content_types[x]}",
        key="modal_suggestion_type",
        index=list(content_types.keys()).index(default_type) if default_type in content_types else 0
    )
    topic = st.text_input("Enter topic or keyword", value=default_topic, key="modal_suggestion_topic")
    with st.expander("Advanced Options"):
        audience = st.multiselect(
            "Target Audience",
            ["Professionals", "Students", "Entrepreneurs", "General Public", "Industry Experts"],
            default=["Professionals"]
        )
        goals = st.multiselect(
            "Content Goals",
            ["Increase Engagement", "Generate Leads", "Build Authority", "Drive Traffic", "Educate"],
            default=["Increase Engagement"]
        )
        tone = st.select_slider(
            "Content Tone",
            options=["Professional", "Casual", "Educational", "Entertaining", "Persuasive"],
            value="Professional"
        )
        length = st.radio(
            "Content Length",
            ["Short", "Medium", "Long"],
            horizontal=True
        )
        st.subheader("AI Model Settings")
        model_settings = {
            "Creativity Level": st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1),
            "Formality Level": st.slider("Formality Level", 0.0, 1.0, 0.5, 0.1),
            "Technical Depth": st.slider("Technical Depth", 0.0, 1.0, 0.5, 0.1)
        }
        st.subheader("Content Style Preferences")
        style_preferences = {
            "Use Examples": st.checkbox("Include Real-world Examples", True),
            "Use Statistics": st.checkbox("Include Statistics and Data", True),
            "Use Quotes": st.checkbox("Include Expert Quotes", False),
            "Use Case Studies": st.checkbox("Include Case Studies", False)
        }
        st.subheader("SEO Preferences")
        seo_preferences = {
            "Keyword Density": st.slider("Keyword Density (%)", 1, 5, 2),
            "Internal Linking": st.checkbox("Suggest Internal Links", True),
            "External Linking": st.checkbox("Suggest External Links", True),
            "Meta Description": st.checkbox("Generate Meta Description", True)
        }
        st.subheader("Platform-specific Settings")
        platform_settings = {
            "Hashtag Usage": st.checkbox("Suggest Hashtags", True),
            "Image Suggestions": st.checkbox("Suggest Images", True),
            "Video Suggestions": st.checkbox("Suggest Videos", False),
            "Interactive Elements": st.checkbox("Suggest Interactive Elements", False)
        }
    if st.button("Generate Suggestions", type="primary", key="modal_generate_btn"):
        with st.spinner("Generating suggestions..."):
            suggestions = generate_ai_suggestions(
                content_type,
                topic,
                audience,
                goals,
                tone,
                length,
                model_settings,
                style_preferences,
                seo_preferences,
                platform_settings
            )
            if suggestions:
                suggestion_tabs = st.tabs([f"Suggestion {i+1}" for i in range(len(suggestions))])
                for i, (tab, suggestion) in enumerate(zip(suggestion_tabs, suggestions)):
                    with tab:
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.subheader(suggestion['title'])
                            st.write(f"**Type:** {suggestion['type']}")
                            st.write(f"**Platform:** {suggestion['platform']}")
                            st.write(f"**Target Audience:** {', '.join(suggestion['audience'])}")
                            st.write(f"**Estimated Impact:** {suggestion['impact']}")
                            with st.expander("Content Preview"):
                                st.write(suggestion.get('preview', 'Preview not available'))
                                if suggestion.get('style_elements'):
                                    st.write("**Style Elements:**")
                                    for element in suggestion['style_elements']:
                                        st.write(f"- {element}")
                                if suggestion.get('seo_elements'):
                                    st.write("**SEO Elements:**")
                                    for element in suggestion['seo_elements']:
                                        st.write(f"- {element}")
                        with col2:
                            st.subheader("Performance Metrics")
                            metrics = {
                                "Engagement Score": suggestion.get('engagement_score', '85%'),
                                "Reach Potential": suggestion.get('reach', 'High'),
                                "Conversion Rate": suggestion.get('conversion', '3.5%'),
                                "SEO Impact": suggestion.get('seo_impact', 'Strong')
                            }
                            for metric, value in metrics.items():
                                st.metric(metric, value)
                            st.subheader("Actions")
                            if st.button("Create Brief", key=f"modal_brief_{i}"):
                                on_create_brief(suggestion)
                            if st.button("Schedule", key=f"modal_schedule_{i}"):
                                on_schedule(suggestion)
                            if st.button("Refine", key=f"modal_refine_{i}"):
                                on_refine(suggestion)
                            if st.button("Customize", key=f"modal_customize_{i}"):
                                on_customize(suggestion)
                        with st.expander("Additional Options"):
                            st.write("**Platform Optimizations**")
                            for platform in suggestion.get('platform_optimizations', []):
                                st.write(f"- {platform}")
                            st.write("**Content Variations**")
                            for variation in suggestion.get('variations', []):
                                st.write(f"- {variation}")
                            st.write("**SEO Recommendations**")
                            for seo in suggestion.get('seo_recommendations', []):
                                st.write(f"- {seo}")
                            if suggestion.get('media_suggestions'):
                                st.write("**Media Suggestions**")
                                for media in suggestion['media_suggestions']:
                                    st.write(f"- {media}") 
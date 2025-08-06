"""Text analysis tools using textstat."""

import streamlit as st
from textstat import textstat

def analyze_text(text):
    """Analyze text using textstat metrics."""
    if not text:
        st.warning("Please enter some text to analyze.")
        return
    
    # Calculate various metrics
    metrics = {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Coleman-Liau Index": textstat.coleman_liau_index(text),
        "Linsear Write Formula": textstat.linsear_write_formula(text),
        "Dale-Chall Readability Score": textstat.dale_chall_readability_score(text),
        "Readability Consensus": textstat.readability_consensus(text)
    }
    
    # Display metrics in a clean format
    st.subheader("Text Analysis Results")
    for metric, value in metrics.items():
        st.metric(metric, f"{value:.2f}")
    
    # Add visualizations
    st.subheader("Visualization")
    st.bar_chart(metrics)

st.title("📖  Text Readability Analyzer:  Making Your Content Easy to Read")

st.write("""
    This tool is your guide to writing content that's easy for your audience to understand.
    Just paste in a sample of your text, and we'll break down the readability scores and offer actionable tips! 
""")

text_input = st.text_area("Paste your text here:", height=200)

if st.button("Analyze!"):
    with st.spinner("Analyzing your text..."):
        test_data = text_input
        if not test_data.strip():
            st.error("Please enter text to analyze.")
        else:
            analyze_text(test_data)

            st.subheader("Key Takeaways:")
            st.write("---")
            st.markdown("""
                * **Don't Be Afraid to Simplify!** Often, simpler language makes content more impactful and easier to digest.
                * **Aim for a Reading Level Appropriate for Your Audience:** Consider the education level, background, and familiarity of your readers.
                * **Use Short Sentences:** This makes your content more scannable and easier to read.
                * **Write for Everyone:** Accessibility should always be a priority. When in doubt, aim for clear, concise language!
            """)

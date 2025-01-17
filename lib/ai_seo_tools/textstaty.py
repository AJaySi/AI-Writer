import textstat
import streamlit as st

st.set_page_config(layout="wide", page_title="Text Readability Analyzer", page_icon=":book:")

st.title("📖  Text Readability Analyzer:  Making Your Content Easy to Read")

st.write("""
    This tool is your guide to writing content that's easy for your audience to understand.
    Just paste in a sample of your text, and we'll break down the readability scores and offer actionable tips! 
""")


def analyze_text(test_data):
    """
    Analyzes the readability of the provided text and returns a dictionary with the results.

    Parameters:
    test_data (str): The text to be analyzed.

    Returns:
    dict: A dictionary containing readability scores and additional metrics.
    """
    return {
        "Flesch Reading Ease": {
            "score": textstat.flesch_reading_ease(test_data),
            "description": "This score rates your text on a scale of 0-100, with higher scores being easier to read.",
            "tips": [
                "Score below 30? Simplify your text by breaking down complex sentences, using shorter words, and avoiding jargon.",
                "Score around 60-70? You're in the 'standard' range.",
                "Score over 90? Your text is very easy to read. Add some complexity or sophistication if needed."
            ]
        },
        "Flesch-Kincaid Grade Level": {
            "score": textstat.flesch_kincaid_grade(test_data),
            "description": "This formula estimates the US school grade level needed to understand your text.",
            "tips": [
                "High Score? Your writing might be too complex for your target audience.",
                "Low Score? Your audience might find the text too simple.",
                "Match Your Audience: Tailor the complexity to your readers."
            ]
        },
        "SMOG Index": {
            "score": textstat.smog_index(test_data),
            "description": "This formula measures text complexity by looking at the number of long words and sentences.",
            "tips": [
                "Best for texts with at least 30 sentences.",
                "Adjust complexity to match your target audience."
            ]
        },
        "Coleman-Liau Index": {
            "score": textstat.coleman_liau_index(test_data),
            "description": "This formula uses sentence length and the number of syllables per word to estimate the reading level."
        },
        "Automated Readability Index (ARI)": {
            "score": textstat.automated_readability_index(test_data),
            "description": "Estimates the grade level required to comprehend your text."
        },
        "Dale-Chall Readability Score": {
            "score": textstat.dale_chall_readability_score(test_data),
            "description": "Focuses on the number of uncommon words (not on a list of 3000 common words) and sentence length.",
            "tips": [
                "Easy to Understand: Aim for a score around the reading level of your audience.",
                "High School Level? Scores between 9 and 12 indicate a high school reading level.",
                "Beyond High School? Scores above 12 are usually for a college-level audience."
            ]
        },
        "Gunning Fog": {
            "score": textstat.gunning_fog(test_data),
            "description": "Calculates the grade level required to understand the text."
        },
        "Linsear Write Formula": {
            "score": textstat.linsear_write_formula(test_data),
            "description": "Estimates the US grade level needed to understand the text."
        },
        "Text Standard (Consensus)": {
            "score": textstat.text_standard(test_data),
            "description": "A consensus estimate of the US grade level needed to understand your text, based on multiple readability scores."
        },
        "Spache Readability": {
            "score": textstat.spache_readability(test_data),
            "description": "Best for analyzing text for children, typically up to grade 4.",
            "tips": [
                "Considers the number of unfamiliar words and the length of sentences."
            ]
        },
        "McAlpine EFLAW": {
            "score": textstat.mcalpine_eflaw(test_data),
            "description": "Evaluates text for foreign language learners, focusing on 'miniwords' and sentence length.",
            "tips": [
                "Target Score: Aim for a score of 25 or less."
            ]
        },
        "Reading Time": {
            "score": textstat.reading_time(test_data),
            "description": "Estimated reading time in minutes."
        },
        "Syllable Count": {
            "score": textstat.syllable_count(test_data),
            "description": "The number of syllables in the text."
        },
        "Word Count": {
            "score": textstat.lexicon_count(test_data),
            "description": "The number of words in the text."
        },
        "Sentence Count": {
            "score": textstat.sentence_count(test_data),
            "description": "The number of sentences in the text."
        },
        "Character Count": {
            "score": textstat.char_count(test_data),
            "description": "The number of characters in the text."
        },
        "Letter Count (without punctuation)": {
            "score": textstat.letter_count(test_data),
            "description": "The number of letters without punctuation."
        },
        "Polysyllable Count": {
            "score": textstat.polysyllabcount(test_data),
            "description": "The number of polysyllabic words in the text."
        },
        "Monosyllable Count": {
            "score": textstat.monosyllabcount(test_data),
            "description": "The number of monosyllabic words in the text."
        }
    }


text_input = st.text_area("Paste your text here:", height=200)

if st.button("Analyze!"):
    with st.spinner("Analyzing your text..."):
        test_data = text_input
        if not test_data.strip():
            st.error("Please enter text to analyze.")
        else:
            results = analyze_text(test_data)

            st.subheader("Readability Scores:")
            st.write("---")
            for metric, data in results.items():
                st.markdown(f"**{metric}:** {data['score']}")
                st.markdown(f"* **What It Means:** {data['description']}")
                if 'tips' in data:
                    st.markdown("* **Actionable Tips:**")
                    for tip in data['tips']:
                        st.markdown(f"    * {tip}")
                st.write("  ")

            st.subheader("Key Takeaways:")
            st.write("---")
            st.markdown("""
                * **Don't Be Afraid to Simplify!** Often, simpler language makes content more impactful and easier to digest.
                * **Aim for a Reading Level Appropriate for Your Audience:** Consider the education level, background, and familiarity of your readers.
                * **Use Short Sentences:** This makes your content more scannable and easier to read.
                * **Write for Everyone:** Accessibility should always be a priority. When in doubt, aim for clear, concise language!
            """)

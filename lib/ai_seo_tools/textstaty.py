import textstat
import streamlit as st

st.set_page_config(layout="wide", page_title="Text Readability Analyzer", page_icon=":book:")

st.title("📖  Text Readability Analyzer:  Making Your Content Easy to Read")

st.write("""
    This tool is your guide to writing content that's easy for your audience to understand.
    Just paste in a sample of your text, and we'll break down the readability scores and offer actionable tips! 
""")

text_input = st.text_area("Paste your text here:", height=200)

if st.button("Analyze!"):
    with st.spinner("Analyzing your text..."):
        test_data = text_input

        st.subheader("Readability Scores:")
        st.write("---")

        # 1. Flesch Reading Ease
        flesch_ease = textstat.flesch_reading_ease(test_data)
        st.markdown(f"**Flesch Reading Ease:** {flesch_ease}")
        st.markdown(""" 
            * **What It Means:**  This score rates your text on a scale of 0-100, with higher scores being easier to read. Imagine a scale from "super confusing" (low scores) to "super easy" (high scores). 
            * **Actionable Tips:**
                * **Score below 30?**  It might be time to simplify. Break down complex sentences, use shorter words, and avoid jargon. 
                * **Score around 60-70?**  You're in the "standard" range.  
                * **Score over 90?**  Your text is very easy to read. But if you want to add some complexity or sophistication, try adding some longer sentences or slightly more complex vocabulary.
        """)

        st.write("  ")

        # 2. Flesch-Kincaid Grade Level
        flesch_kincaid = textstat.flesch_kincaid_grade(test_data)
        st.markdown(f"**Flesch-Kincaid Grade Level:** {flesch_kincaid:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula estimates the US school grade level needed to understand your text.  For example, a score of 7.2 means a 7th-grader should be able to understand it.
            * **Actionable Tips:**
                * **High Score?**   If the grade level is much higher than your target audience's expected level, your writing might be too complex.  
                * **Low Score?**  If the score is significantly lower, your audience might find the text too simple.   
                * **Match Your Audience:**  Remember to tailor the complexity to your readers!  
        """)

        st.write("  ")

        # 3. SMOG Index
        smog_index = textstat.smog_index(test_data)
        st.markdown(f"**SMOG Index:** {smog_index:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula measures how complex your text is by looking at the number of long words and sentences. 
            * **Actionable Tips:**
                * **Important Note:** This formula works best for texts with at least 30 sentences.
                * **Adjust Complexity:**  SMOG helps you determine whether your writing is appropriate for your target audience.  
        """)

        st.write("  ")

        # 4. Coleman-Liau Index
        coleman_liau = textstat.coleman_liau_index(test_data)
        st.markdown(f"**Coleman-Liau Index:** {coleman_liau:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula uses a more advanced method of analyzing sentence length and the number of syllables per word to estimate the reading level. 
        """)

        st.write("  ")

        # 5. Automated Readability Index (ARI)
        ari = textstat.automated_readability_index(test_data)
        st.markdown(f"**Automated Readability Index (ARI):** {ari:.1f}")
        st.markdown(""" 
            * **What It Means:**  Similar to other readability scores, the ARI estimates the grade level required to comprehend your text. 
        """)

        st.write("  ")

        # 6. Dale-Chall Readability Score
        dale_chall = textstat.dale_chall_readability_score(test_data)
        st.markdown(f"**Dale-Chall Readability Score:** {dale_chall:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula focuses on the number of uncommon words (not on a list of 3000 common words) and sentence length. 
            * **Actionable Tips:**
                * **Easy to Understand:**   Aim for a score around the reading level of your audience. If you're writing for a general audience, a score between 6 and 8 is usually considered good.
                * **High School Level?**   Scores between 9 and 12 usually indicate a high school reading level. 
                * **Beyond High School?**   Scores above 12 are usually for a college-level audience.
        """)

        st.write("  ")

        # 7. Gunning Fog
        gunning_fog = textstat.gunning_fog(test_data)
        st.markdown(f"**Gunning Fog:** {gunning_fog:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula calculates the grade level required to understand the text.
        """)

        st.write("  ")

        # 8. Linsear Write Formula 
        linsear = textstat.linsear_write_formula(test_data)
        st.markdown(f"**Linsear Write Formula:** {linsear:.1f}")
        st.markdown(""" 
            * **What It Means:**  This formula aims to estimate the US grade level needed to understand the text. 
        """)

        st.write("  ")

        # 9. Text Standard (Consensus)
        text_standard = textstat.text_standard(test_data)
        st.markdown(f"**Text Standard (Consensus):** {text_standard}")
        st.markdown(""" 
            * **What It Means:** This score is a consensus estimate of the US grade level needed to understand your text. It's an average of all the readability scores. 
        """)

        st.write("  ")

        # 10.  Spache Readability 
        spache = textstat.spache_readability(test_data)
        st.markdown(f"**Spache Readability:** {spache:.1f}")
        st.markdown(""" 
            * **What It Means:** This formula is best for analyzing text for children,  typically up to grade 4.  It considers the number of unfamiliar words and the length of sentences. 
        """)

        st.write("  ")

        # 11. McAlpine EFLAW
        mcalpine = textstat.mcalpine_eflaw(test_data)
        st.markdown(f"**McAlpine EFLAW:** {mcalpine:.1f}")
        st.markdown(""" 
            * **What It Means:**  This formula specifically evaluates text for foreign language learners (typically focusing on English).  It looks at "miniwords" and sentence length.
            * **Target Score:**  Try to aim for a score of 25 or less. 
        """)

        st.write("  ")
  
        #  ---  Spanish Readability Formulas  (For Examples, replace 'test_data' with your Spanish text)---

        # 12.  Fernandez-Huerta
        # fernandez_huerta = textstat.fernandez_huerta(test_data)
        # st.markdown(f"**Fernandez-Huerta (Spanish):** {fernandez_huerta:.1f}")
        # st.markdown(""" 
        #     * **Meaning:**  This is an adaptation of the Flesch Reading Ease formula specifically for Spanish.
        #     * **Interpretation:** Higher scores mean easier readability.
        # """)

        # st.write("  ")

        # 13. Szigriszt-Pazs (Spanish)
        # szigriszt_pazos = textstat.szigriszt_pazos(test_data)
        # st.markdown(f"**Szigriszt-Pazs (Spanish):** {szigriszt_pazos:.1f}")
        # st.markdown(""" 
        #     * **Meaning:**  Another adaptation of the Flesch Reading Ease for Spanish text. It tries to measure the text's understandability. 
        # """)

        # st.write("  ")

        # 14.  Gutierrez-Polini (Spanish)
        # gutierrez_polini = textstat.gutierrez_polini(test_data)
        # st.markdown(f"**Gutierrez-Polini (Spanish):** {gutierrez_polini:.1f}")
        # st.markdown(""" 
        #     * **Meaning:** Designed specifically for Spanish grade-school texts.
        #     * **Note:** The score may be unreliable for more complex text.
        # """)

        # st.write("  ")

        # 15. Crawford (Spanish) 
        # crawford = textstat.crawford(test_data)
        # st.markdown(f"**Crawford (Spanish):** {crawford:.1f}")
        # st.markdown(""" 
        #     * **Meaning:**  This formula estimates the number of years of schooling needed to understand the text, primarily for elementary school-level Spanish.
        # """)

        # st.write("  ")

        #  ---  Arabic Readability Formula  (For Examples, replace 'test_data' with your Arabic text) ---

        # 16.  Osman
        # osman = textstat.osman(test_data)
        # st.markdown(f"**Osman (Arabic):** {osman:.1f}")
        # st.markdown(""" 
        #     * **Meaning:** Designed for Arabic texts. An adaptation of Flesch and Fog formulas.
        # """)

        # st.write("  ")

        # --- Italian Readability Formula ---

        # 17.  Gulpease Index 
        # gulpease = textstat.gulpease_index(test_data)
        # st.markdown(f"**Gulpease Index (Italian):** {gulpease:.1f}")
        # st.markdown(""" 
        #     * **Meaning:**  Measures the readability of Italian text.
        #     * **Interpretation:** Lower scores require a higher level of education for ease of reading. 
        # """)

        # st.write("  ") 

        # ---  German Readability Formula (For Examples, replace 'test_data' with your German text) ---

        # 18. Wiener Sachtextformel
        # wiener_sachtextformel = textstat.wiener_sachtextformel(test_data)
        # st.markdown(f"**Wiener Sachtextformel (German):** {wiener_sachtextformel:.1f}")
        # st.markdown(""" 
        #     * **Meaning:** This formula measures the readability of German texts.
        #     * **Interpretation:**
        #         *  4:  Very easy text 
        #         * 15:  Very difficult text 
        # """)

        # st.write("  ") 

        st.subheader("Additional Insights:")
        st.write("---")
        
        #  19. Reading Time
        reading_time = textstat.reading_time(test_data) 
        st.markdown(f"**Estimated Reading Time:** {reading_time:.1f} minutes")

        st.write("  ")

        # 20. Syllable Count 
        syllable_count = textstat.syllable_count(test_data) 
        st.markdown(f"**Syllable Count:** {syllable_count}")

        st.write("  ")

        # 21. Lexicon Count (Word Count)
        lexicon_count = textstat.lexicon_count(test_data)
        st.markdown(f"**Word Count:** {lexicon_count}")

        st.write("  ") 

        # 22.  Sentence Count 
        sentence_count = textstat.sentence_count(test_data)
        st.markdown(f"**Sentence Count:** {sentence_count}") 

        st.write("  ")

        # 23.  Character Count
        char_count = textstat.char_count(test_data) 
        st.markdown(f"**Character Count:** {char_count}")

        st.write("  ") 

        # 24.  Letter Count 
        letter_count = textstat.letter_count(test_data)
        st.markdown(f"**Letter Count (without punctuation):** {letter_count}")

        st.write("  ") 

        # 25.  Polysyllable Count 
        polysyllable_count = textstat.polysyllabcount(test_data)
        st.markdown(f"**Polysyllable Count:** {polysyllable_count}")

        st.write("  ") 

        # 26. Monosyllable Count
        monosyllable_count = textstat.monosyllabcount(test_data)
        st.markdown(f"**Monosyllable Count:** {monosyllable_count}")

        st.write("  ")

        st.subheader("Key Takeaways:")
        st.write("---")
        st.markdown("""
        *  **Don't Be Afraid to Simplify!**  Often, simpler language makes content more impactful and easier to digest. 
        *  **Aim for a Reading Level Appropriate for Your Audience:** Consider the education level, background, and familiarity of your readers.
        *  **Use Short Sentences:** This makes your content more scannable and easier to read.
        *  **Write for Everyone:** Accessibility should always be a priority. When in doubt, aim for clear, concise language! 
        """)

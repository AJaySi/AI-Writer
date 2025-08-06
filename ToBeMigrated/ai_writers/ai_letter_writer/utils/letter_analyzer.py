"""
Letter Analyzer Utility

This module provides functions for analyzing letter content, including tone,
formality, readability, and offering basic suggestions for improvement.
Note: The analysis methods provided here are simplified rule-based and
keyword-based approaches. For more sophisticated analysis in a production
environment, consider using advanced Natural Language Processing (NLP)
libraries and models.
"""

import re
from typing import Dict, Any, Tuple, List

def analyze_letter_tone(content: str) -> Dict[str, float]:
    """
    Analyze the tone of a letter based on the presence of specific keywords
    and phrases.

    Args:
        content: The letter content to analyze.

    Returns:
        Dictionary with tone scores (formal, friendly, assertive, etc.).
        Scores are based on the frequency of matching patterns and capped at 1.0.
    """
    # This is a simplified version using keyword matching.
    # A more sophisticated approach would involve NLP libraries for sentiment and tone analysis.

    # Initialize tone scores
    # Scores are arbitrary counts normalized in a simple way
    tone_scores = {
        "formal": 0.0,
        "friendly": 0.0,
        "assertive": 0.0,
        "respectful": 0.0,
        "urgent": 0.0,
        "apologetic": 0.0
    }

    # Define patterns for different tones (case-insensitive)
    formal_patterns = [
        r"\bI am writing to\b",
        r"\bI would like to\b",
        r"\bplease find\b",
        r"\bregarding\b",
        r"\bpursuant to\b",
        r"\bhereby\b",
        r"\bthus\b",
        r"\btherefore\b",
        r"\bfurthermore\b",
        r"\bconsequently\b",
        r"\bnevertheless\b",
        r"\bmoreover\b",
        r"\benclosed\b", # Added common formal word
        r"\bherewith\b" # Added common formal word
    ]

    friendly_patterns = [
        r"\bhope you're well\b",
        r"\bhope this finds you well\b",
        r"\bgreat to hear\b",
        r"\blooking forward\b",
        r"\bthanks\b",
        r"\bappreciate\b",
        r"!", # Exclamation points often indicate friendly or excited tone
        r"\bexcited\b",
        r"\bgreat\b", # Common friendly adjective
        r"\bnice\b" # Common friendly adjective
    ]

    assertive_patterns = [
        r"\brequire\b",
        r"\bmust\b",
        r"\bneed\b",
        r"\bexpect\b",
        r"\bdemand\b",
        r"\binsist\b",
        r"\bimmediately\b",
        r"\baction\b", # Often used in assertive contexts
        r"\bresolution\b" # Can imply assertion
    ]

    respectful_patterns = [
        r"\brespectfully\b",
        r"\bhonored\b",
        r"\bplease\b",
        r"\bkindly\b",
        r"\bgrateful\b",
        r"\bthank you\b",
        r"\bappreciate\b",
        r"\bhumbly\b", # Added respectful word
        r"\bapologies\b" # Can show respect for impact
    ]

    urgent_patterns = [
        r"\burgent\b",
        r"\bas soon as possible\b",
        r"\bASAP\b",
        r"\bimmediately\b",
        r"\bpressing\b",
        r"\bcritical\b",
        r"\bdeadline\b",
        r"\bexpedite\b", # Added urgent word
        r"\bpromptly\b" # Added urgent word
    ]

    apologetic_patterns = [
        r"\bapologize\b",
        r"\bsorry\b",
        r"\bregret\b",
        r"\bmistake\b",
        r"\berror\b",
        r"\binconvenience\b",
        r"\bfault\b", # Added apologetic word
        r"\boversight\b" # Added apologetic word
    ]

    # Count pattern matches and update scores (arbitrary weighting)
    # A simple count multiplied by a factor acts as a basic indicator
    for pattern in formal_patterns:
        tone_scores["formal"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    for pattern in friendly_patterns:
        tone_scores["friendly"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    for pattern in assertive_patterns:
        tone_scores["assertive"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    for pattern in respectful_patterns:
        tone_scores["respectful"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    for pattern in urgent_patterns:
        tone_scores["urgent"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    for pattern in apologetic_patterns:
        tone_scores["apologetic"] += len(re.findall(pattern, content, re.IGNORECASE)) * 0.2

    # Cap scores at 1.0 (arbitrary capping)
    # A more meaningful score might be relative frequency or use a proper model
    for tone in tone_scores:
        tone_scores[tone] = min(tone_scores[tone], 1.0)

    return tone_scores

def check_formality(content: str) -> float:
    """
    Check the formality level of a letter based on the presence of formal
    vs. informal indicators and contractions.

    Args:
        content: The letter content to analyze.

    Returns:
        Formality score between 0.0 (very informal) and 1.0 (very formal).
        Calculated as formal_count / (formal_count + informal_count).
    """
    # This is a simplified version based on keyword counting.
    # More accurate formality analysis would require advanced NLP techniques.

    # Define formal and informal indicators (case-insensitive)
    formal_indicators = [
        r"\bDear\b",
        r"\bSincerely\b",
        r"\bRegards\b",
        r"\bRespectfully\b",
        r"\bI am writing to\b",
        r"\bI would like to\b",
        r"\bplease find\b",
        r"\bregarding\b",
        r"\bpursuant to\b",
        r"\bhereby\b",
        r"\bthus\b",
        r"\btherefore\b",
        r"\bfurthermore\b",
        r"\bconsequently\b",
        r"\bnevertheless\b",
        r"\bmoreover\b",
        r"\benclosed\b",
        r"\bherewith\b",
        r"\bsincerely yours\b", # Added
        r"\bto whom it may concern\b" # Added
    ]

    informal_indicators = [
        r"\bHey\b",
        r"\bHi\b",
        r"\bWhat's up\b",
        r"\bCheers\b",
        r"\bThanks\b", # 'Thank you' is formal, 'Thanks' is informal
        r"\bTake care\b",
        r"\bSee you\b",
        r"\bLater\b",
        r"\bBye\b",
        r"\bLove\b", # As a closing
        r"\bXO\b",
        r"!+", # Multiple exclamation points
        r"\bawesome\b",
        r"\bcool\b",
        r"\bgreat\b",
        r"\bnice\b",
        r"\bbtw\b", # By the way
        r"\bimo\b", # In my opinion
        r"\blol\b" # Laugh out loud
    ]

    # Define common contractions (case-insensitive)
    contractions = [
        r"\bdon't\b", r"\bcan't\b", r"\bwon't\b", r"\bshouldn't\b",
        r"\bcouldn't\b", r"\bwouldn't\b", r"\bhasn't\b", r"\bhaven't\b",
        r"\bisn't\b", r"\baren't\b", r"\bwasn't\b", r"\bweren't\b",
        r"\bi'm\b", r"\byou're\b", r"\bhe's\b", r"\bshe's\b", r"\bit's\b",
        r"\bwe're\b", r"\bthey're\b", r"\bi've\b", r"\byou've\b",
        r"\bwe've\b", r"\bthey've\b", r"\bi'd\b", r"\byou'd\b",
        r"\bhe'd\b", r"\bshe'd\b", r"\bit'd\b", r"\bwe'd\b", r"\bthey'd\b",
        r"\bi'll\b", r"\byou'll\b", r"\bhe'll\b", r"\bshe'll\b", r"\bit'll\b",
        r"\bwe'll\b", r"\bthey'll\b"
    ]

    formal_count = 0
    for pattern in formal_indicators:
        formal_count += len(re.findall(pattern, content, re.IGNORECASE))

    informal_count = 0
    for pattern in informal_indicators:
        informal_count += len(re.findall(pattern, content, re.IGNORECASE))

    # Count contractions as informal indicators
    for pattern in contractions:
        informal_count += len(re.findall(pattern, content, re.IGNORECASE))

    # Calculate formality score
    total_indicators = formal_count + informal_count
    if total_indicators == 0:
        # If no indicators found, return a neutral score
        return 0.5

    # Score is the proportion of formal indicators
    formality_score = formal_count / total_indicators
    return formality_score

def count_syllables_simple(word: str) -> int:
    """
    Counts syllables in a word using a simplified heuristic.
    This method is not linguistically perfect but provides a basic estimate
    for readability formulas.

    Args:
        word: The word string.

    Returns:
        Estimated syllable count.
    """
    word = word.lower()
    if len(word) <= 3:
        # Assume short words have one syllable
        return 1

    # Remove common silent endings like 'e', 'es', 'ed'
    if word.endswith(('es', 'ed')):
        word = word[:-2]
    elif word.endswith('e'):
        word = word[:-1]

    # Count vowel groups (consecutive vowels count as one syllable)
    vowels = 'aeiouy'
    count = 0
    prev_is_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    # Ensure at least one syllable is counted
    return max(1, count)


def get_readability_metrics(content: str) -> Dict[str, Any]:
    """
    Calculate readability metrics for a letter using simplified methods
    like Flesch Reading Ease.

    Args:
        content: The letter content to analyze.

    Returns:
        Dictionary with readability metrics: word_count, sentence_count,
        avg_words_per_sentence, flesch_reading_ease, reading_level.
    """
    # Split content into words and sentences using simple regex
    words = re.findall(r'\b\w+\b', content)
    # Split by common sentence terminators, handling potential multiple marks
    sentences = re.split(r'[.!?]+\s*', content)
    # Filter out empty strings resulting from the split (e.g., trailing punctuation)
    sentences = [s for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    syllable_count = sum(count_syllables_simple(word) for word in words)

    if word_count == 0 or sentence_count == 0:
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_words_per_sentence": 0.0,
            "flesch_reading_ease": 0.0,
            "reading_level": "N/A"
        }

    # Calculate average words per sentence
    avg_words_per_sentence = word_count / sentence_count

    # Calculate Flesch Reading Ease Score
    # Formula: 206.835 - (1.015 * AvgWordsPerSentence) - (84.6 * AvgSyllablesPerWord)
    # AvgSyllablesPerWord = syllable_count / word_count
    avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0

    flesch = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    # Clamp score between 0 and 100
    flesch = max(0.0, min(100.0, flesch))

    # Determine reading level based on Flesch score ranges
    if flesch >= 90:
        reading_level = "Very Easy (5th grade)"
    elif flesch >= 80:
        reading_level = "Easy (6th grade)"
    elif flesch >= 70:
        reading_level = "Fairly Easy (7th grade)"
    elif flesch >= 60:
        reading_level = "Standard (8th-9th grade)"
    elif flesch >= 50:
        reading_level = "Fairly Difficult (10th-12th grade)"
    elif flesch >= 30:
        reading_level = "Difficult (College)"
    else:
        reading_level = "Very Difficult (Graduate)"

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_words_per_sentence": round(avg_words_per_sentence, 2), # Rounded for display
        "flesch_reading_ease": round(flesch, 2), # Rounded for display
        "reading_level": reading_level
    }

def suggest_improvements(content: str, letter_type: str) -> List[str]:
    """
    Suggest improvements for a letter based on its content, basic analysis,
    and target letter type.

    Args:
        content: The letter content to analyze.
        letter_type: The type of letter (e.g., "business", "cover", "personal").

    Returns:
        List of improvement suggestions strings.
    """
    suggestions = []

    words = re.findall(r'\b\w+\b', content)
    word_count = len(words)

    # Basic length check based on letter type
    if letter_type in ["business", "formal"]:
        if word_count < 100 and word_count > 10: # Avoid suggesting for very short placeholders
            suggestions.append("Consider adding more details to make your letter more comprehensive.")
        elif word_count > 600: # Increased max length slightly
            suggestions.append("Your letter is quite long. Consider condensing it for better readability and focus.")
    elif letter_type == "cover":
        if word_count < 150 and word_count > 10: # Avoid suggesting for very short placeholders
            suggestions.append("Your cover letter may be too brief. Consider highlighting more of your relevant qualifications.")
        elif word_count > 500: # Increased max length slightly
            suggestions.append("Your cover letter is quite long. Consider focusing on your most relevant qualifications and experiences.")
    elif letter_type == "recommendation":
         if word_count < 150 and word_count > 10:
            suggestions.append("Consider adding more specific examples or anecdotes to strengthen the recommendation.")
         elif word_count > 600:
            suggestions.append("Your recommendation letter is quite long. Ensure it remains focused and impactful.")


    # Check for overuse of "I" (simple count-based heuristic)
    # Count "I" as a standalone word
    i_count = len(re.findall(r"\bI\b", content))
    # Avoid suggestion for very short content or content with few sentences
    sentence_count = len(re.split(r'[.!?]+\s*', content.strip()))
    if sentence_count > 2 and word_count > 50 and i_count > sentence_count * 1.5: # Suggest if 'I' count is significantly higher than sentence count
         suggestions.append("Your letter contains many uses of 'I'. Consider rephrasing some sentences to focus more on the recipient or the subject matter.")


    # Check for expression of gratitude (using common phrases)
    gratitude_patterns = [r"\bthank you\b", r"\bgrateful\b", r"\bappreciate\b"]
    has_gratitude = any(re.search(pattern, content, re.IGNORECASE) for pattern in gratitude_patterns)
    # Suggest adding gratitude, but avoid for letter types where it might be less common (e.g., some complaint letters)
    if not has_gratitude and letter_type not in ["complaint", "urgent"]:
        suggestions.append("Consider expressing gratitude or appreciation somewhere in your letter.")

    # Check for clear call to action (using common phrases)
    # Phrases indicating desired action or next step
    action_phrases = [
        "look forward to", "please", "would appreciate", "request",
        "hope to", "call me", "email me", "contact me", "schedule",
        "arrange", "require action", "next steps"
    ]
    has_call_to_action = any(phrase in content.lower() for phrase in action_phrases)
    # Suggest adding a call to action for relevant letter types
    if not has_call_to_action and letter_type in ["business", "cover", "complaint", "invitation"]:
        suggestions.append("Consider adding a clear call to action or outlining the desired next steps.")

    # Check for proper closing (using common phrases)
    closing_patterns = [
        r"\bSincerely\b", r"\bRegards\b", r"\bThank you\b", r"\bBest regards\b",
        r"\bYours sincerely\b", r"\bYours faithfully\b", r"\bRespectfully\b",
        r"\bBest wishes\b", r"\bKind regards\b"
    ]
    # Check if any standard closing phrase is present, typically near the end
    # A more robust check might look specifically at the last paragraph/lines
    has_proper_closing = any(re.search(pattern, content[-200:], re.IGNORECASE) for pattern in closing_patterns) # Check last 200 chars

    if not has_proper_closing and word_count > 20: # Avoid suggesting for very short snippets
        suggestions.append("Consider adding a proper closing phrase (e.g., Sincerely, Regards) followed by your name.")

    return suggestions

# Example usage (for testing purposes, not part of the module's core functionality)
if __name__ == '__main__':
    sample_formal_letter = """
    Dear Mr. Smith,

    I am writing to follow up regarding the project proposal submitted on October 26, 2023.
    We believe the proposed solution aligns well with your stated requirements.
    Please find the revised budget document attached for your review.
    We look forward to your feedback at your earliest convenience.

    Sincerely,
    Jane Doe
    """

    sample_informal_letter = """
    Hey John,

    Hope you're doing well! Just wanted to quickly touch base about the party next week.
    Excited to catch up with everyone! Let me know if you need any help setting up.
    Thanks!

    Best,
    Alex
    """

    sample_complaint_letter = """
    To Whom It May Concern,

    I am writing to complain about the faulty product I received on November 1, 2023 (Order #12345).
    The device stopped working after only two days of use. I require a full refund or replacement immediately.
    I expect a prompt response regarding this issue.

    Sincerely,
    Concerned Customer
    """

    print("--- Analyzing Formal Letter ---")
    tone = analyze_letter_tone(sample_formal_letter)
    formality = check_formality(sample_formal_letter)
    readability = get_readability_metrics(sample_formal_letter)
    suggestions = suggest_improvements(sample_formal_letter, "business")

    print(f"Tone: {tone}")
    print(f"Formality: {formality:.2f}")
    print(f"Readability: {readability}")
    print(f"Suggestions: {suggestions}")

    print("\n--- Analyzing Informal Letter ---")
    tone = analyze_letter_tone(sample_informal_letter)
    formality = check_formality(sample_informal_letter)
    readability = get_readability_metrics(sample_informal_letter)
    suggestions = suggest_improvements(sample_informal_letter, "personal")

    print(f"Tone: {tone}")
    print(f"Formality: {formality:.2f}")
    print(f"Readability: {readability}")
    print(f"Suggestions: {suggestions}")

    print("\n--- Analyzing Complaint Letter ---")
    tone = analyze_letter_tone(sample_complaint_letter)
    formality = check_formality(sample_complaint_letter)
    readability = get_readability_metrics(sample_complaint_letter)
    suggestions = suggest_improvements(sample_complaint_letter, "complaint")

    print(f"Tone: {tone}")
    print(f"Formality: {formality:.2f}")
    print(f"Readability: {readability}")
    print(f"Suggestions: {suggestions}")
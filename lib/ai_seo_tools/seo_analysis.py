from typing import List, Dict, Union
#from nltk import tokenize, stem, pos_tag
from textblob import TextBlob
import enchant

class TextPreprocessor:
    def preprocess_text(self, text: str) -> str:
        # Tokenize the text
        tokens = tokenize.word_tokenize(text)
        
        # Stem the tokens
        stemmer = stem.PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        
        # Join the stemmed tokens back into a string
        preprocessed_text = ' '.join(stemmed_tokens)
        
        return preprocessed_text

class SEOAnalyzer:
    def calculate_seo_percentage(self, text: str, keywords: List[str]) -> float:
        # Calculate the keyword density
        keyword_density = self.calculate_keyword_density(text, keywords)
        
        # Calculate the readability score
        readability_score = self.calculate_readability_score(text)
        
        # Perform semantic analysis
        semantic_score = self.perform_semantic_analysis(text)
        
        # Calculate the SEO percentage based on the metrics
        seo_percentage = (keyword_density + readability_score + semantic_score) / 3
        
        return seo_percentage
    
    def calculate_keyword_density(self, text: str, keywords: List[str]) -> float:
        # Count the number of occurrences of each keyword in the text
        keyword_counts = {keyword: text.lower().count(keyword.lower()) for keyword in keywords}
        
        # Calculate the total number of words in the text
        word_count = len(tokenize.word_tokenize(text))
        
        # Calculate the keyword density
        keyword_density = sum(keyword_counts.values()) / word_count
        
        return keyword_density
    
    def calculate_readability_score(self, text: str) -> float:
        # Calculate the average number of words per sentence
        sentences = tokenize.sent_tokenize(text)
        word_count = sum(len(tokenize.word_tokenize(sentence)) for sentence in sentences)
        sentence_count = len(sentences)
        average_words_per_sentence = word_count / sentence_count
        
        # Calculate the readability score
        readability_score = 1 / average_words_per_sentence
        
        return readability_score
    
    def perform_semantic_analysis(self, text: str) -> float:
        # Perform part-of-speech tagging on the text
        tagged_text = pos_tag(tokenize.word_tokenize(text))
        
        # Calculate the semantic score based on the number of nouns and verbs
        noun_count = sum(1 for word, pos in tagged_text if pos.startswith('N'))
        verb_count = sum(1 for word, pos in tagged_text if pos.startswith('V'))
        semantic_score = (noun_count + verb_count) / len(tagged_text)
        
        return semantic_score

class SpellChecker:
    def check_spelling(self, text: str) -> List[str]:
        # Create a spellchecker object
        spellchecker = enchant.Dict("en_US")
        
        # Tokenize the text
        tokens = tokenize.word_tokenize(text)
        
        # Check the spelling of each token
        misspelled_words = [token for token in tokens if not spellchecker.check(token)]
        
        return misspelled_words

class SEOAnalysisModule:
    def __init__(self):
        self.text_preprocessor = TextPreprocessor()
        self.seo_analyzer = SEOAnalyzer()
        self.spell_checker = SpellChecker()
    
    def analyze_text(self, text: str, keywords: List[str]) -> Dict[str, Union[float, List[str]]]:
        # Preprocess the text
        preprocessed_text = self.text_preprocessor.preprocess_text(text)
        
        # Calculate the SEO percentage
        seo_percentage = self.seo_analyzer.calculate_seo_percentage(preprocessed_text, keywords)
        
        # Calculate the keyword density
        keyword_density = self.seo_analyzer.calculate_keyword_density(preprocessed_text, keywords)
        
        # Calculate the readability score
        readability_score = self.seo_analyzer.calculate_readability_score(preprocessed_text)
        
        # Perform semantic analysis
        semantic_score = self.seo_analyzer.perform_semantic_analysis(preprocessed_text)
        
        # Check the spelling
        spelling_errors = self.spell_checker.check_spelling(preprocessed_text)
        
        return {
            'seo_percentage': seo_percentage,
            'keyword_density': keyword_density,
            'readability_score': readability_score,
            'semantic_score': semantic_score,
            'spelling_errors': spelling_errors
        }

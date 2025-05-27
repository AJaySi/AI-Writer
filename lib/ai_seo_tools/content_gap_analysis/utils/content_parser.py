"""
Content parser utility for analyzing website content structure.
"""

from typing import Dict, Any, List
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

class ContentParser:
    """Parser for analyzing website content structure."""
    
    def __init__(self):
        """Initialize the content parser."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def parse_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and analyze the structure of website content.
        
        Args:
            content: Dictionary containing website content
            
        Returns:
            Dictionary containing parsed content structure
        """
        try:
            # Parse main content
            main_content = content.get('main_content', '')
            soup = BeautifulSoup(content.get('html', ''), 'html.parser')
            
            # Extract text statistics
            text_stats = self._analyze_text(main_content)
            
            # Extract content sections
            sections = self._extract_sections(soup)
            
            # Extract topics
            topics = self._extract_topics(main_content)
            
            # Analyze readability
            readability = self._analyze_readability(main_content)
            
            # Analyze content hierarchy
            hierarchy = self._analyze_hierarchy(content.get('headings', []))
            
            return {
                'text_statistics': text_stats,
                'sections': sections,
                'topics': topics,
                'readability': readability,
                'hierarchy': hierarchy,
                'metadata': content.get('metadata', {})
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'text_statistics': {},
                'sections': [],
                'topics': [],
                'readability': {},
                'hierarchy': {},
                'metadata': {}
            }
    
    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text statistics."""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'average_sentence_length': len(words) / max(len(sentences), 1),
            'unique_words': len(set(words)),
            'stop_words': len([w for w in word_tokenize(text.lower()) if w in self.stop_words]),
            'characters': len(text),
            'paragraphs': len(text.split('\n\n')),
            'sentences': sentences
        }
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract content sections."""
        sections = []
        
        # Find main content containers
        containers = soup.find_all(['article', 'section', 'div'], class_=re.compile(r'content|main|article|section'))
        
        for container in containers:
            # Get section heading
            heading = container.find(['h1', 'h2', 'h3'])
            heading_text = heading.get_text().strip() if heading else 'Untitled Section'
            
            # Get section content
            content = container.get_text().strip()
            
            # Get section type
            section_type = container.name
            if container.get('class'):
                section_type = ' '.join(container.get('class'))
            
            sections.append({
                'heading': heading_text,
                'content': content,
                'type': section_type,
                'word_count': len(word_tokenize(content)),
                'position': self._get_element_position(container)
            })
        
        return sections
    
    def _extract_topics(self, text: str) -> List[Dict[str, Any]]:
        """Extract main topics from content."""
        # Tokenize and clean text
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        # Get word frequencies
        word_freq = Counter(words)
        
        # Get top topics
        topics = []
        for word, freq in word_freq.most_common(10):
            topics.append({
                'topic': word,
                'frequency': freq,
                'percentage': freq / len(words) * 100
            })
        
        return topics
    
    def _analyze_readability(self, text: str) -> Dict[str, float]:
        """Analyze text readability."""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum()]
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # Calculate average word length
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        
        # Calculate Flesch Reading Ease score
        # Formula: 206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)
        syllables = sum(self._count_syllables(w) for w in words)
        flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * (syllables / max(len(words), 1))
        
        return {
            'flesch_score': max(0, min(100, flesch_score)),
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'syllables_per_word': syllables / max(len(words), 1)
        }
    
    def _analyze_hierarchy(self, headings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content hierarchy."""
        # Group headings by level
        heading_levels = {}
        for heading in headings:
            level = heading['level']
            if level not in heading_levels:
                heading_levels[level] = []
            heading_levels[level].append(heading)
        
        # Calculate hierarchy metrics
        total_headings = len(headings)
        max_depth = max(int(level[1]) for level in heading_levels.keys()) if heading_levels else 0
        
        return {
            'total_headings': total_headings,
            'max_depth': max_depth,
            'heading_distribution': {level: len(headings) for level, headings in heading_levels.items()},
            'has_proper_hierarchy': self._check_proper_hierarchy(heading_levels)
        }
    
    def _check_proper_hierarchy(self, heading_levels: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Check if headings follow proper hierarchy."""
        if not heading_levels:
            return False
        
        # Check if h1 exists
        if 'h1' not in heading_levels:
            return False
        
        # Check if h1 is unique
        if len(heading_levels['h1']) > 1:
            return False
        
        # Check if levels are sequential
        levels = sorted(int(level[1]) for level in heading_levels.keys())
        return all(levels[i] - levels[i-1] <= 1 for i in range(1, len(levels)))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word."""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        word = word.lower()
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count += 1
        return count
    
    def _get_element_position(self, element) -> Dict[str, int]:
        """Get element position in the document."""
        try:
            return {
                'top': element.sourceline,
                'left': element.sourcepos
            }
        except:
            return {
                'top': 0,
                'left': 0
            } 
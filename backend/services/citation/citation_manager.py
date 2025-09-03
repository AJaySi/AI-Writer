"""
Citation Manager Service for ALwrity

This service handles citation management for grounded content generation,
ensuring proper source attribution and citation validation.

Key Features:
- Inline citation formatting and management
- Citation validation and coverage analysis
- Source list generation
- Citation pattern recognition
- Quality assessment for citations

Dependencies:
- re (for pattern matching)
- typing (for type hints)
- logging (for debugging)

Author: ALwrity Team
Version: 1.0
Last Updated: January 2025
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from loguru import logger

class CitationManager:
    """
    Service for managing citations in grounded content.
    
    This service handles the creation, validation, and management of citations
    to ensure proper source attribution in generated content.
    """
    
    def __init__(self):
        """Initialize the Citation Manager."""
        # Citation patterns to recognize
        self.citation_patterns = [
            r'\[Source (\d+)\]',           # [Source 1], [Source 2]
            r'\[(\d+)\]',                  # [1], [2]
            r'\(Source (\d+)\)',           # (Source 1), (Source 2)
            r'\((\d+)\)',                  # (1), (2)
            r'Source (\d+)',               # Source 1, Source 2
            r'Ref\. (\d+)',                # Ref. 1, Ref. 2
            r'Reference (\d+)',            # Reference 1, Reference 2
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.citation_patterns]
        
        logger.info("Citation Manager initialized successfully")
    
    def add_citations(
        self, 
        content: str, 
        sources: List[Any], 
        citation_style: str = "brackets"
    ) -> str:
        """
        Add citations to content based on source information.
        
        Args:
            content: The content to add citations to
            sources: List of research sources (can be Dict or ResearchSource objects)
            citation_style: Style of citations to use (brackets, parentheses, inline)
            
        Returns:
            Content with added citations
        """
        if not sources:
            return content
        
        # Citation style templates
        citation_templates = {
            "brackets": "[Source {num}]",
            "parentheses": "(Source {num})",
            "inline": "Source {num}",
            "numbered": "[{num}]"
        }
        
        template = citation_templates.get(citation_style, "[Source {num}]")
        
        # Add source list at the end
        source_list = self.generate_source_list(sources, citation_style)
        
        # For now, we'll add a general citation at the end
        # In a full implementation, you'd use NLP to identify claims and add specific citations
        citation_text = f"\n\n{source_list}"
        
        return content + citation_text
    
    def validate_citations(
        self, 
        content: str, 
        sources: List[Any]
    ) -> Dict[str, Any]:
        """
        Validate citations in content for completeness and accuracy.
        
        Args:
            content: The content with citations
            sources: List of research sources (can be Dict or ResearchSource objects)
            
        Returns:
            Citation validation results and metrics
        """
        validation_result = {
            "total_sources": len(sources),
            "citations_found": 0,
            "citation_coverage": 0.0,
            "citation_quality": 0.0,
            "missing_citations": [],
            "invalid_citations": [],
            "validation_score": 0.0
        }
        
        if not sources:
            validation_result["validation_score"] = 0.0
            return validation_result
        
        # Find all citations in content
        all_citations = []
        for pattern in self.compiled_patterns:
            matches = pattern.findall(content)
            all_citations.extend(matches)
        
        validation_result["citations_found"] = len(all_citations)
        
        # Calculate citation coverage
        validation_result["citation_coverage"] = min(
            len(all_citations) / len(sources), 1.0
        )
        
        # Validate citation references
        valid_citations = []
        invalid_citations = []
        
        for citation in all_citations:
            try:
                citation_num = int(citation)
                if 1 <= citation_num <= len(sources):
                    valid_citations.append(citation_num)
                else:
                    invalid_citations.append(citation_num)
            except ValueError:
                invalid_citations.append(citation)
        
        validation_result["invalid_citations"] = invalid_citations
        
        # Find missing citations
        expected_citations = set(range(1, len(sources) + 1))
        found_citations = set(valid_citations)
        missing_citations = expected_citations - found_citations
        
        validation_result["missing_citations"] = list(missing_citations)
        
        # Calculate citation quality score
        quality_factors = [
            validation_result["citation_coverage"] * 0.4,  # Coverage (40%)
            (1.0 - len(invalid_citations) / max(len(all_citations), 1)) * 0.3,  # Accuracy (30%)
            (1.0 - len(missing_citations) / len(sources)) * 0.3  # Completeness (30%)
        ]
        
        validation_result["citation_quality"] = sum(quality_factors)
        validation_result["validation_score"] = (
            validation_result["citation_coverage"] * 0.6 + 
            validation_result["citation_quality"] * 0.4
        )
        
        # Round scores
        validation_result["citation_coverage"] = round(validation_result["citation_coverage"], 3)
        validation_result["citation_quality"] = round(validation_result["citation_quality"], 3)
        validation_result["validation_score"] = round(validation_result["validation_score"], 3)
        
        return validation_result
    
    def generate_source_list(
        self, 
        sources: List[Any], 
        citation_style: str = "brackets"
    ) -> str:
        """
        Generate a comprehensive list of sources with proper formatting.
        
        Args:
            sources: List of research sources (can be Dict or ResearchSource objects)
            citation_style: Style of citations used in content
            
        Returns:
            Formatted source list
        """
        if not sources:
            return "**Sources:** No sources available."
        
        # Header based on citation style
        headers = {
            "brackets": "**Sources:**",
            "parentheses": "**Sources:**",
            "inline": "**Sources:**",
            "numbered": "**References:**"
        }
        
        header = headers.get(citation_style, "**Sources:**")
        source_list = f"{header}\n\n"
        
        for i, source in enumerate(sources, 1):
            # Handle both Dict and ResearchSource objects
            if hasattr(source, 'title'):
                # ResearchSource Pydantic model
                title = source.title
                url = source.url
                relevance = source.relevance_score or 0
                credibility = source.credibility_score or 0
                source_type = source.source_type or "general"
                publication_date = source.publication_date or ""
            else:
                # Dictionary object
                title = source.get("title", "Untitled")
                url = source.get("url", "")
                relevance = source.get("relevance_score", 0)
                credibility = source.get("credibility_score", 0)
                source_type = source.get("source_type", "general")
                publication_date = source.get("publication_date", "")
            
            # Format the source entry
            source_entry = f"{i}. **{title}**\n"
            
            if url:
                source_entry += f"   - URL: [{url}]({url})\n"
            
            if relevance and relevance > 0:
                source_entry += f"   - Relevance: {relevance:.2f}\n"
            
            if credibility and credibility > 0:
                source_entry += f"   - Credibility: {credibility:.2f}\n"
            
            if source_type and source_type != "general":
                source_entry += f"   - Type: {source_type.replace('_', ' ').title()}\n"
            
            if publication_date:
                source_entry += f"   - Published: {publication_date}\n"
            
            source_list += source_entry + "\n"
        
        return source_list
    
    def extract_citations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract all citations from content with their positions and references.
        
        Args:
            content: The content to extract citations from
            
        Returns:
            List of citation objects with metadata
        """
        citations = []
        
        for pattern in self.compiled_patterns:
            matches = pattern.finditer(content)
            for match in matches:
                citation_text = match.group(0)
                citation_num = match.group(1) if len(match.groups()) > 0 else None
                position = match.start()
                
                citation_obj = {
                    "text": citation_text,
                    "number": citation_num,
                    "position": position,
                    "pattern": pattern.pattern,
                    "line_number": content[:position].count('\n') + 1
                }
                
                citations.append(citation_obj)
        
        # Sort by position
        citations.sort(key=lambda x: x["position"])
        
        return citations
    
    def analyze_citation_patterns(self, content: str) -> Dict[str, Any]:
        """
        Analyze citation patterns in content for insights.
        
        Args:
            content: The content to analyze
            
        Returns:
            Analysis results and pattern insights
        """
        citations = self.extract_citations(content)
        
        analysis = {
            "total_citations": len(citations),
            "citation_patterns": {},
            "distribution": {},
            "quality_indicators": {}
        }
        
        # Analyze citation patterns
        for citation in citations:
            pattern = citation["pattern"]
            if pattern not in analysis["citation_patterns"]:
                analysis["citation_patterns"][pattern] = 0
            analysis["citation_patterns"][pattern] += 1
        
        # Analyze citation distribution
        if citations:
            positions = [c["position"] for c in citations]
            content_length = len(content)
            
            # Distribution by content thirds
            third_length = content_length // 3
            first_third = sum(1 for pos in positions if pos < third_length)
            second_third = sum(1 for pos in positions if third_length <= pos < 2 * third_length)
            third_third = sum(1 for pos in positions if pos >= 2 * third_length)
            
            analysis["distribution"] = {
                "first_third": first_third,
                "second_third": second_third,
                "third_third": third_third,
                "evenly_distributed": abs(first_third - second_third) <= 1 and abs(second_third - third_third) <= 1
            }
        
        # Quality indicators
        analysis["quality_indicators"] = {
            "has_citations": len(citations) > 0,
            "multiple_citations": len(citations) > 1,
            "even_distribution": analysis["distribution"].get("evenly_distributed", False),
            "consistent_pattern": len(analysis["citation_patterns"]) <= 2
        }
        
        return analysis
    
    def suggest_citation_improvements(
        self, 
        content: str, 
        sources: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Suggest improvements for citation usage in content.
        
        Args:
            content: The content to analyze
            sources: List of research sources
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        if not sources:
            suggestions.append("No sources available for citation.")
            return suggestions
        
        # Analyze current citations
        citations = self.extract_citations(content)
        validation = self.validate_citations(content, sources)
        
        # Coverage suggestions
        if validation["citation_coverage"] < 0.5:
            suggestions.append(f"Low citation coverage ({validation['citation_coverage']:.1%}). Consider adding more citations to support factual claims.")
        
        if validation["citation_coverage"] < 0.8:
            suggestions.append("Moderate citation coverage. Aim for at least 80% of sources to be cited.")
        
        # Distribution suggestions
        analysis = self.analyze_citation_patterns(content)
        if not analysis["distribution"].get("evenly_distributed", False):
            suggestions.append("Citations appear clustered. Consider distributing citations more evenly throughout the content.")
        
        # Pattern suggestions
        if len(analysis["citation_patterns"]) > 2:
            suggestions.append("Multiple citation patterns detected. Consider using consistent citation formatting for better readability.")
        
        # Source quality suggestions
        if sources:
            avg_credibility = sum(s.get("credibility_score", 0) for s in sources) / len(sources)
            if avg_credibility < 0.6:
                suggestions.append("Low average source credibility. Consider using more authoritative sources when available.")
        
        # Content length suggestions
        if len(content) > 1000 and len(citations) < 3:
            suggestions.append("Long content with few citations. Consider adding more citations to support key claims.")
        
        if not suggestions:
            suggestions.append("Citation usage looks good! Consider adding more specific citations if you have additional factual claims.")
        
        return suggestions
    
    def format_citation_for_export(
        self, 
        content: str, 
        sources: List[Dict[str, Any]], 
        format_type: str = "markdown"
    ) -> str:
        """
        Format content with citations for export in different formats.
        
        Args:
            content: The content with citations
            sources: List of research sources
            format_type: Export format (markdown, html, plain_text)
            
        Returns:
            Formatted content for export
        """
        if format_type == "markdown":
            return self._format_markdown_export(content, sources)
        elif format_type == "html":
            return self._format_html_export(content, sources)
        elif format_type == "plain_text":
            return self._format_plain_text_export(content, sources)
        else:
            logger.warning(f"Unknown format type: {format_type}, using markdown")
            return self._format_markdown_export(content, sources)
    
    def _format_markdown_export(self, content: str, sources: List[Dict[str, Any]]) -> str:
        """Format content for markdown export."""
        # Add source list at the end
        source_list = self.generate_source_list(sources, "brackets")
        
        # Ensure proper markdown formatting
        formatted_content = content
        
        # Add source list
        if sources:
            formatted_content += f"\n\n{source_list}"
        
        return formatted_content
    
    def _format_html_export(self, content: str, sources: List[Dict[str, Any]]) -> str:
        """Format content for HTML export."""
        # Convert markdown to basic HTML
        html_content = content
        
        # Convert markdown links to HTML
        html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
        
        # Convert markdown bold to HTML
        html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
        
        # Convert line breaks to HTML
        html_content = html_content.replace('\n', '<br>\n')
        
        # Add source list
        if sources:
            source_list = self.generate_source_list(sources, "brackets")
            # Convert markdown source list to HTML
            html_source_list = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', source_list)
            html_source_list = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_source_list)
            html_source_list = html_source_list.replace('\n', '<br>\n')
            
            html_content += f"<br><br>{html_source_list}"
        
        return html_content
    
    def _format_plain_text_export(self, content: str, sources: List[Dict[str, Any]]) -> str:
        """Format content for plain text export."""
        # Remove markdown formatting
        plain_content = content
        
        # Remove markdown links, keeping just the text
        plain_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain_content)
        
        # Remove markdown bold
        plain_content = re.sub(r'\*\*([^*]+)\*\*', r'\1', plain_content)
        
        # Add source list
        if sources:
            source_list = self.generate_source_list(sources, "brackets")
            # Remove markdown formatting from source list
            plain_source_list = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain_source_list)
            plain_source_list = re.sub(r'\*\*([^*]+)\*\*', r'\1', plain_source_list)
            
            plain_content += f"\n\n{plain_source_list}"
        
        return plain_content
    
    def get_citation_statistics(self, content: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get comprehensive statistics about citations in content.
        
        Args:
            content: The content to analyze
            sources: List of research sources
            
        Returns:
            Citation statistics and metrics
        """
        citations = self.extract_citations(content)
        validation = self.validate_citations(content, sources)
        analysis = self.analyze_citation_patterns(content)
        
        stats = {
            "content_metrics": {
                "total_length": len(content),
                "word_count": len(content.split()),
                "paragraph_count": content.count('\n\n') + 1
            },
            "citation_metrics": {
                "total_citations": len(citations),
                "unique_citations": len(set(c.get("number") for c in citations if c.get("number"))),
                "citation_density": len(citations) / max(len(content.split()), 1) * 1000,  # citations per 1000 words
                "citation_coverage": validation["citation_coverage"],
                "citation_quality": validation["citation_quality"]
            },
            "source_metrics": {
                "total_sources": len(sources),
                "sources_cited": len(set(c.get("number") for c in citations if c.get("number"))),
                "citation_efficiency": len(set(c.get("number") for c in citations if c.get("number"))) / max(len(sources), 1)
            },
            "quality_metrics": {
                "validation_score": validation["validation_score"],
                "distribution_score": 1.0 if analysis["distribution"].get("evenly_distributed", False) else 0.5,
                "pattern_consistency": 1.0 if len(analysis["citation_patterns"]) <= 2 else 0.5
            }
        }
        
        # Calculate overall citation score
        overall_score = (
            stats["citation_metrics"]["citation_coverage"] * 0.3 +
            stats["citation_metrics"]["citation_quality"] * 0.3 +
            stats["quality_metrics"]["validation_score"] * 0.2 +
            stats["quality_metrics"]["distribution_score"] * 0.1 +
            stats["quality_metrics"]["pattern_consistency"] * 0.1
        )
        
        stats["overall_citation_score"] = round(overall_score, 3)
        
        return stats

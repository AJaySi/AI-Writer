####################################################
#
# FIXME: Gotta use this lib: https://github.com/monk1337/resp/tree/main
# https://github.com/danielnsilva/semanticscholar
# https://github.com/shauryr/S2QA
#
####################################################


import os
import sys
import re
import pandas as pd
import arxiv
import PyPDF2
import requests
import networkx as nx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from loguru import logger
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
from matplotlib import pyplot as plt
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np

logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

def create_arxiv_client(page_size=100, delay_seconds=3.0, num_retries=3):
    """
    Creates a reusable arXiv API client with custom configuration.

    Args:
        page_size (int): Number of results per page (default: 100)
        delay_seconds (float): Delay between API requests (default: 3.0)
        num_retries (int): Number of retries for failed requests (default: 3)

    Returns:
        arxiv.Client: Configured arXiv API client
    """
    try:
        client = arxiv.Client(
            page_size=page_size,
            delay_seconds=delay_seconds,
            num_retries=num_retries
        )
        return client
    except Exception as e:
        logger.error(f"Error creating arXiv client: {e}")
        raise e

def expand_search_query(query, research_interests=None):
    """
    Uses AI to expand the search query based on user's research interests.

    Args:
        query (str): Original search query
        research_interests (list): List of user's research interests

    Returns:
        str: Expanded search query
    """
    try:
        interests_context = "\n".join(research_interests) if research_interests else ""
        prompt = f"""Given the original arXiv search query: '{query}'
        {f'And considering these research interests:\n{interests_context}' if interests_context else ''}
        Generate an expanded arXiv search query that:
        1. Includes relevant synonyms and related concepts
        2. Uses appropriate arXiv search operators (AND, OR, etc.)
        3. Incorporates field-specific tags (ti:, abs:, au:, etc.)
        4. Maintains focus on the core topic
        Return only the expanded query without any explanation."""
        
        expanded_query = llm_text_gen(prompt)
        logger.info(f"Expanded query: {expanded_query}")
        return expanded_query
    except Exception as e:
        logger.error(f"Error expanding search query: {e}")
        return query

def analyze_citation_network(papers):
    """
    Analyzes citation relationships between papers using DOIs and references.

    Args:
        papers (list): List of paper metadata dictionaries

    Returns:
        dict: Citation network analysis results
    """
    try:
        # Create a directed graph for citations
        G = nx.DiGraph()
        
        # Add nodes and edges
        for paper in papers:
            paper_id = paper['entry_id']
            G.add_node(paper_id, title=paper['title'])
            
            # Add edges based on DOIs and references
            if paper['doi']:
                for other_paper in papers:
                    if other_paper['doi'] and other_paper['doi'] in paper['summary']:
                        G.add_edge(paper_id, other_paper['entry_id'])
        
        # Calculate network metrics
        analysis = {
            'influential_papers': sorted(nx.pagerank(G).items(), key=lambda x: x[1], reverse=True),
            'citation_clusters': list(nx.connected_components(G.to_undirected())),
            'citation_paths': dict(nx.all_pairs_shortest_path_length(G))
        }
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing citation network: {e}")
        return {}

def categorize_papers(papers):
    """
    Uses AI to categorize papers based on their metadata and content.

    Args:
        papers (list): List of paper metadata dictionaries

    Returns:
        dict: Paper categorization results
    """
    try:
        categorized_papers = {}
        for paper in papers:
            prompt = f"""Analyze this research paper and provide detailed categorization:
            Title: {paper['title']}
            Abstract: {paper['summary']}
            Primary Category: {paper['primary_category']}
            Categories: {', '.join(paper['categories'])}
            
            Provide a JSON response with these fields:
            1. main_theme: Primary research theme
            2. sub_themes: List of related sub-themes
            3. methodology: Research methodology used
            4. application_domains: Potential application areas
            5. technical_complexity: Level (Basic/Intermediate/Advanced)"""
            
            categorization = llm_text_gen(prompt)
            categorized_papers[paper['entry_id']] = categorization
        
        return categorized_papers
    except Exception as e:
        logger.error(f"Error categorizing papers: {e}")
        return {}

def get_paper_recommendations(papers, research_interests):
    """
    Generates personalized paper recommendations based on user's research interests.

    Args:
        papers (list): List of paper metadata dictionaries
        research_interests (list): User's research interests

    Returns:
        dict: Personalized paper recommendations
    """
    try:
        interests_text = "\n".join(research_interests)
        recommendations = {}
        
        for paper in papers:
            prompt = f"""Evaluate this paper's relevance to the user's research interests:
            Paper:
            - Title: {paper['title']}
            - Abstract: {paper['summary']}
            - Categories: {', '.join(paper['categories'])}
            
            User's Research Interests:
            {interests_text}
            
            Provide a JSON response with:
            1. relevance_score: 0-100
            2. relevance_aspects: List of matching aspects
            3. potential_value: How this paper could benefit the user's research"""
            
            evaluation = llm_text_gen(prompt)
            recommendations[paper['entry_id']] = evaluation
        
        return recommendations
    except Exception as e:
        logger.error(f"Error generating paper recommendations: {e}")
        return {}

def fetch_arxiv_data(query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate, sort_order=None, client=None, research_interests=None):
    """
    Fetches arXiv data based on a query with advanced search options.

    Args:
        query (str): The search query (supports advanced syntax, e.g., 'au:einstein AND cat:physics')
        max_results (int): The maximum number of results to fetch
        sort_by (arxiv.SortCriterion): Sorting criterion (default: SubmittedDate)
        sort_order (str): Sort order ('ascending' or 'descending', default: None)
        client (arxiv.Client): Optional custom client (default: None, creates new client)

    Returns:
        list: A list of arXiv data with extended metadata
    """
    try:
        if client is None:
            client = create_arxiv_client()

        # Expand search query using AI if research interests are provided
        expanded_query = expand_search_query(query, research_interests) if research_interests else query
        logger.info(f"Using expanded query: {expanded_query}")

        search = arxiv.Search(
            query=expanded_query,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order
        )

        results = list(client.results(search))
        all_data = [
            {
                'title': result.title,
                'published': result.published,
                'updated': result.updated,
                'entry_id': result.entry_id,
                'summary': result.summary,
                'authors': [str(author) for author in result.authors],
                'pdf_url': result.pdf_url,
                'journal_ref': getattr(result, 'journal_ref', None),
                'doi': getattr(result, 'doi', None),
                'primary_category': getattr(result, 'primary_category', None),
                'categories': getattr(result, 'categories', []),
                'links': [link.href for link in getattr(result, 'links', [])]
            }
            for result in results
        ]

        # Enhance results with AI-powered analysis
        if all_data:
            # Analyze citation network
            citation_analysis = analyze_citation_network(all_data)
            
            # Categorize papers using AI
            paper_categories = categorize_papers(all_data)
            
            # Generate recommendations if research interests are provided
            recommendations = get_paper_recommendations(all_data, research_interests) if research_interests else {}
            
            # Perform content analysis
            content_analyses = [analyze_paper_content(paper['entry_id']) for paper in all_data]
            trend_analysis = analyze_research_trends(all_data)
            concept_mapping = map_cross_paper_concepts(all_data)
            
            # Generate bibliography data
            bibliography_data = {
                'bibtex_entries': [generate_bibtex_entry(paper) for paper in all_data],
                'citations': {
                    'apa': [convert_citation_format(generate_bibtex_entry(paper), 'apa') for paper in all_data],
                    'mla': [convert_citation_format(generate_bibtex_entry(paper), 'mla') for paper in all_data],
                    'chicago': [convert_citation_format(generate_bibtex_entry(paper), 'chicago') for paper in all_data]
                },
                'reference_graph': visualize_reference_graph(all_data),
                'citation_impact': analyze_citation_impact(all_data)
            }
            
            # Add enhanced data to results
            enhanced_data = {
                'papers': all_data,
                'citation_analysis': citation_analysis,
                'paper_categories': paper_categories,
                'recommendations': recommendations,
                'content_analyses': content_analyses,
                'trend_analysis': trend_analysis,
                'concept_mapping': concept_mapping,
                'bibliography': bibliography_data
            }
            return enhanced_data
        
        return {'papers': all_data}
    except Exception as e:
        logger.error(f"An error occurred while fetching data from arXiv: {e}")
        raise e

def create_dataframe(data, column_names):
    """
    Creates a DataFrame from the provided data.

    Args:
        data (list): The data to convert to a DataFrame.
        column_names (list): The column names for the DataFrame.

    Returns:
        DataFrame: The created DataFrame.
    """
    try:
        df = pd.DataFrame(data, columns=column_names)
        return df
    except Exception as e:
        logger.error(f"An error occurred while creating DataFrame: {e}")
        return pd.DataFrame()

def get_arxiv_main_content(url):
    """
    Returns the main content of an arXiv paper.

    Args:
        url (str): The URL of the arXiv paper.

    Returns:
        str: The main content of the paper as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        main_content = soup.find('div', class_='ltx_page_content')
        if not main_content:
            logger.warning("Main content not found in the page.")
            return "Main content not found."
        alert_section = main_content.find('div', class_='package-alerts ltx_document')
        if (alert_section):
            alert_section.decompose()
        for element_id in ["abs", "authors"]:
            element = main_content.find(id=element_id)
            if (element):
                element.decompose()
        return main_content.text.strip()
    except Exception as html_error:
        logger.warning(f"HTML content not accessible, trying PDF: {html_error}")
        return get_pdf_content(url)

def download_paper(paper_id, output_dir="downloads", filename=None, get_source=False):
    """
    Downloads a paper's PDF or source files with enhanced error handling.

    Args:
        paper_id (str): The arXiv ID of the paper
        output_dir (str): Directory to save the downloaded file (default: 'downloads')
        filename (str): Custom filename (default: None, uses paper ID)
        get_source (bool): If True, downloads source files instead of PDF (default: False)

    Returns:
        str: Path to the downloaded file or None if download fails
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get paper metadata
        client = create_arxiv_client()
        paper = next(client.results(arxiv.Search(id_list=[paper_id])))

        # Set filename if not provided
        if not filename:
            safe_title = re.sub(r'[^\w\-_.]', '_', paper.title[:50])
            filename = f"{paper_id}_{safe_title}"
            filename += ".tar.gz" if get_source else ".pdf"

        # Full path for the downloaded file
        file_path = os.path.join(output_dir, filename)

        # Download the file
        if get_source:
            paper.download_source(dirpath=output_dir, filename=filename)
        else:
            paper.download_pdf(dirpath=output_dir, filename=filename)

        logger.info(f"Successfully downloaded {'source' if get_source else 'PDF'} to {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"Error downloading {'source' if get_source else 'PDF'} for {paper_id}: {e}")
        return None

def analyze_paper_content(url_or_id, cleanup=True):
    """
    Analyzes paper content using AI to extract key information and insights.

    Args:
        url_or_id (str): The arXiv URL or ID of the paper
        cleanup (bool): Whether to delete the PDF after extraction (default: True)

    Returns:
        dict: Analysis results including summary, key findings, and concepts
    """
    try:
        # Get paper content
        content = get_pdf_content(url_or_id, cleanup)
        if not content or 'Failed to' in content:
            return {'error': content}

        # Generate paper summary
        summary_prompt = f"""Analyze this research paper and provide a comprehensive summary:
        {content[:8000]}  # Limit content length for API
        
        Provide a JSON response with:
        1. executive_summary: Brief overview (2-3 sentences)
        2. key_findings: List of main research findings
        3. methodology: Research methods used
        4. implications: Practical implications of the research
        5. limitations: Study limitations and constraints"""
        
        summary_analysis = llm_text_gen(summary_prompt)

        # Extract key concepts and relationships
        concepts_prompt = f"""Analyze this research paper and identify key concepts and relationships:
        {content[:8000]}
        
        Provide a JSON response with:
        1. main_concepts: List of key technical concepts
        2. concept_relationships: How concepts are related
        3. novel_contributions: New ideas or approaches introduced
        4. technical_requirements: Required technologies or methods
        5. future_directions: Suggested future research"""
        
        concept_analysis = llm_text_gen(concepts_prompt)

        return {
            'summary_analysis': summary_analysis,
            'concept_analysis': concept_analysis,
            'full_text': content
        }
    except Exception as e:
        logger.error(f"Error analyzing paper content: {e}")
        return {'error': str(e)}

def analyze_research_trends(papers):
    """
    Analyzes research trends across multiple papers.

    Args:
        papers (list): List of paper metadata and content

    Returns:
        dict: Trend analysis results
    """
    try:
        # Collect paper information
        papers_info = []
        for paper in papers:
            content = get_pdf_content(paper['entry_id'], cleanup=True)
            if content and 'Failed to' not in content:
                papers_info.append({
                    'title': paper['title'],
                    'abstract': paper['summary'],
                    'content': content[:8000],  # Limit content length
                    'year': paper['published'].year
                })

        if not papers_info:
            return {'error': 'No valid paper content found for analysis'}

        # Analyze trends
        trends_prompt = f"""Analyze these research papers and identify key trends:
        Papers:
        {str(papers_info)}
        
        Provide a JSON response with:
        1. temporal_trends: How research focus evolved over time
        2. emerging_themes: New and growing research areas
        3. declining_themes: Decreasing research focus areas
        4. methodology_trends: Evolution of research methods
        5. technology_trends: Trends in technology usage
        6. research_gaps: Identified gaps and opportunities"""

        trend_analysis = llm_text_gen(trends_prompt)
        return {'trend_analysis': trend_analysis}

    except Exception as e:
        logger.error(f"Error analyzing research trends: {e}")
        return {'error': str(e)}

def map_cross_paper_concepts(papers):
    """
    Maps concepts and relationships across multiple papers.

    Args:
        papers (list): List of paper metadata and content

    Returns:
        dict: Concept mapping results
    """
    try:
        # Analyze each paper
        paper_analyses = []
        for paper in papers:
            analysis = analyze_paper_content(paper['entry_id'])
            if 'error' not in analysis:
                paper_analyses.append({
                    'paper_id': paper['entry_id'],
                    'title': paper['title'],
                    'analysis': analysis
                })

        if not paper_analyses:
            return {'error': 'No valid paper analyses for concept mapping'}

        # Generate cross-paper concept map
        mapping_prompt = f"""Analyze relationships between concepts across these papers:
        {str(paper_analyses)}
        
        Provide a JSON response with:
        1. shared_concepts: Concepts appearing in multiple papers
        2. concept_evolution: How concepts developed across papers
        3. conflicting_views: Different interpretations of same concepts
        4. complementary_findings: How papers complement each other
        5. knowledge_gaps: Areas needing more research"""

        concept_mapping = llm_text_gen(mapping_prompt)
        return {'concept_mapping': concept_mapping}

    except Exception as e:
        logger.error(f"Error mapping cross-paper concepts: {e}")
        return {'error': str(e)}

def generate_bibtex_entry(paper):
    """
    Generates a BibTeX entry for a paper with complete metadata.

    Args:
        paper (dict): Paper metadata dictionary

    Returns:
        str: BibTeX entry string
    """
    try:
        # Generate a unique citation key
        first_author = paper['authors'][0].split()[-1] if paper['authors'] else 'Unknown'
        year = paper['published'].year if paper['published'] else '0000'
        citation_key = f"{first_author}{year}{paper['entry_id'].split('/')[-1]}"

        # Format authors for BibTeX
        authors = ' and '.join(paper['authors'])

        # Create BibTeX entry
        bibtex = f"@article{{{citation_key},\n"
        bibtex += f"  title = {{{paper['title']}}},\n"
        bibtex += f"  author = {{{authors}}},\n"
        bibtex += f"  year = {{{year}}},\n"
        bibtex += f"  journal = {{arXiv preprint}},\n"
        bibtex += f"  archivePrefix = {{arXiv}},\n"
        bibtex += f"  eprint = {{{paper['entry_id'].split('/')[-1]}}},\n"
        if paper['doi']:
            bibtex += f"  doi = {{{paper['doi']}}},\n"
        bibtex += f"  url = {{{paper['entry_id']}}},\n"
        bibtex += f"  abstract = {{{paper['summary']}}}\n"
        bibtex += "}"

        return bibtex
    except Exception as e:
        logger.error(f"Error generating BibTeX entry: {e}")
        return ""

def convert_citation_format(bibtex_str, target_format):
    """
    Converts BibTeX citations to other formats and validates the output.

    Args:
        bibtex_str (str): BibTeX entry string
        target_format (str): Target citation format ('apa', 'mla', 'chicago', etc.)

    Returns:
        str: Formatted citation string
    """
    try:
        # Parse BibTeX entry
        bib_database = bibtexparser.loads(bibtex_str)
        entry = bib_database.entries[0]

        # Generate citation format prompt
        prompt = f"""Convert this bibliographic information to {target_format} format:
        Title: {entry.get('title', '')}
        Authors: {entry.get('author', '')}
        Year: {entry.get('year', '')}
        Journal: {entry.get('journal', '')}
        DOI: {entry.get('doi', '')}
        URL: {entry.get('url', '')}
        
        Return only the formatted citation without any explanation."""

        # Use AI to generate formatted citation
        formatted_citation = llm_text_gen(prompt)
        return formatted_citation.strip()
    except Exception as e:
        logger.error(f"Error converting citation format: {e}")
        return ""

def visualize_reference_graph(papers):
    """
    Creates a visual representation of the citation network.

    Args:
        papers (list): List of paper metadata dictionaries

    Returns:
        str: Path to the saved visualization file
    """
    try:
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes and edges
        for paper in papers:
            paper_id = paper['entry_id']
            G.add_node(paper_id, title=paper['title'])
            
            # Add citation edges
            if paper['doi']:
                for other_paper in papers:
                    if other_paper['doi'] and other_paper['doi'] in paper['summary']:
                        G.add_edge(paper_id, other_paper['entry_id'])
        
        # Set up the visualization
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # Draw the graph
        nx.draw(G, pos, with_labels=False, node_color='lightblue', 
                node_size=1000, arrowsize=20)
        
        # Add labels
        labels = nx.get_node_attributes(G, 'title')
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        # Save the visualization
        output_path = 'reference_graph.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    except Exception as e:
        logger.error(f"Error visualizing reference graph: {e}")
        return ""

def analyze_citation_impact(papers):
    """
    Analyzes citation impact and influence patterns.

    Args:
        papers (list): List of paper metadata dictionaries

    Returns:
        dict: Citation impact analysis results
    """
    try:
        # Create citation network
        G = nx.DiGraph()
        for paper in papers:
            G.add_node(paper['entry_id'], **paper)
            if paper['doi']:
                for other_paper in papers:
                    if other_paper['doi'] and other_paper['doi'] in paper['summary']:
                        G.add_edge(paper_id, other_paper['entry_id'])

        # Calculate impact metrics
        impact_analysis = {
            'citation_counts': dict(G.in_degree()),
            'influence_scores': nx.pagerank(G),
            'authority_scores': nx.authority_matrix(G).diagonal(),
            'hub_scores': nx.hub_matrix(G).diagonal(),
            'citation_paths': dict(nx.all_pairs_shortest_path_length(G))
        }

        # Add temporal analysis
        year_citations = defaultdict(int)
        for paper in papers:
            if paper['published']:
                year = paper['published'].year
                year_citations[year] += G.in_degree(paper['entry_id'])
        impact_analysis['temporal_trends'] = dict(year_citations)

        return impact_analysis
    except Exception as e:
        logger.error(f"Error analyzing citation impact: {e}")
        return {}

def get_pdf_content(url_or_id, cleanup=True):
    """
    Extracts text content from a paper's PDF with improved error handling.

    Args:
        url_or_id (str): The arXiv URL or ID of the paper
        cleanup (bool): Whether to delete the PDF after extraction (default: True)

    Returns:
        str: The extracted text content or error message
    """
    try:
        # Extract arxiv ID from URL if needed
        arxiv_id = url_or_id.split('/')[-1] if '/' in url_or_id else url_or_id
        
        # Download PDF
        pdf_path = download_paper(arxiv_id)
        if not pdf_path:
            return "Failed to download PDF."

        # Extract text from PDF
        pdf_text = ''
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += f"\n--- Page {page_num} ---\n{page_text}"
                except Exception as err:
                    logger.error(f"Error extracting text from page {page_num}: {err}")
                    continue

        # Clean up
        if cleanup:
            try:
                os.remove(pdf_path)
                logger.debug(f"Cleaned up temporary PDF file: {pdf_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup PDF file {pdf_path}: {e}")

        # Process and return text
        if not pdf_text.strip():
            return "No text content could be extracted from the PDF."
            
        return clean_pdf_text(pdf_text)

    except Exception as e:
        logger.error(f"Failed to process PDF: {e}")
        return f"Failed to retrieve content: {str(e)}"

def clean_pdf_text(text):
    """
    Helper function to clean the text extracted from a PDF.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    pattern = r'References\s*.*'
    text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    sections_to_remove = ['Acknowledgements', 'References', 'Bibliography']
    for section in sections_to_remove:
        pattern = r'(' + re.escape(section) + r'\s*.*?)(?=\n[A-Z]{2,}|$)'
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    return text

def download_image(image_url, base_url, folder="images"):
    """
    Downloads an image from a URL.

    Args:
        image_url (str): The URL of the image.
        base_url (str): The base URL of the website.
        folder (str): The folder to save the image.

    Returns:
        bool: True if the image was downloaded successfully, False otherwise.
    """
    if image_url.startswith('data:image'):
        logger.info(f"Skipping download of data URI image: {image_url}")
        return False
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not urlparse(image_url).scheme:
        if not base_url.endswith('/'):
            base_url += '/'
        image_url = base_url + image_url
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_name = image_url.split("/")[-1]
        with open(os.path.join(folder, image_name), 'wb') as file:
            file.write(response.content)
        return True
    except requests.RequestException as e:
        logger.error(f"Error downloading {image_url}: {e}")
        return False

def scrape_images_from_arxiv(url):
    """
    Scrapes images from an arXiv page.

    Args:
        url (str): The URL of the arXiv page.

    Returns:
        list: A list of image URLs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        return image_urls
    except requests.RequestException as e:
        logger.error(f"Error fetching page {url}: {e}")
        return []

def generate_bibtex(paper_id, client=None):
    """
    Generate a BibTeX entry for an arXiv paper with enhanced metadata.

    Args:
        paper_id (str): The arXiv ID of the paper
        client (arxiv.Client): Optional custom client (default: None)

    Returns:
        str: BibTeX entry as a string
    """
    try:
        if client is None:
            client = create_arxiv_client()

        # Fetch paper metadata
        paper = next(client.results(arxiv.Search(id_list=[paper_id])))
        
        # Extract author information
        authors = [str(author) for author in paper.authors]
        first_author = authors[0].split(', ')[0] if authors else 'Unknown'
        
        # Format year
        year = paper.published.year if paper.published else 'Unknown'
        
        # Create citation key
        citation_key = f"{first_author}{str(year)[-2:]}"
        
        # Build BibTeX entry
        bibtex = [
            f"@article{{{citation_key},",
            f"  author = {{{' and '.join(authors)}}},",
            f"  title = {{{paper.title}}},",
            f"  year = {{{year}}},",
            f"  eprint = {{{paper_id}}},",
            f"  archivePrefix = {{arXiv}},"
        ]
        
        # Add optional fields if available
        if paper.doi:
            bibtex.append(f"  doi = {{{paper.doi}}},")
        if getattr(paper, 'journal_ref', None):
            bibtex.append(f"  journal = {{{paper.journal_ref}}},")
        if getattr(paper, 'primary_category', None):
            bibtex.append(f"  primaryClass = {{{paper.primary_category}}},")
            
        # Add URL and close entry
        bibtex.extend([
            f"  url = {{https://arxiv.org/abs/{paper_id}}}",
            "}"
        ])
        
        return '\n'.join(bibtex)
        
    except Exception as e:
        logger.error(f"Error generating BibTeX for {paper_id}: {e}")
        return ""

def batch_download_papers(paper_ids, output_dir="downloads", get_source=False):
    """
    Download multiple papers in batch with progress tracking.

    Args:
        paper_ids (list): List of arXiv IDs to download
        output_dir (str): Directory to save downloaded files (default: 'downloads')
        get_source (bool): If True, downloads source files instead of PDFs (default: False)

    Returns:
        dict: Mapping of paper IDs to their download status and paths
    """
    results = {}
    client = create_arxiv_client()

    for paper_id in paper_ids:
        try:
            file_path = download_paper(paper_id, output_dir, get_source=get_source)
            results[paper_id] = {
                'success': bool(file_path),
                'path': file_path,
                'error': None
            }
        except Exception as e:
            results[paper_id] = {
                'success': False,
                'path': None,
                'error': str(e)
            }
            logger.error(f"Failed to download {paper_id}: {e}")

    return results

def batch_generate_bibtex(paper_ids):
    """
    Generate BibTeX entries for multiple papers.

    Args:
        paper_ids (list): List of arXiv IDs

    Returns:
        dict: Mapping of paper IDs to their BibTeX entries
    """
    results = {}
    client = create_arxiv_client()

    for paper_id in paper_ids:
        try:
            bibtex = generate_bibtex(paper_id, client)
            results[paper_id] = {
                'success': bool(bibtex),
                'bibtex': bibtex,
                'error': None
            }
        except Exception as e:
            results[paper_id] = {
                'success': False,
                'bibtex': '',
                'error': str(e)
            }
            logger.error(f"Failed to generate BibTeX for {paper_id}: {e}")

    return results

def extract_arxiv_ids_from_line(line):
    """
    Extract the arXiv ID from a given line of text.

    Args:
        line (str): A line of text potentially containing an arXiv URL.

    Returns:
        str: The extracted arXiv ID, or None if not found.
    """
    arxiv_id_pattern = re.compile(r'arxiv\.org\/abs\/(\d+\.\d+)(v\d+)?')
    match = arxiv_id_pattern.search(line)
    if match:
        return match.group(1) + (match.group(2) if match.group(2) else '')
    return None

def read_written_ids(file_path):
    """
    Read already written arXiv IDs from a file.

    Args:
        file_path (str): Path to the file containing written IDs.

    Returns:
        set: A set of arXiv IDs.
    """
    written_ids = set()
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                written_ids.add(line.strip())
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error while reading the file: {e}")
    return written_ids

def append_id_to_file(arxiv_id, output_file_path):
    """
    Append a single arXiv ID to a file. Checks if the file exists and creates it if not.

    Args:
        arxiv_id (str): The arXiv ID to append.
        output_file_path (str): Path to the output file.
    """
    try:
        if not os.path.exists(output_file_path):
            logger.info(f"File does not exist. Creating new file: {output_file_path}")
            with open(output_file_path, 'a', encoding="utf-8") as outfile:
                outfile.write(arxiv_id + '\n')
        else:
            logger.info(f"Appending to existing file: {output_file_path}")
            with open(output_file_path, 'a', encoding="utf-8") as outfile:
                outfile.write(arxiv_id + '\n')
    except Exception as e:
        logger.error(f"Error while appending to file: {e}")

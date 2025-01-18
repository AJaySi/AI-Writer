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
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

def fetch_arxiv_data(query, max_results=10):
    """
    Fetches arXiv data based on a query.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of arXiv data.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
        results = list(client.results(search))
        all_data = [[result.title, result.published, result.entry_id, result.summary, result.pdf_url] for result in results]
        return all_data
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

def get_pdf_content(url):
    """
    Helper function to get the content from a PDF if HTML content is not accessible.

    Args:
        url (str): The URL of the arXiv paper.

    Returns:
        str: The main content of the paper as a string.
    """
    try:
        client = arxiv.Client()
        arxiv_id = url.split('/')[-1]
        paper = next(client.results(arxiv.Search(id_list=[arxiv_id])))
        pdf_filename = paper.download_pdf(filename=f"downloaded-paper-{arxiv_id}.pdf")
        pdf_text = ''
        with open(pdf_filename, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += page_text + '\n'
                except UnicodeDecodeError as err:
                    logger.error(f"UnicodeDecodeError that arises during text extraction: {err}")
                    pass
        os.remove(pdf_filename)
        pdf_text = clean_pdf_text(pdf_text)
        return pdf_text
    except Exception as pdf_error:
        logger.error(f"Failed to process PDF: {pdf_error}")
        return "Failed to retrieve content."

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

def arxiv_bibtex(arxiv_id):
    """
    Get the BibTeX entry for an arXiv paper.

    Args: 
        arxiv_id: The arXiv ID of the paper.

    Returns: 
        A string containing the BibTeX entry.
    """
    try:
        usock = urllib.request.urlopen(f'http://export.arxiv.org/api/query?id_list={arxiv_id}')
        xmldoc = xml.dom.minidom.parse(usock)
        usock.close()
        entry = xmldoc.getElementsByTagName("entry")[0]
        date = entry.getElementsByTagName("updated")[0].firstChild.data
        text_year = date[:4]
        title = entry.getElementsByTagName("title")[0]
        text_title = title.firstChild.data.strip()
        authorlist = []
        first = True
        for person_name in entry.getElementsByTagName("author"):
            name = person_name.getElementsByTagName("name")[0]
            text_name = name.firstChild.data
            text_given_name = ' '.join(text_name.split()[:-1])
            text_surname = text_name.split()[-1]
            authorlist.append(f"{text_surname}, {text_given_name}")
            if first:
                text_first_author_surname = text_surname
                first = False
        bibtex = f"@MISC{{{text_first_author_surname}{text_year[-2:]},\n"
        bibtex += f" author = {' and '.join(authorlist)},\n"
        bibtex += f" title = {{{text_title}}},\n"
        bibtex += f" year = {{{text_year}}},\n"
        bibtex += f" eprint = {{{arxiv_id}}},\n"
        bibtex += f" url = {{http://arxiv.org/abs/{arxiv_id}}}\n"
        bibtex += "}"
        return bibtex
    except Exception as e:
        logger.error(f"Error while generating BibTeX: {e}")
        return ""

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

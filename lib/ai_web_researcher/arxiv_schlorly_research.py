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
import io
import requests
from bs4 import BeautifulSoup
import urllib.parse
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def fetch_arxiv_data(query, max_results=10):
    try:
        # Construct the default API client
        client = arxiv.Client()

        # Search for articles matching the keyword
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        # Fetching results
        results = list(client.results(search))
        # Extracting data
        all_data = []
        for result in results:
            temp = [result.title, result.published, result.entry_id, result.summary, result.pdf_url]
            all_data.append(temp)

        return all_data

    except Exception as e:
        print("An error occurred while fetching data from arXiv:", e)
        raise e


def create_dataframe(data, column_names):
    try:
        df = pd.DataFrame(data, columns=column_names)
        return df
    except Exception as e:
        print("An error occurred while creating DataFrame:", e)
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
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main content in 'ltx_page_content'
        main_content = soup.find('div', class_='ltx_page_content')
        if not main_content:
            logger.warning("Main content not found in the page.")
            return "Main content not found."

        # Remove specific section with class 'package-alerts ltx_document'
        alert_section = main_content.find('div', class_='package-alerts ltx_document')
        if alert_section:
            alert_section.decompose()

        # Optional: Remove abstract and authors if present
        for element_id in ["abs", "authors"]:
            element = main_content.find(id=element_id)
            if element:
                element.decompose()
        return main_content.text.strip()

    # Could not access the arxiv HTML content, instead download pdf and read its content.
    except Exception as html_error:
        logger.warning(f"HTML content not accessible, trying PDF: {html_error}")
        try:
            # Extract arXiv ID from URL
            arxiv_id = url.split('/')[-1]
            # Fetch paper information using arXiv API
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[arxiv_id])))
            pdf_filename = paper.download_pdf(filename=f"downloaded-paper-{arxiv_id}.pdf")
            # Initialize an empty string to store the extracted text
            pdf_text = ''

            # Read the downloaded PDF
            with open(pdf_filename, 'rb', encoding="utf-8") as f:
                pdf_reader = PyPDF2.PdfReader(f)

                for page in pdf_reader.pages:
                    try:
                        # Attempt to extract text from the current page
                        page_text = page.extract_text()
                        # If text extraction is successful, add it to the cumulative text
                        if page_text:
                            pdf_text += page_text + '\n'
                    except UnicodeDecodeError as err:
                        # FIXME: Handle any UnicodeDecodeError that arises during text extraction
                        logger.error(f"UnicodeDecodeError that arises during text extraction: {err}")
                        pass

            # Optionally, remove the downloaded PDF file
            os.remove(pdf_filename)
            
            # Pattern to match 'References' and everything that follows
            pattern = r'References\s*.*'
            pdf_text = re.sub(pattern, '', pdf_text, flags=re.IGNORECASE | re.DOTALL)
            sections_to_remove = ['Acknowledgements', 'References', 'Bibliography']
            for section in sections_to_remove:
                # Pattern to match the section title and any text following it until the next big title or end of document
                pattern = r'(' + re.escape(section) + r'\s*.*?)(?=\n[A-Z]{2,}|$)'
                pdf_text = re.sub(pattern, '', pdf_text, flags=re.DOTALL | re.IGNORECASE)

            return pdf_text

        except Exception as pdf_error:
            logger.error(f"Failed to process PDF: {pdf_error}")
            return "Failed to retrieve content."


def download_image(image_url, base_url, folder="images"):
    # Skip downloading if the image URL is a data URI
    if image_url.startswith('data:image'):
        print(f"Skipping download of data URI image: {image_url}")
        return False

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Form the absolute URL for image paths
    if not urllib.parse.urlparse(image_url).scheme:
        if not base_url.endswith('/'):
            base_url += '/'
        image_url = base_url + image_url

    # Download and save the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        image_name = image_url.split("/")[-1]
        with open(os.path.join(folder, image_name), 'wb', encoding="utf-8") as file:
            file.write(response.content)
        return True

    except requests.RequestException as e:
        print(f"Error downloading {image_url}: {str(e)}")
        return False


def scrape_images_from_arxiv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        return image_urls

    except requests.RequestException as e:
        print(f"Error fetching page {url}: {str(e)}")
        return []


def arxiv_bibtex(arxiv_id):
    """
    Get the BibTeX entry for an arXiv paper.
    Args: 
        arxiv_id: The arXiv ID of the paper.
    Returns: 
        A string containing the BibTeX entry.
    """

    import urllib.request, xml.dom.minidom

    # Download the XML
    try:
        usock = urllib.request.urlopen(f'http://export.arxiv.org/api/query?id_list={arxiv_id}')
        xmldoc = xml.dom.minidom.parse(usock)
        usock.close()
    except Exception as e:
        raise e

    # Parse the XML
    entry = xmldoc.getElementsByTagName("entry")[0]
    date = entry.getElementsByTagName("updated")[0].firstChild.data
    text_year = date[:4]

    title = entry.getElementsByTagName("title")[0]
    text_title = title.firstChild.data.strip()

    authorlist = []
    first = True
    for person_name in entry.getElementsByTagName("author"):
        # Get names
        name = person_name.getElementsByTagName("name")[0]
        text_name = name.firstChild.data
        text_given_name = ' '.join(text_name.split()[:-1])
        text_surname = text_name.split()[-1]
        authorlist.append(f"{text_surname}, {text_given_name}")
        # First author?
        if first:
            text_first_author_surname = text_surname
            first = False

    # Construct the BibTeX entry
    bibtex = f"@MISC{{{text_first_author_surname}{text_year[-2:]},\n"
    bibtex += f" author = {' and '.join(authorlist)},\n"
    bibtex += f" title = {{{text_title}}},\n"
    bibtex += f" year = {{{text_year}}},\n"
    bibtex += f" eprint = {{{arxiv_id}}},\n"
    bibtex += f" url = {{http://arxiv.org/abs/{arxiv_id}}}\n"
    bibtex += "}"

    return bibtex


#from serpapi import GoogleSearch
#params = {
#  "api_key": "os.getenv(SERPER_API_KEY)",
#  "engine": "google_scholar",
#  "q": "llm",
#  "hl": "en",
#  "as_ylo": "2023",
#  "as_yhi": "2024"
#}
#search = GoogleSearch(params)
#results = search.get_dict()

#from llmsherpa.readers import LayoutPDFReader

#llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
#pdf_url = "https://arxiv.org/pdf/1910.13461.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
#pdf_reader = LayoutPDFReader(llmsherpa_api_url)
#doc = pdf_reader.read_pdf(pdf_url)




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
        # Check if file exists
        if not os.path.exists(output_file_path):
            logger.info(f"File does not exist. Creating new file: {output_file_path}")
            # Create a new file and append the ID
            with open(output_file_path, 'a', encoding="utf-8") as outfile:
                outfile.write(arxiv_id + '\n')
        else:
            logger.info(f"Appending to existing file: {output_file_path}")
            # File exists, append the ID
            with open(output_file_path, 'a', encoding="utf-8") as outfile:
                outfile.write(arxiv_id + '\n')

    except Exception as e:
        logger.error(f"Error while appending to file: {e}")

from bs4 import BeautifulSoup
import re

def create_table_of_contents(html_content):
    """
    Create a table of contents for a given HTML content.

    Args:
    html_content (str): HTML content of the blog post.

    Returns:
    str: HTML content with a table of contents.
    """
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all header tags (h1, h2, h3, h4, h5, h6)
    headers = soup.find_all(re.compile('^h[1-6]$'))

    # Create a table of contents
    toc = BeautifulSoup('<div id="table-of-contents"><h2>Table of Contents</h2><ul></ul></div>', 'html.parser')
    toc_ul = toc.find('ul')

    # Loop through headers and add them to the table of contents
    for i, header in enumerate(headers, start=1):
        header_id = f"toc_{i}"
        header['id'] = header_id

        toc_entry = soup.new_tag('li')
        toc_link = soup.new_tag('a', href=f"#{header_id}")
        toc_link.string = header.get_text()
        toc_entry.append(toc_link)
        toc_ul.append(toc_entry)

    # Insert the table of contents at the beginning of the content
    soup.insert(0, toc)

    return str(soup)

# Example usage
html_content = "<h1>Title</h1><p>Some text</p><h2>Subtitle 1</h2><p>Text under subtitle 1</p><h2>Subtitle 2</h2><p>Text under subtitle 2</p>"
html_with_toc = create_table_of_contents(html_content)
print(html_with_toc)


import re

class PlagiarismChecker:
    def __init__(self, known_sources):
        self.known_sources = known_sources

    def check_plagiarism(self, html_content):
        try:
            # Preprocess the HTML content by removing HTML tags and extra spaces
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = re.sub(r'\s+', ' ', text).strip().lower()

            # Check for exact matches with known sources
            for source in self.known_sources:
                source_text = re.sub(r'<[^>]+>', ' ', source)
                source_text = re.sub(r'\s+', ' ', source_text).strip().lower()
                if text == source_text:
                    return f"Plagiarism detected: Matches known source - {source}"

            # If no exact matches are found
            return "No plagiarism detected. Content is original."

        except Exception as e:
            return str(e)

# Example usage:
if __name__ == "__main__":
    # List of known sources
    known_sources = [
        """
        <html>
        <head>
            <title>Sample Page 1</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is sample content from known source 1.</p>
        </body>
        </html>
        """,
        """
        <html>
        <head>
            <title>Sample Page 2</title>
        </head>
        <body>
            <h1>Welcome to Known Source 2</h1>
            <p>This is some content from another known source.</p>
        </body>
        </html>
        """
    ]

    # HTML content to check for plagiarism
    html_content = """
    <html>
    <head>
        <title>Sample Page</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is sample content.</p>
    </body>
    </html>
    """

    plagiarism_checker = PlagiarismChecker(known_sources)
    result = plagiarism_checker.check_plagiarism(html_content)

    print(result)


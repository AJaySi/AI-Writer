## main.py

from wordpress_api import WordpressAPI


def main():
    """
    Main entry point of the program.
    """
    # Create WordpressAPI instance
    wp_api = WordpressAPI(base_url="https://example.com", username="admin", password="password")
    
    # Authenticate
    wp_api.authenticate()
    
    # Upload content
    content = "This is a test content"
    wp_api.upload_content(content)
    
if __name__ == "__main__":
    main()

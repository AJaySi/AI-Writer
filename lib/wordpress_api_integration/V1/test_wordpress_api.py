## test_wordpress_api.py

import pytest
from wordpress_api import WordpressAPI


class TestWordpressAPI:
    @pytest.fixture
    def wp_api(self):
        return WordpressAPI(base_url="https://example.com", username="admin", password="password")
    
    def test_authenticate_success(self, wp_api):
        wp_api.authenticate()
        assert wp_api.authentication.token is not None
    
    def test_authenticate_failure(self, wp_api):
        wp_api.authentication.password = "wrong_password"
        with pytest.raises(Exception):
            wp_api.authenticate()
    
    def test_upload_content_success(self, wp_api):
        content = "This is a test content"
        wp_api.upload_content(content)
        # Add assertions here to verify the success of content upload
    
    def test_upload_content_failure(self, wp_api):
        content = "This is a test content"
        wp_api.content_upload.base_url = "https://wrong_url.com"
        with pytest.raises(Exception):
            wp_api.upload_content(content)

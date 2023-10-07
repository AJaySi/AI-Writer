## wordpress_api.py

import requests
import json

class Authentication:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
    
    def authenticate(self):
        """
        Authenticates the user with the Wordpress API.
        """
        url = f"{self.base_url}/authenticate"
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            self.token = response.json()["token"]
        else:
            raise Exception("Authentication failed")
            

class ContentUpload:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
    
    def upload_content(self, content):
        """
        Uploads the given content to the Wordpress API.
        """
        url = f"{self.base_url}/upload"
        payload = {
            "content": content,
            "token": self.token
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception("Content upload failed")

class WordpressAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.authentication = Authentication(base_url, username, password)
        self.content_upload = ContentUpload(base_url, self.authentication.token)
    
    def authenticate(self):
        """
        Authenticates the user with the Wordpress API.
        """
        self.authentication.authenticate()
    
    def upload_content(self, content):
        """
        Uploads the given content to the Wordpress API.
        """
        self.content_upload.upload_content(content)

"""Website setup component for the API key manager."""

import streamlit as st
from loguru import logger
# Removed website_analyzer imports as analysis is separate now
# from ...website_analyzer import analyze_website
# from ...website_analyzer.seo_analyzer import analyze_seo
import asyncio
import sys
from typing import Dict, Any
import requests
import ssl
import socket
from urllib.parse import urlparse

from ..manager import APIKeyManager
# Navigation is handled in base.py now
# from .base import render_navigation_buttons 

# Configure logger (minimal example)
logger.add(sys.stderr, level="INFO") 

# --- Validation Helpers ---
def _is_valid_url_format(url: str) -> bool:
    """Checks if the URL has a valid basic format (scheme and netloc)."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

def _check_url_reachability(url: str) -> tuple[bool, str]:
    """Checks if the URL is reachable and returns status code or error."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5) # HEAD request is faster
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info(f"URL {url} reachable, status code: {response.status_code}")
        return True, f"Reachable (Status: {response.status_code})"
    except requests.exceptions.Timeout:
        logger.warning(f"URL {url} timed out.")
        return False, "Timeout: Server did not respond in time."
    except requests.exceptions.RequestException as e:
        logger.warning(f"URL {url} not reachable: {e}")
        # Provide a more user-friendly message for common errors
        if isinstance(e, requests.exceptions.ConnectionError):
             return False, "Connection Error: Could not connect to the server."
        elif isinstance(e, requests.exceptions.HTTPError):
             return False, f"HTTP Error: {e.response.status_code}"
        return False, f"Error: {type(e).__name__}"

def _check_ssl_certificate(url: str) -> tuple[bool, str]:
    """Checks if the URL has a valid SSL certificate (for https)."""
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        return True, "(HTTP URL)" # Not applicable for http
        
    hostname = parsed_url.netloc
    port = 443
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Basic check: does it exist? More thorough checks (expiry, chain) are possible
                if cert:
                    logger.info(f"SSL certificate found for {hostname}")
                    return True, "Valid SSL Certificate"
                else:
                    logger.warning(f"No SSL certificate found for {hostname}")
                    return False, "No SSL Certificate found"
    except ssl.SSLCertVerificationError as e:
        logger.warning(f"SSL Verification Error for {hostname}: {e}")
        return False, f"SSL Verification Error: {e.verify_message}"
    except socket.timeout:
        logger.warning(f"SSL check timed out for {hostname}")
        return False, "SSL Check Timeout"
    except Exception as e:
        logger.error(f"Error checking SSL for {hostname}: {e}", exc_info=True)
        return False, f"SSL Check Error: {type(e).__name__}"


# --- Main Component Logic ---

def _validate_website_url(url: str) -> tuple[str, str]:
    """Performs quick validation (format, reachability, basic SSL)."""
    if not url:
        return "unsaved", ""

    # 1. Format Check
    if not _is_valid_url_format(url):
        logger.warning(f"Invalid URL format: {url}")
        return "invalid_format", "Invalid URL format. Please include http:// or https://"

    # 2. Reachability Check
    reachable, reach_status = _check_url_reachability(url)
    if not reachable:
        logger.warning(f"URL not reachable: {url} ({reach_status})")
        return "unreachable", reach_status # Return specific error message

    # 3. Basic SSL Check (only if reachable and HTTPS)
    if urlparse(url).scheme == 'https':
        ssl_valid, ssl_status = _check_ssl_certificate(url)
        if not ssl_valid:
            logger.warning(f"SSL check failed for {url} ({ssl_status})")
            return "ssl_error", ssl_status # Return specific error message

    logger.info(f"URL validation successful for: {url}")
    return "valid", "URL is valid and reachable."


def _handle_website_url_change(api_key_manager: APIKeyManager):
    """Save and validate website URL when input changes."""
    url_input_widget_key = "website_url_input"
    status_widget_key = "website_url_status"
    
    if url_input_widget_key not in st.session_state:
        logger.warning(f"Input widget key '{url_input_widget_key}' not found.")
        return

    url_value = st.session_state[url_input_widget_key]
    logger.debug(f"Handling website URL change. URL: {url_value}")

    # Save the URL regardless of validity for now (maybe refine later)
    # api_key_manager might not be the right place, consider storing directly in session state
    # or a dedicated config manager if this isn't an API key.
    # Let's store in session_state for now.
    st.session_state['configured_website_url'] = url_value
    logger.info(f"Saved website URL to session state: {url_value}")

    if not url_value:
        st.session_state[status_widget_key] = ("unsaved", "")
        logger.info("Cleared website URL.")
        return

    st.session_state[status_widget_key] = ("saving", "") # Indicate validation is running
    st.rerun()

    try:
        validation_status, message = _validate_website_url(url_value)
        st.session_state[status_widget_key] = (validation_status, message)
        logger.info(f"Website URL validation complete. Status: {validation_status}, Msg: {message}")

    except Exception as e:
        logger.error(f"Error during website URL validation: {e}", exc_info=True)
        st.session_state[status_widget_key] = ("error", "An unexpected error occurred during validation.")


def render_website_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the website setup step with immediate feedback."""
    logger.info("[render_website_setup] Rendering website setup component")
    
    status_key = "website_url_status"

    # Initialize status
    if status_key not in st.session_state:
         st.session_state[status_key] = ("unsaved", "")
         # Optionally pre-validate if a URL exists from previous session/config
         # pre_existing_url = api_key_manager.get_config("website_url") # Example
         # if pre_existing_url:
         #    st.session_state[status_key] = _validate_website_url(pre_existing_url)

    st.markdown("""
        <div class='setup-header'>
            <h2>Step 2: Website Setup (Optional)</h2>
            <p>Enter your primary website URL. This helps Alwrity personalize suggestions and analyze your content.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get current value from session state if available, otherwise empty
    current_url = st.session_state.get('configured_website_url', "")
    
    st.text_input(
        "Website URL", 
        value=current_url,
        placeholder="https://example.com", 
        key="website_url_input",
        on_change=_handle_website_url_change,
        args=(api_key_manager,) # Pass manager if needed by save logic
    )
    
    # --- Feedback Area ---
    status, message = st.session_state.get(status_key, ("unsaved", ""))
    feedback_placeholder = st.empty()
    
    if status == "saving":
        feedback_placeholder.info("Validating URL...", icon="⏳")
    elif status == "valid":
        feedback_placeholder.success(message, icon="✅")
    elif status == "invalid_format":
        feedback_placeholder.error(f"Format Error: {message}", icon="❌")
    elif status == "unreachable":
        feedback_placeholder.error(f"Reachability Error: {message}", icon="❌")
    elif status == "ssl_error":
         feedback_placeholder.warning(f"SSL Warning: {message}", icon="⚠️") # Warning for SSL
    elif status == "error":
         feedback_placeholder.error(f"Validation Error: {message}", icon="⚠️")
    elif status == "unsaved" and current_url: # Show warning if field has text but isn't validated yet
         feedback_placeholder.warning("URL not yet validated.", icon="⚠️")

    # --- Removed Analysis Section ---
    # The detailed website analysis should be a separate feature, not part of the initial setup validation.
    st.markdown("---")
    st.markdown("ℹ️ *The detailed Website Analyzer tool is available separately in the main application.*")
    st.info("Entering your website URL is optional. Click Continue to proceed.")

    # Return value is not strictly needed if navigation relies on session state status
    return {}

# Removed old analysis logic and button handling as it's handled in base.py

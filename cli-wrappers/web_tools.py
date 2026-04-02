"""
Web Tools - WebFetch, WebSearch, and WebBrowser functionality

Based on Claude Code's web tools implementation.
"""

import requests
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import json

from file_operations import RiskLevel


@dataclass
class WebFetchResult:
    """Result of a web fetch operation"""
    success: bool
    content: Optional[str] = None
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    final_url: Optional[str] = None
    error: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM


@dataclass
class WebSearchResult:
    """Result from a web search"""
    title: str
    url: str
    snippet: str
    score: Optional[float] = None


class URLValidator:
    """Validates URLs for safety"""

    ALLOWED_PROTOCOLS = {'http', 'https'}
    BLOCKED_DOMAINS = {
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '169.254.169.254',  # AWS metadata
    }

    @classmethod
    def validate(cls, url: str) -> Tuple[bool, str]:
        """Validate URL for safety"""
        try:
            parsed = urlparse(url)

            # Check protocol
            if parsed.scheme not in cls.ALLOWED_PROTOCOLS:
                return False, f"Disallowed protocol: {parsed.scheme}"

            # Check for blocked domains
            if parsed.netloc.lower() in cls.BLOCKED_DOMAINS:
                return False, f"Blocked domain: {parsed.netloc}"

            return True, ""

        except Exception as e:
            return False, f"Invalid URL: {e}"


class WebFetchTool:
    """
    Web content fetching tool.

    Based on Claude Code's WebFetchTool implementation.
    """

    def __init__(
        self,
        timeout: int = 30,
        user_agent: Optional[str] = None,
        max_content_size: int = 10 * 1024 * 1024  # 10MB
    ):
        self.timeout = timeout
        self.max_content_size = max_content_size
        self.session = requests.Session()

        if user_agent:
            self.session.headers.update({'User-Agent': user_agent})

    def fetch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
        max_size: Optional[int] = None
    ) -> WebFetchResult:
        """
        Fetch content from a URL.

        Args:
            url: URL to fetch
            headers: Additional headers
            follow_redirects: Whether to follow HTTP redirects
            max_size: Maximum content size

        Returns:
            WebFetchResult with content or error
        """
        # Validate URL
        is_valid, error_msg = URLValidator.validate(url)
        if not is_valid:
            return WebFetchResult(
                success=False,
                error=error_msg,
                risk_level=RiskLevel.HIGH
            )

        exec_max_size = max_size or self.max_content_size

        try:
            response = self.session.get(
                url,
                headers=headers,
                allow_redirects=follow_redirects,
                timeout=self.timeout,
                stream=True
            )

            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > exec_max_size:
                return WebFetchResult(
                    success=False,
                    status_code=response.status_code,
                    error=f"Content too large: {content_length} bytes",
                    risk_level=RiskLevel.MEDIUM
                )

            # Read content
            content = response.content
            if len(content) > exec_max_size:
                content = content[:exec_max_size]

            return WebFetchResult(
                success=True,
                content=content.decode('utf-8', errors='ignore'),
                status_code=response.status_code,
                headers=dict(response.headers),
                final_url=response.url,
                risk_level=RiskLevel.MEDIUM
            )

        except requests.Timeout:
            return WebFetchResult(
                success=False,
                error=f"Request timed out after {self.timeout} seconds",
                risk_level=RiskLevel.LOW
            )
        except requests.RequestException as e:
            return WebFetchResult(
                success=False,
                error=str(e),
                risk_level=RiskLevel.MEDIUM
            )

    def fetch_json(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> WebFetchResult:
        """Fetch and parse JSON response"""
        result = self.fetch(url, headers)

        if result.success:
            try:
                json_data = json.loads(result.content)
                result.content = json.dumps(json_data, indent=2)
            except json.JSONDecodeError as e:
                result.success = False
                result.error = f"Invalid JSON: {e}"

        return result


class WebSearchTool:
    """
    Web search tool.

    Based on Claude Code's WebSearchTool implementation.
    Note: Actual implementation requires API keys for search engines.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def search(
        self,
        query: str,
        num_results: int = 10,
        lang: Optional[str] = None
    ) -> List[WebSearchResult]:
        """
        Search the web for results.

        Args:
            query: Search query
            num_results: Number of results to return
            lang: Language code

        Returns:
            List of WebSearchResult objects
        """
        # Placeholder implementation
        # Real implementation would use search API (Google, Bing, etc.)

        return [
            WebSearchResult(
                title=f"Result for: {query}",
                url="https://example.com/result",
                snippet="This is a placeholder result. Configure an API key for real search.",
                score=1.0
            )
        ]


class WebBrowserTool:
    """
    Web browser automation tool.

    Based on Claude Code's WebBrowserTool implementation.
    Note: Requires playwright installation for full functionality.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless

    def navigate(
        self,
        url: str,
        wait_for: Optional[str] = None,
        timeout: int = 30000
    ) -> WebFetchResult:
        """
        Navigate to URL and get content.

        Args:
            url: URL to navigate to
            wait_for: CSS selector to wait for
            timeout: Timeout in milliseconds

        Returns:
            WebFetchResult with page content
        """
        is_valid, error_msg = URLValidator.validate(url)
        if not is_valid:
            return WebFetchResult(
                success=False,
                error=error_msg,
                risk_level=RiskLevel.HIGH
            )

        # Placeholder - use WebFetchTool for basic fetching
        fetcher = WebFetchTool()
        return fetcher.fetch(url)

    def screenshot(self, url: str, path: str, full_page: bool = False) -> bool:
        """Take a screenshot of a page"""
        # Placeholder - requires playwright
        return False

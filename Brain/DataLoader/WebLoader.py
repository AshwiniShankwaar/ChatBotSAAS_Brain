from urllib.parse import urlparse
from langchain_core.documents import Document
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from Brain.DataLoader.Loader import Loader  # Import Loader
from Brain.Logger.logger import logger
from Brain.Exceptions.lodderError import lodderError
# Configure logging
class WebLoader(Loader):
    """
    Loads data from a web page, and optionally follows links to load content from linked pages.
    """
    def __init__(self, url: str, follow_links: bool = False, max_depth: int = 1):
        """
        Initialize the WebLoader.

        Args:
            url (str): The URL of the starting web page.
            follow_links (bool, optional): Whether to follow links on the page. Defaults to False.
            max_depth (int, optional):  Maximum depth to traverse links. Defaults to 1.
        """
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL: Must start with http:// or https://")
        if not isinstance(follow_links, bool):
            raise TypeError("follow_links must be a boolean")
        if not isinstance(max_depth, int) or max_depth < 1:
            raise ValueError("max_depth must be an integer greater than 0")

        self._url = url
        self._follow_links = follow_links
        self._max_depth = max_depth
        self._visited_urls = set()  # To keep track of visited URLs


    def _fetch_and_parse(self, url: str) -> BeautifulSoup:
        """
        Fetches the content of a URL and parses it with BeautifulSoup.

        Args:
            url (str): The URL to fetch.

        Returns:
            BeautifulSoup: The parsed HTML content.

        Raises:
            lodderError: If there is an error fetching or parsing the URL.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise lodderError(f"Error fetching URL: {e}", source=url)
        except Exception as e:
            raise lodderError(f"Error parsing URL: {e}", source=url)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """
        Extracts links from a BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The parsed HTML content.
            base_url (str):  The base URL to resolve relative URLs.

        Returns:
            List[str]: A list of absolute URLs.
        """
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            # Construct an absolute URL if the href is relative
            absolute_url = urljoin(base_url, href)
            # Basic filtering to avoid mailto:, etc. and ensure it is http or https
            if absolute_url.startswith("http://") or absolute_url.startswith("https://"):
                links.append(absolute_url)
        return links

    def _load_page(self, url: str, depth: int) -> list[Document]:
        """
        Loads a single page and recursively loads linked pages if follow_links is True.

        Args:
            url (str): The URL of the page to load.
            depth (int): The current depth of recursion.

        Returns:
            List[Document]: A list of LangChain Document objects.
        """
        if url in self._visited_urls:
            logger.debug(f"Skipping already visited URL: {url}")
            return []  # Return empty list for visited URLs

        self._visited_urls.add(url) # Add URL to visited set
        logger.info(f"Loading URL: {url}, Depth: {depth}")

        try:
            soup = self._fetch_and_parse(url)
            text_content = soup.get_text(separator=' ').strip()
            metadata = {"source": url}  # Include URL in metadata
            page_document = Document(page_content=text_content, metadata=metadata)
            documents = [page_document] # Start with the current page

            if self._follow_links and depth < self._max_depth:
                links = self._extract_links(soup, url)
                for link in links:
                    documents.extend(self._load_page(link, depth + 1)) # Recursive call

            return documents

        except lodderError as e:
            logger.error(f"Error loading {url}: {e}")
            return [] # Return empty list on error, continue loading other pages

    def load(self) -> list[Document]:
        """
        Loads the web page(s) and returns the data as LangChain Document objects.

        Returns:
            List[Document]: A list of LangChain Document objects.
        """
        return self._load_page(self._url, 1) # Start loading from the initial URL


    @property
    def source(self) -> str:
        """
        Returns the source of the data being loaded.

        Returns:
            str: The URL of the web page.
        """
        return self._url
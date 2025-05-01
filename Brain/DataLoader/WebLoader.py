from urllib.parse import urljoin
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
from Brain.DataLoader.Loader import Loader
from Logger import logger
from Brain.Exceptions.lodderError import lodderError

class WebLoader(Loader):
    """
    Loads data from a web page, and optionally follows links to load content from linked pages.
    """

    def __init__(self, url: str, follow_links: bool = False, max_depth: int = 1):
        logger.info(f"Initializing WebLoader for URL: {url}")
        if not isinstance(url, str):
            logger.error("URL must be a string.")
            raise TypeError("url must be a string")
        if not url.startswith("http://") and not url.startswith("https://"):
            logger.error("Invalid URL format. Must start with http:// or https://")
            raise ValueError("Invalid URL: Must start with http:// or https://")
        if not isinstance(follow_links, bool):
            logger.error("follow_links must be a boolean.")
            raise TypeError("follow_links must be a boolean")
        if not isinstance(max_depth, int) or max_depth < 1:
            logger.error("max_depth must be an integer greater than 0.")
            raise ValueError("max_depth must be an integer greater than 0")

        self._url = url
        self._follow_links = follow_links
        self._max_depth = max_depth
        self._visited_urls = set()
        logger.info(f"WebLoader initialized with follow_links={follow_links}, max_depth={max_depth}")

    def _fetch_and_parse(self, url: str) -> BeautifulSoup:
        logger.info(f"Fetching and parsing URL: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully fetched URL: {url}")
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for URL {url}: {e}")
            raise lodderError(f"Error fetching URL: {e}", source=url)
        except Exception as e:
            logger.error(f"Parsing failed for URL {url}: {e}")
            raise lodderError(f"Error parsing URL: {e}", source=url)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        logger.info(f"Extracting links from base URL: {base_url}")
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            absolute_url = urljoin(base_url, href)
            if absolute_url.startswith("http://") or absolute_url.startswith("https://"):
                links.append(absolute_url)
        logger.info(f"Extracted {len(links)} links from {base_url}")
        return links

    def _load_page(self, url: str, depth: int) -> list[Document]:
        if url in self._visited_urls:
            logger.debug(f"Skipping already visited URL: {url}")
            return []

        self._visited_urls.add(url)
        logger.info(f"Loading page at depth {depth}: {url}")

        try:
            soup = self._fetch_and_parse(url)
            text_content = soup.get_text(separator=' ').strip()
            metadata = {"source": url}
            page_document = Document(page_content=text_content, metadata=metadata)
            documents = [page_document]

            logger.info(f"Page loaded and converted to Document: {url}")

            if self._follow_links and depth < self._max_depth:
                logger.info(f"Following links on: {url} (depth {depth})")
                links = self._extract_links(soup, url)
                for link in links:
                    documents.extend(self._load_page(link, depth + 1))

            return documents

        except lodderError as e:
            logger.error(f"Error loading {url}: {e}")
            return []

    def load(self) -> list[Document]:
        logger.info(f"Starting to load from root URL: {self._url}")
        documents = self._load_page(self._url, 1)
        logger.info(f"Total documents loaded from web: {len(documents)}")
        return documents

    @property
    def source(self) -> str:
        return self._url

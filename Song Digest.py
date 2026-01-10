import requests
from bs4 import BeautifulSoup


def convert_url(url: str) -> str:
    """
    Collects raw HTML from a URL and returns it as a string.
    """

    response = requests.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")  # use html, not response
    return soup.get_text()


def Wikipedia_Digest(text: str) -> str:
    """
    Digests the text from Wikipedia and returns it prettier.
    Ignored references, headers and pre-vte.
    """

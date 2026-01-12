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
    text = soup.get_text()

    return text


def clean_list(text_list: list[str]) -> list[str]:
    """
    Clean a list for non-alpha characters.
    >>> clean_list(['!#!@', 'ABC', 'Hello'])
    ['ABC', 'Hello']
    """

    cleaned_list = []

    for word in text_list:
        if word.isalpha():
            cleaned_list.append(word)

    return cleaned_list


def wikipedia_digest(text: str) -> list[str]:
    """
    Digests the text from Wikipedia and returns it prettier.
    Ignored references, headers and pre-vte.
    """

    text_list = text.split()
    index_vte = 0
    index_reference = len(text_list)

    for word in text_list:
        if word == 'vte':
            index_vte = text_list.index(word)
        elif word == 'references':
            index_reference = text_list.index(word)
            break

    return text_list[index_vte + 1 : index_reference]

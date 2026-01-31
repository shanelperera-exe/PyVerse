from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin, urlparse


def parse(html):
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else "No Title"
    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())

    return {
        "title": title,
        "word_count": word_count,
    }

def extract_links(html, base_url):
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not href:
            continue

        absolute = urljoin(base_url, href)
        absolute, _frag = urldefrag(absolute)

        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        if not parsed.netloc:
            continue

        links.append(absolute)

    return links

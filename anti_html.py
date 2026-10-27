"""Fetch a webpage and return readable text from its HTML."""
import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def anti_html(url: str, timeout: float = 15) -> str:
    """Return page text; raise ValueError or RequestException on failure."""
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("URL must be an absolute http:// or https:// URL")

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def main() -> int:
    """Parse the URL argument and print extracted page text."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Absolute webpage URL")
    args = parser.parse_args()
    try:
        print(anti_html(args.url))
    except (requests.exceptions.RequestException, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import requests
from bs4 import BeautifulSoup

def anti_html(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n", strip=True)

url = input("Enter URL: ")

try:
    print(anti_html(url))
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
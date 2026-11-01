
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

URL = "https://www.berlin-chemie.de/de.html"
DOMAIN = urlparse(URL).netloc

def main():
    print("=== Berlin-Chemie OSINT Harvester ===")
    print(f"Quelle: {URL}")
    print("Lade Webseite ...")

    try:
        response = requests.get(
            URL,
            headers={"User-Agent": "Uni-OSINT-Project/1.0"},
            timeout=10
        )
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Fehler beim Abrufen: {error}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Seitentitel
    title = soup.title.get_text(strip=True) if soup.title else "Kein Titel"

    print(f"\nSeitentitel: {title}")

    # Überschriften sammeln
    headings = soup.find_all(["h1", "h2", "h3"])

    print(f"\n=== Überschriften ({len(headings)}) ===")

    for heading in headings[:20]:
        text = heading.get_text(" ", strip=True)
        if text:
            print(f"- {text}")

    # Interne Links sammeln
    internal_links = set()

    for link in soup.find_all("a", href=True):
        full_url = urljoin(URL, link["href"])
        parsed = urlparse(full_url)

        if (
            parsed.scheme in ("http", "https")
            and parsed.netloc == DOMAIN
        ):
            internal_links.add(full_url)

    print(f"\n=== Interne Links ({len(internal_links)}) ===")

    for link in sorted(internal_links)[:30]:
        print(link)

    print("\nFertig. Es wurde nur eine Seite abgerufen.")


if __name__ == "__main__":
    main()

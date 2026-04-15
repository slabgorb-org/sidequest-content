#!/usr/bin/env python3
"""Download large ukiyo-e Baido Hosai images from ukiyo-e.org search results."""

import os
import time
import urllib.request
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

BASE_URL = "https://ukiyo-e.org/search?q=Baido%20Hosai"
DATA_PREFIX = "https://data.ukiyo-e.org/"
OUT_DIR = "/Users/keithavery/Downloads/ukiyo-e-portraits"


class ImgSrcParser(HTMLParser):
    """Extract all img src attributes matching data.ukiyo-e.org thumbs."""
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for name, value in attrs:
                if name == "src" and value and "data.ukiyo-e.org" in value and "/thumbs/" in value:
                    self.urls.append(value)


def fetch_page(start: int) -> str:
    url = f"{BASE_URL}&start={start}" if start > 0 else BASE_URL
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def thumb_to_large(thumb_url: str) -> str:
    return thumb_url.replace("/thumbs/", "/images/")


def safe_filename(url: str) -> str:
    parts = url.replace(DATA_PREFIX, "").split("/")
    source = parts[0]
    fname = parts[-1]
    return f"{source}_{fname}"


def download_image(url: str, filepath: str) -> bool:
    if os.path.exists(filepath):
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(filepath, "wb") as f:
            f.write(data)
        return True
    except (HTTPError, URLError, TimeoutError) as e:
        print(f"  FAILED: {url} — {e}")
        return False


def main():
    # First page only (100 max)
    print("Scraping first page ...")
    html = fetch_page(0)
    parser = ImgSrcParser()
    parser.feed(html)
    all_thumbs = parser.urls
    print(f"  Found {len(all_thumbs)} images")

    success = 0
    fail = 0
    for i, thumb in enumerate(all_thumbs, 1):
        large_url = thumb_to_large(thumb)
        fname = safe_filename(large_url)
        filepath = os.path.join(OUT_DIR, fname)
        print(f"[{i}/{len(all_thumbs)}] {fname}")
        if download_image(large_url, filepath):
            success += 1
        else:
            fail += 1
        if i % 20 == 0:
            time.sleep(0.3)

    print(f"\nDone! {success} downloaded, {fail} failed.")


if __name__ == "__main__":
    main()

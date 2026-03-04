#!/usr/bin/env python3
import json, re, sys, datetime, urllib.request
from urllib.error import URLError, HTTPError

FRONTIERS_DOIS = [
  "10.3389/fpubh.2025.1695850",
  "10.3389/fsufs.2023.1091346"
]

# Map DOI -> Frontiers full-text URL pattern
def frontiers_url(doi: str) -> str:
    # DOI suffix after 10.3389/
    suffix = doi.split("10.3389/")[-1]
    # journal slug is embedded in suffix like fpubh.2025.1695850
    # we don't need journal slug because Frontiers uses canonical "articles/<doi>/full"
    return f"https://www.frontiersin.org/articles/{doi}/full"

def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; AIMM-metrics-bot/1.0; +https://aimm.ai)"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def extract_views(html: str) -> int | None:
    # Try to find the "Article metrics" section and a "Views" value nearby.
    # This is intentionally conservative: if pattern fails, return None.
    # Common patterns include "Article metrics" then "Views" then a number with commas.
    # We'll search within a window after "Article metrics".
    m = re.search(r"Article metrics(.{0,20000})", html, flags=re.IGNORECASE | re.DOTALL)
    chunk = m.group(1) if m else html

    # Look for Views followed by a number
    m2 = re.search(r"\bViews\b[^0-9]{0,40}([0-9][0-9,\. ]{0,15})", chunk, flags=re.IGNORECASE)
    if not m2:
        return None
    raw = m2.group(1)
    raw = raw.replace(" ", "").replace(".", "")
    raw = raw.replace(",", "")
    try:
        return int(raw)
    except ValueError:
        return None

def main():
    metrics_path = sys.argv[1] if len(sys.argv) > 1 else "assets/frontiers_metrics.json"
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
    except FileNotFoundError:
        metrics = {}

    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    for doi in FRONTIERS_DOIS:
        url = frontiers_url(doi)
        try:
            html = fetch_html(url)
            views = extract_views(html)
        except (URLError, HTTPError) as e:
            views = None

        if doi not in metrics:
            metrics[doi] = {}
        if views is not None:
            metrics[doi]["views"] = views
        metrics[doi]["updated_utc"] = now

    # Keep other DOIs untouched if present
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json, re, sys, datetime, urllib.request
from urllib.error import URLError, HTTPError

FRONTIERS_DOIS = [
  "10.3389/fpubh.2025.1695850",
  "10.3389/fsufs.2023.1091346"
]

def frontiers_url(doi: str) -> str:
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

def extract_views(html: str):
    m = re.search(r"Article metrics(.{0,20000})", html, flags=re.IGNORECASE | re.DOTALL)
    chunk = m.group(1) if m else html
    m2 = re.search(r"\bViews\b[^0-9]{0,80}([0-9][0-9,\. ]{0,18})", chunk, flags=re.IGNORECASE)
    if not m2:
        return None
    raw = m2.group(1).replace(" ", "").replace(".", "").replace(",", "")
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
        except (URLError, HTTPError):
            views = None

        metrics.setdefault(doi, {})
        if views is not None:
            metrics[doi]["views"] = views
        metrics[doi]["updated_utc"] = now

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

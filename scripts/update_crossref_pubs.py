#!/usr/bin/env python3
import json, sys, datetime, urllib.request, urllib.parse
from urllib.error import URLError, HTTPError

CROSSREF = "https://api.crossref.org/works/"

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent":"AIMM-website/1.0 (mailto: ravi.bhavnani@iheid.ch)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    pubs_path = sys.argv[1] if len(sys.argv) > 1 else "assets/pubs.json"
    with open(pubs_path, "r", encoding="utf-8") as f:
        pubs = json.load(f)

    items = pubs.get("items", [])
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    for pub in items:
        doi = pub.get("doi")
        if not doi:
            continue
        url = CROSSREF + urllib.parse.quote(doi)
        try:
            j = fetch_json(url)
            pub["crossref_message"] = j.get("message", {})
        except (URLError, HTTPError, json.JSONDecodeError):
            pub.setdefault("crossref_message", {})

    pubs["updated_utc"] = now
    with open(pubs_path, "w", encoding="utf-8") as f:
        json.dump(pubs, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

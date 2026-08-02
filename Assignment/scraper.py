"""
scraper.py
----------
Real-world review scraper for Flipkart product review pages.

IMPORTANT ARCHITECTURE NOTE:
Flipkart's product/review pages are rendered with a React (React Native Web)
frontend that uses auto-generated, non-semantic "atomic" CSS classes
(e.g. class="css-146c3p1 r-1c4vpko ..."). These class names are unstable and
regenerate on every build, so they CANNOT be used as reliable CSS selectors.

Instead, Flipkart's server-rendered HTML embeds the page's full data as a
JSON blob inside a <script> tag:

    <script id="is_script">window.__INITIAL_STATE__ = {...huge JSON...};</script>

This script extracts and parses that JSON directly and pulls review objects
(type "ProductReviewValue") out of it. This is far more robust than scraping
HTML/CSS, and survives Flipkart's frontend redesigns as long as they keep
using this embedded-state pattern.

Usage:
    pip install requests beautifulsoup4 pandas
    python scraper.py --url "https://www.flipkart.com/<product>/product-reviews/<id>" \
                       --pages 10 --out reviews_scraped.csv

Notes:
- Run this on YOUR own machine (not in a sandboxed/offline environment) since
  it needs live internet access to flipkart.com.
- Respect the site's robots.txt and Terms of Service. A delay is added
  between requests (--delay, default 2s) — do not remove it.
- Output matches the schema of data/reviews.csv: product_name, rating,
  review_text, sentiment (so it drops straight into the existing pipeline).
"""

import argparse
import json
import re
import time
import pandas as pd
import requests

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36")
}

SCRIPT_VERSION = "v3-recursive-search"

STATE_MARKER = "window.__INITIAL_STATE__ = "


def rating_to_sentiment(rating):
    try:
        r = int(rating)
    except (TypeError, ValueError):
        return "unknown"
    if r >= 4:
        return "positive"
    elif r <= 2:
        return "negative"
    return "neutral"


def extract_initial_state(html):
    """Pull the window.__INITIAL_STATE__ JSON object out of the raw HTML
    using brace-balancing (handles nested braces / braces inside strings)."""
    start = html.find(STATE_MARKER)
    if start == -1:
        return None
    start += len(STATE_MARKER)

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(html)):
        ch = html[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return html[start:i + 1]
    return None


def extract_product_name(state):
    """Best-effort product name lookup: recursively search for a 'tracking'
    dict with a 'title' field, since exact nesting can vary by page/variant."""
    found = {"name": None}

    def walk(node):
        if found["name"]:
            return
        if isinstance(node, dict):
            tracking = node.get("tracking")
            if isinstance(tracking, dict) and tracking.get("title"):
                found["name"] = tracking["title"]
                return
            for v in node.values():
                walk(v)
                if found["name"]:
                    return
        elif isinstance(node, list):
            for item in node:
                walk(item)
                if found["name"]:
                    return

    walk(state)
    return found["name"] or "Unknown Product"


def find_reviews_in_state(state):
    """Recursively search the ENTIRE state tree for any dict with
    type == "ProductReviewValue", regardless of exact nesting path.
    This is deliberately path-independent: Flipkart's nesting under
    pageDataResponse/widgetsData/slots can vary by page, A/B test variant,
    or future redesign, but the review objects themselves keep this
    'type' marker, making them easy to find anywhere in the tree."""
    reviews = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "ProductReviewValue":
                title = node.get("title") or ""
                body = node.get("text") or ""
                full_text = (title + ". " + body).strip(". ").strip()
                reviews.append({
                    "rating": node.get("rating"),
                    "review_text": full_text,
                    "author": node.get("author"),
                    "created": node.get("created"),
                    "certifiedBuyer": node.get("certifiedBuyer"),
                })
                return  # review objects aren't nested inside each other
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(state)
    return reviews


def scrape_reviews(base_url, pages=5, delay=2.0, debug=True):
    all_rows = []
    product_name = None

    for page in range(1, pages + 1):
        url = base_url + (f"&page={page}" if "?" in base_url else f"?page={page}")
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if debug:
            print(f"[debug] page {page} -> status {resp.status_code}, html length {len(resp.text)}")

        if resp.status_code != 200:
            print(f"Stopping: status {resp.status_code} on page {page}")
            break

        raw_json = extract_initial_state(resp.text)
        if not raw_json:
            print(f"[debug] window.__INITIAL_STATE__ not found on page {page}.")
            if page == 1:
                with open("debug_page1.html", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                print("[debug] Saved raw HTML to debug_page1.html for inspection.")
            break

        try:
            state = json.loads(raw_json)
        except json.JSONDecodeError as e:
            print(f"[debug] Failed to parse extracted JSON on page {page}: {e}")
            break

        if product_name is None:
            product_name = extract_product_name(state)

        page_reviews = find_reviews_in_state(state)

        if debug:
            print(f"[debug] found {len(page_reviews)} reviews via __INITIAL_STATE__ on page {page}")
            if not page_reviews:
                marker_count = raw_json.count("ProductReviewValue")
                print(f"[debug] 'ProductReviewValue' appears {marker_count} times in the raw JSON "
                      f"(0 = Flipkart likely changed the data shape; >0 = a bug in this script's "
                      f"walk logic — please report the page URL).")

        if not page_reviews:
            print(f"No more reviews found at page {page}, stopping.")
            break

        for r in page_reviews:
            all_rows.append({
                "product_name": product_name,
                "rating": r["rating"],
                "review_text": r["review_text"],
                "sentiment": rating_to_sentiment(r["rating"]),
            })

        print(f"Page {page}: collected {len(page_reviews)} reviews (total {len(all_rows)})")
        time.sleep(delay)  # be polite to the server

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Flipkart product-reviews page URL")
    parser.add_argument("--pages", type=int, default=5)
    parser.add_argument("--out", default="reviews_scraped.csv")
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()

    print(f"[scraper.py version: {SCRIPT_VERSION}]")

    df = scrape_reviews(args.url, pages=args.pages, delay=args.delay)

    if df.empty or "review_text" not in df.columns:
        print("\nNo reviews were extracted. Check debug_page1.html (saved next to this")
        print("script, if page 1 returned no data) and verify the URL is a genuine")
        print("Flipkart product-reviews page that loads correctly in a normal browser.")
    else:
        # basic cleaning: drop empty/duplicate reviews
        df["review_text"] = df["review_text"].astype(str).str.strip()
        df = df[df["review_text"].str.len() > 0]
        df.drop_duplicates(subset="review_text", inplace=True)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} reviews to {args.out}")

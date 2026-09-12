import argparse
import html
import os
import re
from datetime import datetime, timezone

import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", value)
    return value.strip("-_") or "post"


def extract_title(html_text: str) -> str:
    match = re.search(
        r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>',
        html_text,
        re.DOTALL,
    )
    if not match:
        match = re.search(r'<meta property="og:title" content="([^"]+)"', html_text)
    if not match:
        return "Untitled"
    value = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(value).strip() or "Untitled"


def extract_publish_date(html_text: str) -> str:
    match = re.search(r"create_time:\s*['\"]([\d\- :]+)['\"]", html_text)
    if not match:
        return datetime.now(timezone.utc).date().isoformat()
    return match.group(1).strip().split()[0]


def fetch_metadata(url: str) -> tuple[str, str]:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return extract_title(response.text), extract_publish_date(response.text)


def build_post(title: str, source_url: str) -> str:
    escaped_title = title.replace("\\", "\\\\").replace('"', '\\"')
    return f'''---
title: "{escaped_title}"
categories:
  - WeChat
tags:
  - 公众号
source: "{source_url}"
---
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Import WeChat article metadata into a Jekyll post.")
    parser.add_argument("url", help="WeChat article URL")
    args = parser.parse_args()

    os.makedirs("_posts", exist_ok=True)
    title, date = fetch_metadata(args.url)
    path = f"_posts/{date}-{slugify(title)}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(build_post(title, args.url))

    print(f"Created {path}")


if __name__ == "__main__":
    main()

import argparse
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", value)
    return value.strip("-_") or "post"


def download_image(url: str, path: str) -> bool:
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        return True
    except Exception:
        return False


def save_images(html_node, date: str, slug: str) -> None:
    output_dir = "images/wechat"
    os.makedirs(output_dir, exist_ok=True)

    for index, img in enumerate(html_node.find_all("img"), start=1):
        source = img.get("data-src") or img.get("src")
        if not source or not source.startswith("http"):
            continue

        suffix = os.path.splitext(urlparse(source).path)[1]
        if not suffix:
            suffix = ".jpg"

        filename = f"{date}-{slug}-{index}{suffix}"
        local_path = os.path.join(output_dir, filename)
        local_url = f"/images/wechat/{filename}"

        if download_image(source, local_path):
            img["src"] = local_url


def fetch_article(url: str) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title_node = soup.select_one("#activity-name") or soup.select_one("h1")
    account_node = soup.select_one("#js_name")
    content_node = soup.select_one("#js_content") or soup.select_one(".rich_media_content")

    if content_node is None:
        raise RuntimeError("Could not locate article content. WeChat may require a valid article URL.")

    title = title_node.get_text(" ", strip=True) if title_node else "Untitled"
    account = account_node.get_text(" ", strip=True) if account_node else ""
    date = datetime.now(timezone.utc).date().isoformat()
    slug = slugify(title)

    save_images(content_node, date, slug)
    content_md = md(str(content_node), heading_style="ATX")
    content_md = re.sub(r"\n{3,}", "\n\n", content_md).strip()

    return {
        "title": title,
        "account": account,
        "date": date,
        "slug": slug,
        "content": content_md,
    }


def build_post(data: dict, source_url: str) -> str:
    escaped_title = data["title"].replace("\\", "\\\\").replace('"', '\\"')
    return f'''---
title: "{escaped_title}"
categories:
  - WeChat
tags:
  - 公众号
source: "{source_url}"
---

{data["content"]}
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a WeChat article into a Jekyll post.")
    parser.add_argument("url", help="WeChat article URL")
    args = parser.parse_args()

    data = fetch_article(args.url)
    path = f'_posts/{data["date"]}-{data["slug"]}.md'
    if os.path.exists(path):
        base, ext = os.path.splitext(path)
        index = 2
        while os.path.exists(f"{base}-{index}{ext}"):
            index += 1
        path = f"{base}-{index}{ext}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(build_post(data, args.url))

    print(f"Created {path}")


if __name__ == "__main__":
    main()

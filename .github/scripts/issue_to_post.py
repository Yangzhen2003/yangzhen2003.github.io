import os
import re
from datetime import datetime, timezone


title = os.environ["ISSUE_TITLE"].strip()
body = os.environ["ISSUE_BODY"].strip()

slug = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", title.lower()).strip("-_") or "post"
date = datetime.now(timezone.utc).date().isoformat()
path = f"_posts/{date}-{slug}.md"

if os.path.exists(path):
    base, ext = os.path.splitext(path)
    index = 2
    while os.path.exists(f"{base}-{index}{ext}"):
        index += 1
    path = f"{base}-{index}{ext}"

title_escaped = title.replace("\\", "\\\\").replace('"', '\\"')
content = f'''---
title: "{title_escaped}"
categories:
  - Blog
tags:
  - blog
---

{body}
'''

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Created {path}")

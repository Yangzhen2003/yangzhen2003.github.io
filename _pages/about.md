---
permalink: /
title: "About Me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

Here is **Yang Zhen**. I am a first-year master's student in Journalism and Communication at Nanjing University, with a focus on computational communication.

I am currently studying computational social science, with particular interest in using computational methods to understand media, communication, and narrative.

Before Nanjing University, I received my bachelor's degree in Journalism from Jinan University from 2021 to 2025.

## Research Interests

- Computational Communication
- Computational Narrative
- Computational Social Science

## Education

- **M.A. in Journalism and Communication**, Nanjing University, 2026 - present
- **B.A. in Journalism**, Jinan University, 2021 - 2025

## Contact

- GitHub: [Yangzhen2003](https://github.com/Yangzhen2003)
- Email: [{{ site.author.email }}](mailto:{{ site.author.email }})

## Recent posts

{% for post in site.posts limit:3 %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>{{ post.date | date: "%Y-%m-%d" }}</small>
{% endfor %}

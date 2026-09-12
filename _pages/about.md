---
permalink: /
title: "Hi, I'm Yang Zhen"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I'm Yang Zhen, a student at Nanjing University. This site is where I share my study notes, projects, and occasional thoughts.

## Recent posts

{% for post in site.posts limit:3 %}
- [{{ post.title }}]({{ post.url | relative_url }}) <small>{{ post.date | date: "%Y-%m-%d" }}</small>
{% endfor %}

## Contact

- GitHub: [Yangzhen2003](https://github.com/Yangzhen2003)
- Email: [{{ site.author.email }}](mailto:{{ site.author.email }})
- WeChat: {{ site.author.wechat }}

---
layout: archive
title: "Blog"
permalink: /blog/
author_profile: true
---

{% if site.posts.size > 0 %}
<div class="blog-list">
  {% for post in site.posts %}
  {% assign target = post.source | default: post.url %}
  <article class="blog-card">
    <a class="blog-card__title" href="{{ target }}"{% if post.source %} target="_blank" rel="noopener"{% endif %}>{{ post.title }}</a>
    <div class="blog-card__meta">{{ post.date | date: "%Y-%m-%d" }}</div>
    <p class="blog-card__excerpt">{{ post.excerpt | strip_html | truncate: 140 }}</p>
    <a class="blog-card__more" href="{{ target }}"{% if post.source %} target="_blank" rel="noopener"{% endif %}>{% if post.source %}Read on WeChat{% else %}Read More{% endif %}</a>
  </article>
  {% endfor %}
</div>
{% else %}
<p class="blog-empty">No posts yet.</p>
{% endif %}

<p><a class="blog-card__more" href="https://github.com/Yangzhen2003/yangzhen2003.github.io/issues/new?template=blog-post.yml">Create a New Post</a></p>
<p><a class="blog-card__more" href="https://github.com/Yangzhen2003/yangzhen2003.github.io/issues/new?template=wechat-import.yml">Import from WeChat</a></p>

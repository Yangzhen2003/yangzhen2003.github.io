---
layout: archive
title: "Blog"
permalink: /blog/
author_profile: true
---

{% if site.posts.size > 0 %}
<div class="blog-list">
  {% for post in site.posts %}
  <article class="blog-card">
    <a class="blog-card__title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <div class="blog-card__meta">{{ post.date | date: "%Y-%m-%d" }}</div>
    <p class="blog-card__excerpt">{{ post.excerpt | strip_html | truncate: 140 }}</p>
    <a class="blog-card__more" href="{{ post.url | relative_url }}">Read More</a>
  </article>
  {% endfor %}
</div>
{% else %}
<p class="blog-empty">No posts yet.</p>
{% endif %}

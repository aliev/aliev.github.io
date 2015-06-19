---
layout: page
title: Archive
---

## Blog Posts

{% for post in site.posts %}
  * {{ post.date | date_to_string }}&raquo; [ {{ post.title }} ]({{ post.url }}) {% if post.category %} ({{post.category}}) {% endif %}
{% endfor %}

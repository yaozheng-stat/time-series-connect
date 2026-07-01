---
layout: single
title: Education Blog
permalink: /education-blog/
---

We aim to make time series research more approachable. Posts are written by students under faculty mentorship and provide accessible explanations, brief literature context, and resources for further learning.

<div class="education-index">
  {% assign posts = site.education | sort: "date" | reverse %}
  {% if posts.size > 0 %}
    {% for post in posts %}
      <article class="education-card">
        <p class="education-card__meta">
          {% if post.date %}{{ post.date | date: "%B %-d, %Y" }}{% endif %}
          {% if post.author %} · By {{ post.author }}{% endif %}
          {% if post.reading_time %} · {{ post.reading_time }}{% endif %}
        </p>
        <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
        {% if post.summary %}<p>{{ post.summary }}</p>{% endif %}
        {% if post.topics %}
          <div class="education-topic-list">
            {% for topic in post.topics %}<span>{{ topic }}</span>{% endfor %}
          </div>
        {% endif %}
        <a class="education-read-more" href="{{ post.url | relative_url }}">Read more</a>
      </article>
    {% endfor %}
  {% else %}
    <p>No education posts have been published yet.</p>
  {% endif %}
</div>

**Students:** If you’re interested in developing your scientific writing, deepening your understanding of time series or data science research, and contributing to the blog, contact us at [timeseriesconnect@gmail.com](mailto:timeseriesconnect@gmail.com).

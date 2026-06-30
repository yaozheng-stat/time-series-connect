---
layout: single
title: Past Webinar Archive
permalink: /webinars/archive/
---
{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign webinars = site.webinars | sort: 'date' | reverse %}
<div class="webinar-list">
{% assign count = 0 %}
{% for webinar in webinars %}
  {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
  {% if webinar_date < today %}
    {% assign count = count | plus: 1 %}
    <article class="webinar-item">
      <div><p class="date">{{ webinar.date | date: "%b %-d, %Y" }}</p>{% if webinar.time %}<p class="muted">{{ webinar.time }}</p>{% endif %}</div>
      <div><h2><a href="{{ webinar.url | relative_url }}">{{ webinar.title }}</a></h2><p><strong>{{ webinar.speaker }}</strong>{% if webinar.affiliation %}, {{ webinar.affiliation }}{% endif %}</p><p>{{ webinar.excerpt | strip_html | truncate: 180 }}</p></div>
    </article>
  {% endif %}
{% endfor %}
{% if count == 0 %}
<p>No past webinars are listed yet.</p>
{% endif %}
</div>

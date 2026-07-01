---
layout: single
title: Upcoming Webinars
permalink: /webinars/upcoming/
---

<section class="format-note upcoming-format">
  <h2>Format</h2>
  <p>Sessions run about 55 minutes, typically a 45-minute presentation followed by 10 minutes of discussion. We welcome multiple speakers on a shared theme as well as panel formats.</p>
  <p>Each event often ends with a 30-minute Virtual Coffee, where participants can chat, ask questions, and connect. Everyone’s welcome, even if they missed the main talk!</p>
</section>

{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign webinars = site.webinars | sort: 'date' %}
{% assign upcoming_abstract_limit = 220 %}
<div class="upcoming-event-list">
{% assign count = 0 %}
{% for webinar in webinars %}
  {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
  {% if webinar_date >= today %}
    {% assign count = count | plus: 1 %}
    {% include webinar_card.html webinar=webinar mode="upcoming" abstract_limit=upcoming_abstract_limit %}
  {% endif %}
{% endfor %}
{% if count == 0 %}
  <div class="upcoming-empty-state">
    <p>We'll be back with webinars in Fall 2026.</p>
  </div>
{% endif %}
</div>

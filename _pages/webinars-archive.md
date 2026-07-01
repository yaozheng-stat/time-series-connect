---
layout: single
title: Past Webinar Archive
permalink: /webinars/archive/
---
<p class="archive-intro">Browse previous Time Series Connect webinars. Each entry includes the event date and time, title, abstract, speaker website, available materials, and recording link.</p>

{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign webinars = site.webinars | sort: 'date' | reverse %}
{% assign archive_abstract_limit = 220 %}
<div class="archive-event-list">
{% assign count = 0 %}
{% for webinar in webinars %}
  {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
  {% if webinar_date < today %}
    {% assign count = count | plus: 1 %}
    {% include webinar_card.html webinar=webinar mode="archive" abstract_limit=archive_abstract_limit %}
  {% endif %}
{% endfor %}
{% if count == 0 %}
  <div class="archive-empty-state">
    <p>No past webinars are listed yet. Past events will appear here automatically after their webinar document date has passed.</p>
  </div>
{% endif %}
</div>

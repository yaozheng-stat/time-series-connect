---
layout: single
title: Upcoming Webinars
permalink: /webinars/upcoming/
---
<section class="format-note">
  <h2>Format</h2>
  <p>We host a mix of academic talks, panels, and interactive sessions that connect ideas from research, industry, and government. Sessions run about 55 minutes, typically a 45-minute presentation followed by 10 minutes of discussion. We welcome multiple speakers on a shared theme as well as panel formats. In addition to academic talks, we also invite presentations from industry and public-sector professionals to showcase real-world applications of time series analysis and encourage cross-sector dialogue.</p>
  <p>Each event often ends with a 30-minute Virtual Coffee, where participants can chat, ask questions, and connect. It might be open networking or a light interview-style chat with the speaker(s). Everyone’s welcome, even if they missed the main talk!</p>
</section>

{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign webinars = site.webinars | sort: 'date' %}
<div class="webinar-list">
{% assign count = 0 %}
{% for webinar in webinars %}
  {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
  {% if webinar_date >= today %}
    {% assign count = count | plus: 1 %}
    <article class="webinar-item">
      <div><p class="date">{{ webinar.date | date: "%b %-d, %Y" }}</p>{% if webinar.time %}<p class="muted">{{ webinar.time }}</p>{% endif %}</div>
      <div><h2><a href="{{ webinar.url | relative_url }}">{{ webinar.title }}</a></h2><p><strong>{{ webinar.speaker }}</strong>{% if webinar.affiliation %}, {{ webinar.affiliation }}{% endif %}</p><p>{{ webinar.excerpt | strip_html | truncate: 180 }}</p></div>
    </article>
  {% endif %}
{% endfor %}
{% if count == 0 %}
<p>No upcoming webinars are currently listed. Add a future-dated Markdown file to <code>_webinars/</code> and it will appear here automatically.</p>
{% endif %}
</div>

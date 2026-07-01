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
    <article class="upcoming-event-card">
      <div class="upcoming-event-card__date" aria-label="{{ webinar.date | date: '%B %-d, %Y' }}">
        <span class="upcoming-event-card__month">{{ webinar.date | date: "%b" }}</span>
        <span class="upcoming-event-card__day">{{ webinar.date | date: "%d" }}</span>
        <span class="upcoming-event-card__year">{{ webinar.date | date: "%Y" }}</span>
      </div>
      <div class="upcoming-event-card__body">
        <div class="upcoming-event-card__meta">
          {% if webinar.time %}<span>{{ webinar.time }}</span>{% endif %}
        </div>
        <h2><a href="{{ webinar.url | relative_url }}">{{ webinar.title }}</a></h2>
        {% include webinar_speaker.html webinar=webinar class="upcoming-event-card__speaker" %}
        {% include archive_abstract.html webinar=webinar limit=upcoming_abstract_limit %}
        <div class="upcoming-event-card__actions">
          {% include webinar_buttons.html webinar=webinar primary_button_class="google-button" button_class="google-button outline" registration_label="Sign up" %}
        </div>
      </div>
    </article>
  {% endif %}
{% endfor %}
{% if count == 0 %}
  <div class="upcoming-empty-state">
    <p>No upcoming webinars are currently listed. Add a future-dated Markdown file to <code>_webinars/</code> and it will appear here automatically.</p>
  </div>
{% endif %}
</div>

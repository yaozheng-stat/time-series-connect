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
    {% assign display_title = webinar.title %}
    {% if webinar.title == "Seminar details forthcoming" and webinar.speaker and webinar.speaker != "" %}
      {% assign display_title = webinar.speaker %}
    {% endif %}
    <article class="archive-event-card">
      <div class="archive-event-card__date" aria-label="{{ webinar.date | date: '%B %-d, %Y' }}">
        <span class="archive-event-card__month">{{ webinar.date | date: "%b" }}</span>
        <span class="archive-event-card__day">{{ webinar.date | date: "%d" }}</span>
        <span class="archive-event-card__year">{{ webinar.date | date: "%Y" }}</span>
      </div>
      <div class="archive-event-card__body">
        <div class="archive-event-card__meta">
          {% if webinar.time and webinar.time != "" and webinar.time != "Time TBD" %}<span>{{ webinar.time }}</span>{% endif %}
        </div>
        <h2><a href="{{ webinar.url | relative_url }}">{{ display_title }}</a></h2>
        {% if webinar.speaker and webinar.speaker != "" and display_title != webinar.speaker %}
          <p class="archive-event-card__speaker"><strong>{{ webinar.speaker }}</strong>{% if webinar.affiliation and webinar.affiliation != "" %}, {{ webinar.affiliation }}{% endif %}</p>
        {% endif %}
        {% assign abstract_split = webinar.content | split: '<h2 id="abstract">Abstract</h2>' %}
        {% assign abstract_section = '' %}
        {% if abstract_split.size > 1 %}
          {% assign abstract_section = abstract_split[1] | split: '<h2 id="speaker-bio">Speaker Bio</h2>' | first %}
        {% endif %}
        {% assign archive_summary = abstract_section | default: webinar.excerpt | strip_html | normalize_whitespace %}
        {% if archive_summary.size > archive_abstract_limit %}
          <p>{{ archive_summary | truncate: archive_abstract_limit, "..." }}</p>
        {% else %}
          <p>{{ archive_summary }}</p>
        {% endif %}
        <div class="archive-event-card__actions">
          <a class="google-button" href="{{ webinar.url | relative_url }}">Event details</a>
          {% if webinar.speaker_url and webinar.speaker_url != "" %}
            <a class="google-button outline" href="{{ webinar.speaker_url }}" target="_blank" rel="noopener">Speaker Website</a>
          {% endif %}
          {% if webinar.youtube_url and webinar.youtube_url != "" %}
            <a class="google-button outline" href="{{ webinar.youtube_url }}" target="_blank" rel="noopener">Recording</a>
          {% endif %}
          {% if webinar.slides_url and webinar.slides_url != "" %}
            <a class="google-button outline" href="{{ webinar.slides_url }}" target="_blank" rel="noopener">Slides</a>
          {% endif %}
          {% if webinar.materials_url and webinar.materials_url != "" %}
            <a class="google-button outline" href="{{ webinar.materials_url }}" target="_blank" rel="noopener">{{ webinar.materials_label | default: "Materials" }}</a>
          {% endif %}
          {% if webinar.materials %}
            {% for material in webinar.materials %}
              <a class="google-button outline" href="{{ material.url }}" target="_blank" rel="noopener">{{ material.title | default: "Materials" }}</a>
            {% endfor %}
          {% endif %}
        </div>
      </div>
    </article>
  {% endif %}
{% endfor %}
{% if count == 0 %}
  <div class="archive-empty-state">
    <p>No past webinars are listed yet. Past events will appear here automatically after their webinar document date has passed.</p>
  </div>
{% endif %}
</div>
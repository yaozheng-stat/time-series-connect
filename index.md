---
layout: default
title: Home
---
<section class="google-section home-about">
  <div class="wrap home-about__grid">
    <div>
      <p class="eyebrow">About the series</p>
      <h2>Open to everyone, everywhere.</h2>
    </div>
    <div>
      <p>We are an online interdisciplinary seminar series that brings together researchers, practitioners, and students from fields such as statistics, computer science, economics, business, engineering, and other data-rich disciplines to share insights and advances in time series analysis.</p>
      <p> The series is hosted by the University of Connecticut in partnership with the Business and Economic Statistics Section of the American Statistical Association (ASA BES).</p>
      <p>You can watch recorded events on our <a href="https://www.youtube.com/@TimeSeriesConnect" target="_blank" rel="noopener">YouTube channel</a>.</p>
    </div>
  </div>
</section>

<section class="google-section alt home-events">
  <div class="wrap">
    <div class="section-heading">
      <p class="eyebrow">Upcoming webinars</p>
      <h2>Upcoming Events</h2>
    </div>

    {% assign today = site.time | date: '%Y-%m-%d' %}
    {% assign webinars = site.webinars | sort: 'date' %}
    {% assign upcoming_count = 0 %}
    <div class="home-event-list">
    {% for webinar in webinars %}
      {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
      {% if webinar_date >= today and webinar.published != false %}
        {% assign upcoming_count = upcoming_count | plus: 1 %}
        <article class="home-event-card">
          <div class="home-event-card__date" aria-label="{{ webinar.date | date: '%B %-d, %Y' }}">
            <span class="home-event-card__month">{{ webinar.date | date: "%b" }}</span>
            <span class="home-event-card__day">{{ webinar.date | date: "%d" }}</span>
            <span class="home-event-card__year">{{ webinar.date | date: "%Y" }}</span>
          </div>
          <div class="home-event-card__content">
            {% if webinar.time and webinar.time != "" %}<p class="home-event-card__time">{{ webinar.time }}</p>{% endif %}
            <h3><a href="{{ webinar.url | relative_url }}">{{ webinar.title }}</a></h3>
            {% include webinar_speaker.html webinar=webinar class="home-event-card__speaker" %}
          </div>
          {% if webinar.registration_url and webinar.registration_url != "" %}
            <a class="google-button home-event-card__signup" href="{{ webinar.registration_url }}" target="_blank" rel="noopener" aria-label="Add to calendar or sign up for {{ webinar.title }}">Sign up</a>
          {% endif %}
        </article>
      {% endif %}
    {% endfor %}
    </div>

    {% if upcoming_count == 0 %}
      <div class="home-empty-state">
        <p>No upcoming webinars are listed yet.</p>
      </div>
    {% endif %}
  </div>
</section>

<section class="google-section home-quick-links">
  <div class="wrap">
    <div class="section-heading">
      <p class="eyebrow">Explore</p>
      <h2>Quick Links</h2>
    </div>
    <div class="home-link-grid">
      <a class="home-link-card" href="{{ '/webinars/upcoming/' | relative_url }}">
        <span>Upcoming Webinars</span>
        <small>See future seminars and registration links.</small>
      </a>
      <a class="home-link-card" href="{{ '/webinars/archive/' | relative_url }}">
        <span>Past Webinar Archive</span>
        <small>Browse previous speakers, topics, and recordings.</small>
      </a>
      <a class="home-link-card" href="{{ '/education-blog/' | relative_url }}">
        <span>Education Blog</span>
        <small>Read educational posts and student contributions.</small>
      </a>
      <a class="home-link-card" href="{{ '/news-opportunities/' | relative_url }}">
        <span>News &amp; Opportunities</span>
        <small>Find announcements, calls, and opportunities.</small>
      </a>
    </div>
  </div>
</section>

<section class="google-section acknowledgments">
  <div class="wrap narrow">
    <h2>Organized by</h2>
    <div class="partner-logos" aria-label="Organizing partners">
      <a class="partner-card uconn-card" href="https://uconn.edu/" target="_blank" rel="noopener">
        <img src="{{ '/assets/images/uconn-spring-fog.jpg' | relative_url }}" alt="University of Connecticut">
        <span>University of Connecticut</span>
      </a>
      <a class="partner-card asa-card" href="https://community.amstat.org/businessandeconomicstatisticssection/home" target="_blank" rel="noopener">
        <img src="{{ '/assets/images/84ef319a0cdeb09b89f0d86d22a5b23c.jpg' | relative_url }}" alt="ASA Business and Economic Statistics Section">
      </a>
    </div>
  </div>
</section>

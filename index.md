---
layout: default
title: Home
---
<section class="home-lede">
  <div class="wrap home-lede__inner">
    <p class="eyebrow">Interdisciplinary Online Seminar Series</p>
    <h1>Connecting researchers through modern time series science.</h1>
    <p class="home-lede__summary">Time Series Connect brings together researchers, practitioners, and students across statistics, computer science, economics, business, engineering, and other data-rich fields to exchange ideas and applications in time series analysis.</p>
    <div class="cta-row home-lede__actions">
      <a class="google-button" href="{{ '/webinars/upcoming/' | relative_url }}">View upcoming events</a>
      <a class="google-button outline" href="{{ '/webinars/archive/' | relative_url }}">Browse past webinars</a>
    </div>
  </div>
</section>

<section class="google-section alt home-events">
  <div class="wrap">
    <div class="section-heading">
      <p class="eyebrow">What’s next</p>
      <h2>Upcoming Events</h2>
      <p class="section-lead">Join upcoming talks, panels, and interactive sessions from anywhere in the world.</p>
    </div>

    {% assign today = site.time | date: '%Y-%m-%d' %}
    {% assign webinars = site.webinars | sort: 'date' %}
    {% assign count = 0 %}
    <div class="home-event-list">
      {% for webinar in webinars %}
        {% assign webinar_date = webinar.date | date: '%Y-%m-%d' %}
        {% if webinar_date >= today and count < 3 %}
          {% assign count = count | plus: 1 %}
          <article class="home-event-card">
            <div class="home-event-card__date">
              <span class="home-event-card__month">{{ webinar.date | date: "%b" }}</span>
              <span class="home-event-card__day">{{ webinar.date | date: "%d" }}</span>
              <span class="home-event-card__year">{{ webinar.date | date: "%Y" }}</span>
            </div>
            <div class="home-event-card__content">
              {% if webinar.time %}<p class="date">{{ webinar.time }}</p>{% endif %}
              <h3><a href="{{ webinar.url | relative_url }}">{{ webinar.title }}</a></h3>
              {% if webinar.speaker %}<p><strong>{{ webinar.speaker }}</strong>{% if webinar.affiliation %}, {{ webinar.affiliation }}{% endif %}</p>{% endif %}
              <div class="event-actions">
                <a class="google-button" href="{{ webinar.url | relative_url }}">Event details</a>
                {% if webinar.registration_url %}
                  <a class="google-button outline" href="{{ webinar.registration_url }}" target="_blank" rel="noopener">Sign up</a>
                {% endif %}
              </div>
            </div>
          </article>
        {% endif %}
      {% endfor %}
    </div>

    {% if count == 0 %}
      <div class="home-empty-state">
        <p>No upcoming events are currently listed. Please check back soon or contact us to learn about future seminars.</p>
        <a class="google-button outline" href="mailto:timeseriesconnect@gmail.com">Contact us</a>
      </div>
    {% endif %}
  </div>
</section>

<section class="google-section home-about">
  <div class="wrap home-about__grid">
    <div>
      <p class="eyebrow">About the series</p>
      <h2>Open to everyone, everywhere.</h2>
    </div>
    <div>
      <p>We are an online interdisciplinary seminar series that brings together researchers, practitioners, and students from fields such as statistics, computer science, economics, business, engineering, and other data-rich disciplines to share insights and advances in time series analysis.</p>
      <p>The series is run by faculty at the University of Connecticut in partnership with the Business &amp; Economic Statistics Section of the American Statistical Association.</p>
      <p>You can watch recorded events on our <a href="https://www.youtube.com/" target="_blank" rel="noopener">YouTube channel</a>.</p>
    </div>
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
    <h2>Acknowledgment</h2>
    <div class="partner-logos" aria-label="Partner acknowledgments">
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

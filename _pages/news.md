---
layout: archive
title: "Updates"
permalink: /news/
author_profile: true
news:
  - date: 2026-07-15 12:00:00-0400
    text: >-
      Our paper, "FPGA-Accelerated Model Predictive Control of Gas Turbine Aero-Engines", has been accepted for presentation at the 52nd Annual Meeting of the IEEE Industrial Electronics Society (IECON 2026) in Doha, Qatar.
  - date: 2024-12-11 12:00:00-0400
    text: >-
      I participated at the Rolls-Royce UTC Annual Review in Derby, with a poster about FPGA Co-Processing for civil aerospace.
    gallery_id: "utc-annual-review"
  - date: 2026-10-19 12:00:00-0400
    text: >-
      I presented our paper "FPGA-Accelerated Model Predictive Control of Gas Turbine Aero-Engines", at the 52nd Annual Meeting of the IEEE Industrial Electronics Society (IECON 2026) in Doha, Qatar.
    gallery_id: "iecon-2026"
---

{% include base_path %}

{% assign news = page.news | sort: "date" | reverse %}

{% for post in news %}
  <article class="news-feed__item">
    {% if post.date %}
      <p class="news-feed__date"><i class="fa fa-calendar" aria-hidden="true"></i> <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></p>
    {% endif %}
    <div class="news-feed__text">{{ post.text | escape }}</div>
    {% if post.gallery_id %}
      <a class="news-feed__gallery-link" href="{{ '/gallery/' | relative_url }}#{{ post.gallery_id | escape }}">View event photos <span aria-hidden="true">&rarr;</span></a>
    {% endif %}
  </article>
{% endfor %}
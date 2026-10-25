---
layout: archive
title: "Gallery"
permalink: /gallery/
author_profile: true
---

<div class="event-gallery">
  {% assign events = site.data.gallery | sort: "date" | reverse %}
  {% for event in events %}
    <article class="event-gallery__item" id="{{ event.id | escape }}">
      <div class="event-gallery__photos{% if event.photos.size > 2 %} event-gallery__photos--lead{% elsif event.photos.size == 1 %} event-gallery__photos--single{% endif %}">
        {% for photo in event.photos %}
          <figure class="event-gallery__photo">
            <a class="event-gallery__open" href="{{ photo.image | relative_url }}" data-gallery-open data-caption="{{ event.title | escape }}: {{ photo.caption | escape }}" data-alt="{{ photo.alt | escape }}" aria-label="Open full-size image: {{ photo.caption | escape }}">
              <img src="{{ photo.image | relative_url }}" alt="{{ photo.alt | escape }}">
            </a>
            {% if photo.caption %}<figcaption>{{ photo.caption | escape }}</figcaption>{% endif %}
          </figure>
        {% endfor %}
      </div>
      <div class="event-gallery__body">
        <div class="event-gallery__meta">
          <span>{{ event.category | escape }}</span>
          <time datetime="{{ event.date | date_to_xmlschema }}">{{ event.date | date: "%B %d, %Y" }}</time>
        </div>
        <h2>{{ event.title | escape }}</h2>
        <p>{{ event.description | escape }}</p>
        <div class="event-gallery__footer">
          <span>{{ event.location | escape }}</span>
          {% if event.link %}<a href="{{ event.link | relative_url }}">Related news <span aria-hidden="true">&rarr;</span></a>{% endif %}
        </div>
      </div>
    </article>
  {% endfor %}
</div>

<dialog class="gallery-lightbox" id="gallery-lightbox" aria-labelledby="gallery-lightbox-title">
  <button class="gallery-lightbox__close" type="button" data-gallery-close aria-label="Close image viewer" title="Close">
    <i class="fa fa-times" aria-hidden="true"></i>
  </button>
  <h2 class="sr-only" id="gallery-lightbox-title">Event photo viewer</h2>
  <div class="gallery-lightbox__stage">
    <button class="gallery-lightbox__arrow" type="button" data-gallery-previous aria-label="Previous photo" title="Previous photo">
      <i class="fa fa-chevron-left" aria-hidden="true"></i>
    </button>
    <figure class="gallery-lightbox__figure">
      <img data-gallery-image alt="">
      <figcaption>
        <span data-gallery-caption></span>
        <span class="gallery-lightbox__counter" data-gallery-counter aria-live="polite"></span>
      </figcaption>
    </figure>
    <button class="gallery-lightbox__arrow" type="button" data-gallery-next aria-label="Next photo" title="Next photo">
      <i class="fa fa-chevron-right" aria-hidden="true"></i>
    </button>
  </div>
</dialog>

<script src="{{ '/assets/js/gallery-lightbox.js' | relative_url }}" defer></script>
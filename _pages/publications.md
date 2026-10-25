---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<nav class="publication-index" aria-label="Publication sections">
  <a href="#accepted-preprints">Accepted &amp; Preprints</a>
  <a href="#journal-articles">Journal Articles</a>
  <a href="#conference-papers">Conference Papers</a>
  <a href="#doctoral-thesis">Doctoral Thesis</a>
</nav>

<h2 class="publication-section-title" id="accepted-preprints">Accepted &amp; Preprints</h2>

{% assign accepted_posts = site.publications | where: "status_label", "Accepted" %}
{% assign preprint_posts = site.publications | where: "status_label", "Preprint" %}

{% assign other_posts = accepted_posts | concat: preprint_posts | sort: "date" | reverse %}

{% for post in other_posts %}
  {% include archive-single.html %}
{% endfor %}

<h2 class="publication-section-title" id="journal-articles">Journal Articles</h2>

{% assign journal_posts = site.publications | where: "publication_type", "journal" | sort: "date" | reverse %}
{% for post in journal_posts %}
  {% include archive-single.html %}
{% endfor %}


<h2 class="publication-section-title" id="conference-papers">Conference Papers</h2>

{% assign conference_posts = site.publications | where: "publication_type", "conference" | sort: "date" | reverse %}
{% for post in conference_posts %}
  {% if post.status_label != "Accepted" and post.status_label != "Preprint" %}
    {% include archive-single.html %}
  {% endif %}
{% endfor %}


<h2 class="publication-section-title" id="doctoral-thesis">Doctoral Thesis</h2>

{% assign thesis_posts = site.publications | where: "publication_type", "thesis" | sort: "date" | reverse %}
{% for post in thesis_posts %}
  {% include archive-single.html %}
{% endfor %}
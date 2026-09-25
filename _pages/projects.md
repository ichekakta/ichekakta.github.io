---
layout: archive
title: "Projects"
permalink: /projects/
author_profile: true
---

{% include base_path %}

{% assign projects = site.projects | sort: "date" | reverse %}

{% for post in projects %}
  {% include project-single.html %}
{% endfor %}
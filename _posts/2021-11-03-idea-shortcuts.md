---
# layout: static
title:  "IntelliJ Idea Shortcuts"
date:   2021-11-03 21:55:00
categories: Shortcuts
tags: [Shortcuts]
---



<ul>
{% for shortcut in site.data.shortcuts %}
  <li>
      {{ shortcut.keys }}
      {{ shortcut.shortcut }}
  </li>
{% endfor %}
</ul>

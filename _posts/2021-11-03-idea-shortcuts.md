---
# layout: static
title:  "IntelliJ Idea Shortcuts"
date:   2021-11-03 21:55:00
categories: Shortcuts
tags: [Shortcuts]
---



<!-- <ul>
{% for shortcut in site.data.shortcuts %}
  <li>
      {{ shortcut.keys }}
      {{ shortcut.shortcut }}
  </li>
{% endfor %}
</ul> -->


<table>
  <tr>
    <th>Key Combination</th>
    <th>Details</th>
  </tr>
{% for individual_shortcut in site.data.shortcuts %}
  <tr>
    <td> {{ individual_shortcut.keys }} </td>
    <td> {{ individual_shortcut.shortcut }} </td>
  </tr>
{% endfor %}

</table>

<p>{{ site.time }}</p><

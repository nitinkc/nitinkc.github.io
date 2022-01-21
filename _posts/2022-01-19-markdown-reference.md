---
# layout: static
title:  "Markdown Reference"
date:   2022-01-19 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
---

## Contents

{% include toc title="Index" %}

## Add right side bar Index
{% raw  %}
`{% include toc title="Index" %}`
{% endraw %}


## Include gists as
{% raw  %}
`{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}`
{% endraw %}

## INCLUDE TIME

SITE BUILD TIME

{% raw  %}

{{ site.time  }}

`{{ 'now' | date: "%Y/%m/%d" }}`

`{{ 'now' | date_to_rfc822 }}`

`{{ 'now' | date: "%C" }}`

`{{ 'now' | date: "%c" }}`

`{{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}`

{% endraw %}


## Markdown links syntax

If you're building your pages with markdown, use the following examples to generate internal links.

{% raw  %}
`[Link title]({{ site.baseurl }}{% link index.html %})`

`[Link title]({% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})`

`[Link title]({{ site.baseurl }}{% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})`
{% endraw %}

## Use a picture in a post
{% raw  %}
`![]({{ site.url }}/assets/images/image.png)`
{% endraw %}

## Escape Liquid template tags in Jekyll posts

Use raw tag 

{% raw  %}
`{% raw  %}`
`Any liquid Template Tag`
`{% endraw %}`

{% endraw %}

Use backtick quotes (\`) to display a liquid tag as a span of code .

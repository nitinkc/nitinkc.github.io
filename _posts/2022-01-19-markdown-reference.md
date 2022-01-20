---
# layout: static
title:  "Markdown Reference"
date:   2022-01-19 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
---

## Add right side bar Index
{% include toc title="Index" %}

## Include gists as
{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}

## INCLUDE TIME

SITE BUILD TIME

{{ site.time  }}

NOW 
```sh
{{ 'now' | date: "%Y/%m/%d" }}

{{ 'now' | date_to_rfc822 }}

{{ 'now' | date: "%C" }}

{{ 'now' | date: "%c" }}


{{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}

```

## Markdown links syntax

If you're building your pages with markdown, use the following examples to generate internal links.

```markdown
[Link title]({{ site.baseurl }}{% link page/index.html %})
[Link title]({% post_url 2019-03-06-post-title %})
[Link title]({{ site.baseurl }}{% post_url 2019-03-06-post-title %})
```
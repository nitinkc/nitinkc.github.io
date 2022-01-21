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


```markdown
{% raw  %}
[Link title]({{ site.baseurl }}{% link index.html %})

[Link title]({% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})

[Link title]({{ site.baseurl }}{% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})
{% endraw %}
```

## Use a picture in a post from specific folder
{% raw  %}
`![Image Text]({{ site.url }}/assets/images/image.png)`
{% endraw %}

## Escape Liquid template tags in Jekyll posts

Use raw tag as `{% raw  %}` write liquid tags and end with `{% endraw %}`

{% raw  %}
Use backtick quotes (\`) to display a liquid tag as a span of code .
{% endraw %}

## Insert Table

```markdown
| Column Header 1 	| Column Header 1  						| 
| :---				| :---    								|      
|⌘E            		|Move to the last location you edited.	|
|⌘  + 1        		|It activates the quick fix.			|
```

---
# layout: static
title:  "Markdown Reference"
date:   2022-01-19 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

## Contents

{% include toc title="Index" %}

## Add right side Index bar on this blog

{% raw  %}
`{% include toc title="Index" %}`
{% endraw %}


## Include gists as

Include code as a gist into the Jekyll post. Uses jekyll-gist plugin.
{% raw  %}
`{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}`
{% endraw %}

## INCLUDE TIME

| Column Header 1 | Column Header 1  | 
| :---				| :---   |  
|Site Build Time to be displayed{% raw  %}`{{ site.time  }}`{% endraw %} |{{ site.time  }}|
|{% raw  %}`{{ 'now' | date: "%Y/%m/%d" }}`{% endraw %}|{{ 'now' | date: "%Y/%m/%d" }}|
|{% raw  %}`{{ 'now' | date_to_rfc822 }}`{% endraw %}|{{ 'now' | date_to_rfc822 }}|
|{% raw  %}`{{ 'now' | date: "%C" }}`{% endraw %}|{{ 'now' | date: "%C" }}|
|{% raw  %}`{{ 'now' | date: "%c" }}`{% endraw %}|{{ 'now' | date: "%c" }}|
|{% raw  %}`{{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}`{% endraw %}|{{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}|

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

* Use raw tag 
    * to begin `{{ "{% raw " }}%}` and end with `{{ "{% endraw " }}%} `
* Another way to escape `{{ "{{ tag " }}}}`

Use backtick quotes (\`) to display a liquid tag as a span of code .

## Insert Table

```markdown
| Column Header 1 | Column Header 1  | 
| :---		| :---   |      
| ⌘E    	| Move to the last location you edited.	|
| ⌘  + 1  	|It activates the quick fix.|
```

## Add Sidebar Navigation

In the header tag add

```markdown
---
sidebar:
  nav: "algo"
---
```
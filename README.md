# nitinkc.github.io


[Text using Symbols](https://fsymbols.com/generators/encool/)

Liquid Templating Language


Add Font matter to the top of the page

---
# front matter tells Jekyll to process Liquid
---

To expand the main content to the right, filling the space of what is normally occupied by the table of contents. Add the following to a post or page’s YAML Front Matter:

classes: wide

sudo bundle install --path vendor/bundle 


added in default.html in navigation and in head.html in include
<!-- Added to allow font awesome icons -->
<script src="https://use.fontawesome.com/releases/v5.0.2/js/all.js"></script>   

kill running process occupying 
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9

SiteMap : https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap


pandoc -f docx -t markdown Buying\ a\ bigger\ machine.docx -o x.md  

## Add right side bar Index
{% comment %} 
{% include toc title="Index" %}
{% endcomment %}

## Include gists as
{% comment %} 
{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}
{% endcomment %}

## INCLUDE TIME

SITE BUILD TIME
{% comment %} 
{{ site.time  }}
{% endcomment %}

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

```code
[Link title]({{ site.baseurl }}{% link index.html %})
[Link title]({% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})
[Link title]({{ site.baseurl }}{% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})
```                                                                                     ─╯
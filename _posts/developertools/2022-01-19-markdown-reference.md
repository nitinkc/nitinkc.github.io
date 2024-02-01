---
# layout: static
title:  "Markdown Reference"
date:   2022-01-19 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

{% include toc title="Index" %}

## Add Table of contents
right side Index bar (on this blog)
{% raw  %}
`{% include toc title="Index" %}`
{% endraw %}
OR

simply add `toc: true` on the [front matter](https://jekyllrb.com/docs/front-matter/).
**Has some issues when the page is long**
{: .notice--danger}

OR

## Contents
{% raw  %}
{:.no_toc}
{% endraw %}

Will be replaced with the ToC, excluding the "Contents" header
{% raw  %}
{:toc}
{% endraw %}

## Include gists as

Include code as a gist into the Jekyll post. Uses jekyll-gist plugin.
{% raw  %}
`{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}`
{% endraw %}

## Markdown links syntax

If you're building your pages with markdown, use the following examples to generate internal links.

```markdown
{% raw  %}
[Link title]({{ site.baseurl }}{% link index.html %})

[Link title]({{ site.baseurl }}{% post_url 2016-04-04-jekyll-blog-GitHub-hosting %})

[Link title]({% post_url /developertools/2021-02-01-iterm2-zsh-config %})
{% endraw %}
```

## Hyperlinks

- Open link in another tab
[Try me for another Tab](https://www.google.com/){:target="_blank"}

{% raw %}
`[Link title](https://www.google.com/){:target="_blank"}`
{% endraw %}

- Open link in same tab
[Try me for same Tab](https://www.google.com/)

{% raw %}
`[Link title](https://www.google.com/)`
{% endraw %}

## Use a picture in a post from specific folder
{% raw  %}
`![Image Text]({{ site.url }}/assets/images/image.png)`
{% endraw %}

## Resize an image
{% raw  %}
`<img src="assets/images/image.png" width="300" height="200">`
{% endraw %}

## Escape Liquid template tags in Jekyll posts

* to begin `{{ "{% raw " }}%}` and end with `{{ "{% endraw " }}%} `
* Another way to escape `{{ "{{ tag " }}}}`

Use backtick quotes `(\`)` to display a liquid tag as a span of code .

## Insert Table

```markdown
| Column Header 1  | Column Header 1                       | 
|:-----------------|:--------------------------------------|      
| ⌘E     	       | Move to the last location you edited. |
| ⌘  + 1  	       | It activates the quick fix.           |
```

## Add Sidebar Navigation

In the header tag add

```markdown
---
sidebar:
  nav: "algo"
---
```

## Embed pdf document
```markdown
## PDF Reference
<object data="https://nitinkc.github.io/assets/media/file.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://nitinkc.github.io/assets/media/file.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://nitinkc.github.io/assets/media/file.pdf">Download PDF</a>.</p>
    </embed>
</object>

```
## INCLUDE TIME

| Column Header 1                                                         | Column Header 1                          <br/> | Format   |
|:------------------------------------------------------------------------|:-----------------------------------------------|:---------| 
| Site Build Time to be displayed{% raw  %}`{{ site.time  }}`{% endraw %} | {{ site.time  }}                               |          |
| {% raw  %}`{{ 'now'                                                     | date: "%Y/%m/%d" }}`{% endraw %}               | {{ 'now' | date: "%Y/%m/%d" }} |
| {% raw  %}`{{ 'now'                                                     | date_to_rfc822 }}`{% endraw %}                 | {{ 'now' | date_to_rfc822 }} |
| {% raw  %}`{{ 'now'                                                     | date: "%C" }}`{% endraw %}                     | {{ 'now' | date: "%C" }} |
| {% raw  %}`{{ 'now'                                                     | date: "%c" }}`{% endraw %}                     | {{ 'now' | date: "%c" }} |
| {% raw  %}`{{ 'now'                                                     | date: "%a, %b %-d %Y - %r %Z" }}`{% endraw %}  | {{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}|

## Notices with theme

Notice [emphasized](#notices-with-theme) with the `{: .notice}` class.
{: .notice}

Notice [emphasized](#notices-with-theme) with the `{: .notice--primary}` class.
{: .notice--primary}

Notice [emphasized](#notices-with-theme) with the `{: .notice--info}` class.
{: .notice--info}

Notice [emphasized](#notices-with-theme) with the `{: .notice--warning}` class.
{: .notice--warning}

Notice [emphasized](#notices-with-theme) with the `{: .notice--success}` class.
{: .notice--success}

Notice [emphasized](#notices-with-theme) with the `{: .notice--danger}` class.
{: .notice--danger}

# Writing Math Equations

Traditional using subscript and super script

{% raw %}
log<sub>base</sub>index = power

base<sup>power</sup> = index
{% endraw %}


`log<sub>b</sub><sup>x</sup>+log<sub>b</sub><sup>y</sup>`
{% raw %}
log<sub>b</sub><sup>x</sup>+log<sub>b</sub><sup>y</sup>
{% endraw %}

# $$ \LaTeX $$ - Using Lib
- From [https://yihui.org/en/2018/07/latex-math-markdown/](https://yihui.org/en/2018/07/latex-math-markdown/)
- Cheatsheet - html [https://quickref.me/latex.html](https://quickref.me/latex.html)
- Cheatsheet - pdf [https://tug.ctan.org/info/latex-refsheet/LaTeX_RefSheet.pdf](https://tug.ctan.org/info/latex-refsheet/LaTeX_RefSheet.pdf)

[https://nitinkc.github.io/develope| x^{n+1}                                                        | $$ x^{n+1} $$                                                                                           |
| \frac{a+b}{2}                    r%20tools/LaTex/](https://nitinkc.github.io/developer%20tools/LaTex/)

# $$ \LaTeX $$ Summary

keep the expressions between `$$`

| Math Expression                                                   | Rendered Output                                                                                         |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| log{_a}{n}                                                     | $$ log{_a}{n} $$                                                                                        |
| y = ax^2 + bx + c                                              | $$ y = ax^2 + bx + c, $$                                                                                |
| $$ \frac{a+b}{2} $$                                                                                     |
| \sqrt[n]{a^2+b^2}                                              | $$ \sqrt[n]{a^2+b^2} $$                                                                                 |
| x_1, \ldots, x_n                                               | $$ x_1, \ldots, x_n $$                                                                                  |
| x_1 + \cdots + x_n                                             | $$ x_1 + \cdots + x_n $$                                                                                |
| \left( a + \frac{1}{2} \right)^2                               | $$ \left( a + \frac{1}{2} \right)^2 $$                                                                  |
| while this $$ a > 0 $$ is inline math mode.                    | while this $$ a > 0 $$ is inline math mode.                                                             |
| \vec{u} \otimes \vec{v} = \mathbf{M}                           | $$ \vec{u} \otimes \vec{v} = \mathbf{M} $$                                                              |
| \log \left[1 + \left( \frac{x + \sin y}{z} - \sqrt{a} \right)^b \right] | $$ \log \left[1 + \left( \frac{x + \sin y}{z} - \sqrt{a} \right)^b \right] $$                           |
| \frac{\frac12 - 2}{5 + \frac43} - \frac{\displaystyle \frac12 - 2}{\displaystyle 5 + \frac43} = 0 | $$ \frac{\frac12 - 2}{5 + \frac43} - \frac{\displaystyle \frac12 - 2}{\displaystyle 5 + \frac43} = 0 $$ |
| \xrightarrow[under]{over}                                      | $$ \xrightarrow[under]{over} $$                                                                         |

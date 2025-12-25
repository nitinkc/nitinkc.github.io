---
title: Markdown Reference
date: 2022-01-19 21:55:00
categories:
- Developer Tools
tags:
- Reference
- Documentation
sidebar:
  nav: algo
---

{% include toc title="Index" %}

Color Pallet

```
HEX : #b51b58
RGB : 181, 27, 88
CMYK : 0, 85, 51, 29

HEX : #1bb578
RGB : 27, 181, 120
CMYK : 85, 0, 34, 29
```

![colorPallete.png](/assets/images/colorPallete.png)

# Add Table of contents

- right side Index bar (on this blog)
  {% raw %}
  `{% include toc title="Index" %}`
  {% endraw %}

- simply add `toc: true` on
  the [front matter](https://jekyllrb.com/docs/front-matter/).
    - **Has some issues when the page is long**
- Contents `{:.no_toc}`
    - Will be replaced with the ToC, excluding the "Contents" header `{:toc}`

# Escape Liquid template tags in Jekyll posts
- Use backtick(`) to display a liquid tag as a span of code .

* to begin `{{ "{% raw " }}%}` and end with `{{ "{% endraw " }}%} `
* Another way to escape `{{ "{{ tag " }}}}`

# Include gists
Include code as a gist into the Jekyll post. Uses jekyll-gist plugin.
{% raw %}
`{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}`
{% endraw %}

# Hyperlinks - External links

- Open link in new/other tab -  `{:target="\_blank"}`
  `[Try me for another Tab](https://www.google.com/){:target="_blank"}`
- Open link in same tab
  `[Link title](https://www.google.com/)` 

### Markdown hyperlinks syntax

If you're building your pages with Markdown, use the following examples to
generate internal links.

- [Link title]({{ site.baseurl }}{% link index.html %})
  {% raw %}
  `[Link title]({{ site.baseurl }}{% link index.html %})`
  {% endraw %}

- [Link title]({{ site.baseurl }}{% post_url
  /developertools/2016-04-04-jekyll-blog-GitHub-hosting %})
  {% raw %}
  `[Link title]({{ site.baseurl }}{% post_url /developertools/2016-04-04-jekyll-blog-GitHub-hosting %})`
  {% endraw %}

- skipping `site.baseurl` [Link title without site.baseurl]({% post_url
  /developertools/2021-02-01-terminal-config %})
  {% raw %}
  ``
  {% endraw %}

# Image

in a post from specific folder
`![Image Text]({{ site.url }}/assets/images/image.png)`

### Resize an image

- `<img src="assets/images/image.png" width="300" height="200">`
- `![platformThreads.png](/assets/images/platformThreads.png){:width="70%" height="50%"}`

# Video

```
<iframe
src="https://www.youtube.com/embed/1yaUn_PhlM8"
title="git revert - local and remote" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
allowfullscreen>
</iframe>
```

using Spaceship jekyll plugin

```
![](https://www.youtube.com/watch?v=I6jB0nM9SKU)
```

# Insert Table

**Jekyll Spaceship plugin Table** [https://github.com/jeffreytse/jekyll-spaceship?tab=readme-ov-file#1-table-usage](https://github.com/jeffreytse/jekyll-spaceship?tab=readme-ov-file#1-table-usage)

```markdown
| Left Aligned Header 1  | Center Aligned Header                 | 
|:-----------------------|:-------------------------------------:|      
| ⌘E     	             | Move to the last location you edited. |
| ⌘  + 1  	             | It activates the quick fix.           |
```

# Add Sidebar Navigation

In the header tag add

```markdown
---
sidebar:
  nav: "algo"
---
```

# Embed pdf document

```markdown
<object data="https://nitinkc.github.io/assets/media/file.pdf"
type="application/pdf"
width="700px"
height="700px">
<embed src="https://nitinkc.github.io/assets/media/file.pdf">
<p>This browser does not support PDFs. Please download the PDF to view it:
<a href="https://nitinkc.github.io/assets/media/file.pdf">Download PDF</a>.
</p>
</embed>
</object>
```

# DateFormatting with Liquid
Use the [**date filter**](https://cloud.google.com/looker/docs/best-practices/how-to-use-liquid-to-format-dates#strftime-reference)
to change the display format of dates.

- {% raw %}`{{ '2023-04-06' | date: "%B %d, %Y" }}`{% endraw %}: Displays the
  date as "April 06, 2023"
- {% raw %}`{{ customer.date_of_birth | date: '%D' }}`{% endraw %}: Displays a
  customer's date of birth in the format "03/09/80"
- {% raw %}`{{ site.time | date: '%D' }}`{% endraw %}: Site Build Time to be
  displayed

**Examples**

- {% raw %}`{{ 'now' | date: "%Y/%m/%d" }}`{% endraw %}
    - {{ 'now' | date: "%Y/%m/%d" }}
- {% raw %}`{{ 'now' | date_to_rfc822 }}`{% endraw %}
    - {{ 'now' | date_to_rfc822 }}
- {% raw %}`{{ 'now' | date: "%C" }}`{% endraw %}
    - {{ 'now' | date: "%C" }} : %C - Year divided by 100 and truncated to
      integer (00-99)
- {% raw %}`{{ 'now' | date: "%c" }}`{% endraw %}
    - {{ 'now' | date: "%c" }}
- {% raw %}`{{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}`{% endraw %}
    - {{ 'now' | date: "%a, %b %-d %Y - %r %Z" }}

# Notices with theme
- Default `{: .notice}`
- Primary {: .notice--primary}
- Info {: .notice--info}
- Warning {: .notice--warning}
- Success {: .notice--success}
- Danger {: .notice--danger}

# Writing Math Equations
Traditional using subscript and super-script

- `log<sub>base</sub>index = power` ==> log<sub>base</sub>index = power
- `base<sup>power</sup> = index` ==> base<sup>power</sup> = index
- `log<sub>b</sub><sup>x</sup>+log<sub>b</sub><sup>y</sup>` ==> log<sub>
  b</sub><sup>x</sup>+log<sub>b</sub><sup>y</sup>

# $$ \LaTeX $$ - Using Lib
- From [https://yihui.org/en/2018/07/latex-math-markdown/](https://yihui.org/en/2018/07/latex-math-markdown/)
- Cheatsheet - html [https://quickref.me/latex.html](https://quickref.me/latex.html)
- Cheatsheet - pdf [https://tug.ctan.org/info/latex-refsheet/LaTeX_RefSheet.pdf](https://tug.ctan.org/info/latex-refsheet/LaTeX_RefSheet.pdf)

[https://nitinkc.github.io/developer%20tools/LaTex/](https://nitinkc.github.io/developer%20tools/LaTex/)

# $$ \LaTeX $$ Summary

| Math Expression                                                              | Rendered Output                                                                  |
|:-----------------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| log{_a}{n}                                                                   | $ log{_a}{n} $                                                                   |
| y = ax^2 + bx + c                                                            | $ y = ax^2 + bx + c $                                                            |
| \frac{a+b}{2}                                                                | $ \frac{a+b}{2} $                                                                |
| \sqrt[n]{a^2+b^2}                                                            | $ \sqrt[n]{a^2+b^2} $                                                            |
| x_1, \ldots, x_n                                                             | $ x_1, \ldots, x_n $                                                             |
| x_1 + \cdots + x_n                                                           | $ x_1 + \cdots + x_n $                                                           |
| \left( a + \frac{1}{2} \right)^2                                             | $ \left( a + \frac{1}{2} \right)^2 $                                             |
| \vec{u} \otimes \vec{v} = \mathbf{M}                                         | $ \vec{u} \otimes \vec{v} = \mathbf{M} $                                         |
| \log \left[1 + \left( \frac{x + \sin y}{z} - \sqrt{a} \right)^b \right]      | $ \log \left[1 + \left( \frac{x + \sin y}{z} - \sqrt{a} \right)^b \right] $      |
| \frac{\frac12 - 2}{5 + \frac43}                                              | $ \frac{\frac12 - 2}{5 + \frac43} $                                              |
| \frac{\displaystyle \frac12 - 2}{\displaystyle 5 + \frac43}                  | $\frac{\displaystyle \frac12 - 2}{\displaystyle 5 + \frac43} $                   |
| \xrightarrow[under]{over}                                                    | $ \xrightarrow[under]{over} $                                                    |
| 24\times 60\times 60 \approx \text{90K secs}, \text{1 Day has 86400 seconds} | $ 24\times 60\times 60 \approx \text{90K secs}, \text{1 Day has 86400 seconds} $ |

### Spaceship - LaTex, Table, Media, Math, Plant UML
[Jeykll Spaceship](https://github.com/jeffreytse/jekyll-spaceship?tab=readme-ov-file#table-of-contents)

# Diagrams
[Plant UML Sequence Diagram](https://plantuml.com/sequence-diagram)

### Mermaid Diagram
[Mermaid Live Editor with gist code load](https://mermaid.live/edit?gist=https://gist.github.com/nitinkc/404befd918e8109cc830d23e3f7206fc#pako:eNqVUz1PwzAQ_SuWpyK1EiuRQIIi0YEKRBEDmOGSXBLTxI7OzlC1_e84cRM3bRm46d353cc721ue6BR5xHOCumDvD0IxZ6aJfWBlIVn7WGvV5lka-4bZl-AeswlhhoQqQWY1uyeCLn4l-HfI8whVKtRJgwVCHXhDuqs_4FGllSWp8pf4xzE8ZpMFEG3Yq7YWadx3AaZYQu3pB6cjXGjJZrO7XaKVBakMO1a1C13_FrJEC6aGBEPp1p5KHUP5AeQGyHssIS6R3bKb65Nh5iUY01ZKwYLL6HzWB0bSRtRu9nk_u1SZZhDrxu6CvH9nht2diR6eQZc9rMqctRvUt8Sjuw61Tw6GRR_F-ZRXSBXI1L3TbcsT3BZYoeCRgynQWnCh9o4HjdWrjUp4ZKnBKSfd5AWPMiiN85raKcZHCe7Gqp6CqbSalv4XdJ9hymtQn1pXh8T9L4IkBGE)

use the tag `mermaid!`

{% gist nitinkc/404befd918e8109cc830d23e3f7206fc %}
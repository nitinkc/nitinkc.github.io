

# Mermaid diagrams to work between both themes

`format: !!python/name:pymdownx.superfences.fence_div_format`

Does not work with mkdocs-material 9.0.0, so using the default format instead

`disable_indented_code_blocks` : Encourages use of fenced code blocks (```), which support syntax highlighting and custom fences such as Mermaid.

```yaml
- pymdownx.superfences:
  disable_indented_code_blocks: true
  custom_fences:
    - name: mermaid
      class: mermaid
      format: !!python/name:pymdownx.superfences.fence_code_format
```
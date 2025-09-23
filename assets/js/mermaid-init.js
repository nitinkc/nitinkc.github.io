(function(){
  // Initialize Mermaid on page load if available, and convert ```mermaid fenced code blocks if needed.
  function initMermaidIfPresent(){
    if (window.mermaid && typeof window.mermaid.initialize === 'function'){
      try { window.mermaid.initialize({ startOnLoad: false }); } catch(e) {}
      // Convert GitHub-style highlighted blocks to Mermaid divs if needed
      var blocks = document.querySelectorAll(
        "pre>code.language-mermaid, pre>code.mermaid, pre>code[class*='language-mermaid'], pre>code[class*='mermaid']"
      );
      blocks.forEach(function(code){
        var pre = code.parentElement;
        var container = document.createElement('div');
        container.className = 'mermaid';
        container.textContent = code.textContent;
        pre.replaceWith(container);
      });
      try { window.mermaid.init(undefined, document.querySelectorAll('.mermaid')); } catch(e) {}
    }
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initMermaidIfPresent);
  } else {
    initMermaidIfPresent();
  }
})();

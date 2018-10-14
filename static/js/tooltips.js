
var btns = document.querySelectorAll('.bibtex');

for(var i=0; i < btns.length; i++) { 
  btns[i].addEventListener('mouseleave',clearTooltip);
  btns[i].addEventListener('blur',clearTooltip);
}

function clearTooltip(e) { 
  e.currentTarget.setAttribute('class','one column content__icon bibtex');
  e.currentTarget.removeAttribute('aria-label');
}

function showTooltip(elem, msg) { 
  elem.setAttribute('class','one column content__icon bibtex tooltipped tooltipped-s');
  elem.setAttribute('aria-label', msg);
}

function fallbackMessage(action) { 
  var actionMsg='';
  var actionKey = (action === 'cut' ? 'X' : 'C');
  if(/iPhone|iPad/i.test(navigator.userAgent)) { 
    actionMsg='No support :(';
  }
  else if(/Mac/i.test(navigator.userAgent)) { 
    actionMsg='Press ⌘-'+actionKey+' to '+action;
  }
  else { 
    actionMsg='Press Ctrl-'+actionKey+' to '+action;
  }
  return actionMsg;
}
hljs.initHighlightingOnLoad();

var clipboardDemos = new ClipboardJS('[data-clipboard]');
clipboardDemos.on('success', function(e) { 
  e.clearSelection();
  showTooltip(e.trigger,'Copied!');});
clipboardDemos.on('error', function(e){ 
  showTooltip(e.trigger, fallbackMessage(e.action));
});

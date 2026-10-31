/* Shared artifact preview controls. Example content stays local to this page. */
(function(){'use strict';
function openHashTarget(){var id;try{id=decodeURIComponent(location.hash.slice(1));}catch(error){return;}var target=id&&document.getElementById(id);for(var node=target;node;node=node.parentElement){if(node.tagName==='DETAILS')node.open=true;}if(target)target.scrollIntoView();}
window.addEventListener('hashchange',openHashTarget);if(location.hash)openHashTarget();
document.querySelectorAll('[data-artifact-viewer]').forEach(function(root){
 var modes=[].slice.call(root.querySelectorAll('[data-view-mode]'));
 modes.forEach(function(button){button.addEventListener('click',function(){
  var empty=button.getAttribute('data-view-mode')==='empty';
  modes.forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});
  root.querySelector('[data-example]').hidden=empty;
  root.querySelector('[data-empty]').hidden=!empty;
  root.querySelector('[data-mode-name]').textContent=empty?'Empty preview':root.getAttribute('data-example-label');
 });});
});
function legacyCopy(text){var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;top:0;left:0;width:1px;height:1px;opacity:0';document.body.appendChild(ta);ta.select();var ok=false;try{ok=document.execCommand('copy');}catch(error){ok=false;}document.body.removeChild(ta);return ok;}
document.querySelectorAll('.artifact .copy-prompt').forEach(function(button){button.addEventListener('click',async function(){
 var root=button.closest('.artifact');var field=root.querySelector('.prompt');var group=button.closest('.actions');var status=group.querySelector('.copy-feedback')||(group.nextElementSibling&&group.nextElementSibling.matches('.copy-feedback')?group.nextElementSibling:root.querySelector('.copy-feedback'));
 root.querySelectorAll('.copy-feedback').forEach(function(n){n.textContent='';});
 var copied=false;
 try{await navigator.clipboard.writeText(field.value);copied=true;}catch(error){copied=legacyCopy(field.value);}
 if(copied){var message=root.getAttribute('data-copy-message')||(root.querySelector('#development-demo')?'Copied. Unzip the pack; attach starter.html, schema.json, blank-data.json and README.md.':'Copied. Unzip the pack and attach the relevant files in your assistant.');status.textContent=message;var label=button.getAttribute('data-label')||button.textContent;button.setAttribute('data-label',label);button.textContent='Copied';setTimeout(function(){button.textContent=label;if(status.textContent===message)status.textContent='';},2500);return;}
 /* Clipboard blocked: open the prompt, select it and show the message beside it, so both stay in view */
 var details=field.closest('details');if(details)details.open=true;
 var note=root.querySelector('.copy-fallback');
 if(!note){note=document.createElement('p');note.className='copy-feedback copy-fallback';note.setAttribute('role','status');note.setAttribute('aria-live','polite');var before=field.previousElementSibling&&field.previousElementSibling.tagName==='LABEL'?field.previousElementSibling:field;before.parentNode.insertBefore(note,before);}
 note.textContent='Copying was blocked. The prompt is selected: press Ctrl+C, or Cmd+C on a Mac.';
 status.textContent='Copying was blocked. The prompt is open under Read or edit the prompt.';
 field.focus({preventScroll:true});field.select();note.scrollIntoView({block:'start'});
});});
function markScroll(){document.querySelectorAll('.artifact .tscroll').forEach(function(t){t.classList.toggle('is-scroll',t.scrollWidth>t.clientWidth+2);});}
markScroll();window.addEventListener('resize',markScroll);document.querySelectorAll('.artifact [data-view-mode]').forEach(function(b){b.addEventListener('click',function(){setTimeout(markScroll,0);});});
})();

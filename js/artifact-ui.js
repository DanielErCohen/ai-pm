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
document.querySelectorAll('.artifact .copy-prompt').forEach(function(button){button.addEventListener('click',async function(){
 var root=button.closest('.artifact');var field=root.querySelector('.prompt');var group=button.closest('.actions');var status=group.querySelector('.copy-feedback')||(group.nextElementSibling&&group.nextElementSibling.matches('.copy-feedback')?group.nextElementSibling:root.querySelector('.copy-feedback'));
 root.querySelectorAll('.copy-feedback').forEach(function(n){n.textContent='';});
 try{await navigator.clipboard.writeText(field.value);status.textContent=root.querySelector('#development-demo')?'Copied. Unzip the pack; attach starter.html, schema.json, blank-data.json and README.md.':'Copied. Unzip the pack and attach the relevant files in your assistant.';button.textContent='Copied';setTimeout(function(){button.textContent='Copy prompt';},2500);}
 catch(error){field.closest('details').open=true;field.focus();field.select();status.textContent='The prompt is selected. Use your keyboard copy command.';}
});});
})();

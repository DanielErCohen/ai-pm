/* ai-pm site: copy buttons, install tabs, filter chips, book search, cycle ring, visit counts (GoatCounter). No dependencies. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');

  function store(k, v) {
    try { if (v === undefined) { return window.localStorage.getItem(k); } window.localStorage.setItem(k, v); } catch (e) { return null; }
    return null;
  }

  /* Copy buttons */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '-1000px';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); } finally { document.body.removeChild(ta); }
    });
  }
  var live = document.createElement('div');
  live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite');
  live.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
  document.body.appendChild(live);
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]');
    if (!b) { return; }
    copyText(b.getAttribute('data-copy')).then(function () {
      b.classList.add('done'); live.textContent = 'Copied';
      clearTimeout(b._t); b._t = setTimeout(function () { b.classList.remove('done'); live.textContent = ''; }, 2000);
    }, function () { live.textContent = 'Copy failed. Select the text and copy it by hand.'; });
  });

  /* Tabs with roving focus; last choice remembered */
  document.querySelectorAll('[data-tabs]').forEach(function (root) {
    var tabs = [].slice.call(root.querySelectorAll('[role="tab"]'));
    function select(tab, focus, remember) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) { tab.focus(); }
      if (remember) { store('sk-install-tab', tab.getAttribute('data-key')); }
    }
    function byKey(key) { return tabs.filter(function (t) { return t.getAttribute('data-key') === key; })[0]; }
    /* Order of choice: the remembered tab, then the tab named in data-default, then the first tab */
    var start = byKey(store('sk-install-tab')) || byKey(root.getAttribute('data-default')) || tabs[0];
    select(start, false, false);
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t, false, true); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') { n = tabs[(i + 1) % tabs.length]; }
        else if (e.key === 'ArrowLeft') { n = tabs[(i - 1 + tabs.length) % tabs.length]; }
        else if (e.key === 'Home') { n = tabs[0]; }
        else if (e.key === 'End') { n = tabs[tabs.length - 1]; }
        if (n) { e.preventDefault(); select(n, true, true); }
      });
    });
  });

  /* Filter chips on the toolkit index */
  var grid = document.querySelector('[data-filter-grid]');
  if (grid) {
    var items = [].slice.call(grid.querySelectorAll('li[data-cat]'));
    var chips = [].slice.call(document.querySelectorAll('[data-filter]'));
    var status = document.getElementById('filter-status');
    var empty = document.getElementById('filter-empty');
    var apply = function () {
      var on = function (kind) {
        return chips.filter(function (c) { return c.getAttribute('data-kind') === kind && c.getAttribute('aria-pressed') === 'true'; })
          .map(function (c) { return c.getAttribute('data-filter'); });
      };
      var cats = on('cat'), surfs = on('surface'), shown = 0;
      items.forEach(function (li) {
        var okC = !cats.length || cats.indexOf(li.getAttribute('data-cat')) > -1;
        var have = (li.getAttribute('data-surfaces') || '').split(' ');
        var okS = !surfs.length || surfs.every(function (s) { return have.indexOf(s) > -1; });
        li.hidden = !(okC && okS);
        if (!li.hidden) { shown++; }
      });
      if (status) { status.textContent = shown + ' of ' + items.length + ' tools shown'; }
      if (empty) { empty.hidden = shown > 0; }
    };
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
        apply();
      });
    });
    var reset = document.getElementById('filter-reset');
    if (reset) { reset.addEventListener('click', function () { chips.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); }); apply(); }); }
    apply();
  }

  /* Cycle ring */
  var ring = document.querySelector('[data-ring]');
  if (ring) {
    var nodes = [].slice.call(ring.querySelectorAll('.node'));
    var panels = [].slice.call(document.querySelectorAll('[data-ring-panel]'));
    var cname = ring.querySelector('.ctr-name'), clane = ring.querySelector('.ctr-lane'), chint = ring.querySelector('.ctr-hint');
    var cur = 0;
    var pick = function (i, focus) {
      cur = i;
      nodes.forEach(function (n, k) { n.setAttribute('aria-pressed', k === i ? 'true' : 'false'); n.setAttribute('tabindex', k === i ? '0' : '-1'); });
      panels.forEach(function (p, k) { p.hidden = k !== i; });
      var n = nodes[i];
      cname.textContent = n.getAttribute('data-name');
      clane.textContent = n.getAttribute('data-lane');
      clane.setAttribute('fill', n.getAttribute('data-color'));
      chint.textContent = 'Step ' + (i + 1) + ' of 9';
      if (focus) { n.focus(); }
    };
    nodes.forEach(function (n, i) {
      n.addEventListener('click', function () { pick(i, false); });
      n.addEventListener('keydown', function (e) {
        var j = null;
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(i, false); return; }
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { j = (i + 1) % nodes.length; }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { j = (i - 1 + nodes.length) % nodes.length; }
        else if (e.key === 'Home') { j = 0; } else if (e.key === 'End') { j = nodes.length - 1; }
        if (j !== null) { e.preventDefault(); pick(j, true); }
      });
    });
    ring.querySelectorAll('[data-ring-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        pick((cur + Number(b.getAttribute('data-ring-step')) + nodes.length) % nodes.length, false);
      });
    });
    ring.querySelectorAll('[data-ring-pick]').forEach(function (b) {
      b.addEventListener('click', function () { pick(Number(b.getAttribute('data-ring-pick')) - 1, false); });
    });
    /* Keep the ring on the step the reader opened below */
    document.querySelectorAll('details.stepcard').forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (d._bulk) { d._bulk = false; return; }
        var m = /^step-(\d)$/.exec(d.id);
        if (d.open && m) { pick(Number(m[1]) - 1, false); }
      });
    });
    var fromHash = /^#step-(\d)$/.exec(location.hash);
    pick(fromHash ? Number(fromHash[1]) - 1 : 0, false);
  }

  /* Collapsible steps: open the step a link points to, and open or close all */
  var openFromHash = function () {
    var el = location.hash.length > 1 && document.getElementById(location.hash.slice(1));
    if (el && el.tagName === 'DETAILS') { el.open = true; }
  };
  openFromHash();
  window.addEventListener('hashchange', openFromHash);
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) { return; }
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (el && el.tagName === 'DETAILS') { el.open = true; }
  });
  var all = document.querySelector('[data-expand-all]');
  if (all) {
    var cards = [].slice.call(document.querySelectorAll('details.stepcard'));
    var sync = function () {
      all.textContent = cards.every(function (d) { return d.open; }) ? 'Close all steps' : 'Open all steps';
    };
    all.addEventListener('click', function () {
      var open = !cards.every(function (d) { return d.open; });
      cards.forEach(function (d) { if (d.open !== open) { d._bulk = true; d.open = open; } });
      sync();
    });
    cards.forEach(function (d) { d.addEventListener('toggle', sync); });
    sync();
  }

  /* Timeline */
  var tl = document.querySelector('[data-timeline]');
  if (tl) {
    var btns = [].slice.call(tl.querySelectorAll('.tl-btn'));
    btns.forEach(function (b) {
      var panel = document.getElementById(b.getAttribute('aria-controls'));
      panel.hidden = true;
      b.addEventListener('click', function () {
        var open = b.getAttribute('aria-expanded') === 'true';
        btns.forEach(function (o) { o.setAttribute('aria-expanded', 'false'); document.getElementById(o.getAttribute('aria-controls')).hidden = true; });
        if (!open) { b.setAttribute('aria-expanded', 'true'); panel.hidden = false; }
      });
    });
  }

  /* Visit counts: GoatCounter, self-hosted count.js, no cookies. Live site only. */
  var me = document.currentScript;
  if (me && location.hostname === 'danielercohen.github.io') {
    var gc = document.createElement('script');
    gc.async = true;
    gc.src = me.src.replace(/site\.js(\?.*)?$/, 'count.js');
    gc.setAttribute('data-goatcounter', 'https://danielercohen.goatcounter.com/count');
    document.head.appendChild(gc);
    /* Clicks that show a tool was taken: copy buttons, zip downloads, GitHub and LinkedIn links */
    document.addEventListener('click', function (e) {
      if (!window.goatcounter || !window.goatcounter.count) { return; }
      var page = location.pathname.replace(/^\/ai-pm/, '') || '/';
      var name = null, el = e.target.closest('[data-copy], a[href]');
      if (!el) { return; }
      if (el.hasAttribute('data-copy')) { name = (el.closest('.adapt') ? 'adapt ' : 'copy ') + page; }
      else {
        var href = el.getAttribute('href');
        if (/\.zip$/.test(href)) { name = 'download ' + href.split('/').pop(); }
        else if (/github\.com\/DanielErCohen\//i.test(href)) { name = 'github ' + href.replace(/^https?:\/\/github\.com\/DanielErCohen\//i, ''); }
        else if (/linkedin\.com\/in\/danielercohen/i.test(href)) { name = 'linkedin from ' + page; }
      }
      if (name) { window.goatcounter.count({ path: name, title: name, event: true }); }
    });
  }
})();

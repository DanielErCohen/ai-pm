/* Fun stuff page: a made-up sample of the Movie Night picker.
   The films and marks come from the list in the page, so without JavaScript that list stays as plain text.
   No network request and nothing stored: a reload resets the sample.
   The draw flicks titles past for under a second, then settles with a bounce (CSS, .rolling and .landed).
   With reduced motion the pick appears at once. */
(function () {
  var list = document.getElementById('mn-list');
  var host = document.getElementById('mn-demo');
  if (!list || !host) return;

  var films = [].map.call(list.querySelectorAll('li'), function (li) {
    var d = li.dataset;
    return { title: d.title, year: d.year, genre: d.genre, erin: d.erin === '1', josh: d.josh === '1', service: d.service === '1', watched: false };
  });
  var genres = films.map(function (f) { return f.genre; })
    .filter(function (g, i, a) { return a.indexOf(g) === i; }).sort();
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  var filters = { newErin: false, service: false, genre: '' };
  var current = null, drawn = false, rolling = false, announceTimer = 0;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }
  function button(cls, text) {
    var b = el('button', cls, text);
    b.type = 'button';
    return b;
  }

  host.textContent = '';
  var controls = el('div', 'mn-controls');
  var chips = el('div', 'mn-chips');
  chips.setAttribute('role', 'group');
  chips.setAttribute('aria-label', 'Filters');
  function chip(label, key) {
    var b = button('chip cat-personal', label);
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () {
      filters[key] = !filters[key];
      b.setAttribute('aria-pressed', String(filters[key]));
      refresh();
    });
    return b;
  }
  chips.appendChild(chip('New to Erin', 'newErin'));
  chips.appendChild(chip('On a service you have', 'service'));

  var selLabel = el('label', 'mn-genre');
  selLabel.appendChild(el('span', '', 'Genre'));
  var sel = el('select');
  sel.appendChild(new Option('Any genre', ''));
  genres.forEach(function (g) { sel.appendChild(new Option(g, g)); });
  sel.addEventListener('change', function () { filters.genre = sel.value; refresh(); });
  selLabel.appendChild(sel);

  var drawBtn = button('btn primary', 'Draw a film');
  controls.appendChild(chips);
  controls.appendChild(selLabel);
  controls.appendChild(drawBtn);

  var count = el('p', 'mn-count');
  var card = el('div', 'mn-card');
  var kind = el('p', 'mn-kind');
  var title = el('p', 'mn-title');
  var meta = el('p', 'mn-meta');
  var seen = el('p', 'mn-seen');
  var status = el('p', 'mn-status');
  [kind, title, meta, seen, status].forEach(function (e) { card.appendChild(e); });

  var actions = el('div', 'mn-actions');
  var watchBtn = button('btn', "We're watching this");
  var againBtn = button('btn', 'Draw again');
  actions.appendChild(watchBtn);
  actions.appendChild(againBtn);

  var live = el('p', 'sr-only');
  live.setAttribute('aria-live', 'polite');
  live.setAttribute('aria-atomic', 'true');
  var note = el('p', 'mock-note', 'Nothing is saved. Refreshing the page puts the sample back.');

  [controls, count, card, actions, live, note].forEach(function (e) { host.appendChild(e); });

  function pool() {
    return films.filter(function (f) {
      if (f.watched) return false;
      if (filters.newErin && f.erin) return false;
      if (filters.service && !f.service) return false;
      if (filters.genre && f.genre !== filters.genre) return false;
      return true;
    });
  }
  function seenText(f) {
    if (f.erin && f.josh) return 'Seen by both';
    if (f.erin) return 'Seen by Erin';
    if (f.josh) return 'Seen by Josh';
    return 'Seen by neither';
  }
  function announce(text) {
    clearTimeout(announceTimer);
    live.textContent = '';
    announceTimer = setTimeout(function () { live.textContent = text; }, 40);
  }
  function refresh() {
    var n = pool().length;
    count.textContent = n + (n === 1 ? ' title' : ' titles') + ' in the hat';
    watchBtn.disabled = !current || current.watched;
    againBtn.disabled = !drawn;
  }
  function show(k, t, m, s, st) {
    kind.textContent = k || ' ';
    title.textContent = t;
    meta.textContent = m || ' ';
    seen.textContent = s || ' ';
    status.textContent = st || ' ';
  }
  function showFilm(f) {
    show('Tonight', f.title, f.year + ', ' + f.genre, seenText(f), '');
  }
  function landed() {
    card.classList.remove('rolling', 'landed');
    if (!reduce) {
      void card.offsetWidth;
      card.classList.add('landed');
    }
  }
  function settle(f) {
    rolling = false;
    current = f;
    showFilm(f);
    landed();
    refresh();
    announce(f.title + ', ' + f.year + ', ' + f.genre + '. ' + seenText(f) + '.');
  }
  function empty() {
    current = null;
    drawn = true;
    show('', 'The hat is empty', 'Loosen a filter to put titles back.', '', '');
    card.classList.remove('landed');
    refresh();
    announce('The hat is empty. Loosen a filter to put titles back.');
  }
  function draw() {
    if (rolling) return;
    var p = pool();
    drawn = true;
    if (!p.length) { empty(); return; }
    var others = p.length > 1 ? p.filter(function (f) { return f !== current; }) : p;
    var pick = others[Math.floor(Math.random() * others.length)];
    if (reduce) { settle(pick); return; }
    rolling = true;
    card.classList.remove('landed');
    card.classList.add('rolling');
    show('Drawing', '', '', '', '');
    var delays = [50, 55, 65, 80, 100, 125, 155, 190], i = 0;
    (function tick() {
      if (i >= delays.length) { settle(pick); return; }
      title.textContent = films[Math.floor(Math.random() * films.length)].title;
      setTimeout(tick, delays[i++]);
    })();
  }

  drawBtn.addEventListener('click', draw);
  againBtn.addEventListener('click', draw);
  watchBtn.addEventListener('click', function () {
    if (!current || current.watched) return;
    current.watched = true;
    current.erin = true;
    current.josh = true;
    seen.textContent = seenText(current);
    status.textContent = 'Marked as watched for both. It is out of the hat for this visit.';
    refresh();
    announce(current.title + ' is marked as watched for both and is out of the hat for this visit.');
    againBtn.focus();
  });

  show('', 'Nothing drawn yet', 'Press Draw a film to pull a slip from the hat.', '', '');
  refresh();
})();

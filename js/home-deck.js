/* Home page: the three tool cards in the hero flip, one at a time, through every tool.
   Without JavaScript, or with reduced motion, the first three cards stay as they are.
   The cards pause while a pointer or the keyboard is on them, while the tab is hidden, and after Pause. */
(function () {
  var deck = document.querySelector('.home-hero .deck');
  if (!deck || !window.matchMedia || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var tools = [
    ['skills', 'Product-sparring skill', 'Challenge a plan', 'Ask for the strongest counter to your plan and a test that could change your mind.', 'Any chat', 'toolkit/skills.html#start'],
    ['skills', 'Recipient-panel skill', 'Get your draft challenged', 'Simulated readers list their objections to your doc before the real ones see it.', 'Claude Code, or one chat per reader', 'toolkit/skills.html#start-readers'],
    ['method', 'Decision record', 'Record a decision', 'Write down a decision, its evidence and the test that would change it, so you can check it later.', 'Any document or chat', 'toolkit/decision-record.html#start'],
    ['routines', 'Work task board', 'Get each decision prepared', 'Claude reads your notes, mail and chat and prepares each decision for your yes.', 'Claude Code', 'toolkit/work-task-board.html#start'],
    ['skills', 'Voice skill', 'Write in your own voice', 'Rules taken from your own writing, so a draft sounds like you before you edit it.', 'Any chat or Claude Code', 'toolkit/skills.html#voice'],
    ['setup', 'Project start', 'Start a project with an owner', 'Claude interviews you and writes down who decides, what waits on you and when to stop.', 'Any chat or Claude Code', 'toolkit/project-start.html#start'],
    ['career', 'Meeting review', 'Run better meetings', 'Find the habits to change in how you run meetings, from your own transcripts.', 'Any chat or Claude Code', 'toolkit/meeting-review.html#start'],
    ['setup', 'Second brain', 'Stop repeating your context', 'Give Claude your context at every session start, so you stop repeating it.', 'Claude Code', 'toolkit/second-brain.html#start'],
    ['routines', 'Routines', 'Read your newsletters in 4 minutes', 'Your PM newsletters as one digest, twice a week.', 'Claude Code to schedule it', 'toolkit/routines.html#start'],
    ['career', 'cv-tailor', 'Tailor your CV to a role', 'Improve your CV so it gets read, then tailor it to each role.', 'Any chat or Claude Code', 'toolkit/cv-tailor.html#start'],
    ['skills', 'Distill-to-gh-issue skill', 'Turn a bug into an issue', 'A bug report becomes a GitHub issue an engineer can start on.', 'Claude Code', 'toolkit/skills.html#distill-to-gh-issue'],
    ['setup', 'Claude Code setup', 'Set up Claude Code your way', 'Claude follows your rules and loads less context at every session start.', 'Claude Code', 'toolkit/claude.html#start'],
    ['career', 'Personal development review', 'Review your week of PM work', 'Look back at your week and pick one practice to try next week.', 'Any chat', 'toolkit/development-review.html#start'],
    ['builds', 'Page-saving extension', 'Save pages to your notes', 'Save the pages and podcasts worth keeping to your notes in one click.', 'An AI API key', 'toolkit/small-builds.html#start']
  ];
  var cards = [].slice.call(deck.querySelectorAll('.card')).slice(0, 3);
  if (cards.length < 3) return;
  var shown = [0, 1, 2], next = 3, slot = 0, hover = false, stopped = false;

  function fill(card, t) {
    card.className = card.className.replace(/\bcat-[a-z]+\b/, 'cat-' + t[0]);
    card.querySelector('.ch').textContent = t[1];
    var a = card.querySelector('h3 a');
    a.textContent = t[2];
    a.setAttribute('href', t[5]);
    card.querySelector('.cb > p:not(.meta)').textContent = t[3];
    card.querySelector('.badge').textContent = t[4];
  }
  function flip() {
    if (hover || stopped || document.hidden) return;
    var card = cards[slot], i = next;
    shown[slot] = i;
    do { next = (next + 1) % tools.length; } while (shown.indexOf(next) !== -1);
    slot = (slot + 1) % cards.length;
    card.classList.add('flip-out');
    setTimeout(function () {
      fill(card, tools[i]);
      card.classList.remove('flip-out');
      card.classList.add('flip-in');
      setTimeout(function () { card.classList.remove('flip-in'); }, 450);
    }, 260);
  }
  deck.addEventListener('mouseenter', function () { hover = true; });
  deck.addEventListener('mouseleave', function () { hover = false; });
  deck.addEventListener('focusin', function () { hover = true; });
  deck.addEventListener('focusout', function () { hover = false; });

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'deck-pause';
  btn.setAttribute('aria-pressed', 'false');
  btn.textContent = 'Pause the cards';
  btn.addEventListener('click', function () {
    stopped = !stopped;
    btn.setAttribute('aria-pressed', String(stopped));
    btn.textContent = stopped ? 'Play the cards' : 'Pause the cards';
  });
  deck.appendChild(btn);
  deck.classList.add('is-live');
  setInterval(flip, 2600);
})();

/* The shared tool list (docs/FinderAndToolRow.md), on the landing page and
   /features/. Hand-authored. The pages are complete without it: rows open and
   close as <details>, every link works. This adds:

   - the tick on each row, writing localStorage 'fns.pick' -- the same list
     /get restores its selection from, so picks made here arrive ticked there
   - the bar that carries them into the picker
   - on a list (.tl): the search, the Free/Patreon filter and the
     Expand all / Collapse all toggle
   - "Ask the finder" links (.js-finder), shown only when the finder answers */
(function () {
  'use strict';

  var PICK_KEY = 'fns.pick';
  var picked = [];
  try { picked = JSON.parse(localStorage.getItem(PICK_KEY) || '[]') || []; } catch (e) { picked = []; }
  if (!Array.isArray(picked)) picked = [];
  var titles = {};

  function isPicked(name) { return picked.indexOf(name) !== -1; }
  function setPicked(name, on) {
    var i = picked.indexOf(name);
    if (on && i === -1) picked.push(name);
    if (!on && i !== -1) picked.splice(i, 1);
    try { localStorage.setItem(PICK_KEY, JSON.stringify(picked)); } catch (e) { /* not remembered: the bar still works this visit */ }
    refreshPicks();
  }

  // ── the bar that carries picks into /get ──
  var carry = null;
  function ensureCarry() {
    if (carry) return carry;
    carry = document.createElement('div');
    carry.className = 'tl-carry';
    carry.hidden = true;
    carry.innerHTML = '<div class="tl-carry-in"><b></b><span class="tl-carry-names"></span>'
      + '<button type="button" class="tl-carry-clear">Clear</button>'
      + '<a class="btn btn-primary" href="/get/#catalog">Continue in the picker →</a></div>';
    carry.querySelector('.tl-carry-clear').addEventListener('click', function () {
      picked = [];
      try { localStorage.setItem(PICK_KEY, '[]'); } catch (e) { /* see setPicked */ }
      refreshPicks();
    });
    document.body.appendChild(carry);
    return carry;
  }

  function refreshPicks() {
    var ticks = document.querySelectorAll('.tick[data-name]');
    for (var i = 0; i < ticks.length; i++) {
      var on = isPicked(ticks[i].getAttribute('data-name'));
      ticks[i].setAttribute('aria-pressed', on ? 'true' : 'false');
      ticks[i].textContent = on ? '✓' : '+';
    }
    if (!carry) return;
    // only names this page can show count: /get may have kept others
    var mine = picked.filter(function (n) { return titles[n]; });
    carry.hidden = !mine.length;
    carry.querySelector('b').textContent = mine.length + ' tool' + (mine.length === 1 ? '' : 's') + ' picked';
    carry.querySelector('.tl-carry-names').textContent = mine.map(function (n) { return titles[n]; }).join(', ');
  }

  // A tick for every element carrying data-pick-name. The slot is where it goes.
  function addTicks(scope) {
    var hosts = scope.querySelectorAll('[data-pick-name]');
    for (var i = 0; i < hosts.length; i++) {
      var host = hosts[i];
      var name = host.getAttribute('data-pick-name');
      titles[name] = host.getAttribute('data-pick-title') || name;
      var slot = host.querySelector('.pick-slot');
      if (!slot || slot.querySelector('.tick')) continue;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'tick';
      b.setAttribute('data-name', name);
      b.setAttribute('aria-label', 'Pick ' + titles[name]);
      slot.appendChild(b);
    }
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('.tick[data-name]') : null;
    if (!t) return;
    // inside a <summary>: a tick must not also open or close the row
    e.preventDefault();
    e.stopPropagation();
    setPicked(t.getAttribute('data-name'), !isPicked(t.getAttribute('data-name')));
  });

  // ── a list: search, filter, views ──
  // Ranked by WHERE a typed word sits, as /features/ ranks
  // (docs/FeatureSearchPosition.md): the first word of a feature's name first.
  var LEAD = 0, NAME = 1, DOES = 2, ANY = 3, TOOL = 4, DESC = 5;
  function words(s) { return s.split(/[^a-z0-9]+/).filter(Boolean); }
  function wordAt(ws, w) {
    for (var i = 0; i < ws.length; i++) if (ws[i].indexOf(w) === 0) return i;
    return -1;
  }
  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function lit(text, qs) {
    var h = escapeHtml(text);
    qs.forEach(function (w) {
      var safe = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      h = h.replace(new RegExp('(' + safe + ')', 'gi'), '<mark>$1</mark>');
    });
    return h;
  }

  function mountList(root) {
    root.classList.add('js');
    var bar = root.querySelector('.tl-bar');
    var q = root.querySelector('.tl-q');
    var status = root.querySelector('.tl-status');
    var cats = root.querySelector('.tl-cats');
    var results = root.querySelector('.tl-results');
    var resultsList = results.querySelector('.trows');
    var empty = root.querySelector('.tl-empty');
    if (bar) bar.hidden = false;
    // expanded: every category and every tool open (the Expand all toggle)
    var st = { expanded: false, access: 'all' };
    var expandBtn = root.querySelector('.tl-expand');
    var catEls = Array.prototype.slice.call(cats.querySelectorAll('details.cat'));
    var catOpen = catEls.map(function (d) { return d.open; });

    var index = Array.prototype.slice.call(cats.querySelectorAll('.trow')).map(function (li, order) {
      var d = li.querySelector('.trow-d');
      var title = (li.getAttribute('data-pick-title') || '').toLowerCase();
      var desc = (li.querySelector('.trow-desc') || { textContent: '' }).textContent.toLowerCase();
      var feats = Array.prototype.slice.call(li.querySelectorAll('.trow-feats li')).map(function (fli) {
        var nameEl = fli.querySelector('.f-name');
        var name = nameEl ? nameEl.textContent.toLowerCase() : '';
        var does = (fli.querySelector('.f-does') || fli).textContent.toLowerCase();
        return { li: fli, nameEl: nameEl, nameText: nameEl ? nameEl.textContent : '', name: name,
                 nameWords: words(name), does: does, doesWords: words(does),
                 plain: (nameEl ? nameEl.textContent + ': ' : '') + (fli.querySelector('.f-does') || fli).textContent };
      });
      var tool = title + ' ' + (li.getAttribute('data-cat') || '').toLowerCase();
      return { li: li, d: d, home: li.parentNode, order: order, paid: li.getAttribute('data-paid') === '1',
               tool: tool, toolWords: words(tool), desc: desc, feats: feats };
    });

    function place(w, t, f) {
      if (f) {
        var at = wordAt(f.nameWords, w);
        if (at === 0) return LEAD;
        if (at > 0) return NAME;
        if (wordAt(f.doesWords, w) >= 0) return DOES;
        if (f.name.indexOf(w) !== -1 || f.does.indexOf(w) !== -1) return ANY;
      }
      if (wordAt(t.toolWords, w) >= 0 || t.tool.indexOf(w) !== -1) return TOOL;
      if (t.desc.indexOf(w) !== -1) return DESC;
      return -1;
    }
    function rankOf(t, f, qs) {
      var r = 0;
      for (var k = 0; k < qs.length && r >= 0; k++) {
        var p = place(qs[k], t, f);
        r = p < 0 ? -1 : Math.max(r, p);
      }
      return r;
    }

    function clearMarks(t) {
      var hit = t.li.querySelector('.trow-hit');
      if (hit) hit.parentNode.removeChild(hit);
      t.feats.forEach(function (f) {
        f.li.hidden = false;
        if (f.nameEl) f.nameEl.textContent = f.nameText;
      });
    }

    function apply() {
      var qs = q ? q.value.toLowerCase().split(/\s+/).filter(Boolean) : [];
      var flat = st.expanded;
      if (expandBtn) {
        expandBtn.setAttribute('aria-pressed', flat ? 'true' : 'false');
        expandBtn.textContent = flat ? 'Collapse all' : 'Expand all';
      }
      root.querySelectorAll('[data-access]').forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-access') === st.access ? 'true' : 'false');
      });
      var shown = [], nFeats = 0;
      index.forEach(function (t) {
        clearMarks(t);
        var ok = st.access === 'all' || (st.access === 'patreon') === t.paid;
        t.rank = Infinity;
        t.best = null;
        if (!ok) return;
        if (!qs.length) { t.rank = 0; shown.push(t); nFeats += t.feats.length; return; }
        var best = Infinity, bestF = null;
        t.feats.forEach(function (f) {
          f.rank = rankOf(t, f, qs);
          if (f.rank >= 0 && f.rank < best) { best = f.rank; bestF = f; }
        });
        if (best === Infinity) {
          var r = rankOf(t, null, qs);
          if (r >= 0) best = r;
        }
        if (best === Infinity) return;
        t.rank = best;
        t.best = best < TOOL ? bestF : null;
        shown.push(t);
        var n = 0;
        t.feats.forEach(function (f) {
          // as on /features/: a tool-level hit shows the whole tool, a feature hit shows the features that answer
          var on = best >= TOOL || (f.rank >= 0 && f.rank < TOOL);
          f.li.hidden = flat && !on;
          if (on) n++;
          if (on && f.nameEl) f.nameEl.innerHTML = lit(f.nameText, qs);
        });
        nFeats += n;
        if (!flat && t.best) {
          var hit = document.createElement('span');
          hit.className = 'trow-hit';
          hit.innerHTML = lit(t.best.plain, qs);
          t.li.querySelector('.trow-s').appendChild(hit);
        }
      });

      var searching = qs.length > 0;
      index.forEach(function (t) { t.li.hidden = shown.indexOf(t) === -1; });
      if (searching) {
        // one list, best first, as the picker and /features/ show a query
        shown.sort(function (a, b) { return a.rank - b.rank || a.order - b.order; })
          .forEach(function (t) { resultsList.appendChild(t.li); });
        cats.hidden = true;
        results.hidden = !shown.length;
      } else {
        index.forEach(function (t) { t.home.appendChild(t.li); });
        cats.hidden = false;
        results.hidden = true;
        catEls.forEach(function (d, i) {
          d.hidden = !d.querySelector('.trow:not([hidden])');
          d.open = flat || st.access === 'patreon' ? true : catOpen[i];
        });
      }
      index.forEach(function (t) { t.d.open = flat && shown.indexOf(t) !== -1; });
      if (empty) empty.hidden = shown.length > 0;
      if (status) {
        status.textContent = searching || st.access !== 'all' || flat
          ? shown.length + ' tool' + (shown.length === 1 ? '' : 's') + (searching ? ' match' : '') + ' · ' + nFeats + ' feature' + (nFeats === 1 ? '' : 's')
          : '';
      }
    }

    root.addEventListener('click', function (e) {
      var a = e.target.closest('[data-access]');
      if (expandBtn && e.target.closest('.tl-expand') === expandBtn) { st.expanded = !st.expanded; apply(); }
      if (a && root.contains(a)) { st.access = a.getAttribute('data-access'); apply(); }
    });
    var timer;
    if (q) q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(apply, 80); });
    if (/^#all-features$/.test(location.hash)) st.expanded = true;
    apply();
  }

  // ── the finder: a link only when it answers (off until launch) ──
  function showFinderLinks() {
    var links = document.querySelectorAll('.js-finder');
    if (!links.length || !window.fetch) return;
    fetch('/api/chat/', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!j || !j.ready) return;
        for (var i = 0; i < links.length; i++) links[i].hidden = false;
      })
      .catch(function () { /* no finder: the links stay hidden */ });
  }

  function init() {
    addTicks(document);
    if (Object.keys(titles).length) ensureCarry();
    var lists = document.querySelectorAll('.tl');
    for (var i = 0; i < lists.length; i++) mountList(lists[i]);
    refreshPicks();
    showFinderLinks();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

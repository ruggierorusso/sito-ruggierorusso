(function () {
  // Index filter + hover preview
  var list = document.querySelector('.list');
  if (list) {
    var rows = Array.prototype.slice.call(list.querySelectorAll('li'));
    var chips = Array.prototype.slice.call(document.querySelectorAll('.chips button'));
    var count = document.querySelector('.count');
    var prev = document.querySelector('.preview img');
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-f'), n = 0;
        chips.forEach(function (c) { c.setAttribute('aria-pressed', c === b ? 'true' : 'false'); });
        rows.forEach(function (r) {
          var show = f === 'ALL' || r.getAttribute('data-cat') === f;
          r.hidden = !show;
          if (show) { n++; r.querySelector('.n').textContent = (n < 10 ? '0' : '') + n; }
        });
        if (count) count.textContent = '(' + n + ')';
        var first = rows.filter(function (r) { return !r.hidden; })[0];
        if (first && prev) prev.src = first.getAttribute('data-img');
      });
    });
    if (prev) rows.forEach(function (r) {
      var show = function () { var s = r.getAttribute('data-img'); if (prev.getAttribute('src') !== s) prev.src = s; };
      r.addEventListener('mouseenter', show);
      r.querySelector('a').addEventListener('focus', show);
    });
  }

  // Lightbox
  var gal = document.querySelector('.gallery');
  var lb = document.querySelector('.lb');
  if (gal && lb) {
    var links = Array.prototype.slice.call(gal.querySelectorAll('a'));
    var img = lb.querySelector('img'), cap = lb.querySelector('.lb-c'), cur = 0, last = null;
    function show(i) {
      cur = (i + links.length) % links.length;
      img.src = links[cur].getAttribute('href');
      img.alt = links[cur].querySelector('img').alt;
      cap.textContent = (cur + 1) + ' / ' + links.length;
    }
    function open(i) { last = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; lb.querySelector('.lb-x').focus(); }
    function close() { lb.hidden = true; document.body.style.overflow = ''; if (last) last.focus(); }
    links.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
    lb.querySelector('.lb-x').addEventListener('click', close);
    lb.querySelector('.lb-p').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.lb-n').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(cur - 1);
      else if (e.key === 'ArrowRight') show(cur + 1);
    });
    var x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); x0 = null;
    });
  }
})();

// ---- Effetto luce sulle foto della home ----
(function () {
  var h = document.querySelector('.hero.torch');
  if (!h) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = window.matchMedia('(hover: none)').matches;
  function set(x, y) { h.style.setProperty('--x', x + 'px'); h.style.setProperty('--y', y + 'px'); }
  var r = h.getBoundingClientRect(); set(r.width / 2, r.height * 0.35);
  h.classList.add('on');
  if (!touch) {
    h.addEventListener('pointermove', function (e) { var b = h.getBoundingClientRect(); set(e.clientX - b.left, e.clientY - b.top); });
    h.addEventListener('pointerleave', function () { var b = h.getBoundingClientRect(); set(b.width / 2, b.height * 0.35); });
  } else if (!reduce) {
    var t0 = performance.now();
    (function loop(t) {
      var b = h.getBoundingClientRect(), k = (t - t0) / 4200;
      set(b.width * (0.5 + 0.38 * Math.sin(k)), b.height * (0.4 + 0.18 * Math.sin(k * 1.7)));
      requestAnimationFrame(loop);
    })(t0);
  }
})();

// ---- Moduli a passi (preventivo / prenotazione) ----
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('form.wizard'), function (f) {
    var steps = Array.prototype.slice.call(f.querySelectorAll('.step'));
    var prev = f.querySelector('[data-prev]'), next = f.querySelector('[data-next]'), send = f.querySelector('[data-send]');
    var bar = f.querySelector('.progress span');
    var sum = document.querySelector('[data-summary]');
    var cur = 0;
    f.classList.add('js');
    function valid(st) {
      var els = st.querySelectorAll('input,select,textarea');
      for (var i = 0; i < els.length; i++) { if (!els[i].checkValidity()) { els[i].reportValidity(); return false; } }
      return true;
    }
    function show(i) {
      cur = Math.max(0, Math.min(steps.length - 1, i));
      steps.forEach(function (s, k) { s.hidden = k !== cur; });
      prev.hidden = cur === 0; next.hidden = cur === steps.length - 1; send.hidden = cur !== steps.length - 1;
      if (bar) bar.style.width = ((cur + 1) / steps.length * 100) + '%';
    }
    function refresh() {
      Array.prototype.forEach.call(f.querySelectorAll('input[type=range]'), function (r) {
        var o = r.parentNode.querySelector('output'); if (o) o.textContent = r.value;
      });
      if (!sum) return;
      var rows = [];
      steps.forEach(function (s) {
        var vals = [];
        Array.prototype.forEach.call(s.querySelectorAll('input,select,textarea'), function (el) {
          if (el.name === 'privacy' || el.name === 'bot-field' || el.name === 'form-name') return;
          if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
          if (el.value && el.value.trim()) vals.push(el.type === 'range' ? el.value + ' ' + ((el.parentNode.querySelector('small') || {}).textContent || '') : el.value.trim().slice(0, 60));
        });
        var title = s.querySelector('legend').lastChild.textContent;
        rows.push('<dt>' + title + '</dt><dd>' + (vals.length ? vals.map(function (v) { return v.replace(/[<>&"]/g, ''); }).join(', ') : sum.getAttribute('data-empty')) + '</dd>');
      });
      sum.innerHTML = rows.join('');
    }
    prev.addEventListener('click', function () { show(cur - 1); });
    next.addEventListener('click', function () { if (valid(steps[cur])) { show(cur + 1); f.scrollIntoView({ behavior: 'smooth', block: 'start' }); } });
    f.addEventListener('input', refresh); f.addEventListener('change', refresh);
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && cur < steps.length - 1) { e.preventDefault(); next.click(); }
    });
    show(0); refresh();
  });
})();

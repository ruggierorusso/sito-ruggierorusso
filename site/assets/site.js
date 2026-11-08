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

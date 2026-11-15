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

// ---- Home: tre foto in ombra, luce a cerchio sotto il mouse, cambio ogni 3 secondi ----
(function () {
  var h = document.querySelector('.hero.torch');
  if (!h) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = matchMedia('(hover: none)').matches;
  var phs = h.querySelectorAll('.ph');
  // x, y relativi alla sezione: ogni foto calcola il proprio punto, così il cerchio passa da una foto all'altra
  function set(x, y) {
    var hb = h.getBoundingClientRect();
    Array.prototype.forEach.call(phs, function (ph) {
      var b = ph.getBoundingClientRect();
      ph.style.setProperty('--x', (x + hb.left - b.left) + 'px'); ph.style.setProperty('--y', (y + hb.top - b.top) + 'px');
    });
  }
  // Ombra e luce solo con il mouse; su telefono le foto restano visibili
  if (!touch) {
    h.classList.add('on');
    h.addEventListener('pointermove', function (e) { var b = h.getBoundingClientRect(); set(e.clientX - b.left, e.clientY - b.top); h.classList.add('lit'); });
    h.addEventListener('pointerleave', function () { h.classList.remove('lit'); });
  }

  // Rotazione dei lavori: ogni 3 secondi cambia un riquadro alla volta
  var pool = []; try { pool = JSON.parse(h.getAttribute('data-pool') || '[]'); } catch (e) {}
  var slots = Array.prototype.slice.call(h.querySelectorAll('a'));
  if (reduce || pool.length <= slots.length) return;
  var shown = slots.map(function (a) { return a.getAttribute('href'); });
  var turn = 0, timer = null;
  function pick() {
    var free = pool.filter(function (p) { return shown.indexOf(p.h) < 0; });
    return free[Math.floor(Math.random() * free.length)];
  }
  function swap() {
    var k = turn++ % slots.length, a = slots[k], img = a.querySelector('img'), cap = a.querySelector('.cap'), p = pick();
    if (!p) return;
    var pre = new Image();
    pre.onload = function () {
      a.classList.add('fade');
      setTimeout(function () {
        img.src = p.i; img.alt = p.a; cap.textContent = p.t; a.href = p.h; shown[k] = p.h;
        a.classList.remove('fade');
      }, 600);
    };
    pre.src = p.i;
  }
  function start() { if (!timer) timer = setInterval(swap, 3000); }
  function stop() { clearInterval(timer); timer = null; }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { e[0].isIntersecting ? start() : stop(); }).observe(h); else start();
  document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
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

// ---- Moodboard: foto preferite salvate solo in questo browser ----
(function () {
  var KEY = 'rr-moodboard';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(l) { try { localStorage.setItem(KEY, JSON.stringify(l)); } catch (e) {} paint(); }
  function has(src) { return load().some(function (x) { return x.s === src; }); }
  function toggle(item) {
    var l = load(), i = -1;
    l.forEach(function (x, k) { if (x.s === item.s) i = k; });
    if (i >= 0) l.splice(i, 1); else l.push(item);
    save(l);
  }
  var gal = document.querySelector('.gallery');
  var lbImg = document.querySelector('.lb img'), lbFav = document.querySelector('.lb-f');
  function lbSrc() { if (!lbImg || !lbImg.getAttribute('src')) return null; var m = lbImg.getAttribute('src').match(/img\/[^?#]+$/); return m ? m[0] : null; }
  function paint() {
    var n = load().length;
    Array.prototype.forEach.call(document.querySelectorAll('.mb-link'), function (a) { a.hidden = n === 0; a.querySelector('[data-mb-n]').textContent = n; });
    if (gal) Array.prototype.forEach.call(gal.querySelectorAll('.fav'), function (b) {
      var on = has(b.getAttribute('data-src'));
      b.setAttribute('aria-pressed', on); b.textContent = on ? '♥' : '♡';
      b.title = gal.getAttribute(on ? 'data-saved' : 'data-save');
    });
    if (lbFav) { var s = lbSrc(), on2 = s && has(s); lbFav.hidden = !gal; lbFav.setAttribute('aria-pressed', !!on2); lbFav.textContent = on2 ? '♥' : '♡'; }
  }
  if (gal) gal.addEventListener('click', function (e) {
    var b = e.target.closest('.fav'); if (!b) return;
    e.preventDefault();
    toggle({ s: b.getAttribute('data-src'), p: b.getAttribute('data-p'), t: b.getAttribute('data-t') });
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
  });
  if (lbFav && gal) {
    lbImg.addEventListener('load', paint);
    lbFav.addEventListener('click', function () {
      var s = lbSrc(); if (!s) return;
      var b = gal.querySelector('.fav[data-src="' + s + '"]');
      if (b) toggle({ s: s, p: b.getAttribute('data-p'), t: b.getAttribute('data-t') });
    });
  }
  window.addEventListener('storage', paint);

  // Pagina moodboard
  var pg = document.querySelector('[data-mb-page]');
  if (pg) {
    var root = pg.getAttribute('data-root'), grid = pg.querySelector('.mbgrid');
    var q = new URLSearchParams(location.search).get('p');
    var shared = q ? q.split(',').filter(function (f) { return /^[a-z0-9-]+$/.test(f); }).map(function (f) {
      return { s: 'img/' + f + '.jpg', p: (document.documentElement.lang === 'en' ? 'works/' : 'lavori/') + f.replace(/-\d+$/, '') + '.html', t: '' };
    }) : null;
    var render = function () {
      var l = shared || load();
      grid.innerHTML = '';
      l.forEach(function (x) {
        var d = document.createElement('figure');
        var a = document.createElement('a'), slug = (x.p.match(/([^\/]+)\.html$/) || [, ''])[1];
        a.href = (document.documentElement.lang === 'en' ? 'works/' : 'lavori/') + slug + '.html';
        var im = document.createElement('img'); im.src = root + x.s; im.alt = x.t || ''; im.loading = 'lazy';
        a.appendChild(im); d.appendChild(a);
        if (!shared) {
          var r = document.createElement('button'); r.type = 'button'; r.className = 'rm'; r.textContent = '×';
          r.setAttribute('aria-label', pg.getAttribute('data-remove'));
          r.addEventListener('click', function () { save(load().filter(function (y) { return y.s !== x.s; })); render(); });
          d.appendChild(r);
        }
        grid.appendChild(d);
      });
      pg.querySelector('.mb-empty').hidden = l.length > 0;
      pg.querySelector('.mb-actions').hidden = l.length === 0;
      pg.querySelector('[data-mb-keep]').hidden = !shared;
      pg.querySelector('[data-mb-clear]').hidden = !!shared;
      var c = document.querySelector('[data-mb-count]'); if (c) c.textContent = l.length + (document.documentElement.lang === 'en' ? ' photos' : ' foto');
      var sh = pg.querySelector('.mb-shared'); sh.hidden = !shared; sh.textContent = pg.getAttribute('data-shared');
    };
    pg.querySelector('[data-mb-share]').addEventListener('click', function (e) {
      var l = shared || load(), btn = e.currentTarget;
      var url = location.origin + location.pathname + '?p=' + l.map(function (x) { return x.s.replace(/^img\//, '').replace(/\.jpg$/, ''); }).join(',');
      var done = function () { var o = btn.textContent; btn.textContent = pg.getAttribute('data-copied') + ' ✓'; setTimeout(function () { btn.textContent = o; }, 2000); };
      if (navigator.share && matchMedia('(hover: none)').matches) navigator.share({ url: url }).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { prompt('', url); });
      else prompt('', url);
    });
    pg.querySelector('[data-mb-keep]').addEventListener('click', function () {
      var l = load(); shared.forEach(function (x) { if (!l.some(function (y) { return y.s === x.s; })) l.push(x); });
      save(l); shared = null; history.replaceState(null, '', location.pathname); render();
    });
    pg.querySelector('[data-mb-mail]').addEventListener('click', function () {
      var l = shared || load(), en = document.documentElement.lang === 'en';
      var body = (en ? 'Hi Ruggiero, here is my moodboard:' : 'Ciao Ruggiero, ecco la mia moodboard:') + '\n\n' +
        l.map(function (x) { return 'https://ruggierorusso.com/' + x.s; }).join('\n') + '\n\n';
      location.href = 'mailto:info@ruggierorusso.com?subject=' + encodeURIComponent('Moodboard') + '&body=' + encodeURIComponent(body);
    });
    pg.querySelector('[data-mb-clear]').addEventListener('click', function () { save([]); render(); });
    render();
  }

  // Modulo preventivo: allega la moodboard
  var att = document.querySelector('.mb-att'), hid = document.querySelector('input[name="moodboard"]');
  if (att && hid) {
    var l = load();
    if (l.length) {
      hid.value = l.map(function (x) { return 'https://ruggierorusso.com/' + x.s; }).join('\n');
      var r = att.getAttribute('data-root');
      att.innerHTML = '<p class="label">' + l.length + ' ' + att.getAttribute('data-label') + '</p><div>' +
        l.slice(0, 12).map(function (x) { return '<img src="' + r + x.s + '" alt="">'; }).join('') + '</div>';
      att.hidden = false;
    }
  }
  paint();
})();

// ---- 404: disegna con la luce ----
(function () {
  var s = document.querySelector('[data-lp]'); if (!s) return;
  var c = s.querySelector('canvas'), g = c.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var pts = [], last = null, auto = true, t0 = performance.now();
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function size() { var r = s.getBoundingClientRect(); c.width = r.width * dpr; c.height = r.height * dpr; c.style.width = r.width + 'px'; c.style.height = r.height + 'px'; g.setTransform(dpr, 0, 0, dpr, 0, 0); }
  size(); addEventListener('resize', size);
  function add(x, y) {
    if (last) { var dx = x - last.x, dy = y - last.y, n = Math.max(1, Math.floor(Math.hypot(dx, dy) / 3));
      for (var i = 1; i <= n; i++) pts.push({ x: last.x + dx * i / n, y: last.y + dy * i / n, a: 1 }); }
    last = { x: x, y: y };
  }
  function pos(e) { var r = c.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
  s.addEventListener('pointermove', function (e) { if (e.target.closest('a,button')) return; if (auto) { auto = false; last = null; } var p = pos(e); add(p[0], p[1]); });
  s.addEventListener('pointerdown', function (e) { if (e.target.closest('a,button')) return; auto = false; last = null; var p = pos(e); add(p[0], p[1]); });
  s.addEventListener('pointerup', function () { last = null; });
  s.addEventListener('pointerleave', function () { last = null; });
  s.querySelector('[data-lp-clear]').addEventListener('click', function () { pts = []; last = null; });
  function frame(t) {
    if (auto && !reduce) {
      var w = c.width / dpr, h = c.height / dpr, k = (t - t0) / 1000;
      add(w * (0.5 + 0.36 * Math.sin(k * 0.9)), h * (0.5 + 0.3 * Math.sin(k * 1.7 + 1)));
    }
    g.globalCompositeOperation = 'source-over'; g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height);
    g.globalCompositeOperation = 'lighter';
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i], r = 14;
      var gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
      gr.addColorStop(0, 'rgba(255,240,230,' + 0.5 * p.a + ')');
      gr.addColorStop(0.35, 'rgba(255,42,31,' + 0.35 * p.a + ')');
      gr.addColorStop(1, 'rgba(255,42,31,0)');
      g.fillStyle = gr; g.fillRect(p.x - r, p.y - r, r * 2, r * 2);
      p.a *= 0.996;
    }
    pts = pts.filter(function (p) { return p.a > 0.04; }).slice(-2500);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

// ---- Slide foto accanto a ERRE studio: cambia ogni 2 secondi ----
(function () {
  var box = document.querySelector('[data-slides]'); if (!box) return;
  var imgs = box.querySelectorAll('img'); if (imgs.length < 2) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  Array.prototype.forEach.call(imgs, function (im) { im.loading = 'eager'; });
  var i = 0, timer = null;
  function next() { imgs[i].classList.remove('on'); i = (i + 1) % imgs.length; imgs[i].classList.add('on'); }
  function start() { if (!timer) timer = setInterval(next, 2000); }
  function stop() { clearInterval(timer); timer = null; }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { e[0].isIntersecting ? start() : stop(); }).observe(box); else start();
  document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
})();

// ---- Mappa di ERRE studio: Google Maps si carica solo quando la chiedi ----
(function () {
  var m = document.querySelector('[data-map]'); if (!m) return;
  var b = m.querySelector('[data-map-load]');
  b.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = m.getAttribute('data-map'); f.loading = 'lazy'; f.title = 'ERRE studio – Google Maps';
    f.referrerPolicy = 'no-referrer-when-downgrade'; f.allowFullscreen = true;
    m.appendChild(f);
  });
})();
/* contact form */
(function(){
  var f=document.querySelector('.cform'); if(!f) return;
  var msg=f.querySelector('.fmsg');
  function bad(el,on){var w=el.closest('.f,.pc'); if(w) w.classList.toggle('bad',on);}
  f.addEventListener('input',function(e){bad(e.target,false);});
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=true, first=null;
    ['nome','email','messaggio','privacy'].forEach(function(n){
      var el=f.elements[n], v=el.type==='checkbox'?el.checked:el.value.trim();
      var good=!!v && (n!=='email'||/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim()));
      bad(el,!good); if(!good){ok=false; if(!first) first=el;}
    });
    msg.classList.remove('err');
    if(!ok){msg.textContent=f.dataset.inv; msg.classList.add('err'); first.focus(); return;}
    var d=new URLSearchParams();
    Array.prototype.forEach.call(f.elements,function(el){
      if(!el.name) return;
      if((el.type==='radio'||el.type==='checkbox')&&!el.checked) return;
      d.append(el.name,el.value);
    });
    f.classList.add('sending'); msg.textContent='…';
    fetch(f.action,{method:'POST',body:d}).then(function(r){return r.json();}).then(function(j){
      if(!j.ok) throw 0;
      f.classList.remove('sending'); f.classList.add('done'); msg.textContent=f.dataset.ok;
    }).catch(function(){
      f.classList.remove('sending'); msg.textContent=f.dataset.err; msg.classList.add('err');
    });
  });
})();

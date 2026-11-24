/* ==========================================================================
   THE VIJAYRAN PALACE — motion & interaction
   Re-implements the interaction model of thesujanlife.com with
   GSAP 3.13 (+ScrollTrigger, SplitText, Draggable, Inertia) and Lenis.
   Timings/eases mirror the reference: line reveals y110%→0, power4.out,
   1.8s stagger .1 (titles) / 2.4s stagger .04 (paragraphs), scrubbed
   parallax, clip-path menu, scaleY booking panel, draggable rails.
   ========================================================================== */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = typeof gsap !== 'undefined';
  document.documentElement.classList.toggle('js', hasGsap && !reduce);

  /* ---------- image fallback: local media → live site ---------- */
  $$('img[data-live]').forEach(img => {
    const swap = () => { const l = img.dataset.live; if (l) { img.removeAttribute('data-live'); img.src = l; } };
    img.addEventListener('error', swap, { once: true });
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('loading') !== 'lazy') swap();
  });
  /* local preview (file://): folder links → index.html */
  if (location.protocol === 'file:') document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a) return;
    const h = a.getAttribute('href'); if (/^(https?:|mailto:|tel:|#)/.test(h)) return;
    const [p, hash] = h.split('#'); if (p.endsWith('/')) { e.preventDefault(); location.href = p + 'index.html' + (hash ? '#' + hash : ''); }
  });

  /* ---------- forms (static build: point data-endpoint at a handler) ---------- */
  $$('form[data-form]').forEach(f => f.addEventListener('submit', async e => {
    e.preventDefault();
    if (f.dataset.endpoint) { try { await fetch(f.dataset.endpoint, { method: 'POST', body: new FormData(f) }); } catch (_) {} }
    f.classList.add('sent');
  }));
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

  /* ---------- hero video sound toggle ---------- */
  const vid = $('.hero video'), snd = $('.sound');
  if (vid && snd) snd.addEventListener('click', () => { vid.muted = !vid.muted; snd.classList.toggle('on', !vid.muted); snd.setAttribute('aria-pressed', String(!vid.muted)); });

  /* ---------- lightbox ---------- */
  const lb = $('.lightbox');
  if (lb) {
    $$('.masonry figure').forEach(f => f.addEventListener('click', () => { const i = $('img', f); $('img', lb).src = i.currentSrc || i.src; $('img', lb).alt = i.alt; lb.classList.add('open'); }));
    lb.addEventListener('click', e => { if (e.target.tagName !== 'IMG') lb.classList.remove('open'); });
  }

  /* ---------- accordion (works without GSAP too) ---------- */
  $$('.acc-i').forEach(it => {
    const q = $('.acc-q', it), a = $('.acc-a', it);
    q.addEventListener('click', () => {
      const open = !it.classList.contains('open');
      it.classList.toggle('open', open); q.setAttribute('aria-expanded', String(open));
      if (hasGsap) gsap.to(a, { height: open ? 'auto' : 0, duration: 0.9, ease: 'power4.inOut', onComplete: () => window.ScrollTrigger && ScrollTrigger.refresh() });
      else a.style.height = open ? 'auto' : '0';
    });
  });


  /* ---------- LIVE WEATHER at the palace (Open-Meteo, free, no API key) ---------- */
  (() => {
    const nodes = $$('[data-wx]'); if (!nodes.length) return;
    const LAT = 27.03, LON = 75.89, KEY = 'vj-wx', UNIT = 'vj-wx-unit', TTL = 15 * 60 * 1000;
    const URL = `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,weather_code,is_day&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Asia%2FKolkata`;
    const store = { get: k => { try { return localStorage.getItem(k); } catch (_) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} } };
    let unit = store.get(UNIT) === 'F' ? 'F' : 'C', data = null;
    const I = {
      sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg>',
      moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M19.5 14.6A8 8 0 0 1 9.4 4.5a8 8 0 1 0 10.1 10.1z"/></svg>',
      partly: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><circle cx="8.5" cy="8.5" r="3.2"/><path d="M8.5 2.5v1.4M2.5 8.5h1.4M4.3 4.3l1 1M12.7 4.3l-1 1"/><path d="M8 19.5h9.5a3.5 3.5 0 0 0 .4-7 5 5 0 0 0-9.5 1.3A2.9 2.9 0 0 0 8 19.5z"/></svg>',
      cloud: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M6.5 18.5h11a4 4 0 0 0 .5-8 6 6 0 0 0-11.4 1.6A3.3 3.3 0 0 0 6.5 18.5z"/></svg>',
      fog: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M4 9h16M2.5 13h19M4 17h16M7 21h10"/></svg>',
      rain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M6.5 14.5h11a4 4 0 0 0 .5-8 6 6 0 0 0-11.4 1.6A3.3 3.3 0 0 0 6.5 14.5z"/><path d="M8 17.5l-1 3M12 17.5l-1 3M16 17.5l-1 3"/></svg>',
      storm: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 14.5h11a4 4 0 0 0 .5-8 6 6 0 0 0-11.4 1.6A3.3 3.3 0 0 0 6.5 14.5z"/><path d="M12.5 15.5 10 19h3l-2 3.5"/></svg>',
      snow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/></svg>'
    };
    const describe = (c, day) => {
      if (c === 0) return [day ? 'Clear sky' : 'Clear night', day ? 'sun' : 'moon'];
      if (c === 1) return [day ? 'Mainly sunny' : 'Mainly clear', day ? 'sun' : 'moon'];
      if (c === 2) return ['Partly cloudy', day ? 'partly' : 'cloud'];
      if (c === 3) return ['Overcast', 'cloud'];
      if (c === 45 || c === 48) return ['Haze', 'fog'];
      if (c >= 51 && c <= 57) return ['Drizzle', 'rain'];
      if ((c >= 61 && c <= 67) || (c >= 80 && c <= 82)) return ['Rain', 'rain'];
      if ((c >= 71 && c <= 77) || c === 85 || c === 86) return ['Snow', 'snow'];
      if (c >= 95) return ['Thunderstorm', 'storm'];
      return ['Fair', day ? 'sun' : 'moon'];
    };
    const t = v => Math.round(unit === 'F' ? v * 9 / 5 + 32 : v);
    const time = () => new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' }).format(new Date());
    const render = () => {
      if (!data) return;
      const c = data.current, d = data.daily, [label, ico] = describe(c.weather_code, c.is_day === 1);
      const deg = `°${unit}`;
      $$('[data-wx="icon"]').forEach(n => n.innerHTML = I[ico]);
      $$('[data-wx="temp"]').forEach(n => n.textContent = `${t(c.temperature_2m)}${deg}`);
      $$('[data-wx="desc"]').forEach(n => n.textContent = label);
      $$('[data-wx="hilo"]').forEach(n => n.textContent = `H ${t(d.temperature_2m_max[0])}° / L ${t(d.temperature_2m_min[0])}°`);
      $$('[data-wx="time"]').forEach(n => n.textContent = time());
      $$('[data-wx="inline"]').forEach(n => { n.textContent = `Right now at the palace: ${t(c.temperature_2m)}${deg}, ${label.toLowerCase()} (today H ${t(d.temperature_2m_max[0])}° / L ${t(d.temperature_2m_min[0])}°).`; n.hidden = false; });
      $$('[data-wx="chip"],[data-wx="hero"]').forEach(n => { n.hidden = false; requestAnimationFrame(() => n.classList.add('on')); });
    };
    const load = async (force) => {
      const cached = store.get(KEY);
      if (!force && cached) { try { const o = JSON.parse(cached); if (Date.now() - o.at < TTL) { data = o.d; render(); return; } } catch (_) {} }
      try {
        const r = await fetch(URL); if (!r.ok) throw 0;
        data = await r.json(); store.set(KEY, JSON.stringify({ at: Date.now(), d: data })); render();
      } catch (_) { if (cached) { try { data = JSON.parse(cached).d; render(); } catch (_) {} } }
    };
    $$('[data-wx="temp"], [data-wx="chip"]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); unit = unit === 'C' ? 'F' : 'C'; store.set(UNIT, unit); render(); }));
    load(false);
    setInterval(() => load(true), TTL);
    setInterval(() => $$('[data-wx="time"]').forEach(n => n.textContent = time()), 30000);
  })();

  const nav = $('.nav');
  const menu = $('.menu'), menuBtn = $('.nav-menu');
  const book = $('.book'), bookBtn = $('.book > button'), bookPanel = $('.book-panel');

  if (!hasGsap || reduce) {
    /* graceful no-motion fallback */
    menuBtn?.addEventListener('click', () => { const o = menu.style.display !== 'block'; menu.style.display = o ? 'block' : 'none'; menu.style.clipPath = 'none'; document.body.classList.toggle('menu-open', o); });
    bookBtn?.addEventListener('click', e => { e.stopPropagation(); bookPanel.style.display = bookPanel.style.display === 'block' ? 'none' : 'block'; });
    const solid = () => nav && nav.classList.toggle('is-solid', !$('.hero') || scrollY > innerHeight * .8);
    solid(); addEventListener('scroll', solid, { passive: true });
    $$('.rail').forEach(r => { r.style.overflowX = 'auto'; });
    return;
  }

  gsap.registerPlugin(ScrollTrigger, SplitText, Draggable, InertiaPlugin);

  /* ---------- Lenis smooth scroll ---------- */
  let lenis = null;
  if (typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const t = $(a.getAttribute('href')); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -80 }); } }));
  }

  /* ---------- nav state ---------- */
  const hero = $('.hero');
  if (nav && !nav.classList.contains('is-light')) {
    const navSolid = () => nav.classList.toggle('is-solid', (lenis ? lenis.scroll : scrollY) > (hero ? hero.offsetHeight * .85 : 1));
    navSolid(); ScrollTrigger.create({ start: 0, end: 'max', onUpdate: navSolid }); addEventListener('scroll', navSolid, { passive: true });
  }

  /* ---------- MENU (clip-path wipe + staggered line reveals) ---------- */
  if (menu && menuBtn) {
    const items = $$('.m-col h4 span, .m-link span, .m-card p span, .m-social a span', menu);
    const pics = $$('.m-card .im', menu);
    gsap.set(items, { yPercent: 105 });
    const tl = gsap.timeline({ paused: true, onReverseComplete: () => { gsap.set(menu, { display: 'none' }); } })
      .set(menu, { display: 'block' })
      .fromTo(menu, { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power4.inOut' })
      .to(items, { yPercent: 0, duration: 1.2, ease: 'power4.out', stagger: .025 }, .45)
      .fromTo(pics, { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.2, ease: 'power4.inOut', stagger: .08 }, .5);
    let open = false;
    const toggle = o => {
      open = o; document.body.classList.toggle('menu-open', o);
      menuBtn.setAttribute('aria-expanded', String(o));
      nav.classList.toggle('is-menu', o);
      if (o) { closeBook(); lenis?.stop(); tl.timeScale(1).play(); nav.classList.add('is-light'); }
      else { lenis?.start(); tl.timeScale(1.6).reverse(); if (!nav.dataset.light) nav.classList.remove('is-light'); }
    };
    menuBtn.addEventListener('click', () => toggle(!open));
    addEventListener('keydown', e => { if (e.key === 'Escape' && open) toggle(false); });
    $$('a', menu).forEach(a => a.addEventListener('click', () => open && toggle(false)));
  }
  if (nav?.classList.contains('is-light')) nav.dataset.light = '1';

  /* ---------- BOOK NOW panel (scaleY + sliding thumbnails) ---------- */
  let bookTl, bookOpen = false;
  function closeBook() { if (bookOpen) { bookOpen = false; book.classList.remove('open'); bookTl.timeScale(1.8).reverse(); } }
  if (book && bookPanel) {
    const ims = $$('.book-item .im img', bookPanel), txs = $$('.book-item .tx > *', bookPanel);
    bookTl = gsap.timeline({ paused: true, onReverseComplete: () => gsap.set(bookPanel, { display: 'none' }) })
      .set(bookPanel, { display: 'block' })
      .fromTo(bookPanel, { scaleY: 0, opacity: 1 }, { scaleY: 1, duration: 1, ease: 'power4.inOut' })
      .fromTo(ims, { xPercent: -100 }, { xPercent: 0, duration: 1.1, ease: 'power4.inOut', stagger: .03 }, .35)
      .fromTo(txs, { yPercent: 105, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1.1, ease: 'power4.inOut', stagger: .02 }, .45);
    bookBtn.addEventListener('click', e => { e.stopPropagation(); bookOpen = !bookOpen; book.classList.toggle('open', bookOpen); bookOpen ? bookTl.timeScale(1).play() : bookTl.timeScale(1.8).reverse(); });
    document.addEventListener('click', e => { if (!book.contains(e.target)) closeBook(); });
  }

  /* ---------- SPLIT-LINE REVEALS ---------- */
  const splitReveal = (el, opts) => {
    const st = SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'ln', autoSplit: false });
    el.classList.add('is-ready');
    gsap.fromTo(st.lines, { yPercent: 110 }, {
      yPercent: 0, duration: opts.d, ease: 'power4.out', stagger: opts.s, delay: opts.delay || 0,
      scrollTrigger: opts.immediate ? null : { trigger: el, start: opts.start, once: true },
      onComplete: () => { st.revert(); }
    });
  };
  document.fonts.ready.then(() => {
    $$('[data-split]').forEach(el => {
      const kind = el.dataset.split;
      if (kind === 'hero') splitReveal(el, { d: 1.8, s: .1, immediate: true, delay: .35 });
      else if (kind === 'text') splitReveal(el, { d: 2.4, s: .04, start: 'top 95%' });
      else splitReveal(el, { d: 1.8, s: .1, start: 'top 90%' });
    });
    ScrollTrigger.refresh();
  });

  /* ---------- HERO video zoom + INTRO card scale-up ---------- */
  const intro = $('.intro'), heroMedia = $('.hero-media');
  if (hero && intro) {
    gsap.fromTo(intro, { scale: .8, yPercent: -17.5 }, { scale: 1, yPercent: 0, ease: 'power2.out',
      scrollTrigger: { trigger: hero, start: 'top 92%', end: 'bottom 30%', scrub: 2, invalidateOnRefresh: true } });
    if (heroMedia) gsap.fromTo(heroMedia, { scale: 1 }, { scale: 1.5, ease: 'none', scrollTrigger: { trigger: intro, start: 'top bottom', end: 'bottom top', scrub: true } });
  } else if (heroMedia) {
    gsap.to(heroMedia, { scale: 1.25, yPercent: 8, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }
  if (heroMedia) gsap.from(heroMedia, { scale: 1.12, duration: 2.4, ease: 'power3.out' });

  /* ---------- QUOTE OVER IMAGE (cert) ---------- */
  $$('.cert').forEach(sec => {
    const line = $('.cert-lbl i', sec), lbl = $('.cert-lbl span', sec), img = $('.cert-img', sec);
    gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top 40%', once: true } })
      .fromTo(line, { scaleX: 0 }, { scaleX: 1, duration: 2.6, ease: 'power4.out' })
      .fromTo(lbl, { yPercent: 110 }, { yPercent: 0, duration: 2.6, ease: 'power4.out' }, '<');
    gsap.fromTo(img, { scale: 1, yPercent: 0 }, { scale: 1.2, yPercent: 10, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- DRAG RAILS (collection, experiences, gallery) ---------- */
  $$('[data-rail]').forEach(sec => {
    const rail = $('.rail', sec), track = $('.rail-track', sec);
    if (!rail || !track) return;
    
    const isAuto = sec.dataset.autoScroll === 'true';
    if (isAuto) {
      track.innerHTML += track.innerHTML;
    }
    
    const items = $$('.ca-item', track);
    const bar = $('.rail-bar i', sec), dots = $('.dots', sec);
    let max = 0;
    const measure = () => { max = Math.max(0, track.scrollWidth - rail.clientWidth); };
    measure();
    const upd = () => {
      const x = gsap.getProperty(track, 'x');
      const baseSpan = isAuto ? (track.scrollWidth / 2) : max;
      const p = baseSpan ? Math.abs(x % baseSpan) / baseSpan : 0;
      if (bar) gsap.set(bar, { left: `${p * 80}%` });
      if (dots) { const i = Math.round(p * (items.length - 1)); $$('button', dots).forEach((b, j) => b.classList.toggle('on', i === j)); }
    };
    const dragBounds = isAuto ? { minX: -track.scrollWidth + rail.clientWidth, maxX: 0 } : { minX: -max, maxX: 0 };
    const drag = Draggable.create(track, { type: 'x', inertia: true, edgeResistance: isAuto ? 0.6 : 0.9, bounds: dragBounds, allowContextMenu: true, zIndexBoost: false,
      onDrag: upd, onThrowUpdate: upd, onPress() { this.startX = this.x; }, onClick() {} })[0];
    $$('a', track).forEach(a => a.addEventListener('click', e => { if (Math.abs(drag.x - (drag.startX ?? drag.x)) > 6) e.preventDefault(); }));
    const step = () => (items[0]?.offsetWidth || 400) + parseFloat(getComputedStyle(track).columnGap || 24);
    const go = x => {
      if (isAuto) {
        const half = track.scrollWidth / 2;
        if (x < -half) x += half;
        if (x > 0) x -= half;
      } else {
        x = gsap.utils.clamp(-max, 0, x);
      }
      gsap.to(track, { x, duration: 1.2, ease: 'power4.out', onUpdate: () => { drag.update(); upd(); } });
    };
    $('[data-prev]', sec)?.addEventListener('click', () => go(gsap.getProperty(track, 'x') + step()));
    $('[data-next]', sec)?.addEventListener('click', () => go(gsap.getProperty(track, 'x') - step()));
    if (dots) { dots.innerHTML = items.map((_, i) => `<button aria-label="Slide ${i + 1}"></button>`).join(''); $$('button', dots).forEach((b, i) => b.addEventListener('click', () => go(-Math.min(max, items[i].offsetLeft)))); }
    rail.tabIndex = 0; rail.addEventListener('keydown', e => { if (e.key === 'ArrowRight') go(gsap.getProperty(track, 'x') - step()); if (e.key === 'ArrowLeft') go(gsap.getProperty(track, 'x') + step()); });
    addEventListener('resize', () => { measure(); drag.applyBounds(isAuto ? { minX: -track.scrollWidth + rail.clientWidth, maxX: 0 } : { minX: -max, maxX: 0 }); upd(); });
    upd();

    if (isAuto) {
      let speed = 0.75;
      let hovered = false;
      let userInteracting = false;
      let resumeTimer = null;
      let inView = false;
      
      ScrollTrigger.create({
        trigger: sec,
        start: 'top bottom',
        end: 'bottom top',
        onEnter: () => inView = true,
        onLeave: () => inView = false,
        onEnterBack: () => inView = true,
        onLeaveBack: () => inView = false
      });
      
      const tick = () => {
        if (!inView || hovered || userInteracting) return;
        const half = track.scrollWidth / 2;
        if (!half) return;
        let cur = gsap.getProperty(track, 'x') - speed;
        if (cur <= -half) cur += half;
        gsap.set(track, { x: cur });
        drag.update();
        upd();
      };
      
      gsap.ticker.add(tick);
      
      sec.addEventListener('mouseenter', () => { hovered = true; });
      sec.addEventListener('mouseleave', () => { hovered = false; });
      
      const pauseAuto = () => {
        userInteracting = true;
        clearTimeout(resumeTimer);
      };
      const resumeAuto = () => {
        clearTimeout(resumeTimer);
        resumeTimer = setTimeout(() => { userInteracting = false; }, 2200);
      };
      
      drag.addEventListener('press', pauseAuto);
      drag.addEventListener('dragEnd', resumeAuto);
      drag.addEventListener('throwComplete', resumeAuto);
      $('[data-prev]', sec)?.addEventListener('click', () => { pauseAuto(); resumeAuto(); });
      $('[data-next]', sec)?.addEventListener('click', () => { pauseAuto(); resumeAuto(); });
      
      gsap.fromTo(items, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1, stagger: 0.04, ease: 'power3.out', scrollTrigger: { trigger: sec, start: 'top 85%', once: true } });
    } else {
      /* items rise into place as the section scrolls in (scrubbed) */
      gsap.fromTo(items, { yPercent: 50 }, { yPercent: 0, ease: 'none', stagger: { each: .1 }, scrollTrigger: { trigger: sec, start: 'top center', end: 'bottom bottom', scrub: 1 } });
    }
    $$('.ca-line', sec).forEach(l => gsap.fromTo(l, { scaleX: 0 }, { scaleX: 1, duration: 2, ease: 'power4.out', scrollTrigger: { trigger: l, start: 'top 95%', once: true } }));
  });

  /* ---------- STORY: sticky text, images drift (desktop) ---------- */
  ScrollTrigger.matchMedia({
    '(min-width: 992px)': () => {
      $$('.story').forEach(sec => {
        const tl = gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 1 } });
        $$('.story-item', sec).forEach((it, i) => {
          tl.fromTo(it, { yPercent: 3 }, { yPercent: -3, duration: 1 + i * .2, ease: 'none' }, 0)
            .to($('img', it), { scale: 1.1, duration: 1.4, ease: 'none' }, 0);
        });
      });
    }
  });

  /* ---------- STACKING CARDS ---------- */
  $$('.stack-item').forEach((it, i) => {
    const img = $(':scope > img', it), panel = $('.stack-panel', it);
    gsap.fromTo(img, { scale: 1.18 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: it, start: 'top bottom', end: 'top top', scrub: true } });
    if (panel) gsap.fromTo(panel, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 1.6, ease: 'power4.out', scrollTrigger: { trigger: it, start: 'top 35%', toggleActions: 'play none none reverse' } });
  });

  /* ---------- RED FEATURE image parallax ---------- */
  $$('.feat .im img').forEach(img => gsap.fromTo(img, { yPercent: -8, scale: 1.18 }, { yPercent: 8, scale: 1.18, ease: 'none', scrollTrigger: { trigger: img.closest('.feat'), start: 'top bottom', end: 'bottom top', scrub: true } }));

  /* ---------- generic image reveals ---------- */
  $$('[data-reveal]').forEach(el => {
    const img = $('img', el) || el;
    gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 88%', once: true } })
      .fromTo(el, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.6, ease: 'power4.inOut' })
      .fromTo(img, { scale: 1.25 }, { scale: 1, duration: 2.2, ease: 'power3.out' }, 0);
  });
  $$('[data-fade]').forEach(el => gsap.fromTo(el, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.6, ease: 'power4.out', scrollTrigger: { trigger: el, start: 'top 92%', once: true } }));
  $$('.sk path, .sk circle').forEach(p => {
    try { const L = p.getTotalLength(); gsap.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 2.6, ease: 'power2.inOut', scrollTrigger: { trigger: p.closest('svg'), start: 'top 85%', once: true } }); } catch (_) {}
  });

  /* ==========================================================================
     ROYAL TYPOGRAPHY STUDIO (Live Font Switcher & Persistence)
     ========================================================================== */
  (() => {
    const PRESET_KEY = 'vj-font-preset';
    const widget = $('#royalFontWidget');
    const toggleBtn = $('#rfToggleBtn');
    const panel = $('#rfPanel');
    const closeBtn = $('#rfCloseBtn');
    const resetBtn = $('#rfResetBtn');
    const opts = $$('.rf-opt');

    const setPreset = (preset, save = true) => {
      document.documentElement.setAttribute('data-font-preset', preset);
      opts.forEach(o => o.classList.toggle('is-active', o.dataset.preset === preset));
      if (save) {
        try { localStorage.setItem(PRESET_KEY, preset); } catch (_) {}
      }
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    };

    // Load saved preset or default to caslon (Font #10 Libre Caslon Display)
    let saved = 'caslon';
    try { saved = localStorage.getItem(PRESET_KEY) || 'caslon'; } catch (_) {}
    setPreset(saved, false);

    if (toggleBtn && panel) {
      toggleBtn.addEventListener('click', () => {
        const isOpen = !panel.hasAttribute('hidden');
        if (isOpen) {
          panel.setAttribute('hidden', '');
          toggleBtn.setAttribute('aria-expanded', 'false');
        } else {
          panel.removeAttribute('hidden');
          toggleBtn.setAttribute('aria-expanded', 'true');
        }
      });
    }

    if (closeBtn && panel) {
      closeBtn.addEventListener('click', () => {
        panel.setAttribute('hidden', '');
        toggleBtn?.setAttribute('aria-expanded', 'false');
      });
    }

    // Close panel if clicked outside
    document.addEventListener('click', e => {
      if (widget && !widget.contains(e.target) && panel && !panel.hasAttribute('hidden')) {
        panel.setAttribute('hidden', '');
        toggleBtn?.setAttribute('aria-expanded', 'false');
      }
    });

    opts.forEach(opt => {
      opt.addEventListener('click', () => {
        const preset = opt.dataset.preset;
        if (preset) setPreset(preset);
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', () => setPreset('caslon'));
    }
  })();

  /* ==========================================================================
     WEDDINGS AT THE PALACE — INTERACTIVE VENUE SHOWCASE
     ========================================================================== */
  (() => {
    const mainImg = $('#hwMainImg');
    const title = $('#hwCardTitle');
    const desc = $('#hwCardDesc');
    const badgeTag = $('#hwBadgeTag');
    const badgeSetting = $('#hwBadgeSetting');
    const hl1 = $('#hwHl1');
    const hl2 = $('#hwHl2');
    const hl3 = $('#hwHl3');
    const cards = $$('.hw-vcard');

    if (!mainImg || !cards.length) return;

    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('is-active'));
        card.classList.add('is-active');

        // Cross-fade image transition
        if (hasGsap) {
          gsap.to(mainImg, {
            opacity: 0,
            scale: 0.98,
            duration: 0.25,
            ease: 'power2.in',
            onComplete: () => {
              mainImg.src = card.dataset.img;
              mainImg.alt = card.dataset.title;
              if (title) title.textContent = card.dataset.title;
              if (desc) desc.textContent = card.dataset.desc;
              if (badgeTag) badgeTag.textContent = card.dataset.tag;
              if (badgeSetting) badgeSetting.textContent = card.dataset.setting;
              if (hl1) hl1.textContent = card.dataset.hl1;
              if (hl2) hl2.textContent = card.dataset.hl2;
              if (hl3) hl3.textContent = card.dataset.hl3;

              gsap.to(mainImg, { opacity: 1, scale: 1, duration: 0.45, ease: 'power2.out' });
            }
          });
        } else {
          mainImg.src = card.dataset.img;
          mainImg.alt = card.dataset.title;
          if (title) title.textContent = card.dataset.title;
          if (desc) desc.textContent = card.dataset.desc;
          if (badgeTag) badgeTag.textContent = card.dataset.tag;
          if (badgeSetting) badgeSetting.textContent = card.dataset.setting;
          if (hl1) hl1.textContent = card.dataset.hl1;
          if (hl2) hl2.textContent = card.dataset.hl2;
          if (hl3) hl3.textContent = card.dataset.hl3;
        }
      });
    });
  })();

  /* ==========================================================================
     3D MAGNETIC TILT MOTION ([data-tilt])
     ========================================================================== */
  (() => {
    if (reduce) return;
    const tiltEls = $$('[data-tilt]');
    tiltEls.forEach(el => {
      let rect = null;
      const onMove = e => {
        if (!rect) rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const cx = rect.width / 2;
        const cy = rect.height / 2;
        const rotX = ((y - cy) / cy) * -6;
        const rotY = ((x - cx) / cx) * 6;
        el.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.01, 1.01, 1.01)`;
      };
      const onLeave = () => {
        rect = null;
        el.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      };
      el.addEventListener('mouseenter', () => { rect = el.getBoundingClientRect(); });
      el.addEventListener('mousemove', onMove);
      el.addEventListener('mouseleave', onLeave);
    });
  })();

  addEventListener('load', () => ScrollTrigger.refresh());
})();

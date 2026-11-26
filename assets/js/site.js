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
      } catch (_) {
        if (cached) { try { data = JSON.parse(cached).d; render(); return; } catch (_) {} }
        const hr = Number(new Intl.DateTimeFormat('en-GB', { hour: 'numeric', hour12: false, timeZone: 'Asia/Kolkata' }).format(new Date()));
        data = { current: { temperature_2m: 27, weather_code: 0, is_day: (hr >= 6 && hr < 19) ? 1 : 0 }, daily: { temperature_2m_max: [31], temperature_2m_min: [17] } };
        render();
      }
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

  /* ---------- Lenis smooth scroll + scroll-velocity card physics ---------- */
  let lenis = null;
  if (typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    let curSkew = 0, targetSkew = 0;
    lenis.on('scroll', ({ velocity }) => { targetSkew = gsap.utils.clamp(-1.8, 1.8, velocity * 0.05); });
    gsap.ticker.add(t => {
      lenis.raf(t * 1000);
      targetSkew *= 0.9;
      curSkew += (targetSkew - curSkew) * 0.16;
      if (Math.abs(curSkew) > 0.005) document.documentElement.style.setProperty('--vj-skew', `${curSkew.toFixed(3)}deg`);
      else if (curSkew !== 0) { curSkew = 0; document.documentElement.style.setProperty('--vj-skew', '0deg'); }
    });
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

  /* ---------- DRAG & CONTINUOUS AUTO-GLIDE RAILS (collection, experiences, gallery) ---------- */
  $$('[data-rail]').forEach(sec => {
    const rail = $('.rail', sec), track = $('.rail-track', sec);
    if (!rail || !track) return;

    const origHTML = track.innerHTML;
    const origCount = track.children.length;
    const canLoop = origCount > 1;
    if (canLoop) {
      track.innerHTML = origHTML + origHTML + origHTML;
    }

    const items = $$('.ca-item', track);
    const bar = $('.rail-bar i', sec), dots = $('.dots', sec);
    let cycleWidth = 0, max = 0;

    const measure = () => {
      cycleWidth = canLoop && track.children[origCount]
        ? (track.children[origCount].offsetLeft - track.children[0].offsetLeft)
        : 0;
      max = Math.max(0, track.scrollWidth - rail.clientWidth);
    };
    measure();
    if (cycleWidth > 0) gsap.set(track, { x: -cycleWidth });

    const recenter = () => {
      if (!cycleWidth) return;
      const x = gsap.getProperty(track, 'x');
      if (x <= -2 * cycleWidth) {
        gsap.set(track, { x: x + cycleWidth });
        drag?.update();
      } else if (x >= 0) {
        gsap.set(track, { x: x - cycleWidth });
        drag?.update();
      }
    };

    const upd = () => {
      const x = gsap.getProperty(track, 'x');
      const rel = cycleWidth ? (((-x - cycleWidth) % cycleWidth + cycleWidth) % cycleWidth) : Math.abs(x);
      const p = cycleWidth ? (rel / cycleWidth) : (max ? Math.min(1, Math.abs(x) / max) : 0);
      if (bar) gsap.set(bar, { left: `${p * 80}%` });
      if (dots && origCount) {
        const active = Math.round(p * origCount) % origCount;
        $$('button', dots).forEach((b, j) => b.classList.toggle('on', active === j));
      }
    };

    let hovered = false;
    let userInteracting = false;
    let resumeTimer = null;
    let inView = false;

    const pauseAuto = () => {
      userInteracting = true;
      clearTimeout(resumeTimer);
    };
    const resumeAuto = () => {
      clearTimeout(resumeTimer);
      resumeTimer = setTimeout(() => { userInteracting = false; }, 2200);
    };

    const drag = Draggable.create(track, {
      type: 'x',
      inertia: true,
      edgeResistance: canLoop ? 0.65 : 0.9,
      bounds: { minX: -max, maxX: 0 },
      allowContextMenu: true,
      zIndexBoost: false,
      onPress() { this.startX = this.x; pauseAuto(); },
      onDrag: upd,
      onThrowUpdate: upd,
      onDragEnd() { if (!this.isThrowing) { recenter(); resumeAuto(); } },
      onThrowComplete() { recenter(); resumeAuto(); },
      onClick() {}
    })[0];

    $$('a', track).forEach(a => a.addEventListener('click', e => {
      if (Math.abs(drag.x - (drag.startX ?? drag.x)) > 6) e.preventDefault();
    }));

    const step = () => (items[0]?.offsetWidth || 400) + parseFloat(getComputedStyle(track).columnGap || 24);
    const go = targetX => {
      pauseAuto();
      gsap.killTweensOf(track);
      if (!canLoop) targetX = gsap.utils.clamp(-max, 0, targetX);
      gsap.to(track, {
        x: targetX,
        duration: 1.15,
        ease: 'power4.out',
        onUpdate: () => { drag.update(); upd(); },
        onComplete: () => { recenter(); upd(); resumeAuto(); }
      });
    };

    $('[data-prev]', sec)?.addEventListener('click', () => { recenter(); go(gsap.getProperty(track, 'x') + step()); });
    $('[data-next]', sec)?.addEventListener('click', () => { recenter(); go(gsap.getProperty(track, 'x') - step()); });

    if (dots) {
      dots.innerHTML = Array.from({ length: origCount }, (_, i) => `<button aria-label="Slide ${i + 1}"></button>`).join('');
      $$('button', dots).forEach((b, i) => b.addEventListener('click', () => {
        const base = track.children[origCount];
        const target = track.children[origCount + i];
        const offset = base && target ? (target.offsetLeft - base.offsetLeft) : 0;
        go(-(cycleWidth + offset));
      }));
    }

    rail.tabIndex = 0;
    rail.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { recenter(); go(gsap.getProperty(track, 'x') - step()); }
      if (e.key === 'ArrowLeft') { recenter(); go(gsap.getProperty(track, 'x') + step()); }
    });

    addEventListener('resize', () => {
      const prevCycle = cycleWidth;
      measure();
      if (canLoop && cycleWidth && !prevCycle) gsap.set(track, { x: -cycleWidth });
      drag.applyBounds({ minX: -max, maxX: 0 });
      recenter();
      upd();
    });
    upd();

    if (canLoop) {
      const speed = sec.classList.contains('gal') ? 0.5 : 0.6;
      ScrollTrigger.create({
        trigger: sec,
        start: 'top bottom',
        end: 'bottom top',
        onEnter: () => { inView = true; },
        onLeave: () => { inView = false; },
        onEnterBack: () => { inView = true; },
        onLeaveBack: () => { inView = false; }
      });

      gsap.ticker.add(() => {
        if (!inView || hovered || userInteracting || !cycleWidth) return;
        gsap.set(track, { x: gsap.getProperty(track, 'x') - speed });
        recenter();
        drag.update();
        upd();
      });

      sec.addEventListener('mouseenter', () => { hovered = true; });
      sec.addEventListener('mouseleave', () => { hovered = false; });
    }

    /* Scroll-scrubbed card cascade, horizontal rail glide & inner window image parallax */
    gsap.fromTo(items,
      { y: i => 60 + (i % 4) * 26, scale: 0.92, opacity: 0.35 },
      { y: 0, scale: 1, opacity: 1, ease: 'power2.out',
        scrollTrigger: { trigger: sec, start: 'top 95%', end: 'top 28%', scrub: 0.85 } }
    );
    gsap.fromTo(rail,
      { xPercent: 4.5 },
      { xPercent: -4.5, ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.9 } }
    );
    const cardImgs = $$('.ca-item .im img', track);
    if (cardImgs.length) {
      gsap.fromTo(cardImgs,
        { scale: 1.22, yPercent: -13 },
        { scale: 1.06, yPercent: 13, ease: 'none',
          scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.6 } }
      );
    }
    $$('.ca-line', sec).forEach(l => gsap.fromTo(l, { scaleX: 0 }, {
      scaleX: 1, ease: 'none',
      scrollTrigger: { trigger: sec, start: 'top 90%', end: 'top 38%', scrub: 0.7 }
    }));
  });

  /* ---------- STORY: sticky text, images drift (desktop) ---------- */
  ScrollTrigger.matchMedia({
    '(min-width: 1081px)': () => {
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
  $$('.stack-item').forEach((it) => {
    const img = $(':scope > img', it), panel = $('.stack-panel', it);
    if (img) gsap.fromTo(img, { scale: 1.2, yPercent: -5 }, { scale: 1, yPercent: 5, ease: 'none', scrollTrigger: { trigger: it, start: 'top bottom', end: 'bottom top', scrub: 0.7 } });
    if (panel) {
      gsap.fromTo(panel,
        { y: 90, scale: 0.93, opacity: 0.2 },
        { y: 0, scale: 1, opacity: 1, ease: 'power2.out',
          scrollTrigger: { trigger: it, start: 'top 85%', end: 'top 15%', scrub: 0.8 } }
      );
    }
  });

  /* ---------- RED FEATURE scroll-scrubbed inset frame + image parallax ---------- */
  $$('.feat').forEach(sec => {
    const imWrap = $('.im', sec), img = $('.im img', sec), tx = $('.tx', sec);
    if (imWrap) gsap.fromTo(imWrap,
      { clipPath: 'inset(11% 8% 11% 8% round 0.75rem)' },
      { clipPath: 'inset(0% 0% 0% 0% round 0rem)', ease: 'power2.out',
        scrollTrigger: { trigger: sec, start: 'top 92%', end: 'top 32%', scrub: 0.85 } }
    );
    if (img) gsap.fromTo(img,
      { yPercent: -13, scale: 1.24 },
      { yPercent: 13, scale: 1.06, ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.6 } }
    );
    if (tx) gsap.fromTo(tx,
      { y: 45 },
      { y: -25, ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.9 } }
    );
  });

  /* ---------- generic image reveals (excluding masonry cards handled below) ---------- */
  $$('[data-reveal]:not(.masonry figure)').forEach(el => {
    const img = $('img', el) || el;
    gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 92%', end: 'top 35%', scrub: 0.8 } })
      .fromTo(el, { clipPath: 'inset(24% 6% 24% 6%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'power2.out' })
      .fromTo(img, { scale: 1.24 }, { scale: 1, ease: 'power2.out' }, 0);
  });
  const scrubManagedSelector = '.story-diptych, .itin .map, #hwStage, .hw-nav-tabs, .hw-stats-strip, .pk > article, .contact-cols > div';
  $$('[data-fade]').filter(el => !el.matches(scrubManagedSelector)).forEach(el => {
    gsap.fromTo(el, { opacity: 0.15, y: 42 }, {
      opacity: 1, y: 0, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 94%', end: 'top 52%', scrub: 0.75 }
    });
  });

  /* ==========================================================================
     SCROLL-BASED CARD & SECTION MOTION LAYER — every page, every card
     ========================================================================== */
  (() => {
    const skip = el => el.matches('[data-fade], [data-split], [data-reveal]') || Boolean(el.closest('[data-split], [data-reveal], .menu, .book-panel, .nav, .stack-panel, .story-chronicle, .maharaja-scroll'));
    const scrubRise = (els, o = {}) => {
      els = els.filter(el => o.any || !skip(el)); if (!els.length) return;
      els.forEach((el, i) => {
        const yFrom = (o.y ?? 45) + (i % (o.mod || 4)) * (o.step ?? 16);
        gsap.fromTo(el,
          { opacity: o.oFrom ?? 0.2, y: yFrom, scale: o.scale ?? 0.95 },
          { opacity: 1, y: 0, scale: 1, ease: 'power2.out',
            scrollTrigger: { trigger: o.trigger || el, start: o.start || 'top 94%', end: o.end || 'top 50%', scrub: o.scrub ?? 0.8 } }
        );
      });
    };

    /* 1. Gold scroll-progress hairline */
    const bar = document.createElement('div'); bar.className = 'scroll-progress'; document.body.appendChild(bar);
    gsap.to(bar, { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .3 } });

    /* 2. Nav glides away on scroll down, returns immediately on scroll up */
    if (nav) ScrollTrigger.create({ start: 120, end: 'max', onUpdate: s => {
      if (document.body.classList.contains('menu-open') || book?.classList.contains('open')) return nav.classList.remove('is-hidden');
      nav.classList.toggle('is-hidden', s.direction === 1 && s.scroll() > innerHeight * .6);
    }, onLeaveBack: () => nav.classList.remove('is-hidden') });

    /* 3. Hero: kicker tracked reveal & continuous living zoom-drift on photo/video */
    $$('.hero-cap .lbl').forEach(l => gsap.from(l, { opacity: 0, y: 20, letterSpacing: '.48em', duration: 2, ease: 'power3.out', delay: .2 }));
    $$('.hero-media img, .hero-media video').forEach(m => gsap.to(m, { scale: 1.08, xPercent: -1.5, duration: 14, ease: 'sine.inOut', yoyo: true, repeat: -1 }));

    /* 4. Kicker labels across all sections: scroll-scrubbed letter-spacing tighten */
    $$('main .lbl').filter(el => !skip(el) && !el.closest('.hero-cap, .wx-hero')).forEach(l => {
      const targetLS = getComputedStyle(l).letterSpacing;
      gsap.fromTo(l,
        { opacity: 0.15, letterSpacing: '.42em', y: 14 },
        { opacity: 1, letterSpacing: targetLS, y: 0, ease: 'power2.out',
          scrollTrigger: { trigger: l, start: 'top 95%', end: 'top 62%', scrub: 0.7 } }
      );
    });

    /* 5. Royal ornaments self-draw with scroll */
    $$('main .orn, footer .orn').filter(o => !o.closest('.story-chronicle')).forEach(o => {
      const ps = $$('path', o), dot = $('circle', o);
      ps.forEach(p => { try { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); } catch (_) {} });
      const tl = gsap.timeline({ scrollTrigger: { trigger: o, start: 'top 94%', end: 'top 58%', scrub: 0.8 } });
      tl.to(ps, { strokeDashoffset: 0, duration: 1, ease: 'none', stagger: .12 });
      if (dot) tl.from(dot, { scale: 0, transformOrigin: '50% 50%', duration: .45, ease: 'back.out(2)' }, '-=.35');
    });

    /* 6. Buttons & CTAs scrub smoothly into place */
    scrubRise($$('main .btn'), { y: 26, step: 10, scale: 0.97, start: 'top 96%', end: 'top 68%', scrub: 0.65 });

    /* 7. Accurate count-up for heritage figures & distances (preserves decimals & commas) */
    $$('.sdp-num, .hw-stat-n, .ims-num, .f-badge > span').forEach(el => {
      const node = [...el.childNodes].find(n => n.nodeType === 3 && /\d/.test(n.textContent)); if (!node) return;
      const m = node.textContent.match(/^(\D*)([\d,]+(?:\.\d+)?)(.*)$/s); if (!m) return;
      const end = parseFloat(m[2].replace(/,/g, '')), comma = m[2].includes(','), dec = (m[2].split('.')[1] || '').length, o = { v: 0 };
      const fmt = v => {
        const num = dec ? v.toFixed(dec) : (comma ? Math.round(v).toLocaleString('en-IN') : String(Math.round(v)));
        return m[1] + num + m[3];
      };
      node.textContent = fmt(0);
      gsap.to(o, { v: end, duration: 2.1, ease: 'power2.out', onUpdate: () => { node.textContent = fmt(o.v); },
        scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
    });

    /* 8. Day Clock & Activity Card (#experiences) scroll-scrubbed depth */
    $$('.day-clock-section').forEach(sec => {
      const clockCol = $('.dcs-clock-col', sec), actCol = $('.dcs-activity-col', sec), imgIn = $$('.dcs-img-inner', sec);
      if (clockCol) gsap.fromTo(clockCol, { y: 55, scale: 0.94 }, { y: -25, scale: 1, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.9 } });
      if (actCol) gsap.fromTo(actCol, { y: 95, scale: 0.92 }, { y: -35, scale: 1.01, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.85 } });
      if (imgIn.length) gsap.fromTo(imgIn, { yPercent: -10 }, { yPercent: 10, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.65 } });
    });

    /* 9. Weddings Venue Cards & Featured Arch Stage Card (#weddings) scroll-scrubbed depth */
    $$('.home-wedding').forEach(sec => {
      const tabs = $$('.hw-tab', sec), media = $('.hw-stage-media', sec), info = $('.hw-stage-info', sec), mImg = $('#hwMainImg', sec), stats = $$('.hw-stat', sec);
      if (tabs.length) scrubRise(tabs, { any: true, trigger: $('.hw-nav-tabs', sec), y: 40, step: 18, scale: 0.94, start: 'top 92%', end: 'top 48%', scrub: 0.75 });
      if (media) gsap.fromTo(media, { y: 85, scale: 0.92 }, { y: -35, scale: 1.02, ease: 'none', scrollTrigger: { trigger: '#hwStage', start: 'top bottom', end: 'bottom top', scrub: 0.9 } });
      if (mImg) gsap.fromTo(mImg, { scale: 1.18, yPercent: -11 }, { scale: 1.04, yPercent: 11, ease: 'none', scrollTrigger: { trigger: '#hwStage', start: 'top bottom', end: 'bottom top', scrub: 0.6 } });
      if (info) gsap.fromTo(info, { y: 50 }, { y: -20, ease: 'none', scrollTrigger: { trigger: '#hwStage', start: 'top bottom', end: 'bottom top', scrub: 0.9 } });
      if (stats.length) scrubRise(stats, { any: true, trigger: $('.hw-stats-strip', sec), y: 34, step: 14, scale: 0.96, start: 'top 94%', end: 'top 58%', scrub: 0.75 });
    });

    /* 10. Watercolour Heritage Map Frame (.itin) scroll-scrubbed directly on background (unclipped) */
    $$('.itin').forEach(sec => {
      const mapCard = $('.map', sec), pills = $$('.itin-ms', sec);
      if (mapCard) gsap.fromTo(mapCard,
        { y: 65, scale: 0.93, opacity: 0.35 },
        { y: -18, scale: 1.0, opacity: 1, ease: 'power2.out',
          scrollTrigger: { trigger: sec, start: 'top 95%', end: 'bottom top', scrub: 0.85 } }
      );
      if (pills.length) scrubRise(pills, { any: true, trigger: $('.itin-milestones', sec), y: 24, step: 10, scale: 0.96, start: 'top 94%', end: 'top 60%', scrub: 0.7 });
    });

    /* 11. Masonry Gallery Image Cards (.masonry figure): 3-speed column depth + inner window parallax */
    $$('.masonry figure').forEach((fig, i) => {
      const im = $('img', fig), colSpeed = (i % 3);
      gsap.fromTo(fig,
        { y: 55 + colSpeed * 32, scale: 0.93, opacity: 0.25 },
        { y: -(15 + colSpeed * 18), scale: 1, opacity: 1, ease: 'none',
          scrollTrigger: { trigger: fig, start: 'top bottom', end: 'bottom top', scrub: 0.8 } }
      );
      if (im) gsap.fromTo(im,
        { scale: 1.2, yPercent: -10 },
        { scale: 1.04, yPercent: 10, ease: 'none',
          scrollTrigger: { trigger: fig, start: 'top bottom', end: 'bottom top', scrub: 0.6 } }
      );
    });

    /* 12. Package cards, Contact cards, Accordions, Venue tables, Forms, Prose & Map */
    scrubRise($$('.sd-pillar'), { any: true, y: 32, step: 14, scale: 0.95, start: 'top 94%', end: 'top 58%', scrub: 0.75 });
    scrubRise($$('.dcs-dot'), { any: true, y: 20, step: 8, scale: 0.95, start: 'top 95%', end: 'top 65%', scrub: 0.7 });
    scrubRise($$('.pk > article'), { any: true, mod: 2, y: 60, step: 28, scale: 0.94, start: 'top 94%', end: 'top 45%', scrub: 0.8 });
    scrubRise($$('.contact-cols > div'), { any: true, mod: 3, y: 50, step: 22, scale: 0.95, start: 'top 94%', end: 'top 48%', scrub: 0.8 });
    scrubRise($$('.acc-i'), { y: 24, step: 8, scale: 0.99, start: 'top 95%', end: 'top 65%', scrub: 0.65 });
    scrubRise($$('.venues thead tr, .venues tbody tr'), { y: 22, step: 8, scale: 0.99, start: 'top 95%', end: 'top 65%', scrub: 0.65 });
    scrubRise($$('.form .checks, .form label'), { y: 22, step: 6, scale: 0.99, start: 'top 96%', end: 'top 68%', scrub: 0.65 });
    scrubRise($$('.prose > *'), { y: 24, step: 6, scale: 0.99, start: 'top 95%', end: 'top 68%', scrub: 0.65 });
    $$('.map-frame').forEach(f => gsap.fromTo(f, { clipPath: 'inset(8% 6% 8% 6% round 1.25rem)', opacity: .45 }, { clipPath: 'inset(0% 0% 0% 0% round 0rem)', opacity: 1, ease: 'none', scrollTrigger: { trigger: f, start: 'top 92%', end: 'top 32%', scrub: 0.85 } }));

    /* 13. Quote section: handwritten signature writes in with scroll */
    $$('.quote .sig').forEach(s => gsap.fromTo(s, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', ease: 'none', scrollTrigger: { trigger: s, start: 'top 92%', end: 'top 48%', scrub: 0.8 } }));

    /* 14. Footer choreography: scrubbed entrance */
    $$('.footer').forEach(f => {
      const tl = gsap.timeline({ scrollTrigger: { trigger: f, start: 'top 92%', end: 'top 38%', scrub: 0.8 } });
      const crest = $('.f-crest', f), word = $('.f-word', f);
      if (crest) tl.from(crest, { opacity: 0, scale: .72, rotate: -8, duration: 1 });
      if (word) tl.from(word, { opacity: 0, x: -28, duration: 0.9 }, '-=.7');
      tl.from($$('.f-badges > *', f), { opacity: 0, y: 20, duration: 0.8, stagger: .1 }, '-=.6')
        .from($$('.f-grid > div', f), { opacity: 0, y: 36, duration: 1, stagger: .14 }, '-=.5');
    });

    /* 15. Subtle magnetic pull on buttons (desktop pointer) */
    if (matchMedia('(hover: hover)').matches) {
      $$('main .btn, footer .btn').forEach(b => {
        const xTo = gsap.quickTo(b, 'x', { duration: .5, ease: 'power3.out' }), yTo = gsap.quickTo(b, 'y', { duration: .5, ease: 'power3.out' });
        b.addEventListener('mousemove', e => { const r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .18); yTo((e.clientY - r.top - r.height / 2) * .28); });
        b.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
      });
    }
  })();

  /* ---------- ROYAL ARCHITECTURAL SKETCH SHAPE-UP WITH SCROLL ---------- */
  $$('.sk-wrap').forEach(skWrap => {
    const strokes = $$('.sk-p', skWrap);
    const sun = $('.sk-p-sun', skWrap);
    const full = $('.sk-p-full', skWrap);
    const q = s => $$(s, skWrap);

    strokes.forEach(p => {
      try {
        const len = p.getTotalLength();
        gsap.set(p, { strokeDasharray: len + 4, strokeDashoffset: len + 4 });
      } catch (_) {}
    });

    if (sun) gsap.set(sun, { scale: 0, transformOrigin: '475px 120px' });
    if (full) gsap.set(full, { opacity: 0 });
    gsap.set(skWrap, { opacity: 0.35, y: 30, scale: 0.96 });

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: skWrap,
        start: 'top 92%',
        end: 'bottom 55%',
        scrub: 1.2,
        invalidateOnRefresh: true
      }
    });

    tl.to(q('.sk-p1, .sk-p2'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.35 }, 0);
    tl.to(skWrap, { opacity: 1, y: 0, scale: 1, ease: 'power2.out', duration: 0.8 }, 0);
    tl.to(q('.sk-p3, .sk-p4'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.4 }, 0.15);
    tl.to(q('.sk-p5, .sk-p6, .sk-p7'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.45 }, 0.2);
    tl.to(q('.sk-p8, .sk-p9, .sk-p10'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.45 }, 0.35);
    tl.to(q('.sk-p11, .sk-p12'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.4 }, 0.4);
    tl.to(q('.sk-p13, .sk-p14'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.35 }, 0.55);
    tl.to(q('.sk-p15, .sk-p16'), { strokeDashoffset: 0, ease: 'power1.inOut', duration: 0.35 }, 0.6);
    if (sun) tl.to(sun, { scale: 1, ease: 'back.out(1.4)', duration: 0.35 }, 0.7);
    if (full) tl.to(full, { opacity: 1, ease: 'power1.out', duration: 0.25 }, 0.85);
  });

  /* Clear any legacy font preset overrides to enforce Libre Caslon Display */
  try { localStorage.removeItem('vj-font-preset'); } catch (_) {}
  document.documentElement.removeAttribute('data-font-preset');

  /* ==========================================================================
     WEDDINGS AT THE PALACE — AUTO-NAVIGATING VENUE SHOWCASE
     ========================================================================== */
  (() => {
    const stage = $('#hwStage');
    const mainImg = $('#hwMainImg');
    const title = $('#hwCardTitle');
    const desc = $('#hwCardDesc');
    const badgeTag = $('#hwBadgeTag');
    const badgeSetting = $('#hwBadgeSetting');
    const hl1 = $('#hwHl1');
    const hl2 = $('#hwHl2');
    const hl3 = $('#hwHl3');
    const counter = $('#hwCounter');
    const tabs = $$('.hw-tab');
    const prevBtn = $('#hwPrevBtn');
    const nextBtn = $('#hwNextBtn');

    if (!stage || !mainImg || !tabs.length) return;

    const venuesData = Array.from(tabs).map(t => ({
      img: t.dataset.img,
      title: t.dataset.title,
      tag: t.dataset.tag,
      setting: t.dataset.setting,
      desc: t.dataset.desc,
      hl1: t.dataset.hl1,
      hl2: t.dataset.hl2,
      hl3: t.dataset.hl3,
      num: t.dataset.num
    }));

    let current = 0;
    const total = venuesData.length;
    let timer = null;
    let isHovered = false;
    const DURATION = 5000; // 5 seconds per venue

    const showVenue = (index, manual = false) => {
      current = (index + total) % total;
      const v = venuesData[current];

      tabs.forEach((tab, i) => {
        const isActive = i === current;
        tab.classList.toggle('is-active', isActive);
        tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      if (hasGsap) {
        gsap.to(mainImg, {
          opacity: 0,
          scale: 0.98,
          duration: 0.25,
          ease: 'power2.in',
          onComplete: () => {
            mainImg.src = v.img;
            mainImg.alt = v.title;
            if (title) title.textContent = v.title;
            if (desc) desc.textContent = v.desc;
            if (badgeTag) badgeTag.textContent = v.tag;
            if (badgeSetting) badgeSetting.textContent = v.setting;
            if (hl1) hl1.textContent = v.hl1;
            if (hl2) hl2.textContent = v.hl2;
            if (hl3) hl3.textContent = v.hl3;
            if (counter) counter.textContent = `${v.num} / 0${total}`;

            gsap.to(mainImg, { opacity: 1, scale: 1, duration: 0.45, ease: 'power2.out' });
          }
        });
      } else {
        mainImg.src = v.img;
        mainImg.alt = v.title;
        if (title) title.textContent = v.title;
        if (desc) desc.textContent = v.desc;
        if (badgeTag) badgeTag.textContent = v.tag;
        if (badgeSetting) badgeSetting.textContent = v.setting;
        if (hl1) hl1.textContent = v.hl1;
        if (hl2) hl2.textContent = v.hl2;
        if (hl3) hl3.textContent = v.hl3;
        if (counter) counter.textContent = `${v.num} / 0${total}`;
      }

      resetTimer();
    };

    const nextVenue = () => showVenue(current + 1);
    const prevVenue = () => showVenue(current - 1);

    const startTimer = () => {
      clearTimeout(timer);
      const activeTab = tabs[current];
      const activeBar = activeTab ? $('.hw-progress-bar', activeTab) : null;
      if (activeBar && hasGsap) {
        gsap.killTweensOf(activeBar);
        gsap.fromTo(activeBar, { width: '0%' }, { width: '100%', duration: DURATION / 1000, ease: 'none' });
      }
      timer = setTimeout(() => {
        if (!isHovered) {
          nextVenue();
        }
      }, DURATION);
    };

    const resetTimer = () => {
      $$('.hw-progress-bar').forEach(b => {
        if (hasGsap) gsap.killTweensOf(b);
        b.style.width = '0%';
      });
      startTimer();
    };

    tabs.forEach((tab, idx) => {
      tab.addEventListener('click', () => showVenue(idx, true));
    });

    if (prevBtn) prevBtn.addEventListener('click', () => prevVenue());
    if (nextBtn) nextBtn.addEventListener('click', () => nextVenue());

    // Pause auto-navigation on hover
    stage.addEventListener('mouseenter', () => {
      isHovered = true;
      clearTimeout(timer);
      const activeBar = $('.is-active .hw-progress-bar');
      if (activeBar && hasGsap) gsap.getTweensOf(activeBar).forEach(t => t.pause());
    });

    stage.addEventListener('mouseleave', () => {
      isHovered = false;
      const activeBar = $('.is-active .hw-progress-bar');
      if (activeBar && hasGsap) gsap.getTweensOf(activeBar).forEach(t => t.resume());
      startTimer();
    });

    // Start auto-navigation when section enters viewport
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.create({
        trigger: '#weddings',
        start: 'top 80%',
        once: true,
        onEnter: () => startTimer()
      });
    } else {
      startTimer();
    }
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

  /* ==========================================================================
     ROYAL EXPEDITION & 3D HORSE MOTION CONTROLLER
     ========================================================================== */
  (() => {
    const mapSvg = $('#royalExpeditionMap');
    if (!mapSvg) return;

    const path = $('#royalHighwayPath');
    const travelTrail = $('#royalTravelTrail');
    const horseRig = $('#royalHorseRig');
    const stage = $('#map3DStage');
    const mapCard = $('#map3DCard');
    const playBtn = $('#expPlayBtn');
    const resetBtn = $('#expResetBtn');
    const playLabel = $('#expPlayLabel');
    const statusText = $('#expStatusText');
    const stopCards = $$('.exp-stop-card');
    const floatingCard = $('#expFloatingCard');
    const efcBadge = $('#efcBadge');
    const efcTitle = $('#efcTitle');
    const efcDesc = $('#efcDesc');
    const efcTip = $('#efcTip');
    const particleContainer = $('#horseDustParticles');

    if (!path || !horseRig) return;

    const totalLength = path.getTotalLength();
    if (travelTrail) {
      travelTrail.style.strokeDasharray = totalLength;
      travelTrail.style.strokeDashoffset = totalLength;
    }

    // 5 Stops configuration matching exact spline geometry
    const stops = [
      {
        idx: 0,
        dist: 0,
        name: "Jaipur Airport",
        distLabel: "30 KM FROM PALACE · ~45 MIN DRIVE",
        role: "Gateway of Rajasthan",
        desc: "Where your princely journey begins. Chauffeur-driven luxury palace transfers glide northwards along the scenic highway directly into the peaceful Aravalli valley.",
        tip: "Private airport transfers can be pre-arranged with the palace concierge.",
        pos: { x: 392, y: 915 }
      },
      {
        idx: 1,
        dist: totalLength * 0.11,
        name: "Hawa Mahal & Pink City",
        distLabel: "19 KM FROM PALACE · ~35 MIN DRIVE",
        role: "Palace of Winds & Bazaars",
        desc: "Maharaja Sawai Pratap Singh's 1799 architectural masterpiece with 953 honeycombed jharokhas, adjacent to the City Palace, Jantar Mantar, and bustling Johari gem bazaar.",
        tip: "Visit in the morning when the rising sun illuminates the pink sandstone facade.",
        pos: { x: 475, y: 780 }
      },
      {
        idx: 2,
        dist: totalLength * 0.335,
        name: "Jal Mahal",
        distLabel: "15 KM FROM PALACE · ~25 MIN DRIVE",
        role: "Sunlit Water Palace",
        desc: "An ethereal pale yellow sandstone palace resting gracefully amidst the turquoise waters of Man Sagar Lake, framed by ancient rolling Aravalli peaks.",
        tip: "A breathtaking photography viewpoint along Amer Road, especially at twilight.",
        pos: { x: 245, y: 530 }
      },
      {
        idx: 3,
        dist: totalLength * 0.605,
        name: "Amber Fort",
        distLabel: "12 KM FROM PALACE · ~18 MIN DRIVE",
        role: "Citadel of the Kachhwahas",
        desc: "The colossal 16th-century mountain stronghold renowned for the glittering Sheesh Mahal (Mirror Palace), majestic elephant ramparts, and Maota Lake reflections.",
        tip: "Enjoy the evening sound-and-light show before returning for high tea at the palace.",
        pos: { x: 315, y: 375 }
      },
      {
        idx: 4,
        dist: totalLength,
        name: "The Vijayran Palace",
        distLabel: "DESTINATION · KUKAS IN THE ARAVALLIS",
        role: "Your Palatial Sanctuary",
        desc: "Nestled in secluded tranquility among the ancient Aravalli hills. Thirty-five royal haveli suites and private pool villas, lush Mughal gardens, and timeless Rajasthani royalty.",
        tip: "The ultimate haven for stillness, royal dining, and bespoke heritage stays.",
        pos: { x: 775, y: 275 }
      }
    ];

    let currentDist = 0;
    let targetDist = null; // null = continuous auto-ride mode
    let isPlaying = true;
    let isDwelling = false;
    let dwellTimer = null;
    let currentStopIdx = 0;
    let lastFrameTime = performance.now();
    let lastParticleTime = 0;
    const autoSpeed = 75; // pixels per second for graceful majestic canter

    const spawnParticle = (x, y) => {
      if (!particleContainer || reduce) return;
      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', x + (Math.random() * 6 - 3));
      c.setAttribute('cy', y + 16 + (Math.random() * 4));
      c.setAttribute('r', '2.2');
      c.setAttribute('fill', '#d7b46a');
      c.setAttribute('opacity', '0.75');
      particleContainer.appendChild(c);

      if (hasGsap) {
        gsap.to(c, {
          attr: { r: 5, cy: y + 20 + Math.random() * 6 },
          opacity: 0,
          duration: 0.7,
          ease: 'power1.out',
          onComplete: () => { if (c.parentNode) c.parentNode.removeChild(c); }
        });
      } else {
        setTimeout(() => { if (c.parentNode) c.parentNode.removeChild(c); }, 700);
      }
    };

    const updateFloatingCard = (stop) => {
      if (!floatingCard) return;
      if (efcBadge) efcBadge.textContent = stop.distLabel;
      if (efcTitle) efcTitle.textContent = stop.name;
      if (efcDesc) efcDesc.textContent = stop.desc;
      if (efcTip) efcTip.innerHTML = `<b>Royal Tip:</b> ${stop.tip}`;

      // Update active stop card UI
      stopCards.forEach((c, idx) => {
        const isActive = idx === stop.idx;
        c.classList.toggle('is-active', isActive);
        c.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      // Update beacon active state
      $$('.map-stop-beacon').forEach((b, idx) => {
        b.classList.toggle('is-active', idx === stop.idx);
      });

      // Update status text
      if (statusText) {
        if (stop.idx === 4) {
          statusText.textContent = `Arrived at The Vijayran Palace · Kukas`;
        } else {
          statusText.textContent = `At ${stop.name} (${stop.distLabel.split('·')[0].trim()})`;
        }
      }
    };

    const renderHorseAtDist = (dist, isMoving) => {
      const clampedDist = Math.max(0, Math.min(totalLength, dist));
      const p = path.getPointAtLength(clampedDist);
      const lookAhead = Math.min(totalLength, clampedDist + 3);
      const pNext = path.getPointAtLength(lookAhead);
      const dx = pNext.x - p.x;
      const dy = pNext.y - p.y;

      let angle = Math.atan2(dy, dx) * 180 / Math.PI;
      let flip = Math.cos(angle * Math.PI / 180) < 0;

      // 3D elevation scaling as the horse journeys into the Aravalli hills (heroic royal scale)
      const elevationScale = 1.35 + (clampedDist / totalLength) * 0.35;

      if (flip) {
        horseRig.setAttribute('transform', `translate(${p.x}, ${p.y}) rotate(${angle + 180}) scale(${-elevationScale}, ${elevationScale})`);
      } else {
        horseRig.setAttribute('transform', `translate(${p.x}, ${p.y}) rotate(${angle}) scale(${elevationScale}, ${elevationScale})`);
      }

      // Update travel trail
      if (travelTrail) {
        travelTrail.style.strokeDashoffset = totalLength - clampedDist;
      }

      // Spawn hooves dust
      const now = performance.now();
      if (isMoving && now - lastParticleTime > 90) {
        lastParticleTime = now;
        spawnParticle(p.x, p.y);
      }
    };

    const arriveAtStop = (stopIdx) => {
      currentStopIdx = stopIdx;
      isDwelling = true;
      updateFloatingCard(stops[stopIdx]);

      // Pause for dwelling to let guest admire the stop
      clearTimeout(dwellTimer);
      const dwellMs = (stopIdx === 4) ? 4000 : 2200;
      dwellTimer = setTimeout(() => {
        isDwelling = false;
        if (stopIdx === 4) {
          // Reached destination! Restart loop smoothly from airport
          currentDist = 0;
          currentStopIdx = 0;
          updateFloatingCard(stops[0]);
        }
      }, dwellMs);
    };

    const goToStop = (idx) => {
      clearTimeout(dwellTimer);
      isDwelling = false;
      targetDist = stops[idx].dist;
      updateFloatingCard(stops[idx]);
      if (statusText) {
        statusText.textContent = `Riding towards ${stops[idx].name}...`;
      }
    };

    // Main 60fps Animation Loop
    const tick = (now) => {
      const dt = Math.min(0.1, (now - lastFrameTime) / 1000);
      lastFrameTime = now;

      let isMoving = false;

      if (isPlaying && !isDwelling) {
        if (targetDist !== null) {
          // Navigating to a specific stop
          const diff = targetDist - currentDist;
          const step = Math.sign(diff) * autoSpeed * 1.8 * dt;
          if (Math.abs(diff) <= Math.abs(step) || Math.abs(diff) < 2) {
            currentDist = targetDist;
            targetDist = null;
            arriveAtStop(currentStopIdx);
          } else {
            currentDist += step;
            isMoving = true;
          }
        } else {
          // Continuous Auto-Ride Progress
          currentDist += autoSpeed * dt;
          isMoving = true;

          // Check if passed next milestone stop
          const nextStop = stops[currentStopIdx + 1];
          if (nextStop && currentDist >= nextStop.dist) {
            currentDist = nextStop.dist;
            arriveAtStop(nextStop.idx);
          }
        }
      }

      renderHorseAtDist(currentDist, isMoving);
      requestAnimationFrame(tick);
    };

    // Initialize position at Stop 0
    renderHorseAtDist(0, false);
    updateFloatingCard(stops[0]);
    requestAnimationFrame(tick);

    // Event Listeners for Stop Cards
    stopCards.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        currentStopIdx = idx;
        goToStop(idx);
      });
    });

    // Event Listeners for Map Beacons
    $$('.map-stop-beacon').forEach((b, idx) => {
      b.addEventListener('click', () => {
        currentStopIdx = idx;
        goToStop(idx);
      });
    });

    // Play / Pause Toggle
    if (playBtn) {
      const playIcon = $('.exp-icon-play', playBtn);
      const pauseIcon = $('.exp-icon-pause', playBtn);

      const updatePlayState = (playing) => {
        isPlaying = playing;
        playBtn.classList.toggle('is-playing', playing);
        if (playIcon) playIcon.style.display = playing ? 'none' : 'inline-block';
        if (pauseIcon) pauseIcon.style.display = playing ? 'inline-block' : 'none';
        if (playLabel) playLabel.textContent = playing ? 'Pause Journey' : 'Resume Journey';
      };

      playBtn.addEventListener('click', () => {
        updatePlayState(!isPlaying);
      });
    }

    // Reset Route Button
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        clearTimeout(dwellTimer);
        isDwelling = false;
        targetDist = null;
        currentDist = 0;
        currentStopIdx = 0;
        updateFloatingCard(stops[0]);
        if (statusText) statusText.textContent = `Restarted from Jaipur Airport (30 km)`;
      });
    }

    // 3D Parallax Tilt for Map Card on Mouse/Touch Movement
    if (stage && mapCard && !reduce) {
      let rect = null;
      stage.addEventListener('mouseenter', () => { rect = stage.getBoundingClientRect(); });
      stage.addEventListener('mousemove', (e) => {
        if (!rect) rect = stage.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        mapCard.style.transform = `rotateX(${(6 - y * 12).toFixed(2)}deg) rotateY(${(-0.5 + x * 14).toFixed(2)}deg) translateZ(8px)`;
      });
      stage.addEventListener('mouseleave', () => {
        rect = null;
        mapCard.style.transform = `rotateX(6deg) rotateY(-0.5deg) translateZ(0px)`;
      });
    }

    // Auto-start journey when section enters viewport
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.create({
        trigger: '#territory-map',
        start: 'top 75%',
        once: true,
        onEnter: () => {
          isPlaying = true;
        }
      });
    }
  })();

  /* ==========================================================================
     STORY CHRONICLE — PINNED ALTERNATING HORIZONTAL SCROLLYTELLING
     ========================================================================== */
  $$('.story-chronicle').forEach(sec => {
    const pinWrap = $('.sc-pin', sec);
    const chapters = $$('.sc-chapter', sec);
    const stepBtns = $$('.sc-step', sec);
    const progFill = $('.sc-progress-fill', sec);
    if (!pinWrap || chapters.length < 2 || typeof ScrollTrigger === 'undefined' || reduce) return;

    ScrollTrigger.matchMedia({
      '(min-width: 992px)': () => {
        sec.classList.add('is-pinned');
        const N = chapters.length;

        const setActiveStep = idx => {
          chapters.forEach((ch, i) => ch.classList.toggle('is-active', i === idx));
          stepBtns.forEach((b, i) => b.classList.toggle('is-active', i === idx));
        };

        chapters.forEach((ch, i) => {
          const tx = $('.sc-text', ch), md = $('.sc-media', ch), im = $('.sc-img', ch);
          if (i === 0) {
            gsap.set(ch, { autoAlpha: 1 });
            gsap.set([tx, md], { x: 0, y: 0, autoAlpha: 1, clipPath: 'inset(0% 0% 0% 0%)' });
            if (im) gsap.set(im, { scale: 1.08 });
          } else {
            gsap.set(ch, { autoAlpha: 0 });
          }
        });
        setActiveStep(0);

        const tl = gsap.timeline({
          scrollTrigger: {
            trigger: sec,
            pin: pinWrap,
            start: 'top top',
            end: () => `+=${Math.round(innerHeight * (N * 0.92))}`,
            scrub: 0.75,
            anticipatePin: 1,
            invalidateOnRefresh: true,
            onUpdate: self => {
              const p = self.progress;
              if (progFill) gsap.set(progFill, { scaleX: Math.max(0.08, p) });
              const idx = Math.min(N - 1, Math.floor(p * N));
              setActiveStep(idx);
            }
          }
        });

        for (let i = 0; i < N; i++) {
          const ch = chapters[i];
          const tx = $('.sc-text', ch), md = $('.sc-media', ch), im = $('.sc-img', ch);
          const isRev = ch.classList.contains('is-reverse');
          const segStart = i;

          if (i === 0) {
            if (im) tl.fromTo(im, { scale: 1.09 }, { scale: 1.0, duration: 0.75, ease: 'none' }, 0);
          } else {
            const clipFrom = isRev ? 'inset(0% 100% 0% 0%)' : 'inset(0% 0% 0% 100%)';
            const xFrom = isRev ? -56 : 56;
            const txFromX = isRev ? 40 : -40;
            tl.set(ch, { autoAlpha: 1 }, segStart - 0.18)
              .fromTo(md,
                { x: xFrom, autoAlpha: 0, clipPath: clipFrom },
                { x: 0, autoAlpha: 1, clipPath: 'inset(0% 0% 0% 0%)', duration: 0.48, ease: 'power2.out' },
                segStart - 0.16
              )
              .fromTo(tx,
                { x: txFromX, y: 42, autoAlpha: 0 },
                { x: 0, y: 0, autoAlpha: 1, duration: 0.48, ease: 'power2.out' },
                segStart - 0.12
              );
            if (im) {
              tl.fromTo(im, { scale: 1.16 }, { scale: 1.0, duration: 0.85, ease: 'power1.out' }, segStart - 0.16);
            }
          }

          if (i < N - 1) {
            const exitAt = segStart + 0.68;
            const xTo = isRev ? -44 : 44;
            tl.to(tx, { y: -38, autoAlpha: 0, duration: 0.34, ease: 'power2.in' }, exitAt)
              .to(md, { x: xTo, scale: 0.96, autoAlpha: 0, duration: 0.36, ease: 'power2.in' }, exitAt)
              .set(ch, { autoAlpha: 0 }, exitAt + 0.37);
          } else {
            /* Hold final chapter gracefully before releasing pin */
            tl.to(ch, { autoAlpha: 1, duration: 0.55 }, segStart + 0.35);
          }
        }

        stepBtns.forEach((btn, idx) => {
          btn.addEventListener('click', () => {
            const st = tl.scrollTrigger;
            if (!st) return;
            const targetP = N > 1 ? (idx + 0.18) / N : 0;
            const y = st.start + targetP * (st.end - st.start);
            if (lenis) lenis.scrollTo(y, { duration: 1.1 });
            else window.scrollTo({ top: y, behavior: 'smooth' });
          });
        });

        return () => {
          sec.classList.remove('is-pinned');
          gsap.set(chapters, { clearProps: 'all' });
        };
      },

      '(max-width: 991px)': () => {
        sec.classList.remove('is-pinned');
        chapters.forEach(ch => {
          const md = $('.sc-media', ch), tx = $('.sc-text', ch), im = $('.sc-img', ch);
          if (md) gsap.fromTo(md, { y: 45, opacity: 0.2 }, { y: 0, opacity: 1, ease: 'power2.out', scrollTrigger: { trigger: ch, start: 'top 92%', end: 'top 48%', scrub: 0.75 } });
          if (im) gsap.fromTo(im, { scale: 1.15, yPercent: -8 }, { scale: 1.02, yPercent: 8, ease: 'none', scrollTrigger: { trigger: ch, start: 'top bottom', end: 'bottom top', scrub: 0.6 } });
          if (tx) gsap.fromTo(tx, { y: 35, opacity: 0.2 }, { y: 0, opacity: 1, ease: 'power2.out', scrollTrigger: { trigger: ch, start: 'top 88%', end: 'top 45%', scrub: 0.75 } });
        });
      }
    });
  });

  /* ==========================================================================
     GUEST SALON — CENTERED UPRIGHT CASLON SHOWCASE
     ========================================================================== */
  $$('.guest-salon').forEach(salon => {
    const slides = $$('.gs-slide', salon);
    const tabs = $$('.gs-tab', salon);
    const prev = $('[data-gs-prev]', salon);
    const next = $('[data-gs-next]', salon);
    if (slides.length < 2) return;

    let cur = 0, timer = null, paused = false;
    const DUR = 5800;

    const armTimer = () => {
      clearTimeout(timer);
      tabs.forEach(t => {
        const b = $('.gs-tab-bar', t);
        if (b) { if (hasGsap) gsap.killTweensOf(b); b.style.width = '0%'; }
      });
      const activeBar = tabs[cur] ? $('.gs-tab-bar', tabs[cur]) : null;
      if (activeBar && hasGsap && !paused) {
        gsap.fromTo(activeBar, { width: '0%' }, { width: '100%', duration: DUR / 1000, ease: 'none' });
      }
      if (!paused) {
        timer = setTimeout(() => show(cur + 1), DUR);
      }
    };

    const show = idx => {
      cur = (idx + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle('is-active', i === cur));
      tabs.forEach((t, i) => {
        const on = i === cur;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      armTimer();
    };

    tabs.forEach((t, i) => t.addEventListener('click', () => show(i)));
    prev?.addEventListener('click', () => show(cur - 1));
    next?.addEventListener('click', () => show(cur + 1));
    salon.addEventListener('mouseenter', () => {
      paused = true;
      clearTimeout(timer);
      const b = tabs[cur] ? $('.gs-tab-bar', tabs[cur]) : null;
      if (b && hasGsap) gsap.killTweensOf(b);
    });
    salon.addEventListener('mouseleave', () => {
      paused = false;
      armTimer();
    });

    if (hasGsap && !reduce) {
      gsap.fromTo($('.gs-stage', salon),
        { y: 45, opacity: 0.25 },
        { y: 0, opacity: 1, ease: 'power2.out',
          scrollTrigger: { trigger: salon, start: 'top 90%', end: 'top 45%', scrub: 0.8 } }
      );
    }
    armTimer();
  });

  /* ==========================================================================
     MAHARAJA'S HAND-PAINTED HERITAGE SCROLL — UNROLLING PARCHMENT & BRUSHWORK
     ========================================================================== */
  (() => {
    const scrollEl = $('#maharaja-scroll');
    if (!scrollEl) return;

    $$('[data-ms-words]', scrollEl).forEach(p => {
      const words = p.textContent.trim().split(/\s+/);
      p.innerHTML = words.map(w => `<span class="ms-w">${w}</span>`).join(' ');
    });

    if (!hasGsap || typeof ScrollTrigger === 'undefined' || reduce) {
      $$('.ms-w', scrollEl).forEach(w => { w.style.opacity = '1'; });
      return;
    }

    /* 1. Gentle Suryavanshi sun medallion rotation with scroll */
    const surya = $('.ms-surya-svg', scrollEl);
    if (surya) {
      gsap.to(surya, {
        rotation: 28,
        ease: 'none',
        scrollTrigger: { trigger: scrollEl, start: 'top top', end: 'bottom bottom', scrub: 1 }
      });
    }

    /* 2. Hand-painted Jaipur miniature frescoes — unrolling parchment reveal */
    $$('[data-ms-fresco]', scrollEl).forEach((fig, idx) => {
      const im = $('.ms-fresco-img', fig);
      if (!im) return;
      if (idx === 0) {
        gsap.fromTo(im,
          { opacity: 0.15, y: 26, scale: 0.97 },
          { opacity: 1, y: 0, scale: 1, duration: 1.4, ease: 'power2.out' }
        );
      } else {
        gsap.fromTo(im,
          { clipPath: 'inset(0% 0% 18% 0%)', opacity: 0.2, y: 34, scale: 0.96 },
          { clipPath: 'inset(0% 0% 0% 0%)', opacity: 1, y: 0, scale: 1, ease: 'power2.out',
            scrollTrigger: { trigger: fig, start: 'top 92%', end: 'top 46%', scrub: 0.75 } }
        );
      }
    });

    /* 3. Kos Minar fort distance milestones — mineral ink bloom along the route */
    const kosItems = $$('[data-ms-kos]', scrollEl);
    if (kosItems.length) {
      kosItems.forEach((item, i) => {
        gsap.fromTo(item,
          { opacity: 0.15, y: 22 + (i % 3) * 10 },
          { opacity: 1, y: 0, ease: 'power2.out',
            scrollTrigger: { trigger: item, start: 'top 94%', end: 'top 64%', scrub: 0.65 } }
        );
      });
    }

    /* 4. Winding vermilion-and-gold caravan trails & word-by-word scroll illumination */
    $$('.ms-trail', scrollEl).forEach(tr => {
      const path = $('.ms-trail-draw', tr);
      const words = $$('.ms-w', tr);
      if (path) {
        try {
          const L = path.getTotalLength();
          gsap.set(path, { strokeDasharray: L, strokeDashoffset: L });
          gsap.to(path, {
            strokeDashoffset: 0,
            ease: 'none',
            scrollTrigger: { trigger: tr, start: 'top 86%', end: 'bottom 38%', scrub: 0.55 }
          });
        } catch (_) {}
      }
      if (words.length) {
        gsap.fromTo(words,
          { opacity: 0.22 },
          { opacity: 1, stagger: 0.04, ease: 'none',
            scrollTrigger: { trigger: tr, start: 'top 82%', end: 'bottom 44%', scrub: 0.5 } }
        );
      }
    });

    /* 5. Chapter prose & Mehrab peep-windows gentle scroll rise */
    $$('.ms-story-prose', scrollEl).forEach(pr => {
      gsap.fromTo(pr,
        { opacity: 0.22, y: 32 },
        { opacity: 1, y: 0, ease: 'power2.out',
          scrollTrigger: { trigger: pr, start: 'top 92%', end: 'top 52%', scrub: 0.75 } }
      );
    });
    $$('[data-ms-peep]', scrollEl).forEach(peep => {
      const pImg = $('img', peep);
      gsap.fromTo(peep,
        { opacity: 0.2, y: 40, scale: 0.95 },
        { opacity: 1, y: 0, scale: 1, ease: 'power2.out',
          scrollTrigger: { trigger: peep, start: 'top 92%', end: 'top 50%', scrub: 0.8 } }
      );
      if (pImg && pImg.classList.contains('ms-peep-img')) {
        gsap.fromTo(pImg,
          { scale: 1.14, yPercent: -7 },
          { scale: 1.02, yPercent: 7, ease: 'none',
            scrollTrigger: { trigger: peep, start: 'top bottom', end: 'bottom top', scrub: 0.65 } }
        );
      }
    });
  })();

  addEventListener('load', () => ScrollTrigger.refresh());
})();

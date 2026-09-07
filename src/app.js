/* Progressive enhancement only. Every essential link and all content work without JS. */
(() => {
  'use strict';
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('#site-nav');
  if (toggle && nav) {
    const mobile = window.matchMedia('(max-width: 620px)');
    const setOpen = (open, returnFocus = false) => {
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (returnFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a') && mobile.matches) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && document.body.classList.contains('nav-open')) setOpen(false, true);
    });
    document.addEventListener('click', (event) => {
      if (mobile.matches && !event.target.closest('.site-header')) setOpen(false);
    });
    mobile.addEventListener('change', () => setOpen(false));
    toggle.hidden = false;
    document.body.classList.add('has-js');
  }

  const bar = document.querySelector('.filter-bar');
  const status = document.querySelector('#filter-status');
  const items = [...document.querySelectorAll('[data-category]')];
  if (bar && status && items.length) {
    bar.hidden = false;
    bar.addEventListener('click', (event) => {
      const selected = event.target.closest('button[data-filter]');
      if (!selected) return;
      const category = selected.dataset.filter;
      let count = 0;
      items.forEach((item) => {
        item.hidden = category !== 'all' && item.dataset.category !== category;
        if (!item.hidden) count += 1;
      });
      bar.querySelectorAll('button').forEach((button) => button.setAttribute('aria-pressed', String(button === selected)));
      const more = document.querySelector('.more-flavours');
      if (more) more.hidden = !more.querySelector('.flavour-item:not([hidden])');
      status.textContent = `${count} food and drink ${count === 1 ? 'highlight' : 'highlights'} shown. ${selected.textContent}.`;
    });
  }

  // Broken media never receives an unrelated replacement photograph.
  document.querySelectorAll('img[data-business-photo]').forEach((img) => {
    const showFallback = () => {
      const picture = img.closest('picture');
      if (!picture || picture.dataset.failed) return;
      picture.dataset.failed = 'true';
      const fallback = document.createElement('div');
      fallback.className = 'image-fallback';
      const title = document.createElement('span');
      title.textContent = 'A little of Eme’s.';
      const note = document.createElement('small');
      note.textContent = 'This photo is unavailable. Explore the café’s own posts on Instagram.';
      fallback.append(title, note);
      picture.replaceChildren(fallback);
    };
    img.addEventListener('error', showFallback, { once: true });
    if (img.complete && img.naturalWidth === 0) showFallback();
  });
})();

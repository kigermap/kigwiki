(() => {
  const initDirectory = () => {
    const root = document.querySelector('[data-maker-directory]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const form = root.querySelector('form');
    const rows = Array.from(root.querySelectorAll('.maker-row'));
    const count = root.querySelector('[data-maker-count]');
    const empty = root.querySelector('[data-maker-empty]');
    const more = root.querySelector('[data-maker-more]');
    const progress = root.querySelector('[data-maker-progress]');
    let limit = 24;
    const names = ['q', 'region', 'status', 'category', 'platform'];
    const active = new Set(['sales', 'inquiry', 'lottery']);
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
    const restore = () => {
      const params = new URLSearchParams(location.search);
      form.reset();
      names.forEach(name => {
        const key = `maker_${name}`;
        if (!params.has(key)) return;
        const field = form.elements.namedItem(name);
        const value = params.get(key);
        if (field.tagName !== 'SELECT' || Array.from(field.options).some(option => option.value === value)) field.value = value;
      });
    };
    const filter = (save = true, resetLimit = true) => {
      if (resetLimit) limit = 24;
      const values = Object.fromEntries(new FormData(form));
      const terms = normalize(values.q).split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        const data = row.dataset;
        const matches = terms.every(term => normalize(data.search).includes(term))
          && (!values.region || data.region === values.region)
          && (values.status === 'all' || (values.status === 'active' ? active.has(data.status) : data.status === values.status))
          && (!values.category || data.category.split('|').includes(values.category))
          && (!values.platform || data.platform.split('|').includes(values.platform));
        if (matches) visible++;
        row.hidden = !matches || visible > limit;
      });
      count.textContent = `${visible} 家符合条件 / 共 ${rows.length} 份档案`;
      empty.hidden = visible !== 0;
      more.hidden = visible <= limit;
      progress.textContent = visible ? `已展示 ${Math.min(limit, visible)} / ${visible} 家店铺` : '';
      more.textContent = `查看更多店铺（还有 ${Math.max(0, visible - limit)} 家） ↓`;
      if (save) {
        const url = new URL(location.href);
        names.forEach(name => {
          const value = values[name];
          const key = `maker_${name}`;
          if (value && !(name === 'status' && value === 'all')) url.searchParams.set(key, value);
          else url.searchParams.delete(key);
        });
        history.replaceState(null, '', url);
      }
    };
    more.addEventListener('click', () => { limit += 24; filter(false, false); });
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => filter());
    form.addEventListener('change', () => filter());
    form.addEventListener('reset', () => setTimeout(() => filter(), 0));
    root.querySelector('[data-maker-clear]').addEventListener('click', () => {
      form.reset();
      form.elements.q.focus();
    });
    window.addEventListener('popstate', () => { restore(); filter(false); });
    restore();
    filter(false);
  };
  const revealHash = (hash = location.hash) => {
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = id && document.getElementById(id);
    if (!target) return;
    let parent = target.closest('details');
    while (parent) {
      parent.open = true;
      parent = parent.parentElement?.closest('details');
    }
  };
  const init = () => {
    initDirectory();
    document.querySelectorAll('[data-maker-gallery]').forEach(root => {
      if (root.dataset.initialized) return;
      root.dataset.initialized = 'true';
      const thumbs = Array.from(root.querySelectorAll('[data-gallery-thumb]'));
      const select = button => {
        const image = root.querySelector('[data-gallery-image]');
        image.src = button.dataset.src;
        image.alt = button.dataset.caption;
        root.querySelector('[data-gallery-open]').href = button.dataset.src;
        root.querySelector('[data-gallery-caption]').textContent = button.dataset.caption;
        root.querySelector('[data-gallery-credit]').href = button.dataset.credit;
        thumbs.forEach(thumb => thumb.setAttribute('aria-pressed', String(thumb === button)));
      };
      thumbs.forEach((button, index) => {
        button.addEventListener('click', () => select(button));
        button.addEventListener('keydown', event => {
          if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
          event.preventDefault();
          const next = thumbs[(index + (event.key === 'ArrowRight' ? 1 : -1) + thumbs.length) % thumbs.length];
          select(next);
          next.focus();
        });
      });
    });
    revealHash();
  };
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link) revealHash(link.getAttribute('href'));
  });
  window.addEventListener('hashchange', () => revealHash());
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
  if (typeof document$ !== 'undefined') document$.subscribe(init);
})();

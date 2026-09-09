(() => {
  const init = () => {
    const root = document.querySelector('[data-maker-directory]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const form = root.querySelector('form');
    const rows = Array.from(root.querySelectorAll('.maker-row'));
    const count = root.querySelector('[data-maker-count]');
    const empty = root.querySelector('[data-maker-empty]');
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
    const filter = (save = true) => {
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
        row.hidden = !matches;
        if (matches) visible++;
      });
      count.textContent = `${visible} 家符合条件 / 共 ${rows.length} 份档案`;
      empty.hidden = visible !== 0;
      if (save) {
        const url = new URL(location.href);
        names.forEach(name => {
          const value = values[name];
          const key = `maker_${name}`;
          if (value && !(name === 'status' && value === 'active')) url.searchParams.set(key, value);
          else url.searchParams.delete(key);
        });
        history.replaceState(null, '', url);
      }
    };
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
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
  if (typeof document$ !== 'undefined') document$.subscribe(init);
})();

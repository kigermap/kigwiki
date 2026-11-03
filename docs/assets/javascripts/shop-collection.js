(() => {
  const init = () => {
    const root = document.querySelector('[data-shop-collection]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const form = root.querySelector('form');
    const rows = Array.from(root.querySelectorAll('[data-collection-row]'));
    const more = root.querySelector('[data-collection-more]');
    const progress = root.querySelector('[data-collection-progress]');
    let limit = 24;
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
    const filter = (resetLimit = true) => {
      if (resetLimit) limit = 24;
      const terms = normalize(form.elements.q.value).split(/\s+/).filter(Boolean);
      const category = form.elements.category.value;
      let count = 0;
      for (const row of rows) {
        const matches = (!category || row.dataset.category === category) && terms.every(term => normalize(row.dataset.search).includes(term));
        if (matches) count++;
        row.hidden = !matches || count > limit;
      }
      root.querySelector('[data-collection-count]').textContent = `${count} 条符合条件 / 共 ${rows.length} 条记录`;
      root.querySelector('[data-collection-empty]').hidden = count !== 0;
      more.hidden = count <= limit;
      more.textContent = `查看更多店铺（还有 ${Math.max(0, count - limit)} 条） ↓`;
      progress.textContent = count ? `已展示 ${Math.min(limit, count)} / ${count} 条记录` : '';
    };
    more.addEventListener('click', () => { limit += 24; filter(false); });
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', filter);
    form.addEventListener('change', filter);
    form.addEventListener('reset', () => setTimeout(filter, 0));
    filter();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
  if (typeof document$ !== 'undefined') document$.subscribe(init);
})();

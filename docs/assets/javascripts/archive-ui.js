(() => {
  const ready = (callback) => {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
      return;
    }
    callback();
  };

  const normalize = (value) => value.toLowerCase().replace(/\s+/g, " ").trim();
  const MESSAGES = {
    "zh-Hans": {
      showingMatches: (visible) => `显示 ${visible} 条匹配记录`,
      showingAll: (total) => `显示全部 ${total} 条记录`,
      noResults: "没有找到符合条件的结果",
      noResultsTitle: "未找到匹配记录",
      noResultsHint: "可以试试大事记、来源索引或地点索引。",
      events: "大事记",
      sources: "来源索引",
      places: "地点索引",
      resultsFound: (count) => `找到 ${count} 个符合条件的结果`,
      untitled: "未命名页面",
      typeToSearch: "键入以开始搜索",
      indexUnavailable: "搜索索引暂时不可用",
    },
    "zh-Hant": {
      showingMatches: (visible) => `顯示 ${visible} 筆符合記錄`,
      showingAll: (total) => `顯示全部 ${total} 筆記錄`,
      noResults: "沒有找到符合條件的結果",
      noResultsTitle: "未找到符合記錄",
      noResultsHint: "可以試試全量大事記、來源索引或地點索引。",
      events: "全量大事記",
      sources: "來源索引",
      places: "地點索引",
      resultsFound: (count) => `找到 ${count} 個符合條件的結果`,
      untitled: "未命名頁面",
      typeToSearch: "輸入以開始搜尋",
      indexUnavailable: "搜尋索引暫時不可用",
    },
    en: {
      showingMatches: (visible) => `Showing ${visible} matching records`,
      showingAll: (total) => `Showing all ${total} records`,
      noResults: "No matching results found",
      noResultsTitle: "No matching records",
      noResultsHint: "Try the event index, sources index, or places index.",
      events: "Event Index",
      sources: "Sources Index",
      places: "Places Index",
      resultsFound: (count) => `Found ${count} matching results`,
      untitled: "Untitled page",
      typeToSearch: "Type to start searching",
      indexUnavailable: "Search index is temporarily unavailable",
    },
    ja: {
      showingMatches: (visible) => `${visible} 件の一致する記録を表示`,
      showingAll: (total) => `全 ${total} 件の記録を表示`,
      noResults: "一致する結果が見つかりません",
      noResultsTitle: "一致する記録はありません",
      noResultsHint: "事件索引、出典索引、場所索引も試してください。",
      events: "事件索引",
      sources: "出典索引",
      places: "場所索引",
      resultsFound: (count) => `${count} 件の一致する結果が見つかりました`,
      untitled: "無題のページ",
      typeToSearch: "入力して検索を開始",
      indexUnavailable: "検索索引は一時的に利用できません",
    },
    ru: {
      showingMatches: (visible) => `Показано совпадающих записей: ${visible}`,
      showingAll: (total) => `Показаны все записи: ${total}`,
      noResults: "Подходящие результаты не найдены",
      noResultsTitle: "Совпадений нет",
      noResultsHint: "Попробуйте индекс событий, источников или мест.",
      events: "Индекс событий",
      sources: "Индекс источников",
      places: "Индекс мест",
      resultsFound: (count) => `Найдено результатов: ${count}`,
      untitled: "Страница без названия",
      typeToSearch: "Начните вводить запрос",
      indexUnavailable: "Поисковый индекс временно недоступен",
    },
  };

  const getMessages = () => {
    const lang = document.documentElement.lang || "zh-Hans";
    return MESSAGES[lang] || MESSAGES[lang.split("-")[0]] || MESSAGES["zh-Hans"];
  };

  let searchIndexPromise;

  const enhanceTables = () => {
    document.querySelectorAll(".md-typeset table:not([data-archive-enhanced])").forEach((table) => {
      table.dataset.archiveEnhanced = "true";
      table.classList.add("archive-data-table");

      const headers = Array.from(table.querySelectorAll("thead th")).map((cell) =>
        cell.textContent.trim()
      );

      table.querySelectorAll("tbody tr").forEach((row) => {
        row.dataset.archiveFilterText = normalize(row.textContent);
        Array.from(row.children).forEach((cell, index) => {
          if (headers[index]) {
            cell.dataset.label = headers[index];
          }
        });
      });
    });
  };

  const setupIndexFilters = () => {
    document.querySelectorAll("[data-archive-filter]").forEach((panel) => {
      if (panel.dataset.archiveFilterReady) return;
      panel.dataset.archiveFilterReady = "true";

      const article = panel.closest(".md-content__inner") || document;
      const input = panel.querySelector("[data-archive-filter-input]");
      const reset = panel.querySelector("[data-archive-filter-reset]");
      const chips = Array.from(panel.querySelectorAll("[data-archive-filter-chip]"));
      const rows = Array.from(article.querySelectorAll("table tbody tr"));
      const status = document.createElement("p");

      status.className = "archive-filter-status";
      status.setAttribute("aria-live", "polite");
      panel.append(status);

      const setActiveChip = (activeChip) => {
        [reset, ...chips].forEach((chip) => {
          chip?.classList.remove("archive-chip--active");
          chip?.setAttribute("aria-pressed", "false");
        });
        activeChip?.classList.add("archive-chip--active");
        activeChip?.setAttribute("aria-pressed", "true");
      };

      const applyFilter = (value, activeChip = null) => {
        const query = normalize(value);
        let visible = 0;

        rows.forEach((row) => {
          const match = !query || row.dataset.archiveFilterText.includes(query);
          row.hidden = !match;
          if (match) visible += 1;
        });

        const messages = getMessages();
        status.textContent = query ? messages.showingMatches(visible) : messages.showingAll(rows.length);
        if (input && input.value !== value) input.value = value;
        if (activeChip) setActiveChip(activeChip);
      };

      input?.addEventListener("input", () => applyFilter(input.value));
      reset?.addEventListener("click", () => applyFilter("", reset));
      chips.forEach((chip) => {
        chip.addEventListener("click", () => applyFilter(chip.dataset.archiveFilterChip || "", chip));
      });

      applyFilter("", reset);
    });
  };

  const escapeHtml = (value) =>
    value.replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[char]);

  const getSiteBase = () => {
    const config = document.querySelector("#__config");
    if (!config?.textContent) return new URL(".", location.href);
    try {
      const value = JSON.parse(config.textContent);
      return new URL(`${value.base || "."}/`, location.href);
    } catch {
      return new URL(".", location.href);
    }
  };

  const loadSearchIndex = () => {
    if (searchIndexPromise) return searchIndexPromise;

    searchIndexPromise = new Promise((resolve, reject) => {
      const request = new XMLHttpRequest();
      request.open("GET", new URL("search/search_index.json", getSiteBase()).href, true);
      request.responseType = "json";
      request.addEventListener("load", () => {
        if (request.status >= 200 && request.status < 300) {
          resolve(request.response || JSON.parse(request.responseText));
          return;
        }
        reject(new Error(`Search index returned ${request.status}`));
      });
      request.addEventListener("error", () => reject(new Error("Search index request failed")));
      request.send();
    });

    return searchIndexPromise;
  };

  const highlight = (value, terms) => {
    let output = escapeHtml(value);
    terms
      .filter(Boolean)
      .sort((a, b) => b.length - a.length)
      .forEach((term) => {
        const escapedTerm = escapeHtml(term).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        output = output.replace(new RegExp(escapedTerm, "gi"), (match) => `<mark>${match}</mark>`);
      });
    return output;
  };

  const snippet = (text, terms) => {
    const normalizedText = normalize(text);
    const first = terms.map((term) => normalizedText.indexOf(term)).find((index) => index >= 0) ?? 0;
    const start = Math.max(0, first - 48);
    const body = text.replace(/\s+/g, " ").trim();
    return `${start > 0 ? "... " : ""}${body.slice(start, start + 132)}${body.length > start + 132 ? " ..." : ""}`;
  };

  const renderFallbackSearch = async (query, resultList, meta) => {
    const terms = normalize(query).split(" ").filter(Boolean);
    if (!terms.length) return;

    const index = await loadSearchIndex();
    const base = getSiteBase();
    const results = (index.docs || [])
      .map((doc) => {
        const title = doc.title || "";
        const locationValue = doc.location || "";
        const text = doc.text || "";
        const haystack = normalize(`${title} ${locationValue} ${text}`);
        if (!terms.every((term) => haystack.includes(term))) return null;
        const score =
          terms.reduce((total, term) => total + (normalize(title).includes(term) ? 8 : 0), 0) +
          terms.reduce((total, term) => total + (normalize(locationValue).includes(term) ? 4 : 0), 0) +
          terms.reduce((total, term) => total + (normalize(text).includes(term) ? 1 : 0), 0);
        return { doc, score };
      })
      .filter(Boolean)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8);

    resultList.classList.add("archive-search-fallback-list");
    resultList.innerHTML = "";

    if (!results.length) {
      const messages = getMessages();
      meta.textContent = messages.noResults;
      resultList.innerHTML = `
        <li class="md-search-result__item archive-search-fallback-empty">
          <div class="md-search-result__link">
            <article class="md-search-result__article md-typeset">
              <h1 class="md-search-result__title">${escapeHtml(messages.noResultsTitle)}</h1>
              <p class="md-search-result__teaser">${escapeHtml(messages.noResultsHint)}</p>
              <p class="archive-search-fallback-links">
                <a href="${new URL("generated/events/", location.href).href}">${escapeHtml(messages.events)}</a>
                <a href="${new URL("generated/sources-index/", location.href).href}">${escapeHtml(messages.sources)}</a>
                <a href="${new URL("generated/places-index/", location.href).href}">${escapeHtml(messages.places)}</a>
              </p>
            </article>
          </div>
        </li>`;
      return;
    }

    const messages = getMessages();
    meta.textContent = messages.resultsFound(results.length);
    resultList.innerHTML = results
      .map(({ doc }) => {
        const href = new URL(doc.location || ".", base).href;
        return `
          <li class="md-search-result__item archive-search-fallback-item">
            <a href="${href}" class="md-search-result__link">
              <article class="md-search-result__article md-typeset">
                <h1 class="md-search-result__title">${highlight(doc.title || messages.untitled, terms)}</h1>
                <p class="md-search-result__teaser">${highlight(snippet(doc.text || "", terms), terms)}</p>
              </article>
            </a>
          </li>`;
      })
      .join("");
  };

  const setupSearchFallback = () => {
    const input = document.querySelector(".md-search__input");
    const resultList = document.querySelector(".md-search-result__list");
    const meta = document.querySelector(".md-search-result__meta");
    if (!input || !resultList || !meta || input.dataset.archiveSearchFallbackReady) return;

    input.dataset.archiveSearchFallbackReady = "true";
    let timer;

    input.addEventListener("input", () => {
      clearTimeout(timer);
      const query = input.value;
      if (!normalize(query)) {
        if (resultList.classList.contains("archive-search-fallback-list")) {
          resultList.classList.remove("archive-search-fallback-list");
          resultList.innerHTML = "";
          meta.textContent = getMessages().typeToSearch;
        }
        return;
      }

      timer = setTimeout(() => {
        const hasNativeResults =
          resultList.querySelector(".md-search-result__item:not(.archive-search-fallback-item):not(.archive-search-fallback-empty)");
        if (hasNativeResults) return;
        renderFallbackSearch(query, resultList, meta).catch(() => {
          meta.textContent = getMessages().indexUnavailable;
        });
      }, 700);
    });
  };

  const setupNavigationState = () => {
    const primaryLinks = Array.from(document.querySelectorAll(".md-sidebar--primary .md-nav__link"));
    const secondaryLinks = Array.from(document.querySelectorAll(".md-sidebar--secondary .md-nav__link"));
    const headings = secondaryLinks
      .map((link) => {
        const hash = new URL(link.href, location.href).hash;
        if (!hash) return null;
        const target = document.getElementById(decodeURIComponent(hash.slice(1)));
        return target ? { hash, link, target } : null;
      })
      .filter(Boolean);

    const samePath = (href) => new URL(href, location.href).pathname === location.pathname;
    const visible = (element) => {
      const rect = element.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    };

    const updatePrimary = () => {
      primaryLinks.forEach((link) => {
        const active = visible(link) && link.href && samePath(link.href);
        link.classList.toggle("archive-nav-link--current", active);
        if (active) {
          link.setAttribute("aria-current", "page");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };

    const updateSecondary = () => {
      let active = null;
      if (location.hash) {
        active = headings.find((item) => item.hash === location.hash);
      }

      if (!active) {
        const offset = 120;
        active = headings[0] || null;
        headings.forEach((item) => {
          if (item.target.getBoundingClientRect().top <= offset) {
            active = item;
          }
        });
      }

      secondaryLinks.forEach((link) => {
        const selected = active?.link === link;
        link.classList.toggle("archive-toc-link--current", selected);
        if (selected) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };

    const update = () => {
      updatePrimary();
      updateSecondary();
    };

    update();
    window.removeEventListener("hashchange", window.__archiveNavHashUpdate);
    window.removeEventListener("scroll", window.__archiveNavScrollUpdate);
    window.__archiveNavHashUpdate = update;
    window.__archiveNavScrollUpdate = () => window.requestAnimationFrame(updateSecondary);
    window.addEventListener("hashchange", window.__archiveNavHashUpdate);
    window.addEventListener("scroll", window.__archiveNavScrollUpdate, { passive: true });
  };

  ready(() => {
    enhanceTables();
    setupIndexFilters();
    setupSearchFallback();
    setupNavigationState();
  });

  if (window.document$?.subscribe) {
    window.document$.subscribe(() => {
      enhanceTables();
      setupIndexFilters();
      setupSearchFallback();
      setupNavigationState();
    });
  }
})();

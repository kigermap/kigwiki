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
      noResultsHint: "可以试试首页、参与加入或编年总览。",
      home: "首页",
      join: "参与加入",
      chronicle: "编年总览",
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
      noResultsHint: "可以試試首頁、參與加入或編年總覽。",
      home: "首頁",
      join: "參與加入",
      chronicle: "編年總覽",
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
      noResultsHint: "Try Home, Join, or Chronicle.",
      home: "Home",
      join: "Join",
      chronicle: "Chronicle",
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
      noResultsHint: "ホーム、参加案内、編年総覧も試してください。",
      home: "ホーム",
      join: "参加案内",
      chronicle: "編年総覧",
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
      noResultsHint: "Попробуйте главную страницу, участие или хронику.",
      home: "Главная",
      join: "Участие",
      chronicle: "Хроника",
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

  const LOCALES = {
    "/zh-Hant/": {
      lang: "zh-Hant",
      siteName: "Kigurumi 編年志",
      navLabel: "導航",
      links: [
        ["首頁", "/zh-Hant/"],
        ["關於介紹", "/zh-Hant/about/"],
        ["參與加入", "/zh-Hant/join/"],
        ["貢獻與支持", "/zh-Hant/support/"],
        ["編年總覽", "/zh-Hant/chronicle/"],
        ["年份目錄", "/zh-Hant/years/"],
        ["地點目錄", "/zh-Hant/places/"],
        ["人物目錄", "/zh-Hant/people/"],
        ["來源目錄", "/zh-Hant/sources/"],
      ],
    },
    "/en/": {
      lang: "en",
      siteName: "Kigurumi Chronicle",
      navLabel: "Navigation",
      links: [
        ["Home", "/en/"],
        ["About", "/en/about/"],
        ["Join", "/en/join/"],
        ["Contribute", "/en/support/"],
        ["Chronicle", "/en/chronicle/"],
        ["Years", "/en/years/"],
        ["Places", "/en/places/"],
        ["People", "/en/people/"],
        ["Sources", "/en/sources/"],
      ],
    },
    "/ja/": {
      lang: "ja",
      siteName: "Kigurumi 編年誌",
      navLabel: "ナビゲーション",
      links: [
        ["ホーム", "/ja/"],
        ["紹介", "/ja/about/"],
        ["参加案内", "/ja/join/"],
        ["貢献と支援", "/ja/support/"],
        ["編年総覧", "/ja/chronicle/"],
        ["年別目録", "/ja/years/"],
        ["場所目録", "/ja/places/"],
        ["人物目録", "/ja/people/"],
        ["出典目録", "/ja/sources/"],
      ],
    },
    "/ru/": {
      lang: "ru",
      siteName: "Хроника Kigurumi",
      navLabel: "Навигация",
      links: [
        ["Главная", "/ru/"],
        ["О проекте", "/ru/about/"],
        ["Участие", "/ru/join/"],
        ["Поддержать", "/ru/support/"],
        ["Хроника", "/ru/chronicle/"],
        ["Годы", "/ru/years/"],
        ["Места", "/ru/places/"],
        ["Люди", "/ru/people/"],
        ["Источники", "/ru/sources/"],
      ],
    },
    "/": {
      lang: "zh-Hans",
      siteName: "Kigurumi 编年志",
      navLabel: "导航栏",
      links: [
        ["首页", "/"],
        ["关于介绍", "/about/"],
        ["参与加入", "/join/"],
        ["贡献与支持", "/support/"],
        ["编年总览", "/chronicle/"],
        ["年份目录", "/years/"],
        ["地点目录", "/places/"],
        ["人物目录", "/people/"],
        ["来源目录", "/sources/"],
      ],
    },
  };

  const getLocaleForPath = (path = location.pathname) => {
    return (
      ["/zh-Hant/", "/en/", "/ja/", "/ru/"].find((prefix) => path.startsWith(prefix)) || "/"
    );
  };

  const stripPermalink = (value) => value.replace(/\s*¶\s*$/, "").replace(/\s+/g, " ").trim();

  const getMobilePageTitle = () => {
    const locale = LOCALES[getLocaleForPath()] || LOCALES["/"];
    const headingTitle = stripPermalink(document.querySelector(".md-content h1")?.textContent || "");
    if (headingTitle && headingTitle !== locale.siteName) return headingTitle;

    const documentTitle = stripPermalink(document.title.split(" - ")[0] || "");
    if (documentTitle && documentTitle !== locale.siteName) return documentTitle;

    const currentPath = location.pathname.replace(/\/?$/, "/");
    const matchingNavLink = Array.from(document.querySelectorAll(".md-nav--primary .md-nav__link"))
      .find((link) => {
        try {
          return new URL(link.href, location.href).pathname.replace(/\/?$/, "/") === currentPath;
        } catch {
          return false;
        }
      });
    const navTitle = stripPermalink(matchingNavLink?.textContent || "");
    if (navTitle && navTitle !== locale.siteName) return navTitle;

    return locale.links[0][0];
  };

  const setupMobilePageTitle = () => {
    const headerTitle = document.querySelector(".md-header__title");
    const current = headerTitle?.querySelector(
      '.md-header__topic[data-md-component="header-topic"] .md-ellipsis'
    );
    if (!headerTitle || !current) return;

    current.textContent = document.querySelector(".archive-hero")
      ? LOCALES[getLocaleForPath()].siteName : getMobilePageTitle();
    headerTitle.classList.add("archive-mobile-page-title-ready");
  };

  const setupNotFoundLocale = () => {
    const isNotFound =
      document.body?.classList.contains("error") ||
      document.body?.classList.contains("archive-error-page") ||
      document.title.startsWith("404") ||
      document.querySelector(".md-content h1")?.textContent.trim().startsWith("404");
    if (!isNotFound) return;

    const localePath = getLocaleForPath();
    const locale = LOCALES[localePath] || LOCALES["/"];
    document.documentElement.lang = locale.lang;

    document.querySelectorAll('.md-header__topic:not([data-md-component="header-topic"]) .md-ellipsis').forEach((label) => {
      if (label.textContent.trim()) label.textContent = locale.siteName;
    });

    document.querySelectorAll("[data-md-component='logo']").forEach((logo) => {
      logo.setAttribute("href", locale.links[0][1]);
      logo.setAttribute("title", locale.siteName);
      logo.setAttribute("aria-label", locale.siteName);
    });

    document.querySelectorAll(".md-nav--primary").forEach((nav) => {
      nav.setAttribute("aria-label", locale.navLabel);
      const title = nav.querySelector(".md-nav__title");
      if (title) {
        Array.from(title.childNodes)
          .filter((node) => node.nodeType === Node.TEXT_NODE)
          .forEach((node) => {
            node.textContent = ` ${locale.siteName}`;
          });
      }

      const list = nav.querySelector(":scope > .md-nav__list");
      if (!list) return;
      list.innerHTML = locale.links
        .map(
          ([label, href]) => `
            <li class="md-nav__item">
              <a href="${href}" class="md-nav__link">
                <span class="md-ellipsis">${label}</span>
              </a>
            </li>`
        )
        .join("");
    });
  };

  let searchIndexPromise;

  const enhanceTables = () => {
    document.querySelectorAll(".md-typeset table:not([data-archive-enhanced])").forEach((table) => {
      table.dataset.archiveEnhanced = "true";
      table.classList.add("archive-data-table");

      if (!table.closest(".md-typeset__scrollwrap, .archive-table-scroll")) {
        const wrapper = document.createElement("div");
        wrapper.className = "archive-table-scroll";
        table.before(wrapper);
        wrapper.append(table);
      }
      const scrollRegion = table.closest(".md-typeset__scrollwrap, .archive-table-scroll");
      scrollRegion.tabIndex = 0;
      scrollRegion.setAttribute("role", "region");
      scrollRegion.setAttribute("aria-label", table.querySelector("th")?.textContent || getMobilePageTitle());

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
    const body = new DOMParser().parseFromString(text, "text/html").body.textContent.replace(/\s+/g, " ").trim();
    const normalizedText = normalize(body);
    const first = terms.map((term) => normalizedText.indexOf(term)).find((index) => index >= 0) ?? 0;
    const start = Math.max(0, first - 48);
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
        if (getLocaleForPath(new URL(locationValue || ".", base).pathname) !== getLocaleForPath()) return null;
        const text = doc.text || "";
        const haystack = normalize(`${title} ${locationValue} ${text}`);
        if (!terms.every((term) => haystack.includes(term))) return null;
        const score =
          (locationValue.includes("#") ? 0 : 6) +
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
                <a href="${new URL(".", getSiteBase()).href}">${escapeHtml(messages.home)}</a>
                <a href="${new URL("join/", getSiteBase()).href}">${escapeHtml(messages.join)}</a>
                <a href="${new URL("chronicle/", getSiteBase()).href}">${escapeHtml(messages.chronicle)}</a>
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

  const THEME_MESSAGES = {
    "zh-Hans": { search: "搜索年份或关键词", all: "全部", oldest: "年份从早到晚", newest: "年份从晚到早", sort: "年份排序", toc: "本页目录" },
    "zh-Hant": { search: "搜尋年份或關鍵詞", all: "全部", oldest: "年份由早到晚", newest: "年份由晚到早", sort: "年份排序", toc: "本頁目錄" },
    en: { search: "Search years or keywords", all: "All", oldest: "Oldest first", newest: "Newest first", sort: "Sort years", toc: "On this page" },
    ja: { search: "年・キーワードを検索", all: "すべて", oldest: "古い順", newest: "新しい順", sort: "年の並び順", toc: "このページの目次" },
    ru: { search: "Поиск по году или слову", all: "Все", oldest: "Сначала ранние", newest: "Сначала поздние", sort: "Порядок годов", toc: "На этой странице" },
  };

  const themeIcon = (name) => document.querySelector("#archive-theme-icons")?.content
    .querySelector(`[data-icon="${name}"]`)?.cloneNode(true) || document.createElement("span");

  const setupYearCatalogues = (messages) => {
    document.querySelectorAll(".archive-feature-grid:not([data-year-catalogue])").forEach((grid) => {
      const records = Array.from(grid.querySelectorAll(".archive-feature")).map((item) => {
        const link = item.querySelector("a");
        const year = link && new URL(link.href).pathname.match(/\/years\/(\d{4})\/$/)?.[1];
        return { item, year: Number(year), text: normalize(item.textContent) };
      });
      if (records.length < 10 || records.some((record) => !record.year)) return;
      grid.dataset.yearCatalogue = "true";
      grid.classList.add("archive-year-grid");
      records.forEach(({ item, year }) => {
        const badge = item.querySelector(".archive-feature__icon");
        if (badge) badge.textContent = year;
      });

      const panel = document.createElement("div");
      panel.className = "archive-year-tools";
      const row = document.createElement("div");
      row.className = "archive-year-tools__row";
      const label = document.createElement("label");
      label.className = "archive-year-search";
      const input = document.createElement("input");
      input.type = "search";
      input.placeholder = messages.search;
      input.setAttribute("aria-label", messages.search);
      label.append(themeIcon("magnify"), input);
      const sort = document.createElement("select");
      sort.setAttribute("aria-label", messages.sort);
      [["asc", messages.oldest], ["desc", messages.newest]].forEach(([value, text]) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = text;
        sort.append(option);
      });
      row.append(label, sort);
      const chips = document.createElement("div");
      chips.className = "archive-chip-list";
      const status = document.createElement("p");
      status.className = "archive-filter-status";
      status.setAttribute("aria-live", "polite");
      const empty = document.createElement("p");
      empty.className = "archive-empty";
      empty.textContent = getMessages().noResults;
      empty.hidden = true;
      let decade = null;

      const filter = () => {
        const query = normalize(input.value);
        let count = 0;
        records.forEach(({ item, year, text }) => {
          const visible = (!decade || Math.floor(year / 10) * 10 === decade) && text.includes(query);
          item.hidden = !visible;
          if (visible) count += 1;
        });
        status.textContent = getMessages().showingMatches(count);
        empty.hidden = count > 0;
        grid.hidden = count === 0;
      };
      const decades = [...new Set(records.map(({ year }) => Math.floor(year / 10) * 10))].sort();
      [null, ...decades].forEach((value) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = `archive-chip${value === null ? " archive-chip--active" : ""}`;
        chip.textContent = value === null ? messages.all : `${value}s`;
        chip.setAttribute("aria-pressed", String(value === null));
        chip.addEventListener("click", () => {
          decade = value;
          chips.querySelectorAll("button").forEach((button) => {
            button.classList.toggle("archive-chip--active", button === chip);
            button.setAttribute("aria-pressed", String(button === chip));
          });
          filter();
        });
        chips.append(chip);
      });
      input.addEventListener("input", filter);
      sort.addEventListener("change", () => {
        [...records].sort((a, b) => sort.value === "asc" ? a.year - b.year : b.year - a.year)
          .forEach(({ item }) => grid.append(item));
      });
      panel.append(row, chips, status);
      grid.before(panel);
      grid.after(empty);
      filter();

      if (/\/years\/$/.test(location.pathname)) {
        const intro = document.querySelector(".archive-page-intro");
        const section = grid.closest(".archive-section");
        if (intro && section) intro.after(section);
      }
    });
  };

  const setupTheme = () => {
    const article = document.querySelector(".md-content__inner");
    if (!article || article.dataset.themeReady) return;
    article.dataset.themeReady = "true";
    const locale = LOCALES[getLocaleForPath()] || LOCALES["/"];
    const messages = THEME_MESSAGES[locale.lang];
    const hero = article.querySelector(".archive-hero");
    if (hero) {
      const catalogue = article.querySelector(".archive-feature-grid")?.closest(".archive-section");
      if (catalogue) {
        catalogue.classList.add("archive-catalogue");
        hero.after(catalogue);
        catalogue.querySelectorAll(".archive-feature").forEach((feature, index) => {
          const number = document.createElement("span");
          number.className = "archive-number";
          number.textContent = String(index + 1).padStart(2, "0");
          number.setAttribute("aria-hidden", "true");
          feature.prepend(number);
          const link = feature.querySelector("a");
          const source = Array.from(document.querySelectorAll(".archive-nav-main a, .archive-nav-meta a"))
            .find((navLink) => navLink.href === link?.href)?.querySelector(".archive-nav-icon");
          if (source) feature.querySelector(".archive-feature__icon")?.replaceChildren(source.cloneNode(true));
        });
      }
      const chronicle = Array.from(hero.querySelectorAll(".md-button"))
        .find((link) => new URL(link.href).pathname.endsWith("/chronicle/"));
      if (chronicle) {
        hero.querySelectorAll(".md-button").forEach((link) => link.classList.toggle("md-button--primary", link === chronicle));
        chronicle.parentElement.prepend(chronicle);
      }
    }
    article.querySelectorAll(".archive-feature > a, .archive-actions > a").forEach((link) => link.append(themeIcon("arrow-right")));
    setupYearCatalogues(messages);

    const toc = document.querySelector(".md-nav--secondary .md-nav__list");
    if (!hero && toc?.children.length) {
      const mobileToc = document.createElement("details");
      mobileToc.className = "archive-mobile-toc";
      const summary = document.createElement("summary");
      summary.append(themeIcon("format-list-bulleted"), document.createTextNode(messages.toc));
      const list = toc.cloneNode(true);
      list.removeAttribute("data-md-component");
      list.querySelectorAll("[id]").forEach((element) => element.removeAttribute("id"));
      list.addEventListener("click", (event) => {
        if (event.target.closest("a")) mobileToc.open = false;
      });
      mobileToc.append(summary, list);
      (article.querySelector(".archive-page-intro") || article.querySelector("h1"))?.after(mobileToc);
    }
    if (!hero && !document.querySelector(".archive-reading-progress")) {
      const progress = document.createElement("div");
      progress.className = "archive-reading-progress";
      progress.setAttribute("aria-hidden", "true");
      document.body.append(progress);
      let scheduled = false;
      const update = () => {
        const available = article.scrollHeight - window.innerHeight;
        const offset = window.scrollY - (article.getBoundingClientRect().top + window.scrollY) + 64;
        progress.style.transform = `scaleX(${available > 0 ? Math.min(1, Math.max(0, offset / available)) : 0})`;
        scheduled = false;
      };
      window.addEventListener("scroll", () => {
        if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
      }, { passive: true });
      window.addEventListener("resize", update);
      update();
    }
  };

  const initialize = () => {
    setupNotFoundLocale();
    setupMobilePageTitle();
    setupTheme();
    enhanceTables();
    setupIndexFilters();
    setupSearchFallback();
    setupNavigationState();
  };

  ready(initialize);

  if (window.document$?.subscribe) {
    window.document$.subscribe(initialize);
  }
})();

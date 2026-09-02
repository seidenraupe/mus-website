(() => {
  const root = document.documentElement.dataset.root || "";
  const page = document.documentElement.dataset.page || "";

  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js", "pagestatus-loaded");

  window.wOpenURL = function wOpenURL(url) {
    if (!url) return;
    window.location.href = url;
  };

  window.wsmn = function wsmn(ml) {
    let mln = "";
    for (let i = 0; i < ml.length / 3; i += 1) {
      mln = ml.substr(i * 3 + 1, 1) + mln;
    }
    let pms = "";
    const q = mln.match(/(\?.*)/);
    if (q) {
      pms = q[1].replace(/wApos/g, "'");
      mln = mln.replace(/(\?.*)/, "");
    }
    mln =
      mln
        .replace(/a/g, "@")
        .replace(/e/g, ".")
        .replace(/\*/g, "a")
        .replace(/;/g, "e")
        .replace(/:/g, "o")
        .replace(/,/g, "u")
        .replace(/!/g, "i") + pms;
    window.location.href = `mailto:${mln}`;
  };

  const toggler = document.getElementById("navigationMainToggler");
  const closer = document.querySelector("#navigationMain .closemenu");
  function setNav(open) {
    document.documentElement.classList.toggle("navmenu-open", open);
    if (toggler) toggler.classList.toggle("open", open);
  }
  if (toggler) {
    toggler.addEventListener("click", () => {
      setNav(!document.documentElement.classList.contains("navmenu-open"));
    });
  }
  if (closer) closer.addEventListener("click", () => setNav(false));
  document.querySelectorAll("#navigationMain a").forEach((a) => {
    a.addEventListener("click", () => setNav(false));
  });

  document.querySelectorAll(".accordionHeader").forEach((header) => {
    header.addEventListener("click", () => {
      const content = header.nextElementSibling;
      const opening = content && content.classList.contains("accordionContentHidden");
      document.querySelectorAll(".accordionHeader").forEach((other) => {
        other.classList.add("accordionHeaderHidden");
        other.classList.remove("accordionHeaderVisible");
        const otherContent = other.nextElementSibling;
        if (otherContent && otherContent.classList.contains("accordionContent")) {
          otherContent.classList.add("accordionContentHidden");
          otherContent.classList.remove("accordionContentVisible");
        }
      });
      if (opening && content) {
        header.classList.add("accordionHeaderVisible");
        header.classList.remove("accordionHeaderHidden");
        content.classList.remove("accordionContentHidden");
        content.classList.add("accordionContentVisible");
      }
    });
  });
  if (location.hash) {
    const id = decodeURIComponent(location.hash.replace(/^#/, "")).split("?")[0];
    const target = id ? document.getElementById(id) : null;
    const header = target && target.classList.contains("accordionHeader")
      ? target
      : target?.closest(".accordionContent")?.previousElementSibling;
    if (header && header.classList.contains("accordionHeader")) header.click();
  }

  const notice = document.getElementById("cookieNotice");
  const closerBtn = document.getElementById("cookieNoticeCloser");
  if (notice && /hideCookieNotice=1/.test(document.cookie)) {
    notice.classList.add("is-hidden");
  }
  if (closerBtn) {
    closerBtn.addEventListener("click", () => {
      document.cookie = `hideCookieNotice=1;path=/;max-age=${60 * 60 * 24 * 30}`;
      if (notice) notice.classList.add("is-hidden");
    });
  }

  document.querySelectorAll("img[data-src]").forEach((img) => {
    img.src = img.getAttribute("data-src");
  });
  document.querySelectorAll("source[data-src]").forEach((source) => {
    source.setAttribute("srcset", source.getAttribute("data-src").trim());
  });

  function fmtDate(isoLike) {
    if (!isoLike) return "";
    const p = String(isoLike).replaceAll("-", "/").split("/");
    if (p.length < 3) return isoLike;
    return `${p[2]}.${p[1]}.${String(p[0]).slice(-2)}`;
  }

  function weekdayShort(isoLike) {
    const p = String(isoLike).replaceAll("-", "/").split("/");
    if (p.length < 3) return "";
    const d = new Date(`${p[0]}-${p[1]}-${p[2]}T12:00:00`);
    return ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"][d.getDay()] || "";
  }

  function eventHref(ev) {
    return `${root}programm/event.html?id=${encodeURIComponent(ev.reference)}`;
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function tagsFor(ev) {
    const map = {
      69: "Konzerte",
      70: "Fest",
      11: "Film",
      14: "Lesungen",
      71: "Theater",
      72: "Tanz",
      13: "Sonderausstellung",
      217: "Vernissage",
      213: "Kinderprogramm",
      280: "Führungen",
      281: "Gespräche",
      15: "Highlights",
    };
    const out = [];
    if (map[ev.category]) out.push(map[ev.category]);
    const t = (ev.title || "").toLowerCase();
    if (t.includes("quiz") || t.includes("pims")) out.push("Fest");
    if (t.includes("käfele") || t.includes("kafele") || t.includes("afterwork")) out.push("Gespräche");
    if (t.includes("führung") || t.includes("fuehrung")) out.push("Führungen");
    if (t.includes("konzert")) out.push("Konzerte");
    if (t.includes("workshop")) out.push("Workshops");
    return [...new Set(out)];
  }

  async function loadEvents() {
    try {
      const res = await fetch(`${root}data/mus_export.json`);
      if (!res.ok) return [];
      const data = await res.json();
      return Array.isArray(data) ? data : data.events || [];
    } catch (_) {
      return [];
    }
  }

  function upcoming(events) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return events
      .filter((ev) => {
        if (!ev.date) return false;
        const [y, m, d] = String(ev.date).split("/");
        return new Date(`${y}-${m}-${d}T23:59:59`) >= today;
      })
      .sort((a, b) => String(a.date).localeCompare(String(b.date)) || String(a.time_start || "").localeCompare(String(b.time_start || "")));
  }

  function eventRow(ev, { image, dateTwice } = {}) {
    const href = eventHref(ev);
    const date = fmtDate(ev.date);
    const title = `${escapeHtml(ev.title || "")}&#160;`;
    const thumb = image && ev.image
      ? `<div class="listEntryElement listEntryElement_var0 listEntryElementThumbnail listEntryElementThumbnail_var0 listEntryElementPosition_var0 listEntryElementPadding_var0 listEntryElementThumbnailSize_var6 listEntryElementThumbnailAspectRatio_var15"><picture><img src="${escapeHtml(ev.image)}" alt=""></picture></div>`
      : "";
    const extraDate = dateTwice
      ? `<div class="listEntryElement listEntryElement_var0 listEntryElementPosition_var0 listEntryElementFontSize_var2 hidden">${date}</div>`
      : "";
    const pos = dateTwice ? "listEntryElementPosition_var6" : "listEntryElementPosition_var1";
    return `<li class="listEntry clickable listEntryObject-event listEntryObject-event_var" onclick="wOpenURL(this.getAttribute('data-url'));return false;" data-url="${href}"><div class="listEntryInner"><div class="listEntryElement listEntryElement_var0 listEntryElementContainer_var22 listEntryElementPadding_var6"><time datetime="" class="listEntryElement listEntryElement_var0 listEntryElementFontSize_var2">${date}</time> <div class="listEntryElement listEntryElement_var0 ${pos} listEntryElementFontSize_var2 lineticker">${title}</div> ${extraDate}</div>${thumb}</div></li>`;
  }

  function startTicker(el) {
    if (!el || el.dataset.tickerReady) return;
    el.dataset.tickerReady = "1";
    const text = el.innerHTML;
    el.innerHTML = `<div class="ticker-items">${text}</div><div class="ticker-items">${text}</div>`;
  }

  function startLineTickers(scope) {
    (scope || document).querySelectorAll(".lineticker").forEach((el) => {
      if (el.dataset.tickerReady) return;
      if (el.scrollWidth <= el.offsetWidth + 1) return;
      el.dataset.tickerReady = "1";
      const hidden = el.nextElementSibling;
      if (hidden && hidden.classList.contains("hidden")) hidden.remove();
      const text = el.innerHTML;
      el.innerHTML = `<div class="ticker-items">${text}</div><div class="ticker-items">${text}</div>`;
    });
  }

  function renderTicker(events) {
    const host = document.getElementById("mus-ticker");
    if (!host) return;
    const next = upcoming(events)[0];
    if (!next) {
      host.closest("#blockBodyBefore")?.remove();
      return;
    }
    const wd = weekdayShort(next.date);
    const d = fmtDate(next.date);
    const shortDate = `${wd} ${d.replace(/^0/, "").replace(/\.(\d{2})\.(\d{2})$/, ".$1")}`;
    const piece = `${shortDate} ${next.title} +++ `;
    host.innerHTML = `<li class="listEntry clickable listEntryObject-event" onclick="wOpenURL(this.getAttribute('data-url'));return false;" data-url="${eventHref(next)}"><div class="listEntryInner"><div class="listEntryElement listEntryElement_var0 listEntryElementPadding_var6 listEntryElementFontSize_var5 ticker">${escapeHtml(piece)}</div></div></li>`;
    startTicker(host.querySelector(".ticker"));
  }

  function renderHome(events) {
    const featured = document.getElementById("mus-home-featured");
    const rest = document.getElementById("mus-home-rest");
    if (!featured || !rest) return;
    const list = upcoming(events);
    featured.innerHTML = list[0] ? eventRow(list[0], { image: true, dateTwice: true }) : "";
    rest.innerHTML = list.slice(1, 7).map((ev) => eventRow(ev, { image: false })).join("");
    startLineTickers(document.getElementById("Veranstaltungen"));
  }

  function monthName(isoLike) {
    const p = String(isoLike).replaceAll("-", "/").split("/");
    if (p.length < 2) return "";
    return ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"][Number(p[1]) - 1] || "";
  }

  function agendaRow(ev, { showMonth }) {
    const href = eventHref(ev);
    const date = fmtDate(ev.date);
    const month = monthName(ev.date);
    const time = [ev.time_start, ev.time_end].filter(Boolean).join("–");
    const tags = tagsFor(ev).map((t) => `<span>${escapeHtml(t)}</span>`).join(" ");
    const hideMonth = showMonth ? "" : " removeMonth";
    return `<li class="listEntry clickable listEntryObject-event listEntryObject-event_var${hideMonth}" onclick="wOpenURL(this.getAttribute('data-url'));return false;" data-url="${href}" data-month="${escapeHtml(month)}"><div class="listEntryInner"><div class="listEntryElement listEntryElement_var0 listEntryElementContainer_var3 listEntryElementPadding_var6"><div class="listEntryElement listEntryElement_var0 listEntryElementContainer_var2 listEntryElementPosition_var50"><div class="listEntryElement listEntryElement_var0 listEntryDate"><time datetime="" class="listEntryElement listEntryElement_var0 listEntryElementFontSize_var3">${date}</time></div><div class="listEntryElement listEntryElement_var0 listEntryElementPosition_var1 listEntryElementFontSize_var2 lineticker"><a href="${href}">${escapeHtml(ev.title || "")}&#160;</a></div></div><div class="listEntryElement listEntryElement_var0 listEntryElementPosition_var25 listEntryElementPadding_var11 listEntryElementFontSize_var2 listEntryTime">${escapeHtml(time)}</div><div class="listEntryElement listEntryElement_var0 listEntryElementContainer_var2 listEntryElementPosition_var25 listEntryElementPadding_var11"><div class="listEntryElement listEntryElementFontSize_var2">${tags}</div><div class="listEntryElement listEntryElement_var0 listEntryElementPosition_var2 listEntryElementLink_var1"><a href="${href}">Zum Eintrag</a></div></div></div></div></li>`;
  }

  function renderProgramm(events) {
    const host = document.getElementById("mus-event-list");
    const agenda = document.getElementById("mus-event-agenda");
    const filters = document.getElementById("filterElement-categories");
    if (!host) return;
    const list = upcoming(events);
    let active = "";

    const paint = () => {
      const shown = list.filter((ev) => !active || tagsFor(ev).includes(active));
      host.innerHTML = shown.slice(0, 2).map((ev) => eventRow(ev, { image: true, dateTwice: true })).join("");
      startLineTickers(host);
      if (agenda) {
        let lastMonth = "";
        agenda.innerHTML = shown.map((ev) => {
          const month = monthName(ev.date);
          const showMonth = month !== lastMonth;
          lastMonth = month;
          return agendaRow(ev, { showMonth });
        }).join("");
      }
      if (filters) {
        filters.querySelectorAll("span").forEach((span) => {
          const value = (span.textContent || "").trim();
          const on = (active === "" && value === "Alle") || value === active;
          span.classList.toggle("selected", on);
          if (on) span.setAttribute("data-selected", "selected");
          else span.setAttribute("data-selected", "");
          const used = value === "Alle" || list.some((ev) => tagsFor(ev).includes(value));
          span.style.display = used ? "" : "none";
        });
      }
    };

    if (filters && !filters.dataset.bound) {
      filters.dataset.bound = "1";
      filters.querySelectorAll("span").forEach((span) => {
        span.addEventListener("click", () => {
          const value = (span.textContent || "").trim();
          active = value === "Alle" ? "" : value;
          paint();
        });
      });
    }
    paint();
  }

  function renderEventDetail(events) {
    const host = document.getElementById("mus-event-detail");
    if (!host) return;
    const id = new URLSearchParams(location.search).get("id");
    const ev = events.find((e) => String(e.reference) === String(id)) || upcoming(events)[0];
    if (!ev) {
      host.innerHTML = `<div class="elementText elementText_var1"><p>Keine Veranstaltung gefunden.</p></div>`;
      return;
    }
    document.title = `${ev.title} — Museum Schaffen`;
    const date = fmtDate(ev.date);
    const time = [ev.time_start, ev.time_end].filter(Boolean).join("–");
    const loc = [ev.location_name, ev.location_street, ev.location_zip, ev.location_city].filter(Boolean).join(", ");
    const htmlDesc = ev.description_html || `<p>${escapeHtml(ev.description_long || ev.description || "")}</p>`;
    const img = ev.image
      ? `<div class="elementPicture elementPicture_var0"><figure><img src="${escapeHtml(ev.image)}" alt="${escapeHtml(ev.title || "")}"></figure></div>`
      : "";
    const ticket = ev.presale && String(ev.presale).startsWith("http") && !String(ev.presale).includes("mail@")
      ? `<p><a href="${escapeHtml(ev.presale)}" target="_blank" rel="noopener">Tickets</a></p>`
      : "";
    host.innerHTML = `
      <div class="elementLink elementLinkBack"><a href="${root}programm/" class="back">zurück</a></div>
      <div class="elementSection elementSection_var2 elementSectionPadding_var0 elementSectionMargin_var0 elementSectionInnerWidth_var100">
        <div class="sectionInner">
          <div class="elementHeadline elementHeadline_var5 elementHeadlineLevel_vardiv3 elementHeadlineAlign_var0 elementHeadlineSize_var3">
            <div class="h3">${date}</div>
            <div class="h3 lineticker listEntryElementPosition_var6">${escapeHtml(ev.title || "")}</div>
            <div class="h3 hidden">${date}</div>
          </div>
        </div>
      </div>
      <div class="elementSection elementSection_var0 elementSectionPadding_var0 elementSectionMargin_var0 elementSectionInnerWidth_var100">
        <div class="sectionInner">
          <div class="elementHeadline elementHeadline_var0 elementHeadlineLevel_varh1 elementHeadlineAlign_var30 elementHeadlineSize_var0"><h1>${escapeHtml(ev.title || "")}</h1></div>
          <div class="elementText elementText_var0 elementTextListStyle_var0">${htmlDesc}</div>
          <div class="elementStandard elementContent elementContainerStandard elementContainerStandard_var0 elementContainerStandardColumns_var5050 elementContainerStandardColumns elementContainerStandardColumns2">
            <div class="col col1"><div><div class="elementText elementText_var1"><p>${date}${time ? `<br />${escapeHtml(time)} UHR` : ""}</p><p>${escapeHtml(loc)}</p></div></div></div>
            <div class="col col2"><div><div class="elementText elementText_var2">${ticket}${ev.url ? `<p><a href="${escapeHtml(ev.url)}" target="_blank" rel="noopener">Zum Eintrag</a></p>` : ""}</div></div></div>
          </div>
          ${img}
        </div>
      </div>`;
    startLineTickers(host);
  }

  loadEvents().then((events) => {
    renderTicker(events);
    if (page === "home") renderHome(events);
    if (page === "programm") renderProgramm(events);
    if (page === "event") renderEventDetail(events);
  });
})();

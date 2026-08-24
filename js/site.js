(() => {
  const root = document.documentElement.dataset.root || "";
  const page = document.documentElement.dataset.page || "";

  const MAIN = [
    ["Ausstellungen", `${root}ausstellungen/`],
    ["Programm", `${root}programm/`],
    ["Besucherinfos", `${root}besucherinfos/`],
    ["Journal", `${root}journal/`],
    ["Über uns", `${root}ueber-uns/`],
  ];
  const META = [
    ["Kontakt", `${root}kontakt/`],
    ["Raummiete", `${root}raummiete/`],
    ["Medien", `${root}medien/`],
    ["Jobs", `${root}ueber-uns/#jobs`],
    ["Unterstützen", `${root}unterstuetzen/`],
  ];

  function el(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }

  function chrome() {
    const header = el(`
      <header class="site-header">
        <div class="header-inner">
          <a class="logo" href="${root}">Museum Schaffen</a>
          <button class="menu-toggle" type="button" aria-label="Menu">
            <span></span><span></span><span></span>
          </button>
        </div>
      </header>`);
    const overlay = el(`
      <div class="menu-overlay" hidden>
        <nav>
          <div>${MAIN.map(([l, h]) => `<a href="${h}">${l}</a>`).join("")}</div>
          <div class="meta">${META.map(([l, h]) => `<a href="${h}">${l}</a>`).join("")}</div>
        </nav>
      </div>`);
    overlay.removeAttribute("hidden");
    const footer = el(`
      <footer class="site-footer">
        <div class="footer-grid">
          <div>
            <p>Öffnungszeiten<br>MI–SO 10–17 UHR</p>
            <p><a href="${root}besucherinfos/">Besucherinfos</a></p>
          </div>
          <div>
            <p>Museum Schaffen<br>Lagerplatz 9<br>8400 Winterthur</p>
            <p><a href="mailto:mail@museumschaffen.ch">Mail</a></p>
          </div>
          <div>
            <p>Eintritt<br>CHF 12 / CHF 9</p>
          </div>
          <div>
            <p>Folge uns auf<br>Instagram</p>
            <p><a href="https://www.instagram.com/museum_schaffen/" target="_blank" rel="noopener">@museum_schaffen</a></p>
          </div>
        </div>
        <div class="footer-ctas">
          <a href="${root}newsletter/">Newsletter</a>
          <a href="${root}unterstuetzen/">Unter-<br>stützen</a>
        </div>
        <div class="footer-bottom">
          <p>Ein Museum des <a href="${root}ueber-uns/#traegerschaft">Historischen Vereins Winterthur</a></p>
          <nav>
            <a href="${root}impressum/">Impressum</a>
            <a href="${root}datenschutz/">Datenschutz</a>
            <a href="${root}medien/">Medien</a>
            <a href="${root}ueber-uns/#jobs">Jobs</a>
          </nav>
        </div>
      </footer>`);
    const cookie = el(`
      <div class="cookie" hidden>
        <p>Mit der Nutzung unserer Dienste erklären Sie sich damit einverstanden, dass wir Cookies verwenden. <a href="${root}datenschutz/">Mehr Informationen</a></p>
        <button type="button">Akzeptieren</button>
      </div>`);

    const pageEl = document.getElementById("page");
    const ticker = document.getElementById("ticker");
    if (ticker) {
      ticker.after(header);
      header.after(overlay);
    } else {
      pageEl.prepend(overlay);
      pageEl.prepend(header);
    }
    pageEl.append(footer);
    document.body.append(cookie);

    const toggle = header.querySelector(".menu-toggle");
    toggle.addEventListener("click", () => {
      document.documentElement.classList.toggle("nav-open");
    });
    overlay.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => document.documentElement.classList.remove("nav-open"));
    });

    if (!localStorage.getItem("mus-cookie-ok")) {
      cookie.hidden = false;
      cookie.querySelector("button").addEventListener("click", () => {
        localStorage.setItem("mus-cookie-ok", "1");
        cookie.hidden = true;
      });
    }
  }

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

  function tagsFor(ev) {
    const map = {
      69: "Konzerte",
      70: "Fest",
      11: "Film",
      14: "Lesung",
      71: "Theater",
      72: "Tanz",
      13: "Ausstellung",
      217: "Vernissage",
      213: "Kinder",
      280: "Führungen",
      281: "Gespräche",
      15: "Highlights",
    };
    const out = [];
    if (map[ev.category]) out.push(map[ev.category]);
    const t = (ev.title || "").toLowerCase();
    if (t.includes("quiz") || t.includes("pims")) out.unshift("Fest");
    if (t.includes("käfele") || t.includes("kafele") || t.includes("afterwork")) out.unshift("Gespräche");
    if (t.includes("führung") || t.includes("fuehrung")) out.unshift("Führungen");
    return [...new Set(out)];
  }

  async function loadEvents() {
    const urls = [`${root}data/mus_export.json`];
    for (const url of urls) {
      try {
        const res = await fetch(url);
        if (res.ok) {
          const data = await res.json();
          return Array.isArray(data) ? data : data.events || [];
        }
      } catch (_) {
        /* try next */
      }
    }
    return [];
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

  function renderTicker(events) {
    const host = document.getElementById("ticker");
    if (!host) return;
    const next = upcoming(events)[0];
    if (!next) {
      host.remove();
      return;
    }
    const label = `${weekdayShort(next.date)} ${fmtDate(next.date)} ${next.title} +++ `;
    const doubled = (label + " ").repeat(6);
    host.innerHTML = `<a href="${eventHref(next)}">${doubled}${doubled}</a>`;
  }

  function renderHome(events) {
    const list = upcoming(events);
    const featured = document.getElementById("home-featured");
    const rest = document.getElementById("home-rest");
    if (!featured || !rest) return;
    const first = list[0];
    const more = list.slice(1, 7);
    if (first) {
      featured.innerHTML = `
        <a class="row-link" href="${eventHref(first)}">
          <div class="row-meta">
            <span class="date">${fmtDate(first.date)}</span>
            <span class="lineticker">${first.title}</span>
            <span class="date">${fmtDate(first.date)}</span>
          </div>
          ${first.image ? `<div class="row-image"><img src="${first.image}" alt=""></div>` : ""}
        </a>`;
    }
    rest.innerHTML = more
      .map(
        (ev) => `
        <a class="row-link" href="${eventHref(ev)}">
          <div class="row-meta">
            <span class="date">${fmtDate(ev.date)}</span>
            <span class="lineticker">${ev.title}</span>
          </div>
        </a>`
      )
      .join("");
  }

  function renderProgramm(events) {
    const host = document.getElementById("event-list");
    const filters = document.getElementById("event-filters");
    if (!host) return;
    const list = upcoming(events);
    const allTags = ["Alle", ...new Set(list.flatMap(tagsFor))];
    let active = "Alle";

    const paint = () => {
      const shown = list.filter((ev) => active === "Alle" || tagsFor(ev).includes(active));
      host.innerHTML = shown
        .map((ev) => {
          const t = tagsFor(ev);
          return `
            <a class="event-card" href="${eventHref(ev)}">
              <div class="when">
                <div>${fmtDate(ev.date)}</div>
                <div>${ev.time_start || ""}${ev.time_end ? "–" + ev.time_end : ""}</div>
                <p class="tags">${t.join(" ")}</p>
              </div>
              <div>
                <h2>${ev.title}</h2>
                ${ev.image ? `<img src="${ev.image}" alt="">` : ""}
              </div>
            </a>`;
        })
        .join("");
      if (filters) {
        filters.innerHTML = allTags
          .map((tag) => `<button type="button" data-tag="${tag}" class="${tag === active ? "is-on" : ""}">${tag}</button>`)
          .join("");
        filters.querySelectorAll("button").forEach((btn) => {
          btn.addEventListener("click", () => {
            active = btn.dataset.tag;
            paint();
          });
        });
      }
    };
    paint();
  }

  function renderEventDetail(events) {
    const host = document.getElementById("event-detail");
    if (!host) return;
    const id = new URLSearchParams(location.search).get("id");
    const ev = events.find((e) => String(e.reference) === String(id)) || upcoming(events)[0];
    if (!ev) {
      host.innerHTML = "<p>Keine Veranstaltung gefunden.</p>";
      return;
    }
    document.title = `${ev.title} — Museum Schaffen`;
    host.innerHTML = `
      <p class="page-title">${ev.title}</p>
      <div class="event-body">
        ${ev.image ? `<img class="hero" src="${ev.image}" alt="">` : ""}
        <p class="meta-line">${fmtDate(ev.date)} · ${ev.time_start || ""}${ev.time_end ? "–" + ev.time_end : ""} · ${ev.location_name || "Museum Schaffen"}</p>
        ${ev.description_html || `<p>${ev.description_long || ev.description || ""}</p>`}
        <p class="muted">${[ev.location_name, ev.location_street, ev.location_zip, ev.location_city].filter(Boolean).join(", ")}</p>
        <p>
          ${ev.url ? `<a class="btn" href="${ev.url}" target="_blank" rel="noopener">Zum Eintrag</a>` : ""}
          ${ev.presale && String(ev.presale).startsWith("http") && !String(ev.presale).includes("mail@") ? ` <a class="btn" href="${ev.presale}" target="_blank" rel="noopener">Tickets</a>` : ""}
        </p>
      </div>`;
  }

  chrome();

  loadEvents().then((events) => {
    renderTicker(events);
    if (page === "home") renderHome(events);
    if (page === "programm") renderProgramm(events);
    if (page === "event") renderEventDetail(events);
  });
})();

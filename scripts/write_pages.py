# -*- coding: utf-8 -*-
"""Clone museumschaffen.ch HTML/CSS, keep Eventfrog JSON for live events."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRAPE = ROOT / "_scrape"
ORIGIN = "https://www.museumschaffen.ch"

PAGES = [
    ("home.html", "index.html", "", "home", None),
    ("ausstellungen.html", "ausstellungen/index.html", "../", "ausstellungen", "ausstellungen/"),
    (
        "ausstellung-detail.html",
        "ausstellungen/erinnerungstank-haldengut.html",
        "../",
        "exhibition",
        "ausstellungen/",
    ),
    ("programm.html", "programm/index.html", "../", "programm", "programm/"),
    ("event-sample.html", "programm/event.html", "../", "event", "programm/"),
    ("besuch.html", "besucherinfos/index.html", "../", "besuch", "besucherinfos/"),
    ("journal.html", "journal/index.html", "../", "journal", "journal/"),
    ("journal-hesch.html", "journal/hesch-gwuesst.html", "../", "journal", "journal/"),
    ("journal-growing.html", "journal/growing-green.html", "../", "journal", "journal/"),
    ("ueber-uns.html", "ueber-uns/index.html", "../", "ueber-uns", "ueber-uns/"),
    ("kontakt.html", "kontakt/index.html", "../", "kontakt", "kontakt/"),
    ("raummiete.html", "raummiete/index.html", "../", "raummiete", "raummiete/"),
    ("medien.html", "medien/index.html", "../", "medien", "medien/"),
    ("unterstuetzen.html", "unterstuetzen/index.html", "../", "unterstuetzen", "unterstuetzen/"),
    ("newsletter.html", "newsletter/index.html", "../", "newsletter", "newsletter/"),
    ("impressum.html", "impressum/index.html", "../", "impressum", None),
    ("datenschutz.html", "datenschutz/index.html", "../", "datenschutz", None),
]


def empty_list_ul(html: str, list_id: str, ul_id: str) -> str:
    pattern = rf'(id="{list_id}"><ul)([^>]*)(>)(.*?)(</ul>)'

    def repl(m: re.Match) -> str:
        attrs = m.group(2)
        if f'id="{ul_id}"' not in attrs:
            attrs = f'{attrs} id="{ul_id}"'
        return f"{m.group(1)}{attrs}{m.group(3)}{m.group(5)}"

    out, n = re.subn(pattern, repl, html, count=1, flags=re.DOTALL)
    if n != 1:
        raise SystemExit(f"could not empty list {list_id}")
    return out


def activate_lazy(html: str) -> str:
    html = re.sub(
        r'(<source\b[^>]*?)\ssrcset="data:image/svg\+xml[^"]*"([^>]*?)\sdata-src="([^"]+)"',
        lambda m: f'{m.group(1)} srcset="{m.group(3).strip()}"{m.group(2)}',
        html,
    )
    html = re.sub(
        r'(<img\b[^>]*?)\ssrc="data:image/svg\+xml[^"]*"([^>]*?)\sdata-src="([^"]+)"',
        lambda m: f'{m.group(1)} src="{m.group(3)}"{m.group(2)}',
        html,
    )
    return html.replace(' class="wglLazyLoadInit"', "").replace(" class=\"wglLazyLoadInit\"", "")


def rewrite_paths(html: str, root: str) -> str:
    home = root if root else "./"
    local = [
        ("/de/ausstellungen/2026_erinnerungstank_haldengut.php", f"{root}ausstellungen/erinnerungstank-haldengut.html"),
        ("/de/journal/tanz-zu-heimweh-melancholie-weit-weg-2.php", f"{root}journal/hesch-gwuesst.html"),
        ("/de/journal/tanz-zu-heimweh-melancholie-weit-weg-1.php", f"{root}journal/growing-green.html"),
        ("/de/ausstellungen/", f"{root}ausstellungen/"),
        ("/de/programm/", f"{root}programm/"),
        ("/de/besucherinfos/", f"{root}besucherinfos/"),
        ("/de/journal/", f"{root}journal/"),
        ("/de/ueber-uns/", f"{root}ueber-uns/"),
        ("/de/kontakt/", f"{root}kontakt/"),
        ("/de/raummiete/", f"{root}raummiete/"),
        ("/de/medien/", f"{root}medien/"),
        ("/de/unterstuetzen/", f"{root}unterstuetzen/"),
        ("/de/newsletter/", f"{root}newsletter/"),
        ("/de/impressum/", f"{root}impressum/"),
        ("/de/datenschutz/", f"{root}datenschutz/"),
        ("/de/datenschutz", f"{root}datenschutz/"),
        ("https://www.museumschaffen.ch/de/unterstuetzen/", f"{root}unterstuetzen/"),
        ("/de/", home),
    ]
    for src, dst in local:
        html = html.replace(f'href="{src}', f'href="{dst}')
        html = html.replace(f"href='{src}'", f"href='{dst}'")
        html = html.replace(f'data-url="{src}', f'data-url="{dst}')
    html = re.sub(
        r'(href|data-url)="(/de/(?:programm|journal|ausstellungen)/[^"]+\.php[^"]*)"',
        lambda m: f'{m.group(1)}="{ORIGIN}{m.group(2)}"',
        html,
    )
    for prefix in ("href", "src", "data-src", "action", "content"):
        html = html.replace(f'{prefix}="/wAssets/', f'{prefix}="{ORIGIN}/wAssets/')
        html = html.replace(f"{prefix}='/wAssets/", f"{prefix}='{ORIGIN}/wAssets/")
        html = html.replace(f'{prefix}="/weblication/', f'{prefix}="{ORIGIN}/weblication/')
        html = html.replace(f'{prefix}="/wGlobal/', f'{prefix}="{ORIGIN}/wGlobal/')
    html = html.replace('srcset="/wAssets/', f'srcset="{ORIGIN}/wAssets/')
    html = html.replace(', /wAssets/', f', {ORIGIN}/wAssets/')
    html = html.replace('url(/wAssets/', f'url({ORIGIN}/wAssets/')
    html = html.replace('url(/wGlobal/', f'url({ORIGIN}/wGlobal/')
    html = html.replace('href="//webfonts3.', 'href="https://webfonts3.')
    return html


def strip_scripts(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", "", html)
    html = re.sub(
        r'(id="cookieNoticeCloser")([^>]*) onclick="[^"]*"',
        r"\1\2",
        html,
    )
    return html


def set_selected(html: str, root: str, selected: str | None) -> str:
    html = html.replace('class="selected "', 'class="default "')
    if not selected:
        return html
    needle = f'<li class="default "><a href="{root}{selected}"'
    repl = f'<li class="selected "><a href="{root}{selected}"'
    return html.replace(needle, repl, 1)


def transform(html: str, root: str, page: str, selected: str | None) -> str:
    html = re.sub(
        r"<html[^>]*>",
        (
            '<html lang="de" class="js pagestatus-loaded no-weditor scrolled-top '
            'page_var1 object-start project-de subdir-de navId-wNoNavpoint" '
            f'data-root="{root}" data-page="{page}">'
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'<link href="//webfonts3\.radimpesko\.com/[^"]+" rel="stylesheet">\s*',
        "",
        html,
    )
    html = re.sub(
        r'<link rel="stylesheet" href="/wGlobal/wGlobal/layout/styles/optimized/design_[^"]+"\s*/>',
        (
            f'<link rel="stylesheet" href="{root}wGlobal/wGlobal/layout/styles/optimized/design.css"/>'
            f'<link rel="stylesheet" href="{root}css/mus-overrides.css"/>'
        ),
        html,
    )
    if page == "home":
        html = empty_list_ul(html, "list_ac8a2e18", "mus-ticker")
        html = empty_list_ul(html, "list_0bcce8b8", "mus-home-featured")
        html = empty_list_ul(html, "list_646165ae", "mus-home-rest")
    if page == "programm":
        html = empty_list_ul(html, "list_27d85760", "mus-event-list")
        html = empty_list_ul(html, "list_9a9b555d", "mus-event-agenda")
        html = html.replace(
            'id="filterElement-categories"',
            'id="filterElement-categories" data-mus-filters="1"',
        )
        html = re.sub(r' onclick="adaptFilter_sab6be7\(this\);"', "", html)
    if page == "event":
        html = re.sub(
            r'(id="blockContentInner">)<!--CONTENT:START-->.*?<!--CONTENT:STOP-->',
            r'\1<!--CONTENT:START--><div id="mus-event-detail"></div><!--CONTENT:STOP-->',
            html,
            count=1,
            flags=re.DOTALL,
        )

    html = strip_scripts(html)
    html = rewrite_paths(html, root)
    html = activate_lazy(html)
    html = set_selected(html, root, selected)

    back = (
        '<div class="elementLink elementLinkBack">'
        '<a href="javascript:history.back()" class="back">zurück</a></div>'
    )
    html = html.replace(
        '<div style="position:absolute;right:0;top:2px"></div>',
        f'<div style="position:absolute;right:0;top:2px">{back}</div>',
    )
    html = html.replace("</body>", f'<script src="{root}js/site.js?v=20260901" defer></script></body>')
    return html


def main() -> None:
    if not SCRAPE.exists():
        raise SystemExit(f"missing scrape dir: {SCRAPE}")
    for src_name, dest_rel, root, page, selected in PAGES:
        src = SCRAPE / src_name
        if not src.exists():
            raise SystemExit(f"missing scrape file: {src}")
        html = transform(src.read_text(encoding="utf-8"), root, page, selected)
        dest = ROOT / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print("wrote", dest_rel, len(html))


if __name__ == "__main__":
    main()

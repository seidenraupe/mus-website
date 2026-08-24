"""
Eventfrog → data/mus_export.json (Museum Schaffen, OrgID 5116588)
================================================================

Gleicher Coucou-Record wie prototype-hvw-website/cronjobs/eventfrog_to_mus.py.
Für GitHub Actions ist scripts/fetch-mus-events.mjs die bevorzugte Variante.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    sys.stderr.write("pip install requests\n")
    raise

ORG_IDS = ["5116588"]
API_BASE = "https://api.eventfrog.net"
PREFERRED = ["de", "de_CH", "en", "fr", "it"]
RUBRIC_TO_COUCOU = [
    ("konzert", 69),
    ("party", 70),
    ("film", 11),
    ("literatur", 14),
    ("theater", 71),
    ("tanz", 72),
    ("ausstellung", 13),
    ("vernissage", 217),
    ("kinder", 213),
    ("führung", 280),
    ("fuehrung", 280),
    ("vortrag", 281),
]
DEFAULT_CATEGORY = 15
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "mus_export.json"


def load_key() -> str:
    env = os.environ.get("EVENTFROG_API_KEY", "").strip()
    if env:
        return env
    keyfile = Path(__file__).with_name("eventfrog_api_key")
    if keyfile.exists():
        for line in keyfile.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                _, value = line.split("=", 1)
                return value.strip().strip('"').strip("'")
            return line
    raise SystemExit("EVENTFROG_API_KEY fehlt (Env oder cronjobs/eventfrog_api_key).")


def pick_lang(value):
    if not value:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for lang in PREFERRED:
            if value.get(lang):
                return value[lang]
        for text in value.values():
            if text:
                return text
    return None


def strip_html(html):
    if not html:
        return None
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip() or None


def date_str(iso):
    if not iso:
        return None
    s = str(iso)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.strftime("%Y/%m/%d")
    except ValueError:
        if len(s) >= 10 and s[4] == "-" and s[7] == "-":
            return s[0:4] + "/" + s[5:7] + "/" + s[8:10]
    return None


def time_str(iso):
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except ValueError:
        return None


def api_get(path, params, key):
    r = requests.get(
        API_BASE + path,
        params=params,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def map_category(rubric_id, rubrics):
    title = (pick_lang((rubrics.get(rubric_id) or {}).get("title")) or "").lower()
    for keyword, cid in RUBRIC_TO_COUCOU:
        if keyword in title:
            return cid
    return DEFAULT_CATEGORY


def main():
    key = load_key()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    events = []
    page = 1
    while True:
        data = api_get(
            "/public/v1/events",
            {"orgId": ORG_IDS, "perPage": 100, "page": page, "from": today, "country": "CH"},
            key,
        )
        batch = data.get("events") or []
        events.extend(batch)
        if not batch or len(events) >= data.get("totalNumberOfResources", len(batch)):
            break
        page += 1

    loc_ids = sorted({lid for ev in events for lid in (ev.get("locationIds") or [])})
    locations = {}
    if loc_ids:
        for loc in api_get("/public/v1/locations", {"id": loc_ids}, key).get("locations") or []:
            locations[loc["id"]] = loc
    rubrics = {}
    try:
        for rub in api_get("/public/v1/rubrics", {}, key).get("rubrics") or []:
            rubrics[rub["id"]] = rub
    except requests.RequestException:
        pass

    export = []
    for ev in sorted(events, key=lambda e: e.get("begin") or ""):
        html = pick_lang(ev.get("descriptionAsHTML"))
        long_text = strip_html(html)
        loc = locations.get((ev.get("locationIds") or [None])[0])
        image = None
        emblem = ev.get("emblemToShow")
        if isinstance(emblem, dict):
            image = emblem.get("url")
        date = date_str(ev.get("begin"))
        date_end = date_str(ev.get("end"))
        rec = {
            "reference": str(ev.get("id") or ""),
            "title": pick_lang(ev.get("title")),
            "description": pick_lang(ev.get("shortDescription")) or long_text,
            "image": image,
            "url": ev.get("url"),
            "date": date,
            "time_start": time_str(ev.get("begin")),
            "time_end": time_str(ev.get("end")),
            "fee": ev.get("lowestTicketPrice"),
            "presale": ev.get("presaleLink"),
            "category": map_category(ev.get("rubricId"), rubrics),
            "description_long": long_text,
            "description_html": html,
        }
        if date_end and date_end != date:
            rec["date_end"] = date_end
        if loc:
            rec["location_name"] = pick_lang(loc.get("title"))
            rec["location_street"] = loc.get("addressLine")
            rec["location_zip"] = loc.get("zip")
            rec["location_city"] = loc.get("city")
            rec["location_website"] = loc.get("websiteUrl")
        export.append({k: v for k, v in rec.items() if v not in (None, "", [])})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(export, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(export)} events to {OUTPUT}")


if __name__ == "__main__":
    main()
